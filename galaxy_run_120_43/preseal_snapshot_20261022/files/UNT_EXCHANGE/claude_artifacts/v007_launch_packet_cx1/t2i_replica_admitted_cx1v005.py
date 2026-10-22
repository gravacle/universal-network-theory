"""Gate T2-I (TAIL_SCHEME_DESIGN_V002 sec 1.3; R1 IA8; root A48 AMB-10): the nodes_v001 transform replicas applied to a COMPLETED
run's own rosters, compared with that run's STORED packet sources on G_ext \\ G_K (every extra node), per stage.  Read-only on the
run; writes one JSON (exclusive create).  numpy only; one process.  No row value, speed or velocity is read or written (RA13).

  route A   fixed stars (prep analytic J0 rings) vs START fixed_source_fourier_J; initial rings vs iteration-0 START gas;
            physical_source_fourier(elements_n) (elements from the checkpoint column records, solver L187-193) vs COMPLETED
            updated_gas_fourier_J for every completed iteration; the L215 mixture vs START gas_fourier_J for every n >= 1
  offset    the offset's Cartesian forward sum of the body base_integrated_source_J vs source_offset.npz new_body_fourier_J
            (this is the new-body part of the fs stages' packet as well)
  feedback  for every feedback stage of the run: the feedback ring J0 transform of its source rotation's rings vs its
            gas_source_feedback.npz new_gas_fourier_J (absent stages -> NOT_AVAILABLE, listed)
Required: max |replica - stored| / max |stored| <= 1e-12 per item, else UV_TAIL_TRANSFORM_REPLICA_MISMATCH (verdict FAIL).
Usage: python3 -I -B t2i_replica_check_c2v001.py RUN_DIR KEPT_SPEC_JSON OUT_JSON
  KEPT_SPEC_JSON: the kept composite grid spec (e.g. the C4T-D5 G4 spec); the ext grid is the run's own seed composite spec."""
import sys as _guard_sys
from pathlib import Path as _GuardPath
_guard_sys.path.insert(0, str(_GuardPath(__file__).parent))
import producer_guard_cx1v008 as _root_guard
_root_guard.admission(__file__)
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
import numpy as np
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
PINS = {'nodes': (X / 'tail_scheme_impl_c2/nodes_v001/lib/owned_uv_tail_nodes_v001.py', 'c8a04fb55f6c388c7cc5b735cb0e19222836c49acfce46d846198951593be551'), 'roster': (X / 'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'), 'provider': (X / 'tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'), 'checkpoint': (X / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'), 'kernel': (X / 'annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py', '2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e'), 'profile': (ROOT / 'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b')}
TOL = 1e-12
C = 299792458.0

@_root_guard.guarded
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()

@_root_guard.guarded
def load(name):
    p, s = PINS[name]
    if sha(p) != s:
        raise SystemExit('PIN ' + str(p))
    sp = importlib.util.spec_from_file_location('t2i_' + name, str(p))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m

@_root_guard.guarded
def blob(cdir, ref):
    p = Path(cdir) / ref['blob']
    if sha(p) != ref['file_sha256']:
        raise SystemExit('blob sha ' + str(p))
    return np.load(p, mmap_mode='r', allow_pickle=False)

@_root_guard.guarded
def rel(a, b):
    return float(np.max(np.abs(a - b)) / np.max(np.abs(b)))

@_root_guard.guarded
def roster_and_rings(ni, prof_all, kern):
    kpc = ni['kpc_m']
    gas = prof_all['galaxies']['DDO154']['HI_plus_He']
    edges = [float(x) for x in gas['s_edges_kpc2']]
    means = [float(x) for x in gas['annular_means_Msun_pc2']]
    controls = [float(x) for x in gas['boundary_controls_Msun_pc2']]
    sigma_unit = ni['solar_mass_kg'] / (kpc / 1000) ** 2
    hi = dict(sigma0_m_s=11000.0, gamma=5 / 3, search_step_m=ni['hi_search_step_kpc'] * kpc, search_limit_m=ni['hi_search_limit_kpc'] * kpc, root_tolerance_m=ni['hi_root_tolerance_kpc'] * kpc, log_lapse_tolerance=ni['hi_log_lapse_tolerance'], max_metric_calls=ni['hi_max_metric_calls'], panels_per_side=ni['hi_panels_per_side'])
    gx, gw = np.polynomial.legendre.leggauss(ni['source_gauss_order'])
    n_az = ni['source_azimuth_count']
    phis = [2 * math.pi * i / n_az for i in range(n_az)]
    dphi = 2 * math.pi / n_az
    roster = []
    for lo, hi_ in zip(edges, edges[1:]):
        for x, w in zip(gx, gw):
            s = (lo + hi_) / 2 + (hi_ - lo) * float(x) / 2
            R = math.sqrt(s) * kpc
            dR = (hi_ - lo) * float(w) * kpc * kpc / (4 * R)
            p = kern.annular_bernstein_sigma(s_edges=edges, annular_means=means, boundary_controls=controls, s_query=[float((R / kpc) ** 2)])
            Sig = float(p['sigma'][0]) * sigma_unit
            if Sig == 0:
                continue
            for phi in phis:
                roster.append(dict(R_m=R, phi=phi, radial_weight_m=dR, azimuth_weight_rad=dphi, Sigma_kg_m2=Sig, hi_options=dict(hi)))
    rings = dict(R=np.array([c['R_m'] for c in roster if c['phi'] == phis[0]]), z=np.zeros(sum((c['phi'] == phis[0] for c in roster))), m=np.array([c['Sigma_kg_m2'] * c['R_m'] * c['radial_weight_m'] * (2 * math.pi) for c in roster if c['phi'] == phis[0]]))
    return (roster, rings)

@_root_guard.guarded
def main():
    run, kept_spec_path, out = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    t0 = time.monotonic()
    nl, rs, pv, ck, kern = (load('nodes'), load('roster'), load('provider'), load('checkpoint'), load('kernel'))
    if sha(PINS['profile'][0]) != PINS['profile'][1]:
        raise SystemExit('profile pin')
    prof_all = json.loads(PINS['profile'][0].read_text())
    jn = pv.create_provider()
    ni = json.loads((run / 'inputs/seed_c2v001.json').read_text())['numerical_inputs']
    kept = json.loads(kept_spec_path.read_text())
    ctx = nl.ext_context(ext_spec=ni['composite_grid_spec'], kept_spec=kept, kpc_m=ni['kpc_m'])
    ax = ctx['axis']
    N = len(ax)
    m3 = ctx['mask3']

    @_root_guard.guarded
    def ext(a):
        return np.ascontiguousarray(np.asarray(a[:, 0, 0]).reshape(N, N, N)[m3])
    items = {}
    stages = {d.name: d for d in sorted((run / 'stages').iterdir()) if d.is_dir()}
    ra = next((d for n, d in stages.items() if n.endswith('_route_a')), None)
    if ra is None:
        admitted = (json.loads((run / 'result.json').read_bytes()).get('identity') or {}).get('route_a') or {}
        if admitted.get('checkpoint'):
            ra = Path(admitted['checkpoint']).parent
    if ra is not None and (ra / 'checkpoint/IDENTITY.json').is_file():
        cdir = ra / 'checkpoint'
        ident = json.loads((cdir / 'IDENTITY.json').read_text())['identity']
        roster, rings = roster_and_rings(ni, prof_all, kern)
        roster_ok = ck.digest(roster) == ident['inputs_sha256']['gas_columns']
        s0 = json.loads((cdir / 'iteration_0000/START.json').read_text())
        waves_ok = bool(np.array_equal(np.asarray(blob(cdir, s0['prepared_wavevectors'])), nl.tensor_waves(ax)))
        star_rings = rs.stars_gl4_rings(prof_all, 'DDO154', kpc_m=ni['kpc_m'], solar_mass_kg=ni['solar_mass_kg'], gauss_order=ni['source_gauss_order'])
        fix = nl.extract_ext(nl.ring_transform_tensor(ax, star_rings['R'], star_rings['z'], star_rings['m'], C, jn.j0), m3)
        items['route_a.fixed_stars'] = rel(fix, ext(blob(cdir, s0['fixed_source_fourier_J'])))
        init = nl.extract_ext(nl.ring_transform_tensor(ax, rings['R'], rings['z'], rings['m'], C, jn.j0), m3)
        items['route_a.initial_rings'] = rel(init, ext(blob(cdir, s0['gas_fourier_J'])))
        r = float(ni['relaxation'])
        upd = []
        its = sorted((int(p.name.split('_')[1]) for p in cdir.glob('iteration_*') if (p / 'COMPLETED.json').is_file()))
        for it in its:
            d = cdir / ('iteration_%04d' % it)
            pos = []
            J = []
            for k, col in enumerate(roster):
                res = ck.decode(json.loads((d / ('column_%05d.json' % k)).read_text())['result'])
                for node, e in zip(res['nodes'], res['source_quadrature']['elements']):
                    pos.append([col['R_m'] * math.cos(col['phi']), col['R_m'] * math.sin(col['phi']), node['z_m']])
                    J.append(-e['rho_kg_m3'] * C * C * e['proper_volume_m3'])
            u = nl.extract_ext(nl.point_transform_tensor(ax, np.array(pos), np.array(J)), m3)
            upd.append(u)
            done = json.loads((d / 'COMPLETED.json').read_text())
            items['route_a.updated_%04d' % it] = rel(u, ext(blob(cdir, done['updated_gas_fourier_J'])))
            nxt = cdir / ('iteration_%04d' % (it + 1)) / 'START.json'
            if nxt.is_file():
                coeff = [1.0]
                for _ in range(it + 1):
                    coeff = [(1 - r) * q for q in coeff] + [r]
                g = coeff[0] * init
                for q, x in zip(coeff[1:], upd):
                    g = g + q * x
                items['route_a.mixture_%04d' % (it + 1)] = rel(g, ext(blob(cdir, json.loads(nxt.read_text())['gas_fourier_J'])))
        items_meta = {'route_a': dict(roster_digest_equals_identity=roster_ok, waves_equal_ext_tensor=waves_ok, iterations=its)}
    else:
        items_meta = {'route_a': 'NOT_AVAILABLE (no computed route-A checkpoint in this run)'}
    off = next((d for n, d in stages.items() if n.endswith('_offset')), None)
    if off is not None and (off / 'offset/finish.json').is_file():
        fin = json.loads((off / 'offset/finish.json').read_text())
        so = fin['outputs']['source_offset.npz']
        req = json.loads((off / 'request.json').read_text())['argv']
        bdir = Path(req[req.index('--body-directory') + 1])
        bf = json.loads((bdir / 'finish.json').read_text())
        if sha(so['path']) != so['sha256'] or sha(bf['array_file']) != bf['array_sha256']:
            raise SystemExit('offset/body pins')
        with np.load(bf['array_file'], allow_pickle=False) as f:
            pos = f['physical_positions_m'].reshape(-1, 3).copy()
            J = f['base_integrated_source_J'][..., 0, 0].reshape(-1).copy()
        nb = nl.extract_ext(nl.point_transform_tensor(ax, pos, J), m3)
        with np.load(so['path'], allow_pickle=False) as f:
            items['offset.new_body'] = rel(nb, ext(f['new_body_fourier_J']))
        items_meta['offset'] = dict(body_directory=str(bdir), elements=int(len(J)))
    else:
        items_meta['offset'] = 'NOT_AVAILABLE'
    fbs = [d for n, d in stages.items() if n.endswith('_feedback')]
    items_meta['feedback'] = [] if fbs else 'NOT_AVAILABLE (no feedback stage in this run)'
    for d in fbs:
        req = json.loads((d / 'request.json').read_text())['argv']
        rot = Path(req[req.index('--rotation-directory') + 1])
        out_d = next((p for p in d.iterdir() if p.is_dir()))
        with np.load(rot / 'rotation_base_arrays.npz', allow_pickle=False) as f:
            arr = {k: f[k].copy() for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}
        mm = np.sum(arr['volume_weights_m3'] * arr['rho0'], axis=1)
        Rg = np.repeat(arr['radial_nodes_m'], arr['z'].shape[2])
        zg = arr['z'][:, 0, :].reshape(-1)
        fb = nl.extract_ext(nl.ring_transform_tensor(ax, Rg, zg, mm.reshape(-1), C, jn.j0), m3)
        with np.load(out_d / 'gas_source_feedback.npz', allow_pickle=False) as f:
            items['feedback.%s' % d.name] = rel(fb, ext(f['new_gas_fourier_J']))
        items_meta['feedback'].append(d.name)
    worst = max(items.values()) if items else None
    verdict = 'PASS' if items and worst <= TOL and (not isinstance(items_meta['route_a'], dict) or (items_meta['route_a']['roster_digest_equals_identity'] and items_meta['route_a']['waves_equal_ext_tensor'])) else 'FAIL'
    rec = {'schema': 'UNT_UV_TAIL_T2I_REPLICA_CHECK_C2V001', 'tool': [str(Path(__file__).resolve()), sha(__file__)], 'pins': {k: [str(p), s] for k, (p, s) in PINS.items()}, 'run': str(run), 'kept_spec': json.loads(kept_spec_path.read_text()), 'ext_context': ctx['record'], 'items_max_rel': items, 'meta': items_meta, 'rtol': TOL, 'worst': worst, 'verdict': verdict, 'refusal': None if verdict == 'PASS' else 'UV_TAIL_TRANSFORM_REPLICA_MISMATCH', 'seconds': round(time.monotonic() - t0, 1), 'blinding': 'transform residuals only; no row value, speed or velocity is read or written'}
    _root_guard.check_run_path(out, allow_registered=False)
    with open(out, 'x') as f:
        json.dump(_root_guard.stamp(rec, __file__), f, indent=1)
    print(json.dumps(_root_guard.stamp({'verdict': verdict, 'worst': worst, 'n_items': len(items)}, __file__)))
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    import producer_guard_cx1v008 as guard
    guard.authorize(sys.argv, 'run')
    main()
