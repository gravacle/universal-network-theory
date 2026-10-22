"""Classifier B c2v005 own suite, part 7: the A190 fix-round cases.  Extends case_defs_c2v004_v7.

The runner builds every case with suite_lib_c2v005, whose stand-ins are in the producers' forms (V006 A190: score
alternatives[], the frozen manifest, row_registration, L1, AT1; README_CLASSIFIER_B_C2V005.md lists the bytes).
Hand expectations, written from the producer bytes, the contract texts and the A190 rulings before c2v005 ran on
these cases.  Retired (RETIRED below), each with the case that re-runs its input or its clause:
- inputs written in an encoding A190 ruling 1 withdraws (PB-3 registrations, PB-7 L1 rows, PB-17 frozen
  alternatives, a role other than NON_PRIMARY, a c2v004 stand-in manifest mutation, an echo of c2v004's stand-in
  member_within_error_counts);
- expectations that A190 changes: RC4/RC4D (a failed synthesis also prints the score-missing detail; the producer's
  row and band reads), RL5B, ruling 2 (RC06/RL6 member word, RC2b/RC2R compare details, RC14 whole map, RL3 malformed
  flag record) and ruling 3 (field-map partial rename, non-list input_files).
"""
import copy
import suite_lib_c2v005 as LIB
import case_defs_c2v004_v7 as V7
from case_defs_c2v004_v7 import CASES, case, setrows, setratios, QIDS, OUTER_IDS  # noqa: F401
from case_defs_c2v004_v7 import TS, NTS, NA_PM, D_S0REC, ALT_S0REC, real, _ring  # noqa: F401
from case_defs_c2v003_v6 import D_A, D_C, D_D, D_E, D_SUP, NA_PIN, NA_AGREE, SYN  # noqa: F401
from case_defs_c2v002_v5 import D_NTEST, D_N1, D_Q25, D_OWN, D_MALF, D_FILES, D_NATIVE, NA_TSR  # noqa: F401
from case_defs_c2v001_v3 import blk, mblk, NA_ROW, NA_GATE  # noqa: F401
from case_defs_c2v001_v2 import _evaluated

RETIRED = dict(V7.RETIRED)
_R = {
    'B055': ('echoed c2v004\'s stand-in member_within_error_counts {M0, M1}; the producer writes the distribution '
             '{n, min, median, max} (v003g L4287, _distribution L4091-L4094)', 'B360'),
    'B138': ('expected the per-reason entry blanked for a registration {status, reason} with no registration key; RC5 '
             '(v003g L1788-L1798) makes it unreadable and ruling 2 (RC14) blanks the whole map', 'B361'),
    'B145': ('wrote a partial alternative_results entry and left the declared ML status NOT_EVALUATED; the library '
             'now writes an evaluated ML alternative in the producer form (ml_scored)', 'B362'),
    'B146': ('appended the recorded distance alternative with role NUISANCE; RC3 (v003g L4297) writes NON_PRIMARY', 'B363'),
    'B161': ('expected MEMBER_BEFORE_STEP4 for a finished row whose before_step4 contradicts its receipt time; ruling 2 '
             '(RC06/RC5/RL6) prints MEMBER_FINISHED', 'B365'),
    'B220': ('PB-3 (a gate pin under a nested authority object) is withdrawn by RC5', 'B366'),
    'B221': ('PB-3 (a query-id-keyed registration) is withdrawn by RC5; its expectation still held only because no row '
             'consulted the registration', 'B367'),
    'B223': ('PB-7 (L1 rows under band_rows) is withdrawn by RC7 (phase1_c2v003b L946)', 'B368'),
    'B243': ('expected a string pins.input_files to be unreadable; ruling 3 prints classifier A\'s form', 'B369'),
    'B244': ('expected a malformed flag record\'s pin conditions printed; ruling 2 (RC12/RL3) prints the malformed '
             'detail alone', 'B370'),
    'B266': ('expected (c) for ring records keyed ring_ordinal; ruling 2 (RC2R candidate (i)) prints (d)', 'B371'),
    'B296': ('RC4D (ruling 2): a failed synthesis also prints \'score output missing or malformed (None)\'', 'B372'),
    'B297': ('RC4D (ruling 2), as B296', 'B373'),
    'B298': ('RC4: the producer\'s _band_rows indexes the envelope by row (an object raises KeyError); RC4D', 'B374'),
    'B299': ('mutated c2v004\'s alternatives list, which RC4 withdraws; producer form {primary, declared}', 'B375'),
    'B300': ('mutated c2v004\'s alternatives list (scored); scored is not a frozen field in the producer form', 'B376'),
    'B304': ('RC4: the producer\'s _band_rows reads per_query[j] for every query id, so a 42-entry list raises '
             'IndexError; RC4D', 'B377'),
    'B305': ('RC4D (ruling 2), as B296', 'B378'),
    'B306': ('RC4: a row whose frozen registration is null and row_valid false is UNEVALUATED_OR_REFUSED (v003g L4045), '
             'never INVALID_AS_MISS', 'B379'),
    'B310': ('PB-17 (frozen alternatives as an object keyed by name) is withdrawn by RC4', 'B381'),
    'B311': ('RC4D (ruling 2), as B296', 'B383'),
    'B326': ('ruling 2 (RC2b/RC2R (i)): a TRUNCATION_SHAPE record without a classification is a list of objects; '
             'classification is not read', 'B384'),
    'B331': ('ruling 2 (RC2R (i)): (e) is checked independently of (c)', 'B385'),
    'B332': ('ruling 2 (RC2R (i)): classification is not read (C4-2 withdrawn)', 'B386'),
    'B333': ('ruling 2 (RC2R (i)): classification is not read (C4-2 withdrawn)', 'B387'),
    'B334': ('ruling 2 (RC2R (i)): a missing non-TRUNCATION_SHAPE list prints (e), not (c)', 'B388'),
    'B335': ('ruling 2 (RC2R (i)): 15.0 is no ordinal, so (d) prints, not (c)', 'B389'),
    'B337': ('ruling 2 (RC2R (i)): a null non-TRUNCATION_SHAPE list prints (e), not (c)', 'B390'),
    'B357': ('RL5B: prescore applies the null-phase STAGE0 rule (C4-3 withdrawn)', 'B391'),
    'B113': ('expected only that the partial map prints a row stop; ruling 3 prints classifier A\'s form, which this '
             'suite now states exactly', 'B392'),
}
for _old, (_why, _new) in _R.items():
    RETIRED[_old] = 'c2v004 %s %s; c2v005 re-runs it as %s' % (_old, _why, _new)
CASES[:] = [c for c in CASES if c['id'] not in RETIRED]

ROLE = 'NON_PRIMARY'
D_UNREAD = 'gate registration of an INVALID_AS_MISS row not readable from the frozen manifest'
D_SCORE_NONE = 'score output missing or malformed (None)'
NA_RG = {'NOT_AVAILABLE': ['FIELD_DEFECT_ROW', 'GATE_STATUS_LIST_DEFECT']}
NA_L1R = {'NOT_AVAILABLE': ['L1_RECORD_DEFECT']}
NA_L1S = {'NOT_AVAILABLE': ['L1_SHA_MISMATCH']}


def _alt(d, name):
    return [a for a in d['score']['alternatives'] if a['name'] == name][0]


def _decl(m, name):
    return [a for a in m['alternatives']['declared'] if a['name'] == name][0]


def _man(fn):
    return lambda s: s.mutate.append(lambda d, c: fn(d['manifest']))


def _pre(cid, cls, clause, fn, exp, phase='PHASE_1', successor=False):
    @case(cid, cls, clause, phase=phase, successor=successor, mode='prescore')
    def _(s):
        fn(s)
        return ([('result', 'CLASSIFICATION_INPUT_DEFECT' if cls == 'MUST_FAIL' else 'PASS')] + exp)


def _syn_fail(name):
    return [('#codes', ['FIELD_DEFECT_OUTSIDE_ROWS']), ('#details', sorted([SYN % name, D_SCORE_NONE])),
            ('stops/0/class', 'ALL')]


# ----------------------------------------------------------------------------- re-runs of retired cases
@case('B360', 'MUST_PASS', 'C-6.1 TWIN_INVALID (B055 in the producer form): the twin\'s member_within_error_counts is '
      'echoed as the scorer writes it, the distribution {n, min, median, max} (v003g L4287)', phase='PHASE_2')
def _(s):
    s.ok_rows = copy.deepcopy(s.rows)
    s.ok_twin_valid = False
    return [('A=ORIGINAL_K/status', 'TWIN_INVALID'),
            ('A=ORIGINAL_K/member_within_error_counts', {'n': 2, 'min': 41, 'median': 41.0, 'max': 41}),
            ('p8_report/ORIGINAL_K_twin_OUTER', {'NOT_AVAILABLE': ['ORIGINAL_K_TWIN_NOT_CLASSIFIED']})]


@case('B361', 'MUST_FAIL', 'RC5 + RC14 (B138): a gate row whose frozen registration lacks the registration key is not '
      'readable; FIELD_DEFECT_ROW, its reason unknown, so OUTER I_per_reason is blanked whole (ruling 2)')
def _(s):
    s.gates = {'GG': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_G'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GG')
    s.reg_extra = {'NGC3198-Q40': {'status': 'INVALID', 'reason': 'ROOT_GATE_G'}}
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD]),
            ('zones/OUTER/I_per_reason', NA_ROW), ('zones/OUTER/N_v', NA_ROW),
            ('patterns/P0_per_zone_per_reason/OUTER', NA_ROW), ('a15/E2/OUTER_I_per_reason', NA_ROW),
            ('e3_line/I_per_reason', NA_ROW)]


@case('B362', 'MUST_PASS', 'OC-22 (B145 in the producer form): an ML alternative evaluated before the freeze, scored '
      'by the scorer from alternative_results, is classified by the twin rule')
def _(s):
    s.ml_scored = True
    return [('A=ML_3p6_0.4/status', 'EVALUATED_BEFORE_FREEZE'),
            ('A=ML_3p6_0.4/classification/patterns_holding', ['P0', 'P8']), ('stops', [])]


@case('B363', 'MUST_PASS', 'C-I4 + RC3 (B146 in the producer form): the recorded distance alternative, written as '
      'score_after_freeze writes it (role NON_PRIMARY, unscored, v003g L4295-L4299), is listed with its status only',
      phase='PHASE_2')
def _(s):
    s.mutate.append(lambda d, c: d['score']['alternatives'].append(
        {'name': 'DDO154_DISTANCE_NUISANCE', 'kind': 'state', 'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'role': ROLE,
         'scored': False, 'headline': False,
         'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline (A13)'}))
    return [('alternatives/4', {'name': 'DDO154_DISTANCE_NUISANCE', 'status': 'NOT_EVALUATED_BEFORE_FREEZE',
                                'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'}),
            ('alternatives/5/name', 'STAGE0_GRID_OUTER'), ('stops', [])]


@case('B364', 'MUST_FAIL', 'RC3 (1): the recorded distance alternative with c2v004\'s role NUISANCE is a field defect of '
      'that alternative', phase='PHASE_2')
def _(s):
    s.mutate.append(lambda d, c: d['score']['alternatives'].append(
        {'name': 'DDO154_DISTANCE_NUISANCE', 'kind': 'state', 'status': 'NOT_EVALUATED_BEFORE_FREEZE',
         'role': 'NUISANCE', 'scored': False, 'headline': False}))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['DDO154_DISTANCE_NUISANCE: role']),
            ('stops/0/alternative', 'DDO154_DISTANCE_NUISANCE'),
            ('A=DDO154_DISTANCE_NUISANCE/status', 'TWIN_INPUT_DEFECT')]


@case('B365', 'MUST_FAIL', 'Ruling 2 (RC06, RC5, RL6; B161): a finished member row whose before_step4 contradicts '
      '(receipt time <= step-4 start) reads MEMBER_FINISHED', phase='PHASE_2', successor=True)
def _(s):
    s.mutate.append(mblk(lambda b: b['members'][0].__setitem__('before_step4', False)))
    return [('stage0/defect', 'MEMBER_FINISHED'), ('stage0/twin', 'TWIN_INPUT_DEFECT'),
            ('#codes', ['FIELD_DEFECT_ALTERNATIVE'])]


@case('B366', 'MUST_FAIL', 'RC5 (B220): a gate pin under a nested authority object (status AUTHORIZED_INVALID) is not '
      'the producer form: FIELD_DEFECT_ROW, whole I_per_reason blanked')
def _(s):
    s.gates = {'GN': {'status': 'LATE', 'reason': 'ROOT_GATE_N'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GN')

    def m(d, c):
        reg = d['manifest']['members'][0]['row_registration']
        i = QIDS.index('NGC3198-Q40')
        g = reg[i]['registration']
        reg[i] = {'query_id': 'NGC3198-Q40', 'status': 'AUTHORIZED_INVALID', 'reason': 'ROOT_GATE_N',
                  'authority': {'kind': 'ROOT_GATE', 'gate': g}}
    s.mutate.append(m)
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD]),
            ('zones/OUTER/I_per_reason', NA_ROW), ('status', 'NOT_READ')]


@case('B367', 'MUST_FAIL', 'RC5 (B221): a registration keyed by query id is not the producer\'s list; a gate row then '
      'reads FIELD_DEFECT_ROW')
def _(s):
    s.gates = {'GK': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_K'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GK')

    def m(d, c):
        reg = d['manifest']['members'][0]['row_registration']
        d['manifest']['members'][0]['row_registration'] = {q: e for q, e in zip(QIDS, reg)}
    s.mutate.append(m)
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD])]


@case('B368', 'MUST_FAIL', 'RC7 (B223): L1 rows under band_rows are not the band command\'s form: L1_RECORD_DEFECT on '
      'all 43 rows, no fd_noise_not_bounded entry')
def _(s):
    s.mutate_l1 = [lambda d, c: d['l1'].__setitem__('band_rows', d['l1'].pop('rows'))]
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1R), ('row=NGC3198-Q43/phase1_band/overlaps', NA_L1R),
            ('row=NGC3198-Q10/phase1_band/fd_noise_not_bounded', '#absent'), ('stops', []),
            ('status', 'CLASSIFIED')]


@case('B369', 'MUST_FAIL', 'Ruling 3 (c2v002 RC11, c2v003 RL4; B243): a string pins.input_files is iterated as A '
      'iterates it and holds no pin: every input-files requirement reads "not pinned"')
def _(s):
    s.mutate.append(lambda d, c: LIB_pin(d, 'n1_record_pin', '1'))
    s.mutate.append(lambda d, c: d['flag']['flags'][QIDS.index('NGC3198-Q26')].__setitem__('TRUNCATION_SHAPE_RESIDUAL', True))
    s.mutate_late = [lambda d, c: d['manifest'].__setitem__('pins', {'code_files': [], 'input_files': 'x'})]
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']),
            ('#details', sorted([D_N1, D_Q25, D_OWN, 'ntest_compare_pin not pinned among the freeze input files',
                                 'gl_node_record_pin not pinned among the freeze input files']))]


def LIB_pin(d, key, hexchar):
    d['flag'][key] = {'path': key + '.json', 'sha256': hexchar * 64}


@case('B370', 'MUST_FAIL', 'Ruling 2 (c2v002 RC12, c2v003 RL3; B244): a flag record with an extra key prints its single '
      '"missing or malformed" detail and no field condition (its wrong n1 pin is not printed)')
def _(s):
    s.mutate.append(lambda d, c: d['flag'].__setitem__('note', 'extra key'))
    s.mutate.append(lambda d, c: LIB_pin(d, 'n1_record_pin', '1'))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_MALF])]


@case('B371', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B266): ring records keyed ring_ordinal: the list is a list of objects, '
      'so not (c); no record has the integer ordinal 15, so (d), and native_ring has no record')
def _(s):
    s.ring_key = 'ring_ordinal'
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', sorted([D_D, D_NATIVE]))]


_pre('B372', 'MUST_FAIL', 'RC4 + V-F3 + RC4D (B296): a frozen speed beyond float range raises OverflowError in the '
     'producer\'s ladder; the score is then read as missing',
     _man(lambda m: m['members'][1]['speeds_km_s'].__setitem__(7, 10 ** 400)), _syn_fail('OverflowError'))
_pre('B373', 'MUST_FAIL', 'RC4 + RC4D (B297): members[].row_valid missing', _man(lambda m: m['members'][0].pop('row_valid')),
     _syn_fail('KeyError'))
_pre('B374', 'MUST_FAIL', 'RC4 + RC4D (B298): pointwise_envelope an object, indexed by row as _band_rows indexes it',
     _man(lambda m: m.__setitem__('pointwise_envelope', {'rows': []})), _syn_fail('KeyError'))
_pre('B375', 'MUST_FAIL', 'RC4 (B299): ML_3p6_0.4 missing from the frozen alternatives.declared (score-mode condition)',
     _man(lambda m: m['alternatives'].__setitem__(
         'declared', [a for a in m['alternatives']['declared'] if a['name'] != 'ML_3p6_0.4'])),
     [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['ML_3p6_0.4: declared alternative missing']),
      ('stops/0/alternative', 'ML_3p6_0.4'), ('stops/0/class', 'ALT')])
_pre('B376', 'MUST_FAIL', 'RC4 + RC3 (B300): a declared alternative whose status is not a registered value reaches the '
     'synthetic score unscored and is a field defect (status)',
     _man(lambda m: _decl(m, 'GL10_SOURCE_GAUSS_ORDER').__setitem__('status', 'MAYBE')),
     [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['GL10_SOURCE_GAUSS_ORDER: status'])])
_pre('B377', 'MUST_FAIL', 'RC4 + RC4D (B304): a 42-entry sensitivity.per_query raises IndexError in _band_rows',
     _man(lambda m: m['sensitivity']['per_query'].pop()), _syn_fail('IndexError'), phase='PHASE_2')
_pre('B378', 'MUST_FAIL', 'RC4 + RC4D (B305): sensitivity missing from a Phase-2 frozen manifest',
     _man(lambda m: m.pop('sensitivity')), _syn_fail('KeyError'), phase='PHASE_2')
_pre('B379', 'MUST_FAIL', 'RC4 (B306): a reference row with row_valid false and a null frozen registration is '
     'UNEVALUATED_OR_REFUSED (the producer\'s ladder), which fires the class-ALL stop in prescore',
     _man(lambda m: m['members'][0]['row_valid'].__setitem__(5, False)),
     [('#codes', ['REFERENCE_ROW_UNEVALUATED_OR_REFUSED']),
      ('#details', ['a reference-member row has status UNEVALUATED_OR_REFUSED']), ('stops/0/class', 'ALL')])
_pre('B380', 'MUST_FAIL', 'RC4: a frozen INVALID registration whose reason is null reaches the synthetic row as '
     'registered_reason null: the score-mode row rule (FIELD_DEFECT_ROW)',
     _man(lambda m: (m['members'][0]['row_valid'].__setitem__(5, False),
                     m['members'][0]['speeds_km_s'].__setitem__(5, None),
                     m['members'][0]['row_registration'].__setitem__(
                         5, {'status': 'INVALID', 'reason': None, 'registration': None}))),
     [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q06: registered_reason missing on an INVALID_AS_MISS row']),
      ('stops/0/rows', ['NGC3198-Q06']), ('stops/0/class', 'ROW')])
_pre('B381', 'MUST_FAIL', 'RC4 (B310): frozen alternatives as an object keyed by name (PB-17) is not the producer\'s '
     '{primary, declared}: no synthetic score (KeyError)',
     _man(lambda m: m.__setitem__('alternatives', {a['name']: {k: v for k, v in a.items() if k != 'name'}
                                                   for a in m['alternatives']['declared']})), _syn_fail('KeyError'))
_pre('B382', 'MUST_FAIL', 'RC4: frozen alternatives as a list (c2v004\'s stand-in form): no synthetic score (TypeError)',
     _man(lambda m: m.__setitem__('alternatives', list(m['alternatives']['declared']))), _syn_fail('TypeError'))
_pre('B383', 'MUST_FAIL', 'RC4 + RC4D (B311): a frozen speed that is a string', _man(
    lambda m: m['members'][0]['speeds_km_s'].__setitem__(3, 'fast')), _syn_fail('TypeError'))


@case('B384', 'MUST_FAIL', 'Ruling 2 (RC2b, RC2R (i); B326): a TRUNCATION_SHAPE record {ordinal 3} added: the list is '
      'a list of objects (not (c)) of two records (d); the single ordinal-15 record still equals native_ring')
def _(s):
    s.compare_mut.append(lambda c, r: c[TS].append({'ordinal': 3}))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_D])]


@case('B385', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B331): c2v003\'s PB-5\' form: no TRUNCATION_SHAPE list (c), no '
      'non-TRUNCATION_SHAPE list (e, independently), native_ring has no record')
def _(s):
    def m(c, r):
        c.pop(TS)
        c.pop(NTS)
        rr = {k: v for k, v in r.items() if k != 'classification'}
        rr['class'] = 'TRUNCATION_SHAPE'
        c['failing_rings'] = [rr]
    s.compare_mut.append(m)
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', sorted([D_C, D_E, D_NATIVE]))]


@case('B386', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B332): classification is not read; the record differs from native_ring '
      'only in classification, so native_ring alone')
def _(s):
    s.compare_mut.append(lambda c, r: c.__setitem__(TS, [dict(r, classification='NOT_GRID')]))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_NATIVE])]


@case('B387', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B333): a TRUNCATION_SHAPE-classified record in the non-TRUNCATION_SHAPE '
      'list: that list is not empty (e)')
def _(s):
    s.compare_mut.append(lambda c, r: c[NTS].append(_ring(40, 'TRUNCATION_SHAPE')))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_E])]


@case('B388', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B334): the non-TRUNCATION_SHAPE list missing reads (e)')
def _(s):
    s.compare_mut.append(lambda c, r: c.pop(NTS))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_E])]


@case('B389', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B335): ordinal 15.0 is no ordinal: (d), and native_ring has no record')
def _(s):
    s.compare_mut.append(lambda c, r: c.__setitem__(TS, [dict(r, ordinal=15.0)]))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', sorted([D_D, D_NATIVE]))]


@case('B390', 'MUST_FAIL', 'Ruling 2 (RC2R (i); B337): the non-TRUNCATION_SHAPE list null reads (e)')
def _(s):
    s.compare_mut.append(lambda c, r: c.__setitem__(NTS, None))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_E])]


@case('B391', 'MUST_FAIL', 'RL5B (B357): in prescore a null phase reads the STAGE0 record as score mode does; a malformed '
      'record prints the STAGE0 alternative\'s stop beside PHASE_MISMATCH', phase='PHASE_2', mode='prescore')
def _(s):
    s.mutate_pi = [lambda d, c: d['phase_inputs'].pop('run_status_code')]
    s.stage0_record = {'schema': 'STAGE0_STATUS_RECORD_C4V003'}
    return [('mode', 'prescore'), ('phase', None), ('result', 'CLASSIFICATION_INPUT_DEFECT'),
            ('#codes', ['FIELD_DEFECT_ALTERNATIVE', 'PHASE_MISMATCH']), ('stops/0', ALT_S0REC)]


@case('B392', 'MUST_FAIL', 'Ruling 3 (c2v001 RC11, c2v002 RC9, c2v003 RL1; B113): the rename sig_ratio -> sigma_ratio at '
      'members[].rows[] collides on Q11: Q01-Q10 are renamed, Q11 keeps its key, and nothing after it is renamed')
def _(s):
    def m(d, c):
        rows = d['score']['members'][0]['rows']
        for r in rows:
            r['sig_ratio'] = r.pop('sigma_ratio')
        rows[10]['sigma_ratio'] = 'collide'
    s.mutate.append(m)
    s.field_map = {'schema': 'KEY_FIELD_MAP_C4V001',
                   'renames': {'score': [{'at': 'members[].rows[]', 'from': 'sig_ratio', 'to': 'sigma_ratio'}]}}
    return [('header/field_map', 'FIELD_MAP_DEFECT_PARTIAL'), ('#codes', ['FIELD_DEFECT_ROW']),
            ('#details', sorted(['NGC3198-Q11: sigma_ratio wrong type or non-finite'] +
                                ['%s: sigma_ratio missing' % q for q in QIDS[11:]]))]


# ----------------------------------------------------------------------------- RC3: score alternatives[] entry form
@case('B393', 'MUST_PASS', 'RC3: the scorer\'s Phase-2 alternatives (a PRIMARY entry, NON_PRIMARY roles, scoring_scope '
      'only on STAGE0, no members on an unscored entry) read with no stop; the evaluated ORIGINAL_K is classified',
      phase='PHASE_2')
def _(s):
    return [('stops', []), ('status', 'CLASSIFIED'), ('A=ORIGINAL_K/status', 'EVALUATED_BEFORE_FREEZE'),
            ('A=ORIGINAL_K/twin_log_index', 0), ('A=ML_3p6_0.4/status', 'NOT_EVALUATED_BEFORE_FREEZE'),
            ('A=GL10_SOURCE_GAUSS_ORDER/status', 'NOT_EVALUATED_BEFORE_FREEZE'),
            ('A=STAGE0_GRID_OUTER/status', 'NOT_EVALUATED_BEFORE_FREEZE')]


@case('B394', 'MUST_FAIL', 'RC3 (1): c2v004\'s stand-in role ALTERNATIVE on a non-PRIMARY entry is a field defect')
def _(s):
    s.mutate.append(lambda d, c: _alt(d, 'ML_3p6_0.4').__setitem__('role', 'ALTERNATIVE'))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['ML_3p6_0.4: role']),
            ('A=ML_3p6_0.4/status', 'TWIN_INPUT_DEFECT')]


@case('B395', 'MUST_FAIL', 'RC3 (1): role null on a non-PRIMARY entry is a field defect')
def _(s):
    s.mutate.append(lambda d, c: _alt(d, 'GL10_SOURCE_GAUSS_ORDER').__setitem__('role', None))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['GL10_SOURCE_GAUSS_ORDER: role'])]


@case('B396', 'MUST_FAIL', 'RC3 (2): STAGE0_GRID_OUTER without scoring_scope', phase='PHASE_2')
def _(s):
    s.mutate.append(lambda d, c: _alt(d, 'STAGE0_GRID_OUTER').pop('scoring_scope'))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['STAGE0_GRID_OUTER: scoring_scope']),
            ('stops/0/alternative', 'STAGE0_GRID_OUTER')]


@case('B397', 'MUST_FAIL', 'RC3 (2), c2v001 RC03 item (5): a STAGE0 scoring_scope whose query_ids are not the OUTER set '
      'is the field defect scoring_scope', phase='PHASE_2', successor=True)
def _(s):
    _evaluated(s, [0.5] * 8)
    s.mutate.append(lambda d, c: _alt(d, 'STAGE0_GRID_OUTER')['scoring_scope'].__setitem__('query_ids', QIDS[34:42]))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['STAGE0_GRID_OUTER: scoring_scope']),
            ('stage0/twin', 'TWIN_INPUT_DEFECT')]


@case('B398', 'MUST_FAIL', 'RC3 (4) + ruling 2 (RC3c): two failing fields of one entry, joined by a bare comma in the '
      'order kind, status, role, scored, scoring_scope, members')
def _(s):
    s.mutate.append(lambda d, c: _alt(d, 'GL10_SOURCE_GAUSS_ORDER').update(status='X', role='ALTERNATIVE'))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['GL10_SOURCE_GAUSS_ORDER: status,role'])]


@case('B399', 'MUST_FAIL', 'RC3 (3): an entry scored true without a members key', phase='PHASE_2')
def _(s):
    s.mutate.append(lambda d, c: _alt(d, 'ORIGINAL_K').pop('members'))
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE']), ('#details', ['ORIGINAL_K: members'])]


@case('B400', 'MUST_PASS', 'RC3 (2)/(3): an unscored entry has no members key and no scoring_scope (the scorer\'s form); '
      'neither is a defect', phase='PHASE_2')
def _(s):
    def m(d, c):
        a = _alt(d, 'ML_3p6_0.6')
        assert 'members' not in a and 'scoring_scope' not in a
    s.mutate.append(m)
    return [('stops', []), ('A=ML_3p6_0.6/status', 'NOT_EVALUATED_BEFORE_FREEZE')]


# ----------------------------------------------------------------------------- RC4: the prescore synthetic score
_pre('B401', 'MUST_PASS', 'RC4: Phase-1 prescore on a manifest in the freeze module\'s form: PASS', lambda s: None,
     [('stops', []), ('manifest_phase_derived', 'PHASE_1')])
_pre('B402', 'MUST_FAIL', 'RC4: envelope rows keyed lo_km_s / hi_km_s (c2v004\'s stand-in) are not the producer form',
     _man(lambda m: m.__setitem__('pointwise_envelope', [
         {'query_id': r['id'], 'lo_km_s': 90.0, 'hi_km_s': 110.0, 'valid': True} for r in m['pointwise_envelope']])),
     _syn_fail('KeyError'))
_pre('B403', 'MUST_FAIL', 'RC4: a member without member_valid (no default)', _man(lambda m: m['members'][1].pop('member_valid')),
     _syn_fail('KeyError'))
_pre('B404', 'MUST_FAIL', 'RC4: the envelope label the frozen rows carry is the synthetic score\'s label; one that does '
     'not start with the registered prefix is ENVELOPE_LABEL_MISMATCH',
     _man(lambda m: [r.__setitem__('label', 'POINTWISE_ENVELOPE') for r in m['pointwise_envelope']]),
     [('#codes', ['ENVELOPE_LABEL_MISMATCH']), ('#details', ['pointwise_envelope.label prefix differs or is missing'])])
_pre('B405', 'MUST_FAIL', 'RC4: an evaluated non-PRIMARY alternative with no alternative_results entry (KeyError)',
     _man(lambda m: m['alternative_results'].pop('ORIGINAL_K')), _syn_fail('KeyError'), phase='PHASE_2')
_pre('B406', 'MUST_PASS', 'RC4 + RC5: a reference row frozen INVALID with a gate registration on the list reads '
     'INVALID_AS_MISS in the synthetic score; PASS',
     lambda s: (s.gates.update({'GP': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_P'}}),
                setrows(s, ['NGC3198-Q40'], 'G', gate='GP')),
     [('stops', [])])
_pre('B407', 'MUST_FAIL', 'RC4: the reference member not among the frozen members (score_after_freeze L4228 next() '
     'raises StopIteration)',
     _man(lambda m: m['reference_member'].__setitem__('member_id', 'M9')), _syn_fail('StopIteration'))
_pre('B408', 'MUST_FAIL', 'RC4 + RC5: a frozen gate registration in c2v004\'s stand-in form (pin under gate) is read as '
     'not readable on the synthetic INVALID_AS_MISS row',
     lambda s: (s.gates.update({'GQ': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_Q'}}),
                setrows(s, ['NGC3198-Q40'], 'G', gate='GQ'),
                s.mutate.append(lambda d, c: d['manifest']['members'][0]['row_registration'].__setitem__(
                    QIDS.index('NGC3198-Q40'), {'status': 'INVALID', 'reason': 'ROOT_GATE_Q',
                                                'gate': {'path': 'gate_GQ.json', 'sha256': '0' * 64}}))),
     [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD])])
_pre('B409', 'MUST_PASS', 'RC4: an evaluated STAGE0 alternative is scored on its scope rows from its declared '
     'scoring_scope; Phase-2 successor prescore PASS', lambda s: _evaluated(s, [0.5] * 8), [('stops', [])],
     phase='PHASE_2', successor=True)


# ----------------------------------------------------------------------------- RC5 / RL9: row_registration form
@case('B410', 'MUST_PASS', 'RC5: a producer-form gate registration (registration = the gate pin) is read: LATE gate, '
      'LATE_GATE_MISS')
def _(s):
    s.gates = {'GL': {'status': 'LATE', 'reason': 'ROOT_GATE_L'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GL')
    return [('row=NGC3198-Q40/reading_kind', 'LATE_GATE_MISS'), ('row=NGC3198-Q40/gate_status', 'LATE'),
            ('stops', []), ('status', 'CLASSIFIED')]


@case('B411', 'MUST_FAIL', 'RC5: c2v004\'s stand-in gate form (the pin under the key gate, no registration key) is not '
      'readable')
def _(s):
    s.gates = {'GO': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_O'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GO')

    def m(d, c):
        reg = d['manifest']['members'][0]['row_registration']
        i = QIDS.index('NGC3198-Q40')
        reg[i] = {'status': 'INVALID', 'reason': 'ROOT_GATE_O', 'gate': reg[i]['registration']}
    s.mutate.append(m)
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD]),
            ('zones/OUTER/I_per_reason', NA_ROW)]


@case('B412', 'MUST_FAIL', 'RC5: a frozen gate reason that differs from the score row\'s registered_reason is not '
      'readable for that row')
def _(s):
    s.gates = {'GR': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_R'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GR')
    s.mutate.append(lambda d, c: d['manifest']['members'][0]['row_registration'][QIDS.index('NGC3198-Q40')].__setitem__(
        'reason', 'ROOT_GATE_OTHER'))
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q40: ' + D_UNREAD])]


@case('B413', 'MUST_PASS', 'RC5 + V-F1: a gate pin with an upper-case sha is read lower-cased')
def _(s):
    s.gates = {'GU': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_U'}}
    setrows(s, ['NGC3198-Q40'], 'G', gate='GU')

    def m(d, c):
        p = d['manifest']['members'][0]['row_registration'][QIDS.index('NGC3198-Q40')]['registration']
        p['sha256'] = p['sha256'].upper()
    s.mutate.append(m)
    return [('row=NGC3198-Q40/gate_status', 'ON-TIME'), ('stops', []), ('status', 'CLASSIFIED')]


@case('B414', 'MUST_FAIL', 'RC5: a built-in reason with a gate pin is not the producer form (v003g L1919-L1922): '
      'the row\'s kinds are unknown when it also has a field defect, so I_per_reason is blanked whole (RL9)')
def _(s):
    def m(d, c):
        reg = d['manifest']['members'][0]['row_registration']
        reg[0] = {'status': 'INVALID', 'reason': LIB.BUILTIN_IN, 'registration': {'path': 'g.json', 'sha256': '3' * 64}}
        d['score']['members'][0]['rows'][0].pop('within_error')
    s.mutate.append(m)
    return [('#codes', ['FIELD_DEFECT_ROW']),
            ('#details', ['NGC3198-Q01: within_error missing; within_error wrong type']),
            ('zones/INNER/I_per_reason', NA_ROW)]


@case('B415', 'MUST_FAIL', 'RL9: a readable gate that is not on the list blanks only its own reason; the built-in '
      'reason keeps its count')
def _(s):
    s.gates = {'GM': {'status': 'LATE', 'on_list': False, 'in_roster': False, 'reason': 'ROOT_GATE_M'}}
    setrows(s, ['NGC3198-Q03'], 'G', gate='GM')
    return [('#codes', ['GATE_STATUS_LIST_DEFECT']),
            ('zones/INNER/I_per_reason', {'QUERY_INSIDE_INNERMOST_NODE': 2,
                                          'ROOT_GATE_M': {'NOT_AVAILABLE': ['GATE_STATUS_LIST_DEFECT']}})]


@case('B416', 'MUST_PASS', 'RC5: an evaluated STAGE0 twin row registered INVALID with an on-time gate: its frozen '
      'registration is the 43-row list aligned with query_ids (v003g L4086-L4087), read for the scope ids',
      phase='PHASE_2', successor=True)
def _(s):
    s.gates = {'GS': {'status': 'ON-TIME', 'reason': 'ROOT_GATE_S'}}
    setratios(s, OUTER_IDS, [-2.0] * 8)
    _evaluated(s, [-0.5] * 3 + [-1.5] * 5)
    s.stage0_rows[4] = {'kind': 'G', 'gate': 'GS'}
    return [('stops', []), ('stage0/twin_classification/rows/4/reading_kind', 'INVALID_AS_MISS'),
            ('stage0/twin_classification/rows/4/invalid_reason', 'ROOT_GATE_S')]


# ----------------------------------------------------------------------------- RC7 + ruling 2 (RC15): the L1 record
@case('B417', 'MUST_FAIL', 'RC7: an L1 record without the band label is L1_RECORD_DEFECT on all 43 rows')
def _(s):
    s.mutate_l1 = [lambda d, c: d['l1'].pop('label')]
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1R), ('row=NGC3198-Q03/phase1_band/overlaps', NA_L1R),
            ('row=NGC3198-Q10/phase1_band/fd_noise_not_bounded', '#absent'), ('stops', [])]


@case('B418', 'MUST_FAIL', 'RC7: an L1 record whose label is not exactly the band command\'s label')
def _(s):
    s.mutate_l1 = [lambda d, c: d['l1'].__setitem__('label', LIB.L1_LABEL + ' ')]
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1R)]


@case('B419', 'MUST_FAIL', 'Ruling 2 (c2v002 RC15): L1 bytes that do not hash to the bundle pin read L1_SHA_MISMATCH')
def _(s):
    s.mutate_bundle.append(lambda b, c: b['inputs']['l1_record'].__setitem__('sha256', '1' * 64))
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1S), ('stops', []), ('status', 'CLASSIFIED')]


@case('B420', 'MUST_FAIL', 'Ruling 2 (c2v002 RC15): the record form is checked before the phase1_header.l1_sha256 '
      'comparison: a record with another module and a header sha that differs reads L1_RECORD_DEFECT')
def _(s):
    s.mutate_l1 = [lambda d, c: d['l1'].__setitem__('module', 'phase1_c2v002')]
    s.mutate_pi = [lambda d, c: d['phase_inputs']['phase1_header'].__setitem__('l1_sha256', '1' * 64)]
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1R)]


@case('B421', 'MUST_FAIL', 'Ruling 2 (c2v002 RC15) control: a record in form whose phase1_header.l1_sha256 differs '
      'reads L1_SHA_MISMATCH')
def _(s):
    s.mutate_pi = [lambda d, c: d['phase_inputs']['phase1_header'].__setitem__('l1_sha256', '1' * 64)]
    return [('row=NGC3198-Q10/phase1_band/overlaps', NA_L1S)]


# ----------------------------------------------------------------------------- RC8: AT1 at0
def _at1(outcome='COVERED', **kw):
    r = {'schema': 'PHASE1_AT1_C2V001', 'module': 'phase1_c2v003b', 'outcome': outcome, 'failing': [],
         'non_discriminating_rows': ['NGC3198-Q03'], 'reported': LIB.reported_v003a()}
    r.update(LIB.at1_extras(outcome))
    r.update(kw)
    return r


@case('B422', 'MUST_FAIL', 'RC8: an AT1 record without at0 is AGREE_RECORD_DEFECT (OUTCOME); Phase 1 keeps its label',
      phase='PHASE_2')
def _(s):
    s.agree = {k: v for k, v in _at1().items() if k != 'at0'}
    s.agree_raw = True
    return [('agreement/outcome', NA_AGREE), ('agreement/agree_record_defect', 'OUTCOME'),
            ('agreement/phase1_consequence', 'PHASE_1_KEEPS_PROVISIONAL_LABEL_NEITHER_STANDING_NOR_WITHDRAWN'),
            ('stops', []), ('status', 'CLASSIFIED')]


@case('B423', 'MUST_FAIL', 'RC8: at0 is a field of the AT1 record itself, so AGREEMENT_DEFECT does not excuse it',
      phase='PHASE_2')
def _(s):
    s.agree = {'schema': 'PHASE1_AT1_C2V001', 'module': 'phase1_c2v003b', 'outcome': 'AGREEMENT_DEFECT'}
    s.agree_raw = True
    return [('agreement/outcome', NA_AGREE), ('agreement/agree_record_defect', 'OUTCOME')]


@case('B424', 'MUST_FAIL', 'RC8: at0 that is not exactly two strings (one entry)', phase='PHASE_2')
def _(s):
    s.agree = _at1(at0=['PASS'])
    s.agree_raw = True
    return [('agreement/agree_record_defect', 'OUTCOME')]


@case('B425', 'MUST_PASS', 'RC8: an AGREEMENT_DEFECT AT1 record with at0 [PASS, AGREEMENT_DEFECT] is read',
      phase='PHASE_2')
def _(s):
    s.agree = {'schema': 'PHASE1_AT1_C2V001', 'module': 'phase1_c2v003b', 'outcome': 'AGREEMENT_DEFECT',
               'at0': ['PASS', 'AGREEMENT_DEFECT']}
    s.agree_raw = True
    return [('agreement/outcome', 'AGREEMENT_DEFECT'), ('agreement/agree_record_defect', '#absent'),
            ('agreement/phase1_consequence', 'PHASE_2_STANDS_ROOT_INVESTIGATES')]


# ----------------------------------------------------------------------------- RL5B control
@case('B426', 'MUST_FAIL', 'RL5B control: in prescore a null phase with an honest STAGE0 record prints PHASE_MISMATCH '
      'alone', phase='PHASE_2', mode='prescore')
def _(s):
    s.mutate_pi = [lambda d, c: d['phase_inputs'].pop('run_status_code')]
    return [('mode', 'prescore'), ('phase', None), ('#codes', ['PHASE_MISMATCH'])]


@case('B427', 'MUST_FAIL', 'RL5B: a null-phase Phase-1 prescore bundle supplies no STAGE0 record (C4-4): the stop prints',
      mode='prescore')
def _(s):
    s.mutate_pi = [lambda d, c: d['phase_inputs'].pop('run_status_code')]
    return [('#codes', ['FIELD_DEFECT_ALTERNATIVE', 'PHASE_MISMATCH']), ('stops/0', ALT_S0REC)]


# ----------------------------------------------------------------------------- ruling 2: row field wording, status
@case('B428', 'MUST_FAIL', 'Ruling 2 (c2v001 RC07, c2v002 RC8, c2v003 RC6): an absent within_error prints "missing" and '
      '"wrong type"')
def _(s):
    s.mutate.append(lambda d, c: d['score']['members'][0]['rows'][QIDS.index('NGC3198-Q40')].pop('within_error'))
    return [('#details', ['NGC3198-Q40: within_error missing; within_error wrong type'])]


@case('B429', 'MUST_FAIL', 'Ruling 2 (RC07): every "missing" message first, then the type messages, each in field order; '
      'an absent sigma_ratio prints "missing" only')
def _(s):
    def m(d, c):
        r = d['score']['members'][0]['rows'][QIDS.index('NGC3198-Q40')]
        r.pop('status')
        r.pop('sigma_ratio')
        r.pop('score_status')
    s.mutate.append(m)
    return [('#details', ['NGC3198-Q40: score_status missing; sigma_ratio missing; status missing; '
                          'score_status wrong type; status wrong type'])]


@case('B430', 'MUST_FAIL', 'Ruling 2 (c2v001 RC08, c2v003 RL2; OC-14): a row status outside VALID, INVALID, '
      'UNEVALUATED_OR_REFUSED is "status wrong type"')
def _(s):
    s.mutate.append(lambda d, c: d['score']['members'][0]['rows'][QIDS.index('NGC3198-Q20')].__setitem__('status', 'x'))
    return [('#codes', ['FIELD_DEFECT_ROW']), ('#details', ['NGC3198-Q20: status wrong type'])]


# ----------------------------------------------------------------------------- ruling 2: RC13, RC16, compare, STAGE0
@case('B431', 'MUST_FAIL', 'Ruling 2 (c2v002 RC13): a frozen manifest that does not load also prints the dependent '
      'detail "manifest reference_member / members unreadable"')
def _(s):
    s.mutate_bundle.append(lambda b, c: b['inputs']['freeze_manifest'].__setitem__('sha256', '1' * 64))
    return [('#details', 'has:freeze manifest missing or malformed (SHA_MISMATCH)'),
            ('#details', 'has:manifest reference_member / members unreadable'), ('status', 'NOT_READ')]


@case('B432', 'MUST_FAIL', 'Ruling 2 (c2v002 RC16): a v002 failing entry with the six keys and a category outside the '
      'three v002 categories reads FAILING_KEYS_V002', phase='PHASE_2')
def _(s):
    s.tool = {'sha256': LIB.TOOL_V002, 'module': 'phase1_c2v002'}
    s.agree = {'schema': 'PHASE1_AT1_C2V001', 'module': 'phase1_c2v002', 'outcome': 'SUPERSEDED',
               'failing': [{'log_index': 1, 'id': 'NGC3198-Q40', 'excess': 0.7, 'norm_n': 1.2,
                            'category': 'OUTSIDE_BOX_SLICE', 'flag': None}],
               'non_discriminating_rows': [], 'reported': LIB.reported_v002()}
    return [('agreement/agree_record_defect', 'FAILING_KEYS_V002'), ('agreement/outcome', NA_AGREE)]


@case('B433', 'MUST_FAIL', 'Ruling 2 (RC2R (i)): a supplied compare that loads as a non-object (a JSON list) prints '
      '"compare unreadable (None)" and no (c), (d) or (e); its pin is not the registered one (a), and native_ring has '
      'no record')
def _(s):
    def m(d, c):
        raw = LIB.dumps([1, 2, 3])
        with open(c['dir'] + '/compare_list.json', 'xb') as f:
            f.write(raw)
        c['compare_list_sha'] = LIB.sha(raw)
    s.mutate.append(m)
    s.mutate_bundle.append(lambda b, c: b['inputs'].__setitem__(
        'ntest_compare', {'path': 'compare_list.json', 'sha256': c['compare_list_sha']}))
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']),
            ('#details', sorted([D_A, 'compare unreadable (None)', D_NATIVE]))]


@case('B434', 'MUST_FAIL', 'Ruling 2 (RL6): on the exception path a finished row with a null step-4 start (before_step4 '
      'null) lacks a step-4 start: MEMBER_FINISHED', phase='PHASE_2', successor=True)
def _(s):
    blk(s, diagnostics=['STAGE0_RECEIPT_RULE_EXCEPTION: TypeError'], rule_a_receipts_finished=False,
        rule_b_successor_sealed=False, reasons=['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'],
        reading='NOT_EVALUATED_BEFORE_FREEZE', step4_start_utc=None)
    s.mutate.append(mblk(lambda b: [x.__setitem__('before_step4', None) for x in b['members']]))
    return [('stage0/defect', 'MEMBER_FINISHED'), ('#codes', ['FIELD_DEFECT_ALTERNATIVE'])]


@case('B435', 'MUST_PASS', 'Ruling 2 (RL6) control: on the exception path a finished row with before_step4 null and a '
      'step-4 start is read (NOT_EVALUATED_BEFORE_FREEZE [RNF, NSS])', phase='PHASE_2', successor=True)
def _(s):
    blk(s, diagnostics=['STAGE0_RECEIPT_RULE_EXCEPTION: TypeError'], rule_a_receipts_finished=False,
        rule_b_successor_sealed=False, reasons=['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'],
        reading='NOT_EVALUATED_BEFORE_FREEZE')
    s.mutate.append(mblk(lambda b: [x.__setitem__('before_step4', None) for x in b['members']]))
    return [('stage0/status', 'NOT_EVALUATED_BEFORE_FREEZE'), ('stops', [])]


@case('B436', 'MUST_FAIL', 'Ruling 2 (RL6): an unfinished member row with before_step4 set reads MEMBER_BEFORE_STEP4',
      phase='PHASE_2', successor=True)
def _(s):
    s.mutate.append(mblk(lambda b: b['members'][1].update(terminal_status='FAILED', finished=False)))
    return [('stage0/defect', 'MEMBER_BEFORE_STEP4')]


# ----------------------------------------------------------------------------- ruling 3
@case('B437', 'MUST_FAIL', 'Ruling 3: after a refused rename the role\'s later renames are skipped; another role\'s '
      'rename still applies (the flag record reads in form, so no TSR stop)')
def _(s):
    def m(d, c):
        rows = d['score']['members'][0]['rows']
        rows[0]['sig_ratio'] = 1.0           # Q01 holds both keys: the first rename collides at once
        for r in rows[1:]:
            r['wthn'] = r.pop('within_error')
        d['flag']['flag_list'] = d['flag'].pop('flags')
    s.mutate.append(m)
    s.field_map = {'schema': 'KEY_FIELD_MAP_C4V001',
                   'renames': {'score': [{'at': 'members[].rows[]', 'from': 'sig_ratio', 'to': 'sigma_ratio'},
                                         {'at': 'members[].rows[]', 'from': 'wthn', 'to': 'within_error'}],
                               'tsr_flag_record': [{'at': '', 'from': 'flag_list', 'to': 'flags'}]}}
    return [('header/field_map', 'FIELD_MAP_DEFECT_PARTIAL'), ('#codes', ['FIELD_DEFECT_ROW']),
            ('#details', 'has:NGC3198-Q02: within_error missing; within_error wrong type'),
            ('#details', 'has:NGC3198-Q43: within_error missing; within_error wrong type')]


@case('B438', 'MUST_FAIL', 'Ruling 3: pins.input_files an object is iterated (its keys) and holds no pin')
def _(s):
    s.mutate_late = [lambda d, c: d['manifest']['pins'].__setitem__('input_files', {'tsr_flag_record.json': 'x'})]
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']),
            ('#details', sorted([D_OWN, 'ntest_compare_pin not pinned among the freeze input files',
                                 'n1_record_pin not pinned among the freeze input files',
                                 'gl_node_record_pin not pinned among the freeze input files']))]


@case('B439', 'MUST_FAIL', 'Ruling 3 scope: pins.input_files a number is not iterable and stays unreadable')
def _(s):
    s.mutate_late = [lambda d, c: d['manifest']['pins'].__setitem__('input_files', 7)]
    return [('#codes', ['TSR_FLAG_TABLE_MISMATCH']), ('#details', [D_FILES])]
