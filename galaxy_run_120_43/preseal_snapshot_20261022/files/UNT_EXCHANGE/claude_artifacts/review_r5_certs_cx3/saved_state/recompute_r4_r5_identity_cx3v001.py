"""Independent saved-body tail-build identity review; no forward stage or target reads."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import time
import numpy as np

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
TAIL = BASE / 'tail_scheme_impl_c2'
OUT = Path(__file__).parent
PINS = {}
CHECKS = []

def guard(path):
    p = Path(path)
    resolved = str(p.resolve())
    if '/runs_ext/UVT_' in resolved or 'KMAX_A2F10_C5H_RUN_V001' in resolved:
        raise RuntimeError('prohibited input')
    return p

def pin(path, expected=None):
    p = guard(path)
    h = hashlib.sha256()
    with p.open('rb') as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    got = h.hexdigest()
    if expected is not None and got != expected:
        raise RuntimeError('input pin mismatch: ' + str(p))
    PINS[str(p)] = got
    return p

def mod(name, path, expected):
    p = pin(path, expected)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    pin(p, expected)
    return m

def check(name, passed, **details):
    CHECKS.append(dict(name=name, status='TESTED', passed=bool(passed), **details))
    if not passed:
        raise AssertionError(name)

def same(a, b):
    return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()

def arr_info(a):
    return dict(shape=list(a.shape), dtype=str(a.dtype), bytes=int(a.nbytes),
                sha256=hashlib.sha256(a.tobytes()).hexdigest())

def main():
    started = time.monotonic()
    utc = subprocess.check_output(['date', '-u'], text=True).strip()
    env = {k: os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')}
    check('single_thread_environment', all(v == '1' for v in env.values()), environment=env)
    pin(__file__)
    old = mod('cx3_old_tail', TAIL / 'module/owned_uv_tail_lapse_v001.py', 'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22')
    new = mod('cx3_new_tail', TAIL / 'driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
    rs = mod('cx3_roster', TAIL / 'module/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2')
    pv = mod('cx3_provider', TAIL / 'module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')
    pin(rs.FORWARD_V002, rs.FORWARD_V002_SHA)
    manifest = json.loads(pin(TAIL / 'route_b/fixtures/rp2_route_a_on_manifest.json').read_bytes())
    cfg_raw = json.loads(pin(TAIL / 'route_b/fixtures/rp2_cfg_on.json').read_bytes())
    record = manifest['state']['record']
    check('saved_fixture_is_nonproduction', record['production_admissible'] is False and record['roster_record']['kind'] == 'synthetic')
    ap = pin(manifest['state']['arrays']['path'], manifest['state']['arrays']['sha256'])
    with np.load(ap, allow_pickle=False) as f:
        radii = f['ring_radii_m'].copy()
    body_pin = record['roster_record']['provenance']['body_arrays']
    bp = pin(body_pin['path'], body_pin['sha256'])
    with np.load(bp, allow_pickle=False) as f:
        body = dict(physical_positions_m=f['physical_positions_m'].reshape(-1, 3).copy(),
                    base_integrated_source_J=f['base_integrated_source_J'][..., 0, 0].reshape(-1).copy())
    profile_path = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json')
    prof = json.loads(pin(profile_path, 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b').read_bytes())
    units = {k: record['roster_record']['stars'][k] for k in ('kpc_m', 'solar_mass_kg')}
    states = []
    build_seconds = []
    for tag, lib in (('r4', old), ('r5', new)):
        stars = rs.stars_registered(prof, 'DDO154', units=units)
        roster = rs.roster_body(body, stars, s_edges_kpc2=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],
                               kpc_m=units['kpc_m'], M_s=cfg_raw['gas']['M_s'], c_m_s=record['c_m_s'])
        roster.kind = 'synthetic'
        roster.provenance = record['roster_record']['provenance']
        cfg = lib.normalize_config(cfg_raw)
        check(tag + '_config_matches_saved', cfg['sha256'] == manifest['config_sha256'])
        t = time.monotonic()
        print(tag + ' nonempty saved-body build starting', flush=True)
        st = lib.build(config=cfg, kept=record['kept'], roster=roster, gamma_eff=record['gamma_eff'],
                       c_m_s=record['c_m_s'], eval_radii_m=radii, jn_provider=pv.create_provider(),
                       i1t=record['i1t'], stage_kind=record['stage_kind'])
        build_seconds.append(time.monotonic() - t)
        states.append(st)
        check(tag + '_nonempty_under_old_cap', not st.empty and st.record['memory_estimate_bytes'] < old.TAIL_MEMORY_CAP_BYTES,
              memory_estimate_bytes=st.record['memory_estimate_bytes'], old_cap_bytes=old.TAIL_MEMORY_CAP_BYTES)
        check(tag + '_saved_roster_identity', st.record['roster_digest'] == record['roster_digest'])
        print(tag + ' complete: ' + st.digest, flush=True)
    a, b = states
    check('records_equal', a.record == b.record)
    check('state_digest_equal', a.digest == b.digest, r4=a.digest, r5=b.digest)
    check('state_array_names_equal', a._a.keys() == b._a.keys())
    arrays = {}
    for k in sorted(a._a):
        check('array_bitwise_' + k, same(a._a[k], b._a[k]))
        arrays[k] = arr_info(a._a[k])
    # Also compare every state array against the pinned historical saved fixture.
    historical = {}
    with np.load(ap, allow_pickle=False) as f:
        check('historical_array_names_equal', sorted(f.files) == sorted(a._a))
        for k in sorted(a._a):
            historical[k] = same(a._a[k], f[k])
    check('historical_saved_array_identity', all(historical.values()), arrays=historical)
    # Registered radii, axis, and one on-demand radius; asymmetric z and phi exercise all jet terms.
    kpc = units['kpc_m']
    positions = np.array([[0., 0., 0.], [radii[0], 0., .23*kpc],
                          [radii[len(radii)//2]/np.sqrt(2), radii[len(radii)//2]/np.sqrt(2), -.37*kpc],
                          [.731*kpc, .419*kpc, .123*kpc]])
    jet_hashes = {}
    for order in (1, 2):
        ja, jb = a.jet(positions, order), b.jet(positions, order)
        for k in sorted(ja):
            check('jet_order_%s_%s' % (order, k), same(ja[k], jb[k]) and np.all(np.isfinite(ja[k])))
            jet_hashes['order_%s_%s' % (order, k)] = arr_info(ja[k])
        check('jet_order_%s_nonzero_field_gradient' % order,
              np.any(ja['boundary_fields']) and np.any(ja['boundary_gradient']))
    check('second_order_nonzero_hessian', np.any(ja['boundary_hessian']))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    check('rss_below_8GB', rss < 8 * 2**30, max_rss_bytes=rss)
    result = dict(schema='CX3_R4_R5_SAVED_BODY_IDENTITY_V001', verdict='PASS', date_u=utc,
                  completion_date_u=subprocess.check_output(['date','-u'], text=True).strip(),
                  scope='Nonempty tail-ON library builds from pinned DDO154 saved body fixture, K=2 cube to K_big=32 cylinder, gas M_s=64; synthetic fixture is not a production route-A mixture. No forward, route-A, or route-B run.',
                  untested=['Production stage execution', 'UVT identity runs (principal read prohibition)', 'Other source states/geometries'],
                  input_pins=PINS, checks=CHECKS, count=len(CHECKS), arrays=arrays, jet_hashes=jet_hashes,
                  points_m=positions.tolist(), state_digest=a.digest, historical_saved_digest=manifest['state']['digest'],
                  historical_record_equal=a.record == record, build_seconds=build_seconds,
                  elapsed_seconds=time.monotonic()-started, max_rss_bytes=rss)
    target = OUT / 'RESULTS_V001.json'
    with target.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False); f.write('\n')
    print(json.dumps(dict(verdict='PASS', checks=len(CHECKS), result=str(target), sha256=hashlib.sha256(target.read_bytes()).hexdigest(), elapsed_seconds=result['elapsed_seconds'], max_rss_bytes=rss)), flush=True)

if __name__ == '__main__':
    main()
