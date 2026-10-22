# Claude4 text-stage helper (dispatch 0619 / A98, r3 TEXT BUILDER). Synthetic self-test of the r3 pattern rules.
# It encodes the r3 text's §2 and §4 rules (S(Z), P0-P15, P1g/P11g, OUTER_FAILURE, LATE gates, the deficit-type
# score relation) and checks the FORMAL claims the text makes on random and exhaustive synthetic outcomes.
# Synthetic dimensionless ratios only. It reads no file, opens no target, launches nothing, and writes only --out
# (exclusive create). An audit hook refuses every other write, subprocess and socket use.
# usage: python3 -I -B verify_r3_rules_c4.py --out RESULT.json [--samples N] [--seed S]
import argparse, itertools, json, os, random, sys

_OUT = []


def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND))
        if writing and os.path.abspath(os.fsdecode(path)) not in _OUT:
            raise PermissionError('write refused: %r' % (path,))
    elif event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.exec', 'os.fork', 'socket.connect',
                   'socket.getaddrinfo', 'os.remove', 'os.rename', 'shutil.rmtree'):
        raise PermissionError('refused: %s' % event)


ZONES = ('INNER', 'TRANSITION', 'OUTER')
HIT_R = (-1.0, -0.5, 0.0, 0.5, 1.0)
MISS_R = (-3.0, -2.0, -1.5, -1.01, 1.01, 1.5, 2.0, 3.0)


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def zone_summary(rows, late):
    """rows: list of (kind, r, tsr). kind in HIT, MISS, NULLR, GATE, BUILTIN. Returns the r3 §2 summary."""
    nv = h = m = u = i = 0
    defined = []
    signed_deficit = signed_excess = 0
    for kind, r, _ in rows:
        if kind == 'BUILTIN' or (kind == 'GATE' and not late):
            i += 1
            continue
        nv += 1
        if kind == 'HIT':
            h += 1
            defined.append(r)
        elif kind == 'MISS':
            m += 1
            defined.append(r)
            if r < -1:
                signed_deficit += 1
            elif r > 1:
                signed_excess += 1
        else:                       # NULLR, or GATE under LATE: an unsigned MISS
            m += 1
            u += 1
    med = median(defined)
    miss_dom = nv >= 1 and 2 * m >= nv
    hit_dom = nv >= 1 and 2 * h > nv
    if med is None or (miss_dom and 2 * (m - u) < nv):
        s = 'UNDEFINED'
    elif med < -1:
        s = 'DEFICIT'
    elif med > 1:
        s = 'EXCESS'
    else:
        s = 'CENTERED'
    return dict(nv=nv, h=h, m=m, u=u, i=i, med=med, s=s, miss_dom=miss_dom, hit_dom=hit_dom,
                signed_deficit=signed_deficit, signed_excess=signed_excess, defined=defined)


def outer_trend(rows):
    d = [r for kind, r, _ in rows if kind in ('HIT', 'MISS')]       # radius order is list order
    n = len(d)
    if n < 2:
        return None, None
    near, far = d[:n // 2], d[n // 2:]                                 # odd count: the middle row goes to the far half
    return median(far) - median(near), median(far)


def classify(z, late):
    S = {k: zone_summary(z[k], late) for k in ZONES}
    dout, far_med = outer_trend(z['OUTER'])
    O, I, T = S['OUTER'], S['INNER'], S['TRANSITION']
    pats = set()
    if any(S[k]['i'] > 0 for k in ZONES):
        pats.add('P0')
    if O['miss_dom']:
        pats.add({'DEFICIT': 'P1', 'EXCESS': 'P2', 'CENTERED': 'P11', 'UNDEFINED': 'P14'}[O['s']])
    if I['miss_dom']:
        pats.add({'DEFICIT': 'P4', 'EXCESS': 'P3', 'CENTERED': 'P12', 'UNDEFINED': 'P15'}[I['s']])
    if T['miss_dom']:
        pats.add('P13')
    if I['hit_dom'] and O['miss_dom'] and T['nv'] >= 1 and not T['hit_dom']:
        pats.add('P5')
    if all(S[k]['s'] != 'UNDEFINED' for k in ZONES) and len({S[k]['s'] for k in ZONES}) == 1 and O['s'] != 'CENTERED':
        pats.add('P6')
    total_m = sum(S[k]['m'] for k in ZONES)
    total_nv = sum(S[k]['nv'] for k in ZONES)
    if total_m >= 1 and not any(S[k]['miss_dom'] for k in ZONES):
        pats.add('P7')
    if total_nv >= 1 and total_m == 0:
        pats.add('P8')
    if O['nv'] == 0:
        pats.add('P9')
    if any(tsr and kind in ('MISS', 'NULLR') for k in ZONES for kind, _, tsr in z[k]):
        pats.add('P10')
    trend_ok = dout is not None and dout < 0 and T['med'] is not None and O['med'] is not None and T['med'] > O['med']
    if 'P1' in pats and trend_ok:
        pats.add('P1g')
    if 'P11' in pats and trend_ok and far_med is not None and far_med < -1:
        pats.add('P11g')
    of = O['miss_dom']
    e3 = 'TESTED-NEGATIVE' if of else ('NOT_NEGATIVE_AT_OUTER' if O['nv'] >= 1 else 'NOT_TESTABLE')
    if not of:
        deficit_reading = None
    elif O['s'] in ('DEFICIT', 'CENTERED') and O['signed_deficit'] >= 1:
        deficit_reading = 'CONSISTENT'
    else:
        deficit_reading = 'NOT_ADDRESSED:' + {'EXCESS': 'EXCESS', 'UNDEFINED': 'UNSIGNED'}.get(O['s'], 'NO_DEFICIT_MISS')
    return dict(S=S, dout=dout, pats=pats, of=of, e3=e3, deficit_reading=deficit_reading)


KINDS = ('HIT', 'MISS', 'NULLR', 'GATE', 'BUILTIN')


def rand_row(rng, wts):
    kind = rng.choices(KINDS, weights=wts)[0]
    r = rng.choice(HIT_R) if kind == 'HIT' else (rng.choice(MISS_R) if kind == 'MISS' else None)
    return (kind, r, False)


E3_ORDER = {'NOT_TESTABLE': 0, 'NOT_NEGATIVE_AT_OUTER': 1, 'TESTED-NEGATIVE': 2}
CAN_REMOVE = {'P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P11', 'P11g', 'P12'}
CAN_ADD = {'P5', 'P7', 'P13', 'P14', 'P15'}


def check(z, tally, witnesses):
    a = classify(z, late=True)
    fails = []
    p = a['pats']
    outer = [x for x in ('P1', 'P2', 'P11', 'P14') if x in p]
    if a['of'] != bool(outer) or len(outer) > 1:
        fails.append('C1_OUTER_FAILURE_EQUIVALENCE')
    total_m = sum(a['S'][k]['m'] for k in ZONES)
    if total_m >= 1 and not (p & {'P1', 'P2', 'P11', 'P14', 'P3', 'P4', 'P12', 'P15', 'P13', 'P7'}):
        fails.append('C2_COVERAGE')
    for k in ZONES:
        s = a['S'][k]
        if s['med'] is not None and abs(s['med']) > 1 and not s['miss_dom']:
            fails.append('C3_SIGNED_CLASS_IMPLIES_MISS_DOMINATED')
        if s['miss_dom'] and s['s'] in ('DEFICIT', 'EXCESS', 'CENTERED') and 2 * (s['m'] - s['u']) < s['nv']:
            fails.append('C6_SIGN_FROM_A_MINORITY')
        if s['miss_dom'] and s['s'] != 'UNDEFINED' and s['m'] - s['u'] == 0:
            fails.append('C6_SIGN_FROM_HITS_ALONE')
    inner_hd = a['S']['INNER']['hit_dom']
    if ('P5' in p) != (inner_hd and a['of'] and 'P13' in p):
        fails.append('C4_P5_EQUIVALENCE')
    if 'P6' in p and not ((p & {'P1', 'P2'}) and (p & {'P3', 'P4'}) and 'P13' in p):
        fails.append('C5_P6_IMPLIES_ZONE_PATTERNS')
    if any(kind == 'GATE' for k in ZONES for kind, _, _ in z[k]):
        b = classify(z, late=False)
        tally['late_pairs'] += 1
        for k in ZONES:
            sl, so = a['S'][k], b['S'][k]
            if sl['nv'] < so['nv'] or sl['m'] < so['m'] or sl['h'] != so['h'] or sl['med'] != so['med']:
                fails.append('C7a_COUNTS_OR_MEDIAN')
            if so['s'] != 'UNDEFINED' and sl['s'] not in (so['s'], 'UNDEFINED'):
                fails.append('C7b_DEFINED_SIGN_CHANGED')
            if so['s'] == 'UNDEFINED' and sl['s'] != 'UNDEFINED':
                fails.append('C7b_UNDEFINED_BECAME_DEFINED')
            if so['miss_dom'] and not sl['miss_dom']:
                fails.append('C7c_MISS_DOMINATION_REMOVED')
            if sl['hit_dom'] and not so['hit_dom']:
                fails.append('C7c_HIT_DOMINATION_ADDED')
        if a['dout'] != b['dout']:
            fails.append('C7a_DELTA_OUT_CHANGED')
        removed, added = b['pats'] - a['pats'], a['pats'] - b['pats']
        for x in removed:
            tally['removed'][x] = tally['removed'].get(x, 0) + 1
            witnesses.setdefault('removed_' + x, z)
            if x not in CAN_REMOVE:
                fails.append('C7d_UNLISTED_REMOVAL_' + x)
        for x in added:
            tally['added'][x] = tally['added'].get(x, 0) + 1
            witnesses.setdefault('added_' + x, z)
            if x not in CAN_ADD:
                fails.append('C7d_UNLISTED_ADDITION_' + x)
        if E3_ORDER[a['e3']] < E3_ORDER[b['e3']]:
            fails.append('C7e_E3_TOWARD_FAVOURABLE')
        if a['e3'] != b['e3']:
            key = '%s->%s' % (b['e3'], a['e3'])
            tally['e3_moves'][key] = tally['e3_moves'].get(key, 0) + 1
        if b['of'] and not a['of']:
            fails.append('C7g_OUTER_FAILURE_REMOVED')
        if a['deficit_reading'] == 'CONSISTENT' and b['deficit_reading'] != 'CONSISTENT':
            fails.append('C7f_DEFICIT_READING_BECAME_CONSISTENT')
        if b['deficit_reading'] != a['deficit_reading']:
            key = '%s->%s' % (b['deficit_reading'], a['deficit_reading'])
            tally['deficit_reading_moves'][key] = tally['deficit_reading_moves'].get(key, 0) + 1
    for f in fails:
        tally['fail'][f] = tally['fail'].get(f, 0) + 1
        witnesses.setdefault('FAIL_' + f, z)
    tally['outcomes'] += 1
    for x in p:
        tally['patterns_seen'][x] = tally['patterns_seen'].get(x, 0) + 1


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=200000)
    ap.add_argument('--seed', type=int, default=20261018)
    a = ap.parse_args()
    _OUT.append(os.path.abspath(a.out))
    sys.addaudithook(_hook)
    rng = random.Random(a.seed)
    tally = dict(outcomes=0, late_pairs=0, fail={}, removed={}, added={}, e3_moves={}, deficit_reading_moves={},
                 patterns_seen={})
    witnesses = {}
    for _ in range(a.samples):
        wts = [rng.random() for _ in KINDS]
        z = {k: [rand_row(rng, wts) for _ in range(rng.randint(0, 6))] for k in ZONES}
        t = z['TRANSITION']
        if t and rng.random() < 0.5:                                    # one flagged transition row, like the TSR row
            j = rng.randrange(len(t))
            t[j] = (t[j][0], t[j][1], True)
        check(z, tally, witnesses)
    cells = [('HIT', 0.0), ('HIT', -0.5), ('MISS', -3.0), ('MISS', -1.5), ('MISS', 1.5), ('MISS', 3.0),
             ('NULLR', None), ('GATE', None), ('BUILTIN', None)]
    others = [[], [('HIT', 0.0, False)], [('MISS', -2.0, False)], [('MISS', 2.0, False), ('HIT', 0.5, False)],
              [('GATE', None, False), ('HIT', 0.0, False)], [('NULLR', None, False)]]
    n_exh = 0
    for n in range(0, 5):
        for seq in itertools.product(cells, repeat=n):
            orow = [(k, r, False) for k, r in seq]
            for inner in others:
                for trans in others:
                    check({'INNER': list(inner), 'TRANSITION': list(trans), 'OUTER': orow}, tally, witnesses)
                    n_exh += 1
    res = dict(schema='UNT_MISS_READING_R3_RULES_SELFTEST_C4V001', seed=a.seed, random_samples=a.samples,
               exhaustive_outcomes=n_exh, tally=tally, all_checks_pass=not tally['fail'],
               can_remove_claimed=sorted(CAN_REMOVE), can_add_claimed=sorted(CAN_ADD),
               can_remove_witnessed=sorted(tally['removed']), can_add_witnessed=sorted(tally['added']),
               witnesses={k: v for k, v in sorted(witnesses.items())},
               note='synthetic dimensionless ratios only; existence counts, not frequencies; no target, no file read')
    text = json.dumps(res, indent=1, sort_keys=True) + '\n'
    with open(a.out, 'x') as f:
        f.write(text)
    print(json.dumps({k: res[k] for k in ('all_checks_pass', 'exhaustive_outcomes', 'random_samples')}))
    print(json.dumps(tally['fail']))
    print(json.dumps({'removed': tally['removed'], 'added': tally['added'], 'e3_moves': tally['e3_moves'],
                      'deficit_reading_moves': tally['deficit_reading_moves']}, sort_keys=True))
    return 0 if res['all_checks_pass'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
