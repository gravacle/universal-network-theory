"""Read-only saved-state initial annulus release; stdout JSON freeze/run only."""
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
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.resolve()
FREEZE = HERE/"PREPARED_ANNULUS_RELEASE_V001_FROZEN.json"
ANCESTOR = HERE/"COMMON_HISTORY_MECHANISM_V001_RESULTS.json"
ANCESTOR_FREEZE = HERE/"COMMON_HISTORY_MECHANISM_V001_FROZEN.json"
ANCESTOR_SHA = "e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a"
ANCESTOR_FREEZE_SHA = "13d05e24680166cb903e02fb961717a2bef1a89771a1d76c80156ab50cbe76ef"
ANCESTOR_PAYLOAD_SHA = "91793086852fe6fe12908bae49f6eb983c7aa15d7211cd7abf496a7827d4691e"
GC = .0025
CONFIG = dict(case_indices=(0, 1, 2), observation_index=0,
              expected_order_dt=((64, .01), (128, .01), (128, .005)),
              gap=.001, duration=8., hold=0., source=GC,
              inner_radii=(1/4096, 1/8192), outer_ratio=2., radial_cells=(64, 128),
              metric_refinement_factor=2, simpson_panels_per_cell=2, gauss_per_cell=4,
              endpoint_reference_orders=(96, 192), root_bisections=96,
              M_squared=1., algebra_tolerance=2e-11,
              metric_u_tolerance=2e-9, clock_quadrature_tolerance=2e-7,
              eta_boundary_tolerance=2e-11, independent_eta_tolerance=2e-7,
              fd_metric_tolerance=2e-6, fd_release_tolerance=2e-5,
              baseline_rule="same finite-parent high-source endpoint, no fitted offset",
              action_evolution="not numerically evaluated")
SOURCES = (
    "prepared_annulus_release_v001.py", "PREPARED_ANNULUS_RELEASE_PROTOCOL_V001.md",
    "UNIFORM_PREPARED_ANNULUS_RELEASE_V001.md", "PREPARED_SPHERICAL_TEST_REDUCTION_V001.md",
    "COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md", "EXPLICIT_MODE_COSMOLOGY_PATHWAY.md",
    "../joint_parent_dynamics/SAME_PARENT_FORCE_VOLUME_LINK.md",
)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_path(path):
    path = path.resolve()
    path.relative_to(PROJECT)
    return path


def authenticate():
    if sha(ANCESTOR) != ANCESTOR_SHA or sha(ANCESTOR_FREEZE) != ANCESTOR_FREEZE_SHA:
        raise RuntimeError("Saved preparation bytes differ")
    result = json.loads(ANCESTOR.read_text())
    if (result["freeze_sha256"] != ANCESTOR_FREEZE_SHA
            or result["payload_sha256"] != ANCESTOR_PAYLOAD_SHA
            or hashlib.sha256(encoded(result["payload"])).hexdigest() != ANCESTOR_PAYLOAD_SHA):
        raise RuntimeError("Saved preparation payload/freeze link differs")
    if not all(result["payload"]["checks"].values()):
        raise RuntimeError("Preparation qualification did not pass")
    files = {}
    visited = set()

    def visit(manifest_path):
        manifest_path = project_path(manifest_path)
        if manifest_path in visited:
            return
        visited.add(manifest_path)
        files[str(manifest_path.relative_to(PROJECT))] = sha(manifest_path)
        manifest = json.loads(manifest_path.read_text())
        for name, expected in manifest["files"].items():
            path = project_path(Path(name) if Path(name).is_absolute() else manifest_path.parent/name)
            if sha(path) != expected:
                raise RuntimeError("Ancestor source differs: "+str(path))
            files[str(path.relative_to(PROJECT))] = expected
            if path.name.endswith("FROZEN.json"):
                visit(path)

    visit(ANCESTOR_FREEZE)
    files[str(ANCESTOR.relative_to(PROJECT))] = ANCESTOR_SHA
    for name in SOURCES:
        path = project_path(HERE/name)
        files[str(path.relative_to(PROJECT))] = sha(path)
    snapshot = dict(files=files, configuration=CONFIG,
                    ancestor_payload_sha256=ANCESTOR_PAYLOAD_SHA)
    return result["payload"], snapshot


def bounded(a, gs):
    z = (np.asarray(a)/gs)**2
    return (a/np.sqrt(1+z), (1+z)**-1.5,
            -3*a/gs**2*(1+z)**-2.5)


def root(delta, held):
    return 2*delta/math.sqrt(3)*np.sinh(
        np.arcsinh(3*math.sqrt(3)*held/(2*delta**2))/3)


def endpoint(delta, weights, gs):
    y = root(delta, gs)
    return float(np.dot(weights, .5*delta**2*y**2+.75*y**4)), y


def endpoint_reference(gap, order, gs):
    # delta=z^3 regularizes the endpoint's delta^(7/3) leading integrand.
    nodes, weights = leggauss(order)
    low = gap**(1/3)
    z = low+(nodes+1)*(1-low)/2
    return endpoint(z**3, weights*(1-low)/2*3*z**5, gs)[0]


def metric_rhs(x, u, state, inner):
    f = 1-inner*u
    if not math.isfinite(f) or f <= 0:
        raise ValueError("Initial metric left the positive-f branch")
    a = GC*math.sqrt(f)
    h, hp, hpp = bounded(a, state["gs"])
    e = state["E0"]+state["DeltaU"]-state["B"]*h+a*state["B"]*hp
    numerator = -u/x+state["C"]*inner*x*e+2*state["C"]*math.sqrt(f)*state["B"]*hp
    denominator = 1+state["C"]*inner*x*state["B"]*hpp*GC/2
    if not math.isfinite(denominator) or denominator == 0:
        raise ValueError("Initial metric ODE denominator vanished")
    return float(numerator/denominator)


def metric_grid(state, inner, cells):
    x = np.linspace(1., 2., cells+1)
    u = np.empty_like(x)
    u[0] = 2*GC+state["Lambda"]*inner/3
    step = 1/cells
    for i in range(cells):
        a = metric_rhs(x[i], u[i], state, inner)
        b = metric_rhs(x[i]+step/2, u[i]+step*a/2, state, inner)
        c = metric_rhs(x[i]+step/2, u[i]+step*b/2, state, inner)
        d = metric_rhs(x[i]+step, u[i]+step*c, state, inner)
        u[i+1] = u[i]+step*(a+2*b+2*c+d)/6
    slopes = np.array([metric_rhs(t, y, state, inner) for t, y in zip(x, u)])
    return x, u, slopes


def hermite(x, u, slopes, query):
    query = np.asarray(query)
    step = x[1]-x[0]
    cell = np.clip(np.searchsorted(x, query, side="right")-1, 0, len(x)-2)
    t = (query-x[cell])/step
    return ((2*t**3-3*t**2+1)*u[cell]+(t**3-2*t**2+t)*step*slopes[cell]
            +(-2*t**3+3*t**2)*u[cell+1]+(t**3-t**2)*step*slopes[cell+1])


def fields(x, u, state, inner):
    f = 1-inner*u
    if np.any(f <= 0) or not np.all(np.isfinite(f)):
        raise ValueError("Interpolated metric left the positive-f branch")
    lapse = np.exp(GC*inner*(x-2))
    a = GC*np.sqrt(f)
    h, hp, hpp = bounded(a, state["gs"])
    d = lapse*x*x*state["B"]*hpp*np.sqrt(f)
    aflux = lapse*lapse*x*x*state["VB"]*hp
    if np.any(d >= 0) or not np.all(np.isfinite(d)):
        raise ValueError("Release is not on the prescribed fixed-negative-D branch")
    return dict(f=f, N=lapse, a=a, h=h, hp=hp, hpp=hpp, d=d, A=aflux)


def release(state, inner, x, u, slopes):
    cells, step = len(x)-1, x[1]-x[0]
    mid = (x[:-1]+x[1:])/2
    quarters = np.stack((x[:-1]+step/4, x[:-1]+3*step/4), axis=1)
    node = fields(x, u, state, inner)
    midpoint = fields(mid, hermite(x, u, slopes, mid), state, inner)
    quarter = fields(quarters, hermite(x, u, slopes, quarters), state, inner)

    def simpson(node_values, midpoint_values, quarter_values):
        return step*(node_values[:-1]+4*quarter_values[:, 0]+2*midpoint_values
                     +4*quarter_values[:, 1]+node_values[1:])/12

    ia = simpson(node["A"]/node["d"], midpoint["A"]/midpoint["d"], quarter["A"]/quarter["d"])
    id_ = simpson(1/node["d"], 1/midpoint["d"], 1/quarter["d"])
    k = float(np.sum(ia)/np.sum(id_))
    rate = (k-node["A"])/node["d"]
    rate_mid = (k-midpoint["A"])/midpoint["d"]
    rate_quarter = (k-quarter["A"])/quarter["d"]
    eta = inner*np.r_[0., np.cumsum(simpson(rate, rate_mid, rate_quarter))]
    gn, gw = leggauss(CONFIG["gauss_per_cell"])
    q = mid[:, None]+step*gn[None, :]/2
    gauss = fields(q, hermite(x, u, slopes, q), state, inner)
    weights = step*gw/2
    ka = float(np.sum((gauss["A"]/gauss["d"])*weights))
    kd = float(np.sum((1/gauss["d"])*weights))
    kg = ka/kd
    gauss_rate = (kg-node["A"])/node["d"]
    gauss_eta = inner*np.r_[0., np.cumsum(np.sum(
        ((kg-gauss["A"])/gauss["d"])*weights, axis=1))]
    independent_boundary = inner*float(np.sum(((k-gauss["A"])/gauss["d"])*weights))
    return dict(node=node, k=k, k_gauss=kg, eta=eta, rate=rate,
                gauss_rate=gauss_rate, gauss_eta=gauss_eta,
                independent_boundary=independent_boundary,
                inverse_d_integral=float(np.sum(id_)), A_over_d_integral=float(np.sum(ia)),
                a_dot=np.sqrt(node["f"])*rate,
                Dh=node["hp"]*np.sqrt(node["f"])*rate/node["N"])


def centered_derivative(values, step):
    coefficients = (-1., 9., -45., 0., 45., -9., 1.)
    length = len(values)-6
    return sum(c*values[j:j+length] for j, c in enumerate(coefficients))/(60*step)


def run():
    started = time.perf_counter()
    old, inputs = authenticate()
    if encoded(json.loads(FREEZE.read_text())) != encoded(inputs):
        raise RuntimeError("Prospective annulus freeze differs")
    checks, states, cases, controls = [], [], [], []

    def check(name, actual, expected=0., tolerance=CONFIG["algebra_tolerance"]):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))

    parameters = old["parameters"]
    if any(parameters[key] != 1 for key in ("A", "Lambda", "kappa", "u4", "m")):
        raise RuntimeError("Saved mode parameter convention differs")
    gs = float(parameters["gs_internal"])
    hc = float(bounded(GC, gs)[0])
    refs = {str(gap): {str(order): endpoint_reference(gap, order, gs)
                       for order in CONFIG["endpoint_reference_orders"]}
            for gap in (0., CONFIG["gap"])}
    for gap, values in refs.items():
        check('endpoint_quadrature:'+gap, (values['96']-values['192'])/values['192'],
              tolerance=CONFIG["clock_quadrature_tolerance"])
    for index, expected in zip(CONFIG["case_indices"], CONFIG["expected_order_dt"]):
        original = old["cases"][index]
        obs = original["observations"][CONFIG["observation_index"]]
        if ((original["order"], original["dt"]) != tuple(expected)
                or original["gap"] != CONFIG["gap"] or original["duration"] != CONFIG["duration"]
                or obs["hold"] != CONFIG["hold"] or not all(original["checks"].values())):
            raise RuntimeError("Saved state census/qualification differs")
        check(f'state{index}:source', obs["g_over_a0"]*parameters["a0_internal"], GC)
        delta, weights = np.array(original["delta"]), np.array(original["weights"])
        y, v = np.array(obs["y"]), np.array(obs["v"])
        if (len(delta) != expected[0] or any(a.shape != delta.shape for a in (weights, y, v))
                or np.any(delta <= 0) or np.any(weights <= 0)
                or not all(np.all(np.isfinite(a)) for a in (delta, weights, y, v))):
            raise RuntimeError("Invalid retained mode arrays")
        kb = float(np.sum(weights))
        check(f'state{index}:Kb', kb, original["Kb"])
        du, ys = endpoint(delta, weights, gs)
        lo, hi = np.zeros_like(delta), np.cbrt(delta*gs)
        for _ in range(CONFIG["root_bisections"]):
            mid = (lo+hi)/2
            above = mid**3+delta**2*mid > delta*gs
            hi = np.where(above, mid, hi)
            lo = np.where(above, lo, mid)
        check(f'state{index}:endpoint_root', ys, (lo+hi)/2)
        check(f'state{index}:endpoint_cubic', (ys**3+delta**2*ys-delta*gs)/(delta*gs))
        wel = float(np.dot(weights, .5*(gs-delta*ys)**2+.25*ys**4))
        check(f'state{index}:endpoint_energy', du, kb*gs*gs/2-wel)
        kinetic = float(np.dot(weights, v*v/2))
        quadratic = float(np.dot(weights, delta*delta*y*y/2))
        quartic = float(np.dot(weights, y**4/4))
        b, vb = float(np.dot(weights, delta*y)), float(np.dot(weights, delta*v))
        e0 = kinetic+quadratic+quartic
        check(f'state{index}:saved_B', b, obs["B"])
        check(f'state{index}:saved_kinetic', kinetic, obs["kinetic"])
        check(f'state{index}:saved_complete_energy', kb*GC*GC/2+e0-b*hc, obs["energy"])
        check(f'state{index}:old_work', obs["energy"], obs["work"])
        if du <= 0 or b <= 0:
            raise RuntimeError("Endpoint or prepared polarization not on stated branch")
        _, hpc, hppc = bounded(GC, gs)
        weak_coefficient = vb*hpc/(b*hppc)
        state = dict(index=index, order=expected[0], preparation_dt=expected[1],
                     gs=gs, Kb=kb, C=2/kb, DeltaU=du, Lambda=2*du/kb,
                     B=b, VB=vb, E0=e0, kinetic=kinetic, quadratic=quadratic, quartic=quartic,
                     old_clamp_h=hc, old_clamp_work=obs["work"], old_clamp_energy=obs["energy"],
                     weak_rate_coefficient=float(weak_coefficient),
                     clock_rate_scale=max(1., abs(float(weak_coefficient))),
                     local_curvature_frequencies=np.sqrt(delta**2+3*y*y).tolist(),
                     endpoint_full_band_difference=du-refs[str(0.)]['192'],
                     endpoint_same_band_quadrature_difference=du-refs[str(CONFIG['gap'])]['192'])
        states.append(state)
        for inner in CONFIG["inner_radii"]:
            for cells in CONFIG["radial_cells"]:
                name = f'state{index}:rin{inner}:cells{cells}'
                try:
                    x, u, slopes = metric_grid(state, inner, cells)
                    fine_x, fine_u, fine_slopes = metric_grid(state, inner, 2*cells)
                    released = release(state, inner, x, u, slopes)
                    refined = release(state, inner, fine_x, fine_u, fine_slopes)
                    node = released["node"]
                    u_error = float(np.max(abs(u-fine_u[::2])))
                    rate_error = float(np.max(abs(released["rate"]-refined["rate"][::2])))
                    quad_error = float(np.max(abs(released["rate"]-released["gauss_rate"])))
                    check(name+':metric_refinement', u_error, tolerance=CONFIG["metric_u_tolerance"])
                    check(name+':rate_refinement', rate_error/state["clock_rate_scale"], tolerance=CONFIG["clock_quadrature_tolerance"])
                    check(name+':rate_quadrature', quad_error/state["clock_rate_scale"], tolerance=CONFIG["clock_quadrature_tolerance"])
                    check(name+':eta_boundary', released["eta"][[0, -1]], tolerance=CONFIG["eta_boundary_tolerance"])
                    check(name+':eta_independent_boundary', released["independent_boundary"], tolerance=CONFIG["independent_eta_tolerance"])
                    f, a, h, hp, hpp = [node[key] for key in ("f", "a", "h", "hp", "hpp")]
                    e = e0+du-b*h+a*b*hp
                    coefficient = 1+state["C"]*inner*x*b*hpp*GC/2
                    metric_scale = abs(u[0])+2*state["C"]*abs(b)+state["C"]*inner*(abs(e0)+du)
                    algebra_constraint = coefficient*slopes+u/x-state["C"]*inner*x*e-2*state["C"]*np.sqrt(f)*b*hp
                    check(name+':metric_algebra', algebra_constraint/metric_scale)
                    ufd = centered_derivative(u, 1/cells)
                    sl = slice(3, -3)
                    fdmetric = coefficient[sl]*ufd+u[sl]/x[sl]-state["C"]*inner*x[sl]*e[sl]-2*state["C"]*np.sqrt(f[sl])*b*hp[sl]
                    check(name+':metric_fd', fdmetric/metric_scale, tolerance=CONFIG["fd_metric_tolerance"])
                    eta_fd = centered_derivative(released["eta"], 1/cells)/inner
                    reconstructed_flux = node["d"][sl]*eta_fd+node["A"][sl]
                    fdrelease = centered_derivative(reconstructed_flux, 1/cells)
                    check(name+':release_fd', fdrelease/max(2*abs(vb), 1e-30), tolerance=CONFIG["fd_release_tolerance"])
                    exact_flux = node["d"]*released["rate"]+node["A"]
                    check(name+':flux_algebra', exact_flux, released["k"])
                    # Full original lapse density, with f'_r=-u_x, evaluated
                    # without the numerically subtractive expression 1-f.
                    divergence = 2*b*np.sqrt(f)*hp/(inner*x)-b*hpp*GC*slopes/2
                    rho_mode = state["C"]*(e+divergence)
                    curvature_density = (u+x*slopes)/(inner*x*x)
                    check(name+':original_constraint', (curvature_density-rho_mode)*inner*x/metric_scale)
                    gm = inner*inner*x*u/2
                    gm_subtracted = gm-state["Lambda"]*(inner*x)**3/6
                    check(name+':inner_mass', gm_subtracted[0], GC*inner*inner)
                    weak = state["weak_rate_coefficient"]*(2/x**2-1)
                    baseline_only = dict(state, B=0., E0=0.)
                    bx, bu, _ = metric_grid(baseline_only, inner, cells)
                    exact_bu = 2*GC/bx+state["Lambda"]*inner*bx*bx/3
                    check(name+':null_metric_control', bu, exact_bu, CONFIG["metric_u_tolerance"])
                    controls.append(dict(state_index=index, inner_radius=inner, cells=cells,
                                         null_metric_max_u_error=float(np.max(abs(bu-exact_bu)))))
                    rows = []
                    for j in range(len(x)):
                        rows.append(dict(x=float(x[j]), r=float(inner*x[j]), u=float(u[j]), f=float(f[j]),
                            lapse=float(node["N"][j]), acceleration=float(a[j]), held_source=float(h[j]),
                            u_x=float(slopes[j]), metric_denominator=float(coefficient[j]),
                            scaled_D=float(node["d"][j]), scaled_A=float(node["A"][j]),
                            eta=float(released["eta"][j]), eta_r=float(released["rate"][j]),
                            eta_gauss=float(released["gauss_eta"][j]), eta_r_gauss=float(released["gauss_rate"][j]),
                            acceleration_dot=float(released["a_dot"][j]),
                            proper_source_rate=float(released["Dh"][j]),
                            source_fractional_rate=float(released["Dh"][j]/h[j]),
                            weak_eta_r=float(weak[j]), weak_rate_difference=float(released["rate"][j]-weak[j]),
                            interaction_quench=float(-b*(h[j]-hc)),
                            mode_density=float(rho_mode[j]), curvature_density=float(curvature_density[j]),
                            source_aBhprime=float(a[j]*b*hp[j]), polarization_divergence=float(divergence[j]),
                            GM_geometric=float(gm[j]), GM_Lambda_subtracted=float(gm_subtracted[j])))
                    cases.append(dict(status="COMPLETE", state_index=index, inner_radius=inner,
                        outer_radius=2*inner, cells=cells, rows=rows,
                        constant_scaled_flux=released["k"], constant_flux=inner**2*released["k"],
                        gauss_scaled_flux=released["k_gauss"],
                        inverse_scaled_D_integral=released["inverse_d_integral"],
                        A_over_D_integral=released["A_over_d_integral"],
                        min_f=float(np.min(f)), min_lapse=float(np.min(node["N"])),
                        min_abs_scaled_D=float(np.min(abs(node["d"]))),
                        min_abs_metric_denominator=float(np.min(abs(coefficient))),
                        metric_u_refinement_error=u_error, clock_rate_refinement_error=rate_error,
                        clock_rate_quadrature_error=quad_error,
                        independent_gauss_eta_at_outer=released["independent_boundary"],
                        weak_oracle_max_scaled_difference=float(np.max(abs(released["rate"]-weak))/state["clock_rate_scale"]),
                        fd_metric_node_indices=list(range(3, cells-2)), fd_metric_residual=fdmetric.tolist(),
                        fd_release_node_indices=list(range(6, cells-5)), fd_release_residual=fdrelease.tolist(),
                        annulus_GM_geometric=float(gm[-1]-gm[0]),
                        annulus_GM_Lambda_subtracted=float(gm_subtracted[-1]-gm_subtracted[0]),
                        action_drift="not computed; no action evolution qualification"))
                except (ValueError, FloatingPointError) as exc:
                    check(name+':domain_failure', 1., tolerance=0.)
                    cases.append(dict(status="DOMAIN_FAILURE", state_index=index,
                                      inner_radius=inner, cells=cells, reason=str(exc)))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    payload = dict(configuration=CONFIG, checks=checks, state_summaries=states,
                   cases=cases, null_metric_controls=controls, endpoint_continuum_contrasts=refs,
                   source_parameters=parameters, elapsed_seconds=time.perf_counter()-started,
                   peak_rss_bytes=int(peak),
                   interpretation="initial conditional constraint/clock derivative census; not a long-time gravity solution")
    return dict(status="COMPLETE" if all(c["passed"] for c in checks) else "FAILED_CHECKS",
                freeze_sha256=sha(FREEZE), payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                payload=payload)


def main():
    if sys.argv[1:] == ["freeze"]:
        report = authenticate()[1]
    elif sys.argv[1:] == ["run"]:
        report = run()
    else:
        raise ValueError("usage: prepared_annulus_release_v001.py freeze|run")
    print(json.dumps(report, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status="ERROR", error_type=type(exc).__name__, error=str(exc))))
        sys.exit(1)
