#!/usr/bin/env python3
"""classifier_a_c4v004 -- Implementation A of the M-12 classifier for PREREG_MISS_READING_R3A (lane Claude4).
Successor of classifier_a_c4v003 (394a8b61, verified 0 BLOCKING), itself the successor of c4v002 (a11ae7b9) and c4v001
(06f169e2). The only change against c4v003 is root ruling A168 V-N1: a frozen stage0_status block written on the STAGE0
successor's exception path (d260ee30 _stage0_receipt_verdict's except clause, STAGE0_RECEIPT_RULE_EXCEPTION) is read at
the module's own reading, NOT_EVALUATED_BEFORE_FREEZE [STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR], with every
identity and structure check the module still guarantees on that path (_stage0_exception_path, _stage0_facts); the
output schema is unchanged. What c4v003 changed against c4v002 follows.

Text of record: basis/PREREG_MISS_READING_R3A.md (sha 4242ee15..., the r3a render with the classifier-build table
F1-F15 and the c4v002 rows T3 and D6), with ROOT_ITEMS_R3A.md (ed9f5c5b...) as ruled in A142 (rulings draft 0f45f3c4);
the phase1 `band`/`agree` encodings bound from the bytes of the pinned tool: phase1_c2v002 (d64351ec) and
phase1_c2v003b (7d891ff7; A144, A149, and v003b's values custody); the STAGE0 successor
prediction_freeze_c2v003g_stage0_c2v002 (d260ee30; A154, E_A154_1) bound through the frozen manifest's stage0_status
block when the seal pins it.
Changes against c4v002 (README section CHANGES): the phase1 binding switches by the pinned sha between d64351ec and
7d891ff7 only (385b287c and any other sha: PHASE1_TOOL_PIN_DEFECT); the v003b AT0B values_sha256 is bound and printed;
the STAGE0 status is read from the successor's frozen stage0_status block in a Phase 2 that the seal runs under the
successor, and otherwise from root's STAGE0 status record, whose contract is now an exact projection of that block;
the freeze manifest's schema must be the one of the module the seal names for the phase; basis row T3 (an
envelope-row defect blanks NEAR and N(Z) only on tier-MISS rows) is implemented; basis row D6 (a missing agree record
is a defective one) needed no change.
Every rule below lives in a function whose docstring names the clause (section and tag) it implements. The classifier
is target-blind by construction: it reads only the files named in its input bundle, verifies each file's sha256 before
parsing, and never opens anything else.

Usage (stdlib only, Python 3.12):
    classifier_a_c4v004.py BUNDLE.json OUT.json      writes one canonical JSON output (exclusive create)
The importable entry point is classify_bundle(path) -> bytes.

Canonical output: json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n'.
An output that the text's stop-to-output map blanks is written {"NOT_AVAILABLE": [codes...]}.
"""
import hashlib
import itertools
import json
import math
import os
import sys

NAME = 'classifier_a_c4v004'
OUT_SCHEMA = 'CLASSIFIER_A_OUTPUT_C4V001'
BUNDLE_SCHEMA = 'CLASSIFIER_A_BUNDLE_C4V001'
NA_KEY = 'NOT_AVAILABLE'
PHASE1, PHASE2 = 'PHASE_1', 'PHASE_2'

# ---------------------------------------------------------------- constants fixed by the text
QIDS = tuple('NGC3198-Q%02d' % i for i in range(1, 44))                     # C-I1
ZONES = ('INNER', 'TRANSITION', 'OUTER')
ZONE_TABLE = dict([(q, 'INNER') for q in QIDS[:24]] + [(q, 'TRANSITION') for q in QIDS[24:35]] +
                  [(q, 'OUTER') for q in QIDS[35:]])                          # C-1.3 table
OUTER_IDS = QIDS[35:]
E1_SUBTABLE_IDS = QIDS[2:15]                                                 # C-5.1 (Q03-Q15)
FLAGGED_IDS = ('NGC3198-Q25',)                                               # C-1.4 "This id list governs"
ALWAYS_NA_BAND_IDS = ('NGC3198-Q01', 'NGC3198-Q02')                         # C-1.1 Phase-1 band, M-16 ruling
BUILTIN_REASONS = ('QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT', 'QUERY_OUTSIDE_RETAINED_SUPPORT')
ENVELOPE_PREFIX = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'               # C-I3, C-1.1
COMPARE_SHA = '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'
N1_SHA = '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70'
NODE_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
SUPPORT_LOWER_KPC = 9.901810628740723                                        # C-1.4 support record
SUPPORT_UPPER_KPC = 10.911721936765339
FAILING_RING_ORDINAL = 15
PHASE1_TOOL_V002_SHA = 'd64351ecc06c61e99e2d7253c5d4311617fc1f64d34d37523102ed32720a6754'
PHASE1_TOOL_V003B_SHA = '7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4'   # phase1_c2v003b.py (shasum)
PHASE1_TOOL_V003B_MODULE = 'phase1_c2v003b'                                    # its MODULE literal (L99)
PHASE1_TOOLS = {PHASE1_TOOL_V002_SHA: 'phase1_c2v002', PHASE1_TOOL_V003B_SHA: PHASE1_TOOL_V003B_MODULE}   # brief item 1
# freeze modules the seal names per phase (M-5 addition (2), A142; A154 and erratum E_A154_1, read from the bytes)
MANIFEST_SCHEMA_V003G = 'FREEZE_MANIFEST_C2V003G'                             # v003g 48a1e48a L49
MANIFEST_SCHEMA_SUCCESSOR = 'FREEZE_MANIFEST_C2V003G_STAGE0_C2V002'           # successor d260ee30 L64
STAGE0_SUCCESSOR_SHA = 'd260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0'   # (shasum)
STAGE0_SUCCESSOR_MODULE = 'prediction_freeze_c2v003g_stage0_c2v002'           # its MODULE_NAME (L66)
# the frozen stage0_status block as the successor writes it (STAGE0_BLOCK_KEYS, STAGE0_MEMBER_KEYS; L3541-3550)
STAGE0_BLOCK_KEYS = frozenset({'rule', 'alternative', 'module', 'successor_module_sha256', 'status_record',
                               'status_record_custody_ok', 'phase', 'sealed_successor', 'step4_start_utc', 'members',
                               'rule_a_receipts_finished', 'rule_b_successor_sealed', 'receipts_before_step4',
                               'receipt_refusals', 'evaluation_refusals', 'diagnostics', 'reading', 'reasons',
                               'post_score_exploratory'})
STAGE0_MEMBER_KEYS = frozenset({'member_id', 'log_index', 'receipt', 'custody_ok', 'terminal_status', 'written_utc',
                                'finished', 'before_step4', 'defects'})
# root's STAGE0 status record (contract STAGE0_STATUS_RECORD_C4V003): an exact projection of that block (A154)
STAGE0_RECORD_SCHEMA = 'STAGE0_STATUS_RECORD_C4V003'
STAGE0_PROJ_KEYS = ('phase', 'sealed_successor', 'step4_start_utc', 'members', 'rule_a_receipts_finished',
                    'rule_b_successor_sealed', 'receipts_before_step4', 'receipt_refusals', 'evaluation_refusals',
                    'reading', 'reasons', 'post_score_exploratory')
STAGE0_PROJ_MEMBER_KEYS = ('log_index', 'terminal_status', 'written_utc', 'finished', 'before_step4')
STAGE0_SOURCE_RECORD = 'STAGE0_STATUS_RECORD_C4V003'
STAGE0_SOURCE_BLOCK = 'FREEZE_MANIFEST_STAGE0_STATUS_BLOCK'
S0_EVALUATED, S0_NOT_EVALUATED, S0_REFUSED = 'EVALUATED_BEFORE_FREEZE', 'NOT_EVALUATED_BEFORE_FREEZE', 'EVALUATED_REFUSED'
S0_RNF, S0_NSS, S0_RA4 = 'STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR', 'RECEIPTS_AFTER_STEP4'
# A168 V-N1: the successor's exception path (d260ee30 L3841-3843): `except Exception as exc:` forces
# rule_a_receipts_finished and rule_b_successor_sealed to False and appends
# 'STAGE0_RECEIPT_RULE_EXCEPTION: %s' % type(exc).__name__ as the last diagnostic.
S0_EXCEPTION_PREFIX = 'STAGE0_RECEIPT_RULE_EXCEPTION'      # a diagnostic starting with this claims the path
S0_EXCEPTION_FORM = 'STAGE0_RECEIPT_RULE_EXCEPTION: '      # the exact form: this, then a class __name__
E3_NEGATIVE = 'TESTED-NEGATIVE (A15 E3 scope)'                               # C-5.3 value; C-8 words rule (V-F2)
NEAR_LABEL = 'envelope overlaps the error bar'                                # C-1.1 NEAR gloss (V-F6)
PHASE1_BAND_LABEL = 'PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER'
PHASE1_BAND_CONDITION = 'conditional on A13 (the fixed DDO154 distance 4.04 Mpc and inclination 66 deg)'
ALT_ORDER = ('BR_A_F10_PRIMARY', 'ORIGINAL_K', 'ML_3p6_0.4', 'ML_3p6_0.6', 'GL10_SOURCE_GAUSS_ORDER',
             'STAGE0_GRID_OUTER')                                            # C-I4 table
PRIMARY = 'BR_A_F10_PRIMARY'
DISTANCE_ALT = 'DDO154_DISTANCE_NUISANCE'
NOT_EVAL_NOTE = 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'   # C-6.2
LABEL_P1 = 'PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE)'                       # C-I7
LABEL_INCOMPLETE = 'PROVISIONAL (FREEZE_INCOMPLETE)'
LABEL_NGATE = 'PROVISIONAL (N_GATE_NOT_OPEN)'                                # C-I6
LABEL_EXPLORATORY_P2 = 'EXPLORATORY (PHASE 2 NOT AS COMMITTED)'             # C-I7
D2_NOTE = 'D-2/A65.4: counted coefficient-grid uncertainty; not converted into a number; widens no sigma; changes no tier'
SENS_LABEL = 'conditional on trial values'
P1_ATTEST_NOTE = 'Phase 2 attestation covers only the Phase-2-only output values (the calls not re-bound from Phase 1)'

# Readings (C-3.2, table order). Triggers: 'OF' = OUTER_FAILURE; 'MM:Z' = MINORITY_MISS(Z).
READINGS = ('R-MF', 'R-UT1', 'R-REACH', 'R-HIST', 'R-DRIFT', 'R-S1', 'R-GRID', 'R-NAX', 'R-GEFF', 'R-ML',
            'R-SPEC', 'R-GEO', 'R-TSR')
TRIGGERS = {
    'R-MF': ('OF', 'P3', 'P4', 'P12', 'P15', 'P13', 'P6', 'P7', 'MM:INNER', 'MM:TRANSITION', 'MM:OUTER'),
    'R-UT1': ('OF',),
    'R-REACH': ('OF',),
    'R-HIST': ('OF', 'P13', 'P6', 'P7', 'MM:TRANSITION', 'MM:OUTER'),
    'R-DRIFT': ('OF',),
    'R-S1': ('P2', 'P11', 'P6'),
    'R-GRID': ('P2', 'P11'),
    'R-NAX': ('P11', 'P14', 'P3', 'P4', 'P12', 'P15', 'P13', 'P7'),
    'R-GEFF': ('P3', 'P4', 'P12', 'P15'),
    'R-ML': ('P3', 'P4', 'P12', 'P15'),
    'R-SPEC': ('P3', 'P4', 'P12', 'P15', 'MM:INNER'),
    'R-GEO': ('P3', 'P4', 'P12', 'P15', 'P6'),
    'R-TSR': ('P10',),
}
# C-3 scope rule: the zone (or ALL / FLAGGED) each trigger names.
TRIGGER_SCOPE = {'OF': 'OUTER', 'P2': 'OUTER', 'P11': 'OUTER', 'P14': 'OUTER', 'P3': 'INNER', 'P4': 'INNER',
                 'P12': 'INNER', 'P15': 'INNER', 'P13': 'TRANSITION', 'P6': 'ALL', 'P7': 'ALL', 'P10': 'FLAGGED',
                 'MM:INNER': 'INNER', 'MM:TRANSITION': 'TRANSITION', 'MM:OUTER': 'OUTER'}
DEFICIT_TYPE = ('R-UT1', 'R-REACH')                                          # C-3.2 sign rule
SIGN_SCOPE = {'R-MF': 'sign-free', 'R-UT1': 'deficit-type', 'R-REACH': 'deficit-type', 'R-HIST': 'sign-free',
              'R-DRIFT': 'sign-free'}
DECIDING = {   # C-3.1 status at writing; part 2 is OPEN for each (R-MF and R-DRIFT have their own rule)
    'R-UT1': ('DT-UT1', 'NOT SCHEDULED'), 'R-REACH': ('DT-U12', 'NOT SCHEDULED'), 'R-HIST': ('DT-BHD', 'NOT SCHEDULED'),
    'R-S1': ('DT-S1', 'UNTESTED'), 'R-GRID': ('NONE_REGISTERED', 'none registered'), 'R-NAX': ('DT-NAX', 'not run'),
    'R-GEFF': ('DT-S1', 'UNTESTED'), 'R-ML': ('DT-ALT', 'NOT_EVALUATED_BEFORE_FREEZE (M/L); DT-T1a diagnostic'),
    'R-SPEC': ('DT-T1a', 'diagnostic; never changes part 2'), 'R-GEO': ('DT-GEO', 'NOT_EVALUATED_BEFORE_FREEZE'),
    'R-TSR': ('DT-TSR', 'NOT SCHEDULED'),
}
PRIOR = {   # C-3.2 prior-evidence column (closed list), ASCII rendering
    'R-MF': ['for: A15 E2, which expected an outer deficit', 'for: A41'],
    'R-UT1': ['against: A41 item 3 (FORMAL + TESTED): no gate-consistent typing gives an attractive tail, and the '
              'spec-compliant T(0+) is finite and repulsive on current estimates'],
    'R-REACH': [], 'R-HIST': [],
    'R-DRIFT': ['for: the sealed k = 0 drift reading is SUPPORTED (A63)',
                'against: its causal gloss is UNTESTED (A65 check R-3)'],
    'R-S1': [],
    'R-GRID': ["against: T120L passes C2, C3, C4 and C1' (A27)",
               "against: the production N-tests N0, NQ, N2 and N3' pass (A90)"],
    'R-NAX': [], 'R-GEFF': [],
    'R-ML': ['the ML_3p6 alternatives are NOT_EVALUATED_BEFORE_FREEZE (slots V003)'],
    'R-SPEC': [], 'R-GEO': [],
    'R-TSR': ['against: route B consumes the azimuthal mean, so the phi-spread S enters no row directly '
              '(A66.2; A42 TESTED)'],
}
PATTERN_IDS = ('P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P11g', 'P12',
               'P13', 'P14', 'P15')
PATTERN_NAMES = {'P0': 'INVALID rows', 'P1': 'OUTER_DEFICIT', 'P1g': 'P1 flag GROWING', 'P2': 'OUTER_EXCESS',
                 'P3': 'INNER_EXCESS', 'P4': 'INNER_DEFICIT', 'P5': 'TRANSITION_ONSET', 'P6': 'GLOBAL_OFFSET',
                 'P7': 'SCATTERED', 'P8': 'NO_MISS_AMONG_VALID_ROWS', 'P9': 'OUTER_UNTESTABLE', 'P10': 'TSR_MISS',
                 'P11': 'OUTER_MIXED', 'P11g': 'P11 flag CROSSING', 'P12': 'INNER_MIXED', 'P13': 'TRANSITION_MISS',
                 'P14': 'OUTER_UNSIGNED', 'P15': 'INNER_UNSIGNED'}
KINDS = ('H', 'MS', 'MN', 'I', 'L')     # HIT, signed MISS, null-ratio MISS, INVALID, LATE-gate MISS
KIND_IX = {k: i for i, k in enumerate(KINDS)}
KIND_NAME = {'H': 'HIT', 'MS': 'MISS_SIGNED', 'MN': 'MISS_NULL_RATIO', 'I': 'INVALID_AS_MISS', 'L': 'LATE_GATE_MISS'}

# phase1 tool encodings bound for the A133 `agree` record (C-1.1 map), read from the bytes of the pinned tool:
# phase1_c2v002 d64351ec (unchanged from c4v001) and phase1_c2v003b 7d891ff7, which is phase1_c2v003a 385b287c (at1_rows,
# cmd_at1, cmd_at0b, member_eps, band_region_extent, band_region_box_only_extent; A144 R1-R3, A149 items 1-3) with
# MODULE 'phase1_c2v003b' and one more AT0B key, values_sha256 (v003b V1; cmd_at0b writes a.values_sha256.lower()).
# The AGREE_V003A_* names below are the v003a encodings that v003b keeps unchanged (DIFF v003a->v003b fd095be9).
AGREE_V002_FAIL_KEYS = frozenset({'log_index', 'id', 'excess', 'norm_n', 'category', 'flag'})
AGREE_V002_CATEGORIES = ('OUTSIDE_TRUST_RADIUS', 'OUTSIDE_LINEAR_DDO_REGION', 'NGC_NONLINEAR')
AGREE_V003A_FAIL_KEYS = frozenset({'log_index', 'id', 'excess', 'norm_n', 'category', 'flag', 'flag_reason',
                                   'region_rows_violated', 'region_max_violation', 'geometric_part', 'residual_part'})
AGREE_V003A_CATEGORIES = ('OUTSIDE_TRUST_RADIUS', 'OUTSIDE_BOX_SLICE', 'OUTSIDE_LINEAR_DDO_REGION', 'NGC_NONLINEAR')
AGREE_V003A_FAMILIES = ('TRUST_RADIUS', 'BOX', 'LINEAR_DDO')                 # REGION_FAMILIES, the print order
AGREE_V003A_CAT_OF = {'TRUST_RADIUS': 'OUTSIDE_TRUST_RADIUS', 'BOX': 'OUTSIDE_BOX_SLICE',
                      'LINEAR_DDO': 'OUTSIDE_LINEAR_DDO_REGION'}               # REGION_CATEGORY
# at1_rows: `flag` is None, FD_NOISE_NOT_BOUNDED (row without eps_q; flag_reason NO_ROW_EPS_Q) or
# MEMBER_POINT_NOISE_NOT_BOUNDED (flag_reason = member_eps's reason); flag_reason is None exactly when flag is None.
FLAG_FD = 'FD_NOISE_NOT_BOUNDED'
FLAG_MPN = 'MEMBER_POINT_NOISE_NOT_BOUNDED'
REASON_NO_ROW_EPS = 'NO_ROW_EPS_Q'
MEMBER_EPS_REASONS = ('MEMBER_EPS_LIST_MISSING', 'MEMBER_EPS_NONE', 'MEMBER_EPS_BOOL', 'MEMBER_EPS_NOT_A_NUMBER',
                      'MEMBER_EPS_NON_FINITE', 'MEMBER_EPS_NEGATIVE')           # member_eps return values
AGREE_V002_REPORTED = ('rows_not_tested_phase1_not_available', 'e_q_per_member_row', 'rows_fd_noise_not_bounded',
                       'ngc_linearity_residuals', 'envelope_vs_band_width', 'max_ddo_linearity_deviation_over_tau',
                       'identified_projection_vs_linear_region')
AGREE_V003A_REPORTED = frozenset(AGREE_V002_REPORTED + (
    'pairs_member_point_noise_not_bounded', 'band_region_extent', 'band_region_single_point',
    'band_region_single_point_reason', 'band_region_box_only_extent'))         # at1_rows' second return value, exactly
AGREE_OUTCOMES = ('COVERED', 'SUPERSEDED', 'AGREEMENT_DEFECT')

INPUT_ROLES = ('phase_inputs', 'freeze_manifest', 'score', 'slots', 'gate_status_list', 'tsr_flag_record',
               'tsr_support_record', 'ntest_compare', 'stage0_status', 'commitment_status', 'agree_record',
               'phase1_classification', 'l1_record', 'c3_record', 'root_disclosures', 'fallback', 'field_map')


class StrictJSONError(ValueError):
    pass


class BundleError(ValueError):
    pass


def _pairs(pairs):
    """A71 / M-12 strict parsing: a duplicate key refuses; nothing is last-wins."""
    d = {}
    for k, v in pairs:
        if k in d:
            raise StrictJSONError('DUPLICATE_KEY:%s' % k)
        d[k] = v
    return d


def _const(name):
    raise StrictJSONError('NON_FINITE_CONSTANT:%s' % name)


def _float(s):
    v = float(s)
    if not math.isfinite(v):
        raise StrictJSONError('NON_FINITE_NUMBER:%s' % s)
    return v


def strict_loads(raw):
    """M-12 strict loader: UTF-8 only; duplicate keys, NaN, Infinity, -Infinity and overflowing float literals (e.g.
    1e400) refuse the whole input. An integer literal is read exactly; one beyond the float range is refused later, as
    a field defect of its class (is_num, V-F3). An integer of more than 4300 digits exceeds Python's int-string limit
    and refuses the whole input (JSON_SYNTAX)."""
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise StrictJSONError('NOT_UTF8')
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_const, parse_float=_float)
    except StrictJSONError:
        raise
    except (ValueError, RecursionError) as exc:
        raise StrictJSONError('JSON_SYNTAX:%s' % type(exc).__name__)


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n').encode()


def sha256_hex(raw):
    return hashlib.sha256(raw).hexdigest()


def is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def is_hex64_ci(s):
    """V-F1: v003g's own _is_hex64 (48a1e48a L289): 64 characters, hex after lower-casing. Used where v003g accepts an
    upper-case pin (the roster root_gates pins, _root_pinned_document) and for the gate identities compared with them;
    the compared values are lower-cased, as v003g compares `pin['sha256'].lower()`."""
    if not isinstance(s, str) or len(s) != 64:
        return False
    return all(c in '0123456789abcdef' for c in s.lower())


def is_num(x):
    """A finite JSON number. V-F3: an integer beyond the float range (math.isfinite raises OverflowError) is not
    finite, so it reads as a field defect of its class, never as an internal error."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    try:
        return math.isfinite(x)
    except OverflowError:
        return False


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_str(x):
    return isinstance(x, str) and x != ''


def na(codes):
    return {NA_KEY: sorted(set(codes))}


def median(vals):
    """C-2: the median; for an even count, the mean of the two middle values."""
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return None
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def under(p, root):
    return p == root or p.startswith(root.rstrip(os.sep) + os.sep)


def parse_utc(s):
    """Timestamps as `date -u` ISO strings YYYY-MM-DDTHH:MM:SS[.ffffff]Z (the classifier's input contract)."""
    if not isinstance(s, str) or len(s) < 20 or not s.endswith('Z') or s[4] != '-' or s[7] != '-' or s[10] != 'T' \
            or s[13] != ':' or s[16] != ':':
        raise ValueError('BAD_UTC')
    body = s[:-1]
    main, frac = (body.split('.', 1) + [''])[:2] if '.' in body else (body, '')
    parts = (main[0:4], main[5:7], main[8:10], main[11:13], main[14:16], main[17:19])
    if len(main) != 19 or not all(p.isdigit() for p in parts) or (frac and not frac.isdigit()):
        raise ValueError('BAD_UTC')
    return tuple(int(p) for p in parts) + (int((frac + '000000')[:6]) if frac else 0,)


# ================================================================ the classifier
class Run:
    """One classification run over one input bundle."""

    def __init__(self, bundle_path):
        self.bundle_path = os.path.abspath(bundle_path)
        self.base = os.path.dirname(self.bundle_path)
        self.docs, self.load_err, self.shas = {}, {}, {}
        self.stops = {}            # (code, cls, alt) -> {'detail': set, 'rows': set}
        self.notes = []
        self.env, self.sens, self.rad = {}, {}, {}
        self.ref_rows_raw, self.mref, self.phase = None, None, None

    # ------------------------------------------------------------ bundle and inputs
    def _path(self, p):
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(self.base, p))

    def load_bundle(self):
        """Input bundle contract (README section 'The input bundle'). A malformed bundle refuses the run."""
        try:
            with open(self.bundle_path, 'rb') as f:
                raw = f.read()
            b = strict_loads(raw)
        except (OSError, StrictJSONError) as exc:
            raise BundleError('BUNDLE_UNREADABLE:%s' % exc)
        if not isinstance(b, dict) or b.get('schema') != BUNDLE_SCHEMA:
            raise BundleError('BUNDLE_SCHEMA')
        need = {'schema', 'mode', 'inputs', 'rosters', 'sealed', 'phase1_tool', 'module_sha256'}
        if set(b) != need:
            raise BundleError('BUNDLE_KEYS:%s' % sorted(set(b) ^ need))
        if b['mode'] not in ('score', 'prescore'):
            raise BundleError('BUNDLE_MODE')
        if not isinstance(b['inputs'], dict) or set(b['inputs']) != set(INPUT_ROLES):
            raise BundleError('BUNDLE_INPUT_ROLES')
        for role, spec in b['inputs'].items():
            if spec is not None and not self._pin_ok(spec):
                raise BundleError('BUNDLE_PIN:%s' % role)
        if not isinstance(b['rosters'], dict) or not all(isinstance(k, str) and self._pin_ok(v)
                                                         for k, v in b['rosters'].items()):
            raise BundleError('BUNDLE_ROSTERS')
        s = b['sealed']
        if not isinstance(s, dict) or set(s) != {'text', 'classifier', 'tsr_flag_record_sha256', 'stage0_successor'}:
            raise BundleError('BUNDLE_SEALED')
        if not self._pin_ok(s['text']) or not self._pin_ok(s['classifier']) or \
                not is_hex64(s['tsr_flag_record_sha256']) or \
                (s['stage0_successor'] is not None and not self._pin_ok(s['stage0_successor'])):
            raise BundleError('BUNDLE_SEALED_PINS')
        t = b['phase1_tool']
        if t is not None and (not isinstance(t, dict) or set(t) != {'sha256', 'module'} or not is_hex64(t['sha256'])
                              or not isinstance(t['module'], str)):
            raise BundleError('BUNDLE_PHASE1_TOOL')
        if not is_hex64(b['module_sha256']):
            raise BundleError('BUNDLE_MODULE_SHA')
        self.b = b
        self.mode = b['mode']

    @staticmethod
    def _pin_ok(spec):
        return isinstance(spec, dict) and set(spec) == {'path', 'sha256'} and isinstance(spec['path'], str) and \
            spec['path'] != '' and is_hex64(spec['sha256'])

    @staticmethod
    def _pin_ok_ci(spec):
        """V-F1: a roster root_gates pin as v003g's _root_pinned_document accepts it (L1603: exactly path and sha256,
        a string path, _is_hex64 sha in either case). The path is not opened here (v003g read it at the freeze)."""
        return isinstance(spec, dict) and set(spec) == {'path', 'sha256'} and isinstance(spec['path'], str) and \
            spec['path'] != '' and is_hex64_ci(spec['sha256'])

    def read_pinned(self, spec):
        """Every input's sha256 is verified on its bytes before it is parsed (brief item 1)."""
        try:
            with open(self._path(spec['path']), 'rb') as f:
                raw = f.read()
        except OSError:
            return None, 'UNREADABLE'
        if sha256_hex(raw) != spec['sha256']:
            return None, 'SHA_MISMATCH'
        try:
            return strict_loads(raw), None
        except StrictJSONError as exc:
            return None, 'JSON_DEFECT:%s' % exc

    def load_inputs(self):
        for role in INPUT_ROLES:
            spec = self.b['inputs'][role]
            if spec is None:
                self.docs[role], self.load_err[role] = None, 'NOT_SUPPLIED'
                continue
            self.shas[role] = spec['sha256']
            doc, err = self.read_pinned(spec)
            self.docs[role], self.load_err[role] = doc, err
        self.rosters = {}
        for name, spec in sorted(self.b['rosters'].items()):
            doc, err = self.read_pinned(spec)
            self.rosters[name] = (doc, err, spec['sha256'])
        fm = self.docs.get('field_map')
        self.field_map_status = 'NOT_SUPPLIED' if self.b['inputs']['field_map'] is None else 'APPLIED'
        if self.b['inputs']['field_map'] is not None:
            renames = self._field_map_renames(fm)
            if renames is None:
                self.field_map_status = 'FIELD_MAP_DEFECT_NOT_APPLIED'
            else:
                for role, lst in renames.items():
                    if self.docs.get(role) is not None:
                        ok = all(self._apply_rename(self.docs[role], r['at'], r['from'], r['to']) for r in lst)
                        if not ok:
                            self.field_map_status = 'FIELD_MAP_DEFECT_PARTIAL'

    # ------------------------------------------------------------ the key-only field map (C-1.1 "Rename a field")
    def _field_map_renames(self, fm):
        """C-1.1 root's one permitted act: a field map renames keys only and never changes a value."""
        if not isinstance(fm, dict) or fm.get('schema') != 'KEY_FIELD_MAP_C4V001' or set(fm) != {'schema', 'renames'} \
                or not isinstance(fm['renames'], dict):
            return None
        for role, lst in fm['renames'].items():
            if role not in INPUT_ROLES or role == 'field_map' or not isinstance(lst, list):
                return None
            for r in lst:
                if not isinstance(r, dict) or set(r) != {'at', 'from', 'to'} or not isinstance(r['at'], str) or \
                        not is_str(r['from']) or not is_str(r['to']) or r['from'] == r['to']:
                    return None
        return fm['renames']

    def _apply_rename(self, doc, at, old, new):
        toks = [t for t in at.split('.') if t] if at else []

        def walk(x, i):
            if i == len(toks):
                if isinstance(x, dict) and old in x:
                    if new in x:
                        return False
                    x[new] = x.pop(old)
                return True
            t = toks[i]
            arr = t.endswith('[]')
            key = t[:-2] if arr else t
            if not isinstance(x, dict) or key not in x:
                return True
            y = x[key]
            if arr:
                if not isinstance(y, list):
                    return True
                return all(walk(e, i + 1) for e in y)
            return walk(y, i + 1)
        return walk(doc, 0)

    # ------------------------------------------------------------ stops
    def stop(self, code, cls, detail, rows=(), alt=None):
        k = (code, cls, alt)
        e = self.stops.setdefault(k, {'detail': set(), 'rows': set()})
        if detail:
            e['detail'].add(detail)
        e['rows'].update(rows)

    def codes(self, *classes):
        return sorted({k[0] for k in self.stops if k[1] in classes})

    def any_stop(self, *classes):
        return any(k[1] in classes for k in self.stops)

    # ================================================================ pre-score checks (C-1.1)
    def check_seal(self):
        """C-1.1 SEAL_SHA_MISMATCH: a sealed sha (this text, the classifier, the flag record, the STAGE0 successor if
        pinned) does not match its bytes. Checked from the bytes named in the bundle's `sealed` block."""
        s = self.b['sealed']
        for label in ('text', 'classifier'):
            spec = s[label]
            try:
                with open(self._path(spec['path']), 'rb') as f:
                    raw = f.read()
            except OSError:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', '%s unreadable' % label)
                continue
            if sha256_hex(raw) != spec['sha256']:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', '%s bytes do not hash to the sealed sha' % label)
        if s['stage0_successor'] is not None:
            spec = s['stage0_successor']
            try:
                with open(self._path(spec['path']), 'rb') as f:
                    raw = f.read()
                if sha256_hex(raw) != spec['sha256']:
                    self.stop('SEAL_SHA_MISMATCH', 'ALL', 'stage0_successor bytes do not hash to the sealed sha')
            except OSError:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', 'stage0_successor unreadable')
        fr = self.b['inputs']['tsr_flag_record']
        if fr is None or fr['sha256'] != s['tsr_flag_record_sha256'] or self.load_err.get('tsr_flag_record') in (
                'UNREADABLE', 'SHA_MISMATCH'):
            self.stop('SEAL_SHA_MISMATCH', 'ALL', 'tsr_flag_record bytes do not hash to the sealed sha')

    def check_phase(self):
        """C-1.1 PHASE_MISMATCH [r3a]: the manifest's phase is PHASE_1 iff its input_bindings.calibration_record path,
        resolved to an absolute real path, lies under the resolved Phase-1 registry root that the seal entry names;
        PHASE_2 otherwise. The Phase-1 root must be disjoint from the Phase-2 registry. The named phase must equal it."""
        pi = self.docs.get('phase_inputs')
        self.phase = None
        why = self._phase_inputs_check(pi)
        if why in ('PHASE1_HEADER_MISSING', 'RUN_STATUS_NOT_OF_PHASE'):
            # the record is well-formed and names a legible phase; it is refused for its header or run status only.
            # The named phase is kept, so no input of the other phase is demanded (PHASE_MISMATCH is the one stop).
            self.phase = pi['phase_named']
        if why == 'PHASE1_HEADER_MISSING':
            self.stop('PHASE_MISMATCH', 'ALL', 'phase inputs record: PHASE1_HEADER_MISSING (a scored Phase 1 needs '
                                                'phase1_header, which carries the L1 sha logged at the Phase-1 freeze; '
                                                'C-1.1 L1 map row; V-F4)')
            return
        if why == 'RUN_STATUS_NOT_OF_PHASE':
            self.stop('PHASE_MISMATCH', 'ALL', 'phase inputs record: RUN_STATUS_NOT_OF_PHASE (%s is not a run status '
                                                'of %s; C-I7; V-F5)' % (pi['run_status'], pi['phase_named']))
            return
        if why is not None:
            self.stop('PHASE_MISMATCH', 'ALL', 'phase inputs record missing or malformed (%s)'
                      % self.load_err.get('phase_inputs'))
            return
        self.phase = pi['phase_named']
        man = self.docs.get('freeze_manifest')
        try:
            cal = man['input_bindings']['calibration_record']['path']
            if not isinstance(cal, str) or not os.path.isabs(cal):
                raise TypeError
        except (TypeError, KeyError):
            self.stop('PHASE_MISMATCH', 'ALL', 'manifest input_bindings.calibration_record.path missing or not absolute')
            return
        r1 = os.path.realpath(pi['phase1_registry_root'])
        r2 = os.path.realpath(pi['phase2_registry_root'])
        if under(r1, r2) or under(r2, r1):
            self.stop('PHASE_MISMATCH', 'ALL', 'Phase-1 and Phase-2 registry roots are not disjoint')
            return
        derived = PHASE1 if under(os.path.realpath(cal), r1) else PHASE2
        self.manifest_phase = derived
        if derived != self.phase:
            self.stop('PHASE_MISMATCH', 'ALL', 'score entry names %s; manifest calibration record gives %s'
                      % (self.phase, derived))

    def successor_mode(self):
        """M-5 addition (2) (A142) and M-14's pin rule: when the seal entry pins the STAGE0 successor, Phase 2 runs under
        it (its manifest, its stage0_status block); Phase 1 always runs under v003g. The bundle's sealed
        stage0_successor pin is the seal entry's (A154)."""
        return self.phase == PHASE2 and self.b['sealed']['stage0_successor'] is not None

    def check_manifest_schema(self, man):
        """M-5 addition (2) (A142): the seal entry names the freeze module per phase, and the frozen manifest is read in
        that module's schema. A154 with erratum E_A154_1: the successor's manifest schema is
        FREEZE_MANIFEST_C2V003G_STAGE0_C2V002 (d260ee30 L64), accepted for Phase 2 when the successor is pinned; v003g's
        is FREEZE_MANIFEST_C2V003G (48a1e48a L49), for Phase 1 and for a Phase 2 without the successor. Any other schema
        is a field of the frozen manifest outside the rows: FIELD_DEFECT_OUTSIDE_ROWS ("every other"; open choice OC-36).
        Not checked when the phase is unknown (the phase inputs were refused: PHASE_MISMATCH already blanks all)."""
        if self.phase is None or not isinstance(man, dict):
            return
        want = MANIFEST_SCHEMA_SUCCESSOR if self.successor_mode() else MANIFEST_SCHEMA_V003G
        if man.get('schema') != want:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'freeze manifest schema %r is not %s, the schema of the freeze '
                                                          'module the seal names for %s (M-5 addition 2; A154)'
                      % (man.get('schema'), want, self.phase if not self.successor_mode()
                         else 'PHASE_2 with the STAGE0 successor pinned'))

    # C-I7 'No classification, or no score of record': an engine terminal status or NO_IDENTIFIED_DIRECTION ends both
    # phases (NO_NGC_CALL); an AT-0a failure stops Phase 1 only (AT0A_FAILED); a campaign halt under A133 3 rule (c)
    # leaves Phase 2 reported HALTED. A run status of the other phase is refused (V-F5).
    RUN_STATUS_PHASES = {'SCORED': (PHASE1, PHASE2), 'NO_NGC_CALL': (PHASE1, PHASE2), 'AT0A_FAILED': (PHASE1,),
                         'HALTED': (PHASE2,)}

    @classmethod
    def _phase_inputs_check(cls, pi):
        """The phase-inputs contract (PHASE_INPUTS_C4V001; README). None when the record holds; otherwise the refusal
        code: MALFORMED, PHASE1_HEADER_MISSING (V-F4: a scored Phase 1 needs the header, whose l1_sha256 the C-1.1 L1
        map row checks) or RUN_STATUS_NOT_OF_PHASE (V-F5)."""
        keys = {'schema', 'phase_named', 'phase1_registry_root', 'phase2_registry_root', 'run_status',
                'run_status_code', 'phase1_header', 'phase1_classification_absent_reason'}
        if not isinstance(pi, dict) or set(pi) != keys or pi['schema'] != 'PHASE_INPUTS_C4V001':
            return 'MALFORMED'
        if pi['phase_named'] not in (PHASE1, PHASE2):
            return 'MALFORMED'
        for k in ('phase1_registry_root', 'phase2_registry_root'):
            if not isinstance(pi[k], str) or not os.path.isabs(pi[k]):
                return 'MALFORMED'
        if pi['run_status'] not in cls.RUN_STATUS_PHASES:
            return 'MALFORMED'
        if pi['run_status_code'] is not None and not is_str(pi['run_status_code']):
            return 'MALFORMED'
        h = pi['phase1_header']
        if h is not None and (not isinstance(h, dict) or set(h) != {'b_p1', 'u_a_log_index', 'phase1_record_sha256',
                                                                     'l1_sha256'}
                              or not is_int(h['b_p1']) or not is_int(h['u_a_log_index'])
                              or not is_hex64(h['phase1_record_sha256']) or not is_hex64(h['l1_sha256'])):
            return 'MALFORMED'
        if pi['phase1_classification_absent_reason'] not in (None, 'AT0A_FAILURE', 'NO_PHASE_1_SCORE'):
            return 'MALFORMED'
        if pi['phase_named'] not in cls.RUN_STATUS_PHASES[pi['run_status']]:
            return 'RUN_STATUS_NOT_OF_PHASE'
        if pi['phase_named'] == PHASE1 and pi['run_status'] == 'SCORED' and h is None:
            return 'PHASE1_HEADER_MISSING'
        return None

    @classmethod
    def _phase_inputs_ok(cls, pi):
        return cls._phase_inputs_check(pi) is None

    def check_zone_table(self):
        """C-1.3 zone rule and membership by id; a mismatch stops (ZONE_TABLE_MISMATCH). R_q is bound by id to the
        slots query block (Rad_text, Rad_unit kpc; C-I3). INNER R < 10.0, TRANSITION 10.0 <= R < 30.0, OUTER R >= 30.0."""
        self.rad = {}
        sl = self.docs.get('slots')
        try:
            rows = sl['query_block']['rows']
            if not isinstance(rows, list) or len(rows) != 43:
                raise ValueError('query block is not 43 rows')
            for j, r in enumerate(rows):
                if not isinstance(r, dict) or r.get('query_id') != QIDS[j] or r.get('Rad_unit') != 'kpc' or \
                        not isinstance(r.get('Rad_text'), str):
                    raise ValueError('row %d id/unit/text' % j)
                R = float(r['Rad_text'])
                if not math.isfinite(R):
                    raise ValueError('row %d radius' % j)
                z = 'INNER' if R < 10.0 else 'TRANSITION' if R < 30.0 else 'OUTER'
                if z != ZONE_TABLE[QIDS[j]]:
                    raise ValueError('%s computes to %s, table says %s' % (QIDS[j], z, ZONE_TABLE[QIDS[j]]))
                self.rad[QIDS[j]] = (r['Rad_text'], R)
        except (TypeError, KeyError, ValueError) as exc:
            self.stop('ZONE_TABLE_MISMATCH', 'ALL', 'slots query block: %s' % exc)
            self.rad = {}

    def check_tsr(self):
        """C-1.1 TSR_FLAG_TABLE_MISMATCH and C-1.4: the freeze's pinned compare is 6f095f64; its failing
        TRUNCATION_SHAPE rings are exactly {ordinal 15}; its failing non-TRUNCATION_SHAPE rings are empty; the N1
        record is 8867c376; the GL-node record is ec1dcca5; the flag record's 43 flags are exactly {NGC3198-Q25}.
        The TSR support record (C-1.4 carrier; C-11 'a carrier that is a stop input') must be the one C-1.4 states.
        A defect in any of these carriers fires this stop (class: P10, R-TSR and the flag column only)."""
        self.compare_gate = None
        cmp_ = self.docs.get('ntest_compare')
        fr = self.docs.get('tsr_flag_record')
        sup = self.docs.get('tsr_support_record')
        man = self.docs.get('freeze_manifest')
        bad = []
        if self.b['inputs']['ntest_compare'] is None or self.b['inputs']['ntest_compare']['sha256'] != COMPARE_SHA:
            bad.append('the N-test compare is not 6f095f64')
        native = None
        if not isinstance(cmp_, dict):
            bad.append('compare unreadable (%s)' % self.load_err.get('ntest_compare'))
        else:
            self.compare_gate = cmp_.get('n_route_ab_gate')
            ts = cmp_.get('failing_TRUNCATION_SHAPE_rings')
            nts = cmp_.get('failing_non_TRUNCATION_SHAPE_rings')
            if cmp_.get('schema') != 'NGC_NTEST_COMPARE_C2V002' or not isinstance(ts, list) or \
                    not all(isinstance(x, dict) for x in ts):
                bad.append('compare schema or failing ring list')
            elif sorted(x.get('ordinal') for x in ts if is_int(x.get('ordinal'))) != [FAILING_RING_ORDINAL] or len(ts) != 1:
                bad.append('failing TRUNCATION_SHAPE rings are not exactly {ordinal 15}')
            else:
                native = ts[0]
            if nts != []:
                bad.append('failing non-TRUNCATION_SHAPE rings are not empty')
        pins = None
        try:
            pins = {p['sha256'] for p in man['pins']['input_files'] if isinstance(p, dict)}
        except (TypeError, KeyError):
            bad.append('manifest pins.input_files unreadable')
        if not isinstance(fr, dict) or fr.get('schema') != 'TSR_FLAG_RECORD_C4V001' or set(fr) != {
                'schema', 'target_free', 'rule', 'failing_ring_ordinal', 'ntest_compare_pin', 'n1_record_pin',
                'gl_node_record_pin', 'flags'}:
            bad.append('flag record missing or malformed (%s)' % self.load_err.get('tsr_flag_record'))
        else:
            want = {'ntest_compare_pin': COMPARE_SHA, 'n1_record_pin': N1_SHA, 'gl_node_record_pin': NODE_SHA}
            for k, sha in want.items():
                p = fr[k]
                if not self._pin_ok(p) or p['sha256'] != sha:
                    bad.append('flag record %s is not %s' % (k, sha[:8]))
                elif pins is not None and sha not in pins:
                    bad.append('%s not pinned among the freeze input files' % k)
            if pins is not None and self.b['inputs']['tsr_flag_record'] is not None and \
                    self.b['inputs']['tsr_flag_record']['sha256'] not in pins:
                bad.append('flag record not pinned among the freeze input files')
            if fr['target_free'] is not True or fr['failing_ring_ordinal'] != FAILING_RING_ORDINAL or \
                    not isinstance(fr['rule'], str):
                bad.append('flag record scope, rule or ring')
            fl = fr['flags']
            if not isinstance(fl, list) or len(fl) != 43 or any(
                    not isinstance(x, dict) or set(x) != {'query_id', 'TRUNCATION_SHAPE_RESIDUAL'} or
                    x['query_id'] != QIDS[j] or not isinstance(x['TRUNCATION_SHAPE_RESIDUAL'], bool)
                    for j, x in enumerate(fl)):
                bad.append('flag record flags are not 43 booleans in manifest order')
            elif sorted(x['query_id'] for x in fl if x['TRUNCATION_SHAPE_RESIDUAL']) != list(FLAGGED_IDS):
                bad.append('flag record flags are not exactly {NGC3198-Q25}')
        skeys = {'schema', 'mode', 'target_free', 'before_target_access', 'point_key', 'slots_pin',
                 'ntest_compare_pin', 'rule_id', 'rings'}
        if not isinstance(sup, dict) or sup.get('schema') != 'UNT_ROOT_TSR_SUPPORT_CX3V001' or set(sup) != skeys:
            bad.append('support record missing or malformed (%s)' % self.load_err.get('tsr_support_record'))
        else:
            rings = sup['rings']
            if sup['target_free'] is not True or sup['before_target_access'] is not True or \
                    not self._pin_ok(sup['ntest_compare_pin']) or sup['ntest_compare_pin']['sha256'] != COMPARE_SHA:
                bad.append('support record scope or compare pin')
            elif not isinstance(rings, list) or len(rings) != 1 or not isinstance(rings[0], dict) or \
                    set(rings[0]) != {'native_ring', 'lower_kpc', 'upper_kpc', 'lower_inclusive', 'upper_inclusive'}:
                bad.append('support record is not one ring entry')
            else:
                r = rings[0]
                if native is None or canonical(r['native_ring']) != canonical(native):
                    bad.append('support record native_ring is not the compare ordinal-15 record verbatim')
                if r['lower_kpc'] != SUPPORT_LOWER_KPC or r['upper_kpc'] != SUPPORT_UPPER_KPC or \
                        r['lower_inclusive'] is not False or r['upper_inclusive'] is not False:
                    bad.append('support record bounds are not (r_14, r_16) exclusive')
        for d in bad:
            self.stop('TSR_FLAG_TABLE_MISMATCH', 'TSR', d)

    def check_gate_list(self):
        """C-1.1 GATE_STATUS_LIST_DEFECT and C-4 (M-15): the list is missing, or a root-listed gate of the rosters is
        not on it. Gate identity is the gate document sha256 (v003g root_gates pins), compared in lower case: v003g
        accepts a root_gates pin in either case and compares it lower-cased, and writes the frozen registration in lower
        case (V-F1); the list's own gate_sha256 values are read the same way. Status ON-TIME or LATE."""
        self.gate_status = {}
        gl = self.docs.get('gate_status_list')
        ok = isinstance(gl, dict) and gl.get('schema') == 'GATE_STATUS_LIST_C4V001' and set(gl) == {'schema', 'gates'} \
            and isinstance(gl['gates'], list)
        if ok:
            seen = {}
            for g in gl['gates']:
                if not isinstance(g, dict) or set(g) != {'gate_sha256', 'status', 'pinned_by_entry'} or \
                        not is_hex64_ci(g['gate_sha256']) or g['status'] not in ('ON-TIME', 'LATE') or \
                        not is_str(g['pinned_by_entry']) or g['gate_sha256'].lower() in seen:
                    ok = False
                    break
                seen[g['gate_sha256'].lower()] = g['status']
            if ok:
                self.gate_status = seen
                self.gate_list_out = [dict(g) for g in gl['gates']]
        if not ok:
            self.gate_status = {}
            self.gate_list_out = na(['GATE_STATUS_LIST_DEFECT'])
            self.stop('GATE_STATUS_LIST_DEFECT', 'GATE', 'gate-status list missing or malformed (%s)'
                      % self.load_err.get('gate_status_list'))
        self.roster_gates = set()
        for name, (doc, err, _sha) in self.rosters.items():
            if not isinstance(doc, dict) or doc.get('schema') != 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001' or \
                    not isinstance(doc.get('root_gates'), list) or \
                    not all(self._pin_ok_ci(p) for p in doc['root_gates']):
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'roster %s missing or malformed (%s)' % (name, err))
                continue
            for p in doc['root_gates']:
                gsha = p['sha256'].lower()
                self.roster_gates.add(gsha)
                if ok and gsha not in self.gate_status:
                    self.stop('GATE_STATUS_LIST_DEFECT', 'GATE', 'root-listed gate %s of roster %s not on the list'
                              % (gsha[:12], name))
        names = set(self.rosters)
        if PRIMARY not in names:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'no PRIMARY roster supplied')

    # ------------------------------------------------------------ the score and the reference member (C-1.1, M-5)
    def check_score(self, score, manifest):
        """C-1.1 tier inputs and the M-5 field list; the stops REFERENCE_MEMBER_MISMATCH, the reference member's row
        status UNEVALUATED_OR_REFUSED, ids Q01-Q43 in order with no repeat, the envelope label prefix, and a field that
        is missing, of the wrong type or non-finite where a finite value is required (by map class)."""
        self.score_ok = False
        self.ref_rows_raw = None
        if not isinstance(score, dict):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'score output missing or malformed (%s)' % self.load_err.get('score'))
            return
        h = score.get('headline')
        members = score.get('members')
        if not isinstance(h, dict) or not is_str(h.get('reference_member_id')) or \
                not is_int(h.get('reference_member_log_index')):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'headline.reference_member_id / reference_member_log_index')
            return
        if not isinstance(members, list) or not all(isinstance(m, dict) and is_str(m.get('member_id')) and
                                                    is_int(m.get('log_index')) for m in members):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'members[].member_id / log_index')
            return
        ids = [m['member_id'] for m in members]
        if len(set(ids)) != len(ids):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'members[].member_id repeated')
            return
        ref = [m for m in members if m['member_id'] == h['reference_member_id']]
        if len(ref) != 1:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'reference member not among members[]')
            return
        ref = ref[0]
        if ref['log_index'] != h['reference_member_log_index']:
            self.stop('REFERENCE_MEMBER_MISMATCH', 'ALL', 'reference member log_index differs from the headline')
        mref = None
        try:
            mr = manifest['reference_member']
            if (h['reference_member_id'], h['reference_member_log_index']) != (mr['member_id'], mr['log_index']):
                self.stop('REFERENCE_MEMBER_MISMATCH', 'ALL', 'score names %s/%s; frozen manifest names %s/%s' % (
                    h['reference_member_id'], h['reference_member_log_index'], mr['member_id'], mr['log_index']))
            mref = [m for m in manifest['members'] if isinstance(m, dict) and m.get('member_id') == mr['member_id']]
            mref = mref[0] if len(mref) == 1 else None
            if mref is None:
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'manifest reference member not unique among manifest members')
        except (TypeError, KeyError):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'manifest reference_member / members unreadable')
        if not isinstance(ref.get('member_valid'), bool):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'reference member member_valid')
        self.ref_member = ref
        self.mref = mref
        rows = ref.get('rows')
        if not isinstance(rows, list) or len(rows) != 43 or not all(isinstance(r, dict) for r in rows) or \
                [r.get('id') for r in rows] != list(QIDS):
            self.stop('QUERY_ID_DEFECT', 'ALL', 'reference member ids are not NGC3198-Q01..Q43 in order without repeat')
            return
        self.ref_rows_raw = rows
        fs = score.get('freeze_status')
        ir = score.get('incomplete_reasons')
        if fs not in ('FREEZE_COMPLETE', 'FREEZE_INCOMPLETE') or not isinstance(ir, list) or \
                not all(isinstance(x, str) for x in ir):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'freeze_status / incomplete_reasons')
        self.score_ok = True

    def check_envelope(self, score):
        """C-1.1 NEAR inputs: pointwise_envelope.label (prefix) and rows[].{valid, band_overlaps_error_bar}. A label that
        differs stops (ENVELOPE_LABEL_MISMATCH); a row field defect blanks NEAR and N(Z) on the rows concerned, only
        where the row is tier-MISS (basis row T3; score_output)."""
        self.env = {}
        pe = score.get('pointwise_envelope') if isinstance(score, dict) else None
        if not isinstance(pe, dict) or not isinstance(pe.get('label'), str) or \
                not pe['label'].startswith(ENVELOPE_PREFIX):
            self.stop('ENVELOPE_LABEL_MISMATCH', 'ALL', 'pointwise_envelope.label prefix differs or is missing')
        rows = pe.get('rows') if isinstance(pe, dict) else None
        if not isinstance(rows, list) or len(rows) != 43:
            self.stop('FIELD_DEFECT_ENVELOPE', 'ENVELOPE', 'pointwise_envelope.rows is not 43 rows', rows=QIDS)
            return
        for j, r in enumerate(rows):
            q = QIDS[j]
            if not isinstance(r, dict) or r.get('id') != q or not isinstance(r.get('valid'), bool) or \
                    not isinstance(r.get('band_overlaps_error_bar'), bool):
                self.stop('FIELD_DEFECT_ENVELOPE', 'ENVELOPE', '%s envelope row field' % q, rows=(q,))
                continue
            self.env[q] = (r['valid'], r['band_overlaps_error_bar'])

    def check_sensitivity(self, score):
        """C-1.1 sensitivity column (Phase 2): sensitivity.rows[].{valid, band_overlaps_error_bar}; a defect blanks only
        the sensitivity column on the rows concerned. Phase 1: every row reads invalid (C-I4), and nothing is checked."""
        self.sens = {}
        if self.phase == PHASE1:
            return
        se = score.get('sensitivity') if isinstance(score, dict) else None
        rows = se.get('rows') if isinstance(se, dict) else None
        if not isinstance(rows, list) or len(rows) != 43:
            self.stop('FIELD_DEFECT_SENSITIVITY', 'SENSITIVITY', 'sensitivity.rows is not 43 rows', rows=QIDS)
            return
        for j, r in enumerate(rows):
            q = QIDS[j]
            if not isinstance(r, dict) or r.get('id') != q or not isinstance(r.get('valid'), bool) or \
                    not isinstance(r.get('band_overlaps_error_bar'), bool):
                self.stop('FIELD_DEFECT_SENSITIVITY', 'SENSITIVITY', '%s sensitivity row field' % q, rows=(q,))
                continue
            self.sens[q] = (r['valid'], r['band_overlaps_error_bar'])

    def _frozen_registration(self, member, j):
        """The frozen manifest registration of a member's row j (v003g row_registration): None for a valid row;
        ('BUILTIN', reason) or ('GATE', reason, gate_sha in lower case; V-F1, v003g _is_hex64); 'BAD' when malformed."""
        try:
            reg = member['row_registration'][j]
        except (TypeError, KeyError, IndexError):
            return 'BAD'
        if reg is None:
            return None
        if not isinstance(reg, dict) or set(reg) != {'status', 'reason', 'registration'} or reg['status'] != 'INVALID' \
                or not is_str(reg['reason']):
            return 'BAD'
        if reg['reason'] in BUILTIN_REASONS:
            return ('BUILTIN', reg['reason']) if reg['registration'] is None else 'BAD'
        g = reg['registration']
        if not isinstance(g, dict) or not is_hex64_ci(g.get('sha256')):
            return 'BAD'
        return ('GATE', reg['reason'], g['sha256'].lower())

    def _kinds_of_registration(self, fr):
        """Kinds an INVALID registration can take for the counts: built-in or ON-TIME gate -> INVALID; LATE gate ->
        LATE-gate MISS (C-4); a gate missing from the list -> both (C-1.1 GATE_STATUS_LIST_DEFECT row rule)."""
        if fr is None:
            return set()
        if fr == 'BAD':
            return {'I', 'L'}
        if fr[0] == 'BUILTIN':
            return {'I'}
        st = self.gate_status.get(fr[2])
        return {'I'} if st == 'ON-TIME' else {'L'} if st == 'LATE' else {'I', 'L'}

    def build_rows(self, raw_rows, member_frozen, twin=False):
        """C-1.1 rule M-T per row: INVALID_AS_MISS if score_status = INVALID_AS_MISS; HIT if within_error = true
        (|r| <= 1, r = sigma_ratio); MISS otherwise. C-4: a LATE root-listed gate's row is, for counts and patterns, a
        non-INVALID MISS with no defined ratio. C-1.1 'A row with no ratio': VALID with sigma_ratio null is a MISS with
        sign UNDEFINED. Returns (rows, problems); problems are (qid, detail, class) with class ROW or GATE."""
        out, problems = [], []
        for j, r in enumerate(raw_rows):
            q = QIDS[j] if not twin else r.get('id')
            row = {'id': q, 'zone': ZONE_TABLE.get(q), 'kind': None, 'r': None, 'reason': None, 'gate_sha': None,
                   'gate_status': None, 'allowed': set(), 'flagged': (q in FLAGGED_IDS) and not twin, 'raw': r}
            fr = self._frozen_registration(member_frozen, j) if member_frozen is not None else 'BAD'
            errs = []
            st, we, sr, rr, status = (r.get('score_status'), r.get('within_error'), r.get('sigma_ratio'),
                                      r.get('registered_reason'), r.get('status'))
            for k in ('score_status', 'within_error', 'sigma_ratio', 'registered_reason', 'status'):
                if k not in r:
                    errs.append('%s missing' % k)
            if st not in ('HIT', 'MISS', 'INVALID_AS_MISS'):
                errs.append('score_status wrong type')
            if not isinstance(we, bool):
                errs.append('within_error wrong type')
            if sr is not None and not is_num(sr):
                errs.append('sigma_ratio wrong type or non-finite')
            if rr is not None and not is_str(rr):
                errs.append('registered_reason wrong type')
            if status not in ('VALID', 'INVALID', 'UNEVALUATED_OR_REFUSED'):
                errs.append('status wrong type')
            if not errs:
                if st == 'INVALID_AS_MISS':
                    if not is_str(rr):
                        errs.append('registered_reason missing on an INVALID_AS_MISS row')
                elif we is True and sr is None:
                    errs.append('sigma_ratio null on a within-error row (finite value required)')
            if errs:
                row['allowed'] = {'H', 'MS', 'MN'} | self._kinds_of_registration(fr)
                problems.append((q, '; '.join(errs), 'ROW'))
                out.append(row)
                continue
            if st == 'INVALID_AS_MISS':
                row['reason'] = rr
                if rr in BUILTIN_REASONS:
                    row['kind'] = 'I'
                else:
                    if fr == 'BAD' or fr is None or fr[0] != 'GATE' or fr[1] != rr:
                        row['allowed'] = {'H', 'MS', 'MN', 'I', 'L'}
                        problems.append((q, 'gate registration of an INVALID_AS_MISS row not readable from the frozen '
                                            'manifest', 'ROW'))
                        out.append(row)
                        continue
                    row['gate_sha'] = fr[2]
                    gs = self.gate_status.get(fr[2])
                    row['gate_status'] = gs
                    if gs == 'ON-TIME':
                        row['kind'] = 'I'
                    elif gs == 'LATE':
                        row['kind'] = 'L'
                    else:
                        row['allowed'] = {'I', 'L'}
                        problems.append((q, 'gate %s of this INVALID row is not on the gate-status list' % fr[2][:12],
                                         'GATE'))
            elif we is True:
                row['kind'], row['r'] = 'H', sr
            elif sr is None:
                row['kind'] = 'MN'
            else:
                row['kind'], row['r'] = 'MS', sr
            out.append(row)
        return out, problems

    # ================================================================ the zone engine (C-2), with the C-1.1 row map
    def zone_vectors(self, rows):
        """All count vectors (H, MS, MN, I, L) reachable when each defective row takes any allowed kind (C-1.1 map)."""
        vecs = {(0, 0, 0, 0, 0)}
        for row in rows:
            ks = [row['kind']] if row['kind'] else sorted(row['allowed'])
            nv = set()
            for v in vecs:
                for k in ks:
                    w = list(v)
                    w[KIND_IX[k]] += 1
                    nv.add(tuple(w))
            vecs = nv
        return vecs

    @staticmethod
    def vec_counts(v):
        """C-2 counts: N_v non-INVALID; H; M (null-ratio and LATE rows included); U = null-ratio + LATE; I."""
        h, ms, mn, i, l = v
        nv = h + ms + mn + l
        m = ms + mn + l
        u = mn + l
        missdom = nv >= 1 and 2 * m >= nv              # C-2 miss-dominated (tie to miss)
        hitdom = nv >= 1 and 2 * h > nv                # C-2 hit-dominated (strict)
        s_undef = (h + ms == 0) or (missdom and 2 * (m - u) < nv)   # C-2 sign class UNDEFINED test
        return {'Nv': nv, 'H': h, 'M': m, 'U': u, 'I': i, 'missdom': missdom, 'hitdom': hitdom, 's_undef': s_undef,
                'pred_miss': ms + mn, 'n_def': h + ms, 'n_null': mn, 'n_late': l}

    def engine(self, rows, codes_d, twin=False):
        """C-2 per-zone summaries, outer trend, OUTER_FAILURE, patterns P0-P15 with P1g/P11g, MINORITY_MISS (C-3),
        and the E3 line (C-5.3), evaluated under the C-1.1 stop-to-output map for the defective rows (rows whose kind is
        None): count-level outputs print iff they take one value over every assignment of an allowed kind; every other
        output computed from a defective row reads NOT_AVAILABLE unless a listed deduction fixes it."""
        Z = {z: [r for r in rows if r['zone'] == z] for z in ZONES}
        hasD = {z: any(r['kind'] is None for r in Z[z]) for z in ZONES}
        vecs = {z: self.zone_vectors(Z[z]) for z in ZONES}
        cnt = {z: [self.vec_counts(v) for v in vecs[z]] for z in ZONES}

        def uniq(vals):
            s = set(vals)
            return s.pop() if len(s) == 1 else None

        res = {'zones': {}, 'hasD': hasD}
        cl = {}      # count-level per zone (None = not printable)
        for z in ZONES:
            c = cnt[z]
            cl[z] = {k: uniq(x[k] for x in c) for k in ('Nv', 'H', 'M', 'U', 'I', 'missdom', 'hitdom', 's_undef',
                                                         'n_def', 'n_null', 'n_late')}
        # m(Z), S(Z): from fixed rows only when the zone has no defective row
        mz, sz = {}, {}
        for z in ZONES:
            if hasD[z]:
                mz[z] = sz[z] = None
                continue
            c = cnt[z][0]
            vals = [r['r'] for r in Z[z] if r['kind'] in ('H', 'MS')]
            m = median(vals)
            mz[z] = 'UNDEFINED' if m is None else m
            if m is None or (c['missdom'] and 2 * (c['M'] - c['U']) < c['Nv']):
                sz[z] = 'UNDEFINED'
            elif m < -1:
                sz[z] = 'DEFICIT'
            elif m > 1:
                sz[z] = 'EXCESS'
            else:
                sz[z] = 'CENTERED'
        res['m'], res['S'], res['cl'] = mz, sz, cl
        # outer trend (C-2): defined-ratio OUTER rows sorted by R_q; odd middle to the far half
        trendD = hasD['TRANSITION'] or hasD['OUTER']
        if trendD:
            delta = far = None
            growing = crossing = None
        else:
            orows = sorted([r for r in Z['OUTER'] if r['kind'] in ('H', 'MS')], key=lambda r: self.rad[r['id']][1])
            d = [r['r'] for r in orows]
            n = len(d)
            if n < 2:
                delta, far = 'UNDEFINED', 'UNDEFINED'
            else:
                fm = median(d[n // 2:])
                delta, far = fm - median(d[:n // 2]), fm
            mt, mo = mz['TRANSITION'], mz['OUTER']
            tgt = (not isinstance(mt, str)) and (not isinstance(mo, str)) and mt > mo
            dneg = not isinstance(delta, str) and delta < 0
            growing = sz['OUTER'] == 'DEFICIT' and dneg and tgt
            crossing = sz['OUTER'] == 'CENTERED' and dneg and tgt and not isinstance(far, str) and far < -1
        if trendD and cl['OUTER']['s_undef'] is True:      # C-1.1 deduction
            growing = crossing = False
        res['delta'], res['far'], res['growing'], res['crossing'] = delta, far, growing, crossing
        P = {}
        # signed zone patterns with the C-1.1 deductions
        for z, sig in (('OUTER', (('P1', 'DEFICIT'), ('P2', 'EXCESS'), ('P11', 'CENTERED'))),
                       ('INNER', (('P4', 'DEFICIT'), ('P3', 'EXCESS'), ('P12', 'CENTERED')))):
            for pid, cls_ in sig:
                if hasD[z]:
                    P[pid] = False if (cl[z]['missdom'] is False or cl[z]['s_undef'] is True) else None
                else:
                    P[pid] = cnt[z][0]['missdom'] and sz[z] == cls_
        P['P13'] = cl['TRANSITION']['missdom']
        P['P14'] = uniq(x['missdom'] and x['s_undef'] for x in cnt['OUTER'])
        P['P15'] = uniq(x['missdom'] and x['s_undef'] for x in cnt['INNER'])
        # P1g / P11g: flags of P1 / P11
        if P['P1'] is False:
            P['P1g'] = False if not trendD or cl['OUTER']['s_undef'] is True else None
        else:
            P['P1g'] = None if (P['P1'] is None or growing is None) else (P['P1'] and growing)
        if trendD and cl['OUTER']['s_undef'] is True:
            P['P1g'] = False
        if P['P11'] is False:
            P['P11g'] = False if not trendD or cl['OUTER']['s_undef'] is True else None
        else:
            P['P11g'] = None if (P['P11'] is None or crossing is None) else (P['P11'] and crossing)
        if trendD and cl['OUTER']['s_undef'] is True:
            P['P11g'] = False
        # P6 (C-2): every class defined, all equal, not CENTERED; false when any 'S(Z) is UNDEFINED' prints true
        if any(hasD.values()):
            P['P6'] = False if any(cl[z]['s_undef'] is True for z in ZONES) else None
        else:
            ss = [sz[z] for z in ZONES]
            P['P6'] = all(s != 'UNDEFINED' for s in ss) and len(set(ss)) == 1 and ss[0] != 'CENTERED'
        # cross-zone count-level outputs: product of per-zone feature sets
        feats = {z: {(x['Nv'] >= 1, x['M'] >= 1, x['missdom'], x['hitdom'], x['pred_miss'] >= 1, x['I'] > 0)
                     for x in cnt[z]} for z in ZONES}
        vals = {k: set() for k in ('P0', 'P5', 'P7', 'P8', 'MM:INNER', 'MM:TRANSITION', 'MM:OUTER')}
        for fi in feats['INNER']:
            for ft in feats['TRANSITION']:
                for fo in feats['OUTER']:
                    f = {'INNER': fi, 'TRANSITION': ft, 'OUTER': fo}
                    anymd = any(f[z][2] for z in ZONES)
                    vals['P0'].add(any(f[z][5] for z in ZONES))
                    vals['P5'].add(fi[3] and fo[2] and ft[0] and not ft[3])
                    vals['P7'].add(any(f[z][1] for z in ZONES) and not anymd)
                    vals['P8'].add(any(f[z][0] for z in ZONES) and not any(f[z][1] for z in ZONES))
                    for z in ZONES:
                        vals['MM:' + z].add(anymd and not f[z][2] and f[z][4])
        for k, v in vals.items():
            P[k] = v.pop() if len(v) == 1 else None
        P['P9'] = uniq(x['Nv'] == 0 for x in cnt['OUTER'])
        # P10 (C-2): a non-INVALID MISS row with a frozen prediction carries the flag; never for an alternative
        if twin:
            P['P10'] = 'NOT_EVALUATED_FOR_ALTERNATIVE'
        else:
            pv = set()
            fl = [r for r in rows if r['flagged']]
            opts = [[r['kind']] if r['kind'] else sorted(r['allowed']) for r in fl]
            if not fl:
                pv.add(False)
            else:
                for combo in itertools.product(*opts):
                    pv.add(any(k in ('MS', 'MN') for k in combo))
            P['P10'] = pv.pop() if len(pv) == 1 else None
        res['OF'] = cl['OUTER']['missdom']
        e3 = set()
        for x in cnt['OUTER']:     # C-5.3 values; the first carries its scope (C-8 words rule; V-F2)
            e3.add(E3_NEGATIVE if x['missdom'] else 'NOT_NEGATIVE_AT_OUTER' if x['Nv'] >= 1 else 'NOT_TESTABLE')
        res['E3'] = e3.pop() if len(e3) == 1 else None
        res['ONM'] = uniq(x['Nv'] >= 1 and x['M'] == 0 for x in cnt['OUTER'])     # C-5.2 OUTER_NO_MISS
        res['P'] = P
        # onset radius (C-3 descriptive): smallest R_q of a MISS row in TRANSITION u OUTER (LATE rows count as MISS)
        tro = sorted([r for r in rows if r['zone'] in ('TRANSITION', 'OUTER')], key=lambda r: self.rad[r['id']][1])
        poss, reach = set(), True
        for r in tro:
            ks = [r['kind']] if r['kind'] else sorted(r['allowed'])
            can_miss = any(k in ('MS', 'MN', 'L') for k in ks)
            can_not = any(k in ('H', 'I') for k in ks)
            if can_miss and reach:
                poss.add(r['id'])
            if not can_not:
                reach = False
                break
        if reach:
            poss.add(None)
        res['onset'] = poss.pop() if len(poss) == 1 else 'NA'
        # I per reason per zone: printed unless a defective row of the zone can be INVALID with that reason
        ipr = {}
        for z in ZONES:
            d, nar = {}, set()
            for r in Z[z]:
                if r['kind'] == 'I':
                    d[r['reason']] = d.get(r['reason'], 0) + 1
                elif r['kind'] is None and 'I' in r['allowed']:
                    fr = r.get('_fr_reason')
                    nar.add(fr if fr else '*')
            ipr[z] = (d, nar)
        res['ipr'] = ipr
        res['Z'] = Z
        return res

    # ------------------------------------------------------------ output helpers
    def o3(self, v, codes):
        return na(codes) if v is None else v

    def zone_out(self, res, z, codes_d, ncodes, nval, twin=False):
        """C-2 'Also reported for each zone': the counts (U included), m(Z), S(Z), N(Z), I per reason."""
        cl = res['cl'][z]
        d, nar = res['ipr'][z]
        if '*' in nar:
            ipr = na(codes_d)
        else:
            ipr = {k: (na(codes_d) if k in nar else v) for k, v in sorted(d.items())}
            for k in nar:
                ipr[k] = na(codes_d)
        o = {'N_v': self.o3(cl['Nv'], codes_d), 'H': self.o3(cl['H'], codes_d), 'M': self.o3(cl['M'], codes_d),
             'U': self.o3(cl['U'], codes_d), 'I': self.o3(cl['I'], codes_d), 'I_per_reason': ipr,
             'miss_dominated': self.o3(cl['missdom'], codes_d), 'hit_dominated': self.o3(cl['hitdom'], codes_d),
             'S_is_UNDEFINED': self.o3(cl['s_undef'], codes_d),
             'm': self.o3(res['m'][z], codes_d), 'S': self.o3(res['S'][z], codes_d),
             'N': 0 if twin else (na(ncodes) if nval is None else nval)}
        return o

    # ================================================================ readings (C-3, C-3.2)
    def readings(self, res, rows, codes_d, s0g_state, s0g_codes, labels, tsr_blank):
        """C-3: every registered reading, every time, in C-3.2 order, as the tuple (score relation, deciding-test
        status, prior evidence). Part 1 order: NOT_ADDRESSED (PATTERN_NOT_HELD) when no trigger holds; INCONSISTENT when
        an against-condition holds (R-DRIFT: DT-S0G AGAINST, C-6.3); NOT_ADDRESSED with a sign-scope code for the
        deficit-type readings (C-3.2 sign rule); CONSISTENT otherwise. Under the C-1.1 map, each part prints when the
        printed outputs fix it, else NOT_AVAILABLE."""
        P = dict(res['P'])
        P['OF'] = res['OF']
        S_o = res['S']['OUTER']
        su_o = res['cl']['OUTER']['s_undef']
        out = []
        for R in READINGS:
            entry = {'reading': R, 'labels': labels}
            if R == 'R-TSR' and tsr_blank:
                out.append(dict(entry, **{'NOT_AVAILABLE': tsr_blank}))
                continue
            tv = [(t, P[t]) for t in TRIGGERS[R]]
            if any(v is True for _, v in tv):
                held = True
            elif all(v is False for _, v in tv):
                held = False
            else:
                held = None
            entry['triggers_holding'] = [{'trigger': t, 'holds': True if v is True else na(codes_d)}
                                         for t, v in tv if v is not False]
            p1, code = None, None
            if held is False:
                p1, code = 'NOT_ADDRESSED', 'PATTERN_NOT_HELD'
            elif held is True:
                against = False
                if R == 'R-DRIFT':
                    against = None if s0g_state is None else (s0g_state == 'AGAINST')
                if against is True:
                    p1 = 'INCONSISTENT'
                elif against is None:
                    p1 = None
                elif R in DEFICIT_TYPE:
                    # CONSISTENT iff S(OUTER) in {DEFICIT, CENTERED} and an OUTER MISS row has s = -1
                    if S_o is not None:
                        s_in = S_o in ('DEFICIT', 'CENTERED')
                    elif su_o is True:
                        s_in = False
                    else:
                        s_in = None
                    neg_fixed = any(r['kind'] == 'MS' and r['r'] < 0 for r in res['Z']['OUTER'])
                    neg_maybe = any(r['kind'] is None and 'MS' in r['allowed'] for r in res['Z']['OUTER'])
                    neg = True if neg_fixed else (None if neg_maybe else False)
                    cond = False if (s_in is False or neg is False) else (True if (s_in and neg) else None)
                    if cond is True:
                        p1 = 'CONSISTENT'
                    elif cond is None:
                        p1 = None
                    else:
                        if P['P2'] is True:
                            p1, code = 'NOT_ADDRESSED', 'SIGN_SCOPE_EXCESS'
                        elif P['P14'] is True:
                            p1, code = 'NOT_ADDRESSED', 'SIGN_SCOPE_UNSIGNED'
                        elif P['P11'] is True and neg is False:
                            p1, code = 'NOT_ADDRESSED', 'SIGN_SCOPE_NO_DEFICIT_MISS'
                        else:
                            p1 = None
                else:
                    p1 = 'CONSISTENT'
            entry['part1'] = {'relation': p1, 'code': code} if p1 is not None else \
                na(sorted(set(codes_d) | (set(s0g_codes) if R == 'R-DRIFT' else set())))
            # part 2
            if R == 'R-MF':
                entry['part2'] = {'status': res['E3'], 'test': 'E3_VERDICT_LINE'} if res['E3'] is not None else na(codes_d)
            elif R == 'R-DRIFT':
                entry['part2'] = self.drift_part2(s0g_state, s0g_codes)
            else:
                t, st = DECIDING[R]
                entry['part2'] = {'status': 'OPEN', 'test': t, 'test_status': st}
            entry['part3_prior_evidence'] = PRIOR[R]
            entry['sign_scope'] = SIGN_SCOPE.get(R, '-')
            if R == 'R-HIST':
                g = [P.get('P1g'), P.get('P11g')]
                entry['qualifier_missing_long_range_component'] = True if True in g else (
                    False if all(x is False for x in g) else na(codes_d))
            # row scope (C-3 'Scope'): MISS rows with a frozen prediction in the zones the holding triggers name
            cited, maybe = set(), set()
            for t, v in tv:
                if v is False:
                    continue
                sc = TRIGGER_SCOPE[t]
                for r in rows:
                    if sc == 'ALL' or r['zone'] == sc or (sc == 'FLAGGED' and r['flagged']):
                        if sc == 'FLAGGED' and not r['flagged']:
                            continue
                        c = (True if r['kind'] in ('MS', 'MN') else False) if r['kind'] else (
                            None if (r['allowed'] & {'MS', 'MN'}) else False)
                        if c is False:
                            continue
                        if c is True and v is True:
                            cited.add(r['id'])
                        else:
                            maybe.add(r['id'])
            entry["scope_zones"] = sorted({TRIGGER_SCOPE[t] for t, v in tv if v is not False})
            entry["cited_miss_rows"] = sorted(cited)
            entry['cited_miss_rows_not_available'] = sorted(maybe - cited)
            out.append(entry)
        return out

    @staticmethod
    def drift_part2(state, codes):
        """C-6.3 closed mapping, part 2 (the last column)."""
        if state is None:
            return na(codes)
        if state == 'CONSISTENT':
            return {'status': 'CONSISTENT', 'test': 'DT-S0G'}
        if state == 'AGAINST':
            return {'status': 'AGAINST', 'test': 'DT-S0G'}
        return {'status': 'OPEN', 'test': 'DT-S0G', 'code': state, 'reasons': list(codes)}

    # ================================================================ alternatives (C-6.1, C-6.2, C-6.3)
    def twin_rows(self, alt, ref_li, scope_ids):
        """C-6.1 twin rule: the alternative's member with the reference member's log_index; valid iff member_valid; ids
        must equal the scope (Q01-Q43, or STAGE0 scoring_scope.query_ids). Returns (state, member, rows) where state is
        None (classified), TWIN_INVALID or TWIN_INPUT_DEFECT."""
        mem = alt.get('members')
        if not isinstance(mem, list) or not all(isinstance(m, dict) and is_int(m.get('log_index')) for m in mem):
            return 'TWIN_INPUT_DEFECT', None, None, 'members field'
        tw = [m for m in mem if m['log_index'] == ref_li]
        if len(tw) != 1:
            return 'TWIN_INPUT_DEFECT', None, None, 'no unique twin with the reference log_index'
        tw = tw[0]
        if not isinstance(tw.get('member_valid'), bool):
            return 'TWIN_INPUT_DEFECT', None, None, 'twin member_valid'
        if tw['member_valid'] is not True:
            return 'TWIN_INVALID', tw, None, None
        rows = tw.get('rows')
        if not isinstance(rows, list) or [r.get('id') if isinstance(r, dict) else None for r in rows] != list(scope_ids):
            return 'TWIN_INPUT_DEFECT', tw, None, 'twin ids differ from its scope'
        frozen = None
        try:
            am = self.docs['freeze_manifest']['alternative_results'][alt['name']]['members']
            fz = [m for m in am if isinstance(m, dict) and m.get('log_index') == ref_li]
            frozen = fz[0] if len(fz) == 1 else None
        except (TypeError, KeyError):
            frozen = None
        if frozen is not None and scope_ids != QIDS:
            # STAGE0 frozen arrays are full 43-row arrays; narrow them to the scored rows
            try:
                idx = [QIDS.index(q) for q in scope_ids]
                frozen = {'row_registration': [frozen['row_registration'][i] for i in idx]}
            except (TypeError, KeyError, IndexError, ValueError):
                frozen = None
        built, problems = self.build_rows(rows, frozen, twin=True)
        if problems:
            return 'TWIN_INPUT_DEFECT', tw, None, '; '.join('%s: %s' % (q, d) for q, d, _c in problems)
        return None, tw, built, None

    def classify_twin(self, alt, rows, labels):
        """C-6.1: a valid twin's rows tiered by M-T with its own INVALID set and the C-4 LATE rule; summaries and
        patterns by the C-2 rules with N(Z) = 0 and no P10."""
        res = self.engine(rows, [], twin=True)
        return {'rows': [self.twin_row_out(r) for r in rows],
                'zones': {z: dict(self.zone_out(res, z, [], [], 0, twin=True), labels=labels) for z in ZONES},
                'outer_trend': {'delta_out': res['delta'], 'far_half_median': res['far'],
                                'GROWING': res['growing'], 'CROSSING': res['crossing']},
                'outer_failure': res['OF'],
                'patterns': dict({p: res['P'][p] for p in PATTERN_IDS}, labels=labels),
                'patterns_holding': [p for p in PATTERN_IDS if res['P'][p] is True]}, res

    def twin_row_out(self, r):
        k = r['kind']
        return {'id': r['id'], 'zone': r['zone'], 'tier': 'INVALID_AS_MISS' if k in ('I', 'L') else
                'HIT' if k == 'H' else 'MISS', 'reading_kind': KIND_NAME[k], 'r_q': r['r'],
                'sign': self.sign_of(r), 'invalid_reason': r['reason'],
                'gate_after_predictions': k == 'L'}

    @staticmethod
    def sign_of(r):
        """C-1.2: s = sign(r) in {-1, 0, +1}; UNDEFINED for a null ratio; INVALID and LATE-gate rows carry no sign."""
        k = r['kind']
        if k in ('I', 'L'):
            return 'NONE'
        if k == 'MN':
            return 'UNDEFINED'
        return -1 if r['r'] < 0 else (1 if r['r'] > 0 else 0)

    def stage0_status(self):
        """C-6.3 receipt rule (M-14) for Phase 2: EVALUATED_BEFORE_FREEZE iff (a) every registered STAGE0 member's
        terminal receipt is FINISHED and (b) the successor is pinned in the seal entry, and the successor refuses no
        record (else EVALUATED_REFUSED); otherwise NOT_EVALUATED_BEFORE_FREEZE with every reason that applies
        (STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR; RECEIPTS_AFTER_STEP4: EXPLORATORY post-score, R-DRIFT OPEN).
        A receipt written at the recorded step-4 start counts as before. Phase 1: NOT_EVALUATED_BEFORE_FREEZE with
        NOT_IN_PHASE_1.
        Where the facts come from (A154; M-5 addition 2): in a Phase 2 that the seal runs under the STAGE0 successor
        (successor_mode), from the frozen manifest's stage0_status block in the successor's own schema (d260ee30); it is
        bound only to that sha (STAGE0_SUCCESSOR_SHA; any other pin: the block is not bound); root's separate record,
        if supplied, must be the exact projection of the block. Otherwise (Phase 2 under v003g), from root's STAGE0
        status record (STAGE0_STATUS_RECORD_C4V003), whose contract is an exact projection of the block's fields; there
        (b) fails by construction. A defect in either is a field of the STAGE0 alternative (C-1.1 map, F8):
        TWIN_INPUT_DEFECT. Returns (printed status, class) where class is None (Phase 1), EVALUATED, EVALUATED_REFUSED,
        NOT_EVALUATED_BEFORE_FREEZE or TWIN_INPUT_DEFECT; self.s0_defect holds the defect word and source."""
        self.s0_defect = None
        if self.phase == PHASE1:
            return {'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'reasons': ['NOT_IN_PHASE_1']}, None
        if self.successor_mode():
            try:
                facts = self._stage0_block_facts()
            except ValueError as exc:
                self.s0_defect = (STAGE0_SOURCE_BLOCK, str(exc))
                return {'status': NA_KEY, 'reasons': ['STAGE0_STATUS_BLOCK_DEFECT'], 'source': STAGE0_SOURCE_BLOCK,
                        'defect': str(exc)}, 'TWIN_INPUT_DEFECT'
            source = STAGE0_SOURCE_BLOCK
        else:
            rec = self.docs.get('stage0_status')
            try:
                if not isinstance(rec, dict) or rec.get('schema') != STAGE0_RECORD_SCHEMA or \
                        set(rec) != set(STAGE0_PROJ_KEYS) | {'schema'}:
                    raise ValueError('RECORD_KEYS')
                facts = self._stage0_facts(rec, STAGE0_PROJ_MEMBER_KEYS, successor=False)
            except ValueError as exc:
                self.s0_defect = (STAGE0_SOURCE_RECORD, str(exc))
                return {'status': NA_KEY, 'reasons': ['STAGE0_STATUS_RECORD_DEFECT']}, 'TWIN_INPUT_DEFECT'
            source = STAGE0_SOURCE_RECORD
        reading = facts['reading']
        info = {'status': reading, 'reasons': list(facts['reasons']), 'source': source,
                'phase2_step4_start_utc': facts['step4_start_utc'],
                'receipt_times_utc': [m['written_utc'] for m in facts['members']],
                'post_score_exploratory': facts['post_score_exploratory']}
        cls_ = {S0_EVALUATED: 'EVALUATED', S0_REFUSED: 'EVALUATED_REFUSED', S0_NOT_EVALUATED: S0_NOT_EVALUATED}[reading]
        return info, cls_

    def _stage0_block_facts(self):
        """Successor mode (A154): the frozen manifest's stage0_status block, read in the successor's schema (its
        _stage0_block / _stage0_receipt_verdict, d260ee30 L3820-3876). Binding: the sealed successor sha is d260ee30
        and the manifest's schema is the successor's; the block has exactly STAGE0_BLOCK_KEYS, its member rows exactly
        STAGE0_MEMBER_KEYS; its module is the successor's MODULE_NAME and its successor_module_sha256 is the sealed sha
        (the module writes the sha of its own bytes); its members are the frozen PRIMARY members in order (M-14 ruling:
        one STAGE0 call per PRIMARY member; _stage0_members_of). The facts must satisfy the receipt rule
        (_stage0_facts). Root's separate STAGE0 status record, when supplied, must be the block's exact projection.
        A168 V-N1 (c4v004): a block on the module's exception path (_stage0_exception_path) keeps every check above
        and is read by _stage0_facts at the module's own reading on that path; a block that claims the path but is not
        in the module's form is a defect (BLOCK_EXCEPTION_PATH).
        Raises ValueError(word) on any defect."""
        pin = self.b['sealed']['stage0_successor']
        if pin['sha256'] != STAGE0_SUCCESSOR_SHA:
            raise ValueError('STAGE0_SUCCESSOR_PIN_NOT_BOUND')
        man = self.docs.get('freeze_manifest')
        if not isinstance(man, dict) or man.get('schema') != MANIFEST_SCHEMA_SUCCESSOR:
            raise ValueError('MANIFEST_SCHEMA_NOT_SUCCESSOR')
        blk = man.get('stage0_status')
        if not isinstance(blk, dict) or set(blk) != STAGE0_BLOCK_KEYS:
            raise ValueError('BLOCK_KEYS')
        if blk['alternative'] != 'STAGE0_GRID_OUTER' or blk['module'] != STAGE0_SUCCESSOR_MODULE or \
                not isinstance(blk['rule'], str):
            raise ValueError('BLOCK_MODULE')
        if blk['successor_module_sha256'] != pin['sha256']:
            raise ValueError('BLOCK_SUCCESSOR_SHA')
        sr = blk['status_record']
        if not isinstance(blk['status_record_custody_ok'], bool) or not (
                sr is None or (isinstance(sr, dict) and set(sr) == {'path', 'sha256'} and isinstance(sr['path'], str)
                               and is_hex64(sr['sha256']))) or (blk['status_record_custody_ok'] and sr is None):
            raise ValueError('BLOCK_STATUS_RECORD')
        if not isinstance(blk['diagnostics'], list) or not all(is_str(x) for x in blk['diagnostics']):
            raise ValueError('BLOCK_DIAGNOSTICS')
        exception_path = self._stage0_exception_path(blk)
        facts = self._stage0_facts(blk, tuple(STAGE0_MEMBER_KEYS), successor=True, exception_path=exception_path)
        for m in blk['members']:
            rc = m['receipt']
            if not is_str(m['member_id']) or not isinstance(m['custody_ok'], bool) or \
                    not isinstance(m['defects'], list) or not all(is_str(x) for x in m['defects']) or \
                    not (rc is None or (isinstance(rc, dict) and set(rc) == {'path', 'sha256'} and is_hex64(rc['sha256']))) \
                    or (m['custody_ok'] and rc is None) or (m['finished'] and not m['custody_ok']):
                raise ValueError('BLOCK_MEMBER')
        try:
            prim = [(m['member_id'], m['log_index']) for m in man['members']]
        except (TypeError, KeyError):
            raise ValueError('BLOCK_MEMBERS_NOT_THE_PRIMARY_MEMBERS')
        if [(m['member_id'], m['log_index']) for m in blk['members']] != prim:
            raise ValueError('BLOCK_MEMBERS_NOT_THE_PRIMARY_MEMBERS')
        if self.b['inputs']['stage0_status'] is not None:
            rec = self.docs.get('stage0_status')
            proj = {'schema': STAGE0_RECORD_SCHEMA}
            proj.update({k: blk[k] for k in STAGE0_PROJ_KEYS if k != 'members'})
            proj['members'] = [{k: m[k] for k in STAGE0_PROJ_MEMBER_KEYS} for m in blk['members']]
            if not isinstance(rec, dict) or canonical(rec) != canonical(proj):
                raise ValueError('STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION')
        return facts

    @staticmethod
    def _stage0_exception_path(blk):
        """A168 V-N1 (root ruling): a block from the module's exception path is taken at the module's own reading.
        When a frozen stage0_status block is an exception-path block, from the bytes of d260ee30: its
        _stage0_receipt_verdict runs _stage0_apply_record inside `try` and, on any Exception, sets
        rule_a_receipts_finished = rule_b_successor_sealed = False and appends
        'STAGE0_RECEIPT_RULE_EXCEPTION: %s' % type(exc).__name__ to diagnostics (L3841-3843); nothing is appended after
        it, and the block is then built by _stage0_block from that verdict (L3853-3875).
        So a block claims the path when one of its diagnostics starts with STAGE0_RECEIPT_RULE_EXCEPTION, and it is an
        exception-path block exactly when (1) that claiming diagnostic is the only one and the last one, (2) it is
        'STAGE0_RECEIPT_RULE_EXCEPTION: ' followed by a class name (a Python identifier: a __name__ has no dot or
        space), and (3) both rule flags are False (the JSON value false). The diagnostics before it are not checked
        (c4v003 OC-43; the module can write STAGE0_SEALED_SUCCESSOR_NOT_NAMED or
        STAGE0_SEALED_SUCCESSOR_IS_NOT_THIS_MODULE there). Returns True for an exception-path block and False for a block
        that does not claim the path; raises ValueError('BLOCK_EXCEPTION_PATH') for a block that claims it but is not in
        that form (it stays TWIN_INPUT_DEFECT)."""
        diags = blk['diagnostics']
        claims = [i for i, x in enumerate(diags) if x.startswith(S0_EXCEPTION_PREFIX)]
        if not claims:
            return False
        last = diags[-1]
        name = last[len(S0_EXCEPTION_FORM):] if last.startswith(S0_EXCEPTION_FORM) else ''
        if claims != [len(diags) - 1] or not name.isidentifier() or \
                blk['rule_a_receipts_finished'] is not False or blk['rule_b_successor_sealed'] is not False:
            raise ValueError('BLOCK_EXCEPTION_PATH')
        return True

    @staticmethod
    def _stage0_facts(src, member_keys, successor, exception_path=False):
        """The receipt-rule facts (C-6.3, M-14) in the successor's encoding, from the block or from its projection,
        checked for the rule: phase None or PHASE_2 (a Phase-2 run; NOT_IN_PHASE_1 has no place in Phase 2);
        step4_start_utc a `date -u` time or null; sealed_successor null or {module_sha256 (lower-case hex), source};
        each member row: finished only with terminal_status FINISHED and a receipt time, before_step4 set exactly when
        finished and equal to (receipt time <= step-4 start) (a receipt at that instant counts as before);
        rule (a) rule_a_receipts_finished = every registered member finished (successor: bool(members) and all, as
        _stage0_receipt_verdict writes it; record: all, so an empty list holds vacuously: without the successor STAGE0
        is not registered for Phase 2); rule (b) rule_b_successor_sealed (successor: the record names the module's own
        sha, as the block's successor_module_sha256; record: false, since (b) fails without the seal pin);
        receipts_before_step4 = no finished receipt after the start; reasons = STAGE0_RECEIPT_NOT_FINISHED if not (a),
        NO_SEALED_SUCCESSOR if not (b), RECEIPTS_AFTER_STEP4 if not on time, in that order; reading
        NOT_EVALUATED_BEFORE_FREEZE with reasons, else EVALUATED_REFUSED when a receipt or evaluation refusal is
        recorded, else EVALUATED_BEFORE_FREEZE; evaluation refusals only where the rule holds; post_score_exploratory
        iff RECEIPTS_AFTER_STEP4.
        A168 V-N1 (c4v004), exception_path True (successor block only; _stage0_exception_path): the facts are those a
        partial _stage0_apply_record left before it raised, so the three recomputations of the receipt rule are replaced
        by the values the module writes on that path (d260ee30 L3830-3843): rule (a) and rule (b) are False whatever the
        member rows say (forced by the except clause), and receipts_before_step4 is True (its initial value, L3835: the
        module assigns it only in the last statement of _stage0_apply_record, L3817, never completed on this path; a block
        saying False is not the module's form and reads RECEIPTS_BEFORE_STEP4). A member row may be left between
        `row['finished'] = True` and the before_step4 assignment, so a finished row may carry before_step4 null; a
        before_step4 that is set must still equal (receipt time <= step-4 start). Every other check above applies. The
        reasons are then derived from the block's own flags as _stage0_block derives them (STAGE0_RECEIPT_NOT_FINISHED,
        NO_SEALED_SUCCESSOR; never RECEIPTS_AFTER_STEP4 on this path), so the reading is NOT_EVALUATED_BEFORE_FREEZE with
        those two reasons, evaluation refusals must be empty, receipt refusals do not change the reading, and
        post_score_exploratory is False. Raises ValueError(word)."""
        if src['phase'] not in (None, PHASE2):
            raise ValueError('PHASE')
        st = src['step4_start_utc']
        try:
            start = parse_utc(st) if st is not None else None
        except ValueError:
            raise ValueError('STEP4_START_UTC')
        ss = src['sealed_successor']
        if not (ss is None or (isinstance(ss, dict) and set(ss) == {'module_sha256', 'source'} and
                               is_hex64(ss['module_sha256']) and is_str(ss['source']))):
            raise ValueError('SEALED_SUCCESSOR')
        mem = src['members']
        if not isinstance(mem, list):
            raise ValueError('MEMBERS')
        for m in mem:
            if not isinstance(m, dict) or set(m) != set(member_keys) or not is_int(m['log_index']) or \
                    not (m['terminal_status'] is None or is_str(m['terminal_status'])) or \
                    not (m['written_utc'] is None or isinstance(m['written_utc'], str)) or \
                    not isinstance(m['finished'], bool) or m['before_step4'] not in (None, True, False):
                raise ValueError('MEMBER_ROW')
            try:
                wt = parse_utc(m['written_utc']) if m['written_utc'] is not None else None
            except ValueError:
                raise ValueError('MEMBER_WRITTEN_UTC')
            if m['finished']:
                if m['terminal_status'] != 'FINISHED' or wt is None or start is None or \
                        (m['before_step4'] is not (wt <= start) and not (exception_path and m['before_step4'] is None)):
                    raise ValueError('MEMBER_FINISHED')
            elif m['before_step4'] is not None:
                raise ValueError('MEMBER_BEFORE_STEP4')
        for k in ('rule_a_receipts_finished', 'rule_b_successor_sealed', 'receipts_before_step4',
                  'post_score_exploratory'):
            if not isinstance(src[k], bool):
                raise ValueError('RULE_FLAGS')
        for k in ('receipt_refusals', 'evaluation_refusals', 'reasons'):
            if not isinstance(src[k], list) or not all(is_str(x) for x in src[k]):
                raise ValueError('LISTS')
        fin = all(m['finished'] for m in mem)
        a = (bool(mem) and fin) if successor else fin
        if exception_path:
            a = False   # A168 V-N1: forced by the except clause (d260ee30 L3842)
        if src['rule_a_receipts_finished'] is not a:
            raise ValueError('RULE_A')
        if successor:
            b = ss is not None and ss['module_sha256'] == src['successor_module_sha256']
        else:
            b = False
        if exception_path:
            b = False   # A168 V-N1: forced by the except clause (d260ee30 L3842)
        if src['rule_b_successor_sealed'] is not b:
            raise ValueError('RULE_B')
        on_time = all(m['before_step4'] is not False for m in mem)
        if exception_path:
            on_time = True   # A168 V-N1: L3817 never completes on this path; the initial True stays (d260ee30 L3835)
        if src['receipts_before_step4'] is not on_time:
            raise ValueError('RECEIPTS_BEFORE_STEP4')
        reasons = ([S0_RNF] if not a else []) + ([S0_NSS] if not b else []) + ([S0_RA4] if not on_time else [])
        if src['reasons'] != reasons:
            raise ValueError('REASONS')
        if src['evaluation_refusals'] and reasons:
            raise ValueError('EVALUATION_REFUSALS')
        want = S0_NOT_EVALUATED if reasons else (S0_REFUSED if (src['receipt_refusals'] or src['evaluation_refusals'])
                                                 else S0_EVALUATED)
        if src['reading'] != want:
            raise ValueError('READING')
        if src['post_score_exploratory'] is not (S0_RA4 in reasons):
            raise ValueError('POST_SCORE_EXPLORATORY')
        return {'reading': want, 'reasons': reasons, 'step4_start_utc': st, 'members': mem,
                'post_score_exploratory': S0_RA4 in reasons}

    def s0g_compare(self, ref_rows, twin_rows):
        """C-6.3 comparison (M-9 as ruled): on the OUTER rows non-INVALID under both members with a defined r_q under
        both, H_P and H_S are the HIT counts and A_P, A_S the medians of |r_q|. CONSISTENT iff H_S > H_P and A_S < A_P;
        AGAINST iff H_S <= H_P and A_S >= A_P; NOT_DECIDED otherwise and when no row qualifies."""
        tw = {r['id']: r for r in twin_rows}
        q = []
        for r in ref_rows:
            if r['zone'] != 'OUTER':
                continue
            t = tw.get(r['id'])
            if t is None:
                continue
            if r['kind'] in ('H', 'MS') and t['kind'] in ('H', 'MS'):
                q.append((r, t))
        if not q:
            return 'NOT_DECIDED', {'qualifying_rows': [], 'H_P': 0, 'H_S': 0, 'A_P': 'UNDEFINED', 'A_S': 'UNDEFINED'}
        hp = sum(1 for r, _ in q if r['kind'] == 'H')
        hs = sum(1 for _, t in q if t['kind'] == 'H')
        ap = median([abs(r['r']) for r, _ in q])
        as_ = median([abs(t['r']) for _, t in q])
        if hs > hp and as_ < ap:
            st = 'CONSISTENT'
        elif hs <= hp and as_ >= ap:
            st = 'AGAINST'
        else:
            st = 'NOT_DECIDED'
        return st, {'qualifying_rows': [r['id'] for r, _ in q], 'H_P': hp, 'H_S': hs, 'A_P': ap, 'A_S': as_,
                    'rows': [{'id': r['id'], 'r_q_reference': r['r'], 'r_q_stage0': t['r']} for r, t in q]}

    # ================================================================ Phase-1 band column (C-1.1, M-16)
    def band_column(self, raw_rows):
        """C-1.1 Phase-1 band [r3a] (M-16 (1), unwidened): 'yes' iff the L1 band [lo_q, hi_q] intersects the error bar
        [v_q - sigma_q, v_q + sigma_q] (closed); NOT_AVAILABLE for a record NOT_AVAILABLE row; Q01 and Q02 always
        NOT_AVAILABLE; FD_NOISE_NOT_BOUNDED beside the entry iff fd_noise is that string (an object means bounded).
        L1 keys are status-conditional. A defect in an L1 row or in the target pair blanks only this column.
        The L1 record of phase1_c2v003b is v002's except `module` (cmd_band and band_rows unchanged since v002; A144
        R2, A149; v003b changes neither: DIFF v003a->v003b), so one row binding serves both pins; `module` must be the
        pin's."""
        col = {}
        l1 = self.docs.get('l1_record')
        tool = self.b['phase1_tool']
        rec_bad = None
        err = self.load_err.get('l1_record')
        if err == 'SHA_MISMATCH':
            rec_bad = 'L1_SHA_MISMATCH'
        elif err is not None:
            rec_bad = 'L1_RECORD_DEFECT'
        elif tool is None or not self._tool_module(tool):
            rec_bad = 'PHASE1_TOOL_PIN_DEFECT'
        elif not isinstance(l1, dict) or l1.get('schema') != 'PHASE1_L1_C2V001' or l1.get('module') != tool['module'] \
                or l1.get('label') != PHASE1_BAND_LABEL or not isinstance(l1.get('rows'), list):
            rec_bad = 'L1_RECORD_DEFECT'
        else:
            pi = self.docs.get('phase_inputs')
            if isinstance(pi, dict) and isinstance(pi.get('phase1_header'), dict) and \
                    self.b['inputs']['l1_record']['sha256'] != pi['phase1_header'].get('l1_sha256'):
                rec_bad = 'L1_SHA_MISMATCH'
        l1rows = {}
        if rec_bad is None:
            ids = [r.get('id') if isinstance(r, dict) else None for r in l1['rows']]
            for r in l1['rows']:
                if isinstance(r, dict) and isinstance(r.get('id'), str) and ids.count(r['id']) == 1:
                    l1rows[r['id']] = r
        for j, q in enumerate(QIDS):
            entry = {'label': PHASE1_BAND_LABEL, 'condition': PHASE1_BAND_CONDITION}
            l1r = l1rows.get(q)
            fdnb = isinstance(l1r, dict) and l1r.get('fd_noise') == 'FD_NOISE_NOT_BOUNDED'
            if rec_bad is not None:
                entry['overlaps'] = na([rec_bad])
                col[q] = entry
                continue
            if q in ALWAYS_NA_BAND_IDS:
                entry['overlaps'] = na(['Q01_Q02_ALWAYS_NOT_AVAILABLE'])
                entry['fd_noise_not_bounded'] = fdnb
                col[q] = entry
                continue
            if l1r is None or l1r.get('status') not in ('AVAILABLE', 'NOT_AVAILABLE'):
                entry['overlaps'] = na(['L1_ROW_DEFECT'])
                col[q] = entry
                continue
            if l1r['status'] == 'NOT_AVAILABLE':
                entry['overlaps'] = na(['L1_ROW_NOT_AVAILABLE'])
                entry['fd_noise_not_bounded'] = fdnb
                col[q] = entry
                continue
            lo, hi, fd = l1r.get('lo'), l1r.get('hi'), l1r.get('fd_noise')
            if not is_num(lo) or not is_num(hi) or not (isinstance(fd, dict) or fd == 'FD_NOISE_NOT_BOUNDED'):
                entry['overlaps'] = na(['L1_ROW_DEFECT'])
                col[q] = entry
                continue
            r = raw_rows[j] if raw_rows is not None else None
            v = r.get('observed_speed_km_s') if isinstance(r, dict) else None
            s = r.get('quoted_sigma_km_s') if isinstance(r, dict) else None
            if not is_num(v) or not is_num(s) or s <= 0:
                entry['overlaps'] = na(['TARGET_PAIR_DEFECT'])
                entry['fd_noise_not_bounded'] = fdnb
                col[q] = entry
                continue
            entry['overlaps'] = 'yes' if (lo <= v + s and hi >= v - s) else 'no'
            entry['fd_noise_not_bounded'] = fdnb
            col[q] = entry
        return col

    @staticmethod
    def _tool_module(tool):
        """The phase1 tool binding switches by the pinned sha (A142 item 4, A144, A149; brief c4v003 item 1): d64351ec
        binds the v002 encodings (module phase1_c2v002); 7d891ff7 binds the v003b encodings (module phase1_c2v003b,
        the MODULE string that sha's bytes write into L1, AT0A, AT0B and AT1). Any other sha (385b287c, the v003a pin
        of c4v002, included), or a module name that is not that sha's, is PHASE1_TOOL_PIN_DEFECT (band column and item
        11 only)."""
        return PHASE1_TOOLS.get(tool['sha256']) == tool['module']

    # ================================================================ item 11 (Phase 2; C-8 item 11)
    def agreement(self, my_rows_out, my_e3, my_patterns, my_headline):
        """C-8 item 11 [r3a]: the A133 section 4 outcome with its NON_DISCRIMINATING rows and failing (member, row)
        list from the pinned `agree` command (target-free); the target-dependent items from the two sealed
        classifications; and the consequence for Phase 1. A defective `agree` record: item 11 NOT_AVAILABLE, no outcome,
        Phase 1 keeps its PROVISIONAL label (neither standing nor WITHDRAWN). A defective Phase-1 classification input:
        outcome stated with its consequence; only the cross-phase items NOT_AVAILABLE. No Phase-1 classification:
        cross-phase items NOT_AVAILABLE with NO_PHASE_1_CLASSIFICATION (not a defect)."""
        rec, why = self.parse_agree()
        out = {}
        if rec is None:
            out['outcome'] = na(['AGREE_RECORD_DEFECT'])
            out['phase1_consequence'] = 'PHASE_1_KEEPS_PROVISIONAL_LABEL_NEITHER_STANDING_NOR_WITHDRAWN'
            out['agree_record_defect'] = why
            out['phase2_is_score_of_record'] = True
            return out
        oc = rec['outcome']
        out['outcome'] = oc
        out['non_discriminating_rows'] = rec.get('non_discriminating_rows', [])
        out['failing_member_rows'] = rec.get('failing', [])
        out['target_free_always_reported'] = rec.get('reported', na(['NOT_RUN_UNDER_AGREEMENT_DEFECT']))
        out['agree_schema'] = rec['schema']
        if 'at0b_members_sha256' in rec:      # phase1_c2v003b AT0B (A149 item 2), echoed target-free
            out['at0b_members_sha256'] = rec['at0b_members_sha256']
        if 'at0b_values_sha256' in rec:       # phase1_c2v003b AT0B (v003b V1), echoed target-free
            out['at0b_values_sha256'] = rec['at0b_values_sha256']
        out['phase2_is_score_of_record'] = True
        if oc == 'COVERED':
            out['phase1_consequence'] = 'STANDING_AS_EARLY_STATEMENT_OF_THE_SCORE_OF_RECORD'
        elif oc == 'SUPERSEDED':
            out['phase1_consequence'] = 'WITHDRAWN'
            out['withdrawn'] = {'patterns': 'WITHDRAWN_REPLACED_BY_PHASE_2', 'readings': 'WITHDRAWN_REPLACED_BY_PHASE_2',
                                'zone_summaries': 'WITHDRAWN_REPLACED_BY_PHASE_2',
                                'e3_line': 'WITHDRAWN_REPLACED_BY_PHASE_2',
                                'band_entries': 'WITHDRAWN_NOT_REPLACED'}
        else:
            out['phase1_consequence'] = 'PHASE_2_STANDS_ROOT_INVESTIGATES'
        # cross-phase items
        pi = self.docs.get('phase_inputs')
        absent = pi.get('phase1_classification_absent_reason') if isinstance(pi, dict) else None
        p1 = self.docs.get('phase1_classification')
        if self.b['inputs']['phase1_classification'] is None and absent is not None:
            out['cross_phase'] = na(['NO_PHASE_1_CLASSIFICATION'])
            out['no_phase1_classification_reason'] = absent
            return out
        if not self._p1_ok(p1):
            out['cross_phase'] = na(['PHASE1_CLASSIFICATION_INPUT_DEFECT'])
            return out
        tier_changes, tier_na = [], []
        for a, b in zip(p1['rows'], my_rows_out):
            ka, kb = a['tier_key'], b['tier_key']
            if isinstance(ka, dict) or isinstance(kb, dict):
                tier_na.append(b['id'])
            elif ka != kb:
                tier_changes.append({'id': b['id'], 'phase1': ka, 'phase2': kb})
        out['cross_phase'] = {'headlines': {'phase1': p1['headline'], 'phase2': my_headline},
                              'e3_lines': {'phase1': p1['e3_line'].get('value') if isinstance(p1['e3_line'], dict)
                                           else p1['e3_line'], 'phase2': my_e3},
                              'pattern_classifications': {'phase1': p1['patterns_holding'], 'phase2': my_patterns},
                              'rows_whose_tier_changed': tier_changes,
                              'rows_tier_comparison_not_available': tier_na}
        return out

    @staticmethod
    def _p1_ok(p1):
        if not isinstance(p1, dict) or p1.get('schema') != OUT_SCHEMA or p1.get('mode') != 'score' or \
                p1.get('phase') != PHASE1 or p1.get('status') not in ('CLASSIFIED', 'NOT_READ'):
            return False
        rows = p1.get('rows')
        if not isinstance(rows, list) or len(rows) != 43 or any(
                not isinstance(r, dict) or r.get('id') != QIDS[j] or 'tier_key' not in r for j, r in enumerate(rows)):
            return False
        return 'headline' in p1 and 'e3_line' in p1 and 'patterns_holding' in p1

    def parse_agree(self):
        """The A133 `agree` record bound to the pinned tool's keys and value encodings (C-1.1 map; the record is the
        AT-1 record, or, when AT-1 did not run, the AT-0a or AT-0b record that reports AGREEMENT_DEFECT [r3a, F2]).
        Under AGREEMENT_DEFECT the fields of a test `agree` did not run may be absent. A missing record (no AT-1 record
        because at1 refused after AT-0a and AT-0b passed, as v003b's VALUES or A149's MEMBERS refusal) is a defective
        one (basis row D6): load_err NOT_SUPPLIED, item 11 NOT_AVAILABLE. Encodings by the pinned sha: d64351ec as in
        c4v001; 7d891ff7 (phase1_c2v003b) from its bytes, which keep every v003a encoding (DIFF v003a->v003b): an AT0B
        record carries members_sha256 (A149 item 2) and values_sha256 (v003b V1), each written lower-cased by
        cmd_at0b, every AT1 failing entry carries exactly the eleven keys at1_rows writes (`flag` included), and
        `reported` has exactly at1_rows' twelve keys (A144 R1-R3, A149 items 1 and 3).
        Returns (record, None) or (None, why)."""
        err = self.load_err.get('agree_record')
        if err is not None:
            return None, err
        tool = self.b['phase1_tool']
        if tool is None or not self._tool_module(tool):
            return None, 'PHASE1_TOOL_PIN_DEFECT'
        v3a = tool['module'] == PHASE1_TOOL_V003B_MODULE    # the v003a encodings, as v003b keeps them
        a = self.docs['agree_record']
        if not isinstance(a, dict) or a.get('module') != tool['module']:
            return None, 'MODULE'
        sch = a.get('schema')
        if sch in ('PHASE1_AT0A_C2V001', 'PHASE1_AT0B_C2V001'):
            if a.get('outcome') != 'AGREEMENT_DEFECT' or not isinstance(a.get('failures'), list) or \
                    not all(isinstance(x, str) for x in a['failures']):
                return None, 'AT0_RECORD'
            rec = {'schema': sch, 'outcome': 'AGREEMENT_DEFECT', 'at0_failures': a['failures']}
            if v3a and sch == 'PHASE1_AT0B_C2V001':
                if not is_hex64(a.get('members_sha256')):     # A149 item 2: a.members_sha256.lower()
                    return None, 'AT0B_MEMBERS_SHA256'
                if not is_hex64(a.get('values_sha256')):      # v003b V1: a.values_sha256.lower(), always written
                    return None, 'AT0B_VALUES_SHA256'
                rec['at0b_members_sha256'] = a['members_sha256']
                rec['at0b_values_sha256'] = a['values_sha256']
            return rec, None
        if sch != 'PHASE1_AT1_C2V001':
            return None, 'SCHEMA'
        oc = a.get('outcome')
        if oc not in AGREE_OUTCOMES or not isinstance(a.get('at0'), list) or len(a['at0']) != 2 or \
                not all(isinstance(x, str) for x in a['at0']):
            return None, 'OUTCOME'
        rec = {'schema': sch, 'outcome': oc}
        for k in ('failing', 'non_discriminating_rows', 'reported'):
            if k not in a:
                if oc == 'AGREEMENT_DEFECT':
                    continue
                return None, 'MISSING:%s' % k
        if 'non_discriminating_rows' in a:
            nd = a['non_discriminating_rows']
            if not isinstance(nd, list) or not all(x in QIDS for x in nd):
                return None, 'NON_DISCRIMINATING_ROWS'
            rec['non_discriminating_rows'] = nd
        if 'failing' in a:
            fl = a['failing']
            if not isinstance(fl, list):
                return None, 'FAILING'
            outl = []
            for f in fl:
                if not isinstance(f, dict):
                    return None, 'FAILING_ENTRY'
                if v3a:
                    if set(f) != AGREE_V003A_FAIL_KEYS:
                        return None, 'FAILING_KEYS_V003A'
                    if f['category'] not in AGREE_V003A_CATEGORIES:
                        return None, 'CATEGORY'
                    rv = f['region_rows_violated']
                    if not isinstance(rv, list) or not all(isinstance(x, str) for x in rv) or \
                            rv != [x for x in AGREE_V003A_FAMILIES if x in rv] or len(set(rv)) != len(rv):
                        return None, 'REGION_ROWS_VIOLATED'
                    want = AGREE_V003A_CAT_OF[rv[0]] if rv else 'NGC_NONLINEAR'
                    if f['category'] != want:
                        return None, 'CATEGORY_MAPPING'
                    mv = f['region_max_violation']
                    if not isinstance(mv, dict) or set(mv) != set(AGREE_V003A_FAMILIES) or \
                            not all(is_num(x) for x in mv.values()):
                        return None, 'REGION_MAX_VIOLATION'
                    if not is_num(f['geometric_part']) or not is_num(f['residual_part']):
                        return None, 'PARTS'
                    if not self._flag_pair_ok(f['flag'], f['flag_reason']):
                        return None, 'FLAG_OR_FLAG_REASON'
                else:
                    if set(f) != AGREE_V002_FAIL_KEYS or f['category'] not in AGREE_V002_CATEGORIES or \
                            f['flag'] not in (None, 'FD_NOISE_NOT_BOUNDED'):
                        return None, 'FAILING_KEYS_V002'
                if not is_int(f['log_index']) or f['id'] not in QIDS or not is_num(f['excess']) or \
                        not is_num(f['norm_n']) or f['norm_n'] < 0:
                    return None, 'FAILING_VALUES'
                e = {'member_log_index': f['log_index'], 'row': f['id'], 'excess': f['excess'],
                     'norm_n': f['norm_n'], 'category': f['category']}
                e['flag'] = f['flag']
                if v3a:
                    for k in ('region_rows_violated', 'region_max_violation', 'geometric_part', 'residual_part',
                              'flag_reason'):
                        e[k] = f[k]
                outl.append(e)
            if oc == 'SUPERSEDED' and not outl:
                return None, 'SUPERSEDED_WITHOUT_FAILING'
            if oc == 'COVERED' and outl:
                return None, 'COVERED_WITH_FAILING'
            rec['failing'] = outl
        if 'reported' in a:
            rp = a['reported']
            if v3a:
                if not isinstance(rp, dict) or set(rp) != AGREE_V003A_REPORTED:
                    return None, 'REPORTED_KEYS'
                bad = self._reported_v003a_defect(rp)
                if bad:
                    return None, bad
            elif not isinstance(rp, dict) or not all(k in rp for k in AGREE_V002_REPORTED):
                return None, 'REPORTED_KEYS'
            rec['reported'] = rp
        return rec, None

    @staticmethod
    def _flag_pair_ok(flag, reason):
        """phase1_c2v003a at1_rows (A144 R3; A149 item 1): a bounded pair has flag and flag_reason None; a row without
        eps_q has flag FD_NOISE_NOT_BOUNDED with flag_reason NO_ROW_EPS_Q; an unbounded member-point entry has flag
        MEMBER_POINT_NOISE_NOT_BOUNDED with flag_reason the member_eps reason (MEMBER_EPS_...; an int beyond the float
        range reads MEMBER_EPS_NON_FINITE)."""
        if flag is None:
            return reason is None
        if flag == FLAG_FD:
            return reason == REASON_NO_ROW_EPS
        if flag == FLAG_MPN:
            return reason in MEMBER_EPS_REASONS
        return False

    @classmethod
    def _extent_list_defect(cls, ext):
        """band_region_extent / band_region_box_only_extent entries as phase1_c2v003a writes them (A144 R2; A149 item 3):
        {direction (an identified index), extent [lo, hi], lp_status [s_min, s_max]}; each bound is a number when its
        program's status is OPTIMAL and the string NOT_AVAILABLE otherwise. Returns None or a defect word."""
        if not isinstance(ext, list):
            return 'EXTENT_LIST'
        for x in ext:
            if not isinstance(x, dict) or set(x) != {'direction', 'extent', 'lp_status'} or not is_int(x['direction']):
                return 'EXTENT_ENTRY'
            e, s = x['extent'], x['lp_status']
            if not isinstance(e, list) or not isinstance(s, list) or len(e) != 2 or len(s) != 2 or \
                    not all(is_str(t) for t in s):
                return 'EXTENT_ENTRY'
            for v, t in zip(e, s):
                if (t == 'OPTIMAL' and not is_num(v)) or (t != 'OPTIMAL' and v != NA_KEY):
                    return 'EXTENT_VALUE'
        return None

    @classmethod
    def _reported_v003a_defect(cls, rp):
        """The target-free always-reported items of a phase1_c2v003a AT1 record that A144 and A149 add, bound to
        at1_rows' encodings (print only: they change no outcome; a defect blanks item 11 as any agree-record field):
        - e_q_per_member_row: {log_index, id, e_q, eps_m, flag, flag_reason}; bounded: e_q and eps_m numbers (eps_m >=
          0); MEMBER_POINT_NOISE_NOT_BOUNDED: e_q a number, eps_m null; FD_NOISE_NOT_BOUNDED: e_q is that string, eps_m
          null (A149: eps_m, flag, flag_reason);
        - pairs_member_point_noise_not_bounded: {log_index, id, flag_reason} with a member_eps reason (A144 R3);
        - band_region_extent and band_region_box_only_extent: _extent_list_defect, over the same directions in order;
        - band_region_single_point: NOT_AVAILABLE iff some band_region_extent program is not OPTIMAL; else true iff
          every extent is exactly [0.0, 0.0] (A144 R2, exact);
        - band_region_single_point_reason: null unless the single point is true; then BOX_CORNER or OTHER_ROWS."""
        eq = rp['e_q_per_member_row']
        if not isinstance(eq, list):
            return 'E_Q_PER_MEMBER_ROW'
        for x in eq:
            if not isinstance(x, dict) or set(x) != {'log_index', 'id', 'e_q', 'eps_m', 'flag', 'flag_reason'} or \
                    not is_int(x['log_index']) or x['id'] not in QIDS or not cls._flag_pair_ok(x['flag'], x['flag_reason']):
                return 'E_Q_PER_MEMBER_ROW'
            if x['flag'] is None:
                ok = is_num(x['e_q']) and is_num(x['eps_m']) and x['eps_m'] >= 0
            elif x['flag'] == FLAG_MPN:
                ok = is_num(x['e_q']) and x['eps_m'] is None
            else:
                ok = x['e_q'] == FLAG_FD and x['eps_m'] is None
            if not ok:
                return 'E_Q_PER_MEMBER_ROW_VALUES'
        pm = rp['pairs_member_point_noise_not_bounded']
        if not isinstance(pm, list) or not all(
                isinstance(x, dict) and set(x) == {'log_index', 'id', 'flag_reason'} and is_int(x['log_index']) and
                x['id'] in QIDS and x['flag_reason'] in MEMBER_EPS_REASONS for x in pm):
            return 'PAIRS_MEMBER_POINT_NOISE_NOT_BOUNDED'
        ext, box = rp['band_region_extent'], rp['band_region_box_only_extent']
        d = cls._extent_list_defect(ext) or cls._extent_list_defect(box)
        if d:
            return 'BAND_REGION_' + d
        if [x['direction'] for x in ext] != [x['direction'] for x in box]:
            return 'BAND_REGION_DIRECTIONS'
        sp = rp['band_region_single_point']
        if any(t != 'OPTIMAL' for x in ext for t in x['lp_status']):
            want = NA_KEY
        else:
            want = all(x['extent'][0] == 0.0 and x['extent'][1] == 0.0 for x in ext)
        if not (sp is want or (isinstance(sp, str) and sp == want)):
            return 'BAND_REGION_SINGLE_POINT'
        reason = rp['band_region_single_point_reason']
        if (sp is True and reason not in ('BOX_CORNER', 'OTHER_ROWS')) or (sp is not True and reason is not None):
            return 'BAND_REGION_SINGLE_POINT_REASON'
        return None

    # ================================================================ the whole run
    def labels(self, score):
        """C-I7, C-I6, M-8: PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) in Phase 1, PROVISIONAL (FREEZE_INCOMPLETE) for an
        incomplete Phase-2 freeze, each with incomplete_reasons; PROVISIONAL (N_GATE_NOT_OPEN) when the record of
        record's gate is not OPEN; EXPLORATORY (PHASE 2 NOT AS COMMITTED) under the Phase-2 commitment status; and the
        fallback record's label. Carried by every pattern, reading and zone summary, the E3 line and DT-S0G."""
        labs = []
        ir = score.get('incomplete_reasons') if isinstance(score, dict) else None
        ir = sorted(ir) if isinstance(ir, list) and all(isinstance(x, str) for x in ir) else na(['FIELD_DEFECT_OUTSIDE_ROWS'])
        if self.phase == PHASE1:
            labs.append({'label': LABEL_P1, 'incomplete_reasons': ir})
        elif isinstance(score, dict) and score.get('freeze_status') == 'FREEZE_INCOMPLETE':
            labs.append({'label': LABEL_INCOMPLETE, 'incomplete_reasons': ir})
        if self.compare_gate != 'OPEN':
            labs.append({'label': LABEL_NGATE, 'gate': self.compare_gate if isinstance(self.compare_gate, str) else NA_KEY})
        if self.phase == PHASE2:
            st = self.commitment()
            if st['status'] == 'EXPLORATORY':
                labs.append({'label': LABEL_EXPLORATORY_P2, 'code': st.get('code')})
        fb = self.docs.get('fallback')
        if isinstance(fb, dict) and fb.get('classification_label') in ('EXPLORATORY (post-prediction)',
                                                                        'POST-PREDICTION (CLASSIFIER)'):
            labs.append({'label': fb['classification_label']})
        return labs

    def commitment(self):
        """C-I7 commitment status [r3a]: COMMITTED, or EXPLORATORY with each stop or change and the entry; a missing or
        malformed status reads EXPLORATORY with COMMITMENT_STATUS_DEFECT (it blanks no output)."""
        c = self.docs.get('commitment_status')
        if isinstance(c, dict) and c.get('schema') == 'PHASE2_COMMITMENT_STATUS_C4V001' and \
                set(c) == {'schema', 'status', 'stops_or_changes'} and isinstance(c['stops_or_changes'], list) and \
                all(isinstance(x, dict) and set(x) == {'what', 'entry'} and is_str(x['what']) and is_str(x['entry'])
                    for x in c['stops_or_changes']):
            if c['status'] == 'COMMITTED' and not c['stops_or_changes']:
                return {'status': 'COMMITTED', 'stops_or_changes': []}
            if c['status'] == 'EXPLORATORY' and c['stops_or_changes']:
                return {'status': 'EXPLORATORY', 'stops_or_changes': c['stops_or_changes'], 'code': None}
        return {'status': 'EXPLORATORY', 'code': 'COMMITMENT_STATUS_DEFECT', 'stops_or_changes': na(['COMMITMENT_STATUS_DEFECT'])}

    def run(self):
        self.load_inputs()
        pi = self.docs.get('phase_inputs')
        self.compare_gate = None
        self.gate_list_out = None
        self.manifest_phase = None
        # no classification at all (C-I7 'No classification, or no score of record')
        if self._phase_inputs_ok(pi) and pi['run_status'] != 'SCORED':
            self.phase = pi['phase_named']
            return {'schema': OUT_SCHEMA, 'classifier': NAME, 'mode': self.mode, 'phase': self.phase,
                    'status': 'NO_CLASSIFICATION', 'status_code': pi['run_status'],
                    'run_status_code': pi['run_status_code'],
                    'note': {'NO_NGC_CALL': 'no NGC call: no classification (engine terminal status or '
                                            'NO_IDENTIFIED_DIRECTION; A133 1.3)',
                             'AT0A_FAILED': 'AGREEMENT_DEFECT (prefix): no Phase-1 classification',
                             'HALTED': 'Phase 2 reported HALTED (A133 3 rule (c))'}[pi['run_status']]}
        self.check_seal()
        self.check_phase()
        self.check_zone_table()
        self.check_gate_list()
        self.check_tsr()
        man = self.docs.get('freeze_manifest')
        if not isinstance(man, dict):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'freeze manifest missing or malformed (%s)'
                      % self.load_err.get('freeze_manifest'))
        self.check_manifest_schema(man)
        if self.mode == 'prescore':
            try:
                score = synthesize_score(man)
            except (TypeError, KeyError, ValueError, IndexError, AttributeError, OverflowError) as exc:   # V-F3
                score = None
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'synthetic score could not be built from the frozen '
                                                              'manifest: %s' % type(exc).__name__)
        else:
            score = self.docs.get('score')
        self.check_score(score, man)
        if isinstance(score, dict):     # an unreadable score is one outside-rows stop; nothing below can be checked
            self.check_envelope(score)
            self.check_sensitivity(score)
        rows, problems = ([], [])
        if self.ref_rows_raw is not None:
            rows, problems = self.build_rows(self.ref_rows_raw, self.mref)
            for q, d, c in problems:
                if c == 'ROW':
                    self.stop('FIELD_DEFECT_ROW', 'ROW', '%s: %s' % (q, d), rows=(q,))
                else:
                    self.stop('GATE_STATUS_LIST_DEFECT', 'GATE', '%s: %s' % (q, d), rows=(q,))
            for r in rows:
                if r['kind'] is None and self.mref is not None:
                    fr = self._frozen_registration(self.mref, QIDS.index(r['id']))
                    r['_fr_reason'] = fr[1] if isinstance(fr, tuple) else None
            if any(r['raw'].get('status') == 'UNEVALUATED_OR_REFUSED' for r in rows):
                self.stop('REFERENCE_ROW_UNEVALUATED_OR_REFUSED', 'ALL', 'a reference-member row has status '
                                                                         'UNEVALUATED_OR_REFUSED')
        alt_info = self.check_alternatives(score) if isinstance(score, dict) else {'list': [], 'by_name': {}}
        self.prepare_alternatives(alt_info)
        if self.mode == 'prescore':
            return self.prescore_output()
        return self.score_output(score, rows, alt_info)

    def check_alternatives(self, score):
        """M-5 alternatives[] fields: name, kind, status, role, scored, members, scoring_scope. A field defect makes that
        alternative read TWIN_INPUT_DEFECT (C-1.1 map); a missing declared alternative likewise. Phase 1: the I-4 rule
        applies before the twin rule (M-10 precedence): ORIGINAL_K reads NOT_AVAILABLE and STAGE0 NOT_IN_PHASE_1."""
        info = {}
        alts = score.get('alternatives') if isinstance(score, dict) else None
        if not isinstance(alts, list):
            alts = []
            for n in ALT_ORDER[1:]:
                if not (self.phase == PHASE1 and n in ('ORIGINAL_K', 'STAGE0_GRID_OUTER')):
                    self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: alternatives list missing' % n, alt=n)
            return {'list': [], 'by_name': {}}
        by = {}
        for a in alts:
            if isinstance(a, dict) and isinstance(a.get('name'), str):
                if a['name'] in by:
                    by[a['name']] = 'DUP'
                else:
                    by[a['name']] = a
        for n in ALT_ORDER[1:] + (DISTANCE_ALT,):
            if self.phase == PHASE1 and n in ('ORIGINAL_K', 'STAGE0_GRID_OUTER'):
                continue
            a = by.get(n)
            if a is None:
                if n != DISTANCE_ALT:
                    self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: declared alternative missing' % n, alt=n)
                continue
            if a == 'DUP':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: repeated' % n, alt=n)
                continue
            bad = []
            for k, ok in (('kind', isinstance(a.get('kind'), str)), ('status', a.get('status') in (
                    'EVALUATED_BEFORE_FREEZE', 'NOT_EVALUATED_BEFORE_FREEZE')),
                          ('role', a.get('role') == 'NON_PRIMARY'), ('scored', isinstance(a.get('scored'), bool))):
                if not ok:
                    bad.append(k)
            if n == 'STAGE0_GRID_OUTER':
                sc = a.get('scoring_scope')
                if not isinstance(sc, dict) or sc.get('query_ids') != list(OUTER_IDS):
                    bad.append('scoring_scope')
            if a.get('scored') is True and not isinstance(a.get('members'), list):
                bad.append('members')
            if bad:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: %s' % (n, ','.join(bad)), alt=n)
        return {'list': alts, 'by_name': by}

    def prepare_alternatives(self, alt_info):
        """C-6.1 twin rule applied to every evaluated non-PRIMARY alternative, and the C-6.3 STAGE0 status with its twin,
        before the output is assembled: a twin field defect (or a missing twin) is a field of an alternative, so it is a
        stop of the alternative class (that alternative reads TWIN_INPUT_DEFECT); a twin id mismatch reads
        TWIN_INPUT_DEFECT by C-6.1 alone; TWIN_INVALID is not a defect."""
        self.alt_res = {}
        self.s0_status, self.s0_cls = self.stage0_status()
        if self.s0_cls == 'TWIN_INPUT_DEFECT':
            if self.s0_defect and self.s0_defect[0] == STAGE0_SOURCE_BLOCK:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', 'STAGE0_GRID_OUTER: the frozen stage0_status block of the '
                                                             'STAGE0 successor is not bound or malformed (%s)'
                          % self.s0_defect[1], alt='STAGE0_GRID_OUTER')
            else:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', 'STAGE0_GRID_OUTER: STAGE0 status record missing or malformed',
                          alt='STAGE0_GRID_OUTER')
        ref = getattr(self, 'ref_member', None)
        if not isinstance(ref, dict) or not is_int(ref.get('log_index')):
            return
        ref_li = ref['log_index']
        todo = []
        for n in ALT_ORDER[1:5]:
            if self.phase == PHASE1 and n == 'ORIGINAL_K':
                continue
            a = alt_info['by_name'].get(n)
            if isinstance(a, dict) and not self.codes_alt(n) and a.get('status') == 'EVALUATED_BEFORE_FREEZE' and \
                    a.get('scored') is True:
                todo.append((n, a, QIDS))
        if self.phase == PHASE2 and self.s0_cls == 'EVALUATED' and not self.codes_alt('STAGE0_GRID_OUTER'):
            a = alt_info['by_name'].get('STAGE0_GRID_OUTER')
            if isinstance(a, dict) and a.get('scored') is True:
                todo.append(('STAGE0_GRID_OUTER', a, OUTER_IDS))
            else:
                self.alt_res['STAGE0_GRID_OUTER'] = ('TWIN_INPUT_DEFECT', None, None, 'STAGE0 evaluated by the receipt '
                                                     'rule but not scored in the score output')
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', 'STAGE0_GRID_OUTER: evaluated by the receipt rule but not '
                                                             'scored', alt='STAGE0_GRID_OUTER')
        for n, a, scope in todo:
            state, tw, trows, why = self.twin_rows(a, ref_li, scope)
            if state == 'TWIN_INPUT_DEFECT' and why != 'twin ids differ from its scope':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: %s' % (n, why), alt=n)
            self.alt_res[n] = (state, tw, trows, why)

    # ------------------------------------------------------------ prescore output
    def prescore_output(self):
        """C-1.1 'Pre-score checks (binding)': every stop condition checked on the frozen manifest, slots and pinned
        records through this classifier, on a synthetic score built from the frozen member arrays. Any stop: the
        classification stops with CLASSIFICATION_INPUT_DEFECT and its code, before target access."""
        stops = self.stops_out()
        return {'schema': OUT_SCHEMA, 'classifier': NAME, 'mode': 'prescore', 'phase': self.phase,
                'manifest_phase_derived': self.manifest_phase,
                'result': 'CLASSIFICATION_INPUT_DEFECT' if stops else 'PASS', 'stops': stops,
                'not_stop_inputs': {'l1_record': self.load_err.get('l1_record') or 'READ',
                                    'agree_record': self.load_err.get('agree_record') or 'READ',
                                    'phase1_classification': self.load_err.get('phase1_classification') or 'READ',
                                    'commitment_status': self.load_err.get('commitment_status') or 'READ'},
                'field_map': self.field_map_status}

    def stops_out(self):
        out = []
        for (code, cls, alt), e in sorted(self.stops.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or '')):
            out.append({'code': code, 'class': cls, 'alternative': alt, 'detail': sorted(e['detail']),
                        'rows': sorted(e['rows'])})
        return out

    # ------------------------------------------------------------ score output
    def score_output(self, score, rows, alt_info):
        """C-8 items 1 to 11 under the C-1.1 stop-to-output map: an "every other" stop blanks every output except the
        header; the row and gate classes go through the engine; the other classes blank only their own outputs."""
        stops = self.stops_out()
        all_codes = self.codes('ALL')
        labels = self.labels(score)
        status = 'NOT_READ' if stops else 'CLASSIFIED'
        header = self.header(score)
        out = {'schema': OUT_SCHEMA, 'classifier': NAME, 'mode': 'score', 'phase': self.phase, 'status': status,
               'status_code': sorted({s['code'] for s in stops}) if stops else None, 'stops': stops, 'labels': labels,
               'header': header, 'exploratory_readings': [], 'fallback': self.fallback_out()}
        out['headline'] = self.headline_out(score)
        if all_codes:
            blank = na(all_codes)
            for k in ('rows', 'zones', 'outer_trend', 'outer_failure', 'e3_line', 'patterns', 'patterns_holding',
                      'minority_miss', 'flagged_rows', 'readings', 'descriptive', 'invalid_list', 'a15', 'p8_report',
                      'alternatives', 'stage0'):
                out[k] = blank
            if self.phase == PHASE2:
                out['agreement'] = blank
            out['rows'] = [{'id': q, 'zone': ZONE_TABLE[q], 'tier_key': blank} for q in QIDS]
            return out
        codes_d = self.codes('ROW', 'GATE')
        tsr_codes = self.codes('TSR')
        res = self.engine(rows, codes_d)
        # NEAR and N(Z) (C-1.1, C-I7)
        env_codes = self.codes('ENVELOPE')
        env_bad = set()
        for k, e in self.stops.items():
            if k[1] == 'ENVELOPE':
                env_bad |= e['rows']
        near = {}
        for r in rows:
            q = r['id']
            if r['kind'] is None:
                near[q] = (None, codes_d)
            elif r['kind'] in ('H', 'I', 'L'):
                # NEAR applies only to tier-MISS rows: an envelope-row defect blanks NEAR and N(Z) only where the row is
                # tier-MISS (C-1.1 map, basis row T3); a HIT, INVALID or LATE-gate row never carries NEAR
                near[q] = (False, [])
            elif q in env_bad:
                near[q] = (None, env_codes)
            elif not self.env[q][0]:
                near[q] = (None, ['ENVELOPE_ROW_INVALID'])
            else:
                near[q] = (self.env[q][1], [])
        nz = {}
        for z in ZONES:
            zr = [r for r in rows if r['zone'] == z]
            cs = set()
            for r in zr:
                if near[r['id']][0] is None:
                    cs |= set(near[r['id']][1])
            nz[z] = (None, sorted(cs)) if cs else (sum(1 for r in zr if near[r['id']][0] is True), [])
        # STAGE0 / DT-S0G
        stage0, s0g_state, s0g_codes, s0g_detail, stage0_class = self.stage0_block(res, rows, alt_info, labels)
        # readings
        tsr_blank = tsr_codes if tsr_codes else None
        if tsr_blank:
            res['P']['P10'] = None
        readings = self.readings(res, rows, codes_d, s0g_state, s0g_codes, labels, tsr_blank)
        # rows out
        band = self.band_column(self.ref_rows_raw) if self.phase == PHASE1 else None
        sens_codes = self.codes('SENSITIVITY')
        sens_bad = set()
        for k, e in self.stops.items():
            if k[1] == 'SENSITIVITY':
                sens_bad |= e['rows']
        rows_out = []
        for r in rows:
            q = r['id']
            o = {'id': q, 'zone': r['zone'], 'R_q': self.rad[q][0], 'notes': D2_NOTE}
            if r['kind'] is None:
                b = na(codes_d)
                for k in ('tier', 'reading_kind', 'r_q', 'sign', 'frozen_prediction', 'near', 'tsr_flag',
                          'invalid_reason', 'gate_status', 'gate_after_predictions', 'sensitivity_band_overlap',
                          'tier_key'):
                    o[k] = b
                o['near_label'] = NEAR_LABEL       # the column's gloss is printed with every NEAR entry (V-F6)
                if self.phase == PHASE1:
                    o['phase1_band'] = b
                rows_out.append(o)
                continue
            k = r['kind']
            o['tier'] = 'INVALID_AS_MISS' if k in ('I', 'L') else 'HIT' if k == 'H' else 'MISS'
            o['reading_kind'] = KIND_NAME[k]
            o['r_q'] = r['r']
            o['sign'] = self.sign_of(r)
            o['frozen_prediction'] = k in ('H', 'MS', 'MN')
            o['near'] = self.o3(near[q][0], near[q][1])
            o['near_label'] = NEAR_LABEL           # C-1.1: NEAR is reported as "envelope overlaps the error bar" (V-F6)
            o['tsr_flag'] = na(tsr_codes) if tsr_codes else r['flagged']
            o['invalid_reason'] = r['reason']
            o['gate_status'] = r['gate_status']
            o['gate_after_predictions'] = k == 'L'
            if self.phase == PHASE1:
                o['sensitivity_band_overlap'] = 'invalid'
            elif q in sens_bad:
                o['sensitivity_band_overlap'] = na(sens_codes)
            else:
                v, ov = self.sens[q]
                o['sensitivity_band_overlap'] = ('yes' if ov else 'no') if v else 'invalid'
            o['sensitivity_band_label'] = SENS_LABEL
            o['tier_key'] = ('INVALID_AS_MISS:' + r['reason']) if k == 'I' else 'LATE_GATE_MISS' if k == 'L' else \
                'WITHIN_ERROR' if k == 'H' else 'MISS_WORST_TIER'
            if self.phase == PHASE1:
                o['phase1_band'] = band[q]
            rows_out.append(o)
        out['rows'] = rows_out
        out['zones'] = {z: dict(self.zone_out(res, z, codes_d, nz[z][1], nz[z][0]), labels=labels) for z in ZONES}
        tD = res['hasD']['TRANSITION'] or res['hasD']['OUTER']
        out['outer_trend'] = {'delta_out': self.o3(res['delta'], codes_d),
                              'far_half_median': self.o3(res['far'], codes_d),
                              'GROWING': self.o3(res['growing'], codes_d), 'CROSSING': self.o3(res['crossing'], codes_d)}
        out['outer_failure'] = self.o3(res['OF'], codes_d)
        P = res['P']
        pat = {}
        for p in PATTERN_IDS:
            if p == 'P10' and tsr_codes:
                pat[p] = na(tsr_codes)
            else:
                pat[p] = self.o3(P[p], codes_d)
        pat["labels"] = labels
        pat["names"] = PATTERN_NAMES
        if P['P13'] is True:
            pat['P13_sign_class'] = self.o3(res['S']['TRANSITION'], codes_d)
        p0z = {}
        for z in ZONES:
            p0z[z] = self.zone_out(res, z, codes_d, [], 0)['I_per_reason']
        pat['P0_per_zone_per_reason'] = p0z
        if P['P8'] is True:
            pat['P8_reported_with'] = {'I': {z: out['zones'][z]['I'] for z in ZONES},
                                       'N': {z: out['zones'][z]['N'] for z in ZONES},
                                       'note': 'never "all hit": INVALID rows still score as misses (C-4)'}
        out['patterns'] = pat
        out['patterns_holding'] = [p for p in PATTERN_IDS if pat[p] is True]
        out['minority_miss'] = {z: self.o3(P['MM:' + z], codes_d) for z in ZONES}
        # flagged-row list (C-2): every flagged row with its tier, INVALID included
        if tsr_codes:
            out['flagged_rows'] = na(tsr_codes)
        else:
            out['flagged_rows'] = [{'id': r['id'], 'tier': rows_out[QIDS.index(r['id'])]['tier']} for r in rows
                                   if r['flagged']]
        out['readings'] = readings
        # E3 line (C-5.3)
        zo = out['zones']['OUTER']
        e3 = {'value': self.o3(res['E3'], codes_d), 'S_OUTER': self.o3(res['S']['OUTER'], codes_d),
              'delta_out': out['outer_trend']['delta_out'], 'N_v': zo['N_v'], 'H': zo['H'], 'M': zo['M'], 'U': zo['U'],
              'N': zo['N'], 'I_per_reason': zo['I_per_reason'], 'labels': labels}
        oD = res['hasD']['OUTER']
        cl = res['cl']['OUTER']
        for k, ck in (('n_defined_ratio', 'n_def'), ('n_late_gate', 'n_late'), ('n_null_ratio', 'n_null')):
            e3[k] = na(codes_d) if oD else cl[ck]
        out['e3_line'] = e3
        # descriptive lines
        on = res['onset']
        out['descriptive'] = {'onset_radius': (na(codes_d) if on == 'NA' else
                                               ({'id': on, 'R_q': self.rad[on][0]} if on else 'NONE')),
                              'onset_comparison': 'k* (A12: wavelengths of tens of kpc), comparison only',
                              'DT_T1a_trend': 'NOT_COMPUTED'}
        out['invalid_list'] = self.invalid_list(rows, codes_d)
        out['a15'] = self.a15(out, res, rows_out, codes_d)
        self._orig_k = None
        out['alternatives'] = self.alternatives_out(alt_info, stage0, labels)
        out['p8_report'] = self.p8_report(P, alt_info, labels) if P['P8'] is True else None
        out['stage0'] = dict(stage0, comparison=dict(s0g_detail, labels=labels) if isinstance(s0g_detail, dict) else s0g_detail)
        if self.phase == PHASE2:
            out['agreement'] = self.agreement(rows_out, out['e3_line']['value'], out['patterns_holding'], out['headline'])
        return out

    def stage0_block(self, res, rows, alt_info, labels):
        """C-6.3 status and the DT-S0G comparison, mapped to R-DRIFT's state."""
        st, cls_ = self.s0_status, self.s0_cls
        alt_codes = self.codes_alt('STAGE0_GRID_OUTER')
        if self.phase == PHASE1:
            return st, 'NOT_EVALUATED_BEFORE_FREEZE', ['NOT_IN_PHASE_1'], None, None
        if cls_ == 'TWIN_INPUT_DEFECT':   # R-DRIFT's code list names the defective source (record or frozen block)
            return dict(st, twin='TWIN_INPUT_DEFECT'), 'TWIN_INPUT_DEFECT', list(st['reasons']), None, cls_
        if cls_ != 'EVALUATED':
            return st, cls_, st['reasons'], None, cls_
        if alt_codes:
            return dict(st, twin='TWIN_INPUT_DEFECT'), 'TWIN_INPUT_DEFECT', alt_codes, None, cls_
        state, tw, trows, why = self.alt_res.get('STAGE0_GRID_OUTER', ('TWIN_INPUT_DEFECT', None, None, 'absent'))
        if state is not None:
            return dict(st, twin=state, twin_detail=why), state, [], None, cls_
        a = alt_info['by_name'].get('STAGE0_GRID_OUTER')
        cls_out, _res = self.classify_twin(a, trows, labels)
        if res['hasD']['OUTER']:
            return dict(st, label='SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), '
                                  'not a recalibration', twin_classification=cls_out), None, \
                self.codes('ROW', 'GATE'), na(self.codes('ROW', 'GATE')), cls_
        comp, detail = self.s0g_compare(rows, trows)
        within = {'n': len(trows), 'within_error': sum(1 for r in trows if r['kind'] == 'H')}
        detail = dict(detail, result=comp)
        return dict(st, label='SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), not a '
                              'recalibration', twin_classification=cls_out, stage0_within_error_distribution=within,
                    denominator=8), comp, [], detail, cls_

    def codes_alt(self, name):
        return sorted({k[0] for k in self.stops if k[1] == 'ALT' and k[2] == name})

    def alternatives_out(self, alt_info, stage0, labels):
        """C-6.1/C-6.2/C-I4: every alternative under its name, in declared order, STAGE0 last; never the headline."""
        out = []
        ref_li = self.ref_member['log_index']
        for n in ALT_ORDER[1:5] + (DISTANCE_ALT,):
            a = alt_info['by_name'].get(n)
            if n == DISTANCE_ALT and a is None:
                continue
            e = {'name': n}
            if self.phase == PHASE1 and n == 'ORIGINAL_K':
                e.update(status=NA_KEY, reason='ORIGINAL_K_NOT_AVAILABLE_IN_PHASE_1 (I-4; budget 0)')
                out.append(e)
                continue
            codes = self.codes_alt(n)
            if codes:
                e.update(status='TWIN_INPUT_DEFECT', codes=codes)
                out.append(e)
                continue
            if n == DISTANCE_ALT or a.get('status') != 'EVALUATED_BEFORE_FREEZE' or a.get('scored') is not True:
                if n == 'ORIGINAL_K' and a.get('status') != 'EVALUATED_BEFORE_FREEZE':
                    e.update(status=NA_KEY, reason='ORIGINAL_K changed to NOT_EVALUATED (A16.2): NOT_AVAILABLE')
                else:
                    e.update(status=a.get('status'), note=NOT_EVAL_NOTE)
                out.append(e)
                continue
            state, tw, trows, why = self.alt_res[n]
            if state == 'TWIN_INVALID':
                mwc = a.get('member_within_error_counts')
                e.update(status='TWIN_INVALID', member_within_error_counts=mwc if isinstance(mwc, dict) else NA_KEY)
            elif state is not None:
                e.update(status=state, detail=why)
            else:
                c, _r = self.classify_twin(a, trows, labels)
                e.update(status='EVALUATED_BEFORE_FREEZE', twin_log_index=ref_li, classification=c,
                         headline=False, note='never triggers, confirms or refutes a PRIMARY reading (C-6.1)')
                self._orig_k = c if n == 'ORIGINAL_K' else getattr(self, '_orig_k', None)
            out.append(e)
        s = {'name': 'STAGE0_GRID_OUTER'}
        s.update({k: v for k, v in stage0.items() if k in ('status', 'reasons', 'twin', 'label')})
        out.append(s)
        return out

    def invalid_list(self, rows, codes_d):
        """C-4 / C-8 item 6: INVALID rows per reason, with each row's zone and, for gate rows, the gate's status; LATE
        rows marked GATE_AFTER_PREDICTIONS; the outer-gas cut's truncation radius and dropped mass fraction."""
        per = {}
        for r in rows:
            if r['kind'] in ('I', 'L'):
                per.setdefault(r['reason'], []).append({'id': r['id'], 'zone': r['zone'], 'gate_status': r['gate_status'],
                                                        'GATE_AFTER_PREDICTIONS': r['kind'] == 'L'})
        out = {'per_reason': per, 'rows_not_available': sorted(r['id'] for r in rows if r['kind'] is None)}
        if out['rows_not_available']:
            out['rows_not_available_codes'] = codes_d
        if 'QUERY_BEYOND_OUTER_GAS_CUT' in per:
            rd = self.docs.get('root_disclosures')
            cut = rd.get('outer_gas_cut_report') if isinstance(rd, dict) else None
            out['outer_gas_cut_report'] = cut if cut is not None else na(['CUT_REPORT_NOT_SUPPLIED'])
        return out

    def a15(self, out, res, rows_out, codes_d):
        """C-5.1 E1 (a) and (b), C-5.2 E2; labelled COMPARISON, never a fit (C-5.4)."""
        zi, zo = out['zones']['INNER'], out['zones']['OUTER']
        sub = [{'id': r['id'], 'tier': r['tier'], 'near': r['near']} for r in rows_out if r['id'] in E1_SUBTABLE_IDS]
        late_o = res['cl']['OUTER']['n_late']
        e2 = {'label': 'COMPARISON with A15 E2', 'OUTER_FAILURE': out['outer_failure'],
              'S_OUTER': out['e3_line']['S_OUTER'],
              'OUTER_NO_MISS': self.o3(res['ONM'], codes_d),
              'P9': out['patterns']['P9'], 'OUTER_I_per_reason': zo['I_per_reason'],
              'OUTER_LATE_gate_count': na(codes_d) if res['hasD']['OUTER'] else late_o}
        if e2['OUTER_NO_MISS'] is True:
            e2['note'] = 'OUTER_NO_MISS runs against the A15 E2 expectation'
        return {'E1': {'label': 'COMPARISON with A15 E1', 'a': {'H': zi['H'], 'M': zi['M'], 'N': zi['N'],
                                                                 'Q03_Q15': sub, 'near_label': NEAR_LABEL},
                       'b': na(['NO_PRE_FREEZE_BARYONIC_NEWTONIAN_CARRIER_M11'])},
                'E2': e2, 'E3': 'see e3_line'}

    def p8_report(self, P, alt_info, labels):
        """C-3.2 P8: the mandatory report, ORIGINAL_K's twin classification for OUTER and the T120L C3 record (M-13:
        per_grid.T120L.C3_max_e and C3_PASS, with A27's provisional label and C1_effective_PASS false disclosed)."""
        if self.phase == PHASE1:
            ok = na(['ORIGINAL_K_NOT_AVAILABLE_IN_PHASE_1'])
        else:
            c = getattr(self, '_orig_k', None)
            ok ={'OUTER': c['zones']['OUTER'], 'outer_failure': c['outer_failure'],
                  'patterns_holding': c['patterns_holding']} if c is not None else na(['ORIGINAL_K_TWIN_NOT_CLASSIFIED'])
        c3 = self.docs.get('c3_record')
        try:
            t = c3['per_grid']['T120L']
            if not is_num(t['C3_max_e']) or not isinstance(t['C3_PASS'], bool):
                raise TypeError
            c3o = {'C3_max_e': t['C3_max_e'], 'C3_PASS': t['C3_PASS'],
                   'disclosures': ['A27: formally provisional until aggregate_v003 is reviewed',
                                   'the same record reads C1_effective_PASS false on 12 TRUNCATION_SHAPE rings (D-3)']}
        except (TypeError, KeyError):
            c3o = na(['C3_RECORD_NOT_AVAILABLE_M13'])
        return {'ORIGINAL_K_twin_OUTER': ok, 'T120L_C3_record': c3o,
                'note': 'changes neither the headline nor any status'}

    def headline_out(self, score):
        """C-I5: the freeze module's headline, echoed (this document never alters it)."""
        h = score.get('headline') if isinstance(score, dict) else None
        if not isinstance(h, dict):
            return na(['FIELD_DEFECT_OUTSIDE_ROWS'])
        keep = ('member_within_error_counts', 'reference_member_id', 'reference_member_log_index',
                'reference_within_error_count', 'n_members', 'n_members_valid')
        return {k: h.get(k, NA_KEY) for k in keep}

    def fallback_out(self):
        """C-8 item 10: under the fallback, the pre-prediction classification and every POST-PREDICTION change (root's
        fallback record, echoed)."""
        fb = self.docs.get('fallback')
        if self.b['inputs']['fallback'] is None:
            return {'applies': False}
        if not isinstance(fb, dict) or fb.get('schema') != 'FALLBACK_RECORD_C4V001' or not isinstance(fb.get('applies'), bool):
            return na(['FALLBACK_RECORD_DEFECT'])
        return fb

    def header(self, score):
        """C-8 item 1: the header (classifier-computed items plus the root disclosures, echoed)."""
        pi = self.docs.get('phase_inputs')
        h = {'phase': self.phase, 'manifest_phase_derived': self.manifest_phase,
             'sealed_text_sha256': self.b['sealed']['text']['sha256'],
             'classifier_sha256': self.b['sealed']['classifier']['sha256'],
             'freeze_manifest_sha256': self.shas.get('freeze_manifest'), 'slots_sha256': self.shas.get('slots'),
             'module_sha256': self.b['module_sha256'],
             'roster_sha256': {n: v[2] for n, v in self.rosters.items()},
             'tsr_records': {'flag_record_sha256': self.shas.get('tsr_flag_record'),
                             'support_record_sha256': self.shas.get('tsr_support_record'),
                             'compare_sha256': self.shas.get('ntest_compare'), 'n1_record_sha256': N1_SHA,
                             'gl_node_record_sha256': NODE_SHA},
             'gate_status_list': self.gate_list_out if self.gate_list_out is not None else na(['GATE_STATUS_LIST_DEFECT']),
             'freeze_status': score.get('freeze_status') if isinstance(score, dict) else NA_KEY,
             'field_map': self.field_map_status,
             'disclosures_D1_D3': ['D-1: stage-0 outcome S0-FAIL-RHAT; the sealed k = 0 drift reading is SUPPORTED; its '
                                   'causal gloss is UNTESTED (A63; A65.4)',
                                   'D-2: the coefficient-grid difference (A65): a counted uncertainty for every row',
                                   'D-3: N1 fails strictly at TRUNCATION_SHAPE ordinal 15; the one flagged row is '
                                   'NGC3198-Q25 (A66; 0550; A90)'],
             'root_disclosures': self.docs.get('root_disclosures') if isinstance(self.docs.get('root_disclosures'), dict)
             else na(['ROOT_DISCLOSURES_NOT_SUPPLIED'])}
        if isinstance(score, dict):
            h['score_echo'] = {k: score.get(k, NA_KEY) for k in ('manifest_file_sha256_expected',
                                                                 'manifest_file_sha256_actual',
                                                                 'registration_file_sha256', 'manifest_sha256_self')}
        if self.phase == PHASE1:
            h['phase1'] = {'label': LABEL_P1, 'phase1_header': pi.get('phase1_header') if isinstance(pi, dict) else NA_KEY,
                           'l1_sha256': self.shas.get('l1_record')}
        if self.phase == PHASE2:
            h['commitment_status'] = self.commitment()
            h['agree_record_sha256'] = self.shas.get('agree_record')
            h['phase1_classification_sha256'] = self.shas.get('phase1_classification')
            h['attestation_scope'] = P1_ATTEST_NOTE
        st, _c = self.stage0_status()
        h['stage0_status'] = st
        return h


def synthesize_score(man):
    """C-1.1 pre-score checks run 'on a synthetic score built from the frozen member arrays': a score_after_freeze-shaped
    object (v003g 48a1e48a _score_members / _band_rows / alternatives) with the synthetic target pair (0.0, 1.0) on
    every row. It carries no target; it exists only so that every stop condition can be checked before target access."""
    ids = list(man['query_ids'])
    bound = [(0.0, 1.0)] * len(ids)

    def ladder(q, predicted, row_valid, reg):
        r = {'id': q, 'observed_speed_km_s': 0.0, 'quoted_sigma_km_s': 1.0, 'predicted_speed_km_s': predicted,
             'sigma_ratio': None, 'row_notes': []}
        if predicted is not None:
            x = predicted / 1.0
            r['sigma_ratio'] = x if math.isfinite(x) else None
        valid = bool(row_valid and predicted is not None)
        within = bool(valid and r['sigma_ratio'] is not None and abs(r['sigma_ratio']) <= 1.0)
        r['valid'], r['within_error'] = valid, within
        if reg is not None:
            r.update(status='INVALID', prediction=None, registered_reason=reg['reason'], score_status='INVALID_AS_MISS',
                     tier='MISS_WORST_TIER')
        else:
            r.update(status='VALID' if valid else 'UNEVALUATED_OR_REFUSED', prediction=predicted, registered_reason=None,
                     score_status='HIT' if within else 'MISS', tier='WITHIN_ERROR' if within else 'MISS_WORST_TIER')
        return r

    def score_members(members, sel):
        out = []
        for m in members:
            rows = [ladder(ids[j], m['speeds_km_s'][j], m['row_valid'][j], m['row_registration'][j]) for j in sel]
            out.append({'member_id': m['member_id'], 'log_index': m['log_index'], 'role': m.get('role'),
                        'evaluated': m.get('evaluated'), 'member_valid': m['member_valid'], 'rows': rows})
        return out

    allj = list(range(len(ids)))
    members = score_members(man['members'], allj)
    ref_id = man['reference_member']['member_id']
    ref = [m for m in members if m['member_id'] == ref_id][0]

    def band(rows_in, lo_k, hi_k):
        out = []
        for j, q in enumerate(ids):
            r = rows_in[j]
            lo, hi, valid = r[lo_k], r[hi_k], r['valid']
            obs, sig = bound[j]
            ov = bool(valid and lo is not None and hi is not None and lo <= obs + sig and hi >= obs - sig)
            out.append({'id': q, 'valid': bool(valid), 'band_overlaps_error_bar': ov})
        return out

    env_rows = man['pointwise_envelope']
    label = env_rows[0]['label'] if env_rows and isinstance(env_rows[0], dict) else None
    sens = man['sensitivity']
    alts = []
    for a in man['alternatives']['declared']:
        rec = {'name': a['name'], 'kind': a['kind'], 'status': a['status'],
               'role': 'PRIMARY' if a['name'] == man['alternatives']['primary'] else 'NON_PRIMARY'}
        if a['name'] == 'STAGE0_GRID_OUTER':
            rec['scoring_scope'] = {'query_ids': list(a['scoring_scope']['query_ids'])}
        if rec['role'] == 'PRIMARY':
            rec['scored'] = True
        elif a['status'] == 'EVALUATED_BEFORE_FREEZE':
            am = man['alternative_results'][a['name']]['members']
            sel = [ids.index(q) for q in rec['scoring_scope']['query_ids']] if 'scoring_scope' in rec else allj
            rec.update(scored=True, members=score_members(am, sel))
        else:
            rec.update(scored=False, note=NOT_EVAL_NOTE)
        alts.append(rec)
    return {'freeze_status': man['freeze_status'], 'incomplete_reasons': list(man['incomplete_reasons']),
            'headline': {'reference_member_id': ref_id, 'reference_member_log_index': ref['log_index']},
            'members': members, 'pointwise_envelope': {'label': label, 'rows': band(env_rows, 'band_low_km_s',
                                                                                    'band_high_km_s')},
            'sensitivity': {'rows': band(sens['per_query'], 'box_limited_band_low_km_s', 'box_limited_band_high_km_s')},
            'alternatives': alts}


def classify_bundle(bundle_path):
    """Entry point: one input bundle in, one canonical JSON output (bytes) out."""
    run = Run(bundle_path)
    try:
        run.load_bundle()
    except BundleError as exc:
        return canonical({'schema': OUT_SCHEMA, 'classifier': NAME, 'refused': True, 'reason': str(exc)})
    try:
        return canonical(run.run())
    except Exception as exc:   # noqa: BLE001 -- fail closed and visibly: an internal error is never a classification
        return canonical({'schema': OUT_SCHEMA, 'classifier': NAME, 'refused': True,
                          'reason': 'INTERNAL_ERROR: %s: %s' % (type(exc).__name__, str(exc)[:300])})


def main(argv):
    if len(argv) != 3:
        sys.stderr.write('usage: classifier_a_c4v004.py BUNDLE.json OUT.json\n')
        return 2
    data = classify_bundle(argv[1])
    with open(argv[2], 'xb') as f:
        f.write(data)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
