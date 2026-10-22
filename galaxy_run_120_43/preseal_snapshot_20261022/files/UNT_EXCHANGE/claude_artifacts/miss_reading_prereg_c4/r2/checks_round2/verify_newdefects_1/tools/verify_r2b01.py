"""Independent synthetic check of finding R2B-01 against the r2 text (PREREG_MISS_READING_R2.md 97d5ce33...).

Written from the r2 text section 2 (L189-L232), section 1.1 L119, section 4 L322-L325 and section 5.3 L357-L362 alone.
No module import, no file read, synthetic ratios only. Writes one JSON file in this verify folder.

Row states (one per query id):
  ('INV',)   INVALID for this document (built-in reason, or a gate registered before step 5)
  ('LATE',)  producer-INVALID row under a LATE gate: a non-INVALID MISS with sign UNDEFINED (C-4 L324)
  ('NULL',)  VALID row with a null sigma_ratio: a MISS with sign UNDEFINED (C-1.1 L119)
  ('R', r)   VALID row with ratio r: HIT iff |r| <= 1 (C-1.1 table)
  ('PINV',)  producer-INVALID gated row whose treatment is chosen by the caller: 'early' -> INV, 'late' -> LATE
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, 'VERIFY_R2B01_RESULTS.json')
BAD = ('rotmod', 'vobs', 'massmodels', 'sparc', 'uvt_', 'runs_ext', 'kmax_a2f10_c5h_run_v001')


def _fence(event, args):
    if event == 'open':
        path = str(args[0]) if args else ''
        low = path.lower()
        if any(b in low for b in BAD):
            raise PermissionError('fence: forbidden name class ' + path)
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
                  (mode is None and isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        if writing and not os.path.abspath(path).startswith(HERE + os.sep):
            raise PermissionError('fence: write outside the verify folder ' + path)
    elif event.startswith(('subprocess', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'socket.')):
        raise PermissionError('fence: ' + event)


sys.addaudithook(_fence)

IDS = ['Q%02d' % i for i in range(1, 44)]
ZONE = {q: ('INNER' if i <= 24 else ('TRANSITION' if i <= 35 else 'OUTER')) for i, q in zip(range(1, 44), IDS)}
ZONES = ('INNER', 'TRANSITION', 'OUTER')
BUILTIN = ('Q01', 'Q02')            # QUERY_INSIDE_INNERMOST_NODE under the primary GL4 (C-4 table)
U = 'UNDEFINED'


def median(v):
    v = sorted(v)
    n = len(v)
    if n == 0:
        return None
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def sclass(m):
    if m is None:
        return U
    return 'DEFICIT' if m < -1 else ('EXCESS' if m > 1 else 'CENTERED')


def resolve(rows, gate_mode):
    out = {}
    for q in IDS:
        s = rows.get(q, ('R', 0.0))
        if q in BUILTIN:
            s = ('INV',)
        if s[0] == 'PINV':
            s = ('INV',) if gate_mode == 'early' else ('LATE',)
        out[q] = s
    return out


def classify(rows, variant='R2', sem='strict', gate_mode='late'):
    """variant: R2 (text as written); FJ (finding JSON: S := UNDEFINED whenever M-U < Nv/2);
    FQ (finding REVIEW.md: same, only when Z is miss-dominated); FB (this check: only when Z is
    miss-dominated and M-U < H).  sem: strict (L201: any condition using an UNDEFINED quantity is false,
    the test 'S is UNDEFINED' included); value (UNDEFINED compared as a label); explicit (P14/P15 test
    definedness explicitly; P6 requires every S defined)."""
    rs = resolve(rows, gate_mode)
    zs = {}
    for Z in ZONES:
        zr = [rs[q] for q in IDS if ZONE[q] == Z]
        nonin = [s for s in zr if s[0] != 'INV']
        hits = [s for s in nonin if s[0] == 'R' and abs(s[1]) <= 1.0]
        Nv = len(nonin)
        H = len(hits)
        M = Nv - H
        Uz = sum(1 for s in nonin if s[0] in ('LATE', 'NULL'))
        signed_miss = M - Uz
        m = median([s[1] for s in nonin if s[0] == 'R'])
        md = Nv >= 1 and M >= Nv / 2.0
        hd = Nv >= 1 and H > Nv / 2.0
        S = sclass(m)
        if variant == 'FJ' and Nv >= 1 and signed_miss < Nv / 2.0:
            S = U
        elif variant == 'FQ' and md and signed_miss < Nv / 2.0:
            S = U
        elif variant == 'FB' and md and signed_miss < H:
            S = U
        zs[Z] = dict(Nv=Nv, H=H, M=M, U=Uz, signed_miss=signed_miss, m=m, S=S, md=md, hd=hd,
                     I=len(zr) - Nv)
    # outer trend (L205-L207)
    o = [rs[q][1] for q in IDS if ZONE[q] == 'OUTER' and rs[q][0] == 'R']    # id order = radius order
    if len(o) < 2:
        d_out = None
    else:
        k = len(o) // 2
        d_out = median(o[k:]) - median(o[:k])
    I, T, O = zs['INNER'], zs['TRANSITION'], zs['OUTER']

    def eq(S, label):                       # a condition comparing S with a defined label
        return S != U and S == label

    def is_undef(S):                         # the P14/P15 definedness test
        if sem == 'strict':
            return False                     # L201 read literally: the condition uses an UNDEFINED quantity
        return S == U

    growing = eq(O['S'], 'DEFICIT') and d_out is not None and d_out < 0 and \
        T['m'] is not None and O['m'] is not None and T['m'] > O['m']
    M_tot = sum(zs[Z]['M'] for Z in ZONES)
    Nv_tot = sum(zs[Z]['Nv'] for Z in ZONES)
    p = {}
    p['P0'] = any(zs[Z]['I'] > 0 for Z in ZONES)
    p['P1'] = O['md'] and eq(O['S'], 'DEFICIT')
    p['P1g'] = p['P1'] and growing
    p['P2'] = O['md'] and eq(O['S'], 'EXCESS')
    p['P11'] = O['md'] and eq(O['S'], 'CENTERED')
    p['P3'] = I['md'] and eq(I['S'], 'EXCESS')
    p['P4'] = I['md'] and eq(I['S'], 'DEFICIT')
    p['P12'] = I['md'] and eq(I['S'], 'CENTERED')
    p['P13'] = T['md']
    p['P5'] = I['hd'] and O['md'] and T['Nv'] >= 1 and not T['hd']
    if sem == 'value':
        p6 = (I['S'] == T['S'] == O['S']) and I['S'] != 'CENTERED'
    else:
        p6 = all(zs[Z]['S'] != U for Z in ZONES) and (I['S'] == T['S'] == O['S']) and I['S'] != 'CENTERED'
    p['P6'] = p6 and all(zs[Z]['Nv'] >= 1 for Z in ZONES)
    p['P7'] = M_tot >= 1 and not any(zs[Z]['md'] for Z in ZONES)
    p['P8'] = Nv_tot >= 1 and M_tot == 0
    p['P9'] = O['Nv'] == 0
    if variant != 'R2':
        p['P14'] = O['md'] and is_undef(O['S'])
        p['P15'] = I['md'] and is_undef(I['S'])
    zone_set = ['P1', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13'] + (['P14', 'P15'] if variant != 'R2' else [])
    of_def1 = O['md']                                             # "OUTER is miss-dominated, whatever its sign class"
    of_def2 = p['P1'] or p['P2'] or p['P11'] or p.get('P14', False)   # "exactly when one of P1, P2 or P11 holds"

    def e3(of):
        if O['Nv'] == 0:
            return 'NOT_TESTABLE'
        return 'TESTED-NEGATIVE' if of else 'NOT_NEGATIVE_AT_OUTER'
    coverage_ok = (M_tot == 0) or any(p[x] for x in zone_set) or p['P7']
    return dict(zones=zs, d_out=d_out, growing=growing, patterns=sorted(k for k, v in p.items() if v),
                p=p, of_def1=of_def1, of_def2=of_def2, e3_def1=e3(of_def1), e3_def2=e3(of_def2),
                coverage_ok=coverage_ok, M_tot=M_tot)


OQ = IDS[35:43]          # Q36..Q43
IQ = IDS[2:24]           # Q03..Q24
TQ = IDS[24:35]          # Q25..Q35


def mk(spec):
    rows = {q: ('R', 0.0) for q in IDS}
    rows.update(spec)
    return rows


def summary(res):
    O = res['zones']['OUTER']
    Iz = res['zones']['INNER']
    return dict(patterns=res['patterns'], OUTER={k: O[k] for k in ('Nv', 'H', 'M', 'U', 'm', 'S', 'md')},
                INNER={k: Iz[k] for k in ('Nv', 'H', 'M', 'U', 'm', 'S', 'md', 'hd')},
                d_out=res['d_out'], growing=res['growing'], of=[res['of_def1'], res['of_def2']],
                e3=[res['e3_def1'], res['e3_def2']], coverage_ok=res['coverage_ok'])


def named_cases():
    c = {}
    c['C14_like_outer_all_null'] = mk({q: ('NULL',) for q in OQ})
    c['C15_like_outer_all_late'] = mk({q: ('LATE',) for q in OQ})
    c['C40_like_inner_all_late'] = mk({q: ('LATE',) for q in IQ})
    c['C16a_like'] = mk({q: ('R', -3.0 if i < 4 else 0.0) for i, q in enumerate(OQ)})
    c['C16b_like'] = mk({q: (('LATE',) if i < 4 else ('R', 0.0)) for i, q in enumerate(OQ)})
    c['C16c_like'] = mk({q: ('R', 3.0 if i < 4 else -3.0) for i, q in enumerate(OQ)})
    c['C16d_like'] = mk({q: (('LATE',) if i < 4 else ('R', -3.0)) for i, q in enumerate(OQ)})
    c['C17c_like'] = mk({q: ('R', float(v)) for q, v in zip(OQ, [-3, -3, -3, -3, -2, -2, -6, -6])})
    c['C17d_like'] = mk({q: (('R', float(v)) if v is not None else ('LATE',))
                         for q, v in zip(OQ, [-3, -3, -3, -3, -2, -2, None, None])})
    return c


def counterfactual_cases():
    """The same producer output (PINV = producer-INVALID, gate-listed rows) under an early gate and a LATE gate."""
    c = {}
    c['G1_outer_all_pinv'] = mk({q: ('PINV',) for q in OQ})
    c['G2_C16b_rows'] = mk({q: (('PINV',) if i < 4 else ('R', 0.0)) for i, q in enumerate(OQ)})
    c['G3_C16d_rows'] = mk({q: (('PINV',) if i < 4 else ('R', -3.0)) for i, q in enumerate(OQ)})
    c['G4_C17d_rows'] = mk({q: (('R', float(v)) if v is not None else ('PINV',))
                            for q, v in zip(OQ, [-3, -3, -3, -3, -2, -2, None, None])})
    spec = {q: (('PINV',) if i < 12 else ('R', 0.0)) for i, q in enumerate(IQ)}
    spec.update({q: ('R', 2.0) for q in TQ})
    spec.update({q: ('R', -3.0) for q in OQ})
    c['G5_inner_P5_rows'] = mk(spec)
    c['G6_inner_three_pinv_rest_hit'] = mk({q: ('PINV',) for q in IQ[:3]})
    spec = {q: ('R', -3.0) for q in OQ[:3]}
    spec[OQ[3]] = ('R', 0.0)
    spec.update({q: ('PINV',) for q in OQ[4:]})
    c['G7_outer_3def_1hit_4pinv'] = mk(spec)
    return c


def rand_outcome(rng):
    rows = {}
    for Z, qs in (('INNER', IQ), ('TRANSITION', TQ), ('OUTER', OQ)):
        w = [rng.random() ** 2 for _ in range(6)]   # INV, PINV, NULL, HIT, MISS-, MISS+
        if rng.random() < 0.15:
            w[2] = 0.0
        tot = sum(w)
        w = [x / tot for x in w]
        for q in qs:
            x = rng.random()
            acc = 0.0
            for kind, wk in zip(('INV', 'PINV', 'NULL', 'HIT', 'MM', 'MP'), w):
                acc += wk
                if x <= acc:
                    break
            if kind == 'INV':
                rows[q] = ('INV',)
            elif kind == 'PINV':
                rows[q] = ('PINV',)
            elif kind == 'NULL':
                rows[q] = ('NULL',)
            elif kind == 'HIT':
                rows[q] = ('R', rng.choice([-1.0, -0.6, -0.2, 0.0, 0.3, 0.7, 1.0]))
            elif kind == 'MM':
                rows[q] = ('R', rng.choice([-1.0000001, -1.5, -2.0, -3.0, -5.0, -6.0]))
            else:
                rows[q] = ('R', rng.choice([1.0000001, 1.5, 2.0, 3.0, 5.0, 6.0]))
    return rows


def sweep(n, seed):
    rng = random.Random(seed)
    stats = {}
    zone_pats = ('P1', 'P1g', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13', 'P6', 'P5', 'P7', 'P8', 'P9', 'P14', 'P15')
    combos = [('R2', 'strict'), ('FJ', 'strict'), ('FJ', 'value'), ('FJ', 'explicit'),
              ('FQ', 'strict'), ('FQ', 'explicit'), ('FB', 'strict'), ('FB', 'explicit')]
    for v, s in combos:
        stats[v + '/' + s] = dict(n=0, of_disagree=0, of_disagree_not_all_unsigned=0, all_unsigned_outer=0,
                                  coverage_fail=0, coverage_fail_unexplained=0, e3_disagree=0,
                                  p6_with_no_zone_miss_dominated=0, sign_from_hits_alone=0,
                                  late_vs_early_removed={k: 0 for k in zone_pats},
                                  late_vs_early_added={k: 0 for k in zone_pats},
                                  defined_S_changed=0, d_out_changed=0, growing_changed=0)
    for _ in range(n):
        rows = rand_outcome(rng)
        for v, s in combos:
            st = stats[v + '/' + s]
            st['n'] += 1
            late = classify(rows, v, s, 'late')
            early = classify(rows, v, s, 'early')
            O = late['zones']['OUTER']
            all_uns = O['Nv'] >= 1 and O['U'] == O['Nv']
            st['all_unsigned_outer'] += all_uns
            if late['of_def1'] != late['of_def2']:
                st['of_disagree'] += 1
                if not all_uns:
                    st['of_disagree_not_all_unsigned'] += 1
            if late['e3_def1'] != late['e3_def2']:
                st['e3_disagree'] += 1
            if not late['coverage_ok']:
                st['coverage_fail'] += 1
                zz = late['zones']
                expl = (not zz['TRANSITION']['md']) and all(
                    (not zz[Z]['md']) or (zz[Z]['U'] == zz[Z]['Nv']) or v != 'R2' for Z in ('INNER', 'OUTER'))
                if not expl:
                    st['coverage_fail_unexplained'] += 1
            if late['p']['P6'] and not any(late['zones'][Z]['md'] for Z in ZONES):
                st['p6_with_no_zone_miss_dominated'] += 1
            for Z, pats in (('OUTER', ('P1', 'P2', 'P11')), ('INNER', ('P3', 'P4', 'P12'))):
                zz = late['zones'][Z]
                if any(late['p'][x] for x in pats) and zz['signed_miss'] == 0:
                    st['sign_from_hits_alone'] += 1
            for k in zone_pats:
                a, b = early['p'].get(k, False), late['p'].get(k, False)
                if a and not b:
                    st['late_vs_early_removed'][k] += 1
                if b and not a:
                    st['late_vs_early_added'][k] += 1
            for Z in ZONES:
                se, sl = early['zones'][Z]['S'], late['zones'][Z]['S']
                if se != U and sl != U and se != sl:
                    st['defined_S_changed'] += 1
            if early['d_out'] != late['d_out']:
                st['d_out_changed'] += 1
            if early['growing'] != late['growing']:
                st['growing_changed'] += 1
    return stats


def main():
    res = {'object_prereg_sha256': '97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407',
           'note': 'synthetic ratios only; no file read; written from the r2 text',
           'named_r2': {}, 'counterfactual_r2': {}, 'fix_checks': {}, 'sweep': None}
    for name, rows in named_cases().items():
        res['named_r2'][name] = summary(classify(rows, 'R2', 'strict', 'late'))
    for name, rows in counterfactual_cases().items():
        res['counterfactual_r2'][name] = {g: summary(classify(rows, 'R2', 'strict', g)) for g in ('early', 'late')}
    allhit = mk({})
    fx = {}
    for v, s in (('FJ', 'strict'), ('FJ', 'value'), ('FJ', 'explicit'), ('FQ', 'strict'), ('FQ', 'explicit'),
                 ('FB', 'strict'), ('FB', 'explicit')):
        key = v + '/' + s
        fx[key] = {
            'all_hit': summary(classify(allhit, v, s)),
            'C15_like': summary(classify(named_cases()['C15_like_outer_all_late'], v, s)),
            'C40_like': summary(classify(named_cases()['C40_like_inner_all_late'], v, s)),
            'C16b_like': summary(classify(named_cases()['C16b_like'], v, s)),
            'C16d_like': summary(classify(named_cases()['C16d_like'], v, s)),
            'C17d_like': summary(classify(named_cases()['C17d_like'], v, s)),
            'G7_early': summary(classify(counterfactual_cases()['G7_outer_3def_1hit_4pinv'], v, s, 'early')),
            'G7_late': summary(classify(counterfactual_cases()['G7_outer_3def_1hit_4pinv'], v, s, 'late')),
        }
    res['fix_checks'] = fx
    res['sweep'] = {'n': 40000, 'seed': 20261018, 'stats': sweep(40000, 20261018)}
    with open(OUT, 'w') as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
