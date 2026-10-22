"""Claude2-review independent T120L iteration-0 re-check (saved-state only; no worker, no solve, no gas iteration).
Differs from Codex3 replay_t120l_cx3v002.py on purpose:
  * the prep arguments are produced by the v011 DRIVER's own seed construction (normalize_spec + _ngc_v011_seed on
    CALL_NGC_V011_A_CX3V003.json), not hand-edited from the base seed;
  * the T120L grid is also rebuilt here from first principles (numpy leggauss on the registered panels), independent of
    ngc_grid_cut_cx3v001.tensor_grid;
  * the operator is recomputed only on three sampled 48,000-node blocks (first, a seeded middle block, last).
usage: t120l_recheck_c2r.py OUT_JSON
"""
import hashlib
import importlib.util
import json
import os
import resource
import sys
import time
from pathlib import Path

for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    if os.environ.get(k) != '1':
        raise SystemExit('set %s=1 for bitwise reproduction' % k)
import numpy as np

A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
S = A / 'ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr'
DRV = A / 'ngc_route_tail_readiness_cx3/v011/galaxy_m0_forward_c2v011_cx3v003.py'
DRV_SHA = 'd120eead0e424d5ae0c2e4854377f2808f258646a7fefdaba5c66f105f5e610b'
CALL_A = A / 'ngc_route_tail_readiness_cx3/v011/CALL_NGC_V011_A_CX3V003.json'
BASE = (A / 'ngc_route_impl_c2/route_a/install/recovered_packet_audit/owned_physical_fourier_metric_quadrature_v005.py',
        '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491')
OPERATOR_SHA = 'e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(p, name, pin=None):
    if pin is not None and sha(p) != pin:
        raise SystemExit('PIN ' + str(p))
    s = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


checks = []


def bit(name, a, b):
    a = np.asarray(a); b = np.asarray(b)
    ok = a.shape == b.shape and a.dtype == b.dtype and a.tobytes() == b.tobytes()
    rec = {'name': name, 'bitwise_equal': bool(ok), 'shape': list(a.shape), 'dtype': a.dtype.str}
    if not ok and a.shape == b.shape:
        rec['max_abs_diff'] = float(np.max(np.abs(a - b)))
    checks.append(rec)
    print(name, ok, flush=True)
    return ok


def main():
    out = Path(sys.argv[1])
    assert not out.exists()
    t0 = time.monotonic()
    assert sha(S / 'OPERATOR.json') == OPERATOR_SHA
    man = json.loads((S / 'PREP.json').read_text()); op = json.loads((S / 'OPERATOR.json').read_text())
    drv = load(DRV, 'v011_review_import', DRV_SHA)
    nspec = drv.normalize_spec(json.loads(CALL_A.read_bytes()))
    seed = drv._ngc_v011_seed(nspec)
    ni = seed['numerical_inputs']
    # first-principles T120L grid
    br = [-2, -1, -.3, -.1, -.03, -.01, 0, .01, .03, .1, .3, 1, 2]
    orders = {'x': [22, 16, 8, 5, 6, 3, 3, 6, 5, 8, 16, 22], 'z': [14, 10, 5, 3, 6, 2, 2, 6, 3, 5, 10, 14]}
    orders['y'] = orders['x']
    kpc = ni['kpc_m']
    ax, aw = {}, {}
    for k in 'xyz':
        xs, ws = [], []
        for lo, hi, n in zip(br[:-1], br[1:], orders[k]):
            g, w = np.polynomial.legendre.leggauss(n)
            xs.append(((lo + hi) / 2 + (hi - lo) * g / 2) / kpc); ws.append((hi - lo) * w / (2 * kpc))
        ax[k] = np.concatenate(xs); aw[k] = np.concatenate(ws)
    mine_k = np.array([(x, y, z) for x in ax['x'] for y in ax['y'] for z in ax['z']])
    mine_w = np.array([x * y * z for x in aw['x'] for y in aw['y'] for z in aw['z']])
    ref_k = np.load(S / 'k_physical.npy', mmap_mode='r'); ref_w = np.load(S / 'dk_weights.npy', mmap_mode='r')
    bit('first_principles_k_physical_vs_saved', mine_k, ref_k)
    bit('first_principles_dk_weights_vs_saved', mine_w, ref_w)
    # driver-built seed -> successor prep
    prep_path = Path(drv.V011_PINS['prep'][0])
    prep = load(prep_path, 'v011_review_prep', drv.V011_PINS['prep'][1])
    data = prep.prepare_inputs(**ni)
    t_prep = time.monotonic() - t0
    fa = data['fourier_arguments']
    current = data['fixed_source_fourier_J'] + data['initial_gas_fourier_J']
    arrays = dict(k_physical=fa['k_physical'], dk_weights=fa['dk_weights'], source_hessian_grid=fa['source_hessian_grid'],
                  fixed_source_fourier_J=data['fixed_source_fourier_J'], initial_gas_fourier_J=data['initial_gas_fourier_J'],
                  current_source_fourier_J=current)
    for key, arr in arrays.items():
        m = man['arrays'][key]
        assert sha(S / m['file']) == m['sha256']
        bit('driver_seed_prep_' + key, arr, np.load(S / m['file'], allow_pickle=False, mmap_mode='r'))
    scal = {}
    for key, val in man['fa_scalars'].items():
        if key.endswith('description'):
            continue
        exp = float.fromhex(val) if isinstance(val, str) and val.lstrip('-').startswith('0x') else val
        scal[key] = bool(fa[key] == exp)
    # operator on sampled blocks
    base = load(BASE[0], 'v005_review_base', BASE[1])
    refw = np.load(S / op['operator']['weighted_responses']['file'], allow_pickle=False, mmap_mode='r')
    refv = np.load(S / op['operator']['wavevectors']['file'], allow_pickle=False, mmap_mode='r')
    W = op['W']; B = 48000
    mid = int(np.random.default_rng(20261018).integers(1, W // B - 1)) * B
    blocks = [(0, B), (mid, mid + B), (W - B, W)]
    for a, b in blocks:
        kw = dict(fa, k_physical=fa['k_physical'][a:b], dk_weights=fa['dk_weights'][a:b], source_density_fourier=current[a:b],
                  retain_node_diagnostics=False, node_diagnostic_callback=lambda rec: None)
        ans = base.prepare(**kw)
        bit('operator_weighted_responses[%d:%d]' % (a, b), ans['weighted_responses'], refw[a:b])
        bit('operator_wavevectors[%d:%d]' % (a, b), ans['wavevectors'], refv[a:b])
        del ans
    rec = {'schema': 'T120L_RECHECK_C2R_V001',
           'status': 'TESTED_PASS' if all(c['bitwise_equal'] for c in checks) and all(scal.values()) else 'TESTED_FAIL',
           'checks': checks, 'fa_scalars_equal': scal, 'blocks': blocks,
           'driver': {'path': str(DRV), 'sha256': DRV_SHA}, 'call_spec': {'path': str(CALL_A), 'sha256': sha(CALL_A)},
           'driver_seed_numerical_inputs': ni, 'saved_operator_json_sha256': OPERATOR_SHA,
           'saved_prep_json_sha256': sha(S / 'PREP.json'), 'tool': {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)},
           'prep_seconds': t_prep, 'wall_seconds': time.monotonic() - t0,
           'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'gas_iterations': 0, 'forward_runs': 0}
    with out.open('x') as f:
        json.dump(rec, f, indent=1, allow_nan=False, default=str)
    print(rec['status'], flush=True)


if __name__ == '__main__':
    main()
