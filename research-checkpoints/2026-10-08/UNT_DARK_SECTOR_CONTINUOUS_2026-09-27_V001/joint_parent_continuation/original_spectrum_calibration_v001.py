"""Inert shared-scale elimination; stdout-only freeze/run, no formation or fit."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.resolve()
FREEZE = HERE/"ORIGINAL_SPECTRUM_CALIBRATION_V001_FROZEN.json"
RETURN = HERE/"PREPARED_ACTION_RETURN_V001_RESULTS.json"
RETURN_FREEZE = HERE/"PREPARED_ACTION_RETURN_V001_FROZEN.json"
HISTORY = HERE/"COMMON_HISTORY_MECHANISM_V001_RESULTS.json"
HISTORY_FREEZE = HERE/"COMMON_HISTORY_MECHANISM_V001_FROZEN.json"
REFERENCE = HERE/"COSMOLOGY_CLOSURE_ARITHMETIC.json"
PINS = {
    RETURN.name: "b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678",
    RETURN_FREEZE.name: "231053248cd6ed2922bb35dd055f9d70bb0c8a2bc583a8202da50bbfe830089d",
    HISTORY.name: "e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a",
    HISTORY_FREEZE.name: "13d05e24680166cb903e02fb961717a2bef1a89771a1d76c80156ab50cbe76ef",
    REFERENCE.name: "258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153",
}
CONFIG = dict(expected_templates=36, expected_references=18, expected_rows=648,
              scale_bisections=80, modal_bisections=80, max_bracket_doublings=128,
              relative_tolerance=2e-11, output_limit_bytes=1048576,
              c_m_s=299792458., mpc_km=3.085677581491367e19,
              gaps=(.001,.002), durations=(8,16), amplitudes=(.0025,.01,.04),
              resolution=((64,.01),(128,.01),(128,.005)))
SOURCES = ("original_spectrum_calibration_v001.py",
           "ORIGINAL_SPECTRUM_CALIBRATION_PROTOCOL_V001.md",
           "ORIGINAL_SPECTRUM_SHARED_CALIBRATION_V001.md",
           "SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md",
           "COSMOLOGY_CLOSURE_TEST_V001.md")


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",",":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def owned(path):
    path = path.resolve()
    path.relative_to(PROJECT)
    return path


def sha(path):
    return hashlib.sha256(owned(path).read_bytes()).hexdigest()


def authenticate():
    files, visited = {}, set()

    def remember(path, expected=None):
        path = owned(path)
        actual = sha(path)
        if expected is not None and actual != expected:
            raise RuntimeError("Inherited source bytes differ: "+str(path))
        files[str(path.relative_to(PROJECT))] = actual
        return path

    def visit(path):
        path = remember(path)
        if path in visited:
            return
        visited.add(path)
        for name, expected in json.loads(path.read_text())["files"].items():
            member = remember(Path(name) if Path(name).is_absolute() else path.parent/name,
                              expected)
            if member.name.endswith("FROZEN.json"):
                visit(member)

    for name, expected in PINS.items():
        remember(HERE/name, expected)
    visit(RETURN_FREEZE)
    visit(HISTORY_FREEZE)

    def wrapper(path, freeze):
        data = json.loads(path.read_text())
        if (data["freeze_sha256"] != sha(freeze)
                or data["payload_sha256"] != digest(data["payload"])
                or not all(data["payload"]["checks"].values())):
            raise RuntimeError("Unqualified or altered inherited result: "+path.name)
        return data["payload"]

    returned, history = wrapper(RETURN, RETURN_FREEZE), wrapper(HISTORY, HISTORY_FREEZE)
    references = json.loads(REFERENCE.read_text())
    if references["status"] != "AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC":
        raise RuntimeError("Unexpected cosmological reference status")
    remember(HERE/"cosmology_closure_arithmetic.py", references["script_sha256"])
    for name, expected in references["input_sha256"].items():
        member = remember(HERE.parent/name, expected)
        if member.name.endswith("FROZEN.json"):
            visit(member)
    for name in SOURCES:
        remember(HERE/name)
    snapshot = dict(files=files, configuration=CONFIG,
                    role="Same original-spectrum excitation and vacuum calibration; no fit")
    return returned, history, references, snapshot


def equilibrium(delta, source):
    return 2*delta/math.sqrt(3)*np.sinh(
        np.arcsinh(3*math.sqrt(3)*source/(2*delta**2))/3)


def modal_bisection(delta, source):
    low = np.zeros_like(delta)
    high = np.minimum(source/delta, np.cbrt(delta*source))
    for _ in range(CONFIG["modal_bisections"]):
        middle = (low+high)/2
        below = middle*(delta**2+middle**2) < delta*source
        low = np.where(below,middle,low)
        high = np.where(below,high,middle)
    return (low+high)/2


def endpoint(delta, weights, source):
    y = equilibrium(delta,source)
    return float(np.dot(weights,.5*delta**2*y**2+.75*y**4)), y


def solve_endpoint(delta, weights, target):
    i0 = float(np.sum(weights))
    low, high = 0., math.sqrt(2*target/i0)
    count = 0
    while endpoint(delta,weights,high)[0] < target:
        high *= 2
        count += 1
        if count > CONFIG["max_bracket_doublings"]:
            raise RuntimeError("Endpoint bracket algorithm guard")
    for _ in range(CONFIG["scale_bisections"]):
        middle = (low+high)/2
        if endpoint(delta,weights,middle)[0] < target:
            low = middle
        else:
            high = middle
    source = (low+high)/2
    q, y = endpoint(delta,weights,source)
    return source, q, y, (high-low)/source, count


def run(returned, history, references):
    start = time.perf_counter()
    tol = CONFIG["relative_tolerance"]
    gates, spectra, templates, refs, rows = [], [], [], [], []
    worst = {}

    def check(name, error, limit=tol):
        error = float(error)
        worst[name] = max(worst.get(name,0.),error)
        gates.append((name,bool(math.isfinite(error) and error <= limit)))

    expected = {(gap,order,dt,duration,g)
                for gap in CONFIG["gaps"] for order,dt in CONFIG["resolution"]
                for duration in CONFIG["durations"] for g in CONFIG["amplitudes"]}
    identity = lambda row: (row["gap"],row["mode_order"],row["dt"],row["duration"],row["g"])
    if (len(returned["rows"]) != 36
            or {identity(row) for row in returned["rows"]} != expected
            or len(references["rows"]) != 18):
        raise RuntimeError("Inherited complete census differs")
    cases = {(c["gap"],c["order"],c["dt"],c["duration"]):c for c in history["cases"]}
    for index, row in enumerate(returned["rows"]):
        key = identity(row)
        case = cases[key[:4]]
        delta, weights = np.array(case["delta"],float), np.array(case["weights"],float)
        modes = row["mode_data"]
        if (len(delta) != row["mode_order"] or len(weights) != len(delta)
                or not np.all(delta>0) or not np.all(weights>0)
                or not all(row["checks"].values())):
            raise RuntimeError("Unqualified or inconsistent inherited template")
        energy, pressure = float(row["return_energy"]), float(row["return_pressure"])
        i0, eps = float(np.sum(weights)), row["gap"]
        check("finite_weight_normalization",abs(i0/((1-eps**2)/2)-1))
        for label, array, total in (
                ("saved_energy",modes["zero_source_energy"],energy),
                ("saved_pressure",modes["zero_source_pressure"],pressure),
                ("saved_action",modes["action"],row["prepared_action_sum"])):
            actual = float(np.dot(weights,np.array(array,float)))
            check(label,abs(actual-total)/max(abs(total),1e-300))
        if energy > 0:
            check("saved_pressure_ratio",abs(pressure/energy-row["return_w"])
                  /max(abs(row["return_w"]),1e-300))
        spectra.append((delta,weights))
        templates.append(dict(template=index,gap=eps,mode_order=len(delta),dt=row["dt"],
            duration=row["duration"],prepared_source=row["g"],energy=energy,pressure=pressure,
            pressure_over_energy=row["return_w"],I0=i0,
            actions_sha256=digest(modes["action"]),
            spectrum_sha256=digest(dict(delta=case["delta"],weights=case["weights"])),
            complete_cycle_work=row["complete_cycle_work"]))
    for index, row in enumerate(references["rows"]):
        source = row["reference_input"]
        h0, ol = source["H0_km_s_Mpc"], source["Omega_Lambda_ref"]
        ob = row["bbn"]["omega_b"]/(h0/100)**2
        oe = 1-ol-ob
        check("reference_missing_fraction",abs(oe-row["reference_H0_missing_Omega"])
              /max(abs(oe),1e-300))
        refs.append(dict(reference=index,reference_case=row["reference_case"],
            inherited_reference_input=source,bbn=row["bbn"],
            H0_s_inverse=h0/CONFIG["mpc_km"],Omega_b=ob,Omega_exc=oe,Omega_Lambda=ol))
    for template, (delta,weights) in zip(templates,spectra):
        e,p,i0,eps = (template[k] for k in ("energy","pressure","I0","gap"))
        for ref in refs:
            oe,ol,h0 = (ref[k] for k in ("Omega_exc","Omega_Lambda","H0_s_inverse"))
            result = dict(template=template["template"],reference=ref["reference"])
            if min(e,oe,ol,h0) <= 0:
                result.update(status="NONPOSITIVE_DOMAIN",E=e,Omega_exc=oe,Omega_Lambda=ol)
                rows.append(result)
                continue
            target = e*ol/oe
            source,q,y,width,doublings = solve_endpoint(delta,weights,target)
            y2 = modal_bisection(delta,source)
            q2 = float(np.dot(weights,.5*delta**2*y2**2+.75*y2**4))
            wel = float(np.dot(weights,.5*(source-delta*y)**2+.25*y**4))
            base = .5*i0*source**2
            d = wel/base
            trial = float(np.dot(weights,np.minimum(.5*source**2,
                                                    source**4/(4*delta**4))))/base
            gradient = float(np.dot(weights,delta*y))
            ch = CONFIG["c_m_s"]*h0
            gstar = ch*math.sqrt(3*i0*oe/(2*e))
            gs = gstar*source
            gslow = ch*math.sqrt(3*ol)
            reconstructed = (2*gstar*gstar*e/(3*i0*ch*ch),
                             2*gstar*gstar*q/(3*i0*ch*ch))
            numerical = dict(root=abs(q/target-1),bracket=width,
                modal_oracle=abs(q2/q-1),
                modal_root=float(np.max(np.abs(y-y2)/y2)),
                cubic=float(np.max(np.abs(y*(delta**2+y**2)/(delta*source)-1))),
                contact=abs((q+wel)/base-1),
                density_exc=abs(reconstructed[0]/oe-1),
                density_vac=abs(reconstructed[1]/ol-1),
                gs_identity=abs(gs*math.sqrt(1-d)/gslow-1),
                trial_violation=max(0.,d-trial))
            for name,error in numerical.items():
                check(name,error)
            check("positive_endpoint",0. if 0 <= d < 1 and gradient>0 and q>0 else 1.)
            a0 = 16*i0/(3*math.pi)
            result.update(status="POSITIVE_CALIBRATION",gstar_m_s2=gstar,S=source,
                gs_m_s2=gs,Q=q,Q_target=target,d=d,discrete_d_upper=trial,
                continuum_only_d_upper=math.pi*source/(4*(1-eps**2)),
                gs_lower_m_s2=gslow,
                gs_discrete_upper_m_s2=gslow/math.sqrt(1-trial) if trial<1 else None,
                dS_dQ=1/gradient,root_relative_condition=target/(source*gradient),
                Omega_exc_reconstructed=reconstructed[0],Omega_vac_reconstructed=reconstructed[1],
                pressure_over_energy=p/e,delta_q0=1.5*oe*p/e,
                relaxed_reference_a0_m_s2=gstar*a0,
                relaxed_quadratic_window_upper_G=source**2/(2*a0),
                relaxed_window_upper_over_cutoff_squared=source**2/(2*a0*eps**2),
                S_over_cutoff_squared=source/eps**2,
                bracket_doublings=doublings,max_numerical_relative_error=max(numerical.values()))
            rows.append(result)
    check("census",0. if len(rows)==CONFIG["expected_rows"] else 1.)
    failures = [name for name,ok in gates if not ok]
    return dict(status="COMPLETE" if not failures else "FAILED_CHECKS",
        scope="Conditional shared-scale calibration of unchanged scalar templates; not a fit, galaxy response or cosmological validation",
        checks=dict(count=len(gates),failed=len(failures),failure_names=failures,
                    worst_relative_errors=worst),
        templates=templates,references=refs,rows=rows,
        domain_counts={name:sum(r["status"]==name for r in rows)
                       for name in ("POSITIVE_CALIBRATION","NONPOSITIVE_DOMAIN")},
        external_primary=references["external_primary"],
        qualifications=["All reference acceleration inputs are historical provenance, not targets",
                        "BBN and inherited H0/Omega_Lambda are model-dependent reference assumptions",
                        "Exact discrete trial bound and continuum-only bound are not interchangeable",
                        "Pressure ratio is retained; old fixed-I/galaxy fields are not recalibrated",
                        "Physical inertia, production, phase/orientation and clock data are not fixed"],
        seconds=time.perf_counter()-start,
        max_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("freeze","run"):
        raise SystemExit("Use freeze or run; stdout only")
    returned,history,references,snapshot = authenticate()
    if sys.argv[1]=="freeze":
        print(encode(snapshot).decode())
        return
    if encode(json.loads(FREEZE.read_text())) != encode(snapshot):
        raise RuntimeError("Current source does not match prospective freeze")
    payload = run(returned,history,references)
    output = dict(freeze_sha256=sha(FREEZE),payload_sha256=digest(payload),payload=payload)
    raw = encode(output)
    if len(raw)>CONFIG["output_limit_bytes"]:
        raise RuntimeError("Compact output exceeds prospective one-MiB limit")
    print(raw.decode())
    if payload["status"]!="COMPLETE":
        raise SystemExit(2)


if __name__=="__main__":
    main()
