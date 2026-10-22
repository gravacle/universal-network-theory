"""P61 V001 SOURCE ONLY. Root alone executes method/numerical functions.
Fresh prospect0171 governs. No geometry selector, native input or physical release.
Dense dimension<=128 guard; every output remains METHOD/COMPARATOR only.
"""
import math
import numpy as np


def _matrix(value, n=None):
    a = np.asarray(value, dtype=complex)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not 0 < len(a) <= 128:
        raise ValueError("square matrix of dimension1..128 required")
    if n is not None and a.shape != (n,n):
        raise ValueError("dimension mismatch")
    if not np.isfinite(a).all():
        raise ValueError("nonfinite matrix")
    return a


def coherent_probe(H, rho0, source, probe, times, tol=1e-10):
    """Raw same-H source/sham cost response. No physics success boolean.

    Tolerance-level positivity/unitarity checks are method diagnostics.
    Eigensystem error estimates are NOT outward-rounded certificates.
    No physical record, earned geometry or apparatus can be certified here.
    """
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("positive finite tolerance required")
    H = _matrix(H)
    n = len(H)
    rho0, source, probe = [_matrix(a,n) for a in (rho0,source,probe)]
    if not np.array_equal(H,H.conj().T) or not np.array_equal(rho0,rho0.conj().T):
        raise ValueError("exact stored Hermiticity required")
    if abs(np.trace(rho0)-1) > tol:
        raise ValueError("density trace mismatch")
    rho_min = float(np.linalg.eigvalsh(rho0)[0])
    if rho_min < -tol:
        raise ValueError("nonpositive density")
    ident = np.eye(n)
    source_defect = float(np.linalg.norm(source.conj().T@source-ident,2))
    probe_defect = float(np.linalg.norm(probe.conj().T@probe-ident,2))
    if max(source_defect,probe_defect) > tol:
        raise ValueError("nonunitary source or probe")
    times = list(times)
    if not times or any(not math.isfinite(t) or t < 0 for t in times):
        raise ValueError("nonempty nonnegative finite times required")
    rho1 = source@rho0@source.conj().T
    O = probe.conj().T@H@probe-H
    values,vectors = np.linalg.eigh(H)
    residual = float(np.linalg.norm(H@vectors-vectors*values,2))
    initial = float(np.linalg.norm(vectors@vectors.conj().T-ident,2))
    orthogonality = float(np.linalg.norm(vectors.conj().T@vectors-ident,2))
    vnorm = float(np.linalg.norm(vectors,2))
    onorm = float(np.linalg.norm(O,2))
    rows = []
    for t in times:
        U = (vectors*np.exp(-1j*t*values))@vectors.conj().T
        a0, a1 = U@rho0@U.conj().T, U@rho1@U.conj().T
        cost0,cost1 = np.trace(O@a0),np.trace(O@a1)
        delta = initial+t*residual*vnorm
        rows.append({"time":float(t),"sham_cost":float(cost0.real),
                     "source_cost":float(cost1.real),"difference":float((cost1-cost0).real),
                     "imaginary_cost_residual":float(max(abs(cost0.imag),abs(cost1.imag))),
                     "sham_trace_error":float(abs(np.trace(a0)-1)),
                     "source_trace_error":float(abs(np.trace(a1)-1)),
                     "unitarity_defect":float(np.linalg.norm(U.conj().T@U-ident,2)),
                     "evolution_error_estimate":delta,
                     "propagation_only_difference_error_estimate":2*onorm*delta*(2+delta)})
    return {"status":"METHOD_OR_COMPARATOR_ONLY_NOT_FIELD_ACCEPTANCE",
            "native_scoring_release":False,"rows":rows,
            "initial_sham_energy":float(np.trace(H@rho0).real),
            "initial_source_energy":float(np.trace(H@rho1).real),
            "initial_source_energy_change":float(np.trace(H@(rho1-rho0)).real),
            "read_norm":onorm,
            "initial_commutation_defect":float(np.linalg.norm(source@O-O@source,2)),
            "source_unitarity_defect":source_defect,"probe_unitarity_defect":probe_defect,
            "input_min_eigenvalue":rho_min,
            "eigensystem_residual_2norm":residual,"orthogonality_defect":orthogonality,
            "error_scope":"FLOAT_PROPAGATION_ESTIMATE_ONLY; input/source/probe/arithmetic certification absent",
            "H1":"UNDETERMINED","H2":"UNDETERMINED"}


def _site(op,site):
    result = np.array([[1]],complex)
    for j in range(3):
        result = np.kron(result,op if j == site else np.eye(2))
    return result


def proposed_probe_controls(tol=1e-9):
    """ROOT-RUN ONLY. Fresh three-site XY method control and failing partners."""
    X = np.array([[0,1],[1,0]],complex)
    Y = np.array([[0,-1j],[1j,0]],complex)
    N = np.array([[0,0],[0,1]],complex)
    xs,ys,ns = [[_site(op,j) for j in range(3)] for op in (X,Y,N)]
    H0 = sum(ns)
    bonds = [(xs[j]@xs[j+1]+ys[j]@ys[j+1])/2 for j in range(2)]
    H = H0+bonds[0]+bonds[1]
    rho = np.zeros((8,8),complex)
    rho[0,0] = 1
    times = [0.0,math.pi/(2*math.sqrt(2)),math.pi/math.sqrt(2)]
    positive = coherent_probe(H,rho,xs[0],xs[2],times,tol)
    detached = coherent_probe(H0+bonds[0],rho,xs[0],xs[2],times,tol)
    identical = coherent_probe(H,rho,np.eye(8),xs[2],times,tol)
    reversed_arms = coherent_probe(H,xs[0]@rho@xs[0],xs[0],xs[2],times,tol)
    offset = coherent_probe(H+3*np.eye(8),rho,xs[0],xs[2],times,tol)
    expected = [-2*math.sin(t/math.sqrt(2))**4 for t in times]
    observed = [row["difference"] for row in positive["rows"]]
    checks = {
        "positive_known_curve":max(abs(a-b) for a,b in zip(expected,observed)) < tol,
        "positive_nonzero_endpoint":abs(observed[-1]) > 1,
        "detached_null":max(abs(r["difference"]) for r in detached["rows"]) < tol,
        "identical_arms_null":max(abs(r["difference"]) for r in identical["rows"]) < tol,
        "reversal":max(abs(a+r["difference"]) for a,r in zip(observed,reversed_arms["rows"])) < tol,
        "common_offset":max(abs(a-r["difference"]) for a,r in zip(observed,offset["rows"])) < tol,
    }
    bad_density = rho.copy()
    bad_density[0,0],bad_density[1,1] = 2,-1
    bad_H = H.copy()
    bad_H[0,1] = 1
    for label,hh,rr,ww,vv in [
        ("density",H,bad_density,xs[0],xs[2]),
        ("hermiticity",bad_H,rho,xs[0],xs[2]),
        ("source",H,rho,2*xs[0],xs[2]),
        ("dimension",H,rho,np.eye(2),xs[2]),
        ("trace",H,2*rho,xs[0],xs[2]),
        ("probe",H,rho,xs[0],2*xs[2]),
    ]:
        try:
            coherent_probe(hh,rr,ww,vv,times,tol)
        except ValueError:
            checks["refuses_"+label] = True
        else:
            checks["refuses_"+label] = False
    return {"checks":checks,"all_method_checks":all(checks.values()),
            "positive":positive,"detached":detached,"identical":identical,
            "reversed":reversed_arms,"offset":offset,"analytic_expected":expected,
            "status":"FRESH_METHOD_CONTROLS_ONLY_NO_NATIVE_FIELD_VERDICT"}
