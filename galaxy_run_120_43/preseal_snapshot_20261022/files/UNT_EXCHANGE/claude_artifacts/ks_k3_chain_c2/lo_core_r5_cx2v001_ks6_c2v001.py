"""KS6 lo_core (ks_k3_chain_c2 c2v001; root A160): lo_core_r5_cx2v001 (12d36305) accepting K=3 states for S1_UA_C3T only.

The response producer is KS2 (custody KS1). For an S1_UA_C3T spec (KS1's gate: C3T label AND CB C3T grid) the saved
state's kept region must be the K=3 cube and its B1 shell edges must start at 3 (12d36305 L85-86, L104 required 4);
produce_current_lo is otherwise 12d36305's code. Every other spec goes to the unchanged 12d36305 module object (P, by
path and sha): its records, producer pins included, are 12d36305's. The retired prelaunch conditional path and the
legacy diagnostic are not extended: S1_UA_C3T is refused there, every other spec is 12d36305's. validate_tail_arrays and
recompute_b1 take kept_k (default 4.0, 12d36305's behaviour). The 12d36305 text follows.

Point-scoped LO evidence from saved TailState arrays or reviewed source caps.

Only static/replay arithmetic is performed. No U.build, forward, route-A or
route-B run is called. TailState digest reconstruction checks custody, not the
truth of a source reconstruction; the latter is a separate trusted-producer
boundary. JSON numbers or booleans alone cannot cross that boundary.

The LO indicator is |dv_i,s| <= |v_i| R_i rho_s B1_s / 4. It is the registered
linear readout indicator, not a nonlinear fixed-point or proper-volume theorem.
rho is numerically searched and B1 is production-node quadrature. Neither is
silently promoted to a rigorous continuous bound.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time

import numpy as np

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # KS6: 12d36305's folder
PREDECESSOR = (HERE / 'lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e')
RESPONSE_PATH = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py')   # KS6: KS2
if hashlib.sha256(RESPONSE_PATH.read_bytes()).hexdigest()!='99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7':raise ValueError('r5 response pin mismatch')
sp = importlib.util.spec_from_file_location('ks6_lo_point_response_ks2', RESPONSE_PATH)
PR = importlib.util.module_from_spec(sp)
sys.modules[sp.name] = PR
sp.loader.exec_module(PR)
CU, CC = PR.CU, PR.CC
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest() != PREDECESSOR[1]:
    raise ValueError('KS6: lo_core 12d36305 pin mismatch')
_psp = importlib.util.spec_from_file_location('ks6_predecessor_lo_core_r5_cx2v001', PREDECESSOR[0])
P = importlib.util.module_from_spec(_psp)          # KS6: 12d36305, unchanged; every non-S1_UA_C3T spec runs its code
sys.modules[_psp.name] = P
_psp.loader.exec_module(P)
STATE_SCHEMA = 'UNT_POINT_LO_STATE_INPUT_CX2V001'
CAP_SCHEMA = 'UNT_POINT_LO_CAPS_CX2V001'
OUTPUT_SCHEMA = 'UNT_POINT_LO_NUMERICAL_CX2V001'


def require_sha(value, name):
    if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('invalid SHA256: ' + name)


def reference(ref, *, schema=None):
    obj = CU.read_pin(ref)
    if schema is not None and obj.get('schema') != schema:
        raise ValueError('reference schema mismatch')
    return obj


def scope(obj, ctx):
    if obj.get('identity') != ctx['details']['identity'] or obj.get('custody') != ctx['details']['custody']:
        raise ValueError('point/custody mismatch')


def trusted_producer(obj, allowed):
    ref = obj.get('producer')
    if not isinstance(ref, dict) or ref.get('sha256') not in allowed:
        return False
    CU.read_pin(ref, document=False)
    return True


def row_values(row, ctx):
    contract = ctx['details']['row_contract']
    ids = [r['id'] for r in contract['rows']]
    radii = np.asarray([r['radius_m'] for r in contract['rows']], float)
    tau = np.asarray(contract['tau_km_s'], float)
    if row.get('row_ids') != ids or row.get('row_contract_sha256') != ctx['details']['custody']['row_contract_sha256']:
        raise ValueError('row order/custody mismatch')
    if not np.array_equal(np.asarray(row['R_m']), radii) or not np.array_equal(np.asarray(row['tau_km_s']), tau):
        raise ValueError('row radii/tau mismatch')
    v = PR.finite(row['v_reference_km_s'], 'row speeds')
    if v.shape != radii.shape:
        raise ValueError('row speed shape')
    PR.finite(radii, 'radii', positive=True)
    PR.finite(tau, 'tau', positive=True)
    return ids, radii, tau, np.abs(v)


def validate_tail_arrays(arrays, record, kept_k=4.0):
    """Validate tensor arrays before any arithmetic; cube/cylinder only. KS6: kept_k 3.0 for S1_UA_C3T only."""
    if record.get('empty') is not False:
        raise ValueError('nonempty saved state required')
    if record['kept'].get('shape') != 'cube' or record['kept'].get('K_inverse_kpc') != kept_k:
        raise ValueError('K4 cube required' if kept_k == 4.0 else 'K3 cube required (S1_UA_C3T)')
    if record['outer'].get('shape') != 'cylinder':
        raise ValueError('cylinder outer required')
    if any(k.startswith('sph_') for k in arrays):
        raise ValueError('sphere saved arrays unsupported')
    for key in ('kp', 'kz', 'wkp', 'wz'):
        PR.finite(arrays[key], key, positive=True)
        if arrays[key].ndim != 1:
            raise ValueError('non-vector ' + key)
    if arrays['wkp'].shape != arrays['kp'].shape or arrays['wz'].shape != arrays['kz'].shape:
        raise ValueError('quadrature shape')
    P, F = PR.finite(arrays['P'], 'P'), PR.finite(arrays['F'], 'F')
    if P.ndim != 2 or F.ndim != 2 or P.shape[0] != len(arrays['kp']) or F.shape != (len(arrays['kz']), P.shape[1]):
        raise ValueError('source factor shape')
    if np.iscomplexobj(P) and np.any(P.imag):
        raise ValueError('non-real radial factor')
    edges = PR.finite(arrays['shell_edges_inverse_kpc'], 'shell edges', positive=True)
    stored = PR.finite(arrays['shell_integrals'], 'shell integrals', nonnegative=True)
    if edges.ndim != 1 or np.any(np.diff(edges) <= 0) or edges[0] != kept_k or stored.shape != (len(edges) - 1, 3):
        raise ValueError('shell data shape/coverage')
    return edges


def recompute_b1(arrays, record, U, *, chunk=64, kept_k=4.0):
    """Recompute stored B1 independently from P/F and the module angular mask."""
    edges = validate_tail_arrays(arrays, record, kept_k)
    pref = float(record['lambda_scale']) / (4 * float(record['gamma_eff']) * (2 * math.pi) ** 3)
    if record.get('pref') != pref:
        raise ValueError('tail prefactor mismatch')
    PR.finite([pref, record['c_m_s']], 'pref/c', positive=True)
    kp, kz = arrays['kp'], arrays['kz']
    out = np.zeros(len(edges) - 1)
    for start in range(0, len(kp), chunk):
        sl = slice(start, min(start + chunk, len(kp)))
        k = kp[sl]
        source = arrays['P'][sl] @ arrays['F'].T
        c0 = U._c0_D(record['kept'], record['outer'], k * U.KPC_M, kz * U.KPC_M)
        if np.any(c0 < 0):
            raise ValueError('negative angular-domain measure')
        km = np.sqrt(k[:, None] ** 2 + kz[None, :] ** 2)
        fac = (pref * arrays['wkp'][sl] * k)[:, None] * arrays['wz'][None, :] / km ** 2
        weight = 2 * np.abs(source) * fac * c0 * km
        index = np.clip(np.searchsorted(edges, km * U.KPC_M, side='right') - 1, 0, len(out) - 1)
        out += np.bincount(index.ravel(), weights=weight.ravel(), minlength=len(out))
    PR.finite(out, 'recomputed B1', nonnegative=True)
    old = arrays['shell_integrals'][:, 1]
    # Exact zeros must stay zero. Tolerance concerns summation order only.
    if np.any((old == 0) != (out == 0)):
        raise ValueError('B1 zero support mismatch')
    relative = np.abs(out - old) / np.maximum(np.maximum(out, old), np.finfo(float).tiny)
    if np.max(relative) > 1e-10:
        raise ValueError('stored B1 does not reproduce from saved source factors')
    return np.maximum(old, out), dict(max_relative_difference=float(np.max(relative)),
                                      arithmetic='max(stored B1, recomputed B1); summation-order check 1e-10')


def aggregate_shares(rho_record, edges, B1, R, tau, speeds):
    """Map exact disjoint unit B1 shells into the declared rho-shell partition."""
    edges = PR.finite(edges, 'edges', positive=True)
    B1 = PR.finite(B1, 'B1', nonnegative=True)
    if edges.ndim != 1 or B1.shape != (len(edges) - 1,) or np.any(np.diff(edges) <= 0):
        raise ValueError('B1 shell dimensions')
    R, tau, speeds = (PR.finite(x, name, positive=(name in ('R', 'tau')), nonnegative=name == 'speeds')
                      for x, name in ((R, 'R'), (tau, 'tau'), (speeds, 'speeds')))
    if R.ndim != 1 or R.shape != tau.shape or R.shape != speeds.shape or not len(R):
        raise ValueError('row dimensions')
    rows = []
    used = np.zeros(len(B1), dtype=bool)
    for sh in rho_record['shells']:
        lo, hi = sh['range_inverse_kpc']
        take = (edges[:-1] >= lo) & (edges[1:] <= hi)
        if not take.any() or edges[:-1][take][0] != lo or edges[1:][take][-1] != hi:
            raise ValueError('B1 does not tile rho shell')
        if used[take].any():
            raise ValueError('duplicate LO shell consumption')
        used |= take
        rho = float(sh['rho_used'])
        PR.finite([rho], 'rho', nonnegative=True)
        b1 = float(B1[take].sum())
        ratios = speeds * R * rho * b1 / (4 * tau)
        PR.finite(ratios, 'LO ratios', nonnegative=True)
        rows.append(dict(range_inverse_kpc=[lo, hi], rho_used=rho, B1_per_m=b1,
                         per_row_over_tau=ratios.tolist(), max_over_tau=float(ratios.max()),
                         row_argmax_0based=int(np.argmax(ratios))))
    total = float(sum(s['max_over_tau'] for s in rows))
    threshold = all(s['max_over_tau'] <= .005 for s in rows) and total <= .05
    return dict(shells=rows, summed_max_over_tau=total,
                max_row_sum_over_tau=float(np.sum([s['per_row_over_tau'] for s in rows], axis=0).max()),
                numerical_thresholds_pass=threshold,
                all_nonzero_B1_consumed=bool(np.all(used | (B1 == 0))))


def base(ctx, kind):
    return dict(schema=OUTPUT_SCHEMA, gate='LO', kind=kind, utc=PR.utc(), status='TESTED',
        producer=CU.pin(__file__), response_producer=CU.pin(RESPONSE_PATH),
        identity=ctx['details']['identity'], point_sha256=ctx['details']['point_sha256'],
        custody=ctx['details']['custody'], production_admissible=False,
        cover_all_consumed_states=False, covers_all_consumed_states=False,
        rigorous_supremum=False, driver_certificate=None,
        limitations=['rho is a numerical maximum estimate; B1 is node quadrature',
                     'linear readout indicator only; no nonlinear/proper-volume closure',
                     'standalone evidence schema; not a driver slot certificate'])


def produce_current_lo(spec, state_ref, *, expected_state=None, trusted_source_producers=(),
                       trusted_review_hashes=(), settings='registered', shell_ranges=None,
                       context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.produce_current_lo(spec, state_ref, expected_state=expected_state,
                                    trusted_source_producers=trusted_source_producers,
                                    trusted_review_hashes=trusted_review_hashes, settings=settings,
                                    shell_ranges=shell_ranges, context=context, progress=progress)
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    obj = reference(state_ref, schema=STATE_SCHEMA)
    scope(obj, ctx)
    state = obj['state']
    blockers = []
    if expected_state is None:
        blockers.append('NO_INDEPENDENT_CONSUMED_STATE_EXPECTATION')
    elif state != expected_state:
        raise ValueError('consumed state differs from independently enumerated state')
    for key in ('state_sha256', 'source_sha256'):
        require_sha(state[key], key)
    tail = obj['tail_state']
    record = reference(tail['record'])
    CU.read_pin(tail['arrays'], document=False)
    with np.load(CU.allowed_path(tail['arrays']['path']), allow_pickle=False) as z:
        arrays = {k: z[k] for k in z.files}
    U, _, _ = CC.uvt_modules()
    st = U.TailState.from_arrays(arrays, record, expected_digest=state['state_sha256'])
    if record.get('roster_digest') != state['source_sha256'] or record.get('stage_kind') != state['stage_kind']:
        raise ValueError('source/stage digest mismatch')
    if record.get('outer') != spec['numerics']['uv_tail']['outer'] or record.get('gamma_eff') != ctx['B'].gam:
        raise ValueError('saved state physical/outer mismatch')
    if record.get('c_m_s') != CC.C or record.get('lambda_scale') != spec['numerics']['uv_tail']['lambda_scale']:
        raise ValueError('saved state physical prefactor mismatch')
    B1, b1check = recompute_b1(arrays, record, U, kept_k=float(PR.kept_k(spec)))   # KS6: the K=3 cube, edges from 3
    row = reference(obj['row_reference'], schema='UNT_POINT_LO_ROWS_CX2V001')
    if row.get('state_sha256') != state['state_sha256']:
        raise ValueError('rows belong to another state')
    ids, R, tau, speed = row_values(row, ctx)
    if not trusted_producer(row, trusted_source_producers):
        blockers.append('ROW_RECONSTRUCTION_PRODUCER_NOT_APPROVED')
    review_ref = row.get('policy_review')
    if not review_ref or review_ref.get('sha256') not in trusted_review_hashes:
        blockers.append('ROW_REFERENCE_POLICY_NOT_REVIEWED')
    else:
        review = reference(review_ref)
        if review.get('verdict') != 'APPROVED' or review.get('row_contract_sha256') != ctx['details']['custody']['row_contract_sha256']:
            blockers.append('ROW_REFERENCE_POLICY_REVIEW_SCOPE_MISMATCH')
    source_ref = obj.get('source_reconstruction')
    if source_ref is None:
        blockers.append('SOURCE_RECONSTRUCTION_MISSING')
    else:
        src = reference(source_ref, schema='UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001')
        scope(src, ctx)
        if src.get('state') != state or src.get('tail_state') != tail:
            raise ValueError('source reconstruction state/custody mismatch')
        expected_pf = CU.digest({k: CU.array_record(arrays[k]) for k in ('P', 'F')})
        if src.get('factor_arrays_sha256') != expected_pf:
            raise ValueError('reconstructed factor-array mismatch')
        refs = src.get('source_files', [])
        for ref in refs:
            CU.read_pin(ref, document=False)
        if not refs or src.get('complete_source_files') is not True or src.get('status') != 'TESTED' or src.get('verdict') != 'PASS':
            blockers.append('SOURCE_RECONSTRUCTION_INCOMPLETE')
        if not trusted_producer(src, trusted_source_producers):
            blockers.append('SOURCE_RECONSTRUCTION_PRODUCER_NOT_APPROVED')
        if src.get('i1t_verdict') != 'PASS' or record.get('i1t', {}).get('verdict') != 'PASS':
            blockers.append('I1T_NOT_ESTABLISHED')
    rho = PR.produce_rho(spec, settings=settings, shell_ranges=shell_ranges, context=ctx, progress=progress)
    shares = aggregate_shares(rho, arrays['shell_edges_inverse_kpc'], B1, R, tau, speed)
    if not rho['full_registered_search_executed']:
        blockers.append('FULL_POINT_RHO_NUMERICAL_SEARCH_UNTESTED')
    if not shares['all_nonzero_B1_consumed']:
        blockers.append('LO_SHELL_COVERAGE_INCOMPLETE')
    if not shares['numerical_thresholds_pass']:
        blockers.append('LO_NUMERICAL_INDICATOR_ABOVE_THRESHOLD')
    rec = base(ctx, 'CURRENT_SAVED_STATE')
    rec.update(state=state, state_input=state_ref, state_digest_verified=st.digest,
        B1_recomputed=b1check, rho=rho, row_ids=ids, v_reference_km_s=speed.tolist(),
        **shares, blockers=blockers,
        verdict='BLOCKED' if blockers else 'CURRENT_LO_NUMERICAL_EVIDENCE_REVIEW_REQUIRED',
        custody_verified_without_scientific_approval=True,
        seconds=time.monotonic() - start, peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return rec


def source_bound_J(radial_factors, column_rdr_m2, component_mass_caps_kg, *, c_m_s=CC.C,
                    stars_radial_kg=None, stars_multiplier_abs=0.0):
    """Pointwise finite-node majorant; cubic Lagrange radial factors may be signed.

    |S_gas(kp,kz)| <= c^2 sum_i |Pi_i(kp)| sum_components M_ci^max/(2 pi rdr_i).
    It holds for all z and signed component mixtures with bounded total
    variation masses. A stellar sech^2 vertical transform has modulus <= 1.
    This never substitutes the invalid generic bound |S_gas| <= c^2 M_gas.
    """
    P = PR.finite(radial_factors, 'radial factors')
    rdr = PR.finite(column_rdr_m2, 'rdr', positive=True)
    caps = PR.finite(component_mass_caps_kg, 'mass caps', nonnegative=True)
    if P.ndim != 2 or rdr.shape != (P.shape[1],) or caps.ndim != 2 or caps.shape[1] != P.shape[1]:
        raise ValueError('source cap shapes')
    PR.finite([c_m_s], 'c', positive=True)
    PR.finite([stars_multiplier_abs], 'stellar multiplier', nonnegative=True)
    bound = np.abs(P) @ (caps.sum(axis=0) / (2 * math.pi * rdr))
    if stars_radial_kg is not None:
        stars = PR.finite(stars_radial_kg, 'stellar radial factor')
        if stars.shape != (len(P),):
            raise ValueError('star radial shape')
        bound += float(stars_multiplier_abs) * np.abs(stars)
    elif stars_multiplier_abs:
        raise ValueError('stellar factor missing')
    return PR.finite(c_m_s ** 2 * bound, 'source envelope', nonnegative=True)


def validate_caps(cap, ctx):
    if cap.get('schema') != CAP_SCHEMA:
        raise ValueError('cap schema')
    scope(cap, ctx)
    n = 4 * (len(ctx['details']['geometry']['profile']['HI_plus_He']['s_edges_kpc2']) - 1)
    names = cap['component_names']
    if not names or len(names) != len(set(names)) or any(not isinstance(x, str) or not x for x in names):
        raise ValueError('component names')
    masses = PR.finite(cap['component_column_TV_mass_caps_kg'], 'component caps', nonnegative=True)
    if masses.shape != (len(names), n):
        raise ValueError('component cap dimension')
    if cap.get('mass_convention') != 'ACTUAL_PROPER_SOURCE_TOTAL_VARIATION_PER_COLUMN':
        raise ValueError('proper source mass convention required')
    PR.finite([cap['fixed_registered_stars_multiplier_abs']], 'stars cap', nonnegative=True)
    PR.finite([cap['gas_z_abs_max_m']], 'source extent', nonnegative=True)
    if cap['gas_z_abs_max_m'] > ctx['spec']['numerics']['uv_tail']['domain']['z_src_max_kpc'] * ctx['L'].KPC:
        raise ValueError('cap exceeds declared source extent')
    rows = cap['readout_caps']
    # The same shape/order contract as actual rows, with speed cap field explicit.
    row = dict(rows, v_reference_km_s=rows['speed_abs_max_km_s'])
    ids, R, tau, speed = row_values(row, ctx)
    PR.finite(rows['speed_abs_max_km_s'], 'speed cap', nonnegative=True)
    return masses, (ids, R, tau, speed)


def enforce_caps(cap, *, ctx, components, row_speeds_km_s, stars_multiplier_abs,
                 geometry_sha256, complete_source_roster):
    """Fail closed before EVERY constructed/consumed state, including monitor states.

    `components` must be reconstructed by the reviewed caller from actual
    source arrays, not caller-selected totals. Each named component supplies
    arrays elements_m_kg/elements_z_m for ALL registered radial columns.
    """
    masses, (_, _, _, vmax) = validate_caps(cap, ctx)
    if complete_source_roster is not True or geometry_sha256 != ctx['details']['custody']['geometry_sha256']:
        raise ValueError('incomplete source roster/geometry')
    if set(components) != set(cap['component_names']):
        raise ValueError('unaccounted source component')
    actual = []
    for name in cap['component_names']:
        c = components[name]
        mm, zz = c['elements_m_kg'], c['elements_z_m']
        if len(mm) != masses.shape[1] or len(zz) != len(mm):
            raise ValueError('source column count')
        row = []
        for m, z in zip(mm, zz):
            m, z = PR.finite(m, 'actual masses'), PR.finite(z, 'actual positions')
            if m.ndim != 1 or m.shape != z.shape or np.any(np.abs(z) > cap['gas_z_abs_max_m']):
                raise ValueError('source shape/extent cap violation')
            row.append(float(np.abs(m).sum()))
        actual.append(row)
    actual = np.asarray(actual)
    if np.any(actual > masses):
        raise ValueError('proper source TV mass cap violation')
    speed = np.abs(PR.finite(row_speeds_km_s, 'actual row speeds'))
    if speed.shape != vmax.shape or np.any(speed > vmax):
        raise ValueError('row speed cap violation')
    PR.finite([stars_multiplier_abs], 'actual star multiplier', nonnegative=True)
    if stars_multiplier_abs > cap['fixed_registered_stars_multiplier_abs']:
        raise ValueError('stellar source cap violation')
    return dict(status='TESTED', verdict='WITHIN_REVIEWED_CAPS', component_TV_masses_kg=actual.tolist(),
                row_speed_abs_km_s=speed.tolist(), scope='one complete supplied source roster; caller must enumerate every state')


def conditional_b1(ctx, cap, U, RS, PV):
    """Numerical envelope on EXACT production tensor nodes using actual Pi_i."""
    masses, _ = validate_caps(cap, ctx)
    uv = ctx['spec']['numerics']['uv_tail']
    kept = U.kept_region('route_a', None, 4 / U.KPC_M)
    grid = U._grid(kept, uv['outer'], uv['quadrature'], uv['domain']['R_eval_max_kpc'])
    kp, kz = grid['kp'] / U.KPC_M, grid['kz'] / U.KPC_M
    wkp, wz = grid['wkp'] / U.KPC_M, grid['wz'] / U.KPC_M
    profile = {'galaxies': {'DDO154': ctx['details']['geometry']['profile']}}
    edges = profile['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    R, rdr = RS.annulus_columns(edges, U.KPC_M)
    gas = RS.GasColumns(s_edges_kpc2=edges, kpc_m=U.KPC_M, M_s=uv['gas']['M_s'],
        column_R_m=R, column_rdr_m2=rdr, present=np.ones(len(R), bool),
        elements_z=[np.zeros(0) for _ in R], elements_m=[np.zeros(0) for _ in R])
    jn = PV.create_provider()
    star_p = None
    if cap['fixed_registered_stars_multiplier_abs']:
        stars = RS.stars_registered(profile, 'DDO154', units=dict(kpc_m=U.KPC_M, solar_mass_kg=ctx['L'].SEED['solar_mass_kg']))
        star_p = stars.radial_transform(kp, jn.j0)
    end = int(math.ceil(math.sqrt(2) * uv['outer']['K_big_inverse_kpc']))
    shell_edges = np.arange(4, end + 1, dtype=float)
    B1 = np.zeros(len(shell_edges) - 1)
    pref = uv['lambda_scale'] / (4 * ctx['B'].gam * (2 * math.pi) ** 3)
    maximum_source = 0.0
    for start in range(0, len(kp), 64):
        sl = slice(start, min(start + 64, len(kp)))
        P = gas.radial_factors(kp[sl], jn.j0)
        src = source_bound_J(P, rdr, masses,
            stars_radial_kg=None if star_p is None else star_p[sl],
            stars_multiplier_abs=cap['fixed_registered_stars_multiplier_abs'])
        maximum_source = max(maximum_source, float(src.max()))
        c0 = U._c0_D(kept, uv['outer'], grid['kp'][sl], grid['kz'])
        if np.any(c0 < 0):
            raise ValueError('negative angular measure')
        km = np.sqrt(kp[sl, None] ** 2 + kz[None, :] ** 2)
        weight = 2 * pref * (wkp[sl] * kp[sl] * src)[:, None] * wz[None, :] * c0 / km
        index = np.clip(np.searchsorted(shell_edges, km * U.KPC_M, side='right') - 1, 0, len(B1) - 1)
        B1 += np.bincount(index.ravel(), weights=weight.ravel(), minlength=len(B1))
    return shell_edges, B1, dict(N_perp=len(kp), N_z_plus=len(kz), maximum_source_envelope_J=maximum_source,
        quadrature='exact point production nodes; absolute Pi and actual proper-source TV caps',
        provider=jn.custody(), modules={k: CC.pin(k) for k in ('uvt_lapse', 'uvt_roster', 'uvt_jn')})


def produce_conditional_lo(spec, cap_ref=None, *, review_ref=None, trusted_review_hashes=(),
                           settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.produce_conditional_lo(spec, cap_ref, review_ref=review_ref, trusted_review_hashes=trusted_review_hashes,
                                        settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    raise ValueError('KS6: the retired prelaunch conditional LO path (A134 Q1/Q5) is not extended to S1_UA_C3T')
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    rec = base(ctx, 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE')
    blockers = []
    cap = None
    if cap_ref is None:
        blockers.append('REVIEWED_PROPER_SOURCE_AND_READOUT_CAPS_MISSING')
    else:
        cap = reference(cap_ref, schema=CAP_SCHEMA)
        validate_caps(cap, ctx)
    review = None
    if not review_ref or review_ref.get('sha256') not in trusted_review_hashes:
        blockers.append('CAP_REVIEW_NOT_IN_CALLER_TRUSTED_ALLOWLIST')
    else:
        review = reference(review_ref, schema='UNT_POINT_LO_CAP_REVIEW_CX2V001')
        scope(review, ctx)
        if review.get('cap_ref') != cap_ref or review.get('verdict') != 'APPROVED':
            blockers.append('CAP_REVIEW_SCOPE_OR_APPROVAL_MISMATCH')
        if review.get('producer_sha256') != CU.sha(__file__) or review.get('response_producer_sha256') != CU.sha(RESPONSE_PATH):
            blockers.append('CAP_REVIEW_PRODUCER_MISMATCH')
        en = review.get('enforcement', {})
        for key in ('every_constructed_and_consumed_state', 'reject_before_consume', 'complete_stage_inventory_reviewed'):
            if en.get(key) is not True:
                blockers.append('CAP_ENFORCEMENT_' + key.upper() + '_UNPROVEN')
        if not en.get('module'):
            blockers.append('REVIEWED_ENFORCEMENT_MODULE_MISSING')
        else:
            CU.read_pin(en['module'], document=False)
        if review.get('accepts_registered_numerical_rho_and_node_quadrature') is not True:
            blockers.append('NUMERICAL_LO_CONVENTION_NOT_REVIEWED')
        if review.get('proper_source_caps_valid_for_all_stage_rosters') is not True:
            blockers.append('PROPER_SOURCE_CAP_COVERAGE_UNPROVEN')
        if review.get('row_speed_and_uncertainty_policy_reviewed') is not True:
            blockers.append('READOUT_CAP_POLICY_UNREVIEWED')
    if blockers:
        rec.update(status='UNTESTED', verdict='BLOCKED', blockers=blockers, cap_ref=cap_ref,
                   review_ref=review_ref, numerical_envelope_executed=False,
                   seconds=time.monotonic() - start)
        return rec
    masses, (ids, R, tau, speed) = validate_caps(cap, ctx)
    U, RS, PV = CC.uvt_modules()
    edges, B1, node_info = conditional_b1(ctx, cap, U, RS, PV)
    rho = PR.produce_rho(spec, settings=settings, shell_ranges=shell_ranges, context=ctx, progress=progress)
    shares = aggregate_shares(rho, edges, B1, R, tau, speed)
    if not rho['full_registered_search_executed']:
        blockers.append('FULL_POINT_RHO_NUMERICAL_SEARCH_UNTESTED')
    if not shares['all_nonzero_B1_consumed']:
        blockers.append('PRELAUNCH_LO_COVERAGE_INCOMPLETE')
    if not shares['numerical_thresholds_pass']:
        blockers.append('CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD')
    covered = not blockers
    rec.update(verdict='BLOCKED' if blockers else 'CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED',
        blockers=blockers, cap_ref=cap_ref, review_ref=review_ref, numerical_envelope_executed=True,
        cover_all_consumed_states=covered, covers_all_consumed_states=covered,
        coverage_is_conditional=True, condition='reviewed enforcer rejects each constructed/consumed source or readout outside caps',
        rho=rho, **shares, row_ids=ids, node_envelope=node_info,
        seconds=time.monotonic() - start, peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return rec


def saved_b1_diagnostic(spec, legacy_ref, *, settings='smoke', shell_ranges=((4., 5.),), context=None):
    """Explicit legacy saved-source diagnostic. NEVER an accepted current-state proof.

    A fixed source and fixed row readouts allow B1 -> B1 gamma_old/gamma_new.
    This deliberately does not claim the old saved source solves the new point.
    Geometry must remain exactly the legacy DDO154 registered distance.
    """
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.saved_b1_diagnostic(spec, legacy_ref, settings=settings, shell_ranges=shell_ranges, context=context)
    raise ValueError('KS6: the legacy saved-source diagnostic is not extended to S1_UA_C3T')
    ctx = context or PR.point_context(spec)
    if spec['physical']['distance_Mpc'] != 4.04 or spec['physical']['inclination_deg'] != 66.0:
        raise ValueError('legacy diagnostic requires registered geometry')
    legacy = reference(legacy_ref)
    rho = PR.produce_rho(spec, settings=settings, shell_ranges=shell_ranges, context=ctx)
    gamma_old = CC.C ** 4 / (16 * math.pi * CC.G * 8.062327971755193)
    # Use the exact old evaluator gamma, not the rounded Qinf inference above.
    gamma_old = ctx['L'].ANCHOR_UNSCALED['common_scale_s'] * ctx['L'].ANCHOR_UNSCALED['gamma']
    scale = gamma_old / ctx['B'].gam
    by_range = {tuple(s['range_inverse_kpc']): s for s in legacy['shells']}
    edges = [rho['shells'][0]['range_inverse_kpc'][0]]
    b1 = []
    for sh in rho['shells']:
        old = by_range.get(tuple(sh['range_inverse_kpc']))
        if old is None:
            raise ValueError('legacy shell missing')
        edges.append(sh['range_inverse_kpc'][1])
        b1.append(old['B1_per_m'] * scale)
    shares = aggregate_shares(rho, np.asarray(edges), np.asarray(b1),
        np.asarray(legacy['R_kpc']) * ctx['L'].KPC, np.asarray(legacy['tau_km_s']), np.abs(legacy['v_state_km_s']))
    rec = base(ctx, 'FIXED_LEGACY_SOURCE_DIAGNOSTIC_ONLY')
    rec.update(verdict='BLOCKED', blockers=['CURRENT_POINT_SOLVED_STATE_ABSENT', 'SOURCE_FACTORS_NOT_RECONSTRUCTED',
        'LEGACY_ROW_REFERENCE_NOT_CALIBRATION_POLICY', 'FULL_POINT_LO_UNTESTED'], legacy_B1=legacy_ref,
        legacy_state_sha256=legacy['state_result_sha256'], fixed_source_B1_gamma_scale=scale,
        rho=rho, **shares)
    return rec


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--mode', choices=('current', 'conditional'), required=True)
    p.add_argument('--input-ref', help='JSON byte reference to state input or source-cap contract')
    p.add_argument('--review-ref', help='JSON byte reference to independently reviewed cap policy')
    p.add_argument('--trusted-review-sha', action='append', default=[])
    p.add_argument('--trusted-source-producer-sha', action='append', default=[])
    p.add_argument('--expected-state', help='JSON state identity from independent enumerator')
    p.add_argument('--settings', choices=tuple(PR.SETTINGS), default='registered')
    p.add_argument('--shells', help='JSON shell list; omission covers full point domain')
    a = p.parse_args()
    spec = json.loads(CU.allowed_path(a.spec).read_bytes())
    ref = None if a.input_ref is None else json.loads(a.input_ref)
    kwargs = dict(settings=a.settings, shell_ranges=None if a.shells is None else json.loads(a.shells),
                  trusted_review_hashes=a.trusted_review_sha,
                  progress=lambda x: print(json.dumps(x), flush=True))
    if a.mode == 'current':
        if ref is None:
            p.error('current mode requires --input-ref')
        rec = produce_current_lo(spec, ref, expected_state=None if a.expected_state is None else json.loads(a.expected_state),
                                 trusted_source_producers=a.trusted_source_producer_sha, **kwargs)
    else:
        rec = produce_conditional_lo(spec, ref, review_ref=None if a.review_ref is None else json.loads(a.review_ref), **kwargs)
    print(json.dumps(CU.write_new(a.out, rec)))


if __name__ == '__main__':
    main()
