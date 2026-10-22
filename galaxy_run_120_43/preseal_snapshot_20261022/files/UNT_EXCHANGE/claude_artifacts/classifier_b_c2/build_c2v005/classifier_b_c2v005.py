#!/usr/bin/env python3
"""classifier_b_c2v005 -- the M-12 classifier B for the miss-reading prereg r3a.

c2v005 applies V006 A190: the producers' bytes are the contract for their records (ruling 1), read from
freeze v003g 48a1e48a (score_after_freeze, the frozen manifest, row_registration), phase1 d64351ec / 7d891ff7 (the L1
band and AT1 records) and the STAGE0 successor d260ee30.  The eight B_DEFECTs: RC3 (score alternatives[] entry
form), RC4 and its downstream (the prescore synthetic score built as score_after_freeze builds it from the frozen
manifest), RC5/RL9 (row_registration {status: INVALID, reason, registration}), RC7 (L1 band label and rows), RC8
(AT1 at0), RL5B (the null-phase STAGE0 stop in prescore).  Ruling 2: the seal candidate's printed form for the
detail-wording items.  Ruling 3: classifier A's printed form for a field-map partial rename and a non-list
pins.input_files.
c2v004 was the fix round of c2v003: RC1 (the phase1 tool and the STAGE0 successor bind at the full sha256 of
phase1_c2v002.py, phase1_c2v003b.py and prediction_freeze_c2v003g_stage0_c2v002.py, from those files' bytes), RC2
(the N-test compare is read in the encoding of its registered bytes, NGC_NTEST_COMPARE_C2V002), RL5 (a null phase
that reads a missing or malformed STAGE0 status record also prints the STAGE0 alternative's stop).
c2v003 was the fix round of c2v002: RC2 (each PREREG L194 compare condition is its own TSR detail;
the support native_ring is the compare's failing ordinal-15 TRUNCATION_SHAPE record), RC3 (the
phase1 tool and the STAGE0 successor bind at the full sha only), RC4 (the frozen STAGE0 block
carries exactly the successor module's key sets), RC7 (prescore checks every stop on the
synthetic score the frozen manifest determines).  c2v002 was the fix round of c2v001 (RC02,
RC13, RC15).

Built by Claude2 behind the A176 information barrier from the basis texts
(PREREG_MISS_READING_R3A, ROOT_ITEMS_R3A, CLAUSE_SOURCE_MAP_R3A), the classifier A
README texts c4v001-c4v004, INPUT_CONTRACTS_C4V004, the output schema c4v003 (with the
c4v004 delta) and V006 A133/A154/A168/A173/A176, on Codex1's prep_v001 kernels (pinned
by sha256 in KERNEL_PINS, loaded from the verified bytes, never modified).

CLI:  python3 -I -B classifier_b_c2v005.py BUNDLE.json OUT.json   (OUT is created exclusively)
Entry point: classify_bundle(bundle_path) -> bytes (canonical JSON plus one newline).
Stdlib only.  Target-blind: it reads only the files the bundle pins.
"""
import ast
import hashlib
import json
import math
import os
import sys
import types
from itertools import product
from pathlib import PurePosixPath

NAME = 'classifier_b_c2v005'
OUT_SCHEMA = 'CLASSIFIER_A_OUTPUT_C4V001'
NA = 'NOT_AVAILABLE'

# ---------------------------------------------------------------------------
# Kernels (Codex1 prep_v001, byte copies; sha256 from bytes, V089 checkpoint)
# ---------------------------------------------------------------------------
KERNEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kernels')
KERNEL_PINS = {
    'input_primitives.py': 'f4c7a7724dd9e0092f50135dde9afa6dd483ea5915e5851a7e0965824c0ae594',
    'bundle_boundary.py': 'efc2d645aa41e4be44426e6b817237da0cb4eb7c442ef32a92cdd556f3f7536b',
    'record_shapes.py': '77e1f601a9b82f76deaf2ef879d0b8d1ceebd18772f8366e5452717f44876677',
    'root_contracts.py': '52a2e32cfe71937545366446f15ad4fe01439e673d50fc65ded5ee75b38b8b58',
    'phase_paths.py': 'fe9778d71f91efd7123e5452d485f5023026ae4239f2a2a8725bc63ad7de4482',
    'terminal_forms.py': '6f4e683e8104e1903dfd1262924ee0746eea44d568f4fcaa14de0a768ec59b9b',
    'stage0_exception_claim.py': '835f6d95674a49181cf1db1669d47fe822878e5408248542cfef059ef9c76012',
    'zone_kernel_v002.py': 'f19125c5d7427feabc87468ecef95209f052a673db983afc70ee0e6ea583cb67',
    'pattern_kernel.py': 'f9d9a4ddd813c78fbb2aec417c63c8b896085aa466c2d2a824ade035cd84c69d',
    'reading_relations.py': '8229eef3946ec93c1e57dda68f2d42b2c5a041281d00609b906068dc9f25f266',
    'row_scopes.py': '60fe8cc603ce4b139dbd7c62b7002263f3ee10293bb29bd26d1fd8289c12828f',
    'partial_counts.py': 'e813d188f5a3c0baf2bddb77703ad7f73b2eb018cea99d14ad94f42a8155c6a0',
    'partial_zone.py': '353a7e1479af341f86a8c661c43d1848125b6b4724ac2546588f040f506bef12',
    'partial_relations.py': '294490b5b289d60c2c6e757d992ae987031a3486a7876c6cc620d504301c6786',
    'band_column_v002.py': '77eafe9d270545789974a80b9de7987e08e751757e8d9b30afa1aff3283c43ce',
}
# load order respects the kernels' own imports (pattern_kernel -> zone_kernel_v002,
# row_scopes -> reading_relations, partial_zone -> partial_counts)
KERNEL_ORDER = ['input_primitives', 'bundle_boundary', 'record_shapes', 'root_contracts',
                'phase_paths', 'terminal_forms', 'stage0_exception_claim', 'zone_kernel_v002',
                'pattern_kernel', 'reading_relations', 'row_scopes', 'partial_counts',
                'partial_zone', 'partial_relations', 'band_column_v002']


class KernelPinError(RuntimeError):
    pass


class ConsistencyError(RuntimeError):
    """B's engine and a Codex1 kernel disagree on a fully determined input (fail closed)."""


class _K:
    pass


K = _K()


def load_kernels():
    if getattr(K, 'loaded', False):
        return K
    for name in KERNEL_ORDER:
        path = os.path.join(KERNEL_DIR, name + '.py')
        with open(path, 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != KERNEL_PINS[name + '.py']:
            raise KernelPinError('%s does not hash to its pin' % name)
        mod = types.ModuleType(name)
        mod.__file__ = path
        sys.modules[name] = mod
        exec(compile(raw, path, 'exec'), mod.__dict__)
        setattr(K, name, mod)
    K.loaded = True
    return K


# ---------------------------------------------------------------------------
# Registered constants (text of record and contracts)
# ---------------------------------------------------------------------------
QIDS = ['NGC3198-Q%02d' % i for i in range(1, 44)]
ZONES = ('INNER', 'TRANSITION', 'OUTER')
ZONE_OF = {}
for _i, _q in enumerate(QIDS):
    ZONE_OF[_q] = 'INNER' if _i < 24 else ('TRANSITION' if _i < 35 else 'OUTER')
OUTER_IDS = QIDS[35:]
Q25 = 'NGC3198-Q25'
E1_SUBTABLE = QIDS[2:15]
BUILTIN_REASONS = ('QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT',
                   'QUERY_OUTSIDE_RETAINED_SUPPORT')
SCORE_STATUSES = ('HIT', 'MISS', 'INVALID_AS_MISS')
ROW_FIELDS = ('score_status', 'within_error', 'sigma_ratio', 'registered_reason', 'status')
ENVELOPE_PREFIX = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'
COMPARE_SHA = '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'
# c2v004 RC2: the encoding of the registered compare bytes (6f095f64...e30e9, PREREG L109, L824; a target-free model
# record, ROOT_ITEMS L204-L205), as root states it from those bytes (README_CLASSIFIER_B_C2V003 P-2): its schema
# string, its list of failing TRUNCATION_SHAPE rings and its list of failing non-TRUNCATION_SHAPE rings.  Each ring
# record is an object with an integer `ordinal` and a string `classification` (the registered ordinal-15 record also
# carries S_over_theta, criterion_over_theta, criterion, R_kpc and radial_support).
COMPARE_SCHEMA = 'NGC_NTEST_COMPARE_C2V002'
COMPARE_TS_RINGS = 'failing_TRUNCATION_SHAPE_rings'
COMPARE_OTHER_RINGS = 'failing_non_TRUNCATION_SHAPE_rings'
TS_CLASS = 'TRUNCATION_SHAPE'
N1_SHA = '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70'
NODE_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
# the first 8 hex printed by 'flag record %s is not %s' (OUTPUT_CONSTANTS_C4V003, TSR_FLAG_TABLE_MISMATCH note)
FLAG_PIN_TEXT = {'ntest_compare_pin': '6f095f64', 'n1_record_pin': '8867c376', 'gl_node_record_pin': 'ec1dcca5'}
R14_KPC = 9.901810628740723
R16_KPC = 10.911721936765339
# c2v003 RC3: a phase1 tool pin binds only when its sha256 is exactly (all 64 hex) the sha of the phase1_c2v002 tool
# (d64351ec...) with module phase1_c2v002, or of the phase1_c2v003b tool (7d891ff7...) with module phase1_c2v003b;
# anything else is PHASE1_TOOL_PIN_DEFECT (README c4v002 L34, L69; c4v003 L39, L58, L74).  The STAGE0 successor binds
# only at exactly the sha of d260ee30... (c4v003 L42, L73), else STAGE0_SUCCESSOR_PIN_NOT_BOUND.
# c2v004 RC1 (README_CLASSIFIER_B_C2V003 P-1 closed): the values are the sha256 of exactly three files' bytes, as
# root states them (a value, not a ruling; V006 A154 L1137-L1141, A168 L1509, L1511; INPUT_CONTRACTS_C4V004 L13;
# PREREG L544).  Computed by the c2v004 builder from the bytes of claude_artifacts/phase1_c2/phase1_c2v002.py
# (MODULE L48 'phase1_c2v002'), phase1_c2/phase1_c2v003b.py (MODULE L99 'phase1_c2v003b') and
# stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py (MODULE_NAME L66), 2026-10-20 (date -u).
# _check_pin_tables still checks the form of every value at every run.
PHASE1_TOOL_SHA256 = {
    'd64351ecc06c61e99e2d7253c5d4311617fc1f64d34d37523102ed32720a6754': 'phase1_c2v002',
    '7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4': 'phase1_c2v003b',
}
PHASE1_MODULES = ('phase1_c2v002', 'phase1_c2v003b')
PHASE1_V003B = 'phase1_c2v003b'
STAGE0_SUCCESSOR_SHA256 = 'd260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0'
MANIFEST_V003G = 'FREEZE_MANIFEST_C2V003G'
MANIFEST_SUCC = 'FREEZE_MANIFEST_C2V003G_STAGE0_C2V002'
STAGE0_MODULE = 'prediction_freeze_c2v003g_stage0_c2v002'
STAGE0 = 'STAGE0_GRID_OUTER'
DIST_ALT = 'DDO154_DISTANCE_NUISANCE'
ALT_ORDER = ('ORIGINAL_K', 'ML_3p6_0.4', 'ML_3p6_0.6', 'GL10_SOURCE_GAUSS_ORDER')
PRIMARY_ROSTER_NAMES = ('BR_A_F10_PRIMARY', 'PRIMARY')
ROSTER_SCHEMA = 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001'
SUPPORT_SCHEMA = 'UNT_ROOT_TSR_SUPPORT_CX3V001'
SUPPORT_KEYS = {'schema', 'mode', 'target_free', 'before_target_access', 'point_key',
                'slots_pin', 'ntest_compare_pin', 'rule_id', 'rings'}
L1_SCHEMA = 'PHASE1_L1_C2V001'
AT1 = 'PHASE1_AT1_C2V001'
AT0A = 'PHASE1_AT0A_C2V001'
AT0B = 'PHASE1_AT0B_C2V001'
AGREE_OUTCOMES = ('COVERED', 'SUPERSEDED', 'AGREEMENT_DEFECT')

S0_RNF = 'STAGE0_RECEIPT_NOT_FINISHED'
S0_NSS = 'NO_SEALED_SUCCESSOR'
S0_RA4 = 'RECEIPTS_AFTER_STEP4'
NEBF = 'NOT_EVALUATED_BEFORE_FREEZE'
EBF = 'EVALUATED_BEFORE_FREEZE'
EREF = 'EVALUATED_REFUSED'
SRC_RECORD = 'STAGE0_STATUS_RECORD_C4V003'
SRC_BLOCK = 'FREEZE_MANIFEST_STAGE0_STATUS_BLOCK'
STAGE0_RECORD_KEYS = ('schema', 'phase', 'sealed_successor', 'step4_start_utc', 'members',
                      'rule_a_receipts_finished', 'rule_b_successor_sealed',
                      'receipts_before_step4', 'receipt_refusals', 'evaluation_refusals',
                      'reading', 'reasons', 'post_score_exploratory')
STAGE0_MEMBER_PROJ = ('log_index', 'terminal_status', 'written_utc', 'finished', 'before_step4')
# The block keys and member-row keys classifier B reads (contract texts).  c2v003 RC4: the block must carry exactly
# the successor module's own key sets (STAGE0_BLOCK_KEYS, STAGE0_MEMBER_KEYS, read from the sealed successor's
# bytes, Run.successor_key_sets); those must contain these.
STAGE0_BLOCK_REQUIRED = ('alternative', 'module', 'successor_module_sha256', 'status_record',
                         'diagnostics') + STAGE0_RECORD_KEYS[1:]
STAGE0_BLOCK_MEMBER_REQUIRED = ('member_id', 'receipt', 'custody_ok', 'defects') + STAGE0_MEMBER_PROJ

LABEL_P1 = 'PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE)'
LABEL_INCOMPLETE = 'PROVISIONAL (FREEZE_INCOMPLETE)'
LABEL_NGATE = 'PROVISIONAL (N_GATE_NOT_OPEN)'
LABEL_EXPL = 'EXPLORATORY (PHASE 2 NOT AS COMMITTED)'
FALLBACK_LABELS = ('EXPLORATORY (post-prediction)', 'POST-PREDICTION (CLASSIFIER)')
D2_NOTE = ('D-2/A65.4: counted coefficient-grid uncertainty; not converted into a number; '
           'widens no sigma; changes no tier')
NEAR_LABEL = 'envelope overlaps the error bar'
SENS_LABEL = 'conditional on trial values'
BAND_LABEL = 'PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER'
BAND_CONDITION = 'conditional on A13 (the fixed DDO154 distance 4.04 Mpc and inclination 66 deg)'
DISCLOSURES = [
    'D-1: stage-0 outcome S0-FAIL-RHAT; the sealed k = 0 drift reading is SUPPORTED; its causal gloss is UNTESTED (A63; A65.4)',
    'D-2: the coefficient-grid difference (A65): a counted uncertainty for every row',
    'D-3: N1 fails strictly at TRUNCATION_SHAPE ordinal 15; the one flagged row is NGC3198-Q25 (A66; 0550; A90)',
]
P2_ATTEST = ('Phase 2 attestation covers only the Phase-2-only output values '
             '(the calls not re-bound from Phase 1)')
E3_NEG = 'TESTED-NEGATIVE (A15 E3 scope)'
E3_NOTNEG = 'NOT_NEGATIVE_AT_OUTER'
E3_NT = 'NOT_TESTABLE'
NOT_EVAL_NOTE = 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'
TWIN_NOTE = 'never triggers, confirms or refutes a PRIMARY reading (C-6.1)'
S0_LABEL = ('SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), '
            'not a recalibration')
TWIN_IDS_DIFFER = 'twin ids differ from its scope'
P8_NOTE = 'never "all hit": INVALID rows still score as misses (C-4)'
NO_RUN_NOTES = {
    'NO_NGC_CALL': 'no NGC call: no classification (engine terminal status or NO_IDENTIFIED_DIRECTION; A133 1.3)',
    'AT0A_FAILED': 'AGREEMENT_DEFECT (prefix): no Phase-1 classification',
    'HALTED': 'Phase 2 reported HALTED (A133 3 rule (c))',
}
RUN_STATUS_PHASES = {'SCORED': ('PHASE_1', 'PHASE_2'), 'NO_NGC_CALL': ('PHASE_1', 'PHASE_2'),
                     'AT0A_FAILED': ('PHASE_1',), 'HALTED': ('PHASE_2',)}
PATTERN_IDS = ('P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10',
               'P11', 'P11g', 'P12', 'P13', 'P14', 'P15')
PATTERN_NAMES = {'P0': 'INVALID rows', 'P1': 'OUTER_DEFICIT', 'P1g': 'P1 flag GROWING',
                 'P2': 'OUTER_EXCESS', 'P3': 'INNER_EXCESS', 'P4': 'INNER_DEFICIT',
                 'P5': 'TRANSITION_ONSET', 'P6': 'GLOBAL_OFFSET', 'P7': 'SCATTERED',
                 'P8': 'NO_MISS_AMONG_VALID_ROWS', 'P9': 'OUTER_UNTESTABLE', 'P10': 'TSR_MISS',
                 'P11': 'OUTER_MIXED', 'P11g': 'P11 flag CROSSING', 'P12': 'INNER_MIXED',
                 'P13': 'TRANSITION_MISS', 'P14': 'OUTER_UNSIGNED', 'P15': 'INNER_UNSIGNED'}
READINGS = ('R-MF', 'R-UT1', 'R-REACH', 'R-HIST', 'R-DRIFT', 'R-S1', 'R-GRID', 'R-NAX',
            'R-GEFF', 'R-ML', 'R-SPEC', 'R-GEO', 'R-TSR')
TRIGGERS = {
    'R-MF': ('OF', 'P3', 'P4', 'P12', 'P15', 'P13', 'P6', 'P7', 'MM:INNER', 'MM:TRANSITION', 'MM:OUTER'),
    'R-UT1': ('OF',), 'R-REACH': ('OF',),
    'R-HIST': ('OF', 'P13', 'P6', 'P7', 'MM:TRANSITION', 'MM:OUTER'),
    'R-DRIFT': ('OF',), 'R-S1': ('P2', 'P11', 'P6'), 'R-GRID': ('P2', 'P11'),
    'R-NAX': ('P11', 'P14', 'P3', 'P4', 'P12', 'P15', 'P13', 'P7'),
    'R-GEFF': ('P3', 'P4', 'P12', 'P15'), 'R-ML': ('P3', 'P4', 'P12', 'P15'),
    'R-SPEC': ('P3', 'P4', 'P12', 'P15', 'MM:INNER'),
    'R-GEO': ('P3', 'P4', 'P12', 'P15', 'P6'), 'R-TSR': ('P10',),
}
TRIGGER_SCOPE = {'OF': 'OUTER', 'P2': 'OUTER', 'P11': 'OUTER', 'P14': 'OUTER',
                 'P3': 'INNER', 'P4': 'INNER', 'P12': 'INNER', 'P15': 'INNER',
                 'P13': 'TRANSITION', 'P6': 'ALL', 'P7': 'ALL', 'P10': 'FLAGGED',
                 'MM:INNER': 'INNER', 'MM:TRANSITION': 'TRANSITION', 'MM:OUTER': 'OUTER'}
SIGN_SCOPE = {'R-MF': 'sign-free', 'R-UT1': 'deficit-type', 'R-REACH': 'deficit-type',
              'R-HIST': 'sign-free', 'R-DRIFT': 'sign-free'}
PRIOR = {
    'R-MF': ['for: A15 E2, which expected an outer deficit', 'for: A41'],
    'R-UT1': ['against: A41 item 3 (FORMAL + TESTED): no gate-consistent typing gives an attractive tail, and the spec-compliant T(0+) is finite and repulsive on current estimates'],
    'R-REACH': [], 'R-HIST': [],
    'R-DRIFT': ['for: the sealed k = 0 drift reading is SUPPORTED (A63)',
                'against: its causal gloss is UNTESTED (A65 check R-3)'],
    'R-S1': [],
    'R-GRID': ["against: T120L passes C2, C3, C4 and C1' (A27)",
               "against: the production N-tests N0, NQ, N2 and N3' pass (A90)"],
    'R-NAX': [], 'R-GEFF': [],
    'R-ML': ['the ML_3p6 alternatives are NOT_EVALUATED_BEFORE_FREEZE (slots V003)'],
    'R-SPEC': [], 'R-GEO': [],
    'R-TSR': ['against: route B consumes the azimuthal mean, so the phi-spread S enters no row directly (A66.2; A42 TESTED)'],
}
DECIDING = {
    'R-UT1': ('DT-UT1', 'NOT SCHEDULED'), 'R-REACH': ('DT-U12', 'NOT SCHEDULED'),
    'R-HIST': ('DT-BHD', 'NOT SCHEDULED'), 'R-S1': ('DT-S1', 'UNTESTED'),
    'R-GRID': ('NONE_REGISTERED', 'none registered'), 'R-NAX': ('DT-NAX', 'not run'),
    'R-GEFF': ('DT-S1', 'UNTESTED'),
    'R-ML': ('DT-ALT', 'NOT_EVALUATED_BEFORE_FREEZE (M/L); DT-T1a diagnostic'),
    'R-SPEC': ('DT-T1a', 'diagnostic; never changes part 2'),
    'R-GEO': ('DT-GEO', 'NOT_EVALUATED_BEFORE_FREEZE'), 'R-TSR': ('DT-TSR', 'NOT SCHEDULED'),
}
KIND_NAME = {'H': 'HIT', 'MS': 'MISS_SIGNED', 'MN': 'MISS_NULL_RATIO', 'I': 'INVALID_AS_MISS',
             'L': 'LATE_GATE_MISS'}
MISS_KINDS = ('MS', 'MN', 'L')
FROZEN_MISS_KINDS = ('MS', 'MN')
ALL_CLASS = ('ENVELOPE_LABEL_MISMATCH', 'FIELD_DEFECT_OUTSIDE_ROWS', 'PHASE_MISMATCH',
             'QUERY_ID_DEFECT', 'REFERENCE_MEMBER_MISMATCH',
             'REFERENCE_ROW_UNEVALUATED_OR_REFUSED', 'SEAL_SHA_MISMATCH', 'ZONE_TABLE_MISMATCH')
# c2v005 (V006 A190 ruling 1): producer encodings read from the producers' bytes.
# v003g 48a1e48a score_after_freeze L4273-L4299 (d260ee30 L4829-L4855): every alternatives[] entry other than the
# PRIMARY carries role 'NON_PRIMARY'.
ROLE_NON_PRIMARY = 'NON_PRIMARY'
# v003g L4045-L4046 with L4042: a score row's status is VALID, INVALID or UNEVALUATED_OR_REFUSED (ruling 2, RC08/RL2:
# any other value is 'status wrong type').
ROW_STATUSES = ('VALID', 'INVALID', 'UNEVALUATED_OR_REFUSED')
# v003g L149 HEADLINE_CONDITIONS_KEY; the manifest carries it only in the fixed-distance mode (L3782-L3783), and
# score_after_freeze then appends its recorded alternatives (L4295-L4299).
HEADLINE_CONDITIONS_KEY = 'headline_conditions'
# c2v005 RC4: the target-free stand-in pair (observed, sigma) of the prescore synthetic score.  No prescore output
# depends on its value: prescore prints stops only, and no stop it can reach depends on a row's hit or ratio.
SYN_PAIR = (0.0, 1.0)


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def na(codes):
    return {NA: sorted(set(codes))}


def is_num(x):
    if type(x) not in (int, float):
        return False
    try:
        return math.isfinite(x)
    except OverflowError:
        return False


def is_int(x):
    return type(x) is int


def is_str(x):
    return type(x) is str and len(x) > 0


def is_hex64(x):
    return type(x) is str and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_hex64_ci(x):
    return type(x) is str and len(x) == 64 and all(c in '0123456789abcdefABCDEF' for c in x)


def is_pin(x):
    return (type(x) is dict and set(x) == {'path', 'sha256'} and is_str(x['path'])
            and is_hex64(x['sha256']))


def sign_of(r):
    return -1 if r < 0 else (1 if r > 0 else 0)


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False)


def parse_utc(s):
    """`date -u` ISO time YYYY-MM-DDTHH:MM:SS[.fff]Z -> comparable tuple, or None."""
    if type(s) is not str or not s.endswith('Z'):
        return None
    body = s[:-1]
    if body.count('T') != 1:
        return None
    d, t = body.split('T')
    dp = d.split('-')
    if len(dp) != 3 or [len(p) for p in dp] != [4, 2, 2]:
        return None
    frac = ''
    if '.' in t:
        t, frac = t.split('.', 1)
        if frac and not frac.isdigit():
            return None
    tp = t.split(':')
    if len(tp) != 3 or [len(p) for p in tp] != [2, 2, 2]:
        return None
    try:
        if not all(p.isdigit() for p in dp + tp):
            return None
        nums = tuple(int(p) for p in dp + tp)
        fr = (int(frac), 10 ** len(frac)) if frac else (0, 1)
    except ValueError:
        return None
    from fractions import Fraction
    return nums + (Fraction(fr[0], fr[1]),)


def tri_and(*vals):
    if any(v is False for v in vals):
        return False
    if any(v is None for v in vals):
        return None
    return True


def tri_or(*vals):
    if any(v is True for v in vals):
        return True
    if any(v is None for v in vals):
        return None
    return False


def median(values):
    return K.zone_kernel_v002.median(list(values))


# ---------------------------------------------------------------------------
# row registration reader (c2v005 RC5: the producer's form only; PB-3's tolerant reader is withdrawn)
# ---------------------------------------------------------------------------
REG_UNREADABLE = object()


def _reg_entries(rr, manifest_ids, ids):
    """c2v005 RC5: a member's frozen row_registration in the producer's form is a list aligned with the manifest's
    query_ids (v003g L1937-L1950 _registered_rows_ok; L4040 reads it by row index).  -> {query id: entry} for the
    wanted ids, or None (unreadable): not a list of that length, query_ids not a list of distinct strings, or a
    wanted id that is not among them.  A query-id-keyed object or a {rows: [...]} wrapper is not the form."""
    if (type(manifest_ids) is not list or any(type(q) is not str for q in manifest_ids)
            or len(set(manifest_ids)) != len(manifest_ids)):
        return None
    if type(rr) is not list or len(rr) != len(manifest_ids):
        return None
    pos = {q: i for i, q in enumerate(manifest_ids)}
    if any(q not in pos for q in ids):
        return None
    return {q: rr[pos[q]] for q in ids}


def reg_info(e):
    """c2v005 RC5: one frozen registration entry in the producer's form (v003g L1788-L1798
    _authorized_row_registration; L1937-L1950 _registered_rows_ok; L1919-L1934 _invalid_registration_ok): null for
    a valid row; for an
    INVALID row an object with exactly the keys status, reason and registration, status 'INVALID', reason a non-empty
    string, and registration null for a built-in (rule-derived) reason or, for a gate reason, the gate pin
    {path, sha256} (sha256 64 hex, read lower-cased as v003g's _is_hex64, README c4v002 V-F1).
    -> ('VALID', None, None) | ('INVALID', reason, gate sha or None) | REG_UNREADABLE (any other entry: a missing
    registration key, a pin under another key, a bare string, ...)."""
    if e is None:
        return ('VALID', None, None)
    if (type(e) is not dict or set(e) != {'status', 'reason', 'registration'} or e['status'] != 'INVALID'
            or not is_str(e['reason'])):
        return REG_UNREADABLE
    g = e['registration']
    if g is None:
        return ('INVALID', e['reason'], None) if e['reason'] in BUILTIN_REASONS else REG_UNREADABLE
    if (type(g) is dict and set(g) == {'path', 'sha256'} and type(g['path']) is str and is_hex64_ci(g['sha256'])
            and e['reason'] not in BUILTIN_REASONS):
        return ('INVALID', e['reason'], g['sha256'].lower())
    return REG_UNREADABLE


# ---------------------------------------------------------------------------
class BundleRefused(Exception):
    pass


class S0Defect(Exception):
    pass


class Row:
    """One classified row: fixed (one kind) or defective (a set of kinds)."""
    __slots__ = ('qid', 'zone', 'radius', 'rad_text', 'fixed', 'kind', 'ratio', 'reason',
                 'gate_status', 'near', 'kinds', 'kind_reason', 'dclass', 'src')

    def __init__(self, qid):
        self.qid = qid
        self.zone = ZONE_OF.get(qid)
        self.radius = None
        self.rad_text = None
        self.fixed = True
        self.kind = None
        self.ratio = None
        self.reason = None
        self.gate_status = None
        self.near = False
        self.kinds = None
        self.kind_reason = {}
        self.dclass = None
        self.src = None

    def possible(self):
        return {self.kind} if self.fixed else set(self.kinds)


class Run:
    def __init__(self, bundle_path):
        self.bundle_path = os.path.abspath(bundle_path)
        self.base = os.path.dirname(self.bundle_path)
        self._stops = []
        self.inp = {}
        self.err = {}
        self.rawsha = {}

    # ------------------------------------------------------------- stops
    def stop(self, code, cls, detail, rows=(), alternative=None):
        self._stops.append({'code': code, 'class': cls, 'alternative': alternative,
                            'detail': [detail], 'rows': list(rows)})

    def stops_out(self):
        return K.terminal_forms.merged_stops(self._stops)

    def codes(self, *classes):
        return sorted({s['code'] for s in self._stops if s['class'] in classes})

    def fired(self, cls):
        return any(s['class'] == cls for s in self._stops)

    def alt_stopped(self, name):
        return any(s['class'] == 'ALT' and s['alternative'] == name for s in self._stops)

    # ------------------------------------------------------------- io
    def resolve(self, path):
        return path if os.path.isabs(path) else os.path.join(self.base, path)

    def read_pinned(self, pin):
        """-> (load_err or None, value, sha of bytes or None)."""
        if pin is None:
            return 'NOT_SUPPLIED', None, None
        try:
            with open(self.resolve(pin['path']), 'rb') as f:
                raw = f.read()
        except OSError:
            return 'UNREADABLE', None, None
        sha = hashlib.sha256(raw).hexdigest()
        if sha != pin['sha256']:
            return 'SHA_MISMATCH', None, sha
        try:
            return None, K.bundle_boundary.strict_json(raw), sha
        except K.bundle_boundary.Defect as e:
            return 'JSON_DEFECT:' + str(e), None, sha

    def sha_of_file(self, pin):
        try:
            with open(self.resolve(pin['path']), 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except OSError:
            return None

    def load_bundle(self):
        try:
            with open(self.bundle_path, 'rb') as f:
                raw = f.read()
        except OSError as e:
            raise BundleRefused('BUNDLE_UNREADABLE:%s' % e)
        bb = K.bundle_boundary
        try:
            x = bb.strict_json(raw)
        except bb.Defect as e:
            raise BundleRefused('BUNDLE_UNREADABLE:' + str(e))
        y = x
        # contract (README c4v002/c4v003): phase1_tool may be null; the kernel requires an
        # object, so a null is checked with a placeholder that passes that one check.
        if type(x) is dict and 'phase1_tool' in x and x['phase1_tool'] is None:
            y = dict(x)
            y['phase1_tool'] = {'sha256': '0' * 64, 'module': 'null-placeholder'}
        try:
            bb.validate_bundle(y)
        except bb.Defect as e:
            raise BundleRefused(str(e))
        self.bundle = x

    def load_inputs(self):
        for role in K.bundle_boundary.ROLES:
            err, val, sha = self.read_pinned(self.bundle['inputs'][role])
            self.err[role] = err
            self.inp[role] = val
            self.rawsha[role] = sha
        self.apply_field_map()

    # ------------------------------------------------------------- field map (C-1.1)
    def apply_field_map(self):
        pin = self.bundle['inputs']['field_map']
        if pin is None:
            self.field_map_status = 'NOT_SUPPLIED'
            return
        rec = self.inp['field_map']
        roles = [r for r in K.bundle_boundary.ROLES if r != 'field_map']
        ok = (self.err['field_map'] is None and K.record_shapes.shape_ok('field_map', rec)
              and type(rec['renames']) is dict)
        plan = []
        if ok:
            for role, lst in rec['renames'].items():
                if role not in roles or type(lst) is not list:
                    ok = False
                    break
                for ren in lst:
                    if (type(ren) is not dict or set(ren) != {'at', 'from', 'to'}
                            or type(ren['at']) is not str or not is_str(ren['from'])
                            or not is_str(ren['to']) or ren['from'] == ren['to']):
                        ok = False
                        break
                    segs = []
                    if ren['at']:
                        for seg in ren['at'].split('.'):
                            arr = seg.endswith('[]')
                            key = seg[:-2] if arr else seg
                            if not key or '[' in key or ']' in key:
                                ok = False
                                break
                            segs.append((key, arr))
                    if not ok:
                        break
                    plan.append((role, segs, ren['from'], ren['to']))
                if not ok:
                    break
        if not ok:
            self.field_map_status = 'FIELD_MAP_DEFECT_NOT_APPLIED'
            return
        # c2v005 (V006 A190 ruling 3; triage c2v001 RC11, c2v002 RC9, c2v003 RL1): classifier A's printed form.  A
        # role's renames are applied in order, each over its containers in document order; at the first container
        # that already holds the target key the rename is refused there, and nothing further of that role is renamed
        # (neither the later containers of that rename nor the role's later renames).  Other roles are unaffected.
        refused = False
        stopped = set()
        for role, segs, old, new in plan:
            if self.inp.get(role) is None or role in stopped:
                continue
            containers = [self.inp[role]]
            for key, arr in segs:
                nxt = []
                for c in containers:
                    if type(c) is dict and key in c:
                        v = c[key]
                        if arr:
                            if type(v) is list:
                                nxt.extend(v)
                        else:
                            nxt.append(v)
                containers = nxt
            for c in containers:
                if type(c) is dict and old in c:
                    if new in c:
                        refused = True
                        stopped.add(role)
                        break
                    c[new] = c.pop(old)
        self.field_map_status = 'FIELD_MAP_DEFECT_PARTIAL' if refused else 'APPLIED'

    # ------------------------------------------------------------- phase (C-1.1 PHASE_MISMATCH)
    def phase_inputs_check(self):
        """-> ('OK'|'MALFORMED'|'PHASE1_HEADER_MISSING'|'RUN_STATUS_NOT_OF_PHASE', record)"""
        rec = self.inp['phase_inputs']
        if self.err['phase_inputs'] is not None or not K.record_shapes.shape_ok('phase_inputs', rec):
            return 'MALFORMED'
        if rec['phase_named'] not in ('PHASE_1', 'PHASE_2'):
            return 'MALFORMED'
        for k in ('phase1_registry_root', 'phase2_registry_root'):
            if not is_str(rec[k]) or not rec[k].startswith('/'):
                return 'MALFORMED'
        if rec['run_status'] not in RUN_STATUS_PHASES:
            return 'MALFORMED'
        if rec['run_status_code'] is not None and not is_str(rec['run_status_code']):
            return 'MALFORMED'
        h = rec['phase1_header']
        if h is not None:
            if (type(h) is not dict or set(h) != {'b_p1', 'u_a_log_index', 'phase1_record_sha256', 'l1_sha256'}
                    or not is_int(h['b_p1']) or not is_int(h['u_a_log_index'])
                    or not is_hex64(h['phase1_record_sha256']) or not is_hex64(h['l1_sha256'])):
                return 'MALFORMED'
        if rec['phase1_classification_absent_reason'] not in (None, 'AT0A_FAILURE', 'NO_PHASE_1_SCORE'):
            return 'MALFORMED'
        if rec['phase_named'] not in RUN_STATUS_PHASES[rec['run_status']]:
            return 'RUN_STATUS_NOT_OF_PHASE'
        if rec['phase_named'] == 'PHASE_1' and rec['run_status'] == 'SCORED' and h is None:
            return 'PHASE1_HEADER_MISSING'
        return 'OK'

    def check_phase(self):
        self.phase = None
        self.manifest_phase = None
        verdict = self.pi_verdict
        rec = self.inp['phase_inputs']
        if verdict == 'MALFORMED':
            self.stop('PHASE_MISMATCH', 'ALL',
                      'phase inputs record missing or malformed (%s)' % self.err['phase_inputs'])
            return
        self.phase = rec['phase_named']
        if verdict == 'PHASE1_HEADER_MISSING':
            self.stop('PHASE_MISMATCH', 'ALL',
                      'phase inputs record: PHASE1_HEADER_MISSING (a scored Phase 1 needs phase1_header, '
                      'which carries the L1 sha logged at the Phase-1 freeze; C-1.1 L1 map row; V-F4)')
            return
        if verdict == 'RUN_STATUS_NOT_OF_PHASE':
            self.stop('PHASE_MISMATCH', 'ALL',
                      'phase inputs record: RUN_STATUS_NOT_OF_PHASE (%s is not a run status of %s; C-I7; V-F5)'
                      % (rec['run_status'], rec['phase_named']))
            return
        m = self.inp['freeze_manifest']
        path = None
        try:
            path = m['input_bindings']['calibration_record']['path']
        except (TypeError, KeyError):
            path = None
        if not is_str(path) or not path.startswith('/'):
            self.stop('PHASE_MISMATCH', 'ALL',
                      'manifest input_bindings.calibration_record.path missing or not absolute')
            return
        p1 = PurePosixPath(os.path.realpath(rec['phase1_registry_root']))
        p2 = PurePosixPath(os.path.realpath(rec['phase2_registry_root']))
        call = os.path.realpath(path)
        if p1 == p2 or p1 in p2.parents or p2 in p1.parents:
            self.stop('PHASE_MISMATCH', 'ALL', 'Phase-1 and Phase-2 registry roots are not disjoint')
            return
        try:
            derived = K.phase_paths.derive_phase(call, str(p1), str(p2), 'PHASE_1')
        except K.phase_paths.PhaseDefect:
            derived = 'PHASE_2'
        self.manifest_phase = derived
        if derived != self.phase:
            self.stop('PHASE_MISMATCH', 'ALL', 'score entry names %s; manifest calibration record gives %s'
                      % (self.phase, derived))

    # ------------------------------------------------------------- seal (C-1.1 SEAL_SHA_MISMATCH)
    def check_seal(self):
        s = self.bundle['sealed']
        for key in ('text', 'classifier'):
            got = self.sha_of_file(s[key])
            if got is None:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', '%s unreadable' % key)
            elif got != s[key]['sha256']:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', '%s bytes do not hash to the sealed sha' % key)
        pin = self.bundle['inputs']['tsr_flag_record']
        got = self.sha_of_file(pin) if pin is not None else None
        if got != s['tsr_flag_record_sha256']:
            self.stop('SEAL_SHA_MISMATCH', 'ALL', 'tsr_flag_record bytes do not hash to the sealed sha')
        if s['stage0_successor'] is not None:
            got = self.sha_of_file(s['stage0_successor'])
            if got is None:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', 'stage0_successor unreadable')
            elif got != s['stage0_successor']['sha256']:
                self.stop('SEAL_SHA_MISMATCH', 'ALL', 'stage0_successor bytes do not hash to the sealed sha')

    def successor_mode(self):
        return self.phase == 'PHASE_2' and self.bundle['sealed']['stage0_successor'] is not None

    def check_manifest(self):
        m = self.inp['freeze_manifest']
        if type(m) is not dict:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL',
                      'freeze manifest missing or malformed (%s)' % self.err['freeze_manifest'])
            return
        if self.phase is None:
            return
        if self.successor_mode():
            want, ph = MANIFEST_SUCC, 'PHASE_2 with the STAGE0 successor pinned'
        else:
            want, ph = MANIFEST_V003G, self.phase
        if m.get('schema') != want:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL',
                      'freeze manifest schema %r is not %s, the schema of the freeze module the seal '
                      'names for %s (M-5 addition 2; A154)' % (m.get('schema'), want, ph))

    # ------------------------------------------------------------- zone table (C-1.3)
    def check_zone_table(self):
        self.rad_text = {}
        self.radius = {}
        slots = self.inp['slots']
        msg = None
        try:
            if slots is None:
                raise TypeError(str(self.err['slots']))
            rows = slots['query_block']['rows']
            if type(rows) is not list or len(rows) != 43:
                msg = 'query block is not 43 rows'
            else:
                for i, r in enumerate(rows):
                    if (r['query_id'] != QIDS[i] or r['Rad_unit'] != 'kpc'
                            or type(r['Rad_text']) is not str):
                        msg = 'row %d id/unit/text' % i
                        break
                    rad = float(r['Rad_text'])
                    if not math.isfinite(rad):
                        msg = 'row %d radius' % i
                        break
                    z = 'INNER' if rad < 10.0 else ('TRANSITION' if rad < 30.0 else 'OUTER')
                    if z != ZONE_OF[QIDS[i]]:
                        msg = '%s computes to %s, table says %s' % (QIDS[i], z, ZONE_OF[QIDS[i]])
                        break
                    self.rad_text[QIDS[i]] = r['Rad_text']
                    self.radius[QIDS[i]] = rad
        except (TypeError, KeyError, ValueError) as e:
            msg = str(e)
        if msg is not None:
            self.stop('ZONE_TABLE_MISMATCH', 'ALL', 'slots query block: %s' % msg)
            self.zone_ok = False
        else:
            self.zone_ok = True

    # ------------------------------------------------------------- gate list (C-4, M-15)
    def check_gate_list(self):
        self.gates = None
        rec = self.inp['gate_status_list']
        self.gate_echo = None
        try:
            if self.err['gate_status_list'] is not None:
                raise K.root_contracts.ContractDefect('load')
            self.gates = K.root_contracts.gate_index(rec)
            self.gate_echo = rec['gates']
        except K.root_contracts.ContractDefect:
            self.gates = None
            self.stop('GATE_STATUS_LIST_DEFECT', 'GATE',
                      'gate-status list missing or malformed (%s)' % self.err['gate_status_list'])
        self.roster_gates = {}
        names = list(self.bundle['rosters'])
        for name in names:
            err, val, _ = self.read_pinned(self.bundle['rosters'][name])
            ok = (err is None and type(val) is dict and val.get('schema') == ROSTER_SCHEMA
                  and type(val.get('root_gates')) is list
                  and all(type(g) is dict and is_str(g.get('path')) and is_hex64_ci(g.get('sha256'))
                          for g in val['root_gates']))
            if not ok:
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'roster %s missing or malformed (%s)' % (name, err))
                continue
            self.roster_gates[name] = [g['sha256'].lower() for g in val['root_gates']]
        if not any(n in self.bundle['rosters'] for n in PRIMARY_ROSTER_NAMES):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL', 'no PRIMARY roster supplied')
        if self.gates is not None:
            for name in names:
                for g in self.roster_gates.get(name, []):
                    if g not in self.gates:
                        self.stop('GATE_STATUS_LIST_DEFECT', 'GATE',
                                  'root-listed gate %s of roster %s not on the list' % (g[:12], name))

    def gate_status_of(self, sha):
        if self.gates is None or sha is None:
            return None
        return self.gates.get(sha.lower())

    # ------------------------------------------------------------- TSR (C-1.4)
    def check_tsr(self):
        details = []
        cpin = self.bundle['inputs']['ntest_compare']
        cmp_val = self.inp['ntest_compare']
        # c2v003 RC2: each PREREG L194 compare condition is its own detail (OUTPUT_CONSTANTS_C4V003 L234-L238):
        # (a) the pin is not the full 6f095f64 sha (INPUT_CONTRACTS_C4V004 L42); (b) the supplied compare does not
        # load; (c) it is not in the registered bytes' encoding (c2v005: the seal candidate's form); (d) its failing
        # TRUNCATION_SHAPE rings are not exactly the one ring of ordinal 15; (e) its failing non-TRUNCATION_SHAPE
        # rings are not empty.  A wrong pin does not suppress (b)-(e); only a compare that did not load skips (c)-(e).
        if cpin is None or cpin['sha256'] != COMPARE_SHA:
            details.append('the N-test compare is not 6f095f64')
        # c2v005 (V006 A190 ruling 2; triage c2v003 RC2b, c2v004 RC2R candidate (i)): the seal candidate's printed
        # form.  A compare that does not load as an object: 'compare unreadable (<load status>)'.  Otherwise (c)
        # prints iff its schema is not the registered compare's or its failing TRUNCATION_SHAPE list is not a list
        # of objects; else (d) prints unless that list holds exactly one record with the integer ordinal 15
        # (classification is not read; 15.0 or a renamed key is no ordinal); and, independently of (c) and (d), (e)
        # prints iff the failing non-TRUNCATION_SHAPE list is not exactly [] (missing or null included).  C4-2 is
        # withdrawn.  ts: the TRUNCATION_SHAPE records when (c) did not print, for the support record's native_ring.
        ts = None
        if self.err['ntest_compare'] is not None or type(cmp_val) is not dict:
            details.append('compare unreadable (%s)' % self.err['ntest_compare'])
        else:
            tsl = cmp_val.get(COMPARE_TS_RINGS)
            if (cmp_val.get('schema') != COMPARE_SCHEMA or type(tsl) is not list
                    or any(type(r) is not dict for r in tsl)):
                details.append('compare schema or failing ring list')
            else:
                ts = tsl
                if not (len(tsl) == 1 and is_int(tsl[0].get('ordinal')) and tsl[0]['ordinal'] == 15):
                    details.append('failing TRUNCATION_SHAPE rings are not exactly {ordinal 15}')
            other = cmp_val.get(COMPARE_OTHER_RINGS)
            if type(other) is not list or other:
                details.append('failing non-TRUNCATION_SHAPE rings are not empty')
        m = self.inp['freeze_manifest']
        pinned = None
        try:
            files = m['pins']['input_files']
            if type(files) is list:
                pinned = {f['sha256'] for f in files if type(f) is dict and is_hex64(f.get('sha256'))}
            elif type(files) in (str, dict):
                # c2v005 (V006 A190 ruling 3; triage c2v002 RC11, c2v003 RL4): classifier A's printed form.  A
                # string or an object is iterated as A iterates it and holds no pin, so every input-files
                # requirement reads 'not pinned'.  Any other non-list value stays unreadable.
                pinned = set()
            else:
                raise TypeError
        except (TypeError, KeyError):
            pinned = None
            details.append('manifest pins.input_files unreadable')
        rec = self.inp['tsr_flag_record']
        ferr = self.err['tsr_flag_record']
        if ferr is not None or not K.record_shapes.shape_ok('tsr_flag_record', rec):
            details.append('flag record missing or malformed (%s)' % ferr)
            # c2v005 (V006 A190 ruling 2; triage c2v002 RC12, c2v003 RL3): the seal candidate's printed form.  A flag
            # record that fails its exact-key contract prints its single 'missing or malformed' detail and no field
            # condition; the record's own input-files requirement (its bytes' sha) still applies.
            rec = None
        # c2v002 RC02: every requirement on the flag record is its own condition (PREREG L194;
        # INPUT_CONTRACTS_C4V004 item 3); a failing one never hides another.  The record's own sha is
        # the sha of bytes that match the bundle pin (load READ or JSON_DEFECT); otherwise it is absent.
        own = self.rawsha['tsr_flag_record'] if (ferr is None or ferr.startswith('JSON_DEFECT:')) else None
        details.extend(self._flag_record_details(rec, pinned, own))
        sup = self.inp['tsr_support_record']
        if (self.err['tsr_support_record'] is not None or type(sup) is not dict
                or set(sup) != SUPPORT_KEYS or sup.get('schema') != SUPPORT_SCHEMA):
            details.append('support record missing or malformed (%s)' % self.err['tsr_support_record'])
        else:
            details.extend(self._support_details(sup, ts))  # ts: the compare's TRUNCATION_SHAPE records
        self.tsr_stop = bool(details)
        for d in details:
            self.stop('TSR_FLAG_TABLE_MISMATCH', 'TSR', d)

    def _flag_record_details(self, rec, pinned, own_sha):
        """c2v002 RC02: -> every failing requirement of the flag record, each its own detail.

        A requirement is skipped only when the thing it tests is absent: a field the record lacks (its absence is
        the 'missing or malformed' detail); the 'not pinned among the freeze input files' requirement of a pin
        that does not carry its fixed sha; 'exactly {NGC3198-Q25}' unless the flags are 43 booleans in manifest
        order; every input-files requirement when pins.input_files is unreadable (pinned None).
        """
        out = []
        if pinned is not None and own_sha is not None and own_sha not in pinned:
            out.append('flag record not pinned among the freeze input files')
        if type(rec) is not dict:
            return out
        for key, sha in (('ntest_compare_pin', COMPARE_SHA), ('n1_record_pin', N1_SHA),
                         ('gl_node_record_pin', NODE_SHA)):
            if key not in rec:
                continue
            if not is_pin(rec[key]) or rec[key]['sha256'] != sha:
                out.append('flag record %s is not %s' % (key, FLAG_PIN_TEXT[key]))
            elif pinned is not None and sha not in pinned:
                out.append('%s not pinned among the freeze input files' % key)
        if (('target_free' in rec and rec['target_free'] is not True)
                or ('rule' in rec and not is_str(rec['rule']))
                or ('failing_ring_ordinal' in rec and (not is_int(rec['failing_ring_ordinal'])
                                                       or rec['failing_ring_ordinal'] != 15))):
            out.append('flag record scope, rule or ring')
        if 'flags' in rec:
            fl = rec['flags']
            if (type(fl) is not list or len(fl) != 43
                    or any(type(f) is not dict or set(f) != {'query_id', 'TRUNCATION_SHAPE_RESIDUAL'}
                           or f['query_id'] != QIDS[i] or type(f['TRUNCATION_SHAPE_RESIDUAL']) is not bool
                           for i, f in enumerate(fl))):
                out.append('flag record flags are not 43 booleans in manifest order')
            elif {f['query_id'] for f in fl if f['TRUNCATION_SHAPE_RESIDUAL']} != {Q25}:
                out.append('flag record flags are not exactly {NGC3198-Q25}')
        return out

    def _support_details(self, sup, ts):
        """-> the failing support-record conditions.  c2v002 RC02: on the single ring entry, the native_ring
        condition and the (r_14, r_16) exclusive-bounds condition (PREREG L275-L277) are reported separately.
        c2v003 RC2: the native_ring condition holds only when native_ring equals, verbatim, the compare's single
        failing ordinal-15 TRUNCATION_SHAPE ring record (PREREG L275; ROOT_ITEMS L220), not when it merely occurs
        somewhere in the compare.  c2v005: ts is the compare's failing TRUNCATION_SHAPE records (a list of objects),
        or None when the compare did not load or printed (c)."""
        if (sup['target_free'] is not True or sup['before_target_access'] is not True
                or not is_pin(sup['ntest_compare_pin']) or sup['ntest_compare_pin']['sha256'] != COMPARE_SHA):
            return ['support record scope or compare pin']
        rings = sup['rings']
        if type(rings) is not list or len(rings) != 1 or type(rings[0]) is not dict:
            return ['support record is not one ring entry']
        ring = rings[0]
        out = []
        nr = ring.get('native_ring')
        rec15 = [r for r in ts if is_int(r.get('ordinal')) and r['ordinal'] == 15] if ts is not None else []
        if not (len(rec15) == 1 and type(nr) is dict and canon(nr) == canon(rec15[0])):
            out.append('support record native_ring is not the compare ordinal-15 record verbatim')
        if not (type(ring.get('lower_kpc')) is float and ring['lower_kpc'] == R14_KPC
                and ring.get('lower_inclusive') is False
                and type(ring.get('upper_kpc')) is float and ring['upper_kpc'] == R16_KPC
                and ring.get('upper_inclusive') is False):
            out.append('support record bounds are not (r_14, r_16) exclusive')
        return out

    # ------------------------------------------------------------- score (C-1.1, M-5)
    def check_score(self):
        self.ref = None
        self.ref_rows = None
        s = self.inp['score']
        A = 'ALL'
        if type(s) is not dict:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'score output missing or malformed (%s)' % self.err['score'])
            return
        h = s.get('headline')
        rid = rli = None
        if type(h) is dict and is_str(h.get('reference_member_id')) and is_int(h.get('reference_member_log_index')):
            rid, rli = h['reference_member_id'], h['reference_member_log_index']
        else:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'headline.reference_member_id / reference_member_log_index')
        members = s.get('members')
        mem_ok = type(members) is list and all(
            type(x) is dict and is_str(x.get('member_id')) and is_int(x.get('log_index')) for x in members)
        if not mem_ok:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'members[].member_id / log_index')
        else:
            ids = [x['member_id'] for x in members]
            if len(set(ids)) != len(ids):
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'members[].member_id repeated')
            if rid is not None:
                cands = [x for x in members if x['member_id'] == rid]
                if not cands:
                    self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'reference member not among members[]')
                else:
                    self.ref = cands[0]
                    if self.ref['log_index'] != rli:
                        self.stop('REFERENCE_MEMBER_MISMATCH', A, 'reference member log_index differs from the headline')
        m = self.inp['freeze_manifest']
        if type(m) is not dict:
            # c2v005 (V006 A190 ruling 2; triage c2v002 RC13): the seal candidate's printed form.  A frozen manifest
            # that is not an object also prints the dependent detail beside its load detail.
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'manifest reference_member / members unreadable')
        else:
            mr = m.get('reference_member')
            mm = m.get('members')
            if (type(mr) is not dict or not is_str(mr.get('member_id')) or not is_int(mr.get('log_index'))
                    or type(mm) is not list or any(type(x) is not dict for x in mm)):
                self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'manifest reference_member / members unreadable')
            else:
                if sum(1 for x in mm if x.get('member_id') == mr['member_id']) != 1:
                    self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'manifest reference member not unique among manifest members')
                if rid is not None and (rid, rli) != (mr['member_id'], mr['log_index']):
                    self.stop('REFERENCE_MEMBER_MISMATCH', A, 'score names %s/%s; frozen manifest names %s/%s'
                              % (rid, rli, mr['member_id'], mr['log_index']))
        if self.ref is not None and type(self.ref.get('member_valid')) is not bool:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'reference member member_valid')
        ir = s.get('incomplete_reasons')
        if (s.get('freeze_status') not in ('FREEZE_COMPLETE', 'FREEZE_INCOMPLETE')
                or type(ir) is not list or any(type(x) is not str for x in ir)):
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', A, 'freeze_status / incomplete_reasons')
        if self.ref is not None:
            rows = self.ref.get('rows')
            if (type(rows) is not list or len(rows) != 43
                    or any(type(r) is not dict or r.get('id') != QIDS[i] for i, r in enumerate(rows))):
                self.stop('QUERY_ID_DEFECT', A, 'reference member ids are not NGC3198-Q01..Q43 in order without repeat')
            else:
                self.ref_rows = rows
                if any(r.get('status') == 'UNEVALUATED_OR_REFUSED' for r in rows):
                    self.stop('REFERENCE_ROW_UNEVALUATED_OR_REFUSED', A,
                              'a reference-member row has status UNEVALUATED_OR_REFUSED')

    def check_envelope(self):
        self.env = {}
        self.env_bad = set()
        s = self.inp['score']
        if type(s) is not dict:
            return
        env = s.get('pointwise_envelope')
        label = env.get('label') if type(env) is dict else None
        if type(label) is not str or not label.startswith(ENVELOPE_PREFIX):
            self.stop('ENVELOPE_LABEL_MISMATCH', 'ALL', 'pointwise_envelope.label prefix differs or is missing')
        rows = env.get('rows') if type(env) is dict else None
        if type(rows) is not list or len(rows) != 43:
            self.stop('FIELD_DEFECT_ENVELOPE', 'ENVELOPE', 'pointwise_envelope.rows is not 43 rows', rows=QIDS)
            self.env_bad = set(QIDS)
            return
        for i, r in enumerate(rows):
            q = QIDS[i]
            if (type(r) is not dict or r.get('id') != q or type(r.get('valid')) is not bool
                    or not _overlap_ok(r)):
                self.stop('FIELD_DEFECT_ENVELOPE', 'ENVELOPE', '%s envelope row field' % q, rows=[q])
                self.env_bad.add(q)
            else:
                self.env[q] = r

    def check_sensitivity(self):
        self.sens = {}
        self.sens_bad = set()
        if self.phase != 'PHASE_2':
            return
        s = self.inp['score']
        if type(s) is not dict:
            return
        sens = s.get('sensitivity')
        rows = sens.get('rows') if type(sens) is dict else None
        if type(rows) is not list or len(rows) != 43:
            self.stop('FIELD_DEFECT_SENSITIVITY', 'SENSITIVITY', 'sensitivity.rows is not 43 rows', rows=QIDS)
            self.sens_bad = set(QIDS)
            return
        for i, r in enumerate(rows):
            q = QIDS[i]
            if (type(r) is not dict or r.get('id') != q or type(r.get('valid')) is not bool
                    or not _overlap_ok(r)):
                self.stop('FIELD_DEFECT_SENSITIVITY', 'SENSITIVITY', '%s sensitivity row field' % q, rows=[q])
                self.sens_bad.add(q)
            else:
                self.sens[q] = r

    # ------------------------------------------------------------- registrations
    def manifest_member(self, member_id):
        m = self.inp['freeze_manifest']
        if type(m) is not dict or type(m.get('members')) is not list:
            return None
        c = [x for x in m['members'] if type(x) is dict and x.get('member_id') == member_id]
        return c[0] if len(c) == 1 else None

    def ref_registration(self):
        if getattr(self, '_ref_reg', None) is not None:
            return self._ref_reg
        mm = None
        m = self.inp['freeze_manifest']
        if type(m) is dict and type(m.get('reference_member')) is dict:
            mm = self.manifest_member(m['reference_member'].get('member_id'))
        ent = _reg_entries(mm.get('row_registration'), m.get('query_ids'), QIDS) if mm is not None else None
        self._ref_reg = ent if ent is not None else {}
        self._ref_reg_ok = ent is not None
        return self._ref_reg

    def reg_of(self, qid):
        reg = self.ref_registration()
        if not self._ref_reg_ok:
            return REG_UNREADABLE
        return reg_info(reg.get(qid))

    def twin_registration(self, alt, log_index, ids):
        """c2v005 RC5: the twin's frozen row_registration under alternative_results[alt].members[] (README c4v001
        L70), a list aligned with the manifest's query_ids (v003g L4086-L4087 narrows it to a STAGE0 scope by those
        indexes), read for the twin's scope ids."""
        m = self.inp['freeze_manifest']
        try:
            ar = m['alternative_results'][alt]
            mem = [x for x in ar['members'] if type(x) is dict and x.get('log_index') == log_index]
            if len(mem) != 1:
                return None
            return _reg_entries(mem[0].get('row_registration'), m.get('query_ids'), ids)
        except (TypeError, KeyError, AttributeError):
            return None

    # ------------------------------------------------------------- rows (rule M-T, C-1.2, C-4)
    def row_messages(self, r):
        # c2v005 (V006 A190 ruling 2): the seal candidate's printed form.  Triage c2v001 RC07, c2v002 RC8, c2v003
        # RC6: presence and type are checked separately on each of the five M-5 row fields, an absent field read as
        # null for the type check; every 'missing' message first, then the type messages, each in the order
        # score_status, within_error, sigma_ratio, registered_reason, status (an absent score_status, within_error or
        # status prints both; null is an allowed sigma_ratio and registered_reason).  Triage c2v001 RC08, c2v003 RL2
        # (OC-14): a row status outside VALID, INVALID, UNEVALUATED_OR_REFUSED is 'status wrong type'.
        msgs = []
        for k in ROW_FIELDS:
            if k not in r:
                msgs.append('%s missing' % k)
        if r.get('score_status') not in SCORE_STATUSES:
            msgs.append('score_status wrong type')
        if type(r.get('within_error')) is not bool:
            msgs.append('within_error wrong type')
        if r.get('sigma_ratio') is not None and not is_num(r['sigma_ratio']):
            msgs.append('sigma_ratio wrong type or non-finite')
        if r.get('registered_reason') is not None and not is_str(r['registered_reason']):
            msgs.append('registered_reason wrong type')
        if r.get('status') not in ROW_STATUSES:
            msgs.append('status wrong type')
        if msgs:
            return msgs
        if r['score_status'] == 'INVALID_AS_MISS' and r['registered_reason'] is None:
            msgs.append('registered_reason missing on an INVALID_AS_MISS row')
        if r['score_status'] != 'INVALID_AS_MISS' and r['within_error'] is True and r['sigma_ratio'] is None:
            msgs.append('sigma_ratio null on a within-error row (finite value required)')
        return msgs

    def classify_row(self, q, r, reg_lookup, gate_msgs):
        """-> (Row, messages). gate_msgs collects (qid, gate sha) of missing gates."""
        row = Row(q)
        msgs = self.row_messages(r)
        unread = False
        if not msgs and r['score_status'] == 'INVALID_AS_MISS':
            reason = r['registered_reason']
            if reason in BUILTIN_REASONS:
                row.kind, row.reason, row.gate_status = 'I', reason, None
            else:
                info = reg_lookup(q)
                # c2v005 RC5: the gate is the frozen entry's pin, provided the entry is in the producer's form and
                # its reason equals this row's registered_reason (v003g L4042: the score row carries the frozen
                # reason).  Otherwise the reason is unknown (RC14, PREREG L205): a row of D under any reason.
                if (info is REG_UNREADABLE or info[0] != 'INVALID' or info[2] is None
                        or info[1] != reason):
                    unread = True
                    msgs.append('gate registration of an INVALID_AS_MISS row not readable from the frozen manifest')
                else:
                    st = self.gate_status_of(info[2])
                    if st is None:
                        gate_msgs.append((q, info[2]))
                        row.fixed = False
                        row.kinds = {'I', 'L'}
                        row.kind_reason = {'I': reason, 'L': reason}
                        row.dclass = 'GATE'
                    elif st == 'ON-TIME':
                        row.kind, row.reason, row.gate_status = 'I', reason, 'ON-TIME'
                    else:
                        row.kind, row.reason, row.gate_status = 'L', reason, 'LATE'
        elif not msgs:
            if r['within_error'] is True:
                row.kind, row.ratio = 'H', r['sigma_ratio']
            elif r['sigma_ratio'] is None:
                row.kind = 'MN'
            else:
                row.kind, row.ratio = 'MS', r['sigma_ratio']
        if msgs:
            row.fixed = False
            row.dclass = 'ROW'
            ks = {'H', 'MS', 'MN'}
            row.kind_reason = {}
            info = reg_lookup(q)
            if info is REG_UNREADABLE or unread:
                ks |= {'I', 'L'}
                row.kind_reason = {'I': None, 'L': None}
            elif info[0] == 'INVALID':
                if info[2] is None and info[1] in BUILTIN_REASONS:
                    ks.add('I')
                    row.kind_reason['I'] = info[1]
                else:
                    st = self.gate_status_of(info[2])
                    if st == 'ON-TIME':
                        ks.add('I')
                    elif st == 'LATE':
                        ks.add('L')
                    else:
                        ks |= {'I', 'L'}
                    for k in ('I', 'L'):
                        if k in ks:
                            row.kind_reason[k] = info[1]
            row.kinds = ks
        return row, msgs

    def build_rows(self):
        self.rows = None
        if self.ref_rows is None or not self.zone_ok:
            return
        rows = []
        gate_msgs = []
        for i, r in enumerate(self.ref_rows):
            q = QIDS[i]
            if r.get('status') == 'UNEVALUATED_OR_REFUSED':
                row = Row(q)
                row.fixed = False
                row.kinds = {'H', 'MS', 'MN'}
                row.dclass = 'ALL'
                rows.append(row)
                continue
            row, msgs = self.classify_row(q, r, self.reg_of, gate_msgs)
            if msgs:
                self.stop('FIELD_DEFECT_ROW', 'ROW', '%s: %s' % (q, '; '.join(msgs)), rows=[q])
            rows.append(row)
        for q, g in gate_msgs:
            self.stop('GATE_STATUS_LIST_DEFECT', 'GATE',
                      '%s: gate %s of this INVALID row is not on the gate-status list' % (q, g[:12]), rows=[q])
        for row in rows:
            row.rad_text = self.rad_text.get(row.qid)
            row.radius = self.radius.get(row.qid)
            if row.fixed and row.kind in ('MS', 'MN'):
                if row.qid in self.env_bad:
                    row.near = ('NA', ['FIELD_DEFECT_ENVELOPE'])
                elif row.qid in self.env:
                    e = self.env[row.qid]
                    row.near = e['band_overlaps_error_bar'] if e['valid'] else ('NA', ['ENVELOPE_ROW_INVALID'])
                else:
                    row.near = ('NA', ['FIELD_DEFECT_ENVELOPE'])
            elif row.fixed:
                row.near = False
        self.rows = rows
        self.row_by_id = {r.qid: r for r in rows}

    # ------------------------------------------------------------- alternatives (C-6)
    def score_alternatives(self):
        s = self.inp['score']
        alts = s.get('alternatives') if type(s) is dict else None
        return alts if type(alts) is list else None

    def alt_entry(self, name):
        alts = self.score_alternatives()
        if alts is None:
            return None
        c = [a for a in alts if type(a) is dict and a.get('name') == name]
        return c[0] if len(c) == 1 else None

    def check_alternatives(self):
        alts = self.score_alternatives()
        names = list(ALT_ORDER[1:]) if self.phase == 'PHASE_1' else list(ALT_ORDER)
        if self.phase != 'PHASE_1':
            names.append(STAGE0)
        if type(self.inp['score']) is not dict:
            return
        if alts is None:
            for n in names:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: alternatives list missing' % n, alternative=n)
            return
        if any(type(a) is dict and a.get('name') == DIST_ALT for a in alts):
            names.append(DIST_ALT)
        for n in names:
            c = [a for a in alts if type(a) is dict and a.get('name') == n]
            if not c:
                if n != DIST_ALT:
                    self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: declared alternative missing' % n, alternative=n)
                continue
            if len(c) > 1:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: repeated' % n, alternative=n)
                continue
            a = c[0]
            # c2v005 RC3: the entry form score_after_freeze writes (v003g 48a1e48a L4273-L4299; d260ee30
            # L4829-L4855).  Every alternative read here is non-PRIMARY, so its role is the string NON_PRIMARY;
            # scoring_scope is written only on STAGE0_GRID_OUTER, as an object whose query_ids are the OUTER set
            # (PREREG L243, L523), and its absence elsewhere is no defect; members is written only on a scored
            # entry, so it is required (a list) only when scored is true.  The failing fields are joined by a bare
            # comma (ruling 2, triage c2v003 RC3c; OUTPUT_CONSTANTS_C4V003 L340).
            bad = []
            if not is_str(a.get('kind')):
                bad.append('kind')
            if a.get('status') not in (EBF, NEBF):
                bad.append('status')
            if a.get('role') != ROLE_NON_PRIMARY:
                bad.append('role')
            if type(a.get('scored')) is not bool:
                bad.append('scored')
            if n == STAGE0:
                sc = a.get('scoring_scope')
                if type(sc) is not dict or sc.get('query_ids') != OUTER_IDS:
                    bad.append('scoring_scope')
            if a.get('scored') is True and type(a.get('members')) is not list:
                bad.append('members')
            if bad:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: %s' % (n, ','.join(bad)), alternative=n)

    def twin_rows(self, name, a, scope_ids):
        """-> ('INVALID', None) | ('IDS', None) | ('DEFECT', None) | ('OK', rows)"""
        ref_li = self.ref['log_index']
        members = a.get('members')
        if type(members) is not list or any(type(x) is not dict or not is_int(x.get('log_index')) for x in members):
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: members field' % name, alternative=name)
            return 'DEFECT', None
        c = [x for x in members if x['log_index'] == ref_li]
        if len(c) != 1:
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: no unique twin with the reference log_index' % name,
                      alternative=name)
            return 'DEFECT', None
        tw = c[0]
        if type(tw.get('member_valid')) is not bool:
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: twin member_valid' % name, alternative=name)
            return 'DEFECT', None
        if tw['member_valid'] is False:
            return 'INVALID', None
        rws = tw.get('rows')
        if type(rws) is not list or any(type(r) is not dict for r in rws):
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: members field' % name, alternative=name)
            return 'DEFECT', None
        if [r.get('id') for r in rws] != list(scope_ids):
            return 'IDS', None
        reg = self.twin_registration(name, ref_li, scope_ids)

        def lookup(q):
            if reg is None:
                return REG_UNREADABLE
            return reg_info(reg.get(q))
        out = []
        parts = []
        gate_msgs = []
        for q, r in zip(scope_ids, rws):
            row, msgs = self.classify_row(q, r, lookup, gate_msgs)
            if msgs:
                parts.append('%s: %s' % (q, '; '.join(msgs)))
            out.append(row)
        for q, g in gate_msgs:
            parts.append('%s: gate %s of this INVALID row is not on the gate-status list' % (q, g[:12]))
        if parts:
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT', '%s: %s' % (name, '; '.join(parts)), alternative=name)
            return 'DEFECT', None
        for row in out:
            row.radius = self.radius.get(row.qid)
            row.rad_text = self.rad_text.get(row.qid)
        return 'OK', out

    def prepare_alternatives(self):
        """Builds self.alt_out (list entries) and the twin classifications."""
        self.twin_class = {}
        self.alt_state = {}
        if self.phase not in ('PHASE_1', 'PHASE_2') or self.ref is None:
            return
        for name in ALT_ORDER:
            if name == 'ORIGINAL_K' and self.phase == 'PHASE_1':
                continue  # C-I4: ORIGINAL_K reads NOT_AVAILABLE in Phase 1
            a = self.alt_entry(name)
            if a is None or self.alt_stopped(name):
                continue
            if name == 'ORIGINAL_K':
                if a.get('status') != EBF or a.get('scored') is not True:
                    continue
            elif a.get('status') != EBF or a.get('scored') is not True:
                continue
            st, rows = self.twin_rows(name, a, QIDS)
            self.alt_state[name] = st
            if st == 'OK':
                self.twin_class[name] = rows

    # ------------------------------------------------------------- STAGE0 (C-6.3, M-14, A154, A168, A173)
    def stage0_status(self):
        """-> (status dict for header/stage0, facts or None).  Phase 1 fixed form."""
        if self.phase == 'PHASE_1':
            return {'status': NEBF, 'reasons': ['NOT_IN_PHASE_1']}, None
        if self.successor_mode():
            try:
                facts = self._stage0_block_facts()
            except S0Defect as e:
                self.s0_defect = ('BLOCK', str(e))
                return {'status': NA, 'reasons': ['STAGE0_STATUS_BLOCK_DEFECT'], 'source': SRC_BLOCK,
                        'defect': str(e)}, None
        else:
            rec = self.inp['stage0_status']
            try:
                if self.err['stage0_status'] is not None or not K.record_shapes.shape_ok('stage0_status', rec):
                    raise S0Defect('RECORD_KEYS')
                facts = self._stage0_facts(rec, 'record', False, None)
            except S0Defect as e:
                self.s0_defect = ('RECORD', str(e))
                return {'status': NA, 'reasons': ['STAGE0_STATUS_RECORD_DEFECT']}, None
        st = {'phase2_step4_start_utc': facts['start'], 'receipt_times_utc': facts['times'],
              'source': facts['source'], 'post_score_exploratory': facts['post'],
              'status': facts['reading'], 'reasons': facts['reasons']}
        return st, facts

    def successor_key_sets(self):
        """c2v003 RC4: (STAGE0_BLOCK_KEYS, STAGE0_MEMBER_KEYS) of the successor module, as frozensets, read from the
        sealed successor's own bytes (README c4v003 L41, L157: the full key sets come from the module bytes) as
        top-level literals, never executed.  Reached only once the pin binds.  -> None when the bytes are unreadable
        or not the pinned bytes, when a constant is not a literal _module_str_set reads, or when a set lacks a key
        classifier B reads (the block is then BLOCK_KEYS, fail closed)."""
        if hasattr(self, '_s0_keys'):
            return self._s0_keys
        self._s0_keys = None
        pin = self.bundle['sealed']['stage0_successor']
        try:
            with open(self.resolve(pin['path']), 'rb') as f:
                raw = f.read()
        except OSError:
            return None
        if hashlib.sha256(raw).hexdigest() != pin['sha256']:
            return None
        bk = _module_str_set(raw, 'STAGE0_BLOCK_KEYS')
        mk = _module_str_set(raw, 'STAGE0_MEMBER_KEYS')
        if (bk is None or mk is None or not set(STAGE0_BLOCK_REQUIRED) <= bk
                or not set(STAGE0_BLOCK_MEMBER_REQUIRED) <= mk):
            return None
        self._s0_keys = (bk, mk)
        return self._s0_keys

    def _stage0_block_facts(self):
        sealed = self.bundle['sealed']['stage0_successor']
        # c2v003 RC3: bound only at exactly the full successor sha (README c4v003 L42, L73), never by a prefix.
        if STAGE0_SUCCESSOR_SHA256 is None or sealed['sha256'] != STAGE0_SUCCESSOR_SHA256:
            raise S0Defect('STAGE0_SUCCESSOR_PIN_NOT_BOUND')
        m = self.inp['freeze_manifest']
        if type(m) is not dict or m.get('schema') != MANIFEST_SUCC:
            raise S0Defect('MANIFEST_SCHEMA_NOT_SUCCESSOR')
        blk = m.get('stage0_status')
        # c2v003 RC4: exactly the module's block keys, no key missing and none extra, and every member row exactly
        # the module's member-row keys (README c4v003 L41, L44, L157); checked before the exception-path test
        # (README c4v004 L44-L50; OC-56), so an exception-path block with a wrong key set is BLOCK_KEYS.
        keys = self.successor_key_sets()
        if keys is None or type(blk) is not dict or set(blk) != keys[0]:
            raise S0Defect('BLOCK_KEYS')
        if type(blk['members']) is list and any(type(x) is not dict or set(x) != keys[1] for x in blk['members']):
            raise S0Defect('BLOCK_KEYS')
        if blk['alternative'] != STAGE0 or blk['module'] != STAGE0_MODULE:
            raise S0Defect('BLOCK_MODULE')
        if blk['successor_module_sha256'] != sealed['sha256']:
            raise S0Defect('BLOCK_SUCCESSOR_SHA')
        if blk['status_record'] is not None and not is_pin(blk['status_record']):
            raise S0Defect('BLOCK_STATUS_RECORD')
        try:
            claim = K.stage0_exception_claim.exception_claim(
                blk['diagnostics'], blk['rule_a_receipts_finished'], blk['rule_b_successor_sealed'])
        except ValueError:
            raise S0Defect('BLOCK_DIAGNOSTICS')
        if claim == 'BLOCK_EXCEPTION_PATH':
            raise S0Defect('BLOCK_EXCEPTION_PATH')
        facts = self._stage0_facts(blk, 'block', claim == 'EXCEPTION', blk['successor_module_sha256'])
        for mrow in blk['members']:
            if (not is_str(mrow['member_id'])
                    or (mrow['receipt'] is not None and not is_pin(mrow['receipt']))
                    or type(mrow['custody_ok']) is not bool or type(mrow['defects']) is not list
                    or (mrow['finished'] is True and mrow['custody_ok'] is not True)):
                raise S0Defect('BLOCK_MEMBER')
        mm = m.get('members')
        prim = ([(x.get('member_id'), x.get('log_index')) for x in mm] if type(mm) is list
                and all(type(x) is dict for x in mm) else None)
        if prim is None or [(x['member_id'], x['log_index']) for x in blk['members']] != prim:
            raise S0Defect('BLOCK_MEMBERS_NOT_THE_PRIMARY_MEMBERS')
        if self.bundle['inputs']['stage0_status'] is not None:
            rec = self.inp['stage0_status']
            proj = {'schema': SRC_RECORD}
            for k in STAGE0_RECORD_KEYS[1:]:
                proj[k] = blk[k]
            proj['members'] = [{k: x[k] for k in STAGE0_MEMBER_PROJ} for x in blk['members']]
            if self.err['stage0_status'] is not None or type(rec) is not dict or canon(rec) != canon(proj):
                raise S0Defect('STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION')
        return facts

    def _stage0_facts(self, d, source, exception_path, self_sha):
        if d['phase'] not in (None, 'PHASE_2'):
            raise S0Defect('PHASE')
        start = d['step4_start_utc']
        if start is not None and parse_utc(start) is None:
            raise S0Defect('STEP4_START_UTC')
        ss = d['sealed_successor']
        if ss is not None and not (type(ss) is dict and set(ss) == {'module_sha256', 'source'}
                                   and is_hex64(ss['module_sha256']) and is_str(ss['source'])):
            raise S0Defect('SEALED_SUCCESSOR')
        mem = d['members']
        if type(mem) is not list:
            raise S0Defect('MEMBERS')
        for x in mem:
            if type(x) is not dict or not all(k in x for k in STAGE0_MEMBER_PROJ):
                raise S0Defect('MEMBER_ROW')
            if source == 'record' and set(x) != set(STAGE0_MEMBER_PROJ):
                raise S0Defect('MEMBER_ROW')
            if (not is_int(x['log_index']) or (x['terminal_status'] is not None and not is_str(x['terminal_status']))
                    or type(x['finished']) is not bool
                    or (x['before_step4'] is not None and type(x['before_step4']) is not bool)):
                raise S0Defect('MEMBER_ROW')
            if x['written_utc'] is not None and parse_utc(x['written_utc']) is None:
                raise S0Defect('MEMBER_WRITTEN_UTC')
            # c2v005 (V006 A190 ruling 2; triage c2v001 RC06, c2v002 RC5, c2v003 RL6): the seal candidate's printed
            # form.  MEMBER_FINISHED: a finished row that lacks terminal status FINISHED, a receipt time or a step-4
            # start, or whose before_step4 is not (receipt time <= step-4 start), a null before_step4 being allowed
            # only on the exception path.  MEMBER_BEFORE_STEP4: an unfinished row whose before_step4 is not null.
            if x['finished']:
                if not (x['terminal_status'] == 'FINISHED' and x['written_utc'] is not None) or start is None:
                    raise S0Defect('MEMBER_FINISHED')
                if x['before_step4'] is None:
                    if not exception_path:
                        raise S0Defect('MEMBER_FINISHED')
                elif x['before_step4'] != (parse_utc(x['written_utc']) <= parse_utc(start)):
                    raise S0Defect('MEMBER_FINISHED')
            elif x['before_step4'] is not None:
                raise S0Defect('MEMBER_BEFORE_STEP4')
        for k in ('rule_a_receipts_finished', 'rule_b_successor_sealed', 'receipts_before_step4',
                  'post_score_exploratory'):
            if type(d[k]) is not bool:
                raise S0Defect('RULE_FLAGS')
        if type(d['receipt_refusals']) is not list or type(d['evaluation_refusals']) is not list:
            raise S0Defect('LISTS')
        if exception_path:
            ra, rb = False, False
            if d['receipts_before_step4'] is not True:
                raise S0Defect('RECEIPTS_BEFORE_STEP4')
            rbs4 = True
        else:
            fin = all(x['finished'] for x in mem)
            ra = (bool(mem) and fin) if source == 'block' else fin
            rb = (ss is not None and ss['module_sha256'] == self_sha) if source == 'block' else False
            rbs4 = not any(x['finished'] and x['before_step4'] is False for x in mem)
        if d['rule_a_receipts_finished'] != ra:
            raise S0Defect('RULE_A')
        if d['rule_b_successor_sealed'] != rb:
            raise S0Defect('RULE_B')
        if d['receipts_before_step4'] != rbs4:
            raise S0Defect('RECEIPTS_BEFORE_STEP4')
        reasons = ([S0_RNF] if not ra else []) + ([S0_NSS] if not rb else []) + ([S0_RA4] if not rbs4 else [])
        if d['reasons'] != reasons:
            raise S0Defect('REASONS')
        if reasons and d['evaluation_refusals']:
            raise S0Defect('EVALUATION_REFUSALS')
        reading = NEBF if reasons else (EREF if (d['receipt_refusals'] or d['evaluation_refusals']) else EBF)
        if d['reading'] != reading:
            raise S0Defect('READING')
        if d['post_score_exploratory'] != (S0_RA4 in reasons):
            raise S0Defect('POST_SCORE_EXPLORATORY')
        return {'start': start, 'times': [x['written_utc'] for x in mem],
                'source': SRC_BLOCK if source == 'block' else SRC_RECORD,
                'post': S0_RA4 in reasons, 'reading': reading, 'reasons': reasons}

    def prepare_stage0(self):
        self.s0_defect = None
        self.s0_status, self.s0_facts = self.stage0_status()
        self.s0_state = None
        self.s0_twin = None
        if self.phase != 'PHASE_2':
            # c2v004 RL5: with refused phase inputs (phase null) header.stage0_status reads the record
            # (README_SCHEMA_C4V003 L61); a missing or malformed record is a field of the STAGE0 alternative, which
            # reads TWIN_INPUT_DEFECT with its stop (PREREG L213, L217; README c4v002 L84, c4v003 L89, F8;
            # OUTPUT_CONSTANTS_C4V003 L333), printed beside PHASE_MISMATCH.  PHASE_MISMATCH is class ALL, so no output
            # value changes; stops and status_code do.
            if self.phase is None and self.s0_defect is not None and self.s0_defect[0] == 'RECORD':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: STAGE0 status record missing or malformed', alternative=STAGE0)
            return
        if self.s0_defect is not None:
            kind, word = self.s0_defect
            if kind == 'BLOCK':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: the frozen stage0_status block of the STAGE0 successor is not '
                          'bound or malformed (%s)' % word, alternative=STAGE0)
            else:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: STAGE0 status record missing or malformed', alternative=STAGE0)
            return
        if self.s0_status['status'] != EBF:
            return
        a = self.alt_entry(STAGE0)
        if a is not None and not self.alt_stopped(STAGE0) and a.get('scored') is not True:
            self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                      'STAGE0_GRID_OUTER: evaluated by the receipt rule but not scored', alternative=STAGE0)
        if a is None or self.alt_stopped(STAGE0) or self.ref is None:
            self.s0_state = 'ALTSTOP'
            return
        scope = a.get('scoring_scope')
        scope_ids = scope.get('query_ids') if type(scope) is dict else None
        if type(scope_ids) is not list:
            scope_ids = None
        st, rows = self.twin_rows(STAGE0, a, scope_ids if scope_ids is not None else OUTER_IDS)
        if st == 'OK' and scope_ids is not None and list(scope_ids) != OUTER_IDS:
            st = 'IDS'
        if st == 'DEFECT':
            self.s0_state = 'ALTSTOP'
        else:
            self.s0_state = st
            self.s0_twin = rows

    # ------------------------------------------------------------- phase1 tool pin (C1, C6; c2v003 RC3)
    def tool_module(self):
        """-> the module the bundle's phase1_tool binds, or None (PHASE1_TOOL_PIN_DEFECT): exactly a full sha of
        PHASE1_TOOL_SHA256 with that sha's module.  A value sharing only a prefix never binds."""
        tool = self.bundle['phase1_tool']
        if tool is None or not is_hex64(tool.get('sha256')):
            return None
        mod = PHASE1_TOOL_SHA256.get(tool['sha256'])
        return mod if mod is not None and tool.get('module') == mod else None

    # ------------------------------------------------------------- band column (C-1.1, M-16)
    def band_column(self):
        self.band = {}
        module = self.tool_module()
        self.p1_module = module
        code = None
        l1 = self.inp['l1_record']
        hdr = self.inp['phase_inputs'].get('phase1_header') if type(self.inp['phase_inputs']) is dict else None
        # c2v005 RC7: the L1 record is read only in the band command's form at the pinned sha (phase1_c2v003b
        # 7d891ff7 L942-L947, phase1_c2v002 d64351ec L838-L843): schema PHASE1_L1_C2V001, module the pinned tool's
        # MODULE, label exactly the band label the command writes, the band rows under 'rows'.  Ruling 2 (triage
        # c2v002 RC15), the seal candidate's printed form: bytes that do not hash to the bundle pin read
        # L1_SHA_MISMATCH, and the record-level conditions are checked in the order tool pin, load status, record
        # form, the phase1_header.l1_sha256 comparison.
        if module is None:
            code = 'PHASE1_TOOL_PIN_DEFECT'
        elif self.err['l1_record'] == 'SHA_MISMATCH':
            code = 'L1_SHA_MISMATCH'
        elif self.err['l1_record'] is not None:
            code = 'L1_RECORD_DEFECT'
        elif (type(l1) is not dict or l1.get('schema') != L1_SCHEMA or l1.get('module') != module
              or l1.get('label') != BAND_LABEL or _l1_rows(l1) is None):
            code = 'L1_RECORD_DEFECT'
        elif type(hdr) is not dict or self.rawsha['l1_record'] != hdr.get('l1_sha256'):
            code = 'L1_SHA_MISMATCH'
        for i, q in enumerate(QIDS):
            if code is not None:
                self.band[q] = {'label': BAND_LABEL, 'condition': BAND_CONDITION, 'overlaps': na([code])}
                continue
            lr = _l1_rows(l1)[i]
            row_ok = type(lr) is dict and lr.get('id') == q and lr.get('status') in ('AVAILABLE', 'NOT_AVAILABLE')
            src = self.ref_rows[i] if self.ref_rows is not None else {}
            e = K.band_column_v002.band_entry(q, lr if row_ok else None,
                                              src.get('observed_speed_km_s'), src.get('quoted_sigma_km_s'))
            ent = {'label': BAND_LABEL, 'condition': BAND_CONDITION}
            if e['code'] is None:
                ent['overlaps'] = 'yes' if e['overlaps'] else 'no'
                ent['fd_noise_not_bounded'] = e['fd_noise_not_bounded']
            else:
                ent['overlaps'] = na([e['code']])
                if e['code'] != 'L1_ROW_DEFECT':
                    # contract (C-1.1): the flag is set when the record's fd_noise is the string
                    ent['fd_noise_not_bounded'] = (type(lr) is dict and lr.get('fd_noise') == 'FD_NOISE_NOT_BOUNDED')
            self.band[q] = ent

    # ------------------------------------------------------------- engine (C-2, C-1.1 map)
    def codes_d(self):
        return self.codes('ROW', 'GATE')

    def engine(self, rows, twin=False):
        """Three-valued classification over fixed and defective rows."""
        E = {'zones': {}}
        byz = {z: [r for r in rows if r.zone == z] for z in ZONES}
        for z in ZONES:
            byz[z].sort(key=lambda r: (r.radius if r.radius is not None else 0.0, QIDS.index(r.qid)))
        E['byz'] = byz
        PK = K.partial_zone
        KMAP = {'H': 'HIT', 'MS': 'SIGNED_MISS', 'MN': 'NULL_MISS', 'L': 'LATE', 'I': 'INVALID'}
        states = {}
        for z in ZONES:
            opts = [sorted(KMAP[k] for k in r.possible()) for r in byz[z]]
            fixed, _amb = PK.partial_zone(opts)
            zs = {'fixed': fixed, 'has_def': any(not r.fixed for r in byz[z])}
            st = {(0, 0, 0, 0, 0)}
            vec = {'H': (1, 0, 0, 0, 0), 'MS': (0, 1, 0, 0, 0), 'MN': (0, 0, 1, 0, 0),
                   'L': (0, 0, 0, 1, 0), 'I': (0, 0, 0, 0, 1)}
            for r in byz[z]:
                incs = {vec[k] for k in r.possible()}
                st = {tuple(a + b for a, b in zip(s, inc)) for s in st for inc in incs}
            states[z] = st
            if not zs['has_def']:
                ratios = [r.ratio for r in byz[z] if r.kind in ('H', 'MS')]
                m = median(ratios) if ratios else 'UNDEFINED'
                md, su = fixed['miss_dominated'], fixed['sign_is_undefined']
                if su:
                    S = 'UNDEFINED'
                elif m < -1:
                    S = 'DEFICIT'
                elif m > 1:
                    S = 'EXCESS'
                else:
                    S = 'CENTERED'
                zs['m'], zs['S'] = m, S
            else:
                zs['m'] = zs['S'] = None
            E['zones'][z] = zs
        E['states'] = states

        def feat(s):
            h, ms, mn, l, i = s
            nv = h + ms + mn + l
            M = ms + mn + l
            md = nv > 0 and 2 * M >= nv
            return {'nv': nv, 'h': h, 'M': M, 'md': md, 'hd': nv > 0 and 2 * h > nv,
                    'su': (h + ms == 0) or (md and 2 * ms < nv), 'fm': ms + mn > 0, 'i': i,
                    'l': l, 'mn': mn, 'def': h + ms}

        feats = {z: [feat(s) for s in states[z]] for z in ZONES}
        E['feats'] = feats

        def cross(fn, keys):
            proj = {}
            for z in ZONES:
                proj[z] = {tuple(f[k] for k in keys) for f in feats[z]}
            vals = set()
            for a, b, c in product(proj['INNER'], proj['TRANSITION'], proj['OUTER']):
                vals.add(fn(dict(zip(keys, a)), dict(zip(keys, b)), dict(zip(keys, c))))
                if len(vals) > 1:
                    return None
            return vals.pop()

        def one(z, fn):
            vals = {fn(f) for f in feats[z]}
            return vals.pop() if len(vals) == 1 else None

        V = {}
        V['OF'] = one('OUTER', lambda f: f['md'])
        V['E3'] = one('OUTER', lambda f: E3_NEG if f['md'] else (E3_NOTNEG if f['nv'] > 0 else E3_NT))
        V['P0'] = cross(lambda a, b, c: a['i'] > 0 or b['i'] > 0 or c['i'] > 0, ('i',))
        V['P5'] = cross(lambda a, b, c: a['hd'] and c['md'] and b['nv'] > 0 and not b['hd'],
                        ('hd', 'md', 'nv'))
        V['P7'] = cross(lambda a, b, c: (a['M'] + b['M'] + c['M'] > 0) and not (a['md'] or b['md'] or c['md']),
                        ('M', 'md'))
        V['P8'] = cross(lambda a, b, c: (a['nv'] + b['nv'] + c['nv'] > 0) and (a['M'] + b['M'] + c['M'] == 0),
                        ('nv', 'M'))
        V['P9'] = one('OUTER', lambda f: f['nv'] == 0)
        V['P13'] = one('TRANSITION', lambda f: f['md'])
        V['P14'] = one('OUTER', lambda f: f['md'] and f['su'])
        V['P15'] = one('INNER', lambda f: f['md'] and f['su'])
        mm = {}
        for idx, z in enumerate(ZONES):
            mm[z] = cross(lambda a, b, c, idx=idx: (a['md'] or b['md'] or c['md']) and not (a, b, c)[idx]['md']
                          and (a, b, c)[idx]['fm'], ('md', 'fm'))
        V['MM'] = mm
        V['ONM'] = one('OUTER', lambda f: f['nv'] > 0 and f['M'] == 0)
        V['OL'] = one('OUTER', lambda f: f['l'])
        zf = {z: E['zones'][z]['fixed'] for z in ZONES}

        def zget(z, key):
            return zf[z].get(key)
        # value-level patterns with the closed deduction list (C-1.1)
        for pid, z, cls in (('P1', 'OUTER', 'DEFICIT'), ('P2', 'OUTER', 'EXCESS'), ('P11', 'OUTER', 'CENTERED'),
                            ('P3', 'INNER', 'EXCESS'), ('P4', 'INNER', 'DEFICIT'), ('P12', 'INNER', 'CENTERED')):
            zs = E['zones'][z]
            if not zs['has_def']:
                V[pid] = bool(zget(z, 'miss_dominated') and zs['S'] == cls)
            elif zget(z, 'miss_dominated') is False or zget(z, 'sign_is_undefined') is True:
                V[pid] = False
            else:
                V[pid] = None
        if not any(E['zones'][z]['has_def'] for z in ZONES):
            Si, St, So = (E['zones'][z]['S'] for z in ZONES)
            V['P6'] = Si == St == So and Si in ('DEFICIT', 'EXCESS')
        elif any(zget(z, 'sign_is_undefined') is True for z in ZONES):
            V['P6'] = False
        else:
            V['P6'] = None
        to_def = E['zones']['TRANSITION']['has_def'] or E['zones']['OUTER']['has_def']
        if not to_def:
            orows = [r for r in byz['OUTER'] if r.kind in ('H', 'MS')]
            rat = [r.ratio for r in orows]
            n = len(rat)
            if n >= 2:
                near, far = rat[:n // 2], rat[n // 2:]
                fm = median(far)
                delta = fm - median(near)
            else:
                fm = delta = 'UNDEFINED'
            mT, mO, SO = E['zones']['TRANSITION']['m'], E['zones']['OUTER']['m'], E['zones']['OUTER']['S']
            trend = (delta != 'UNDEFINED' and delta < 0 and mT != 'UNDEFINED' and mO != 'UNDEFINED' and mT > mO)
            V['GROWING'] = bool(SO == 'DEFICIT' and trend)
            V['CROSSING'] = bool(SO == 'CENTERED' and trend and fm != 'UNDEFINED' and fm < -1)
            V['delta'], V['far'] = delta, fm
            V['P1g'] = bool(V['P1'] and V['GROWING'])
            V['P11g'] = bool(V['P11'] and V['CROSSING'])
        else:
            V['delta'] = V['far'] = None
            if zget('OUTER', 'sign_is_undefined') is True:
                V['GROWING'] = V['CROSSING'] = V['P1g'] = V['P11g'] = False
            else:
                V['GROWING'] = V['CROSSING'] = V['P1g'] = V['P11g'] = None
        # P10 (count-level over Q25's kinds)
        q25 = [r for r in rows if r.qid == Q25]
        if twin:
            V['P10'] = 'NOT_EVALUATED_FOR_ALTERNATIVE'
        elif not q25:
            V['P10'] = False
        else:
            vals = {k in FROZEN_MISS_KINDS for k in q25[0].possible()}
            V['P10'] = vals.pop() if len(vals) == 1 else None
        # onset radius (count-level; F3: LATE and null-ratio rows count)
        to_rows = sorted(byz['TRANSITION'] + byz['OUTER'],
                         key=lambda r: (r.radius if r.radius is not None else 0.0, QIDS.index(r.qid)))
        onset = 'NONE'
        for r in to_rows:
            ps = r.possible()
            miss = {k in MISS_KINDS for k in ps}
            if miss == {False}:
                continue
            onset = {'id': r.qid, 'R_q': r.rad_text} if miss == {True} else None
            break
        V['onset'] = onset
        E['V'] = V
        return E

    # ------------------------------------------------------------- output pieces
    def labels(self):
        out = []
        s = self.inp['score']
        ir = s.get('incomplete_reasons') if type(s) is dict else None
        irs = sorted(ir) if (type(ir) is list and all(type(x) is str for x in ir)) else na(['FIELD_DEFECT_OUTSIDE_ROWS'])
        if self.phase == 'PHASE_1':
            out.append({'label': LABEL_P1, 'incomplete_reasons': irs})
        elif type(s) is dict and s.get('freeze_status') == 'FREEZE_INCOMPLETE':
            out.append({'label': LABEL_INCOMPLETE, 'incomplete_reasons': irs})
        c = self.inp['ntest_compare']
        gate = c.get('n_route_ab_gate') if type(c) is dict else None
        if gate != 'OPEN':
            out.append({'label': LABEL_NGATE, 'gate': gate if type(gate) is str else NA})
        if self.phase == 'PHASE_2':
            cs = self.commitment()
            if cs['status'] == 'EXPLORATORY':
                out.append({'label': LABEL_EXPL, 'code': cs.get('code')})
        fb = self.inp['fallback']
        if type(fb) is dict and fb.get('classification_label') in FALLBACK_LABELS:
            out.append({'label': fb['classification_label']})
        return out

    def commitment(self):
        rec = self.inp['commitment_status'] if self.err['commitment_status'] is None else None
        status, code = K.root_contracts.commitment(rec)
        if code is not None:
            return {'status': 'EXPLORATORY', 'code': code, 'stops_or_changes': na([code])}
        if status == 'COMMITTED':
            return {'status': 'COMMITTED', 'stops_or_changes': []}
        return {'status': 'EXPLORATORY', 'stops_or_changes': rec['stops_or_changes'], 'code': None}

    def header(self):
        b = self.bundle
        ins = b['inputs']

        def pin_sha(role):
            return ins[role]['sha256'] if ins[role] is not None else None
        s = self.inp['score']
        h = {
            'phase': self.phase, 'manifest_phase_derived': self.manifest_phase,
            'sealed_text_sha256': b['sealed']['text']['sha256'],
            'classifier_sha256': b['sealed']['classifier']['sha256'],
            'freeze_manifest_sha256': pin_sha('freeze_manifest'), 'slots_sha256': pin_sha('slots'),
            'module_sha256': b['module_sha256'],
            'roster_sha256': {k: v['sha256'] for k, v in b['rosters'].items()},
            'tsr_records': {'flag_record_sha256': pin_sha('tsr_flag_record'),
                            'support_record_sha256': pin_sha('tsr_support_record'),
                            'compare_sha256': pin_sha('ntest_compare'),
                            'n1_record_sha256': N1_SHA, 'gl_node_record_sha256': NODE_SHA},
            'gate_status_list': self.gate_echo if self.gates is not None else na(['GATE_STATUS_LIST_DEFECT']),
            'freeze_status': (s.get('freeze_status') if type(s) is dict else NA),
            'field_map': self.field_map_status,
            'disclosures_D1_D3': list(DISCLOSURES),
            'root_disclosures': (self.inp['root_disclosures'] if type(self.inp['root_disclosures']) is dict
                                 else na(['ROOT_DISCLOSURES_NOT_SUPPLIED'])),
            'stage0_status': self.s0_status,
        }
        if type(s) is dict:
            h['score_echo'] = {k: s.get(k, NA) for k in ('manifest_file_sha256_expected',
                                                          'manifest_file_sha256_actual',
                                                          'registration_file_sha256', 'manifest_sha256_self')}
        if self.phase == 'PHASE_1':
            pi = self.inp['phase_inputs']
            h['phase1'] = {'label': LABEL_P1, 'phase1_header': pi.get('phase1_header'),
                           'l1_sha256': pin_sha('l1_record')}
        if self.phase == 'PHASE_2':
            h['commitment_status'] = self.commitment()
            h['agree_record_sha256'] = pin_sha('agree_record')
            h['phase1_classification_sha256'] = pin_sha('phase1_classification')
            h['attestation_scope'] = P2_ATTEST
        return h

    def headline_out(self):
        s = self.inp['score']
        h = s.get('headline') if type(s) is dict else None
        if type(h) is not dict:
            return na(['FIELD_DEFECT_OUTSIDE_ROWS'])
        return {k: h.get(k, NA) for k in ('member_within_error_counts', 'reference_member_id',
                                          'reference_member_log_index', 'reference_within_error_count',
                                          'n_members', 'n_members_valid')}

    def fallback_out(self):
        if self.bundle['inputs']['fallback'] is None:
            return {'applies': False}
        fb = self.inp['fallback']
        if self.err['fallback'] is not None or not K.record_shapes.shape_ok('fallback', fb):
            return na(['FALLBACK_RECORD_DEFECT'])
        return fb

    def tier_key(self, row):
        return {'H': 'WITHIN_ERROR', 'MS': 'MISS_WORST_TIER', 'MN': 'MISS_WORST_TIER',
                'L': 'LATE_GATE_MISS'}.get(row.kind) or ('INVALID_AS_MISS:' + row.reason)

    @staticmethod
    def tier_of(kind):
        return {'H': 'HIT', 'MS': 'MISS', 'MN': 'MISS', 'I': 'INVALID_AS_MISS', 'L': 'INVALID_AS_MISS'}[kind]

    def near_out(self, row):
        if not row.fixed:
            return na(self.codes_d())
        if type(row.near) is tuple:
            return na(row.near[1])
        return row.near

    def row_out(self, row):
        cd = na(self.codes_d())
        base = {'id': row.qid, 'zone': row.zone, 'R_q': row.rad_text, 'notes': D2_NOTE,
                'near_label': NEAR_LABEL}
        if not row.fixed:
            for k in ('tier', 'reading_kind', 'r_q', 'sign', 'frozen_prediction', 'near', 'tsr_flag',
                      'invalid_reason', 'gate_status', 'gate_after_predictions', 'sensitivity_band_overlap',
                      'tier_key'):
                base[k] = cd
            if self.phase == 'PHASE_1':
                base['phase1_band'] = cd
            return base
        k = row.kind
        base.update({
            'tier': self.tier_of(k), 'reading_kind': KIND_NAME[k],
            'r_q': row.ratio if k in ('H', 'MS') else None,
            'sign': sign_of(row.ratio) if k in ('H', 'MS') else ('UNDEFINED' if k == 'MN' else 'NONE'),
            'frozen_prediction': k in ('H', 'MS', 'MN'),
            'near': self.near_out(row),
            'tsr_flag': na(['TSR_FLAG_TABLE_MISMATCH']) if self.tsr_stop else (row.qid == Q25),
            'invalid_reason': row.reason if k in ('I', 'L') else None,
            'gate_status': row.gate_status if k in ('I', 'L') else None,
            'gate_after_predictions': k == 'L',
            'sensitivity_band_label': SENS_LABEL,
            'tier_key': self.tier_key(row),
        })
        if self.phase == 'PHASE_1':
            base['sensitivity_band_overlap'] = 'invalid'
            base['phase1_band'] = self.band[row.qid]
        else:
            if row.qid in self.sens_bad:
                base['sensitivity_band_overlap'] = na(['FIELD_DEFECT_SENSITIVITY'])
            else:
                sr = self.sens[row.qid]
                base['sensitivity_band_overlap'] = (('yes' if sr['band_overlaps_error_bar'] else 'no')
                                                    if sr['valid'] else 'invalid')
        return base

    def ipr(self, zrows, twin=False):
        counts = {}
        na_reasons = set()
        whole = False
        for r in zrows:
            if r.fixed:
                if r.kind == 'I':
                    counts[r.reason] = counts.get(r.reason, 0) + 1
            elif 'I' in r.kinds:
                rs = r.kind_reason.get('I')
                if rs is None:
                    whole = True
                else:
                    na_reasons.add(rs)
        if whole:
            return na(self.codes_d())
        out = {k: v for k, v in counts.items()}
        for rs in na_reasons:
            out[rs] = na(self.codes_d())
        return out

    def zone_n(self, zrows):
        codes = set()
        n = 0
        for r in zrows:
            if not r.fixed:
                codes |= set(self.codes_d())
            elif r.kind in ('MS', 'MN'):
                if type(r.near) is tuple:
                    codes |= set(r.near[1])
                elif r.near is True:
                    n += 1
        return na(codes) if codes else n

    def zone_out(self, E, z, labels, twin=False):
        zs = E['zones'][z]
        fx = zs['fixed']
        cd = na(self.codes_d())

        def g(key):
            return fx[key] if key in fx else cd
        out = {'N_v': g('N_v'), 'H': g('H'), 'M': g('M'), 'U': g('U'), 'I': g('I'),
               'I_per_reason': self.ipr(E['byz'][z]),
               'miss_dominated': g('miss_dominated'), 'hit_dominated': g('hit_dominated'),
               'S_is_UNDEFINED': g('sign_is_undefined'),
               'm': zs['m'] if not zs['has_def'] else cd, 'S': zs['S'] if not zs['has_def'] else cd,
               'N': 0 if twin else self.zone_n(E['byz'][z]), 'labels': labels}
        return out

    def val(self, v):
        return na(self.codes_d()) if v is None else v

    def patterns_out(self, E, labels, zones_out):
        V = E['V']
        p = {}
        for pid in PATTERN_IDS:
            if pid == 'P10':
                p[pid] = na(['TSR_FLAG_TABLE_MISMATCH']) if self.tsr_stop else self.val(V['P10'])
            else:
                p[pid] = self.val(V[pid])
        p['labels'] = labels
        p['names'] = dict(PATTERN_NAMES)
        p['P0_per_zone_per_reason'] = {z: zones_out[z]['I_per_reason'] for z in ZONES}
        if p['P13'] is True:
            p['P13_sign_class'] = zones_out['TRANSITION']['S']
        if p['P8'] is True:
            p['P8_reported_with'] = {'I': {z: zones_out[z]['I'] for z in ZONES},
                                     'N': {z: zones_out[z]['N'] for z in ZONES}, 'note': P8_NOTE}
        return p

    # ------------------------------------------------------------- readings (C-3)
    def trig_value(self, E, t):
        V = E['V']
        if t == 'OF':
            return V['OF']
        if t.startswith('MM:'):
            return V['MM'][t[3:]]
        if t == 'P10':
            return None if self.tsr_stop else V['P10']
        return V[t]

    def scope_rows(self, token):
        if token == 'ALL':
            return QIDS
        if token == 'FLAGGED':
            return [Q25]
        return [q for q in QIDS if ZONE_OF[q] == token]

    def readings(self, E, labels, s0):
        V = E['V']
        cd = self.codes_d()
        out = []
        for name in READINGS:
            if name == 'R-TSR' and self.tsr_stop:
                out.append({'reading': 'R-TSR', 'labels': labels, NA: ['TSR_FLAG_TABLE_MISMATCH']})
                continue
            tv = [(t, self.trig_value(E, t)) for t in TRIGGERS[name]]
            kept = [(t, v) for t, v in tv if v is not False]
            th = [{'trigger': t, 'holds': True if v is True else na(cd)} for t, v in kept]
            scope = sorted({TRIGGER_SCOPE[t] for t, _ in kept})
            cited, cna = set(), set()
            for q in QIDS:
                row = self.row_by_id[q]
                ps = row.possible()
                is_miss = {k in FROZEN_MISS_KINDS for k in ps}
                if is_miss == {False}:
                    continue
                in_true = any(v is True and q in self.scope_rows(TRIGGER_SCOPE[t]) for t, v in kept)
                in_any = any(q in self.scope_rows(TRIGGER_SCOPE[t]) for t, v in kept)
                if in_true and is_miss == {True}:
                    cited.add(q)
                elif in_any:
                    cna.add(q)
            any_t = tri_or(*[v for _, v in tv]) if tv else False
            if name in ('R-UT1', 'R-REACH'):
                part1 = self.part1_deficit(E, any_t)
            elif name == 'R-DRIFT':
                part1 = self.part1_drift(any_t, s0)
            else:
                rel = K.partial_relations.partial_relation(any_t)
                if rel['relation_available'] and rel['code_available']:
                    part1 = {'relation': rel['relation'], 'code': rel['code']}
                else:
                    part1 = na(cd)
            if name == 'R-MF':
                part2 = {'status': V['E3'], 'test': 'E3_VERDICT_LINE'} if V['E3'] is not None else na(cd)
            elif name == 'R-DRIFT':
                part2 = s0['part2']
            else:
                part2 = {'status': 'OPEN', 'test': DECIDING[name][0], 'test_status': DECIDING[name][1]}
            ent = {'reading': name, 'labels': labels, 'triggers_holding': th, 'part1': part1,
                   'part2': part2, 'part3_prior_evidence': list(PRIOR[name]),
                   'sign_scope': SIGN_SCOPE.get(name, '-'), 'scope_zones': scope,
                   'cited_miss_rows': sorted(cited), 'cited_miss_rows_not_available': sorted(cna)}
            if name == 'R-HIST':
                q = tri_or(V['P1g'], V['P11g'])
                ent['qualifier_missing_long_range_component'] = na(cd) if q is None else q
            out.append(ent)
        return out

    def outer_neg_miss(self, E):
        orows = E['byz']['OUTER']
        if any(r.fixed and r.kind == 'MS' and r.ratio < 0 for r in orows):
            return True
        if any((not r.fixed) and 'MS' in r.kinds for r in orows):
            return None
        return False

    def part1_deficit(self, E, of):
        cd = na(self.codes_d())
        V = E['V']
        if of is False:
            return {'relation': 'NOT_ADDRESSED', 'code': 'PATTERN_NOT_HELD'}
        if of is None:
            return cd
        zo = E['zones']['OUTER']
        if not zo['has_def']:
            sdef, scen = zo['S'] == 'DEFICIT', zo['S'] == 'CENTERED'
        elif zo['fixed'].get('sign_is_undefined') is True:
            sdef = scen = False
        else:
            sdef = scen = None
        neg = self.outer_neg_miss(E)
        cons = tri_and(tri_or(sdef, scen), neg)
        if cons is True:
            return {'relation': 'CONSISTENT', 'code': None}
        if cons is None:
            return cd
        if V['P2'] is True:
            return {'relation': 'NOT_ADDRESSED', 'code': 'SIGN_SCOPE_EXCESS'}
        if V['P2'] is None:
            return cd
        if V['P14'] is True:
            return {'relation': 'NOT_ADDRESSED', 'code': 'SIGN_SCOPE_UNSIGNED'}
        if V['P14'] is None:
            return cd
        if V['P11'] is True and neg is False:
            return {'relation': 'NOT_ADDRESSED', 'code': 'SIGN_SCOPE_NO_DEFICIT_MISS'}
        return cd

    def part1_drift(self, of, s0):
        if of is False:
            return {'relation': 'NOT_ADDRESSED', 'code': 'PATTERN_NOT_HELD'}
        extra = s0['part2'].get('reasons', []) if s0['part2'].get('status') == 'OPEN' else []
        if of is None or NA in s0['part2']:
            return na(set(self.codes_d()) | set(extra))
        if s0['part2']['status'] == 'AGAINST':
            return {'relation': 'INCONSISTENT', 'code': None}
        return {'relation': 'CONSISTENT', 'code': None}

    # ------------------------------------------------------------- twins (C-6.1)
    def twin_row_out(self, row):
        k = row.kind
        return {'id': row.qid, 'zone': row.zone, 'tier': self.tier_of(k), 'reading_kind': KIND_NAME[k],
                'r_q': row.ratio if k in ('H', 'MS') else None,
                'sign': sign_of(row.ratio) if k in ('H', 'MS') else ('UNDEFINED' if k == 'MN' else 'NONE'),
                'invalid_reason': row.reason if k in ('I', 'L') else None, 'gate_after_predictions': k == 'L'}

    def classify_twin(self, rows, labels):
        E = self.engine(rows, twin=True)
        self._xcheck(E, rows, True)
        zones = {z: self.zone_out(E, z, labels, twin=True) for z in ZONES}
        V = E['V']
        pats = {pid: V[pid] for pid in PATTERN_IDS}
        pats['labels'] = labels
        return {'rows': [self.twin_row_out(r) for r in rows], 'zones': zones,
                'outer_trend': {'delta_out': V['delta'], 'far_half_median': V['far'],
                                'GROWING': V['GROWING'], 'CROSSING': V['CROSSING']},
                'outer_failure': V['OF'],
                'patterns': pats,
                'patterns_holding': [pid for pid in PATTERN_IDS if pid != 'P10' and V[pid] is True]}, E

    # ------------------------------------------------------------- DT-S0G (C-6.3, M-9 as ruled)
    def s0g_compare(self, labels):
        ref_o = [self.row_by_id[q] for q in OUTER_IDS]
        tw = {r.qid: r for r in self.s0_twin}
        qual = [q for q in OUTER_IDS if self.row_by_id[q].kind in ('H', 'MS') and tw[q].kind in ('H', 'MS')]
        if not qual:
            return {'qualifying_rows': [], 'H_P': 0, 'H_S': 0, 'A_P': 'UNDEFINED', 'A_S': 'UNDEFINED',
                    'result': 'NOT_DECIDED', 'labels': labels}
        hp = sum(1 for q in qual if self.row_by_id[q].kind == 'H')
        hs = sum(1 for q in qual if tw[q].kind == 'H')
        ap = median([abs(self.row_by_id[q].ratio) for q in qual])
        as_ = median([abs(tw[q].ratio) for q in qual])
        if hs > hp and as_ < ap:
            res = 'CONSISTENT'
        elif hs <= hp and as_ >= ap:
            res = 'AGAINST'
        else:
            res = 'NOT_DECIDED'
        self._xcheck_drift(ref_o, [tw[q] for q in OUTER_IDS], res)
        return {'qualifying_rows': qual, 'H_P': hp, 'H_S': hs, 'A_P': ap, 'A_S': as_,
                'rows': [{'id': q, 'r_q_reference': self.row_by_id[q].ratio, 'r_q_stage0': tw[q].ratio}
                         for q in qual],
                'result': res, 'labels': labels}

    def stage0_block(self, labels, outer_def):
        """-> (stage0 object, R-DRIFT part2)."""
        if self.phase == 'PHASE_1':
            return ({'status': NEBF, 'reasons': ['NOT_IN_PHASE_1'], 'comparison': None},
                    {'status': 'OPEN', 'test': 'DT-S0G', 'code': NEBF, 'reasons': ['NOT_IN_PHASE_1']})
        st = dict(self.s0_status)
        if st['status'] == NA:
            st['twin'] = 'TWIN_INPUT_DEFECT'
            st['comparison'] = None
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': 'TWIN_INPUT_DEFECT',
                        'reasons': list(st['reasons'])}
        st['comparison'] = None
        if st['status'] == NEBF:
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': NEBF, 'reasons': list(st['reasons'])}
        if st['status'] == EREF:
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': EREF, 'reasons': []}
        if self.s0_state == 'ALTSTOP':
            st['twin'] = 'TWIN_INPUT_DEFECT'
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': 'TWIN_INPUT_DEFECT',
                        'reasons': ['FIELD_DEFECT_ALTERNATIVE']}
        if self.s0_state == 'INVALID':
            st['twin'] = 'TWIN_INVALID'
            st['twin_detail'] = None
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': 'TWIN_INVALID', 'reasons': []}
        if self.s0_state == 'IDS':
            st['twin'] = 'TWIN_INPUT_DEFECT'
            st['twin_detail'] = TWIN_IDS_DIFFER
            return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': 'TWIN_INPUT_DEFECT', 'reasons': []}
        tc, _ = self.classify_twin(self.s0_twin, labels)
        st['label'] = S0_LABEL
        st['twin_classification'] = tc
        if outer_def:
            st['comparison'] = dict(na(self.codes_d()), labels=labels)
            return st, na(self.codes_d())
        st['stage0_within_error_distribution'] = {'n': 8, 'within_error': sum(1 for r in self.s0_twin if r.kind == 'H')}
        st['denominator'] = 8
        cmp_ = self.s0g_compare(labels)
        st['comparison'] = cmp_
        if cmp_['result'] in ('CONSISTENT', 'AGAINST'):
            return st, {'status': cmp_['result'], 'test': 'DT-S0G'}
        return st, {'status': 'OPEN', 'test': 'DT-S0G', 'code': 'NOT_DECIDED', 'reasons': []}

    def alternatives_out(self, labels, stage0_obj):
        out = []
        names = list(ALT_ORDER)
        alts = self.score_alternatives()
        if alts is not None and any(type(a) is dict and a.get('name') == DIST_ALT for a in alts):
            names.append(DIST_ALT)
        self.ok_twin = None
        for n in names:
            if n == 'ORIGINAL_K' and self.phase == 'PHASE_1':
                out.append({'name': n, 'status': NA, 'reason': 'ORIGINAL_K_NOT_AVAILABLE_IN_PHASE_1 (I-4; budget 0)'})
                continue
            if self.alt_stopped(n):
                out.append({'name': n, 'status': 'TWIN_INPUT_DEFECT', 'codes': ['FIELD_DEFECT_ALTERNATIVE']})
                continue
            a = self.alt_entry(n)
            if n == DIST_ALT:
                out.append({'name': n, 'status': a.get('status'), 'note': NOT_EVAL_NOTE})
                continue
            if n == 'ORIGINAL_K':
                if a.get('status') != EBF:
                    out.append({'name': n, 'status': NA, 'reason': 'ORIGINAL_K changed to NOT_EVALUATED (A16.2): NOT_AVAILABLE'})
                    continue
                if a.get('scored') is not True:
                    out.append({'name': n, 'status': EBF, 'note': NOT_EVAL_NOTE})
                    continue
            elif a.get('status') != EBF or a.get('scored') is not True:
                out.append({'name': n, 'status': a.get('status'), 'note': NOT_EVAL_NOTE})
                continue
            st = self.alt_state.get(n)
            if st == 'INVALID':
                mwe = a.get('member_within_error_counts')
                out.append({'name': n, 'status': 'TWIN_INVALID',
                            'member_within_error_counts': mwe if type(mwe) is dict else NA})
            elif st == 'IDS':
                out.append({'name': n, 'status': 'TWIN_INPUT_DEFECT', 'detail': TWIN_IDS_DIFFER})
            elif st == 'OK':
                tc, _ = self.classify_twin(self.twin_class[n], labels)
                out.append({'name': n, 'status': EBF, 'twin_log_index': self.ref['log_index'],
                            'classification': tc, 'headline': False, 'note': TWIN_NOTE})
                if n == 'ORIGINAL_K':
                    self.ok_twin = tc
            else:
                out.append({'name': n, 'status': 'TWIN_INPUT_DEFECT', 'codes': ['FIELD_DEFECT_ALTERNATIVE']})
        s0e = {'name': STAGE0}
        for k in ('status', 'reasons', 'twin', 'label'):
            if k in stage0_obj:
                s0e[k] = stage0_obj[k]
        out.append(s0e)
        return out

    # ------------------------------------------------------------- item 11 (C-8, F2, A144/A149, v003b)
    def parse_agree(self):
        """-> (word or None, record)."""
        rec = self.inp['agree_record']
        if self.err['agree_record'] is not None:
            return self.err['agree_record'], None
        mod = self.p1_module
        if mod is None:
            return 'PHASE1_TOOL_PIN_DEFECT', None
        if type(rec) is not dict or rec.get('module') != mod:
            return 'MODULE', None
        sch = rec.get('schema')
        if sch in (AT0A, AT0B) and rec.get('outcome') != 'AGREEMENT_DEFECT':
            return 'AT0_RECORD', None
        v3 = mod == PHASE1_V003B
        if sch == AT0B and v3:
            if not is_hex64(rec.get('members_sha256')):
                return 'AT0B_MEMBERS_SHA256', None
            if not is_hex64(rec.get('values_sha256')):
                return 'AT0B_VALUES_SHA256', None
        if sch not in (AT1, AT0A, AT0B):
            return 'SCHEMA', None
        oc = rec.get('outcome')
        if oc not in AGREE_OUTCOMES:
            return 'OUTCOME', None
        # c2v005 RC8: the at1 command writes at0, the list of the two AT-0 records' outcomes, beside schema, module and
        # outcome in every outcome (phase1_c2v003b 7d891ff7 L1287-L1292, phase1_c2v002 d64351ec L1043); it is a field
        # of the AT1 record itself, so AGREEMENT_DEFECT does not excuse it.  Missing or not two strings: the record's
        # outcome fields are not in the command's form, word OUTCOME (the seal candidate's word).
        if sch == AT1:
            a0 = rec.get('at0')
            if type(a0) is not list or len(a0) != 2 or any(type(x) is not str for x in a0):
                return 'OUTCOME', None
        if oc != 'AGREEMENT_DEFECT':
            for k in ('failing', 'non_discriminating_rows', 'reported'):
                if k not in rec:
                    return 'MISSING:' + k, None
        if 'non_discriminating_rows' in rec:
            nd = rec['non_discriminating_rows']
            if type(nd) is not list or any(x not in QIDS for x in nd) or len(set(nd)) != len(nd):
                return 'NON_DISCRIMINATING_ROWS', None
        fails = rec.get('failing', [])
        if 'failing' in rec:
            if type(fails) is not list:
                return 'FAILING', None
            for f in fails:
                w = self._failing_word(f, v3)
                if w:
                    return w, None
        if oc == 'SUPERSEDED' and not fails:
            return 'SUPERSEDED_WITHOUT_FAILING', None
        if oc == 'COVERED' and fails:
            return 'COVERED_WITH_FAILING', None
        if 'reported' in rec:
            w = self._reported_word(rec['reported'], v3)
            if w:
                return w, None
        return None, rec

    @staticmethod
    def _failing_word(f, v3):
        if type(f) is not dict:
            return 'FAILING_ENTRY'
        fam = ('TRUST_RADIUS', 'BOX', 'LINEAR_DDO')
        cat_of = {'TRUST_RADIUS': 'OUTSIDE_TRUST_RADIUS', 'BOX': 'OUTSIDE_BOX_SLICE',
                  'LINEAR_DDO': 'OUTSIDE_LINEAR_DDO_REGION'}
        if v3:
            keys = {'log_index', 'id', 'excess', 'norm_n', 'category', 'flag', 'flag_reason',
                    'region_rows_violated', 'region_max_violation', 'geometric_part', 'residual_part'}
            if set(f) != keys:
                return 'FAILING_KEYS_V003A'
            if f['category'] not in ('OUTSIDE_TRUST_RADIUS', 'OUTSIDE_BOX_SLICE', 'OUTSIDE_LINEAR_DDO_REGION',
                                     'NGC_NONLINEAR'):
                return 'CATEGORY'
            rv = f['region_rows_violated']
            if (type(rv) is not list or any(x not in fam for x in rv) or len(set(rv)) != len(rv)
                    or rv != [x for x in fam if x in rv]):
                return 'REGION_ROWS_VIOLATED'
            want = cat_of[rv[0]] if rv else 'NGC_NONLINEAR'
            if f['category'] != want:
                return 'CATEGORY_MAPPING'
            rm = f['region_max_violation']
            if type(rm) is not dict or set(rm) != set(fam) or not all(is_num(rm[k]) for k in fam):
                return 'REGION_MAX_VIOLATION'
            if not is_num(f['geometric_part']) or not is_num(f['residual_part']):
                return 'PARTS'
            fl, fr = f['flag'], f['flag_reason']
            ok = ((fl is None and fr is None) or (fl == 'FD_NOISE_NOT_BOUNDED' and fr == 'NO_ROW_EPS_Q')
                  or (fl == 'MEMBER_POINT_NOISE_NOT_BOUNDED' and fr in MEMBER_EPS_REASONS))
            if not ok:
                return 'FLAG_OR_FLAG_REASON'
        else:
            # c2v005 (V006 A190 ruling 2; triage c2v002 RC16): the seal candidate's printed word.  A v002 entry with
            # the six keys but a category outside the three v002 categories, or a flag outside {null,
            # FD_NOISE_NOT_BOUNDED}, reads FAILING_KEYS_V002.
            if (set(f) != {'log_index', 'id', 'excess', 'norm_n', 'category', 'flag'}
                    or f['category'] not in ('OUTSIDE_TRUST_RADIUS', 'OUTSIDE_LINEAR_DDO_REGION', 'NGC_NONLINEAR')
                    or f['flag'] not in (None, 'FD_NOISE_NOT_BOUNDED')):
                return 'FAILING_KEYS_V002'
        if (not is_int(f['log_index']) or f['id'] not in QIDS or not is_num(f['excess'])
                or not is_num(f['norm_n']) or f['norm_n'] < 0):
            return 'FAILING_VALUES'
        return None

    @staticmethod
    def _reported_word(rep, v3):
        v2keys = {'rows_not_tested_phase1_not_available', 'e_q_per_member_row', 'rows_fd_noise_not_bounded',
                  'ngc_linearity_residuals', 'envelope_vs_band_width', 'max_ddo_linearity_deviation_over_tau',
                  'identified_projection_vs_linear_region'}
        if not v3:
            if type(rep) is not dict or not v2keys <= set(rep):
                return 'REPORTED_KEYS'
            return None
        v3keys = v2keys | {'pairs_member_point_noise_not_bounded', 'band_region_extent',
                           'band_region_single_point', 'band_region_single_point_reason',
                           'band_region_box_only_extent'}
        if type(rep) is not dict or set(rep) != v3keys:
            return 'REPORTED_KEYS'
        eq = rep['e_q_per_member_row']
        if type(eq) is not list or any(type(x) is not dict or set(x) != {'log_index', 'id', 'e_q', 'eps_m', 'flag',
                                                                         'flag_reason'} for x in eq):
            return 'E_Q_PER_MEMBER_ROW'
        for x in eq:
            if not is_int(x['log_index']) or x['id'] not in QIDS:
                return 'E_Q_PER_MEMBER_ROW_VALUES'
            fl, fr = x['flag'], x['flag_reason']
            if fl is None and fr is None:
                ok = is_num(x['e_q']) and is_num(x['eps_m']) and x['eps_m'] >= 0
            elif fl == 'MEMBER_POINT_NOISE_NOT_BOUNDED':
                ok = fr in MEMBER_EPS_REASONS and is_num(x['e_q']) and x['eps_m'] is None
            elif fl == 'FD_NOISE_NOT_BOUNDED':
                ok = fr == 'NO_ROW_EPS_Q' and x['e_q'] == 'FD_NOISE_NOT_BOUNDED' and x['eps_m'] is None
            else:
                ok = False
            if not ok:
                return 'E_Q_PER_MEMBER_ROW_VALUES'
        pr = rep['pairs_member_point_noise_not_bounded']
        if type(pr) is not list or any(type(x) is not dict or set(x) != {'log_index', 'id', 'flag_reason'}
                                       or not is_int(x['log_index']) or x['id'] not in QIDS
                                       or x['flag_reason'] not in MEMBER_EPS_REASONS for x in pr):
            return 'PAIRS_MEMBER_POINT_NOISE_NOT_BOUNDED'
        lists = (rep['band_region_extent'], rep['band_region_box_only_extent'])
        if any(type(lst) is not list for lst in lists):
            return 'BAND_REGION_EXTENT_LIST'
        for lst in lists:
            for e in lst:
                if (type(e) is not dict or set(e) != {'direction', 'extent', 'lp_status'} or not is_int(e['direction'])
                        or type(e['extent']) is not list or len(e['extent']) != 2
                        or type(e['lp_status']) is not list or len(e['lp_status']) != 2
                        or not all(is_str(s) for s in e['lp_status'])):
                    return 'BAND_REGION_EXTENT_ENTRY'
        for lst in lists:
            for e in lst:
                for b, s in zip(e['extent'], e['lp_status']):
                    if not ((s == 'OPTIMAL' and is_num(b)) or (s != 'OPTIMAL' and b == NA)):
                        return 'BAND_REGION_EXTENT_VALUE'
        if [e['direction'] for e in lists[0]] != [e['direction'] for e in lists[1]]:
            return 'BAND_REGION_DIRECTIONS'
        sp = rep['band_region_single_point']
        if any(s != 'OPTIMAL' for e in lists[0] for s in e['lp_status']):
            want = NA
        else:
            want = all(e['extent'][0] == 0.0 and e['extent'][1] == 0.0 for e in lists[0])
        if type(sp) is not type(want) or sp != want:
            return 'BAND_REGION_SINGLE_POINT'
        rsn = rep['band_region_single_point_reason']
        if (sp is True and rsn not in ('BOX_CORNER', 'OTHER_ROWS')) or (sp is not True and rsn is not None):
            return 'BAND_REGION_SINGLE_POINT_REASON'
        return None

    def p1_ok(self, p):
        if (type(p) is not dict or p.get('schema') != OUT_SCHEMA or p.get('mode') != 'score'
                or p.get('phase') != 'PHASE_1' or 'headline' not in p or type(p.get('e3_line')) is not dict
                or 'patterns_holding' not in p):
            return False
        rows = p.get('rows')
        if type(rows) is not list or len(rows) != 43:
            return False
        return all(type(r) is dict and r.get('id') == QIDS[i] and 'tier_key' in r for i, r in enumerate(rows))

    def agreement(self, main):
        word, rec = self.parse_agree()
        if word is not None:
            return {'outcome': na(['AGREE_RECORD_DEFECT']),
                    'phase1_consequence': 'PHASE_1_KEEPS_PROVISIONAL_LABEL_NEITHER_STANDING_NOR_WITHDRAWN',
                    'agree_record_defect': word, 'phase2_is_score_of_record': True}
        oc = rec['outcome']
        v3 = self.p1_module == PHASE1_V003B
        fails = []
        for f in rec.get('failing', []):
            e = {'member_log_index': f['log_index'], 'row': f['id'], 'excess': f['excess'],
                 'norm_n': f['norm_n'], 'category': f['category'], 'flag': f['flag']}
            if v3:
                for k in ('region_rows_violated', 'region_max_violation', 'geometric_part', 'residual_part',
                          'flag_reason'):
                    e[k] = f[k]
            fails.append(e)
        out = {'outcome': oc, 'non_discriminating_rows': list(rec.get('non_discriminating_rows', [])),
               'failing_member_rows': fails,
               'target_free_always_reported': rec['reported'] if 'reported' in rec else na(['NOT_RUN_UNDER_AGREEMENT_DEFECT']),
               'agree_schema': rec['schema'], 'phase2_is_score_of_record': True,
               'phase1_consequence': {'COVERED': 'STANDING_AS_EARLY_STATEMENT_OF_THE_SCORE_OF_RECORD',
                                      'SUPERSEDED': 'WITHDRAWN',
                                      'AGREEMENT_DEFECT': 'PHASE_2_STANDS_ROOT_INVESTIGATES'}[oc]}
        if rec['schema'] == AT0B and v3:
            out['at0b_members_sha256'] = rec['members_sha256']
            out['at0b_values_sha256'] = rec['values_sha256']
        if oc == 'SUPERSEDED':
            out['withdrawn'] = {'patterns': 'WITHDRAWN_REPLACED_BY_PHASE_2', 'readings': 'WITHDRAWN_REPLACED_BY_PHASE_2',
                                'zone_summaries': 'WITHDRAWN_REPLACED_BY_PHASE_2',
                                'e3_line': 'WITHDRAWN_REPLACED_BY_PHASE_2', 'band_entries': 'WITHDRAWN_NOT_REPLACED'}
        pin = self.bundle['inputs']['phase1_classification']
        pi = self.inp['phase_inputs']
        absent = pi.get('phase1_classification_absent_reason') if type(pi) is dict else None
        if pin is None and absent is not None:
            out['cross_phase'] = na(['NO_PHASE_1_CLASSIFICATION'])
            out['no_phase1_classification_reason'] = absent
        elif self.err['phase1_classification'] is not None or not self.p1_ok(self.inp['phase1_classification']):
            out['cross_phase'] = na(['PHASE1_CLASSIFICATION_INPUT_DEFECT'])
        else:
            p = self.inp['phase1_classification']
            e3 = p['e3_line']
            changed, nacmp = [], []
            for i, q in enumerate(QIDS):
                t1 = p['rows'][i]['tier_key']
                t2 = main['rows'][i]['tier_key']
                if type(t1) is dict or type(t2) is dict:
                    nacmp.append(q)
                elif t1 != t2:
                    changed.append({'id': q, 'phase1': t1, 'phase2': t2})
            out['cross_phase'] = {
                'headlines': {'phase1': p['headline'], 'phase2': main['headline']},
                'e3_lines': {'phase1': e3.get('value') if 'value' in e3 else None, 'phase2': main['e3_line']['value']},
                'pattern_classifications': {'phase1': p['patterns_holding'], 'phase2': main['patterns_holding']},
                'rows_whose_tier_changed': changed, 'rows_tier_comparison_not_available': nacmp}
        return out

    # ------------------------------------------------------------- kernel cross-checks
    def _krow(self, r):
        ZK = K.zone_kernel_v002
        k = r.kind
        if k == 'H':
            return ZK.Row('HIT', r.ratio, False)
        if k in ('MS', 'MN'):
            nr = None if type(r.near) is tuple else r.near
            return ZK.Row('MISS', r.ratio if k == 'MS' else None, nr)
        return ZK.Row('INVALID' if k == 'I' else 'LATE')

    def _xcheck(self, E, rows, twin):
        """Compare B's engine with Codex1's pattern/reading/scope kernels on a fully determined input."""
        if any(not r.fixed for r in rows):
            return
        try:
            zr = [[self._krow(r) for r in E['byz'][z]] for z in ZONES]
            flagged = [self._krow(r) for r in rows if r.qid == Q25] if not twin else []
        except ValueError:
            return  # kernel precondition stricter than the contract (README deviation D-K1)
        res = K.pattern_kernel.patterns(zr[0], zr[1], zr[2], flagged)
        V = E['V']
        for pid in PATTERN_IDS:
            if pid == 'P10' and (twin or self.tsr_stop):
                continue
            if bool(res['patterns'][pid]) != V[pid]:
                raise ConsistencyError('pattern %s: kernel %r, engine %r' % (pid, res['patterns'][pid], V[pid]))
        for zi, z in enumerate(ZONES):
            kz = res['zones'][zi]
            fx = E['zones'][z]['fixed']
            for a, b in (('N_v', 'N_v'), ('H', 'H'), ('M', 'M'), ('U', 'U'), ('I', 'I'),
                         ('miss_dominated', 'miss_dominated'), ('hit_dominated', 'hit_dominated')):
                if kz[a] != fx[b]:
                    raise ConsistencyError('zone %s %s' % (z, a))
            km = 'UNDEFINED' if kz['m'] is None else kz['m']
            if km != E['zones'][z]['m'] or kz['S'] != E['zones'][z]['S']:
                raise ConsistencyError('zone %s m/S' % z)
        if res['outer_failure'] != V['OF'] or res['e3'] != V['E3']:
            raise ConsistencyError('outer failure / E3')
        kd = 'UNDEFINED' if res['delta'] is None else res['delta']
        if kd != V['delta'] or res['growing'] != V['GROWING'] or res['crossing'] != V['CROSSING']:
            raise ConsistencyError('outer trend')
        if list(res['minority_miss']) != [V['MM'][z] for z in ZONES]:
            raise ConsistencyError('minority miss')
        return res

    def _xcheck_readings(self, E, res, readings, s0):
        if res is None:
            return
        V = E['V']
        stage0_word = None
        p2 = s0['part2']
        if p2.get('status') in ('CONSISTENT', 'AGAINST'):
            stage0_word = p2['status']
        elif p2.get('code') == 'NOT_DECIDED':
            stage0_word = 'NOT_DECIDED'
        else:
            stage0_word = p2.get('code', 'NA')
        neg = self.outer_neg_miss(E)
        kr = K.reading_relations.relations(res, neg, stage0_word)
        for ent in readings:
            name = ent['reading']
            if name == 'R-TSR' and self.tsr_stop:
                continue
            p1 = ent['part1']
            if NA in p1:
                if name in ('R-UT1', 'R-REACH') and kr[name]['code'] == 'SIGN_SCOPE_NO_DEFICIT_MISS':
                    continue  # README deviation D-K2 (kernel codes the fallthrough; schema prints NA)
                raise ConsistencyError('reading %s part1 NA on a determined input' % name)
            if (p1['relation'], p1['code']) != (kr[name]['relation'], kr[name]['code']):
                raise ConsistencyError('reading %s part1: kernel %r engine %r' % (name, kr[name], p1))
        zone_rows = [[(r.qid, self._krow(r)) for r in E['byz'][z]] for z in ZONES]
        sc = K.row_scopes.citation_scopes(res, zone_rows, (Q25,) if not self.tsr_stop else ())
        for ent in readings:
            name = ent['reading']
            if name == 'R-TSR' and self.tsr_stop:
                continue
            if set(sc[name]['cited_miss_rows']) != set(ent['cited_miss_rows']):
                raise ConsistencyError('reading %s cited rows' % name)
            mine = set()
            for t in ent['scope_zones']:
                if t == 'ALL':
                    mine |= set(ZONES)
                elif t == 'FLAGGED':
                    mine.add(ZONE_OF[Q25])
                else:
                    mine.add(t)
            if set(sc[name]['scope_zones']) != mine:
                raise ConsistencyError('reading %s scope zones' % name)

    def _xcheck_drift(self, ref_o, tw_o, res):
        try:
            a = [self._krow(r) for r in ref_o]
            b = [self._krow(r) for r in tw_o]
        except ValueError:
            return
        if K.zone_kernel_v002.drift_comparison(a, b) != res:
            raise ConsistencyError('DT-S0G')

    # ------------------------------------------------------------- forms
    def out_base(self):
        return {'schema': OUT_SCHEMA, 'classifier': NAME}

    def run_checks(self):
        self.check_phase()
        self.check_seal()
        self.check_manifest()
        self.check_zone_table()
        self.check_gate_list()
        self.check_tsr()

    def prescore_output(self):
        self.run_checks()
        self.prescore_score()
        self.s0_defect = None
        if self.phase == 'PHASE_2':
            self.prepare_stage0_prescore()
        elif self.phase is None:
            # c2v005 RL5B: prescore and the score run check one list of stop conditions (PREREG L185-L187, L199-L200),
            # so the null-phase rule of score mode (c2v004 RL5, prepare_stage0) applies here too: with the phase
            # inputs refused the STAGE0 status record is read, and a missing (C4-4) or malformed record prints the
            # STAGE0 alternative's stop beside PHASE_MISMATCH.  The prescore result is unchanged; C4-3 is withdrawn.
            self.s0_status, self.s0_facts = self.stage0_status()
            if self.s0_defect is not None and self.s0_defect[0] == 'RECORD':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: STAGE0 status record missing or malformed', alternative=STAGE0)
        load = {r: (self.err[r] or 'READ') for r in ('l1_record', 'agree_record', 'phase1_classification',
                                                    'commitment_status')}
        out = K.terminal_forms.prescore(self.phase, self.manifest_phase, self._stops, load, self.field_map_status)
        out['classifier'] = NAME
        return out

    def prescore_score(self):
        """c2v003 RC7: every 1.1 stop on the score the frozen manifest determines, with score mode's conditions
        and classes (PREREG L185-L199; ROOT_ITEMS L297; README c4v001 L39, L70, L106): the reference member and its
        rows' fields, the ids, the envelope label, the envelope and sensitivity rows, the alternatives' fields and
        the freeze status, on top of the frozen-record checks of run_checks.
        c2v005 RC4: the synthetic score is built as v003g's score_after_freeze builds its output from the same
        manifest (synthesize_score).  When any field that construction reads is missing or of the wrong type, no
        synthetic score exists: FIELD_DEFECT_OUTSIDE_ROWS (class ALL) 'synthetic score could not be built from the
        frozen manifest: <the exception's class name>' (KeyError for a missing key; OUTPUT_CONSTANTS_C4V003 L283,
        L285), and the score is then read as missing, as the seal candidate prints it (ruling 2, triage c2v003 RC4b,
        c2v004 RC4D): 'score output missing or malformed (None)' and no detail that needs the score (c2v004
        DOWNSTREAM_RC4).  A manifest that did not load as an object is read the same way (the construction fails
        at its first read)."""
        try:
            syn = self.synthesize_score()
        except (KeyError, TypeError, ValueError, OverflowError, IndexError, AttributeError, StopIteration) as e:
            self.stop('FIELD_DEFECT_OUTSIDE_ROWS', 'ALL',
                      'synthetic score could not be built from the frozen manifest: %s' % type(e).__name__)
            syn = None
        self.inp['score'] = syn
        self.err['score'] = None
        self.check_score()
        self.check_envelope()
        self.check_sensitivity()
        self.build_rows()
        self.check_alternatives()

    def synthesize_score(self):
        """c2v005 RC4: the prescore synthetic score, built from the frozen manifest exactly as v003g 48a1e48a
        score_after_freeze builds its output (L4190, L4218-L4219, L4225-L4228, L4261-L4299; _score_members
        L4034-L4052 with the row ladder _ladder_row L4011-L4031; _band_rows L4097-L4111; _score_members_on_rows
        L4078-L4089), with the target-free stand-in pair SYN_PAIR, and limited to what the classifier reads: a
        field the scorer reads only to build an output the classifier never reads (a member's role and evaluated,
        admitted_region, input_bindings, band_scope, coordinates, the sensitivity status, label, reference speed and
        max delta, member_evaluation) is not read here (choice C5-1).
        - members from members[] (member_id, log_index, member_valid, and speeds_km_s, row_valid, row_registration
          aligned with query_ids): a row whose frozen registration is not null is INVALID_AS_MISS (status INVALID)
          with registered_reason the frozen reason; otherwise VALID when row_valid is true and its speed is not
          null, else UNEVALUATED_OR_REFUSED (score_status MISS).  row_valid false alone never makes a row
          INVALID_AS_MISS.
        - headline: the reference member is reference_member.member_id, its log_index the scored member's (the
          first with that id, as L4228's next(); none raises StopIteration).
        - envelope rows from pointwise_envelope[] {band_low_km_s, band_high_km_s, valid, label}, sensitivity rows
          from sensitivity.per_query[] {box_limited_band_low_km_s, box_limited_band_high_km_s, valid}, in
          either phase (the producer writes the sensitivity block in both).  The row ids are the manifest's
          query_ids, as the producer writes them.  The envelope label is the label the frozen rows carry (the first
          row's; the producer writes one label on every row, L2072-L2086); no fixed label is supplied.
        - alternatives from alternatives = {primary, declared[]} in the score form (RC3): role PRIMARY or
          NON_PRIMARY; STAGE0_GRID_OUTER carries its declared entry's scoring_scope; an evaluated non-PRIMARY entry
          is scored with members from alternative_results[name].members (STAGE0 on its scope rows); then, when the
          manifest carries headline_conditions (the fixed-distance mode), its recorded alternatives, NON_PRIMARY
          and unscored.
        - freeze_status, and list(incomplete_reasons).
        No other encoding is accepted: an alternatives list or name-keyed object, lo_km_s / hi_km_s or query_id
        row keys, a default for a missing member_valid or row valid, or a fixed envelope label.  Raises KeyError,
        TypeError, IndexError, ValueError, OverflowError (a frozen speed beyond float range, V-F3) or StopIteration
        as the producer's own reads and arithmetic raise them."""
        m = self.inp['freeze_manifest']
        ids = list(m['query_ids'])
        freeze_status = m['freeze_status']
        incomplete = list(m['incomplete_reasons'])
        members = _syn_members(m['members'], ids)
        ref_id = m['reference_member']['member_id']
        ref = next(x for x in members if x['member_id'] == ref_id)
        headline = {'reference_member_id': ref_id, 'reference_member_log_index': ref['log_index']}
        primary = m['alternatives']['primary']
        erows = _syn_band_rows(m['pointwise_envelope'], 'band_low_km_s', 'band_high_km_s', ids, True)
        sens = m['sensitivity']
        srows = _syn_band_rows(sens['per_query'], 'box_limited_band_low_km_s', 'box_limited_band_high_km_s', ids,
                               False)
        alts = []
        for a in m['alternatives']['declared']:
            rec = {'name': a['name'], 'kind': a['kind'], 'status': a['status'],
                   'role': 'PRIMARY' if a['name'] == primary else ROLE_NON_PRIMARY}
            scope = a['scoring_scope'] if a['name'] == STAGE0 else None
            if scope is not None:
                rec['scoring_scope'] = scope
            if rec['role'] == 'PRIMARY':
                rec.update({'scored': True, 'headline': True})
            elif a['status'] == EBF:
                am = m['alternative_results'][a['name']]['members']
                rec.update({'scored': True, 'headline': False,
                            'members': (_syn_members_on_rows(am, ids, scope['query_ids']) if scope is not None
                                        else _syn_members(am, ids))})
            else:
                rec.update({'scored': False, 'headline': False, 'note': NOT_EVAL_NOTE})
            alts.append(rec)
        if HEADLINE_CONDITIONS_KEY in m:
            for a in m[HEADLINE_CONDITIONS_KEY]['recorded_alternatives']:
                alts.append({'name': a['name'], 'kind': a['kind'], 'status': a['status'], 'role': ROLE_NON_PRIMARY,
                             'scored': False, 'headline': False, 'note': NOT_EVAL_NOTE + ' (A13)'})
        return {'headline': headline, 'members': members, 'freeze_status': freeze_status,
                'incomplete_reasons': incomplete,
                'pointwise_envelope': {'label': erows[0]['label'] if erows else None, 'rows': erows},
                'sensitivity': {'rows': srows}, 'alternatives': alts}

    def prepare_stage0_prescore(self):
        self.s0_status, self.s0_facts = self.stage0_status()
        if self.s0_defect is not None:
            kind, word = self.s0_defect
            if kind == 'BLOCK':
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: the frozen stage0_status block of the STAGE0 successor is not '
                          'bound or malformed (%s)' % word, alternative=STAGE0)
            else:
                self.stop('FIELD_DEFECT_ALTERNATIVE', 'ALT',
                          'STAGE0_GRID_OUTER: STAGE0 status record missing or malformed', alternative=STAGE0)

    def score_output(self):
        self.run_checks()
        self.check_score()
        self.check_envelope()
        self.check_sensitivity()
        self.build_rows()
        self.check_alternatives()
        self.s0_defect = None
        self.prepare_stage0()
        self.prepare_alternatives()
        if self.phase == 'PHASE_1' and self.ref_rows is not None:
            self.band_column()
        elif self.phase == 'PHASE_1':
            self.band = {}
            self.p1_module = None
        else:
            self.p1_module = self.tool_module()
        labels = self.labels()
        stops = self.stops_out()
        codes_all = sorted({s['code'] for s in stops})
        out = self.out_base()
        out.update({'mode': 'score', 'phase': self.phase, 'stops': stops, 'labels': labels,
                    'header': self.header(), 'exploratory_readings': [], 'fallback': self.fallback_out(),
                    'headline': self.headline_out()})
        if any(s['class'] == 'ALL' for s in stops) or self.rows is None:
            if not any(s['class'] == 'ALL' for s in stops):
                raise ConsistencyError('rows not built without an ALL-class stop')
            blank = na(self.codes('ALL'))
            out['status'] = 'NOT_READ'
            out['status_code'] = codes_all
            out['rows'] = [{'id': q, 'zone': ZONE_OF[q], 'tier_key': blank} for q in QIDS]
            for k in ('zones', 'outer_trend', 'outer_failure', 'e3_line', 'patterns', 'patterns_holding',
                      'minority_miss', 'flagged_rows', 'readings', 'descriptive', 'invalid_list', 'a15',
                      'p8_report', 'alternatives', 'stage0'):
                out[k] = blank
            if self.phase == 'PHASE_2':
                out['agreement'] = blank
            return out
        out['status'] = 'NOT_READ' if stops else 'CLASSIFIED'
        out['status_code'] = codes_all if stops else None
        rows = self.rows
        E = self.engine(rows)
        V = E['V']
        cd = na(self.codes_d())
        out['rows'] = [self.row_out(r) for r in rows]
        zones = {z: self.zone_out(E, z, labels) for z in ZONES}
        out['zones'] = zones
        out['outer_trend'] = {'delta_out': self.val(V['delta']), 'far_half_median': self.val(V['far']),
                              'GROWING': self.val(V['GROWING']), 'CROSSING': self.val(V['CROSSING'])}
        out['outer_failure'] = self.val(V['OF'])
        zo = zones['OUTER']
        odef = E['zones']['OUTER']['has_def']
        fo = E['zones']['OUTER']['fixed']
        out['e3_line'] = {'value': self.val(V['E3']), 'S_OUTER': zo['S'], 'delta_out': self.val(V['delta']),
                          'N_v': zo['N_v'], 'H': zo['H'], 'M': zo['M'], 'U': zo['U'], 'N': zo['N'],
                          'I_per_reason': zo['I_per_reason'], 'labels': labels,
                          'n_defined_ratio': cd if odef else sum(1 for r in E['byz']['OUTER'] if r.kind in ('H', 'MS')),
                          'n_late_gate': cd if odef else sum(1 for r in E['byz']['OUTER'] if r.kind == 'L'),
                          'n_null_ratio': cd if odef else sum(1 for r in E['byz']['OUTER'] if r.kind == 'MN')}
        pats = self.patterns_out(E, labels, zones)
        out['patterns'] = pats
        out['patterns_holding'] = [pid for pid in PATTERN_IDS if pats[pid] is True]
        out['minority_miss'] = {z: self.val(V['MM'][z]) for z in ZONES}
        q25 = self.row_by_id[Q25]
        out['flagged_rows'] = (na(['TSR_FLAG_TABLE_MISMATCH']) if self.tsr_stop else
                               [{'id': Q25, 'tier': self.tier_of(q25.kind) if q25.fixed else cd}])
        stage0_obj, drift2 = self.stage0_block(labels, odef)
        s0 = {'part2': drift2}
        readings = self.readings(E, labels, s0)
        res = self._xcheck(E, rows, False)
        self._xcheck_readings(E, res, readings, s0)
        out['readings'] = readings
        onset = V['onset']
        out['descriptive'] = {'onset_radius': cd if onset is None else onset,
                              'onset_comparison': 'k* (A12: wavelengths of tens of kpc), comparison only',
                              'DT_T1a_trend': 'NOT_COMPUTED'}
        out['invalid_list'] = self.invalid_list(rows)
        out['a15'] = self.a15(E, zones, out['rows'])
        out['stage0'] = stage0_obj
        out['alternatives'] = self.alternatives_out(labels, stage0_obj)
        out['p8_report'] = self.p8_report(pats)
        if self.phase == 'PHASE_2':
            out['agreement'] = self.agreement(out)
        return out

    def invalid_list(self, rows):
        per = {}
        for r in rows:
            if r.fixed and r.kind in ('I', 'L'):
                per.setdefault(r.reason, []).append({'id': r.qid, 'zone': r.zone, 'gate_status': r.gate_status,
                                                     'GATE_AFTER_PREDICTIONS': r.kind == 'L'})
        bad = sorted(r.qid for r in rows if not r.fixed)
        out = {'per_reason': per, 'rows_not_available': bad}
        if bad:
            out['rows_not_available_codes'] = self.codes_d()
        if 'QUERY_BEYOND_OUTER_GAS_CUT' in per:
            rd = self.inp['root_disclosures']
            v = rd.get('outer_gas_cut_report') if type(rd) is dict else None
            out['outer_gas_cut_report'] = v if v is not None else na(['CUT_REPORT_NOT_SUPPLIED'])
        return out

    def a15(self, E, zones, rows_out):
        V = E['V']
        zi = zones['INNER']
        sub = []
        for ro in rows_out:
            if ro['id'] in E1_SUBTABLE:
                sub.append({'id': ro['id'], 'tier': ro['tier'], 'near': ro['near']})
        e2 = {'label': 'COMPARISON with A15 E2', 'OUTER_FAILURE': self.val(V['OF']), 'S_OUTER': zones['OUTER']['S'],
              'OUTER_NO_MISS': self.val(V['ONM']), 'P9': self.val(V['P9']),
              'OUTER_I_per_reason': zones['OUTER']['I_per_reason'],
              # c2v002 RC15: not a count-level output (PREREG L205) and no L206 deduction fixes it, so it reads
              # NOT_AVAILABLE with the ROW/GATE codes when a row of D is in OUTER, as the E3 line's count does.
              'OUTER_LATE_gate_count': (na(self.codes_d()) if E['zones']['OUTER']['has_def']
                                        else self.val(V['OL']))}
        if V['ONM'] is True:
            e2['note'] = 'OUTER_NO_MISS runs against the A15 E2 expectation'
        return {'E1': {'label': 'COMPARISON with A15 E1',
                       'a': {'H': zi['H'], 'M': zi['M'], 'N': zi['N'], 'Q03_Q15': sub, 'near_label': NEAR_LABEL},
                       'b': na(['NO_PRE_FREEZE_BARYONIC_NEWTONIAN_CARRIER_M11'])},
                'E2': e2, 'E3': 'see e3_line'}

    def p8_report(self, pats):
        if pats['P8'] is not True:
            return None
        c3 = self.inp['c3_record']
        c3o = na(['C3_RECORD_NOT_AVAILABLE_M13'])
        try:
            t = c3['per_grid']['T120L']
            if is_num(t['C3_max_e']) and type(t['C3_PASS']) is bool:
                c3o = {'C3_max_e': t['C3_max_e'], 'C3_PASS': t['C3_PASS'],
                       'disclosures': ['A27: formally provisional until aggregate_v003 is reviewed',
                                       'the same record reads C1_effective_PASS false on 12 TRUNCATION_SHAPE rings (D-3)']}
        except (TypeError, KeyError):
            pass
        if self.phase == 'PHASE_1':
            ok = na(['ORIGINAL_K_NOT_AVAILABLE_IN_PHASE_1'])
        elif self.ok_twin is None:
            ok = na(['ORIGINAL_K_TWIN_NOT_CLASSIFIED'])
        else:
            ok = {'OUTER': self.ok_twin['zones']['OUTER'], 'outer_failure': self.ok_twin['outer_failure'],
                  'patterns_holding': self.ok_twin['patterns_holding']}
        return {'ORIGINAL_K_twin_OUTER': ok, 'T120L_C3_record': c3o, 'note': 'changes neither the headline nor any status'}

    def run(self):
        self.load_bundle()
        self.load_inputs()
        self.pi_verdict = self.phase_inputs_check()
        pi = self.inp['phase_inputs']
        if self.pi_verdict == 'OK' and pi['run_status'] != 'SCORED':
            out = K.terminal_forms.no_classification(self.bundle['mode'], pi['phase_named'], pi['run_status'],
                                                     pi['run_status_code'])
            out['classifier'] = NAME
            return out
        if self.bundle['mode'] == 'prescore':
            return self.prescore_output()
        return self.score_output()


MEMBER_EPS_REASONS = ('MEMBER_EPS_LIST_MISSING', 'MEMBER_EPS_NONE', 'MEMBER_EPS_BOOL',
                      'MEMBER_EPS_NOT_A_NUMBER', 'MEMBER_EPS_NON_FINITE', 'MEMBER_EPS_NEGATIVE')


# ---------------------------------------------------------------------------
# c2v005 RC4: the prescore synthetic score, ported from v003g 48a1e48a (target-free; SYN_PAIR stands in for the
# target pair).  Each read and each operation is the producer's, so a frozen field that is missing or of the wrong
# type raises where the producer raises.
# ---------------------------------------------------------------------------
def _syn_ladder(q, predicted, row_valid):
    """v003g _ladder_row L4011-L4031, the fields the classifier reads (the fractional error, L4021-L4026, is not
    read and is skipped: with the stand-in observed 0.0 the producer skips it too)."""
    observed, sigma = SYN_PAIR
    sigma_ratio = None
    if predicted is not None:
        residual = predicted - observed
        r = residual / sigma
        if math.isfinite(r):
            sigma_ratio = r
    valid = bool(row_valid and predicted is not None)
    within = bool(valid and sigma_ratio is not None and abs(sigma_ratio) <= 1.0)
    return {'id': q, 'sigma_ratio': sigma_ratio, 'valid': valid, 'within_error': within}


def _syn_members(members, ids):
    """v003g _score_members L4034-L4052: the rows of each member; L4040-L4046 the registration rule."""
    out = []
    for x in members:
        rows = []
        for j, q in enumerate(ids):
            row = _syn_ladder(q, x['speeds_km_s'][j], x['row_valid'][j])
            reg = x['row_registration'][j]
            if reg is not None:
                row.update(status='INVALID', registered_reason=reg['reason'], score_status='INVALID_AS_MISS')
            else:
                row.update(status='VALID' if row['valid'] else 'UNEVALUATED_OR_REFUSED', registered_reason=None,
                           score_status='HIT' if row['within_error'] else 'MISS')
            rows.append(row)
        out.append({'member_id': x['member_id'], 'log_index': x['log_index'], 'member_valid': x['member_valid'],
                    'rows': rows})
    return out


def _syn_members_on_rows(members, ids, selected_ids):
    """v003g _score_members_on_rows L4078-L4089: an evaluated STAGE0 alternative is scored on its scope rows only."""
    if (not isinstance(selected_ids, list) or not selected_ids or len(set(selected_ids)) != len(selected_ids)
            or any(q not in ids for q in selected_ids)):
        raise ValueError('ALTERNATIVE_SCORE_ROW_SET_REQUIRED')
    indexes = [ids.index(q) for q in selected_ids]
    subset = []
    for member in members:
        narrowed = dict(member)
        for key in ('speeds_km_s', 'row_valid', 'row_registration'):
            narrowed[key] = [member[key][j] for j in indexes]
        subset.append(narrowed)
    return _syn_members(subset, selected_ids)


def _syn_band_rows(rows_in, low_key, high_key, ids, with_label):
    """v003g _band_rows L4097-L4111, the fields the classifier reads (id, valid, band_overlaps_error_bar) and, for
    the envelope (with_label), the frozen row's label, from which the envelope label is read."""
    observed, sigma = SYN_PAIR
    rows = []
    for j, q in enumerate(ids):
        r = rows_in[j]
        lo, hi, valid = r[low_key], r[high_key], r['valid']
        overlaps = bool(valid and lo is not None and hi is not None and lo <= observed + sigma
                        and hi >= observed - sigma)
        row = {'id': q, 'valid': bool(valid), 'band_overlaps_error_bar': overlaps}
        if with_label:
            row['label'] = r['label']
        rows.append(row)
    return rows


def _l1_rows(l1):
    """c2v005 RC7: the L1 band rows under 'rows' (the band command's key, phase1_c2v003b L946, phase1_c2v002 L842),
    43 of them; PB-7's alternative key band_rows is withdrawn."""
    v = l1.get('rows')
    return v if type(v) is list and len(v) == 43 else None


def _overlap_ok(r):
    """c2v002 RC13: band_overlaps_error_bar is a boolean on every envelope and sensitivity row, valid or invalid
    (ROOT_ITEMS M-5 L145-L146, CSM F14; PREREG L172, L190).  No text allows null there (compare PREREG L183,
    L184, where a null or absent field is allowed explicitly).  Retires c2v001's PB-16."""
    return 'band_overlaps_error_bar' in r and type(r['band_overlaps_error_bar']) is bool


def _module_str_set(raw, name):
    """c2v003 RC4: the frozenset of strings that a module's top-level `name = <expr>` denotes, read from its source
    without executing it.  <expr> may be a tuple/list/set of string literals (with *starred parts), the keys of a
    dict literal, a top-level name, frozenset/set/tuple/list/sorted of one such argument, '<string>'.split(), or + or
    | of two such values.  -> None for anything else, an empty set, or a non-string element."""
    try:
        tree = ast.parse(raw.decode('utf-8'))
    except (SyntaxError, ValueError, UnicodeDecodeError, RecursionError, MemoryError):
        return None
    env = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    env[t.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            env[node.target.id] = node.value

    def ev(node, depth):
        if node is None or depth > 16:
            return None
        if isinstance(node, ast.Constant):
            return node.value if type(node.value) is str else None
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            out = []
            for e in node.elts:
                v = ev(e.value if isinstance(e, ast.Starred) else e, depth + 1)
                if isinstance(e, ast.Starred) and isinstance(v, list):
                    out.extend(v)
                elif not isinstance(e, ast.Starred) and isinstance(v, str):
                    out.append(v)
                else:
                    return None
            return out
        if isinstance(node, ast.Dict):
            keys = [ev(k, depth + 1) if k is not None else None for k in node.keys]
            return keys if all(isinstance(k, str) for k in keys) else None
        if isinstance(node, ast.Name):
            return ev(env.get(node.id), depth + 1)
        if isinstance(node, ast.Call) and not node.keywords:
            f = node.func
            if isinstance(f, ast.Name) and f.id in ('frozenset', 'set', 'tuple', 'list', 'sorted') and len(node.args) == 1:
                v = ev(node.args[0], depth + 1)
                return v if isinstance(v, list) else None
            if isinstance(f, ast.Attribute) and f.attr == 'split' and not node.args:
                v = ev(f.value, depth + 1)
                return v.split() if isinstance(v, str) else None
            return None
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.BitOr)):
            a, b = ev(node.left, depth + 1), ev(node.right, depth + 1)
            if isinstance(a, list) and isinstance(b, list):
                return a + b
            if isinstance(a, str) and isinstance(b, str) and isinstance(node.op, ast.Add):
                return a + b
        return None
    v = ev(env.get(name), 0)
    if not isinstance(v, list) or not v or any(type(x) is not str or not x for x in v):
        return None
    return frozenset(v)


def _check_pin_tables():
    """c2v003 RC3: a full sha written into PHASE1_TOOL_SHA256 / STAGE0_SUCCESSOR_SHA256 must be 64 lower-case hex and
    name a known module; otherwise the run refuses (INTERNAL_ERROR, never a classification)."""
    if type(PHASE1_TOOL_SHA256) is not dict or any(not is_hex64(k) or v not in PHASE1_MODULES
                                                  for k, v in PHASE1_TOOL_SHA256.items()):
        raise ConsistencyError('PHASE1_TOOL_SHA256 table')
    if STAGE0_SUCCESSOR_SHA256 is not None and not is_hex64(STAGE0_SUCCESSOR_SHA256):
        raise ConsistencyError('STAGE0_SUCCESSOR_SHA256')


def classify_bundle(bundle_path):
    try:
        load_kernels()
        _check_pin_tables()
        run = Run(bundle_path)
        try:
            out = run.run()
        except BundleRefused as e:
            out = {'schema': OUT_SCHEMA, 'classifier': NAME, 'refused': True, 'reason': str(e)}
        return K.input_primitives.canonical_json(out)
    except Exception as e:  # fail closed: never a classification
        out = {'schema': OUT_SCHEMA, 'classifier': NAME, 'refused': True,
               'reason': 'INTERNAL_ERROR: %s: %s' % (type(e).__name__, str(e)[:300])}
        return (json.dumps(out, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')


def main(argv):
    if len(argv) != 3:
        sys.stderr.write('usage: classifier_b_c2v005.py BUNDLE.json OUT.json\n')
        return 2
    data = classify_bundle(argv[1])
    with open(argv[2], 'xb') as f:
        f.write(data)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
