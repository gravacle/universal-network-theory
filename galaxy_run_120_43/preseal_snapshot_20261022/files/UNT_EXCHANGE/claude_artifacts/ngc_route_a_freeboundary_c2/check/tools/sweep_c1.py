"""CHECKER: roster rebuild + validation + full replay of unsolved iteration-0 columns.
usage: sweep_c1.py validate | sweep_c1.py shard K N
Diagnostics only; no run; writes only under check/out/.
"""
import json, math, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import replay_c1 as C

OUT = Path(__file__).resolve().parent.parent/'out'; OUT.mkdir(exist_ok=True)
BASE = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
PROFILE = BASE/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'
KERNEL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py')


def roster(ctx):
    """Transcription of prep v001:104-125,162-179 (HI columns only)."""
    pins = ctx.caller['code_pins']
    kern = C.load(KERNEL, C.sha(KERNEL), 'kern')
    prof = json.loads(PROFILE.read_text())['galaxies']['NGC3198']['HI_plus_He']
    ni = ctx.caller['numerical_controls']
    kpc = ni['kpc_m']; sigma_unit = ni['solar_mass_kg']/((kpc/1000)**2)
    edges = [float(x) for x in prof['s_edges_kpc2']]; means = [float(x) for x in prof['annular_means_Msun_pc2']]
    ctrls = [float(x) for x in prof['boundary_controls_Msun_pc2']]
    hio = dict(sigma0_m_s=11000., gamma=5/3, search_step_m=ni['hi_search_step_kpc']*kpc,
               search_limit_m=ni['hi_search_limit_kpc']*kpc, root_tolerance_m=ni['hi_root_tolerance_kpc']*kpc,
               log_lapse_tolerance=ni['hi_log_lapse_tolerance'], max_metric_calls=ni['hi_max_metric_calls'],
               panels_per_side=ni['hi_panels_per_side'])
    gx, gw = np.polynomial.legendre.leggauss(ni['source_gauss_order'])
    na = ni['source_azimuth_count']; phis = [2*math.pi*i/na for i in range(na)]; dphi = 2*math.pi/na
    cols = []
    for lo, hi in zip(edges, edges[1:]):
        for x, w in zip(gx, gw):
            x = float(x); w = float(w)
            s = (lo+hi)/2+(hi-lo)*x/2; R = math.sqrt(s)*kpc; dR = (hi-lo)*w*kpc*kpc/(4*R)
            p = kern.annular_bernstein_sigma(s_edges=edges, annular_means=means, boundary_controls=ctrls, s_query=[float((R/kpc)**2)])
            if not p['ok']: raise SystemExit('kernel fail')
            sig = float(p['sigma'][0])*sigma_unit
            if sig == 0: continue
            for phi in phis:
                cols.append(dict(R_m=R, phi=phi, radial_weight_m=dR, azimuth_weight_rad=dphi, Sigma_kg_m2=sig, hi_options=dict(hio)))
    return cols


def outcome(ctx, col, **kw):
    try:
        r = ctx.solve(col, **kw)
        return {'ok': True, 'roots_m': r['roots_m'], 'calls': r['metric_calls']}
    except ValueError as e:
        m = str(e); return {'ok': False, 'msg': m}


def side_max(ctx, col, sgn, lim_kpc, th):
    step = col['hi_options']['search_step_m']; lim = lim_kpc*C.KPC; d = 0.0
    l0 = ctx.lnN(col['R_m'], col['phi'], 0.0); best = -1e300; zbest = None; cross = None
    while d < lim:
        d = min(lim, d+step); v = ctx.lnN(col['R_m'], col['phi'], sgn*d)-l0
        if v > best: best = v; zbest = d/C.KPC
        if cross is None and v >= th: cross = d/C.KPC
    return {'max': best, 'zmax_kpc': zbest, 'first_cross_kpc': cross}


def validate():
    ctx = C.Ctx(); cols = roster(ctx)
    rep = {'n_cols': len(cols)}
    rep['roster_digest_equals_identity'] = ctx.ckm.digest(cols) == ctx.idn['inputs_sha256']['gas_columns']
    raw, f = C.failure_record()
    rep['roster_2503_equals_failure_inputs'] = (cols[2503] == f['column_inputs'])
    th = C.threshold()
    # completed-column input digests and bitwise re-solves
    bad = 0
    for i in range(2503):
        rec = json.loads((C.IT0/('column_%05d.json' % i)).read_text())
        if rec['column_input_sha256'] != ctx.ckm.digest(cols[i]): bad += 1
    rep['completed_input_digest_mismatches'] = bad
    resolve = {}
    for i in (0, 1, 517, 1234, 2000, 2495, 2496, 2497, 2501, 2502):
        rec = json.loads((C.IT0/('column_%05d.json' % i)).read_text())
        old = C.dec(rec['result']); new = ctx.solve(cols[i])
        resolve[str(i)] = {'equal': old == new, 'digest_equal': ctx.ckm.digest(new) == ctx.ckm.digest(old),
                           'roots_kpc': [x/C.KPC for x in new['roots_m']], 'calls': new['metric_calls']}
    rep['bitwise_resolve'] = resolve
    # total HI quadrature mass and ring radii
    m = np.array([c['Sigma_kg_m2']*c['R_m']*c['radial_weight_m']*c['azimuth_weight_rad'] for c in cols])
    rep['total_mass_Msun'] = float(m.sum()/1.98847e30)
    # midplane lnN(R) along phi=0 and far points (asymptote)
    mid = {}
    for Rk in (2, 10, 20, 30, 40, 46, 50, 52.655, 60, 80, 100, 136, 200, 400, 1000, 3000):
        mid[str(Rk)] = ctx.lnN(Rk*C.KPC, 0.0, 0.0)
    rep['midplane_lnN_phi0'] = mid
    # completed-column root maxima
    rmax = 0.0; rmax_i = None
    for i in range(2503):
        rec = C.dec(json.loads((C.IT0/('column_%05d.json' % i)).read_text())['result'])
        r = max(abs(x) for x in rec['roots_m'])/C.KPC
        if r > rmax: rmax = r; rmax_i = i
    rep['completed_max_root_kpc'] = [rmax, rmax_i]
    (OUT/'VALIDATE_C1.json').write_text(json.dumps(rep, indent=1, default=str))
    print(json.dumps(rep, indent=1, default=str))


def shard(k, n):
    ctx = C.Ctx(); cols = roster(ctx); th = C.threshold()
    path = OUT/('sweep_%d_of_%d.jsonl' % (k, n))
    with path.open('w') as fo:
        for i in range(2503, len(cols)):
            if (i-2503) % n != k: continue
            col = cols[i]; t = time.time()
            rec = {'i': i, 'R_kpc': col['R_m']/C.KPC, 'phi': col['phi'],
                   'mass_kg': col['Sigma_kg_m2']*col['R_m']*col['radial_weight_m']*col['azimuth_weight_rad'],
                   'lnN0': ctx.lnN(col['R_m'], col['phi'], 0.0),
                   'd95': outcome(ctx, col),
                   'd136': outcome(ctx, col, search_limit_m=136.5*C.KPC, max_metric_calls=2048)}
            if not rec['d95']['ok']:
                rec['plus500'] = side_max(ctx, col, 1, 500.0, th); rec['minus500'] = side_max(ctx, col, -1, 500.0, th)
            rec['s'] = time.time()-t
            fo.write(json.dumps(rec)+'\n'); fo.flush()


if __name__ == '__main__':
    if sys.argv[1] == 'validate': validate()
    else: shard(int(sys.argv[2]), int(sys.argv[3]))
