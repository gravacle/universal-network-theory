"""Eight frozen exact sixth-order transport-plus-clock coefficient cases."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE=Path(__file__).resolve().parent
PINS={
    "NATIVE_ACTIVE_RECORD_DENSITY_RESPONSE_V001.md":"26c6197b965d3a1e59833d28c35f1a69c4d17f9f30522f1c7bee9ed28f28623c",
    "native_active_record_transport_onset_v001.py":"6cef7370e4a2d3c53f56006dbd713e43c4e13ce31f120b3665e43f1800d990d3",
    "native_active_record_transport_onset_v001_results.json":"7dd5e9f265029226403be69db392ff60a26139d620cf63ee52dc2324c78cde5b",
}
OUT=HERE/"native_active_record_density_response_v001_results.json"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",action="store_true",required=True)
    parser.parse_args()
    start=time.monotonic()
    if OUT.exists():
        raise FileExistsError("No overwrite or completed replay.")
    for name,pin in PINS.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=pin:
            raise ValueError("Input changed: "+name)
    spec=importlib.util.spec_from_file_location("owned_active_onset",HERE/"native_active_record_transport_onset_v001.py")
    base=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)  # Definitions only; its main is not executed.
    old=json.loads((HERE/"native_active_record_transport_onset_v001_results.json").read_text())
    old_rows={r["arm"]:r for r in old["rows"]}
    checks=[]
    def check(name,got,want):
        checks.append(dict(name=name,got=str(got),want=str(want),passed=got==want))
    def guard():
        if time.monotonic()-start>120 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>268435456:
            raise RuntimeError("Frozen resource ceiling exceeded; retain this failed attempt, do not expand scope.")
    def action(vec,arm,feedback):
        out=base.action(vec,arm)
        if not feedback:
            for (graph,carrier,records),amp in vec.items():
                debt=0
                for e,(u,v) in enumerate(base.EDGES):
                    if graph>>e&1:
                        debt+=(records>>u&1)+(records>>v&1)
                base.add(out,(graph,carrier,records),F(debt,2)*amp)
        return {k:v for k,v in out.items() if v}
    raw={}
    for graph in (13,15):
        for feedback in (True,False):
            for copy in (False,True):
                arm=base.ARMS[1] if copy else base.ARMS[0]
                label=f"G{graph}_feedback{int(feedback)}_copy{int(copy)}"
                vectors=[{(graph,0,0):F(1)}]
                for k in range(5):
                    guard()
                    vectors.append(action(vectors[-1],arm,feedback))
                energy=base.dot(vectors[0],vectors[1])
                check(label+" energy",energy,F(61,4) if graph==13 else F(43,2))
                for a in range(5):
                    for b in range(5):
                        check(f"{label} Hermitian {a},{b}",base.dot(vectors[a],vectors[b+1]),
                              base.dot(vectors[a+1],vectors[b]))
                p2=base.dot(vectors[1],vectors[1],2)
                p4=base.dot(vectors[2],vectors[2],2)/4-base.dot(vectors[1],vectors[3],2)/3
                p6=base.dot(vectors[3],vectors[3],2)/36+base.dot(vectors[1],vectors[5],2)/60-base.dot(vectors[2],vectors[4],2)/24
                comm=[sum(((-1)**j*math.comb(k,j)*
                           base.dot(vectors[k-j],base.clock_action(vectors[j],1))
                           for j in range(k+1)),F(0)) for k in range(6)]
                series=[comm[k]/(math.factorial(k)*comm[0]) for k in range(6)]
                log=[F(0)]*6
                for k in range(1,6):
                    log[k]=series[k]-sum((j*log[j]*series[k-j] for j in range(1,k)),F(0))/k
                nu,a3,a5=log[1],-log[3],log[5]
                check(label+" P2",p2,F(1,4))
                check(label+" beta0",comm[0],F(1,2))
                check(label+" nu0",nu,F(2))
                if not feedback and not copy:
                    check(label+" factorized clock cubic",a3,F(-1,3))
                    check(label+" factorized clock fifth",a5,F(29,60))
                if graph==15 and feedback:
                    prior=old_rows[arm]
                    check(label+" saved P2",p2,F(prior["arrivals"][0]["quadratic"]["exact"]))
                    check(label+" saved P4",p4,F(prior["arrivals"][0]["quartic"]["exact"]))
                    for k in range(4):
                        check(label+f" saved clock{k}",comm[k],F(prior["clocks"][1]["commutator_expectations"][k]))
                k6_terms=dict(transport=p6/nu**6,
                              quartic_clock=-4*p4*a3/nu**7,
                              quadratic_clock=p2*(7*a3*a3/nu**8-2*a5/nu**7))
                raw[(graph,feedback,copy)]=dict(label=label,initial_energy=energy,
                    graph=graph,feedback=feedback,copy=copy,
                    support_sizes=[len(v) for v in vectors],commutators=comm,
                    nu=nu,a3=a3,a5=a5,P2=p2,P4=p4,P6=p6,
                    K2=p2/nu**2,K4=p4/nu**4-2*p2*a3/nu**5,
                    K6=sum(k6_terms.values(),F(0)),K6_terms=k6_terms)
    fields=("P2","P4","P6","K2","K4","K6")
    contrasts={}
    for graph in (13,15):
        for feedback in (True,False):
            on,off=raw[(graph,feedback,True)],raw[(graph,feedback,False)]
            c={f:on[f]-off[f] for f in fields}
            c["K6_terms"]={f:on["K6_terms"][f]-off["K6_terms"][f] for f in on["K6_terms"]}
            contrasts[(graph,feedback)]=c
            check(f"G{graph} feedback{feedback} P4 copy contrast",c["P4"],F(-1,24))
            check(f"G{graph} feedback{feedback} K4 copy contrast",c["K4"],F(-1,384))
    graph_contrasts={}
    for feedback in (True,False):
        a,b=contrasts[(15,feedback)],contrasts[(13,feedback)]
        c={f:a[f]-b[f] for f in fields}
        c["K6_terms"]={f:a["K6_terms"][f]-b["K6_terms"][f] for f in a["K6_terms"]}
        graph_contrasts[feedback]=c
    triple={f:graph_contrasts[True][f]-graph_contrasts[False][f] for f in fields}
    triple["K6_terms"]={f:graph_contrasts[True]["K6_terms"][f]-graph_contrasts[False]["K6_terms"][f]
                        for f in graph_contrasts[True]["K6_terms"]}
    def encode(value):
        if isinstance(value,F):
            return base.literal(value)
        if isinstance(value,dict):
            return {str(k):encode(v) for k,v in value.items()}
        if isinstance(value,(list,tuple)):
            return [encode(v) for v in value]
        return value
    guard()
    passed=all(c["passed"] for c in checks)
    result=dict(status="COMPLETE" if passed else "EXACT_CHECK_FAILURE",input_sha256=PINS,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        units="x=tau/hbar",scope="Exact onset coefficients, no history propagation",
        rows=encode(list(raw.values())),copy_contrasts=encode(contrasts),
        graph_contrasts=encode(graph_contrasts),three_factor_contrast=encode(triple),checks=checks,
        check_counts=dict(passed=sum(c["passed"] for c in checks),total=len(checks)),
        qualifications=["Graph degree/connectivity, not measured spatial density",
                        "Different complete preparation energies retained",
                        "Relational interaction includes clock conversion products",
                        "Local Taylor coefficients, not whole-window gravity or expansion"],
        runtime=dict(wall_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    payload=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
    with tempfile.NamedTemporaryFile(mode="w",dir=HERE,prefix=".record-density-",delete=False) as f:
        temporary=Path(f.name)
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary,OUT)
    finally:
        temporary.unlink()
    print(json.dumps({k:result[k] for k in ("status","check_counts","rows","copy_contrasts","graph_contrasts","three_factor_contrast","runtime")},indent=2))
    if not passed:
        raise SystemExit(1)


if __name__=="__main__":
    main()
