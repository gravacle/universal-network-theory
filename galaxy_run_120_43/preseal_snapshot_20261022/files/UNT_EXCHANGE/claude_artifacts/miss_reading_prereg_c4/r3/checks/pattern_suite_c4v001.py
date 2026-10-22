# pattern_suite_c4v001.py -- integrate stage (helper of lane Claude4), miss-reading prereg r3 (A98.2, dispatch 0619).
# An independent implementation, written from PREREG_MISS_READING_R3.md alone (with ROOT_ITEMS_R3.md M-12 for the case list),
# of the r3 rules: per-zone counts N_v/H/M/U/I, m(Z), miss- and hit-domination, the sign class S(Z), the outer trend
# (Delta_out, GROWING, CROSSING), OUTER_FAILURE, the patterns P0-P15 with the flags P1g and P11g, the E3 verdict line, the
# reading triggers, the three-part status tuple, the deficit-type sign rule, the citable-row scope, the LATE-gate rule, the
# DT-S0G comparison and the R-DRIFT mapping, the STAGE0 receipt rule, gate timing, PROVISIONAL labels and the post-target
# acts (field map, NOT_READ). It does not read or import the text stage's verify_r3_rules_c4.py or R3_RULES_SELFTEST.json.
# Synthetic dimensionless rows only. It opens no file except the two texts it hashes, its own bytes (for its sha) and the
# --out file, which it creates exclusively. No target, no launch, no network. numpy vectorizes the exhaustive enumerations.
# usage: python3 -I -B pattern_suite_c4v001.py --prereg PREREG_MISS_READING_R3.md --root ROOT_ITEMS_R3.md --out RESULTS.json
import argparse, hashlib, itertools, json, platform, random, sys, time
import numpy as np

# ------------------------------------------------------------------------------------------------------------ vocabulary
HIT, MISS, NULL, LATE, INV = 'HIT', 'MISS', 'NULL', 'LATE', 'INVALID'      # NULL: a VALID row with a null sigma_ratio
UND, DEF, EXC, CEN = 0, 1, 2, 3
SNAME = {UND: 'UNDEFINED', DEF: 'DEFICIT', EXC: 'EXCESS', CEN: 'CENTERED'}
ZONES = ('INNER', 'TRANSITION', 'OUTER')
E3N = {0: 'TESTED-NEGATIVE (A15 E3 scope)', 1: 'NOT_NEGATIVE_AT_OUTER', 2: 'NOT_TESTABLE'}
PATS = ('P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P11g', 'P12', 'P13', 'P14', 'P15')
C_, INC, NA_PNH, NA_EXC, NA_UNS, NA_NDM, UNDEF = 0, 1, 2, 3, 4, 5, 9
P1N = {C_: 'CONSISTENT', INC: 'INCONSISTENT', NA_PNH: 'NOT_ADDRESSED (PATTERN_NOT_HELD)', NA_EXC: 'NOT_ADDRESSED (SIGN_SCOPE_EXCESS)',
       NA_UNS: 'NOT_ADDRESSED (SIGN_SCOPE_UNSIGNED)', NA_NDM: 'NOT_ADDRESSED (SIGN_SCOPE_NO_DEFICIT_MISS)', UNDEF: 'UNDEFINED_TUPLE'}
# section 3.2, in table order: triggers (any one), sign scope, deciding-test status at writing, prior evidence (closed list)
READINGS = (
    ('R-MF', ('OF', 'P3', 'P4', 'P12', 'P15', 'P13', 'P6', 'P7'), 'sign-free', 'E3_LINE',
     'for: A15 E2, which expected an outer deficit; A41'),
    ('R-UT1', ('OF',), 'deficit-type', 'OPEN (DT-UT1 NOT SCHEDULED)',
     'against: A41 item 3 (FORMAL + TESTED); no gate-consistent typing gives an attractive tail'),
    ('R-REACH', ('OF',), 'deficit-type', 'OPEN (DT-U12 NOT SCHEDULED)', '-'),
    ('R-HIST', ('OF', 'P13', 'P6', 'P7'), 'sign-free', 'OPEN (DT-BHD NOT SCHEDULED)', '-'),
    ('R-DRIFT', ('OF',), 'sign-free', 'S63_MAPPING',
     'for: the sealed k = 0 drift reading is SUPPORTED (A63); against: its causal gloss is UNTESTED (A65 check R-3)'),
    ('R-S1', ('P2', 'P11', 'P6'), '-', 'OPEN (DT-S1 UNTESTED)', '-'),
    ('R-GRID', ('P2', 'P11'), '-', 'OPEN (none registered)', 'against: T120L passes C2, C3, C4 and C1-prime (A27); N0, NQ, N2, N3-prime pass (A90)'),
    ('R-NAX', ('P11', 'P14', 'P3', 'P4', 'P12', 'P15', 'P13', 'P7'), '-', 'OPEN (DT-NAX not run)', '-'),
    ('R-GEFF', ('P3', 'P4', 'P12', 'P15'), '-', 'OPEN (DT-S1 UNTESTED)', '-'),
    ('R-ML', ('P3', 'P4', 'P12', 'P15'), '-', 'OPEN (DT-ALT NOT_EVALUATED; DT-T1a diagnostic)', 'the ML_3p6 alternatives are NOT_EVALUATED_BEFORE_FREEZE'),
    ('R-SPEC', ('P3', 'P4', 'P12', 'P15'), '-', 'OPEN (DT-T1a diagnostic)', '-'),
    ('R-GEO', ('P3', 'P4', 'P12', 'P15', 'P6'), '-', 'OPEN (DT-GEO NOT_EVALUATED)', '-'),
    ('R-TSR', ('P10',), '-', 'OPEN (DT-TSR NOT SCHEDULED)', 'against: route B consumes the azimuthal mean (A66.2; A42 TESTED)'),
)
RNAMES = tuple(r[0] for r in READINGS)
TRIG = {r[0]: r[1] for r in READINGS}
SCOPE_ZONE = {'OF': 'O', 'P2': 'O', 'P11': 'O', 'P14': 'O', 'P3': 'I', 'P4': 'I', 'P12': 'I', 'P15': 'I', 'P13': 'T',
              'P6': 'ALL', 'P7': 'ALL', 'P10': 'FLAG'}
STAGE0_CODES = ('CONSISTENT', 'AGAINST', 'NOT_DECIDED', 'TWIN_INVALID', 'TWIN_INPUT_DEFECT', 'NOT_EVALUATED_BEFORE_FREEZE',
                'EVALUATED_REFUSED')


# ----------------------------------------------------------------------------------------------- scalar reference rules
def med(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def check_row(row):
    kind, r, fl = row
    if kind == HIT:
        assert r is not None and abs(r) <= 1, row          # WITHIN_ERROR_RULE: |r| <= 1
    elif kind == MISS:
        assert r is not None and abs(r) > 1, row
    else:
        assert r is None, row


def zone_summary(rows):
    """Section 2: counts, m(Z), domination and the sign class. NULL and LATE rows are non-INVALID MISS rows with no ratio."""
    Nv = H = M = U = I = cm = 0
    defined = []
    hasdef = False
    for row in rows:
        kind, r, fl = row
        if kind == INV:
            I += 1
            continue
        Nv += 1
        if kind == HIT:
            H += 1
            defined.append(r)
        else:
            M += 1
            if kind == MISS:
                defined.append(r)
                hasdef = hasdef or r < 0                  # s_q = -1 on a MISS row
                cm += 1
            elif kind == NULL:
                U += 1
                cm += 1                                    # citable as a MISS (it has a frozen prediction), never by sign
            else:
                U += 1                                     # LATE: no frozen prediction, never cited
    m = med(defined)
    missdom = Nv >= 1 and 2 * M >= Nv
    hitdom = Nv >= 1 and 2 * H > Nv
    if m is None or (missdom and 2 * (M - U) < Nv):
        S = UND
    elif m < -1:
        S = DEF
    elif m > 1:
        S = EXC
    else:
        S = CEN
    return {'Nv': Nv, 'H': H, 'M': M, 'U': U, 'I': I, 'm': m, 'missdom': missdom, 'hitdom': hitdom, 'S': S, 'hasdef': hasdef,
            'cm': cm, 'n_defined': len(defined), 'n_late': sum(1 for k, _, _ in rows if k == LATE),
            'n_null': sum(1 for k, _, _ in rows if k == NULL)}


def outer_trend(rows):
    d = [r for kind, r, fl in rows if kind in (HIT, MISS)]   # radius order is row order
    n = len(d)
    if n < 2:
        return None, None
    near, far = d[:n // 2], d[n // 2:]                       # odd count: the middle row goes to the far half
    mf = med(far)
    return mf - med(near), mf


def drift_part1(OF, stage0, rule):
    against = stage0 == 'AGAINST'
    if rule == 'S63':           # the closed mapping of 6.3: part 1 shown under OUTER_FAILURE, else PATTERN_NOT_HELD
        if not OF:
            return NA_PNH
        return INC if against else C_
    if against:                 # the 3 rule taken literally: against takes precedence over everything
        return INC
    return C_ if OF else NA_PNH


def drift_part2(stage0):
    return {'CONSISTENT': 'CONSISTENT (DT-S0G)', 'AGAINST': 'AGAINST (DT-S0G)', 'NOT_DECIDED': 'OPEN (NOT_DECIDED)'}.get(
        stage0, 'OPEN (%s)' % stage0)


def classify(z, stage0='NOT_EVALUATED_BEFORE_FREEZE', drift_rule='S63'):
    """z: {zone: [(kind, r, flagged), ...] in radius order}. Returns the full classification."""
    for Z in ZONES:
        for row in z[Z]:
            check_row(row)
    S_ = {Z: zone_summary(z[Z]) for Z in ZONES}
    I_, T_, O_ = S_['INNER'], S_['TRANSITION'], S_['OUTER']
    dout, farmed = outer_trend(z['OUTER'])
    mT_gt_mO = T_['m'] is not None and O_['m'] is not None and T_['m'] > O_['m']
    GROW = O_['S'] == DEF and dout is not None and dout < 0 and mT_gt_mO
    CROSS = O_['S'] == CEN and dout is not None and dout < 0 and mT_gt_mO and farmed is not None and farmed < -1
    OF = O_['missdom']
    P = {}
    P['P0'] = any(S_[Z]['I'] > 0 for Z in ZONES)
    P['P1'] = O_['missdom'] and O_['S'] == DEF
    P['P1g'] = P['P1'] and GROW
    P['P2'] = O_['missdom'] and O_['S'] == EXC
    P['P11'] = O_['missdom'] and O_['S'] == CEN
    P['P11g'] = P['P11'] and CROSS
    P['P14'] = O_['missdom'] and O_['S'] == UND
    P['P3'] = I_['missdom'] and I_['S'] == EXC
    P['P4'] = I_['missdom'] and I_['S'] == DEF
    P['P12'] = I_['missdom'] and I_['S'] == CEN
    P['P15'] = I_['missdom'] and I_['S'] == UND
    P['P13'] = T_['missdom']
    P['P5'] = I_['hitdom'] and O_['missdom'] and T_['Nv'] >= 1 and not T_['hitdom']
    P['P6'] = (all(S_[Z]['S'] != UND for Z in ZONES) and I_['S'] == T_['S'] == O_['S'] and O_['S'] != CEN)
    Mtot = sum(S_[Z]['M'] for Z in ZONES)
    P['P7'] = Mtot >= 1 and not any(S_[Z]['missdom'] for Z in ZONES)
    P['P8'] = sum(S_[Z]['Nv'] for Z in ZONES) >= 1 and Mtot == 0
    P['P9'] = O_['Nv'] == 0
    P['P10'] = any(fl and kind in (MISS, NULL) for Z in ZONES for kind, r, fl in z[Z])
    E3 = 0 if OF else (1 if O_['Nv'] >= 1 else 2)
    hold = dict(P)
    hold['OF'] = OF
    readings = []
    for name, trig, sign, dt, prior in READINGS:
        th = [t for t in trig if hold[t]]
        if name == 'R-DRIFT':
            p1 = drift_part1(OF, stage0, drift_rule)
            p2 = drift_part2(stage0)
        else:
            if not th:
                p1 = NA_PNH
            elif sign == 'deficit-type':
                cases = [O_['S'] in (DEF, CEN) and O_['hasdef'], P['P2'], P['P14'], P['P11'] and not O_['hasdef']]
                p1 = UNDEF if sum(cases) != 1 else (C_, NA_EXC, NA_UNS, NA_NDM)[cases.index(True)]
            else:
                p1 = C_
            p2 = E3N[E3] if dt == 'E3_LINE' else dt
        scope = []
        for t in th:
            zc = SCOPE_ZONE[t]
            for Z, zk in (('INNER', 'I'), ('TRANSITION', 'T'), ('OUTER', 'O')):
                for j, (kind, r, fl) in enumerate(z[Z]):
                    if kind in (INV, LATE):
                        continue                               # no reading cites a row with no frozen prediction
                    if zc == zk or (zc == 'ALL' and kind in (MISS, NULL)) or (zc == 'FLAG' and fl and kind in (MISS, NULL)):
                        scope.append((Z, j))
        scope = sorted(set(scope))
        has_cit_miss = any(z[Z][j][0] in (MISS, NULL) for Z, j in scope)
        readings.append({'reading': name, 'triggers_holding': th, 'part1': p1, 'part2': p2, 'part3': prior,
                         'scope_rows': len(scope), 'scope_has_citable_miss': has_cit_miss})
    e3_counts = {'S_OUTER': SNAME[O_['S']], 'Delta_out': dout, 'Nv': O_['Nv'], 'H': O_['H'], 'M': O_['M'], 'U': O_['U'],
                 'I': O_['I'], 'n_defined_ratio': O_['n_defined'], 'n_late_gate': O_['n_late'], 'n_null_ratio': O_['n_null']}
    return {'summaries': S_, 'Delta_out': dout, 'far_median': farmed, 'GROWING': GROW, 'CROSSING': CROSS, 'OF': OF,
            'patterns': P, 'E3': E3, 'E3_counts': e3_counts, 'readings': readings, 'anymiss': Mtot >= 1}


def held(res):
    return sorted(p for p in PATS if res['patterns'][p])


# --------------------------------------------------------------------- property checks on one scalar classification
ZONE_PATTERNS = ('P1', 'P2', 'P11', 'P14', 'P3', 'P4', 'P12', 'P15', 'P13')


def scalar_props(res):
    """{property: bool ok} for the claims of sections 2 and 3 on one outcome."""
    P, OF = res['patterns'], res['OF']
    rd = {r['reading']: r for r in res['readings']}
    S_ = res['summaries']
    out = {}
    four = [P['P1'], P['P2'], P['P11'], P['P14']]
    out['OF_iff_P1_P2_P11_P14'] = OF == any(four)
    out['OF_exactly_one_of_four'] = (sum(four) == 1) if OF else (sum(four) == 0)
    out['coverage'] = (not res['anymiss']) or any(P[p] for p in ZONE_PATTERNS) or P['P7']
    out['tuples_defined'] = all(r['part1'] != UNDEF and r['part2'] is not None and r['part3'] is not None for r in res['readings'])
    out['P5_iff_hitdomI_OF_P13'] = P['P5'] == (S_['INNER']['hitdom'] and OF and P['P13'])
    out['P6_implies_P1orP2_P3orP4_P13'] = (not P['P6']) or ((P['P1'] or P['P2']) and (P['P3'] or P['P4']) and P['P13'])
    out['A10_every_miss_two_ways'] = (not res['anymiss']) or (rd['R-MF']['part1'] != NA_PNH and (
        rd['R-HIST']['part1'] != NA_PNH or rd['R-SPEC']['part1'] != NA_PNH))
    out['A15E3_five_readings_under_OF'] = (not OF) or all(rd[n]['part1'] != NA_PNH for n in ('R-MF', 'R-UT1', 'R-REACH', 'R-HIST', 'R-DRIFT'))
    out['deficit_type_never_consistent_under_P2_P14'] = not ((P['P2'] or P['P14']) and (rd['R-UT1']['part1'] == C_ or rd['R-REACH']['part1'] == C_))
    out['E3_tested_negative_iff_OF'] = (res['E3'] == 0) == OF
    out['RMF_part2_is_E3'] = rd['R-MF']['part2'] == E3N[res['E3']]
    out['P1g_only_with_P1'] = (not P['P1g']) or P['P1']
    for Z in ZONES:
        s = S_[Z]
        out['FORMAL_signed_class_implies_missdom_' + Z] = s['S'] not in (DEF, EXC) or s['missdom']
        out['FORMAL_exactly_one_domination_' + Z] = (s['missdom'] != s['hitdom']) if s['Nv'] >= 1 else not (s['missdom'] or s['hitdom'])
    return out


LATE_CAN_REMOVE = {'P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P11', 'P11g', 'P12'}
LATE_CAN_ADD = {'P5', 'P7', 'P13', 'P14', 'P15'}


def late_props(X, Y):
    """Section 4 claims, comparing the on-time classification X with the LATE classification Y of the same rows."""
    out = {}
    for Z in ZONES:
        a, b = X['summaries'][Z], Y['summaries'][Z]
        out['Nv_never_lower_' + Z] = b['Nv'] >= a['Nv']
        out['M_never_lower_' + Z] = b['M'] >= a['M']
        out['H_unchanged_' + Z] = b['H'] == a['H']
        out['m_unchanged_' + Z] = b['m'] == a['m']
        out['missdom_never_removed_' + Z] = (not a['missdom']) or b['missdom']
        out['sign_class_same_or_withheld_' + Z] = (b['S'] == UND) if a['S'] == UND else (b['S'] in (a['S'], UND))
    out['Delta_out_unchanged'] = X['Delta_out'] == Y['Delta_out']
    out['OF_never_removed'] = (not X['OF']) or Y['OF']
    rem = {p for p in PATS if X['patterns'][p] and not Y['patterns'][p]}
    add = {p for p in PATS if Y['patterns'][p] and not X['patterns'][p]}
    out['removals_within_listed'] = rem <= LATE_CAN_REMOVE
    out['additions_within_listed'] = add <= LATE_CAN_ADD
    out['P10_never_changes'] = 'P10' not in rem | add
    out['P13_P14_P15_never_removed'] = not (rem & {'P13', 'P14', 'P15'})
    out['outer_signed_replaced_by_P14'] = (not (rem & {'P1', 'P2', 'P11'})) or Y['patterns']['P14']
    out['inner_signed_replaced_by_P15'] = (not (rem & {'P3', 'P4', 'P12'})) or Y['patterns']['P15']
    out['E3_moves_only_toward_tested_negative'] = X['E3'] == Y['E3'] or Y['E3'] == 0
    xr = {r['reading']: r['part1'] for r in X['readings']}
    yr = {r['reading']: r['part1'] for r in Y['readings']}
    out['deficit_type_never_gains_consistent'] = all(not (yr[n] == C_ and xr[n] != C_) for n in ('R-UT1', 'R-REACH'))
    hd_removed = [Z for Z in ZONES if X['summaries'][Z]['hitdom'] and not Y['summaries'][Z]['hitdom']]
    return out, rem, add, hd_removed


# ------------------------------------------------------------------------------------- enumerations: values and rows
def val(scheme, st, zone, pos):
    if scheme == 'V1_flat':
        return {'H': 0.0, 'P': 2.0, 'N': -2.0}[st]
    if scheme == 'V2_outward_growth':
        return {'H': 0.5 if pos % 2 == 0 else -0.5, 'P': 1.5 + 0.5 * pos, 'N': -(1.5 + 0.5 * pos)}[st]
    if scheme == 'V3_boundary_hits_outward_shrink':
        return {'H': 1.0 if pos % 2 == 0 else -1.0, 'P': 3.0 - 0.75 * pos, 'N': -(3.0 - 0.75 * pos)}[st]
    if scheme == 'V4_zone_offsets':
        off = {'INNER': 0.0, 'TRANSITION': 0.4, 'OUTER': -0.4}[zone]
        return {'H': (0.6 + off) if pos % 2 == 0 else (-0.6 + off), 'P': 1.2 + 0.9 * pos + max(off, 0), 'N': -(1.2 + 0.9 * pos) + min(off, 0)}[st]
    raise ValueError(scheme)


def rows_of(seq, zone, scheme, late_as_invalid=False):
    out = []
    for pos, st in enumerate(seq):
        fl = zone == 'TRANSITION' and pos == 0        # the first TRANSITION row plays Q25, the one flagged row
        if st in 'HPN':
            out.append((HIT if st == 'H' else MISS, val(scheme, st, zone, pos), fl))
        elif st == 'U':
            out.append((NULL, None, fl))
        elif st == 'X':
            out.append((INV, None, fl))
        elif st == 'L':
            out.append((INV if late_as_invalid else LATE, None, fl))
        else:
            raise ValueError(st)
    return out


def sequences(alphabet, lmin, lmax):
    return [''.join(t) for n in range(lmin, lmax + 1) for t in itertools.product(alphabet, repeat=n)]


def zone_features(seqs, zone, scheme, late_as_invalid=False):
    keys = ('Nv', 'H', 'M', 'U', 'I', 'cm', 'S', 'missdom', 'hitdom', 'hasdef', 'm', 'dout', 'farmed', 'p10')
    f = {k: [] for k in keys}
    for s in seqs:
        rows = rows_of(s, zone, scheme, late_as_invalid)
        zs = zone_summary(rows)
        for k in ('Nv', 'H', 'M', 'U', 'I', 'cm', 'S', 'missdom', 'hitdom', 'hasdef'):
            f[k].append(zs[k])
        f['m'].append(np.nan if zs['m'] is None else zs['m'])
        d, fm = outer_trend(rows)
        f['dout'].append(np.nan if d is None else d)
        f['farmed'].append(np.nan if fm is None else fm)
        f['p10'].append(any(fl and kind in (MISS, NULL) for kind, r, fl in rows))
    return {k: np.array(v) for k, v in f.items()}


def eval_block(Ii, T, O):
    """Vectorized section 2/3/5.3 rules for one INNER sequence Ii (dict of scalars) against all (T, O) sequence pairs."""
    nT, nO = len(T['Nv']), len(O['Nv'])

    def tt(a):
        return np.repeat(np.asarray(a)[:, None], nO, axis=1)

    def oo(a):
        return np.repeat(np.asarray(a)[None, :], nT, axis=0)

    def ss(v):
        return np.full((nT, nO), v)
    SI, ST, SO = ss(Ii['S']), tt(T['S']), oo(O['S'])
    ImD, TmD, OmD = ss(Ii['missdom']), tt(T['missdom']), oo(O['missdom'])
    IhD, ThD = ss(Ii['hitdom']), tt(T['hitdom'])
    with np.errstate(invalid='ignore'):
        mTgtO = tt(T['m']) > oo(O['m'])
        dneg = oo(O['dout'] < 0)
        farlt = oo(O['farmed'] < -1)
    GROW = (SO == DEF) & dneg & mTgtO
    CROSS = (SO == CEN) & dneg & mTgtO & farlt
    pat = {}
    pat['OF'] = OmD
    pat['P1'] = OmD & (SO == DEF)
    pat['P1g'] = pat['P1'] & GROW
    pat['P2'] = OmD & (SO == EXC)
    pat['P11'] = OmD & (SO == CEN)
    pat['P11g'] = pat['P11'] & CROSS
    pat['P14'] = OmD & (SO == UND)
    pat['P3'] = ImD & (SI == EXC)
    pat['P4'] = ImD & (SI == DEF)
    pat['P12'] = ImD & (SI == CEN)
    pat['P15'] = ImD & (SI == UND)
    pat['P13'] = TmD
    pat['P5'] = IhD & OmD & tt(T['Nv'] >= 1) & ~ThD
    pat['P6'] = (SI != UND) & (ST != UND) & (SO != UND) & (SI == ST) & (ST == SO) & (SO != CEN)
    Mtot = Ii['M'] + tt(T['M']) + oo(O['M'])
    anymiss = Mtot >= 1
    pat['P7'] = anymiss & ~(ImD | TmD | OmD)
    pat['P8'] = ((Ii['Nv'] + tt(T['Nv']) + oo(O['Nv'])) >= 1) & (Mtot == 0)
    pat['P9'] = oo(O['Nv'] == 0)
    pat['P10'] = tt(T['p10'])
    pat['P0'] = (Ii['I'] + tt(T['I']) + oo(O['I'])) > 0
    OF = pat['OF']
    E3 = np.where(OF, 0, np.where(oo(O['Nv'] >= 1), 1, 2))
    hasdefO = oo(O['hasdef'])
    c = [((SO == DEF) | (SO == CEN)) & hasdefO, pat['P2'], pat['P14'], pat['P11'] & ~hasdefO]
    nsum = c[0].astype(np.int8) + c[1] + c[2] + c[3]
    sign_code = np.where(nsum != 1, UNDEF, np.select(c, [C_, NA_EXC, NA_UNS, NA_NDM], UNDEF))
    cmz = {'O': oo(O['cm'] >= 1), 'I': ss(Ii['cm'] >= 1), 'T': tt(T['cm'] >= 1),
           'ALL': (Ii['cm'] + tt(T['cm']) + oo(O['cm'])) >= 1, 'FLAG': pat['P10']}
    part1, hascit = {}, {}
    for name, trig, sign, dt, prior in READINGS:
        th = np.zeros((nT, nO), bool)
        hc = np.zeros((nT, nO), bool)
        for t in trig:
            th |= pat[t]
            hc |= pat[t] & cmz[SCOPE_ZONE[t]]
        if name == 'R-DRIFT':
            part1[name] = np.where(OF, C_, NA_PNH)         # STAGE0 at writing: NOT_EVALUATED_BEFORE_FREEZE, no against
        elif sign == 'deficit-type':
            part1[name] = np.where(OF, sign_code, NA_PNH)
        else:
            part1[name] = np.where(th, C_, NA_PNH)
        hascit[name] = hc
    return {'pat': pat, 'E3': E3, 'part1': part1, 'hascit': hascit, 'anymiss': anymiss, 'GROW': GROW, 'CROSS': CROSS,
            'sign_nsum_under_OF_bad': OF & (nsum != 1)}


def concrete(si, ti, oi, seqs, scheme, late_as_invalid=False):
    return {'INNER': rows_of(seqs['INNER'][si], 'INNER', scheme, late_as_invalid),
            'TRANSITION': rows_of(seqs['TRANSITION'][ti], 'TRANSITION', scheme, late_as_invalid),
            'OUTER': rows_of(seqs['OUTER'][oi], 'OUTER', scheme, late_as_invalid)}


def compare_scalar(res, blk, t, o):
    bad = []
    for p in PATS:
        if bool(blk['pat'][p][t, o]) != bool(res['patterns'][p]):
            bad.append(p)
    if bool(blk['pat']['OF'][t, o]) != res['OF']:
        bad.append('OF')
    if int(blk['E3'][t, o]) != res['E3']:
        bad.append('E3')
    for r in res['readings']:
        if int(blk['part1'][r['reading']][t, o]) != r['part1']:
            bad.append('part1 ' + r['reading'])
    return bad


def seqstr(si, ti, oi, seqs):
    return {'INNER': seqs['INNER'][si], 'TRANSITION': seqs['TRANSITION'][ti], 'OUTER': seqs['OUTER'][oi]}


# -------------------------------------------------------------------------------------------- exhaustive enumerations
def exhaustive_main(scheme, lmin, lmax, rng, n_xval):
    """Every combination of HIT/MISS+/MISS-/MISS-unsigned(null ratio)/INVALID rows, lmin..lmax rows per zone."""
    alph = 'HPNUX'
    seqs = {Z: sequences(alph, lmin, lmax) for Z in ZONES}
    F = {Z: zone_features(seqs[Z], Z, scheme) for Z in ZONES}
    names = ['OF_iff_P1_P2_P11_P14', 'OF_exactly_one_of_four', 'coverage', 'tuples_defined', 'sign_rule_exactly_one_case_under_OF',
             'P5_iff_hitdomI_OF_P13', 'P6_implies_P1orP2_P3orP4_P13', 'A10_every_miss_two_ways', 'A15E3_five_readings_under_OF',
             'deficit_type_never_consistent_under_P2_P14', 'E3_tested_negative_iff_OF', 'P1g_only_with_P1']
    viol = {n: 0 for n in names}
    wit = {}
    metrics = {'CROSSING_without_P11': 0, 'GROWING_without_P1': 0}
    for r in RNAMES:
        metrics['CONSISTENT_without_citable_miss_' + r] = 0
    mwit = {}
    freq = {p: 0 for p in PATS + ('OF',)}
    e3freq = {0: 0, 1: 0, 2: 0}
    p1freq = {r: {} for r in RNAMES}
    n = 0
    nT, nO = len(seqs['TRANSITION']), len(seqs['OUTER'])
    xv_bad, xv_n, xv_wit = 0, 0, []
    xv_targets = {}
    for _ in range(n_xval):
        si = rng.randrange(len(seqs['INNER']))
        xv_targets.setdefault(si, []).append((rng.randrange(nT), rng.randrange(nO)))
    for si in range(len(seqs['INNER'])):
        Ii = {k: F['INNER'][k][si] for k in F['INNER']}
        b = eval_block(Ii, F['TRANSITION'], F['OUTER'])
        pat, p1 = b['pat'], b['part1']
        four = pat['P1'].astype(np.int8) + pat['P2'] + pat['P11'] + pat['P14']
        any_zone = pat['P1'] | pat['P2'] | pat['P11'] | pat['P14'] | pat['P3'] | pat['P4'] | pat['P12'] | pat['P15'] | pat['P13']
        chk = {
            'OF_iff_P1_P2_P11_P14': pat['OF'] == (four > 0),
            'OF_exactly_one_of_four': np.where(pat['OF'], four == 1, four == 0),
            'coverage': ~b['anymiss'] | any_zone | pat['P7'],
            'tuples_defined': np.logical_and.reduce([p1[r] != UNDEF for r in RNAMES]),
            'sign_rule_exactly_one_case_under_OF': ~b['sign_nsum_under_OF_bad'],
            'P5_iff_hitdomI_OF_P13': pat['P5'] == (bool(Ii['hitdom']) & pat['OF'] & pat['P13']),
            'P6_implies_P1orP2_P3orP4_P13': ~pat['P6'] | ((pat['P1'] | pat['P2']) & (pat['P3'] | pat['P4']) & pat['P13']),
            'A10_every_miss_two_ways': ~b['anymiss'] | ((p1['R-MF'] != NA_PNH) & ((p1['R-HIST'] != NA_PNH) | (p1['R-SPEC'] != NA_PNH))),
            'A15E3_five_readings_under_OF': ~pat['OF'] | np.logical_and.reduce([p1[r] != NA_PNH for r in ('R-MF', 'R-UT1', 'R-REACH', 'R-HIST', 'R-DRIFT')]),
            'deficit_type_never_consistent_under_P2_P14': ~((pat['P2'] | pat['P14']) & ((p1['R-UT1'] == C_) | (p1['R-REACH'] == C_))),
            'E3_tested_negative_iff_OF': (b['E3'] == 0) == pat['OF'],
            'P1g_only_with_P1': ~pat['P1g'] | pat['P1'],
        }
        for k, ok in chk.items():
            bad = ~ok
            nb = int(bad.sum())
            if nb:
                viol[k] += nb
                if k not in wit:
                    t, o = np.argwhere(bad)[0]
                    wit[k] = seqstr(si, int(t), int(o), seqs)
        mets = {'CROSSING_without_P11': b['CROSS'] & ~pat['P11'], 'GROWING_without_P1': b['GROW'] & ~pat['P1']}
        for r in RNAMES:
            mets['CONSISTENT_without_citable_miss_' + r] = (p1[r] == C_) & ~b['hascit'][r]
        for k, arr in mets.items():
            nb = int(arr.sum())
            if nb:
                metrics[k] += nb
                if k not in mwit:
                    t, o = np.argwhere(arr)[0]
                    mwit[k] = seqstr(si, int(t), int(o), seqs)
        for p in freq:
            freq[p] += int(pat[p].sum())
        for v in (0, 1, 2):
            e3freq[v] += int((b['E3'] == v).sum())
        for r in RNAMES:
            u, cnt = np.unique(p1[r], return_counts=True)
            for uu, cc in zip(u, cnt):
                p1freq[r][P1N[int(uu)]] = p1freq[r].get(P1N[int(uu)], 0) + int(cc)
        n += nT * nO
        for (t, o) in xv_targets.get(si, []):
            res = classify(concrete(si, t, o, seqs, scheme))
            bad = compare_scalar(res, b, t, o)
            xv_n += 1
            props = scalar_props(res)
            if bad or not all(props.values()):
                xv_bad += 1
                if len(xv_wit) < 5:
                    xv_wit.append({'seq': seqstr(si, t, o, seqs), 'mismatch': bad, 'failed_props': [k for k, v in props.items() if not v]})
    zone_formal = {}
    for Z in ZONES:
        f = F[Z]
        zone_formal[Z] = {'signed_class_without_missdom': int(((f['S'] == DEF) | (f['S'] == EXC)).__and__(~f['missdom']).sum()),
                          'not_exactly_one_domination_Nv_ge_1': int(((f['Nv'] >= 1) & (f['missdom'] == f['hitdom'])).sum()),
                          'domination_with_Nv_0': int(((f['Nv'] == 0) & (f['missdom'] | f['hitdom'])).sum())}
    return {'scheme': scheme, 'alphabet': alph, 'rows_per_zone': [lmin, lmax], 'n_sequences_per_zone': len(seqs['INNER']),
            'n_outcomes': n, 'violations': viol, 'violation_witnesses': wit, 'zone_level_formal_violations': zone_formal,
            'metrics': metrics, 'metric_witnesses': mwit, 'pattern_frequency': freq, 'E3_frequency': {E3N[k]: v for k, v in e3freq.items()},
            'part1_frequency': p1freq, 'scalar_cross_validation': {'n': xv_n, 'mismatched_or_failed': xv_bad, 'witnesses': xv_wit}}


def exhaustive_late(scheme, lmin, lmax, rng, n_xval):
    """Every combination of HIT/MISS+/MISS-/null-ratio/INVALID/LATE rows; each LATE row is compared with the same gate on
    time (the row INVALID). Checks the section 4 statements and counts every pattern change."""
    alph = 'HPNUXL'
    seqs = {Z: sequences(alph, lmin, lmax) for Z in ZONES}
    FY = {Z: zone_features(seqs[Z], Z, scheme, late_as_invalid=False) for Z in ZONES}
    FX = {Z: zone_features(seqs[Z], Z, scheme, late_as_invalid=True) for Z in ZONES}
    zone_viol = {}
    for Z in ZONES:
        x, y = FX[Z], FY[Z]
        same_m = (x['m'] == y['m']) | (np.isnan(x['m']) & np.isnan(y['m']))
        same_d = (x['dout'] == y['dout']) | (np.isnan(x['dout']) & np.isnan(y['dout']))
        zone_viol[Z] = {
            'Nv_lowered': int((y['Nv'] < x['Nv']).sum()), 'M_lowered': int((y['M'] < x['M']).sum()),
            'H_changed': int((y['H'] != x['H']).sum()), 'm_changed': int((~same_m).sum()),
            'Delta_out_changed': int((~same_d).sum()) if Z == 'OUTER' else 0,
            'missdom_removed': int((x['missdom'] & ~y['missdom']).sum()),
            'sign_class_created_or_switched': int(((x['S'] == UND) & (y['S'] != UND)).sum() + ((x['S'] != UND) & (y['S'] != UND) & (y['S'] != x['S'])).sum()),
            'hitdom_removed_witnessed': int((x['hitdom'] & ~y['hitdom']).sum())}
    rem_count = {p: 0 for p in PATS}
    add_count = {p: 0 for p in PATS}
    viol = {'removal_outside_listed': 0, 'addition_outside_listed': 0, 'P10_changed': 0, 'P13_P14_P15_removed': 0,
            'outer_signed_not_replaced_by_P14': 0, 'inner_signed_not_replaced_by_P15': 0, 'OF_removed': 0,
            'E3_moved_away_from_tested_negative': 0, 'deficit_type_gained_consistent': 0, 'tuples_undefined_late': 0,
            'coverage_late': 0, 'OF_equiv_late': 0}
    wit = {}
    e3_trans = {}
    ymet = {'CROSSING_without_P11': 0}
    for r in RNAMES:
        ymet['CONSISTENT_without_citable_miss_' + r] = 0
    ymwit = {}
    n = 0
    nT, nO = len(seqs['TRANSITION']), len(seqs['OUTER'])
    xv_targets = {}
    for _ in range(n_xval):
        si = rng.randrange(len(seqs['INNER']))
        xv_targets.setdefault(si, []).append((rng.randrange(nT), rng.randrange(nO)))
    xv_bad, xv_n, xv_wit = 0, 0, []
    for si in range(len(seqs['INNER'])):
        bx = eval_block({k: FX['INNER'][k][si] for k in FX['INNER']}, FX['TRANSITION'], FX['OUTER'])
        by = eval_block({k: FY['INNER'][k][si] for k in FY['INNER']}, FY['TRANSITION'], FY['OUTER'])
        px, py = bx['pat'], by['pat']
        rem_any_out = np.zeros((nT, nO), bool)
        add_any_out = np.zeros((nT, nO), bool)
        for p in PATS:
            rm = px[p] & ~py[p]
            ad = py[p] & ~px[p]
            rem_count[p] += int(rm.sum())
            add_count[p] += int(ad.sum())
            if p not in LATE_CAN_REMOVE:
                rem_any_out |= rm
            if p not in LATE_CAN_ADD:
                add_any_out |= ad
        four_y = py['P1'].astype(np.int8) + py['P2'] + py['P11'] + py['P14']
        any_zone_y = py['P1'] | py['P2'] | py['P11'] | py['P14'] | py['P3'] | py['P4'] | py['P12'] | py['P15'] | py['P13']
        bad = {
            'removal_outside_listed': rem_any_out,
            'addition_outside_listed': add_any_out,
            'P10_changed': px['P10'] != py['P10'],
            'P13_P14_P15_removed': (px['P13'] & ~py['P13']) | (px['P14'] & ~py['P14']) | (px['P15'] & ~py['P15']),
            'outer_signed_not_replaced_by_P14': ((px['P1'] & ~py['P1']) | (px['P2'] & ~py['P2']) | (px['P11'] & ~py['P11'])) & ~py['P14'],
            'inner_signed_not_replaced_by_P15': ((px['P3'] & ~py['P3']) | (px['P4'] & ~py['P4']) | (px['P12'] & ~py['P12'])) & ~py['P15'],
            'OF_removed': px['OF'] & ~py['OF'],
            'E3_moved_away_from_tested_negative': (bx['E3'] != by['E3']) & (by['E3'] != 0),
            'deficit_type_gained_consistent': ((by['part1']['R-UT1'] == C_) & (bx['part1']['R-UT1'] != C_)) | ((by['part1']['R-REACH'] == C_) & (bx['part1']['R-REACH'] != C_)),
            'tuples_undefined_late': ~np.logical_and.reduce([by['part1'][r] != UNDEF for r in RNAMES]),
            'coverage_late': by['anymiss'] & ~(any_zone_y | py['P7']),
            'OF_equiv_late': np.where(py['OF'], four_y != 1, four_y != 0),
        }
        for k, arr in bad.items():
            nb = int(arr.sum())
            if nb:
                viol[k] += nb
                if k not in wit:
                    t, o = np.argwhere(arr)[0]
                    wit[k] = seqstr(si, int(t), int(o), seqs)
        mets = {'CROSSING_without_P11': by['CROSS'] & ~py['P11']}
        for r in RNAMES:
            mets['CONSISTENT_without_citable_miss_' + r] = (by['part1'][r] == C_) & ~by['hascit'][r]
        for k, arr in mets.items():
            nb = int(arr.sum())
            if nb:
                ymet[k] += nb
                if k not in ymwit:
                    t, o = np.argwhere(arr)[0]
                    ymwit[k] = seqstr(si, int(t), int(o), seqs)
        for a in (0, 1, 2):
            for c in (0, 1, 2):
                cnt = int(((bx['E3'] == a) & (by['E3'] == c)).sum())
                if cnt:
                    key = '%s -> %s' % (E3N[a], E3N[c])
                    e3_trans[key] = e3_trans.get(key, 0) + cnt
        n += nT * nO
        for (t, o) in xv_targets.get(si, []):
            X = classify(concrete(si, t, o, seqs, scheme, late_as_invalid=True))
            Y = classify(concrete(si, t, o, seqs, scheme, late_as_invalid=False))
            mm = compare_scalar(X, bx, t, o) + ['late ' + q for q in compare_scalar(Y, by, t, o)]
            lp, _, _, _ = late_props(X, Y)
            xv_n += 1
            if mm or not all(lp.values()):
                xv_bad += 1
                if len(xv_wit) < 5:
                    xv_wit.append({'seq': seqstr(si, t, o, seqs), 'mismatch': mm, 'failed': [k for k, v in lp.items() if not v]})
    return {'scheme': scheme, 'alphabet': alph, 'rows_per_zone': [lmin, lmax], 'n_pairs': n, 'zone_level': zone_viol,
            'violations': viol, 'violation_witnesses': wit, 'removal_counts': rem_count, 'addition_counts': add_count,
            'E3_transitions': e3_trans, 'late_version_metrics': ymet, 'late_version_metric_witnesses': ymwit,
            'scalar_cross_validation': {'n': xv_n, 'mismatched_or_failed': xv_bad, 'witnesses': xv_wit}}


# --------------------------------------------------------------------------------------- random registered-size outcomes
SIZES = {'INNER': 24, 'TRANSITION': 11, 'OUTER': 8}
REGIMES = ('hit_heavy', 'deficit_heavy', 'excess_heavy', 'mixed', 'unsigned_heavy', 'invalid_heavy', 'late_heavy',
           'growing_deficit', 'crossing', 'half_half', 'boundary')


def rand_hit(rng):
    u = rng.random()
    if u < 0.1:
        return rng.choice((1.0, -1.0, 0.0))
    return rng.uniform(-1.0, 1.0)


def rand_miss(rng, sign):
    u = rng.random()
    if u < 0.1:
        return sign * rng.choice((2.0, 1.5, 3.0))
    return sign * (1.0 + 1e-9 + rng.expovariate(1.0))


def rand_zone(rng, zone, regime, with_late):
    n = SIZES[zone]
    rows = []
    for j in range(n):
        fl = zone == 'TRANSITION' and j == 0
        u = rng.random()
        if regime == 'growing_deficit' and zone == 'OUTER':
            r = -(1.05 + 0.5 * j + rng.uniform(0, 0.2))
            kind = MISS if u > 0.15 else rng.choice((HIT, NULL, INV, LATE if with_late else INV))
            rows.append((kind, r if kind == MISS else (rand_hit(rng) if kind == HIT else None), fl))
            continue
        if regime == 'crossing' and zone == 'OUTER':
            r = 2.2 - 0.62 * j + rng.uniform(-0.1, 0.1)
            if abs(r) <= 1:
                rows.append((HIT, max(-1.0, min(1.0, r)), fl))
            else:
                rows.append((MISS, r, fl))
            continue
        probs = {'hit_heavy': (0.8, 0.07, 0.07, 0.02, 0.02, 0.02), 'deficit_heavy': (0.2, 0.05, 0.6, 0.05, 0.05, 0.05),
                 'excess_heavy': (0.2, 0.6, 0.05, 0.05, 0.05, 0.05), 'mixed': (0.3, 0.3, 0.3, 0.04, 0.03, 0.03),
                 'unsigned_heavy': (0.25, 0.1, 0.1, 0.45, 0.05, 0.05), 'invalid_heavy': (0.3, 0.1, 0.1, 0.05, 0.45, 0.0),
                 'late_heavy': (0.3, 0.1, 0.1, 0.05, 0.05, 0.4), 'growing_deficit': (0.6, 0.1, 0.2, 0.05, 0.05, 0.0),
                 'crossing': (0.6, 0.15, 0.15, 0.05, 0.05, 0.0), 'half_half': (0.5, 0.25, 0.25, 0.0, 0.0, 0.0),
                 'boundary': (0.5, 0.2, 0.2, 0.05, 0.05, 0.0)}[regime]
        k = rng.choices(('H', 'P', 'N', 'U', 'X', 'L'), weights=probs)[0]
        if k == 'L' and not with_late:
            k = 'X'
        if k == 'H':
            rows.append((HIT, (rng.choice((1.0, -1.0)) if regime == 'boundary' else rand_hit(rng)), fl))
        elif k in 'PN':
            rows.append((MISS, rand_miss(rng, 1 if k == 'P' else -1), fl))
        elif k == 'U':
            rows.append((NULL, None, fl))
        elif k == 'X':
            rows.append((INV, None, fl))
        else:
            rows.append((LATE, None, fl))
    return rows


def late_to_invalid(z):
    return {Z: [(INV if k == LATE else k, r, fl) for k, r, fl in z[Z]] for Z in ZONES}


def random_tests(rng, n):
    agg = {}
    first_fail = {}
    late_agg = {}
    late_fail = {}
    rem_count = {p: 0 for p in PATS}
    add_count = {p: 0 for p in PATS}
    hitdom_removed = 0
    freq = {p: 0 for p in PATS + ('OF',)}
    met = {'CROSSING_without_P11': 0}
    for r in RNAMES:
        met['CONSISTENT_without_citable_miss_' + r] = 0
    met_wit = {}
    for i in range(n):
        reg = {Z: rng.choice(REGIMES) for Z in ZONES}
        z = {Z: rand_zone(rng, Z, reg[Z], with_late=True) for Z in ZONES}
        Y = classify(z)
        X = classify(late_to_invalid(z))
        for res, tag in ((Y, 'late'), (X, 'on_time')):
            for k, v in scalar_props(res).items():
                agg[k] = agg.get(k, 0) + (0 if v else 1)
                if not v and k not in first_fail:
                    first_fail[k] = {'which': tag, 'outcome': z}
        for p in PATS:
            freq[p] += Y['patterns'][p]
        freq['OF'] += Y['OF']
        for res, tag in ((Y, 'late'), (X, 'on_time')):
            ms = {'CROSSING_without_P11': res['CROSSING'] and not res['patterns']['P11']}
            for r in res['readings']:
                ms['CONSISTENT_without_citable_miss_' + r['reading']] = r['part1'] == C_ and not r['scope_has_citable_miss']
            for k, v in ms.items():
                if v:
                    met[k] += 1
                    if k not in met_wit:
                        met_wit[k] = {'which': tag, 'outcome': z}
        lp, rem, add, hdr = late_props(X, Y)
        for k, v in lp.items():
            late_agg[k] = late_agg.get(k, 0) + (0 if v else 1)
            if not v and k not in late_fail:
                late_fail[k] = {'outcome': z}
        for p in rem:
            rem_count[p] += 1
        for p in add:
            add_count[p] += 1
        hitdom_removed += bool(hdr)
    return {'n_outcomes': n, 'zone_sizes': SIZES, 'property_violations': agg, 'first_failures': first_fail,
            'late_violations': late_agg, 'late_first_failures': late_fail, 'late_removal_counts': rem_count,
            'late_addition_counts': add_count, 'hitdom_removed_count': hitdom_removed, 'pattern_frequency_late_version': freq,
            'metrics_both_versions': met, 'metric_first_witnesses': met_wit}


# ------------------------------------------------------------------------------- DT-S0G, STAGE0, gates, NOT_READ, labels
def dts0g(primary, twin):
    """6.3 comparison on OUTER rows non-INVALID under both members, with a defined r_q under both."""
    q = [j for j in range(len(primary)) if primary[j][0] in (HIT, MISS) and twin[j][0] in (HIT, MISS)]
    HP = sum(1 for j in q if primary[j][0] == HIT)
    HS = sum(1 for j in q if twin[j][0] == HIT)
    AP = med([abs(primary[j][1]) for j in q])
    AS = med([abs(twin[j][1]) for j in q])
    if HS > HP:
        return 'CONSISTENT', {'n': len(q), 'H_P': HP, 'H_S': HS, 'A_P': AP, 'A_S': AS}
    if HS <= HP and AP is not None and AS is not None and AS >= AP:
        return 'AGAINST', {'n': len(q), 'H_P': HP, 'H_S': HS, 'A_P': AP, 'A_S': AS}
    return 'NOT_DECIDED', {'n': len(q), 'H_P': HP, 'H_S': HS, 'A_P': AP, 'A_S': AS}


def stage0_status(receipts, step4_start, successor_pinned_in_seal, fallback_published_before_first_read, successor_refuses):
    """6.3 / M-14 receipt rule. receipts: {member: FINISHED receipt time or None}; times are ISO strings from date -u."""
    a = bool(receipts) and all(t is not None and t < step4_start for t in receipts.values())
    b = bool(successor_pinned_in_seal or fallback_published_before_first_read)
    if a and b:
        return ('EVALUATED_REFUSED', []) if successor_refuses else ('EVALUATED_BEFORE_FREEZE', [])
    reasons = ([] if a else ['RECEIPTS_AFTER_STEP4']) + ([] if b else ['NO_SEALED_SUCCESSOR'])
    return 'NOT_EVALUATED_BEFORE_FREEZE', reasons


def gate_status(gates, gate_list, first_launch_receipt):
    """4: ON-TIME iff the gate document's sha is pinned in a root entry stamped before the first step-5 launch receipt."""
    missing = [g for g in gates if g not in gate_list]
    if missing:
        return 'GATE_STATUS_LIST_DEFECT', missing
    return {g: ('ON-TIME' if gate_list[g] < first_launch_receipt else 'LATE') for g in gates}, []


STOP_CODES = ('UNEVALUATED_OR_REFUSED', 'REFERENCE_MEMBER_MISMATCH', 'FIELD_DEFECT', 'ID_ORDER_DEFECT', 'ENVELOPE_LABEL_PREFIX',
              'ZONE_TABLE_DIFFERS', 'TSR_FLAG_TABLE_MISMATCH', 'GATE_STATUS_LIST_DEFECT', 'SEAL_SHA_MISMATCH')
# ASSUMED dependency map (the text says only "each output whose own input is defective"): which outputs each stop touches
STOP_AFFECTS = {'UNEVALUATED_OR_REFUSED': {'ALL'}, 'REFERENCE_MEMBER_MISMATCH': {'ALL'}, 'ID_ORDER_DEFECT': {'ALL'},
                'ZONE_TABLE_DIFFERS': {'ALL'}, 'GATE_STATUS_LIST_DEFECT': {'ALL'}, 'ENVELOPE_LABEL_PREFIX': {'NEAR'},
                'TSR_FLAG_TABLE_MISMATCH': {'P10', 'R-TSR', 'TSR_FLAG_COLUMN'}, 'SEAL_SHA_MISMATCH': {'ALL'}}


def post_target(pre_stops, rerun_stops, field_map=None, field_defect_outputs=frozenset({'SENSITIVITY_COLUMN'}),
                declare_not_read=False):
    """1.1: stops checked before target access; after it, only a key-renaming field map or a NOT_READ that a re-run stop
    licenses."""
    if pre_stops:
        return {'result': 'CLASSIFICATION_INPUT_DEFECT', 'codes': sorted(pre_stops), 'when': 'before target access'}
    cleared = set()
    if field_map is not None:
        if not field_map.get('renames_keys_only'):
            return {'result': 'REFUSED_ACT', 'why': 'a field map may rename keys only, never change a value'}
        cleared = set(field_map.get('clears', ())) & set(rerun_stops)
    remaining = set(rerun_stops) - cleared
    if not remaining:
        if declare_not_read:
            return {'result': 'REFUSED_ACT', 'why': 'NOT_READ needs a stop that fires on the re-run (any cleared stop must be '
                    'cleared by the map)', 'applied_field_map': bool(cleared)}
        return {'result': 'READ', 'applied_field_map': bool(cleared)}
    affected = set()
    for s in remaining:
        affected |= (field_defect_outputs if s == 'FIELD_DEFECT' else STOP_AFFECTS[s])
    e3 = 'NOT_AVAILABLE (%s)' % ','.join(sorted(remaining)) if 'ALL' in affected or 'E3' in affected else 'printed with its value'
    return {'result': 'NOT_READ', 'codes': sorted(remaining), 'outputs_not_available': sorted(affected),
            'other_outputs': 'computed and published, labelled NOT_READ', 'E3_line': e3, 'applied_field_map': bool(cleared)}


def provisional_labels(freeze_status, gate_open_at_launch):
    labs = []
    if freeze_status == 'FREEZE_INCOMPLETE':
        labs.append('PROVISIONAL (FREEZE_INCOMPLETE)')
    if not gate_open_at_launch:
        labs.append('PROVISIONAL (N_GATE_NOT_OPEN)')
    return labs


# --------------------------------------------------------------------------------------------------------- named cases
def zone_rows(zone, spec):
    rows = []
    for kind, r, cnt in spec:
        rows += [[kind, r, False] for _ in range(cnt)]
    if zone == 'TRANSITION' and rows:
        rows[0][2] = True
    return [tuple(x) for x in rows]


def outcome(inner, trans, outer):
    z = {'INNER': zone_rows('INNER', inner), 'TRANSITION': zone_rows('TRANSITION', trans), 'OUTER': zone_rows('OUTER', outer)}
    for Zn in ZONES:
        assert len(z[Zn]) == SIZES[Zn], (Zn, len(z[Zn]))
    return z


INNER_BASE = [(INV, None, 2), (HIT, 0.2, 22)]          # Q01, Q02 built-in INVALID (QUERY_INSIDE_INNERMOST_NODE)
TRANS_HIT = [(HIT, 0.2, 11)]
OUTER_HIT = [(HIT, 0.2, 8)]
NA = NA_PNH
ALL_NA = {r: NA for r in RNAMES}


def P1(**kw):
    d = dict(ALL_NA)
    d.update({k.replace('_', '-'): v for k, v in kw.items()})
    return d


def one(vals):
    return [(MISS if abs(v) > 1 else HIT, v, 1) for v in vals]


NAMED = [
    # id, description, outcome, expectation {patterns, OF, E3, S (zone->code), part1}
    ('U1', 'OUTER all undefined-sign (8 null-ratio MISS rows); other zones HIT', outcome(INNER_BASE, TRANS_HIT, [(NULL, None, 8)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0, 'S': {'OUTER': UND},
      'part1': P1(R_MF=C_, R_UT1=NA_UNS, R_REACH=NA_UNS, R_HIST=C_, R_DRIFT=C_, R_NAX=C_)}),
    ('U1L_all_late_outer', 'M-15 (1): every non-INVALID OUTER row is a LATE-gate row', outcome(INNER_BASE, TRANS_HIT, [(LATE, None, 8)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0, 'S': {'OUTER': UND},
      'part1': P1(R_MF=C_, R_UT1=NA_UNS, R_REACH=NA_UNS, R_HIST=C_, R_DRIFT=C_, R_NAX=C_)}),
    ('U1L_on_time_pair', 'the same OUTER gate on time: every OUTER row INVALID', outcome(INNER_BASE, TRANS_HIT, [(INV, None, 8)]),
     {'patterns': ['P0', 'P8', 'P9'], 'OF': False, 'E3': 2, 'part1': dict(ALL_NA)}),
    ('U2', 'INNER all undefined-sign (22 null-ratio rows, 2 built-in INVALID)', outcome([(INV, None, 2), (NULL, None, 22)], TRANS_HIT, OUTER_HIT),
     {'patterns': ['P0', 'P15'], 'OF': False, 'E3': 1, 'S': {'INNER': UND},
      'part1': P1(R_MF=C_, R_NAX=C_, R_GEFF=C_, R_ML=C_, R_SPEC=C_, R_GEO=C_)}),
    ('U3_control', 'OUTER 5 null-ratio MISS + 3 HIT: the sign class is withheld (M - U < N_v/2), never taken from the hits',
     outcome(INNER_BASE, TRANS_HIT, [(NULL, None, 5), (HIT, 0.2, 3)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0, 'S': {'OUTER': UND}}),
    ('L1', '12 producer-INVALID INNER gate rows registered on time', outcome([(INV, None, 14), (HIT, 0.2, 10)], [(HIT, 0.2, 5), (MISS, 1.5, 6)], [(MISS, -3.0, 8)]),
     {'patterns': ['P0', 'P1', 'P13', 'P5'], 'OF': True, 'E3': 0, 'S': {'INNER': CEN, 'TRANSITION': EXC, 'OUTER': DEF}}),
    ('L2', 'the same 12 INNER gate rows LATE (unsigned MISS rows)', outcome([(INV, None, 2), (LATE, None, 12), (HIT, 0.2, 10)], [(HIT, 0.2, 5), (MISS, 1.5, 6)], [(MISS, -3.0, 8)]),
     {'patterns': ['P0', 'P1', 'P13', 'P15'], 'OF': True, 'E3': 0, 'S': {'INNER': UND}}),
    ('L3', '3 OUTER gate rows on time', outcome(INNER_BASE, TRANS_HIT, [(HIT, 0.2, 5), (INV, None, 3)]),
     {'patterns': ['P0', 'P8'], 'OF': False, 'E3': 1, 'part1': dict(ALL_NA)}),
    ('L4', 'the same 3 OUTER gate rows LATE', outcome(INNER_BASE, TRANS_HIT, [(HIT, 0.2, 5), (LATE, None, 3)]),
     {'patterns': ['P0', 'P7'], 'OF': False, 'E3': 1, 'part1': P1(R_MF=C_, R_HIST=C_, R_NAX=C_)}),
    ('CX2_0490_W1', 'Codex2 0490 witness: eight OUTER null-ratio rows, every other row HIT', outcome([(HIT, 0.2, 24)], TRANS_HIT, [(NULL, None, 8)]),
     {'patterns': ['P14'], 'OF': True, 'E3': 0}),
    ('CX2_0490_W1_inner', 'Codex2 0490: the analogous INNER-only case', outcome([(NULL, None, 24)], TRANS_HIT, OUTER_HIT),
     {'patterns': ['P15'], 'OF': False, 'E3': 1}),
    ('CX2_0490_W2_on_time', 'Codex2 0490 second witness, gate on time: 3 deficit MISS + 5 gate rows INVALID', outcome(INNER_BASE, TRANS_HIT, [(MISS, -2.0, 3), (INV, None, 5)]),
     {'patterns': ['P0', 'P1'], 'OF': True, 'E3': 0, 'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_)}),
    ('CX2_0490_W2_late', 'the same 5 gate rows LATE: P1 is replaced by P14 and the E3 line stays TESTED-NEGATIVE', outcome(INNER_BASE, TRANS_HIT, [(MISS, -2.0, 3), (LATE, None, 5)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0, 'part1': P1(R_MF=C_, R_UT1=NA_UNS, R_REACH=NA_UNS, R_HIST=C_, R_DRIFT=C_, R_NAX=C_)}),
    ('P1_outer_deficit', 'OUTER 8 deficit MISS rows', outcome(INNER_BASE, TRANS_HIT, [(MISS, -2.0, 8)]),
     {'patterns': ['P0', 'P1'], 'OF': True, 'E3': 0, 'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_)}),
    ('P1g_growing', 'OUTER deficit growing outward', outcome(INNER_BASE, TRANS_HIT, one([-1.2, -1.5, -1.8, -2.1, -2.4, -2.7, -3.0, -3.3])),
     {'patterns': ['P0', 'P1', 'P1g'], 'OF': True, 'E3': 0}),
    ('P2_outer_excess', 'OUTER 8 excess MISS rows: the E3 readings are present, the deficit-type ones coded', outcome(INNER_BASE, TRANS_HIT, [(MISS, 2.0, 8)]),
     {'patterns': ['P0', 'P2'], 'OF': True, 'E3': 0,
      'part1': P1(R_MF=C_, R_UT1=NA_EXC, R_REACH=NA_EXC, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_)}),
    ('P11_crossing', 'E2-shaped crossing: excess near 30 kpc, deficit near 44 kpc', outcome(INNER_BASE, TRANS_HIT, one([2.0, 1.8, 1.5, 1.2, -1.2, -1.5, -2.0, -2.5])),
     {'patterns': ['P0', 'P11', 'P11g'], 'OF': True, 'E3': 0, 'S': {'OUTER': CEN},
      'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('P11_alternating', 'OUTER alternating excess and deficit misses', outcome(INNER_BASE, TRANS_HIT, one([2.0, -2.0] * 4)),
     {'patterns': ['P0', 'P11'], 'OF': True, 'E3': 0,
      'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('P11_no_deficit_miss', 'OUTER centred (m exactly 1) with only excess misses', outcome(INNER_BASE, TRANS_HIT, [(MISS, 2.0, 4), (HIT, 0.0, 4)]),
     {'patterns': ['P0', 'P11'], 'OF': True, 'E3': 0, 'S': {'OUTER': CEN},
      'part1': P1(R_MF=C_, R_UT1=NA_NDM, R_REACH=NA_NDM, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('P5_excess_outer', 'P5 with an excess OUTER', outcome(INNER_BASE, [(HIT, 0.2, 5), (MISS, 1.5, 6)], [(MISS, 2.0, 8)]),
     {'patterns': ['P0', 'P13', 'P2', 'P5'], 'OF': True, 'E3': 0,
      'part1': P1(R_MF=C_, R_UT1=NA_EXC, R_REACH=NA_EXC, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('P5_centered_outer', 'P5 with a centred (mixed) OUTER', outcome(INNER_BASE, [(HIT, 0.2, 5), (MISS, 1.5, 6)], one([2.0, -2.0] * 4)),
     {'patterns': ['P0', 'P11', 'P13', 'P5'], 'OF': True, 'E3': 0,
      'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('P5_unsigned_outer', 'P5 with an unsigned OUTER', outcome(INNER_BASE, [(HIT, 0.2, 5), (MISS, 1.5, 6)], [(NULL, None, 8)]),
     {'patterns': ['P0', 'P13', 'P14', 'P5'], 'OF': True, 'E3': 0}),
    ('P6_global_excess', 'every zone excess', outcome([(INV, None, 2), (MISS, 2.0, 22)], [(MISS, 2.0, 11)], [(MISS, 2.0, 8)]),
     {'patterns': ['P0', 'P10', 'P13', 'P2', 'P3', 'P6'], 'OF': True, 'E3': 0,
      'part1': P1(R_MF=C_, R_UT1=NA_EXC, R_REACH=NA_EXC, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_, R_GEFF=C_, R_ML=C_,
                  R_SPEC=C_, R_GEO=C_, R_TSR=C_)}),
    ('transition_only', 'only TRANSITION fails (Q25 a MISS)', outcome(INNER_BASE, [(MISS, -2.0, 11)], OUTER_HIT),
     {'patterns': ['P0', 'P10', 'P13'], 'OF': False, 'E3': 1, 'part1': P1(R_MF=C_, R_HIST=C_, R_NAX=C_, R_TSR=C_)}),
    ('scattered', 'misses in every zone, none miss-dominated', outcome([(INV, None, 2), (HIT, 0.2, 19), (MISS, 2.0, 3)], [(HIT, 0.2, 9), (MISS, -2.0, 2)], [(HIT, 0.2, 6), (MISS, -2.0, 2)]),
     {'patterns': ['P0', 'P7'], 'OF': False, 'E3': 1, 'part1': P1(R_MF=C_, R_HIST=C_, R_NAX=C_)}),
    ('all_hit', 'every row HIT, none INVALID', outcome([(HIT, 0.2, 24)], TRANS_HIT, OUTER_HIT),
     {'patterns': ['P8'], 'OF': False, 'E3': 1, 'part1': dict(ALL_NA)}),
    ('P8_P0_P9', 'P8 together with P0 and P9', outcome(INNER_BASE, TRANS_HIT, [(INV, None, 8)]),
     {'patterns': ['P0', 'P8', 'P9'], 'OF': False, 'E3': 2, 'part1': dict(ALL_NA)}),
    ('E_tie', 'exact half: 4 misses of 8 valid OUTER rows read miss-dominated', outcome(INNER_BASE, TRANS_HIT, [(MISS, -2.0, 4), (HIT, 0.2, 4)]),
     {'patterns': ['P0', 'P11'], 'OF': True, 'E3': 0, 'S': {'OUTER': CEN}, 'part1': P1(R_MF=C_, R_UT1=C_, R_REACH=C_, R_HIST=C_, R_DRIFT=C_, R_S1=C_, R_GRID=C_, R_NAX=C_)}),
    ('E_one', 'N_v(OUTER) = 1: one valid OUTER row, a MISS', outcome(INNER_BASE, TRANS_HIT, [(INV, None, 7), (MISS, -2.0, 1)]),
     {'patterns': ['P0', 'P1'], 'OF': True, 'E3': 0}),
    ('E_hit_majority', 'OUTER 5 HIT + 3 MISS', outcome(INNER_BASE, TRANS_HIT, [(HIT, 0.2, 5), (MISS, -2.0, 3)]),
     {'patterns': ['P0', 'P7'], 'OF': False, 'E3': 1}),
    ('P10G', 'Q25 a MISS with a frozen prediction', outcome(INNER_BASE, [(MISS, 2.0, 1), (HIT, 0.2, 10)], OUTER_HIT),
     {'patterns': ['P0', 'P10', 'P7'], 'OF': False, 'E3': 1, 'part1': P1(R_MF=C_, R_HIST=C_, R_NAX=C_, R_TSR=C_)}),
    ('P10L', 'Q25 a LATE-gate row: no P10', outcome(INNER_BASE, [(LATE, None, 1), (HIT, 0.2, 10)], OUTER_HIT),
     {'patterns': ['P0', 'P7'], 'OF': False, 'E3': 1, 'part1': P1(R_MF=C_, R_HIST=C_, R_NAX=C_)}),
    ('P10N', 'Q25 a null-ratio MISS (it has a frozen prediction)', outcome(INNER_BASE, [(NULL, None, 1), (HIT, 0.2, 10)], OUTER_HIT),
     {'patterns': ['P0', 'P10', 'P7'], 'OF': False, 'E3': 1}),
    ('CROSSING_without_OUTER_FAILURE', 'CROSSING holds (S(OUTER) CENTERED, Delta_out < 0, far half < -1) but OUTER is not miss-dominated: P11 and so P11g do not hold',
     outcome(INNER_BASE, TRANS_HIT, one([0.0] * 5 + [-2.0] * 3)),
     {'patterns': ['P0', 'P7'], 'OF': False, 'E3': 1, 'S': {'OUTER': CEN}}),
    ('late_P1g_on_time', 'growing OUTER deficit, 5 gate rows on time', outcome(INNER_BASE, TRANS_HIT, one([-1.2, -1.6, -2.0]) + [(INV, None, 5)]),
     {'patterns': ['P0', 'P1', 'P1g'], 'OF': True, 'E3': 0}),
    ('late_P1g_late', 'the same 5 gate rows LATE: P1 and P1g are replaced by P14', outcome(INNER_BASE, TRANS_HIT, one([-1.2, -1.6, -2.0]) + [(LATE, None, 5)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0}),
    ('late_P11g_on_time', 'OUTER crossing on two valid rows, 6 gate rows on time', outcome(INNER_BASE, TRANS_HIT, one([2.0, -2.0]) + [(INV, None, 6)]),
     {'patterns': ['P0', 'P11', 'P11g'], 'OF': True, 'E3': 0}),
    ('late_P11g_late', 'the same 6 gate rows LATE', outcome(INNER_BASE, TRANS_HIT, one([2.0, -2.0]) + [(LATE, None, 6)]),
     {'patterns': ['P0', 'P14'], 'OF': True, 'E3': 0}),
    ('late_P0_P9_removed_on_time', 'every INVALID row is an OUTER gate row, on time', outcome([(HIT, 0.2, 24)], TRANS_HIT, [(INV, None, 8)]),
     {'patterns': ['P0', 'P8', 'P9'], 'OF': False, 'E3': 2}),
    ('late_P0_P9_removed_late', 'the same gate LATE: P0, P8 and P9 go, P14 comes', outcome([(HIT, 0.2, 24)], TRANS_HIT, [(LATE, None, 8)]),
     {'patterns': ['P14'], 'OF': True, 'E3': 0}),
    ('late_P13_P5_added_on_time', 'TRANSITION 5 HIT + 4 MISS + 2 gate rows on time; OUTER failing', outcome(INNER_BASE, [(HIT, 0.2, 5), (MISS, 2.0, 4), (INV, None, 2)], [(MISS, -2.0, 8)]),
     {'patterns': ['P0', 'P1'], 'OF': True, 'E3': 0}),
    ('late_P13_P5_added_late', 'TRANSITION 5 HIT + 4 MISS + 2 LATE', outcome(INNER_BASE, [(HIT, 0.2, 5), (MISS, 2.0, 4), (LATE, None, 2)], [(MISS, -2.0, 8)]),
     {'patterns': ['P0', 'P1', 'P13', 'P5'], 'OF': True, 'E3': 0}),
]


def check_named(name, desc, z, exp):
    res = classify(z)
    got = {'patterns': held(res), 'OF': res['OF'], 'E3': res['E3'], 'S': {Zn: res['summaries'][Zn]['S'] for Zn in ZONES},
           'part1': {r['reading']: r['part1'] for r in res['readings']}}
    probs = []
    if sorted(exp['patterns']) != got['patterns']:
        probs.append('patterns %s, expected %s' % (got['patterns'], sorted(exp['patterns'])))
    for k in ('OF', 'E3'):
        if k in exp and exp[k] != got[k]:
            probs.append('%s %r, expected %r' % (k, got[k], exp[k]))
    for Zn, s in exp.get('S', {}).items():
        if got['S'][Zn] != s:
            probs.append('S(%s) %s, expected %s' % (Zn, SNAME[got['S'][Zn]], SNAME[s]))
    for r, c in exp.get('part1', {}).items():
        if got['part1'][r] != c:
            probs.append('%s part 1 %s, expected %s' % (r, P1N[got['part1'][r]], P1N[c]))
    props = scalar_props(res)
    failed = [k for k, v in props.items() if not v]
    tuples = [{'reading': r['reading'], 'part1': P1N[r['part1']], 'part2': r['part2'], 'part3': r['part3'],
               'triggers_holding': r['triggers_holding'], 'scope_rows': r['scope_rows'],
               'scope_has_citable_miss': r['scope_has_citable_miss']} for r in res['readings']]
    return {'id': name, 'description': desc, 'ok': not probs and not failed, 'problems': probs, 'failed_properties': failed,
            'patterns': got['patterns'], 'OUTER_FAILURE': res['OF'], 'GROWING': res['GROWING'], 'CROSSING': res['CROSSING'],
            'E3_line': E3N[res['E3']], 'E3_counts': res['E3_counts'],
            'sign_classes': {Zn: SNAME[got['S'][Zn]] for Zn in ZONES},
            'zone_counts': {Zn: {k: res['summaries'][Zn][k] for k in ('Nv', 'H', 'M', 'U', 'I', 'm')} for Zn in ZONES},
            'readings': tuples}


LATE_PAIRS = (('U1L_on_time_pair', 'U1L_all_late_outer'), ('L1', 'L2'), ('L3', 'L4'), ('CX2_0490_W2_on_time', 'CX2_0490_W2_late'),
              ('late_P1g_on_time', 'late_P1g_late'), ('late_P11g_on_time', 'late_P11g_late'),
              ('late_P0_P9_removed_on_time', 'late_P0_P9_removed_late'), ('late_P13_P5_added_on_time', 'late_P13_P5_added_late'))


def named_late_pairs():
    byid = {n[0]: n for n in NAMED}
    out = []
    for a, b in LATE_PAIRS:
        X, Y = classify(byid[a][2]), classify(byid[b][2])
        ok_pair = all(len(byid[a][2][Zn]) == len(byid[b][2][Zn]) for Zn in ZONES) and all(
            ra == rb or (ra[0] == INV and rb[0] == LATE and ra[2] == rb[2])
            for Zn in ZONES for ra, rb in zip(byid[a][2][Zn], byid[b][2][Zn]))
        lp, rem, add, hdr = late_props(X, Y)
        out.append({'on_time': a, 'late': b, 'rows_differ_only_by_gate_timing': ok_pair, 'removed': sorted(rem), 'added': sorted(add),
                    'E3': [E3N[X['E3']], E3N[Y['E3']]], 'hitdom_removed_in': hdr, 'failed': [k for k, v in lp.items() if not v],
                    'ok': ok_pair and all(lp.values())})
    return out


def other_rule_cases():
    out = []

    def add(cid, desc, got, exp):
        out.append({'id': cid, 'description': desc, 'got': got, 'expected': exp, 'ok': got == exp})
    # DT-S0G comparison (6.3; M-9)
    P8m = [(MISS, -2.0, False)] * 8
    add('S0G_twin_gains_one_hit', 'H_S > H_P', dts0g(P8m, [(HIT, 0.5, False)] + [(MISS, -2.0, False)] * 7)[0], 'CONSISTENT')
    add('S0G_shrinks_4x_no_hit', 'every residual 4 times smaller, no hit gained (M-9 recorded consequence)',
        dts0g([(MISS, -8.0, False)] * 8, [(MISS, -2.0, False)] * 8)[0], 'NOT_DECIDED')
    add('S0G_larger_residuals', 'same hits, larger residuals', dts0g(P8m, [(MISS, -3.0, False)] * 8)[0], 'AGAINST')
    add('S0G_equal', 'H_S = H_P and A_S = A_P reads AGAINST (>=)', dts0g(P8m, P8m)[0], 'AGAINST')
    add('S0G_no_row_qualifies', 'no OUTER row valid with a defined ratio under both', dts0g(P8m, [(INV, None, False)] * 8)[0], 'NOT_DECIDED')
    add('S0G_late_rows_excluded', 'LATE and null-ratio rows never qualify', dts0g([(LATE, None, False)] * 4 + [(NULL, None, False)] * 4,
                                                                                  [(HIT, 0.1, False)] * 8)[0], 'NOT_DECIDED')
    # R-DRIFT mapping under OUTER_FAILURE (closed table of 6.3)
    for code, p1, p2 in (('CONSISTENT', C_, 'CONSISTENT (DT-S0G)'), ('AGAINST', INC, 'AGAINST (DT-S0G)'), ('NOT_DECIDED', C_, 'OPEN (NOT_DECIDED)'),
                         ('TWIN_INVALID', C_, 'OPEN (TWIN_INVALID)'), ('TWIN_INPUT_DEFECT', C_, 'OPEN (TWIN_INPUT_DEFECT)'),
                         ('NOT_EVALUATED_BEFORE_FREEZE', C_, 'OPEN (NOT_EVALUATED_BEFORE_FREEZE)'), ('EVALUATED_REFUSED', C_, 'OPEN (EVALUATED_REFUSED)')):
        add('RDRIFT_OF_' + code, 'R-DRIFT tuple under OUTER_FAILURE', [P1N[drift_part1(True, code, 'S63')], drift_part2(code)], [P1N[p1], p2])
        add('RDRIFT_noOF_' + code, 'R-DRIFT part 1 without OUTER_FAILURE (6.3: PATTERN_NOT_HELD)', P1N[drift_part1(False, code, 'S63')], P1N[NA_PNH])
    # STAGE0 receipt rule (6.3 = M-14)
    rec = {'m1': '2026-10-19T01:00:00Z', 'm2': '2026-10-19T01:10:00Z'}
    s4 = '2026-10-19T02:00:00Z'
    add('STAGE0_evaluated', 'FINISHED receipts before step 4; successor pinned in the seal entry',
        list(stage0_status(rec, s4, True, False, False)), ['EVALUATED_BEFORE_FREEZE', []])
    add('STAGE0_receipt_at_step4', 'a receipt stamped at the step-4 start is not before it',
        list(stage0_status({'m1': rec['m1'], 'm2': s4}, s4, True, False, False)), ['NOT_EVALUATED_BEFORE_FREEZE', ['RECEIPTS_AFTER_STEP4']])
    add('STAGE0_missing_receipt', 'a member with no FINISHED receipt', list(stage0_status({'m1': rec['m1'], 'm2': None}, s4, True, False, False)),
        ['NOT_EVALUATED_BEFORE_FREEZE', ['RECEIPTS_AFTER_STEP4']])
    add('STAGE0_no_successor', 'no successor pinned and none published before the first read',
        list(stage0_status(rec, s4, False, False, False)), ['NOT_EVALUATED_BEFORE_FREEZE', ['NO_SEALED_SUCCESSOR']])
    add('STAGE0_fallback_successor', 'under the Status fallback, a successor sha published before the first read',
        list(stage0_status(rec, s4, False, True, False)), ['EVALUATED_BEFORE_FREEZE', []])
    add('STAGE0_refused', 'the pinned successor refuses a STAGE0 record', list(stage0_status(rec, s4, True, False, True)), ['EVALUATED_REFUSED', []])
    add('STAGE0_both_fail', 'both (a) and (b) fail: this suite prints both reasons (the text names one reason per failed condition)',
        list(stage0_status({'m1': None}, s4, False, False, False)), ['NOT_EVALUATED_BEFORE_FREEZE', ['RECEIPTS_AFTER_STEP4', 'NO_SEALED_SUCCESSOR']])
    # gate timing (4; M-15)
    gl = {'g_early': '2026-10-19T03:00:00Z', 'g_equal': '2026-10-19T04:00:00Z', 'g_after': '2026-10-19T05:00:00Z'}
    st, miss = gate_status(['g_early', 'g_equal', 'g_after'], gl, '2026-10-19T04:00:00Z')
    add('GATE_timing', 'pinned before the first launch receipt: ON-TIME; at or after it: LATE', [st, miss],
        [{'g_early': 'ON-TIME', 'g_equal': 'LATE', 'g_after': 'LATE'}, []])
    add('GATE_missing_from_list', 'a root-listed gate missing from the gate-status list', list(gate_status(['g_early', 'g_new'], gl, '2026-10-19T04:00:00Z')),
        ['GATE_STATUS_LIST_DEFECT', ['g_new']])
    # post-target acts (1.1)
    add('NR_pre_target_stop', 'a stop before target access', post_target({'TSR_FLAG_TABLE_MISMATCH'}, set())['result'], 'CLASSIFICATION_INPUT_DEFECT')
    add('NR_no_stop_refused', 'NOT_READ declared with no stop firing on the re-run', post_target(set(), set(), declare_not_read=True)['result'], 'REFUSED_ACT')
    r = post_target(set(), {'FIELD_DEFECT'})
    add('NR_field_defect', 'a re-run stop fires (a sensitivity field missing): NOT_READ; the E3 line is printed with its value',
        [r['result'], r['E3_line'], r['outputs_not_available']], ['NOT_READ', 'printed with its value', ['SENSITIVITY_COLUMN']])
    r = post_target(set(), {'FIELD_DEFECT'}, field_map={'renames_keys_only': True, 'clears': {'FIELD_DEFECT'}}, declare_not_read=True)
    add('NR_map_clears_stop', 'a key-renaming map clears the stop: root must apply it, and NOT_READ is not available', [r['result'], r['applied_field_map']],
        ['REFUSED_ACT', True])
    r = post_target(set(), {'FIELD_DEFECT'}, field_map={'renames_keys_only': True, 'clears': {'FIELD_DEFECT'}})
    add('NR_map_applied_read', 'the same map applied: the classification is read', [r['result'], r['applied_field_map']], ['READ', True])
    add('NR_map_changes_value', 'a field map that changes a value', post_target(set(), {'FIELD_DEFECT'}, field_map={'renames_keys_only': False})['result'], 'REFUSED_ACT')
    r = post_target(set(), {'REFERENCE_MEMBER_MISMATCH'})
    add('NR_E3_input_defective', 'a stop on an E3 input: the E3 line is printed NOT_AVAILABLE with the code', [r['result'], r['E3_line']],
        ['NOT_READ', 'NOT_AVAILABLE (REFERENCE_MEMBER_MISMATCH)'])
    r = post_target(set(), {'TSR_FLAG_TABLE_MISMATCH'})
    add('NR_tsr_only', 'a TSR flag-table stop on the re-run: P10, R-TSR and the flag column NOT_AVAILABLE; E3 printed', [r['result'], r['E3_line'], r['outputs_not_available']],
        ['NOT_READ', 'printed with its value', ['P10', 'R-TSR', 'TSR_FLAG_COLUMN']])
    # PROVISIONAL labels (I-6, I-7)
    add('PROVISIONAL_both', 'FREEZE_INCOMPLETE and a gate not OPEN at launch', provisional_labels('FREEZE_INCOMPLETE', False),
        ['PROVISIONAL (FREEZE_INCOMPLETE)', 'PROVISIONAL (N_GATE_NOT_OPEN)'])
    add('PROVISIONAL_none', 'FREEZE_COMPLETE and the gate OPEN', provisional_labels('FREEZE_COMPLETE', True), [])
    return out


def drift_conflict_case():
    """R-DRIFT when DT-S0G reads AGAINST and OUTER_FAILURE does not hold: 3 says against takes precedence (INCONSISTENT);
    the closed mapping of 6.3 says part 1 is NOT_ADDRESSED (PATTERN_NOT_HELD) without OUTER_FAILURE."""
    z = outcome(INNER_BASE, TRANS_HIT, OUTER_HIT)
    prim = z['OUTER']
    twin = [(HIT, 0.5, False)] * 8
    cmp_ = dts0g(prim, twin)
    a = classify(z, stage0=cmp_[0], drift_rule='S63')
    b = classify(z, stage0=cmp_[0], drift_rule='S3_literal')
    pa = [r for r in a['readings'] if r['reading'] == 'R-DRIFT'][0]
    pb = [r for r in b['readings'] if r['reading'] == 'R-DRIFT'][0]
    return {'outcome': 'PRIMARY OUTER 8 HIT at r = 0.2; STAGE0 twin 8 HIT at r = 0.5; every other row HIT, Q01/Q02 INVALID',
            'DT_S0G': cmp_[0], 'comparison': cmp_[1], 'OUTER_FAILURE': a['OF'],
            'R_DRIFT_part1_under_6_3_mapping': P1N[pa['part1']], 'R_DRIFT_part1_under_3_against_precedence': P1N[pb['part1']],
            'conflict': pa['part1'] != pb['part1']}


def drift_conflict_count():
    """How often the two R-DRIFT rules differ: every outcome with AGAINST and no OUTER_FAILURE (enumerated over OF)."""
    diff = []
    for OF in (False, True):
        for code in STAGE0_CODES:
            if drift_part1(OF, code, 'S63') != drift_part1(OF, code, 'S3_literal'):
                diff.append({'OUTER_FAILURE': OF, 'stage0': code, 'S63': P1N[drift_part1(OF, code, 'S63')],
                             'S3_literal': P1N[drift_part1(OF, code, 'S3_literal')]})
    return diff


def text_findings(res):
    """Places where the r3 text leaves a classifier choice open, as this suite found them (each with its reproduction)."""
    out = []
    dc = res['drift_conflict_case']
    if dc['conflict']:
        out.append({'id': 'PS-1', 'severity': 'SHOULD_FIX',
                    'claim': ('R-DRIFT part 1 is not uniquely defined when DT-S0G reads AGAINST and OUTER_FAILURE does not hold. Section 3 '
                              'says "INCONSISTENT when any registered against-condition of the reading holds. Against takes precedence"; '
                              'the closed mapping of section 6.3 says "Part 1 is shown for an outcome where OUTER_FAILURE holds; otherwise '
                              'part 1 is NOT_ADDRESSED (PATTERN_NOT_HELD)". The two read %s and %s on the same outcome.'
                              % (dc['R_DRIFT_part1_under_3_against_precedence'], dc['R_DRIFT_part1_under_6_3_mapping'])),
                    'reproduction': 'PATTERN_SUITE_RESULTS.json drift_conflict_case: %s; DT-S0G %s %s' % (dc['outcome'], dc['DT_S0G'], dc['comparison']),
                    'fix': 'state which rule governs R-DRIFT part 1 without OUTER_FAILURE (for example: "the 6.3 mapping governs R-DRIFT; '
                           'without OUTER_FAILURE part 1 is NOT_ADDRESSED (PATTERN_NOT_HELD) whatever DT-S0G reads"), and add the case to M-12'})
    rr = res['random_registered_sizes']['metrics_both_versions']
    if rr.get('CROSSING_without_P11'):
        out.append({'id': 'PS-2', 'severity': 'NOTE',
                    'claim': ('CROSSING can hold while OUTER is not miss-dominated (so P11 is false). The section 2 table attaches P11g to '
                              'P11 ("flag P11g if CROSSING"); section 4 lists P11g as a pattern of its own, and R-HIST says "P1g or P11g makes '
                              'it more specific". This suite reads P11g = P11 and CROSSING; the reading P11g = CROSSING differs on %d of the '
                              'random registered-size classifications. P1g has no such gap: GROWING implies P1 (0 exceptions).'
                              % rr['CROSSING_without_P11']),
                    'reproduction': 'named case CROSSING_without_OUTER_FAILURE (OUTER r = 0, 0, 0, 0, 0, -2, -2, -2; CROSSING true; patterns P0, P7)',
                    'fix': 'write "P11g: P11 holds and CROSSING holds" in the table, or say that P11g is reported only with P11'})
    late_cwcm = {}
    for e in res['exhaustive_late_6state_1to3']:
        for k, v in e['late_version_metrics'].items():
            if k.startswith('CONSISTENT_without_citable_miss_') and v:
                late_cwcm[k.split('_')[-1]] = late_cwcm.get(k.split('_')[-1], 0) + v
    if late_cwcm:
        out.append({'id': 'PS-3', 'severity': 'NOTE',
                    'claim': ('A reading can read CONSISTENT although no MISS row in its scope can be cited: when every MISS row of the '
                              'triggering zone is a LATE-gate row (no frozen prediction). It happens for the OUTER readings (U1L, the M-15 '
                              'all-LATE OUTER zone), for the INNER readings under P15 (L2: 12 LATE rows and 10 HIT rows), under P7 (L4) and, in '
                              'the enumeration, under P13. C-9 consequence (iv) and M-15 record only the all-LATE OUTER zone. Readings affected in the exhaustive '
                              'LATE enumeration: %s.' % sorted(late_cwcm)),
                    'reproduction': 'named cases U1L_all_late_outer, L2, L4 (readings with scope_has_citable_miss false); exhaustive_late_6state_1to3 late_version_metrics',
                    'fix': 'extend C-9 (iv) and M-15 to the general case, or state that such a reading is reported with "no citable MISS row"'})
    out.append({'id': 'PS-4', 'severity': 'NOTE',
                'claim': ('When both STAGE0 conditions fail, 6.3 and M-14 do not say whether one reason or both are printed ("with the reason '
                          'RECEIPTS_AFTER_STEP4 if (a) fails, or NO_SEALED_SUCCESSOR if (b) fails"). This suite prints both.'),
                'reproduction': 'other_rule_cases STAGE0_both_fail', 'fix': 'say "with every reason that applies"'})
    out.append({'id': 'PS-5', 'severity': 'NOTE',
                'claim': ('Under NOT_READ, "each output whose own input is defective reads NOT_AVAILABLE" needs a map from each stop code to '
                          'the outputs it touches; the text does not give one. This suite assumes STOP_AFFECTS (for example a sensitivity '
                          'field defect touches only the sensitivity column, a TSR flag-table stop only P10, R-TSR and the flag column, and a '
                          'reference-member or zone-table stop every output, the E3 line included). Two M-12 implementations could differ here.'),
                'reproduction': 'other_rule_cases NR_field_defect, NR_E3_input_defective, NR_tsr_only; suite STOP_AFFECTS',
                'fix': 'fix the stop-to-output map in C-1.1 or in the M-12 suite'})
    return out


# ----------------------------------------------------------------------------------------------------------------- main
def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--prereg', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--random-n', type=int, default=60000)
    ap.add_argument('--xval-n', type=int, default=3000)
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    rng = random.Random(20261018)
    res = {'schema': 'UNT_MISS_READING_R3_PATTERN_SUITE_C4V001', 'started_utc': started,
           'implements': {'prereg': a.prereg, 'prereg_sha256': sha_file(a.prereg), 'root_items': a.root, 'root_items_sha256': sha_file(a.root)},
           'suite_sha256': sha_file(__file__), 'python': platform.python_version(), 'numpy': np.__version__,
           'independence': ('written from the r3 text (PREREG sections 1.1 to 6.3, 4, 5.3) and the ROOT_ITEMS M-12 case list; it does '
                            'not read or import the text stage\'s verify_r3_rules_c4.py or R3_RULES_SELFTEST.json'),
           'model': ('synthetic rows only (dimensionless ratios). Row kinds: HIT (|r| <= 1), MISS (|r| > 1, signed), NULL (a VALID '
                     'row with a null ratio: a MISS with no sign, counted in U, with a frozen prediction), LATE (a LATE-gate row: '
                     'counted as a MISS with no ratio, in U, no frozen prediction), INVALID. The first TRANSITION row plays Q25, the '
                     'one TSR-flagged row. STAGE0 is NOT_EVALUATED_BEFORE_FREEZE unless a case sets it.')}
    named = [check_named(*n) for n in NAMED]
    res['named_cases'] = named
    res['named_late_pairs'] = named_late_pairs()
    res['other_rule_cases'] = other_rule_cases()
    res['drift_conflict_case'] = drift_conflict_case()
    res['drift_rule_differences'] = drift_conflict_count()
    schemes = ['V1_flat', 'V2_outward_growth', 'V3_boundary_hits_outward_shrink', 'V4_zone_offsets']
    if a.quick:
        schemes = schemes[:1]
    res['exhaustive_5state_1to3'] = [exhaustive_main(s, 1, 3, rng, a.xval_n) for s in schemes]
    res['exhaustive_5state_0to3_V1'] = exhaustive_main('V1_flat', 0, 3, rng, a.xval_n)
    res['exhaustive_late_6state_1to3'] = [exhaustive_late(s, 1, 3, rng, a.xval_n) for s in schemes]
    res['random_registered_sizes'] = random_tests(rng, a.random_n if not a.quick else 3000)
    # witnesses for every pattern change that section 4 says a LATE gate CAN make
    seen_rem, seen_add = set(), set()
    for e in res['exhaustive_late_6state_1to3']:
        seen_rem |= {p for p, c in e['removal_counts'].items() if c}
        seen_add |= {p for p, c in e['addition_counts'].items() if c}
    rr = res['random_registered_sizes']
    seen_rem |= {p for p, c in rr['late_removal_counts'].items() if c}
    seen_add |= {p for p, c in rr['late_addition_counts'].items() if c}
    for pr in res['named_late_pairs']:
        seen_rem |= set(pr['removed'])
        seen_add |= set(pr['added'])
    res['late_can_claims'] = {'listed_removals_not_witnessed': sorted(LATE_CAN_REMOVE - seen_rem),
                              'listed_additions_not_witnessed': sorted(LATE_CAN_ADD - seen_add),
                              'removals_witnessed': sorted(seen_rem), 'additions_witnessed': sorted(seen_add)}
    # verdicts
    ex_ok = all(not any(e['violations'].values()) and not any(v for z in e['zone_level_formal_violations'].values() for v in z.values())
                and e['scalar_cross_validation']['mismatched_or_failed'] == 0 for e in res['exhaustive_5state_1to3'])
    late_ok = all(not any(e['violations'].values()) and all(z[k] == 0 for z in e['zone_level'].values() for k in z if k != 'hitdom_removed_witnessed')
                  and e['scalar_cross_validation']['mismatched_or_failed'] == 0 for e in res['exhaustive_late_6state_1to3'])
    rand_ok = not any(rr['property_violations'].values()) and not any(rr['late_violations'].values())
    res['verdicts'] = {
        'named_cases_all_ok': all(c['ok'] for c in named),
        'named_late_pairs_all_ok': all(c['ok'] for c in res['named_late_pairs']),
        'other_rule_cases_all_ok': all(c['ok'] for c in res['other_rule_cases']),
        'exhaustive_5state_1to3_no_violation_and_xval_agree': ex_ok,
        'exhaustive_late_no_violation_and_xval_agree': late_ok,
        'random_no_violation': rand_ok,
        'late_can_claims_all_witnessed': not res['late_can_claims']['listed_removals_not_witnessed'] and not res['late_can_claims']['listed_additions_not_witnessed'],
        'zero_row_zone_variant_no_violation': not any(res['exhaustive_5state_0to3_V1']['violations'].values()),
    }
    res['all_ok'] = all(res['verdicts'].values())
    res['text_findings'] = text_findings(res)
    res['seconds'] = round(time.time() - t0, 1)
    res['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    txt = json.dumps(res, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, 'item') else str(o)) + '\n'
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(txt)
    print(json.dumps({'all_ok': res['all_ok'], 'verdicts': res['verdicts'], 'seconds': res['seconds'],
                      'late_can_claims': res['late_can_claims'], 'drift_conflict': res['drift_conflict_case']['conflict']}, indent=1))
    return 0 if res['all_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
