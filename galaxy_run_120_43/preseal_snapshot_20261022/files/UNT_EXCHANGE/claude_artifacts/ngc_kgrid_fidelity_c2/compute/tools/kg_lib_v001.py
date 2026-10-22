"""ngc_kgrid_fidelity_c2 compute library V001 (Claude2 helper lane). Diagnostics only.

Executes PREREG_KGRID_FIDELITY_V001 (sha 4c2eefeb...). No route-A / forward run is launched.
No NGC3198 target/velocity file and no result.json is opened by this code. The NGC prep v001
itself reads its own target-free inputs (radial source reference, target-free query manifest,
H2 tail reduction); this library never reads them directly.
Every pinned file is verified from bytes before use (pins come from the sealed prereg JSON).
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

LANE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_kgrid_fidelity_c2')
COMP = LANE/'compute'
OPS = COMP/'ops'
OUT = COMP/'out'
PREREG = LANE/'PREREG_KGRID_FIDELITY_V001.json'
PREREG_SHA = '4c2eefeb8a4e191d20173036fe0aa5e641799c70a97b96d354d0984742449869'
CHK_TOOLS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/check/tools')
RUN = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
           'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V001')
THETA = 3.3657664138980042e-09
KPC = 3.085677581491367e19
TIER2_IDS = ('G96F', 'G96FL', 'T120L', 'G120L', 'T160L', 'G160L')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def prereg():
    got = sha(PREREG)
    if got != PREREG_SHA:
        raise SystemExit('PREREG SHA MISMATCH %s' % got)
    return json.loads(PREREG.read_text())


def pin(name):
    """Path of a prereg-pinned input, verified from bytes now."""
    p = prereg()['pins_sha256_from_bytes'][name]
    got = sha(p['path'])
    if got != p['sha256']:
        raise SystemExit('PIN MISMATCH %s %s %s' % (name, got, p['sha256']))
    return Path(p['path'])


def load_module(path, expect, name):
    got = sha(path)
    if got != expect:
        raise SystemExit('MODULE PIN MISMATCH %s %s %s' % (path, got, expect))
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def candidate(cid):
    for c in prereg()['candidates']:
        if c['id'] == cid:
            return c
    raise SystemExit('unknown candidate '+cid)


def seed():
    p = pin('seed_v002_default')
    return json.loads(p.read_text())


def tier1_spec(cid):
    """composite_grid_spec handed to prep v001 for a tier-1 candidate (seed-level change only)."""
    c = candidate(cid)
    if c['tier'] != 1:
        raise SystemExit('not tier 1: '+cid)
    s = seed()['numerical_inputs']['composite_grid_spec']
    if cid == 'G80C':
        return dict(s)
    if cid == 'G80E14':
        spec = dict(json.loads(pin('N2_numerics_proposal_json').read_text())['proposal']['composite_grid_spec'])
    else:
        ax = c['transverse_axis_kx_ky']
        spec = {'version': 'NGC3198_%s_PANELS80_KGRID_PREREG_V001' % cid,
                'breaks_inverse_kpc': list(ax['breaks_inverse_kpc']),
                'panel_orders': list(ax['panel_orders']),
                'total_axis_nodes': ax['total_axis_nodes'],
                'scope': '%s: PREREG_KGRID_FIDELITY_V001 (4c2eefeb) candidate; same full signed cube kmax=2/kpc; '
                         'diagnostic iteration-0 preparation only; not adopted unless the sealed decision rule adopts it.' % cid}
    ax = c['transverse_axis_kx_ky']; vz = c['vertical_axis_kz']
    if (list(map(float, spec['breaks_inverse_kpc'])) != list(map(float, ax['breaks_inverse_kpc'])) or
            spec['panel_orders'] != ax['panel_orders'] or ax['panel_orders'] != vz['panel_orders']):
        raise SystemExit('tier1 spec disagrees with prereg candidate '+cid)
    return spec


def axis_si(breaks, orders, kpc_m):
    """prep v001:146-152 formula, one axis, physical 1/m."""
    breaks = np.asarray(breaks, dtype=float)
    axis_parts = []; weight_parts = []
    for lo, hi, n in zip(breaks[:-1], breaks[1:], orders):
        gxk, gwk = np.polynomial.legendre.leggauss(n)
        axis_parts.append(((lo+hi)/2+(hi-lo)*gxk/2)/kpc_m)
        weight_parts.append((hi-lo)*gwk/(2*kpc_m))
    axis = np.concatenate(axis_parts); w = np.concatenate(weight_parts)
    if np.any(axis == 0):
        raise ValueError('This quadrature excludes the unsupported zero mode')
    return axis, w


def kset_si(cid, kpc_m=KPC):
    """k-set override of H-OVR: per-axis prep formula, tensor order of prep v001:155-157 (x outer, y, z inner)."""
    c = candidate(cid)
    t = c['transverse_axis_kx_ky']; v = c['vertical_axis_kz']
    ax, awx = axis_si(t['breaks_inverse_kpc'], t['panel_orders'], kpc_m)
    az, awz = axis_si(v['breaks_inverse_kpc'], v['panel_orders'], kpc_m)
    ay, awy = ax, awx
    waves = np.array([(x, y, z) for x in ax for y in ay for z in az])
    dkweights = np.array([wx*wy*wz for wx in awx for wy in awy for wz in awz])
    if not np.all(np.isfinite(waves)) or not np.all(np.isfinite(dkweights)) or np.any(dkweights <= 0):
        raise ValueError('Nonfinite or underflowed physical Fourier quadrature')
    return waves, dkweights


def axes_kpc_weights(cid):
    """Known-field weights in kpc units, built exactly as checker aniso_c1/lowk_c1 do (from the spec breaks)."""
    c = candidate(cid)
    out = []
    for key in ('transverse_axis_kx_ky', 'transverse_axis_kx_ky', 'vertical_axis_kz'):
        a = c[key]
        out.append(np.concatenate([(hi-lo)*np.polynomial.legendre.leggauss(n)[1]/2 for lo, hi, n in
                                   zip(a['breaks_inverse_kpc'][:-1], a['breaks_inverse_kpc'][1:], a['panel_orders'])]))
    return out


def load_prep():
    """prep v001 with the A2 coefficient patch exactly as the reviewed driver c2v001 _install_hooks applies it
    (request module_patches: COEFFICIENT=Path(A2 npz), COEFFICIENT_SHA=2e3a36d8...)."""
    p = pin('ngc_prep_v001')
    m = load_module(p, prereg()['pins_sha256_from_bytes']['ngc_prep_v001']['sha256'], 'kg_ngc_prep_v001')
    a2 = pin('A2_pooled_coefficient_grid')
    for name in ('COEFFICIENT', 'COEFFICIENT_SHA'):
        if not hasattr(m, name):
            raise ValueError('Override target absent '+name)
    m.COEFFICIENT = Path(str(a2))
    m.COEFFICIENT_SHA = prereg()['pins_sha256_from_bytes']['A2_pooled_coefficient_grid']['sha256']
    return m


def base_module():
    p = pin('fourier_base_v005')
    return load_module(p, prereg()['pins_sha256_from_bytes']['fourier_base_v005']['sha256'], 'kg_fourier_base_v005')


def checker():
    """Checker replay_c1 / sweep_c1 (pinned), imported by name from their own directory (-B: no bytecode written)."""
    for n in ('checker_replay_c1', 'checker_sweep_c1'):
        pin(n)
    if str(CHK_TOOLS) not in sys.path:
        sys.path.insert(0, str(CHK_TOOLS))
    import replay_c1 as C
    import sweep_c1 as S
    for mod, n in ((C, 'checker_replay_c1'), (S, 'checker_sweep_c1')):
        if sha(mod.__file__) != prereg()['pins_sha256_from_bytes'][n]['sha256']:
            raise SystemExit('checker module changed after import')
    return C, S


def op_dir(cid, path):
    return OPS/('%s_%s' % (cid, path))


def load_operator(cid, path):
    d = op_dir(cid, path)
    man = json.loads((d/'OPERATOR.json').read_text())
    arr = {}
    for key in ('wavevectors', 'weighted_responses'):
        f = d/man['operator'][key]['file']
        if sha(f) != man['operator'][key]['sha256']:
            raise SystemExit('operator blob sha mismatch '+str(f))
        arr[key] = np.load(f, allow_pickle=False)
    return {'wavevectors': arr['wavevectors'], 'weighted_responses': arr['weighted_responses']}, man


def ctx_with(cid, path):
    C, S = checker()
    ctx = C.Ctx()
    if cid is not None:
        prepared, man = load_operator(cid, path)
        ctx.prepared = prepared
        ctx._k = None; ctx._line = None
    return C, S, ctx


def fhex(x):
    return float(x).hex()


def write_json(path, obj):
    path = Path(path)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj, indent=1, allow_nan=False, default=str))
    os.replace(tmp, path)


def save_npy(path, a):
    path = Path(path)
    with open(path, 'xb') as f:
        np.save(f, a, allow_pickle=False)
    return {'file': path.name, 'sha256': sha(path), 'shape': list(a.shape), 'dtype': a.dtype.str}


def threads_env_ok():
    return all(os.environ.get(k) == '1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'))
