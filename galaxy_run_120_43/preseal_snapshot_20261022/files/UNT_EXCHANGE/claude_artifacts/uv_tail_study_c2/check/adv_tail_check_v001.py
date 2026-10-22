r"""ADVERSARIAL CHECKER (independent of tools/common_uvtail_v001.py; nothing imported from tools/).

Read-only on the saved R3 cube states. No run launched. Writes only check/ADV_*.json.

Independent route to the static UV tail of the lapse radial force:
  * source rebuilt here from the saved arrays (gas rings from the field's source rotation; star rings re-derived from
    prep v007:150-190 text) and validated against the saved Fourier packets on random nodes of each case's own grid;
  * symbol q(k) = 4 gamma_eff k^2 * unit(k)(2pi)^3/dk measured on each case's own unit_response;
  * tail integral done in CARTESIAN (kx,ky,kz) with tensor Gauss panels over box(Kb) \ box(K) (no cylindrical
    reduction, no arccos azimuthal measure); the rotation's actual 16-azimuth average of the radial derivative is
    used (P16), and the m=0 (J1) reading is computed alongside to measure the alias;
  * the pinned rotation law (owned_free_surface_rotation_v001:16-20): Omega^2 -> Omega^2 + dB/(A R), rows through the
    pinned column-mean adapter v002 (same call as column mean v004:36-47).
"""
import ctypes, ctypes.util, hashlib, importlib.util, json, math, sys, time
from pathlib import Path
import numpy as np

ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = ROOT/'CLAUDE2/runs'; HR = ROOT/'helpers/recovered_packet_audit'; HC = ROOT/'helpers/coefficient_method'; C1 = ROOT/'CODEX1'
OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check')
PREREG = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json')
CL = 299792458.0
SUF = {'C2': ('C2R3', 2.0), 'C3': ('C3R3', 3.0), 'C4': ('C4R3', 4.0)}

lib = ctypes.CDLL(ctypes.util.find_library('m'))
for nm in ('j0', 'j1'):
    getattr(lib, nm).argtypes = [ctypes.c_double]; getattr(lib, nm).restype = ctypes.c_double
_J0 = np.frompyfunc(lib.j0, 1, 1); _J1 = np.frompyfunc(lib.j1, 1, 1)
def J0(x): return _J0(np.asarray(x, float)).astype(float)
def J1(x): return _J1(np.asarray(x, float)).astype(float)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p, n):
    s = importlib.util.spec_from_file_location('adv_'+n, str(p)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def argmap(req):
    a = json.loads(Path(req).read_text())['argv']; return {a[i]: a[i+1] for i in range(len(a)-1) if a[i].startswith('--')}


def stars_from_prep(ni, continuum=False, nrad=48, ntail=200):
    """prep v007:150-190 re-typed. continuum=True: same declared Sigma(R) on a finer radial roster (my own choice of
    48/200 nodes, deliberately different from the study's 64/256), vertical handled analytically by caller."""
    prof = json.loads((C1/'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json').read_text())['galaxies']['DDO154']['stellar_reference']
    streaming = load(HR/'galaxy_baryonic_source_forward_v002.py', 'streaming')
    kpc = ni['kpc_m']; su = ni['solar_mass_kg']/(kpc/1000)**2
    radii = [float(x) for x in prof['radius_kpc']]; sig = [float(x) for x in prof['surface_density_Msun_pc2']]
    rd = float(prof['outer_scale_kpc']); h = float(prof['height_kpc'])
    cuts = sorted(set([0.]+radii))
    g = np.polynomial.legendre.leggauss(ni['source_gauss_order'])
    ga = np.polynomial.legendre.leggauss(nrad if continuum else ni['source_gauss_order'])
    gt = np.polynomial.legendre.leggauss(ntail if continuum else ni['source_gauss_order'])
    nodes = []
    for lo, hi in zip(cuts, cuts[1:]):
        for x, w in zip(*ga): nodes.append(((lo+hi)/2+(hi-lo)*x/2, (hi-lo)*w/2))
    for x, w in zip(*gt):
        u = (x+1)/2; nodes.append((radii[-1]-rd*math.log(u), rd*w/(2*u)))
    Rr = np.array([r*kpc for r, _ in nodes])
    Mr = np.array([streaming.radial_surface(r, radii, sig, outer_scale=rd)*su*(r*kpc)*(dr*kpc)*2*math.pi for r, dr in nodes])
    zu = np.array([2*h*kpc*math.atanh(u) for u in g[0]]); wu = g[1]/2
    return dict(Rr=Rr, Mr=Mr, zu=zu, wu=wu, h_m=h*kpc)


class Case:
    def __init__(self, cid):
        suf, self.K = SUF[cid]; self.cid = cid
        self.run = RUNS/('KMAX_A2F10_%s_D7R3_RUN_V001' % suf)
        res = json.loads((self.run/'result.json').read_text())
        if json.loads((self.run/'finish.json').read_text())['result_sha256'] != sha(self.run/'result.json'): raise ValueError('result sha')
        last = res['passes'][-1]
        self.rows = np.array([r['speed_km_s'] for r in last['rows']]); self.top_speeds = res['speeds_km_s']
        self.rot = Path(last['rotation']); self.field = Path(last['field'])
        fm = argmap(self.field.parent/'request.json'); self.src_rot = Path(fm['--rotation-directory']); self.offset = Path(fm['--offset-directory'])
        rm = argmap(self.rot.parent/'request.json')
        if Path(rm['--feedback-directory']) != self.field: raise ValueError('rotation not on this field')
        self.manifest = Path(rm['--column-manifest'])
        self.checkpoint = Path(res['identity']['route_a']['checkpoint']); self.gamma = float(res['identity']['route_a']['custody']['physical']['gamma'])


def ring_S(k, R, z, m):
    kp = np.hypot(k[:, 0], k[:, 1]); return -CL*CL*np.einsum('kr,kr,r->k', J0(kp[:, None]*R[None, :]), np.exp(-1j*k[:, 2, None]*z[None, :]), m)


def validate(c, ni, rng):
    with np.load(c.offset/'unit_response.npz') as f:
        waves = f['wavevectors']; dk = f['dk_weights']; unit = f['weighted_responses'][:, 0, 0].copy()
    with np.load(c.field/'refreshed_prepared.npz') as f:
        if not np.array_equal(f['wavevectors'], waves): raise ValueError('wave order')
        tot = f['weighted_responses'][:, 0, 0].copy()
    with np.load(c.field/'gas_source_feedback.npz') as f: gasJ = f['new_gas_fourier_J'][:, 0, 0].copy()
    st = json.loads((c.checkpoint/'iteration_0004/START.json').read_text())['fixed_source_fourier_J']
    if sha(c.checkpoint/st['blob']) != st['file_sha256']: raise ValueError('star blob')
    starJ = np.load(c.checkpoint/st['blob'])[:, 0, 0]
    out = dict(n_nodes=int(len(waves)))
    # I1 on ALL nodes
    pred = unit*(starJ+gasJ); out['I1_max_rel'] = float(np.max(np.abs(tot-pred))/np.max(np.abs(tot)))
    # rebuilt source on 3000 random nodes
    idx = rng.choice(len(waves), 3000, replace=False)
    with np.load(c.src_rot/'rotation_base_arrays.npz') as f:
        rho = f['rho0']; vol = f['volume_weights_m3']; Rg = f['radial_nodes_m']; zg = f['z'][:, 0, :]
    if not np.array_equal(rho, np.broadcast_to(rho[:, :1, :], rho.shape)): raise ValueError('gas not axisymmetric')
    mg = np.sum(vol*rho, axis=1)
    gS = ring_S(waves[idx], np.repeat(Rg, 32), zg.reshape(-1), mg.reshape(-1))
    s = stars_from_prep(ni); sR = np.repeat(s['Rr'], len(s['zu'])); sz = np.tile(s['zu'], len(s['Rr'])); sm = np.outer(s['Mr'], s['wu']).reshape(-1)
    sS = ring_S(waves[idx], sR, sz, sm)
    out['gas_rebuild_max_rel'] = float(np.max(np.abs(gS-gasJ[idx]))/np.max(np.abs(gasJ[idx])))
    out['star_rebuild_max_rel'] = float(np.max(np.abs(sS-starJ[idx]))/np.max(np.abs(starJ[idx])))
    # symbol
    kk = np.sqrt(np.sum(waves*waves, axis=1)); T = unit*(2*np.pi)**3/dk
    q = 4*c.gamma*kk*kk*T.real
    out['unit_imag_max_rel'] = float(np.max(np.abs(T.imag)/np.abs(T.real)))
    kpc = ni['kpc_m']; kk_kpc = kk*kpc; bins = [0.1, 0.3, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7]
    tab = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        sel = (kk_kpc >= lo) & (kk_kpc < hi)
        if sel.sum():
            d = 1-q[sel]; tab.append(dict(k_lo=lo, k_hi=hi, n=int(sel.sum()), mean_1mq=float(d.mean()), max_abs_1mq=float(np.abs(d).max()),
                                         c_mean=float(np.mean(d*kk_kpc[sel]**2))))
    out['symbol_bins'] = tab
    sel = kk_kpc >= 2; out['max_abs_1mq_k_ge_2'] = float(np.max(np.abs(1-q[sel])))
    return out, (Rg, zg, mg), s


def axis_nodes(L, K, width, order, half):
    b = set(np.round(np.arange(0, L+1e-9, width), 10).tolist()) | {float(L), float(K), 0.0}
    b = np.array(sorted(x for x in b if x <= L)); x, w = np.polynomial.legendre.leggauss(order)
    nd = np.concatenate([(lo+hi)/2+(hi-lo)*x/2 for lo, hi in zip(b[:-1], b[1:])]); wt = np.concatenate([(hi-lo)*w/2 for lo, hi in zip(b[:-1], b[1:])])
    if half: return nd, wt
    return np.concatenate([-nd[::-1], nd]), np.concatenate([wt[::-1], wt])


def cart_tail(c, gas, stars, ni, Kb, width, order, R, zcol, star_mode='discrete', disk=None, gas_on=True, stars_on=True):
    """Cartesian quadrature of c^2 d_R n_tail at columns (R_i, z_il), tail region box(Kb)\\box(K) [optionally cut to kp<=disk].
    Returns (P16 average, m=0 average), each (72,32) m/s^2."""
    kpc = ni['kpc_m']
    ax, aw = axis_nodes(Kb, c.K, width, order, half=True)                 # quadrant kx,ky>0 (D4 symmetry; see doc)
    zz, zw = axis_nodes(Kb, c.K, width, order, half=False)
    KX, KY = np.meshgrid(ax, ax, indexing='ij'); KX = KX.ravel()/kpc; KY = KY.ravel()/kpc; WXY = 4*np.outer(aw, aw).ravel()/kpc**2
    KZ = zz/kpc; WZ = zw/kpc; Kc = c.K/kpc
    inner_xy = (np.abs(KX) <= Kc*(1+1e-12)) & (np.abs(KY) <= Kc*(1+1e-12)); inner_z = np.abs(KZ) <= Kc*(1+1e-12)
    KP = np.hypot(KX, KY)
    Rg, zg, mg = gas
    Eg = np.einsum('il,zil->zi', mg, np.exp(-1j*KZ[:, None, None]*zg[None, :, :]))       # (nz,72)
    if star_mode == 'discrete': Es = np.exp(-1j*KZ[:, None]*stars['zu'][None, :]) @ stars['wu']
    else:
        a = np.pi*stars['h_m']*np.abs(KZ); Es = np.where(a > 1e-10, a/np.sinh(np.minimum(a, 700.)), 1.0)*(a < 700)
    phis = 2*np.pi*np.arange(16)/16
    out16 = np.zeros((len(R), len(KZ)), complex); out0 = np.zeros((len(R), len(KZ)), complex)
    pref = 1.0/(4*c.gamma*(2*np.pi)**3)
    for a0 in range(0, len(KX), 6000):
        sl = slice(a0, min(a0+6000, len(KX)))
        kx, ky, kp, w = KX[sl], KY[sl], KP[sl], WXY[sl]
        S = np.zeros((len(kx), len(KZ)), complex)
        if gas_on: S += -CL*CL*(J0(kp[:, None]*Rg[None, :]) @ Eg.T)
        if stars_on: S += -CL*CL*np.outer(J0(kp[:, None]*stars['Rr'][None, :]) @ stars['Mr'], Es)
        mask = ~(inner_xy[sl][:, None] & inner_z[None, :])
        if disk is not None: mask &= (kp[:, None] <= disk/kpc*(1+1e-12))
        F = pref*w[:, None]*WZ[None, :]*S/(kp[:, None]**2+KZ[None, :]**2)*mask
        # P16_i(kx,ky) = mean_j d/dR exp(i k.x) at x=(R cos phi_j, R sin phi_j)  (real by symmetry)
        P16 = np.zeros((len(R), len(kx)))
        for ph in phis:
            proj = kx*math.cos(ph)+ky*math.sin(ph)
            P16 += (1j*proj[None, :]*np.exp(1j*R[:, None]*proj[None, :])).real
        P16 /= 16
        P0 = -kp[None, :]*J1(kp[None, :]*R[:, None])
        out16 += P16 @ F; out0 += P0 @ F
    f16 = np.empty(zcol.shape); f0 = np.empty(zcol.shape)
    for i in range(len(R)):
        E = np.exp(1j*np.outer(KZ, zcol[i])); f16[i] = CL*CL*(out16[i] @ E).real; f0[i] = CL*CL*(out0[i] @ E).real
    return f16, f0


def rows_with(c, rot, cols, dPR, binding, obs, adapter):
    R = rot['radial_nodes_m']; rho = rot['rho0'][:, 0, :]; h = rot['enthalpy'][:, 0, :]
    w = np.array([col['weights_m'] for col in cols]); A = np.sum(w*rho/h, axis=1)
    om2 = rot['rotation_Omega_squared'] + (np.sum(w*rho/h*dPR, axis=1)/A/R)[:, None] if dPR is not None else rot['rotation_Omega_squared']
    if np.any(om2 <= 0): raise ValueError('Omega^2<=0')
    wts = [(np.asarray(col['weights_m'])*rho[i]*binding['HI_to_HI_plus_He_mass_ratio']).tolist() for i, col in enumerate(cols)]
    pk = adapter.evaluate(observation_module=obs, radial_nodes_m=R, query_ids=[q['id'] for q in binding['query_rows']],
                          query_radii_m=[q['radius_m'] for q in binding['query_rows']], v_phi_m_s=R[:, None]*np.sqrt(om2), emissivity_path_weights=wts,
                          physical_inclination_rad=binding['physical_inclination_rad'], released_inclination_rad=binding['released_inclination_rad'],
                          approximation_provenance=binding['observation_rule'], tracer_provenance=binding['tracer_rule'],
                          source_status='ADV_CHECK_PROXY', motion_status='ADV_CHECK_PROXY', nonaxisymmetric_residual_provenance='adversarial check proxy')
    return np.array([r['speed_km_s'] for r in pk['rows']]), A


def main(cids, Kb, width, order, tag):
    t0 = time.time(); rng = np.random.default_rng(20261017)
    ni = json.loads((RUNS/'KMAX_A2F10_C2R3_D7R3_RUN_V001/inputs/seed_c2v001.json').read_text())['numerical_inputs']
    binding = json.loads((C1/'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json').read_text())
    obs = load(HR/'galaxy_hi_observation_forward_v001.py', 'obs'); adapter = load(HR/'owned_column_mean_streaming_observation_v002.py', 'adapter')
    starsC = stars_from_prep(ni, continuum=True)
    res = dict(schema='ADV_TAIL_CHECK_V001', Kb=Kb, width=width, order=order, cases={})
    for cid in cids:
        c = Case(cid); val, gas, starsD = validate(c, ni, rng)
        print(cid, 'validate', json.dumps({k: v for k, v in val.items() if k != 'symbol_bins'}), '%.0fs' % (time.time()-t0)); sys.stdout.flush()
        with np.load(c.rot/'rotation_base_arrays.npz') as f: rot = {k: f[k].copy() for k in ('radial_nodes_m', 'z', 'rho0', 'enthalpy', 'rotation_Omega_squared', 'rotation_A')}
        man = json.loads(c.manifest.read_text()); cols = {}
        for run in man['runs']:
            for it in json.loads((Path(run['directory'])/'finish.json').read_text())['completed']: cols[it['index']] = json.loads(Path(it['path']).read_text())
        cols = [cols[i] for i in range(72)]
        R = rot['radial_nodes_m']; zc = rot['z'][:, 0, :]
        rows0, A = rows_with(c, rot, cols, None, binding, obs, adapter)
        rec = dict(validate=val, rows_saved=c.rows.tolist(), rows_repro_max_abs=float(np.max(np.abs(rows0-c.rows))),
                   A_maxrel=float(np.max(np.abs(A/rot['rotation_A']-1))))
        variants = {
            'box_discrete': dict(star_mode='discrete'),
            'disk_discrete': dict(star_mode='discrete', disk=Kb),
            'box_gas_only': dict(star_mode='discrete', stars_on=False),
            'box_stars_cont_only': dict(star_mode='continuum', gas_on=False),
        }
        for vn, kw in variants.items():
            st = starsC if kw.get('star_mode') == 'continuum' else starsD
            f16, f0 = cart_tail(c, gas, st, ni, Kb, width, order, R, zc, **kw)
            r16, _ = rows_with(c, rot, cols, f16, binding, obs, adapter); r0, _ = rows_with(c, rot, cols, f0, binding, obs, adapter)
            rec[vn] = dict(delta_rows_P16=(r16-c.rows).tolist(), delta_rows_m0=(r0-c.rows).tolist(), rows_P16=r16.tolist(), rows_m0=r0.tolist())
            print(cid, vn, 'P16', np.round(r16-c.rows, 3).tolist(), '\n   ', 'm0 ', np.round(r0-c.rows, 3).tolist(), '%.0fs' % (time.time()-t0)); sys.stdout.flush()
        res['cases'][cid] = rec
    p = OUT/('ADV_TAIL_CHECK_%s_V001.json' % tag)
    with p.open('x') as f: json.dump(res, f, indent=1, allow_nan=False); f.write('\n')


if __name__ == '__main__':
    main(sys.argv[1].split(','), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
