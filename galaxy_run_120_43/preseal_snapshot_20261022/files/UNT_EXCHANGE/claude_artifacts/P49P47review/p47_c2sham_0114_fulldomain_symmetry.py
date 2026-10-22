"""Owner-by-owner C2 intertwiner check on the COMPLETE old (2304) and Born
(5,308,416) tensor domains, including all off-image Born states. Vectorized numpy.
Own code; no Codex import. Diagonal owners compared by integer feature counts
(coefficientwise); off-diagonal owners by target and literal coefficient value."""
import json, os
import numpy as np

OLD = dict(V=2, E=4, edges=[(0, 1)] * 4)
BORN = dict(V=4, E=8, edges=[(0, 3), (2, 1)] * 4)
CUTS = (0, 1, 2, 3)
DSTAR = 2


def enumerate_domain(G):
    V, E = G['V'], G['E']
    inc = np.arange(1 << E, dtype=np.int64)
    p = np.arange(1 << V, dtype=np.int64)
    q = np.arange(1 << V, dtype=np.int64)
    cells = np.arange(3 ** V, dtype=np.int64)
    r = np.zeros_like(cells); s = np.zeros_like(cells)
    c = cells.copy()
    for v in range(V):
        d = c % 3; c //= 3
        r |= (d == 1).astype(np.int64) << v
        s |= (d == 2).astype(np.int64) << v
    I, P, Qa, C = np.meshgrid(inc, p, q, cells, indexing='ij')
    I = I.ravel(); P = P.ravel(); Qa = Qa.ravel(); C = C.ravel()
    return dict(inc=I, p=P, q=Qa, r=r[C], s=s[C])


def bit(x, i):
    return (x >> i) & 1


def popc(x, n):
    return sum(bit(x, i) for i in range(n))


def perm_bits(x, perm):
    y = np.zeros_like(x)
    for i, j in enumerate(perm):
        y |= bit(x, i) << j
    return y


def apply_U(st, sec, born_edge_perm):
    sp = (1, 0) if sec == 0 else (1, 0, 3, 2)
    ep = (0, 1, 2, 3) if sec == 0 else born_edge_perm
    return dict(inc=perm_bits(st['inc'], ep), p=perm_bits(st['p'], sp), q=perm_bits(st['q'], sp),
                r=perm_bits(st['r'], sp), s=perm_bits(st['s'], sp))


def key(st, sec):
    G = OLD if sec == 0 else BORN
    V, E = G['V'], G['E']
    return st['inc'] | (st['p'] << E) | (st['q'] << (E + V)) | (st['r'] << (E + 2 * V)) | (st['s'] << (E + 3 * V))


def degrees(st, G):
    d = [np.zeros_like(st['inc']) for _ in range(G['V'])]
    for e, (u, v) in enumerate(G['edges']):
        b = bit(st['inc'], e)
        d[u] = d[u] + b; d[v] = d[v] + b
    return d


def diag_features(st, G):
    V = G['V']; d = degrees(st, G)
    return np.stack([
        popc(st['inc'], G['E']),
        sum((d[v] - DSTAR) ** 2 for v in range(V)),
        popc(st['p'], V), popc(st['q'], V),
        sum(d[v] * bit(st['q'], v) for v in range(V)),
        sum(d[v] * bit(st['p'], v) for v in range(V)),
        V - popc(st['r'] | st['s'], V), popc(st['r'], V), popc(st['s'], V)])


def owners(st, sec, Pm):
    """Return dict owner_name -> list over index of (valid_mask, target_state, amp_array)."""
    G = OLD if sec == 0 else BORN
    V = G['V']
    phases = Pm['old_phase'] if sec == 0 else Pm['born_phase']
    out = {'flip': [], 'hop': [], 'bind': [], 'adm_f': [], 'adm_r': []}
    n = st['inc'].shape[0]
    for e, (u, v) in enumerate(G['edges']):
        tg = dict(st); tg['inc'] = st['inc'] ^ (1 << e)
        out['flip'].append((np.ones(n, bool), tg, np.full(n, -Pm['h'], complex)))
        pu, pv = bit(st['p'], u), bit(st['p'], v)
        valid = (bit(st['inc'], e) == 1) & (pu != pv)
        tg = dict(st); tg['p'] = st['p'] ^ (1 << u) ^ (1 << v)
        amp = np.where(pu == 1, -Pm['t'] * np.conj(phases[e]), -Pm['t'] * phases[e])
        out['hop'].append((valid, tg, amp))
    for v in range(V):
        pv = bit(st['p'], v); rv = bit(st['r'], v); sv = bit(st['s'], v)
        tg = dict(st); tg['q'] = st['q'] ^ (1 << v)
        out['bind'].append((pv == 1, tg, np.full(n, Pm['g'], complex)))
        tg = dict(st); tg['p'] = st['p'] | (1 << v); tg['r'] = st['r'] ^ (1 << v); tg['s'] = st['s'] | (1 << v)
        out['adm_f'].append(((rv == 1) & (pv == 0), tg, np.full(n, Pm['kappa'][v], complex)))
        tg = dict(st); tg['p'] = st['p'] ^ (1 << v); tg['r'] = st['r'] | (1 << v); tg['s'] = st['s'] ^ (1 << v)
        out['adm_r'].append(((sv == 1) & (pv == 1), tg, np.full(n, np.conj(Pm['kappa'][v]), complex)))
    return out


def T_old(st):
    cut = sum(bit(st['inc'], e) for e in CUTS)
    valid = cut == 2
    inc = np.zeros_like(st['inc'])
    for e in CUTS:
        b = bit(st['inc'], e)
        inc |= (b << (2 * e)) | (b << (2 * e + 1))
    return valid, dict(inc=inc, p=st['p'], q=st['q'], r=st['r'], s=st['s'])


def Tdag_born(st):
    valid = np.ones(st['inc'].shape[0], bool)
    for x in ('p', 'q', 'r', 's'):
        valid &= (st[x] >> 2) == 0
    n = np.zeros_like(st['inc'])
    for e in CUTS:
        x = bit(st['inc'], 2 * e); y = bit(st['inc'], 2 * e + 1)
        valid &= x == y
        n |= x << e
    valid &= sum(bit(n, e) for e in CUTS) == 2
    return valid, dict(inc=n, p=st['p'], q=st['q'], r=st['r'], s=st['s'])


def check(Pm, born_edge_perm, label):
    res = dict(label=label)
    sites = {0: (1, 0), 1: (1, 0, 3, 2)}
    for sec in (0, 1):
        G = OLD if sec == 0 else BORN
        st = enumerate_domain(G)
        n = st['inc'].shape[0]
        Us = apply_U(st, sec, born_edge_perm)
        UUs = apply_U(Us, sec, born_edge_perm)
        r = dict(n_states=int(n), U2_identity=bool(np.array_equal(key(UUs, sec), key(st, sec))),
                 U_bijective=bool(np.unique(key(Us, sec)).size == n))
        r['diag_features_invariant'] = bool(np.array_equal(diag_features(st, G), diag_features(Us, G)))
        # global/local charges covariance
        r['Q_M_invariant'] = bool(np.array_equal(popc(st['p'], G['V']) + popc(st['r'], G['V']), popc(Us['p'], G['V']) + popc(Us['r'], G['V'])) and np.array_equal(popc(st['r'] | st['s'], G['V']), popc(Us['r'] | Us['s'], G['V'])))
        r['site_q_covariant'] = all(bool(np.array_equal(bit(Us['q'], sites[sec][v]), bit(st['q'], v))) for v in range(G['V']))
        r['site_A_covariant'] = all(bool(np.array_equal(bit(Us['r'] | Us['s'], sites[sec][v]), bit(st['r'] | st['s'], v))) for v in range(G['V']))
        O = owners(st, sec, Pm); OU = owners(Us, sec, Pm)
        ep = (0, 1, 2, 3) if sec == 0 else born_edge_perm
        idxmap = {'flip': ep, 'hop': ep, 'bind': sites[sec], 'adm_f': sites[sec], 'adm_r': sites[sec]}
        own = {}
        for name in O:
            ok = True; bad = 0
            for i, (valid, tg, amp) in enumerate(O[name]):
                j = idxmap[name][i]
                validU, tgU, ampU = OU[name][j]
                m1 = np.array_equal(valid, validU)
                kt = key(apply_U(tg, sec, born_edge_perm), sec); kU = key(tgU, sec)
                m2 = np.array_equal(kt[valid], kU[valid])
                m3 = np.array_equal(amp[valid], ampU[valid])
                if not (m1 and m2 and m3):
                    ok = False
                    bad += int((valid != validU).sum() + (kt[valid] != kU[valid]).sum() + (amp[valid] != ampU[valid]).sum())
            own[name] = dict(ok=ok, mismatches=bad)
        # Birth / unBirth intertwiners
        if sec == 0:
            v1, t1 = T_old(st); v2, t2 = T_old(Us)
            ok = np.array_equal(v1, v2) and np.array_equal(key(apply_U(t1, 1, born_edge_perm), 1)[v1], key(t2, 1)[v1])
            own['Birth_T'] = dict(ok=bool(ok), image_count=int(v1.sum()))
        else:
            v1, t1 = Tdag_born(st); v2, t2 = Tdag_born(Us)
            ok = np.array_equal(v1, v2) and np.array_equal(key(apply_U(t1, 0, born_edge_perm), 0)[v1], key(t2, 0)[v1])
            own['unBirth_Tdag'] = dict(ok=bool(ok), image_count=int(v1.sum()), offimage_count=int((~v1).sum()))
        r['owners'] = own
        res['old' if sec == 0 else 'born'] = r
    res['all_ok'] = all(res[k]['U2_identity'] and res[k]['diag_features_invariant'] and all(o['ok'] for o in res[k]['owners'].values()) for k in ('old', 'born'))
    return res


if __name__ == '__main__':
    k01 = complex(2 / 3, 1 / 5); k23 = complex(-1 / 7, 3 / 4)
    base = dict(h=3 / 11, t=4 / 5, g=5 / 7, kappa=[k01, k01, k23, k23],
                old_phase=[1 + 0j] * 4, born_phase=[1 + 0j] * 8)
    good_perm = tuple(2 * (k // 2) + (1 - k % 2) for k in range(8))
    runs = []
    runs.append(check(base, good_perm, 'POSITIVE: stated C2, phases 1, kappa0=kappa1, kappa2=kappa3 (complex)'))
    gen = dict(base); z = complex(3 / 5, 4 / 5); w = complex(5 / 13, -12 / 13)
    gen['old_phase'] = [1, -1, -1, 1]; gen['born_phase'] = [z, z.conjugate(), w, w.conjugate(), 1j, -1j, 1, 1]
    runs.append(check(gen, good_perm, 'POSITIVE-GEN: real +-1 old phases, Born phi_{2e+1}=conj(phi_{2e})'))
    runs.append(check(base, tuple(range(8)), 'NEGATIVE: wrong child-bit map (no 2e<->2e+1 swap)'))
    bad = dict(base); bad['kappa'] = [k01, k01 * 1.5, k23, k23]
    runs.append(check(bad, good_perm, 'NEGATIVE: kappa0 != kappa1'))
    bad = dict(base); bad['kappa'] = [k01, k01, k23, -k23]
    runs.append(check(bad, good_perm, 'NEGATIVE: kappa2 != kappa3'))
    bad = dict(base); bad['born_phase'] = [1j] * 8
    runs.append(check(bad, good_perm, 'NEGATIVE: Born phases i on both children (not conjugate pair)'))
    bad = dict(base); bad['old_phase'] = [z, 1, 1, 1]
    runs.append(check(bad, good_perm, 'NEGATIVE: one complex old phase'))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_fulldomain_symmetry_out.json')
    with open(out, 'w') as fh:
        json.dump(runs, fh, indent=1)
    for r in runs:
        fails = {sec: [k for k, o in r[sec]['owners'].items() if not o['ok']] for sec in ('old', 'born')}
        print(r['label'], '| all_ok=', r['all_ok'], '| failing owners:', fails,
              '| n=', r['old']['n_states'], r['born']['n_states'],
              '| U2', r['old']['U2_identity'], r['born']['U2_identity'],
              '| diag', r['old']['diag_features_invariant'], r['born']['diag_features_invariant'],
              '| QM', r['old']['Q_M_invariant'], r['born']['Q_M_invariant'],
              '| q,A cov', r['old']['site_q_covariant'], r['born']['site_q_covariant'], r['born']['site_A_covariant'])
    print(json.dumps(runs[0]['born']['owners']), json.dumps(runs[0]['old']['owners']))
