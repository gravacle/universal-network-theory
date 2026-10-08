"""Exact H^0..H^3 coefficients for three frozen active-record arms."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE=Path(__file__).resolve().parent
NOTE=HERE/"NATIVE_ACTIVE_RECORD_DRESSED_TRANSPORT_V001.md"
PIN="a507265b9f69849291650c415c56c62fa37f60e07f858db3a6a8ca289505b5fa"
OUT=HERE/"native_active_record_transport_onset_v001_results.json"
EDGES=((0,2),(0,3),(1,2),(1,3))
ARMS=("carrier_copy_off","uniform_carrier_copy","origin_only_carrier_copy")


def add(out,key,value):
    out[key]=out.get(key,F(0))+value


def action(vec,arm):
    out={}
    for (graph,carrier,records),amp in vec.items():
        degrees=[0]*4
        for e,(u,v) in enumerate(EDGES):
            if graph>>e&1:
                degrees[u]+=1
                degrees[v]+=1
        diag=F(4*graph.bit_count()+sum((d-1)**2 for d in degrees)+1)
        diag+=F(degrees[carrier],4)
        diag+=sum((F(1)-F(degrees[v],2)) for v in range(4) if records>>v&1)
        add(out,(graph,carrier,records),diag*amp)
        for e,(u,v) in enumerate(EDGES):
            add(out,(graph^(1<<e),carrier,records),-amp/2)
            if graph>>e&1 and carrier in (u,v):
                target=v if carrier==u else u
                add(out,(graph,target,records),-amp/2)
        for v in range(4):
            copying=(carrier==v and (arm=="uniform_carrier_copy" or
                                     (arm=="origin_only_carrier_copy" and v==0)))
            add(out,(graph,carrier,records^(1<<v)),amp*(1+int(copying)))
    return {k:v for k,v in out.items() if v}


def clock_action(vec,site):
    out={}
    for (graph,carrier,records),amp in vec.items():
        factor=F(1 if not (records>>site&1) else -1,2)
        add(out,(graph,carrier,records),amp*factor)
        add(out,(graph,carrier,records^(1<<site)),amp*factor)
    return {k:v for k,v in out.items() if v}


def dot(a,b,target=None):
    return sum((v*b.get(k,F(0)) for k,v in a.items()
                if target is None or k[1]==target),F(0))


def literal(x):
    return dict(exact=str(x),display=float(x))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",action="store_true",required=True)
    parser.parse_args()
    start=time.monotonic()
    if OUT.exists():
        raise FileExistsError("Preserve completed results; no replay.")
    if hashlib.sha256(NOTE.read_bytes()).hexdigest()!=PIN:
        raise ValueError("Frozen mathematical input differs.")
    checks=[]
    def check(name,actual,expected):
        checks.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
    raw={}
    for arm in ARMS:
        vectors=[{(15,0,0):F(1)}]
        for k in range(3):
            vectors.append(action(vectors[-1],arm))
        check(arm+" initial energy",dot(vectors[0],vectors[1]),F(43,2))
        variance=dot(vectors[1],vectors[1])-F(43,2)**2
        check(arm+" initial variance",variance,F(11 if arm==ARMS[0] else 17,2))
        for a in range(3):
            for b in range(3):
                check(f"{arm} Hermitian moments {a},{b}",
                      dot(vectors[a],vectors[b+1]),dot(vectors[a+1],vectors[b]))
        arrivals={}
        for target in (2,3):
            p2=dot(vectors[1],vectors[1],target)
            p4=dot(vectors[2],vectors[2],target)/4-dot(vectors[1],vectors[3],target)/3
            check(f"{arm} target{target} initial transfer",p2,F(1,4))
            arrivals[target]=(p2,p4)
        clocks={}
        for site in range(4):
            comm=[]
            for k in range(4):
                comm.append(sum(((-1)**j*math.comb(k,j)*
                                 dot(vectors[k-j],clock_action(vectors[j],site))
                                 for j in range(k+1)),F(0)))
            b,c1,c2,c3=comm
            nu=c1/b
            a3=-c3/(6*b)+c1*c2/(2*b*b)-c1**3/(3*b**3)
            check(f"{arm} clock{site} amplitude",b,F(1,2))
            clocks[site]=dict(commutator_expectations=comm,nu0=nu,phase_cubic=a3)
        raw[arm]=dict(support_sizes=[len(v) for v in vectors],arrivals=arrivals,clocks=clocks)
    baseline=raw[ARMS[0]]
    contrasts=[]
    for arm,expected in ((ARMS[1],F(-1,24)),(ARMS[2],F(-1,48))):
        for target in (2,3):
            delta=raw[arm]["arrivals"][target][1]-baseline["arrivals"][target][1]
            check(f"{arm} target{target} quartic contrast",delta,expected)
            phase_rows=[]
            for site in range(4):
                c=raw[arm]["clocks"][site]
                c0=baseline["clocks"][site]
                if c["nu0"]==c0["nu0"] and c["nu0"]:
                    nu=c["nu0"]
                    clock_correction=-2*F(1,4)*(c["phase_cubic"]-c0["phase_cubic"])/nu**5
                    phase_rows.append(dict(clock_site=site,same_initial_rate=True,
                                           generator_term=literal(delta/nu**4),
                                           clock_correction=literal(clock_correction),
                                           total_phase_quartic_contrast=literal(delta/nu**4+clock_correction)))
                else:
                    phase_rows.append(dict(clock_site=site,same_initial_rate=False,
                                           qualification="Leading phase-domain transfer differs; do not use equal-rate contrast"))
            contrasts.append(dict(arm=arm,target=target,generator_quartic_contrast=literal(delta),
                                  reference_clock_comparisons=phase_rows))
        for k in range(4):
            check(f"{arm} remoteclock derivative{k}",raw[arm]["clocks"][1]["commutator_expectations"][k],
                  baseline["clocks"][1]["commutator_expectations"][k])
    rows=[]
    for arm in ARMS:
        a=raw[arm]
        rows.append(dict(arm=arm,support_sizes=a["support_sizes"],
                         arrivals=[dict(target=t,quadratic=literal(c[0]),quartic=literal(c[1]))
                                   for t,c in a["arrivals"].items()],
                         clocks=[dict(site=s,commutator_expectations=[str(v) for v in c["commutator_expectations"]],
                                      nu0=literal(c["nu0"]),phase_cubic=literal(c["phase_cubic"]))
                                 for s,c in a["clocks"].items()]))
    passed=all(c["passed"] for c in checks)
    result=dict(status="COMPLETE" if passed else "EXACT_CHECK_FAILURE",input_sha256=PIN,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                units="x=tau/hbar",scope="Exact low-order coefficients; not a propagated history",
                rows=rows,contrasts=contrasts,checks=checks,
                check_counts=dict(passed=sum(c["passed"] for c in checks),total=len(checks)),
                qualifications=["Supported blank-record preparation, not lower-band ground state",
                                "Local onset only; no all-time, physical gravity or expansion inference",
                                "No temperature, distance or SI clock calibration"],
                runtime=dict(wall_seconds=time.monotonic()-start,
                             peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    payload=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
    with tempfile.NamedTemporaryFile(mode="w",dir=HERE,prefix=".active-record-onset-",delete=False) as f:
        temporary=Path(f.name)
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary,OUT)
    finally:
        temporary.unlink()
    print(json.dumps(dict(status=result["status"],check_counts=result["check_counts"],
                          rows=rows,contrasts=contrasts,runtime=result["runtime"]),indent=2))
    if not passed:
        raise SystemExit(1)


if __name__=="__main__":
    main()
