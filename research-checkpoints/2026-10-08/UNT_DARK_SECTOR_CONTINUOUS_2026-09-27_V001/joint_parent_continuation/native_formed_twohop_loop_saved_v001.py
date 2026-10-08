"""Exploratory saved-state arithmetic, not a held-out observational test.

Edges (a,b,c,d)=(L0R0,L0R1,L1R0,L1R1). A scalar Hermitian square calibrated
by the same-clock one-hop magnitudes has one loop phase Phi. Necessarily
 QL=pa*pc+pb*pd+2*sqrt(pa*pb*pc*pd)*cos(Phi),
 QR=pa*pb+pc*pd+2*sqrt(pa*pb*pc*pd)*cos(Phi).
Thus D=QL-QR-pa*pc-pb*pd+pa*pb+pc*pd must vanish. Native QL=< (ac+bd)^2 >,
QR=< (ab+cd)^2 >; their shared four-edge moment cancels from D, leaving
cov(a,c)+cov(b,d)-cov(a,b)-cov(c,d). Individual phase bounds remain required.
The scalar Hamiltonian may be recalibrated separately at every saved age;
its one loop phase must nevertheless fit both opposite pairs at that age.

No import of a producer, propagation, new ages, fits or file writes. The
unchanged assigned 1e-10 p/Q allowances are NOT certified roundoff intervals.
Ideal fresh-pointer SWAP/readout apparatus and its preparation/control costs
remain uninstantiated. Complete bulk SWAP work is retained for sender R0.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
TOL = 1e-10
PINS = {"native_formed_twohop_v002.py":
        "59e1147a4a58cb9ebdbe57a0db43313756f9bc1de63438456368b4ace90225f0",
        "native_formed_twohop_v002_results.json":
        "cb164dd7a88ef4aa487536a998fffc1f05cedf1cdc9e922f07c6c0149710bbd9"}
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit(g, e):
    return (g >> e) & 1


def degree(g, vertex):
    return sum(bit(g, e) for e, endpoints in enumerate(EDGES) if vertex in endpoints)


def phase_bounds(p, q, pairs):
    lo, hi = [max(0., x-TOL) for x in p], [min(1., x+TOL) for x in p]
    amp = [math.sqrt(p[i]*p[j]) for i, j in pairs]
    al = [math.sqrt(lo[i]*lo[j]) for i, j in pairs]
    ah = [math.sqrt(hi[i]*hi[j]) for i, j in pairs]
    lower_range = [max(0., al[0]-ah[1], al[1]-ah[0])**2,
                   max(abs(al[0]-ah[1]), abs(ah[0]-al[1]))**2]
    upper_range = [(al[0]+al[1])**2, (ah[0]+ah[1])**2]
    outside = q+TOL < lower_range[0] or q-TOL > upper_range[1]
    inside = q-TOL >= lower_range[1] and q+TOL <= upper_range[0]
    return dict(nominal_lower=(amp[0]-amp[1])**2, nominal_upper=(amp[0]+amp[1])**2,
                assigned_lower_boundary_range=lower_range, assigned_upper_boundary_range=upper_range,
                assigned_Q_interval=[q-TOL, q+TOL],
                status="NUMERICAL_PHASE_BOUND_VIOLATION_UNDER_ASSIGNED_ALLOWANCE" if outside else
                       "INDIVIDUALLY_COMPATIBLE_UNDER_ASSIGNED_ALLOWANCE" if inside else
                       "INCONCLUSIVE_UNDER_ASSIGNED_ALLOWANCE")


def run():
    start = time.perf_counter()
    identities = {name: sha(HERE/name) for name in PINS}
    if identities != PINS:
        raise RuntimeError("Pinned saved input changed")
    source_sha = sha(Path(__file__))
    saved = json.loads((HERE/"native_formed_twohop_v002_results.json").read_text())
    if (saved["status"] != "COMPLETE" or not all(c["passed"] for c in saved["checks"])
            or saved["source_sha256"] != PINS["native_formed_twohop_v002.py"]):
        raise RuntimeError("Saved result lacks the pinned successful producer binding")
    census = [(name, age) for name in ("native", "feedback_off", "copying_off") for age in (0., .25, .5, 1., 2.)]
    if [(r["case"], r["age"]) for r in saved["rows"]] != census:
        raise RuntimeError("Unexpected saved row census")
    checks, rows = [], []
    def check(name, a, b=0.):
        residual = abs(a-b)
        checks.append(dict(name=name, residual=residual, allowance=TOL,
                           passed=math.isfinite(residual) and residual <= TOL))
    for row in saved["rows"]:
        tag = row["case"]+":"+str(row["age"])
        re, im = row["state"]["real"], row["state"]["imag"]
        if len(re) != 1024 or len(im) != 1024 or not all(math.isfinite(x) for x in re+im):
            raise RuntimeError("Invalid saved full vector: "+tag)
        weights = [math.fsum((a*a, b*b)) for a, b in zip(re, im)]
        check(tag+":norm", math.fsum(weights), 1.)
        # Route 1: full basis amplitudes with explicit path counts.
        p1 = [math.fsum(w for i, w in enumerate(weights) if bit(i//64, e)) for e in range(4)]
        ql1 = math.fsum(w*(bit(i//64, 0)*bit(i//64, 2)+bit(i//64, 1)*bit(i//64, 3))**2 for i, w in enumerate(weights))
        qr1 = math.fsum(w*(bit(i//64, 0)*bit(i//64, 1)+bit(i//64, 2)*bit(i//64, 3))**2 for i, w in enumerate(weights))
        # Route 2: graph marginal, then subset-projector expansion.
        pg = [math.fsum(weights[64*g:64*(g+1)]) for g in range(16)]
        def joint(mask):
            return math.fsum(pg[g] for g in range(16) if g & mask == mask)
        p = [joint(1 << e) for e in range(4)]
        q4 = joint(15)
        ql, qr = math.fsum((joint(5), joint(10), 2*q4)), math.fsum((joint(3), joint(12), 2*q4))
        for e in range(4):
            check(tag+":p_two_routes:"+str(e), p[e], p1[e])
            check(tag+":p_saved:"+str(e), p[e], row["edge_means"][e])
        check(tag+":QL_two_routes", ql, ql1)
        check(tag+":QR_two_routes", qr, qr1)
        check(tag+":QL_saved", ql, row["M2"])
        base_l = math.fsum((p[0]*p[2], p[1]*p[3]))
        base_r = math.fsum((p[0]*p[1], p[2]*p[3]))
        D = math.fsum((ql, -qr, -base_l, base_r))
        cov_D = math.fsum((joint(5)-p[0]*p[2], joint(10)-p[1]*p[3],
                          -joint(3)+p[0]*p[1], -joint(12)+p[2]*p[3]))
        check(tag+":four_edge_cancellation", D, cov_D)
        pl, ph = [max(0., x-TOL) for x in p], [min(1., x+TOL) for x in p]
        Dlo = math.fsum((ql-TOL, -qr-TOL, -ph[0]*ph[2], -ph[1]*ph[3], pl[0]*pl[1], pl[2]*pl[3]))
        Dhi = math.fsum((ql+TOL, -qr+TOL, -pl[0]*pl[2], -pl[1]*pl[3], ph[0]*ph[1], ph[2]*ph[3]))
        left_bounds, right_bounds = phase_bounds(p, ql, ((0, 2), (1, 3))), phase_bounds(p, qr, ((0, 1), (2, 3)))
        interference = 2*math.sqrt(math.prod(p))
        common_rejected = Dlo > 0 or Dhi < 0
        individual_rejected = any(b["status"].startswith("NUMERICAL_PHASE_BOUND_VIOLATION") for b in (left_bounds, right_bounds))
        params, energies = row["parameters"], row["component_energies"]
        du = math.fsum(pg[g]*degree(g, 2) for g in range(16))
        dc = math.fsum(w*degree(i//64, i % 4) for i, w in enumerate(weights))
        check(tag+":sender_degree_two_routes", du, p[0]+p[2])
        check(tag+":old_current_square", params["lambda_J"]*dc, energies["current_square"])
        hopping = -2*params["t_hop"]*math.fsum(
            bit(g, e)*(re[(g*16+r)*4+u]*re[(g*16+r)*4+v]+im[(g*16+r)*4+u]*im[(g*16+r)*4+v])
            for g in range(16) for r in range(16) for e, (u, v) in enumerate(EDGES))
        check(tag+":old_hopping", hopping, energies["carrier_hopping"])
        work = params["lambda_J"]*(p[0]+p[2])-energies["current_square"]-energies["carrier_hopping"]
        work_alt = params["lambda_J"]*(du-dc)-hopping
        check(tag+":SWAP_work_two_routes", work, work_alt)
        check(tag+":complete_old_energy", math.fsum(energies.values()), row["energy"])
        after = math.fsum(value for key, value in energies.items() if key not in ("current_square", "carrier_hopping"))+params["lambda_J"]*du
        check(tag+":complete_after_energy", after-row["energy"], work)
        nu = row["clock"]["nu"]
        clock_ok = row["clock"]["status"] == "DEFINED" and nu is not None and abs(nu) > TOL
        scale = params["t_hop"]**4/(4*params["hbar"]**4*nu**4) if clock_ok else None
        if clock_ok:
            check(tag+":saved_clock_L", scale*ql, row["L"])
        rows.append(dict(case=row["case"], age=row["age"], edge_means=p,
                         independent_basis_moments=dict(edge_means=p1, QL=ql1, QR=qr1),
                         QL=ql, QR=qr, four_edge_moment=q4, D=D, covariance_D=cov_D,
                         assigned_D_interval=[Dlo, Dhi], left_phase_bounds=left_bounds, right_phase_bounds=right_bounds,
                         cos_left=(ql-base_l)/interference if interference > 0 else None,
                         cos_right=(qr-base_r)/interference if interference > 0 else None,
                         common_loop_status="NUMERICAL_COMMON_LOOP_INCOMPATIBILITY_UNDER_ASSIGNED_ALLOWANCE" if common_rejected else
                                            "NOT_REJECTED_BY_ASSIGNED_ALLOWANCE_TEST",
                         scalar_square_rejected_under_assigned_allowance=common_rejected or individual_rejected,
                         clock=row["clock"], L_left=scale*ql if clock_ok else None, L_right=scale*qr if clock_ok else None,
                         swap_R0=dict(current_square=params["lambda_J"]*du-energies["current_square"],
                                      hopping=-energies["carrier_hopping"], total=work, independent_total=work_alt,
                                      old_complete_energy=row["energy"], after_complete_energy=after)))
    check("self_source_unchanged", float(sha(Path(__file__)) != source_sha))
    output = dict(status="COMPLETE" if all(c["passed"] for c in checks) else "FAILED_CHECKS",
                  source_sha256=source_sha, input_sha256=identities,
                  scope="Exploratory follow-on analysis of all saved formed states, not held-out observational validation",
                  numerical_allowance=TOL, allowance_is_certified_error=False, rows=rows, checks=checks,
                  check_counts=dict(total=len(checks), passed=sum(c["passed"] for c in checks)),
                  qualification=dict(new_evolution=False, new_preparation=False, physical_metric=False,
                                     same_scalar_original_square_for_all_senders_at_each_age=True,
                                     arbitrary_edge_phases_allowed=True,
                                     pointer_preparation_control_readout_instantiated=False, complete_bulk_SWAP_work=True),
                  runtime=dict(wall_seconds=time.perf_counter()-start,
                               max_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                               max_rss_units="bytes" if sys.platform == "darwin" else "KiB"))
    print(json.dumps(output, separators=(",", ":"), allow_nan=False))
    return 0 if output["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; reads saved states only")
    try:
        code = run()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        code = 1
    raise SystemExit(code)
