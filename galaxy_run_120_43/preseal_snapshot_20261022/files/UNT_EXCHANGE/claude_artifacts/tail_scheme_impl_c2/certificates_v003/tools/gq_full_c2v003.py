"""GQ at gas M_s 128 vs 256 on EVERY production tail node of one T-case geometry (root A57.1: "the GQ certificate at M_s 128
over the full DDO reach (all nodes, not only sampled ones)").  Replay / static computation only; no launch.

Object (unchanged from certificates_v001/v002 GQ, RA7): the module gas transform S_gas(k_perp, k_z) = sum_i P_i(k_perp)
sigma_i(k_z) of the present gas columns (uv_tail_source_roster_c2v001 GasColumns; only P_i depends on M_s), at M_s and 2 M_s,
normalized by P0 = |S_gas(0, 0)| (= the roster gas mass).  Gate value: max over nodes |S(M_s) - S(2M_s)| / P0 <= 1e-12.

Node set = exactly the nodes a production build integrates (owned_uv_tail_lapse_v001.build, c28d4209 L694-781):
  the tensor nodes (k_perp_i, k_z_j >= 0) of the module's own _grid(kept, outer, quadrature, R_eval) with c0^D(i, j) != 0
  (module _c0_D: the ring/shell integrand weight) OR inside a corner family zone (L < k_perp <= sqrt2 L, k_z <= Lz: the corner
  blocks M_c), plus, for a sphere kept region, every node of the module's _sphere_piece (cyl(K,K) minus sphere(K)).
  k_z < 0: sigma_i(-k_z) = conj(sigma_i(k_z)) (real masses) and P_i real, so |dS| and |S| are even in k_z; TESTED on the
  4096-node sample (field kz_negative_check).
Per node two differences are formed: d_sub = |S(M_s) - S(2M_s)| (two transforms subtracted, as certificates_v002) and
d_dP = |sum_i (P_i(M_s) - P_i(2M_s)) sigma_i| (difference of radial factors first); the gate value is the max of both.
Also: max_rel_change = max |S(M_s) - S(2M_s)| / |S(2M_s)| (all nodes with S != 0; and over nodes with |S|/P0 >= 1e-6),
log10 histograms, the per-k_perp-row maximum profile (out/*.npy), corner / rest / sphere-piece maxima, max |S(2M_s)|/P0,
and the certificates_v001 every-k_perp bound max_kp sum_i |dP_i| sigma_i(0) / P0.
Contract sample (FIELDS_R5 GQ: nodes 4096): 4096 nodes drawn with rng 20261018 from the same node set (1024 from the corner
zones, or from the sphere piece for a sphere kept region, + 3072 from the rest), evaluated the certificates_v002 way.
Usage: python3 -I -B gq_full_c2v003.py GEOMETRY_LABEL   (labels in GEOMETRIES)"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certs3_common_c2v003 as C3  # noqa: E402

CC = C3.CC
# label -> (saved roster state, compare roster name, kept stage-kind truncation, kept K, outer, role)
GEOMETRIES = {
    'C2T_KB128': ('C2R3', 'DDO_C2T', None, 2.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'C2T production (P = 128)'),
    'C2T_KB256': ('C2R3', 'DDO_C2T', None, 2.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 256.0}, 'C2T roster over the full DDO reach (|k| <= 362.04)'),
    'C3T_KB128': ('C3R3', 'DDO_C3T', None, 3.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'C3T production (P = 128)'),
    'C3T_KB256': ('C3R3', 'DDO_C3T', None, 3.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 256.0}, 'C3T roster over the full DDO reach (|k| <= 362.04)'),
    'C4T_KB64': ('C4R3', 'DDO_C4T-KLO', None, 4.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 64.0}, 'C4T-KLO (P/2)'),
    'C4T_KB128': ('C4R3', 'DDO_C4T', None, 4.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'C4T and C4T-A production (P = 128; C4T-A differs only in lambda_scale)'),
    'C4T_KB256': ('C4R3', 'DDO_C4T-KHI', None, 4.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 256.0}, 'C4T-KHI (2P); the C4T roster over the full DDO reach (|k| <= 362.04)'),
    'C4T-C5c': ('C4R3', 'DDO_C4T-C5c', None, 4.0, {'shape': 'cube', 'K_out_inverse_kpc': 5.0}, 'C4T-C5c (outer cube K_out 5)'),
    'S4T_SPHERE_KB128': ('C4R3', 'DDO_S4T', {'shape': 'sphere', 'kmax_inverse_kpc': 4.0}, 4.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0},
                         'S4T mask stages (kept sphere 4; its cube-kept stages are the C4T_KB128 node set); C4R3 roster (S4T is on grid G4)'),
    'C6T_KB128': ('C4R3', 'DDO_C6T', None, 6.0, {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0},
                  'C6T geometry (kept cube 6); C4R3 roster as the stand-in source (no saved C6R3 le3 roster is pinned here; A48 AMB-12: '
                  'P_i depends on the s-edge geometry and M_s only, shared by every DDO T-case)'),
}
BLK = 64


def node_mask(U, kept, outer, fam, kk, kz_kpc):
    c0 = U._c0_D(kept, outer, kk, kz_kpc)
    m = c0 != 0
    zone = np.zeros_like(m)
    for f in fam:
        zr = (kk > f['L']) & (kk <= math.sqrt(2) * f['L'])
        if zr.any():
            zone |= zr[:, None] & (kz_kpc <= f['Lz'])[None, :]
    return m | zone, zone


def sample(U, kept, outer, g, fam, sph, rng, n_zone=1024, n_rest=3072):
    """(I, J, kind) for 4096 contract nodes: tensor (i, j) pairs, or sphere-piece entries (I = -1, J = entry index)."""
    kp, kz = g['kp'], g['kz']
    out = []

    def draw(n, want_zone):
        got = []
        while len(got) < n:
            i = rng.integers(0, len(kp), 8 * n); j = rng.integers(0, len(kz), 8 * n)
            ok = np.zeros(len(i), bool); zn = np.zeros(len(i), bool)
            # pairwise evaluation (the module functions are tensor-shaped): evaluate per pair
            for t in range(len(i)):
                mm, zz = node_mask(U, kept, outer, fam, kp[i[t]:i[t] + 1], kz[j[t]:j[t] + 1])
                ok[t] = mm[0, 0]; zn[t] = zz[0, 0]
            sel = ok & (zn if want_zone else ~zn)
            for a, b in zip(i[sel], j[sel]):
                got.append((int(a), int(b), 'zone' if want_zone else 'rest'))
                if len(got) == n:
                    break
        return got
    if fam:
        out += draw(n_zone, True)
    elif sph is not None:
        e = rng.choice(len(sph['kz']), n_zone, replace=False)
        out += [(-1, int(x), 'sphere') for x in e]
    out += draw(n_rest if (fam or sph is not None) else n_zone + n_rest, False)
    return out


def main():
    CC.require_env(); t0 = time.time()
    label = sys.argv[1]
    cid, rname, trunc, K, outer, role = GEOMETRIES[label]
    U, RS, PV = CC.uvt_modules(); jn = PV.create_provider()
    case, ros, i1t, units, prof, s_edges = C3.ddo_roster(U, RS, PV, jn, cid, C3.MS_PROD)
    gas = ros.gas
    M_s = C3.MS_PROD
    gA = C3.clone_gas(RS, gas, M_s); gB = C3.clone_gas(RS, gas, 2 * M_s)
    if trunc is None:
        kept = U.kept_region('fs_rotation', {'shape': 'cube', 'kmax_inverse_kpc': None}, K / U.KPC_M)
    else:
        kept = U.kept_region('fs_rotation', trunc, K / U.KPC_M)
    if not U._outer_contains(outer, kept) or U.domain_is_empty(kept, outer):
        raise SystemExit('geometry not a production tail domain')
    g = U._grid(kept, outer, C3.QUAD_DDO, C3.R_EVAL_DDO)
    fam = g['families']
    sph = None
    if kept['shape'] == 'sphere':
        skp, swkp, skz, swz, sgi = U._sphere_piece(kept['K_inverse_kpc'], C3.QUAD_DDO['w_perp_max_inverse_kpc'],
                                                   C3.QUAD_DDO['w_z_max_inverse_kpc'], C3.QUAD_DDO['order'])
        sph = dict(kp=skp, kz=skz, gi=sgi)
    kp_k, kz_k = g['kp'], g['kz']
    kpm = kp_k / U.KPC_M; kzm = kz_k / U.KPC_M
    P0 = float(abs(gA.radial_factors(np.array([0.0]), jn.j0)[0] @ gA.vertical_factors(np.array([0.0]))[0]))
    mass = float(sum(float(np.sum(m)) for m, p in zip(gas.elements_m, gas.present) if p))
    sig = gA.vertical_factors(kzm)                                        # (nz, r) complex; M_s-independent
    sr = np.ascontiguousarray(sig.real.T); si = np.ascontiguousarray(sig.imag.T)
    s0 = np.abs(gA.vertical_factors(np.array([0.0]))[0].real)
    print(label, rname, 'kept', kept, 'outer', outer, 'N_perp', len(kp_k), 'N_z', len(kz_k), 'r', sig.shape[1], flush=True)

    # ---------------- full node set
    HB = np.linspace(-20.0, 2.0, 89)                                      # log10 bins (0.25 dex)
    hd = np.zeros(len(HB) + 1, np.int64); hr = np.zeros(len(HB) + 1, np.int64)
    acc = dict(n=0, n_zone=0, n_big=0, dmax=-1.0, dsub=-1.0, ddp=-1.0, dzone=0.0, drest=0.0, rel=-1.0, relbig=-1.0, smax=0.0, n_S0=0)
    at = {}
    row_max = np.zeros(len(kp_k)); row_relbig = np.zeros(len(kp_k))
    bmax = 0.0; kat = None
    for a in range(0, len(kp_k), BLK):
        sl = slice(a, min(a + BLK, len(kp_k)))
        kk = kp_k[sl]
        mask, zone = node_mask(U, kept, outer, fam, kk, kz_k)
        PA = gA.radial_factors(kpm[sl], jn.j0); PB = gB.radial_factors(kpm[sl], jn.j0)
        dPa = np.abs(PA - PB) @ s0
        if dPa.max() / P0 > bmax:
            bmax = float(dPa.max() / P0); kat = float(kk[int(np.argmax(dPa))])
        if not mask.any():
            continue
        Ar = PA @ sr; Ai = PA @ si; Br = PB @ sr; Bi = PB @ si
        dP = PA - PB
        Dr = dP @ sr; Di = dP @ si
        dsub = np.hypot(Ar - Br, Ai - Bi) / P0
        ddp = np.hypot(Dr, Di) / P0
        sB = np.hypot(Br, Bi) / P0
        del Ar, Ai, Dr, Di
        d = np.maximum(dsub, ddp)
        dm = np.where(mask, d, -1.0)
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = np.where(mask & (sB > 0), dsub / sB, -1.0)
        big = mask & (sB >= 1e-6)
        relb = np.where(big, rel, -1.0)
        acc['n'] += int(mask.sum()); acc['n_zone'] += int((mask & zone).sum()); acc['n_big'] += int(big.sum())
        acc['n_S0'] += int((mask & (sB == 0)).sum())
        row_max[sl] = dm.max(axis=1); row_relbig[sl] = relb.max(axis=1)
        for key, arr in (('dmax', dm), ('dsub', np.where(mask, dsub, -1.0)), ('ddp', np.where(mask, ddp, -1.0)), ('rel', rel), ('relbig', relb)):
            j = int(np.argmax(arr)); v = float(arr.flat[j])
            if v > acc[key]:
                acc[key] = v; ii, jj = np.unravel_index(j, arr.shape)
                at[key] = dict(k_perp=float(kk[ii]), k_z=float(kz_k[jj]), k_abs=float(math.hypot(kk[ii], kz_k[jj])),
                               S_over_P0=float(sB[ii, jj]), d_over_P0=float(d[ii, jj]), zone=bool(zone[ii, jj]))
        if (mask & zone).any():
            acc['dzone'] = max(acc['dzone'], float(d[mask & zone].max()))
        if (mask & ~zone).any():
            acc['drest'] = max(acc['drest'], float(d[mask & ~zone].max()))
        acc['smax'] = max(acc['smax'], float(sB[mask].max()))
        dv = d[mask]; rv = rel[mask & (sB > 0)]
        hd += np.bincount(np.searchsorted(HB, np.log10(np.maximum(dv, 1e-300))), minlength=len(HB) + 1)
        hr += np.bincount(np.searchsorted(HB, np.log10(np.maximum(rv, 1e-300))), minlength=len(HB) + 1)
        if (a // BLK) % 64 == 0:
            print('  rows %d/%d nodes %d dmax %.3e rel %.3e relbig %.3e %.0fs' % (sl.stop, len(kp_k), acc['n'], acc['dmax'], acc['rel'], acc['relbig'],
                                                                              time.time() - t0), flush=True)
    sphere = None
    if sph is not None:
        PAs = gA.radial_factors(sph['kp'] / U.KPC_M, jn.j0); PBs = gB.radial_factors(sph['kp'] / U.KPC_M, jn.j0)
        dmx = 0.0; rmx = 0.0; rbig = 0.0; n = len(sph['kz'])
        for s0_ in range(0, n, 65536):
            ss = slice(s0_, min(n, s0_ + 65536))
            sg = gA.vertical_factors(sph['kz'][ss] / U.KPC_M); gi = sph['gi'][ss]
            SA = np.einsum('nr,nr->n', PAs[gi], sg); SB = np.einsum('nr,nr->n', PBs[gi], sg)
            SD = np.einsum('nr,nr->n', (PAs - PBs)[gi], sg)
            dd = np.maximum(np.abs(SA - SB), np.abs(SD)) / P0; sb = np.abs(SB) / P0
            dmx = max(dmx, float(dd.max()))
            rr = np.abs(SA - SB) / np.where(sb > 0, np.abs(SB), np.inf)
            rmx = max(rmx, float(rr.max())); rbig = max(rbig, float(rr[sb >= 1e-6].max()) if (sb >= 1e-6).any() else 0.0)
        sphere = dict(nodes=int(n), max_abs_diff_over_P0=dmx, max_rel_change=rmx, max_rel_change_S_over_P0_ge_1em6=rbig)
        acc['dmax'] = max(acc['dmax'], dmx); acc['n'] += n
    # ---------------- contract sample (FIELDS_R5 GQ: 4096 nodes), certificates_v002 arithmetic
    rng = np.random.default_rng(20261018)
    pairs = sample(U, kept, outer, g, fam, sph, rng)
    tI = np.array([p[0] for p in pairs if p[0] >= 0]); tJ = np.array([p[1] for p in pairs if p[0] >= 0])
    sE = np.array([p[1] for p in pairs if p[0] < 0], dtype=int)
    uk, inv = np.unique(tI, return_inverse=True)
    PAu = gA.radial_factors(kpm[uk], jn.j0); PBu = gB.radial_factors(kpm[uk], jn.j0)
    sgJ = gA.vertical_factors(kzm[tJ]); sgJn = gA.vertical_factors(-kzm[tJ])
    SA = np.einsum('ni,ni->n', PAu[inv], sgJ); SB = np.einsum('ni,ni->n', PBu[inv], sgJ)
    SAn = np.einsum('ni,ni->n', PAu[inv], sgJn); SBn = np.einsum('ni,ni->n', PBu[inv], sgJn)
    ds = list(np.abs(SA - SB) / P0); rs = list(np.abs(SA - SB) / np.abs(SB)); sbs = list(np.abs(SB) / P0)
    kz_neg = dict(max_rel_diff_abs_dS=float(np.max(np.abs(np.abs(SAn - SBn) - np.abs(SA - SB)) / np.maximum(np.abs(SA - SB), 1e-300 * P0))),
                  max_rel_diff_abs_S=float(np.max(np.abs(np.abs(SBn) - np.abs(SB)) / np.abs(SB))))
    kabs = list(np.hypot(kp_k[tI], kz_k[tJ]))
    if len(sE):
        PAs = gA.radial_factors(sph['kp'][sph['gi'][sE]] / U.KPC_M, jn.j0); PBs = gB.radial_factors(sph['kp'][sph['gi'][sE]] / U.KPC_M, jn.j0)
        sg = gA.vertical_factors(sph['kz'][sE] / U.KPC_M)
        a_ = np.einsum('ni,ni->n', PAs, sg); b_ = np.einsum('ni,ni->n', PBs, sg)
        ds += list(np.abs(a_ - b_) / P0); rs += list(np.abs(a_ - b_) / np.abs(b_)); sbs += list(np.abs(b_) / P0)
        kabs += list(np.hypot(sph['kp'][sph['gi'][sE]], sph['kz'][sE]))
    ds = np.array(ds); rs = np.array(rs); sbs = np.array(sbs); kabs = np.array(kabs)
    kinds = np.array([p[2] for p in pairs if p[0] >= 0] + [p[2] for p in pairs if p[0] < 0])     # the order of ds above
    bigs = sbs >= 1e-6; jr = int(np.argmax(rs))
    k_out = outer.get('K_big_inverse_kpc', outer.get('K_out_inverse_kpc'))
    kabs_max = float(math.hypot(g['top'], g['topz']))
    contract = dict(roster=rname, k_range_inverse_kpc=[float(K), float(k_out)], M_s=int(M_s), M_s_doubled=int(2 * M_s), nodes=int(len(pairs)),
                    max_abs_diff_over_P0=float(ds.max()), max_rel_change=float(rs[jr]), max_rel_change_at_k_abs_inverse_kpc=float(kabs[jr]),
                    max_rel_change_S_over_P0_there=float(sbs[jr]), median_rel_change=float(np.median(rs)),
                    max_rel_change_S_over_P0_ge_1em6=(float(rs[bigs].max()) if bigs.any() else None), nodes_S_over_P0_ge_1em6=int(bigs.sum()),
                    nodes_by_kind={k: int((kinds == k).sum()) for k in ('zone', 'sphere', 'rest')},
                    max_by_kind={k: float(ds[kinds == k].max()) for k in ('zone', 'sphere', 'rest') if (kinds == k).any()},
                    node_k_abs_max=float(kabs.max()), kz_negative_check=kz_neg, seed=20261018)
    hist = dict(log10_bin_edges=HB.tolist(), d_over_P0_counts=hd.tolist(), rel_change_counts=hr.tolist(),
                note='counts per bin: index 0 = below the first edge, index i = [edge_(i-1), edge_i), last = above the last edge')
    prof_path = C3.CERT3 / ('out/GQ_FULL_ROWMAX_%s_V001.npy' % label)
    if prof_path.exists():
        raise SystemExit('exists ' + str(prof_path))
    np.save(prof_path, np.stack([kp_k, row_max, row_relbig]))
    full = dict(nodes=int(acc['n']), nodes_tensor=int(acc['n'] - (0 if sphere is None else sphere['nodes'])), nodes_corner_zone=int(acc['n_zone']),
                nodes_S_over_P0_ge_1em6=int(acc['n_big']), nodes_S_zero=int(acc['n_S0']),
                max_abs_diff_over_P0=float(acc['dmax']), max_abs_diff_over_P0_subtracted=float(acc['dsub']),
                max_abs_diff_over_P0_dP_first=float(acc['ddp']), max_corner_zone=float(acc['dzone']), max_rest_of_D=float(acc['drest']),
                sphere_piece=sphere, max_rel_change=float(acc['rel']), max_rel_change_S_over_P0_ge_1em6=float(acc['relbig']),
                max_S_over_P0=float(acc['smax']), at=at, histogram=hist,
                all_kperp_nodes_bound_over_P0=bmax, bound_k_perp_at_max=kat,
                row_max_profile={'path': str(prof_path), 'sha256': CC.sha(prof_path), 'rows': ['k_perp_inverse_kpc', 'max_kz_d_over_P0', 'max_kz_rel_S_ge_1em6']},
                k_abs_max_inverse_kpc=kabs_max, k_z_half='k_z >= 0 tensor nodes; k_z < 0 by symmetry (kz_negative_check)')
    rec = dict(schema='UVT_GQ_FULL_PART_C2V003', label=label, role=role, roster_state=cid, state_result_sha256=case.result_sha,
               source_rotation=str(case.src_rot), i1t=i1t, kept=kept, outer=outer, quadrature=C3.QUAD_DDO, R_eval_max_kpc=C3.R_EVAL_DDO,
               grid=dict(N_perp=int(len(kp_k)), N_z_plus=int(len(kz_k)), kp_intervals=g['kp_intervals'], kz_intervals=g['kz_intervals'],
                         families=fam, top=g['top'], topz=g['topz']),
               P0=P0, gas_mass_kg=mass, P0_over_gas_mass=P0 / mass, n_present_columns=int(gas.present.sum()),
               contract_sample=contract, full_domain=full, threshold_over_P0=1e-12,
               verdict_part='PASS' if (full['max_abs_diff_over_P0'] <= 1e-12 and contract['max_abs_diff_over_P0'] <= 1e-12) else 'UV_TAIL_GAS_QUADRATURE_UNCERTIFIED',
               producer=CC.producer(__file__), common=CC.producer(C3.HERE / 'certs3_common_c2v003.py'),
               pins={k: CC.pin(k) for k in ('uvt_lapse', 'uvt_roster', 'uvt_jn', 'profile')}, method=__doc__.split('Usage:')[0].strip(),
               decisions=C3.decisions(), seconds=round(time.time() - t0, 1))
    h = C3.write_new(C3.CERT3 / ('out/GQ_FULL_%s_V001.json' % label), rec)
    print(json.dumps(dict(label=label, verdict=rec['verdict_part'], full_max=full['max_abs_diff_over_P0'], nodes=full['nodes'],
                          rel=full['max_rel_change'], relbig=full['max_rel_change_S_over_P0_ge_1em6'], sample_max=contract['max_abs_diff_over_P0'],
                          sha256=h, seconds=rec['seconds'])), flush=True)


if __name__ == '__main__':
    main()
