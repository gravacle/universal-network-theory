"""build_records_c4v001.py -- Claude4 helper, seal_records_c4/build (dispatch 0598 da395935, root A87).

Builds FIELDS_R11-shape V007 gate records (schema UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002) from EXISTING outputs only:
  B3 (independent lane Claude4, saved C4R3), and on driver v010 r5 (b5cc62af): B0, B0prime_DRY and B0_FA.
No launch, no driver / route / dry run, no recomputation of any numeric result.  Every input file is read from bytes and its
sha256 checked (task-pinned inputs against the task value, the rest recorded from bytes).  Every record value is a copy of a
pinned value or a deterministic derivation named in the record's provenance: the max over copied values; a filter over copied
exit codes, verdicts and report-file sizes read by stat; an implication from a copied exact-zero indicator.
B0_N3, B0_RO1 and I4 are NOT built: no output on the sealed driver exists for them; MISSING_RUNS names the run each needs.
The audit fence fence_c4v001.py (f813c430; write root = build/) is installed before any input is read.
Records: canonical JSON (sort_keys, indent 1, trailing newline, allow_nan False), re-parsed strictly, exclusive create.
Usage: python3 -I -B build_records_c4v001.py dry|write RECDIR AUXDIR
  dry: build and validate everything, print the summary and the would-be record shas, write nothing.
  write: RECDIR and AUXDIR inside build/; files are created with open(path, 'x'); an existing file refuses.
  env TS (date -u) is written into the build manifest only (never into a gate record)."""
import hashlib
import importlib.util
import json
import math
import os
import re
import stat as stat_mod
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
FENCE = HERE / 'fence_c4v001.py'
FENCE_SHA = 'f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0'


def _sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


with open(FENCE, 'rb') as _f:
    if _sha_bytes(_f.read()) != FENCE_SHA:
        raise SystemExit('REFUSED: fence sha')
_spec = importlib.util.spec_from_file_location('fence_c4v001', str(FENCE))
FEN = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FEN)                                    # installs the audit hook (cannot be removed)
if os.path.realpath(FEN.REVIEW) != os.path.realpath(str(BUILD)):
    raise SystemExit('REFUSED: fence write root is not build/')

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
FCR = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
EXC = '/Users/bgm/Research/UNT_EXCHANGE'
SCHEMA = 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'
TSI = ART + '/tail_scheme_impl_c2'
B3D = ART + '/gate_b3_c4'
DRY5 = TSI + '/driver_r5/out/B0_R5_RUN_V001/dry'
DRY4 = TSI + '/driver_r4/out/B0_RUN_V001/dry'

# role -> (path, expected sha256 or prefix or None).  None: recorded from bytes (not task-pinned).
PINS = {
    'DISPATCH_0598': (EXC + '/FROM_CODEX/0598_2026-10-18_claude4_B3_json_and_B0_family_records.md',
                      'da395935443317525ed72a42ae0cd7880897dc04fbec84e11a0429169dd33466'),
    'COMPARE_R11': (ART + '/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py',
                    'a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a'),
    'FIELDS_R11': (ART + '/v007_compare_c2/r11/FIELDS_R11.md',
                   'c7f0dec6ff1ae45dc242c69686e88ad73089a39e1b582e73650e6e18a7368cc5'),
    'B3_COMPARE': (B3D + '/out/B3_COMPARE_V001.json', '773e4ae91f2a77782590264bb7b3a34c7c37d587fbf4ffb4b9a27cfcb2c7c5ae'),
    'B3_REPORT_V002': (B3D + '/GATE_B3_C4_V002.md', '465cb3c3b105c8bea994259bcf347e86910e8a9ebbc502ba83ff617fa83ceacf'),
    'B3_REPORT_V001': (B3D + '/GATE_B3_C4_V001.md', 'a336838a'),
    'B3_TAP_REF_BODY': (B3D + '/out/B3_TAP_COMPARE_REF_BODY_V001.json', None),
    'B3_TAP_FSC': (B3D + '/out/B3_TAP_COMPARE_FSC_V001.json', None),
    'B3_IND_CUBE': (B3D + '/out/B3_IND_CUBE_V001.json', None),
    'B3_IND_CYL': (B3D + '/out/B3_IND_CYL_V001.json', None),
    'B3_IND_CUBE_DOUBLE': (B3D + '/out/B3_IND_CUBE_DOUBLE_V001.json', None),
    'B3_IND_CYL_DOUBLE': (B3D + '/out/B3_IND_CYL_DOUBLE_V001.json', None),
    'B3_TOOL_COMPARE': (B3D + '/tools/b3_compare_v001.py', None),
    'B3_TOOL_INDEPENDENT': (B3D + '/tools/b3_independent_v001.py', None),
    'B3_TOOL_POINTS': (B3D + '/tools/b3_points_v001.py', None),
    'B3_TOOL_TAP': (B3D + '/tools/b3_tap_compare_v001.py', None),
    'B3_FORWARD': (FCR + '/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py', None),
    'UV_TAIL_MODULE_V001': (TSI + '/module/owned_uv_tail_lapse_v001.py', None),
    'B0_R5': (TSI + '/driver_r5/out/B0_R5_RUN_V001/B0_R5_VS_R4_C2V001.json',
              'e10e6a584ab49083f24bf4fbb7d94a32ccb667c1c1c7e0e3ff3943ca1061f929'),
    'B0_R5_TOOL': (TSI + '/driver_r5/gates/b0_r5_vs_r4_c2v001.py', None),
    'R5_DRIVER': (TSI + '/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'),
    'R5_BUILD': (TSI + '/driver_r5/BUILD.md', '0c188312'),
    'R5_CASCADE_MAP': (TSI + '/driver_r5/CASCADE_MAP_R5_C2V001.json', None),
    'R5_P128_REGISTRY': (TSI + '/driver_r5/specs/SPECS_P128_R5_C2V001.json', None),
    'R5_DRYRUN_P128': (TSI + '/driver_r5/out/DRYRUN_P128_R5_RUN_V001/DRYRUN_P128_R5_C2V001.json', None),
    'R4_DRIVER': (TSI + '/driver_r4/galaxy_m0_forward_c2v010.py', None),
    'R4_B0_RECORD': (TSI + '/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0.json', None),
    'R4_B0prime_DRY_RECORD': (TSI + '/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0prime_DRY.json', None),
    'R4_B0_FA_RECORD': (TSI + '/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0_FA.json', None),
    'R4_B0_N3_RECORD': (TSI + '/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0_N3.json', None),
    'R4_RECORD_WRITER': (TSI + '/driver_r4/gates/write_gate_records_v007_c2v003.py', None),
    'R4_B0_EVIDENCE': (TSI + '/driver_r4/out/B0_RUN_V001/B0_PLAN_IDENTITY_C2V001.json', None),
    'R4_B0_TOOL': (TSI + '/driver_r4/gates/b0_plan_identity_c2v002.py', None),
    'V009_EXT_DRIVER': (ART + '/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py', None),
    'V009_GEO_DRIVER': (ART + '/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py', None),
    'CHECK_V001': (TSI + '/check/CHECK_V001.md', None),
    'TOKENS_I4': (TSI + '/driver/launch_v002/TOKENS_I4_SERIAL_PARALLEL.json', None),
    'RO1_TEST_C6_REPLAY': (ART + '/ro1_readout_c2/out/TEST_C6_REPLAY_C2V003.json', None),
    'RO1_TEST_SYN': (ART + '/ro1_readout_c2/out/TEST_SYN_RO1_C2V001.json', None),
    'RO1_TEST_DRIVER_PATCH': (ART + '/ro1_readout_c2/out/TEST_DRIVER_PATCH_C2V002.json', None),
    'R6_B0': (TSI + '/driver_r6/out/B0_R6_RUN_V001/B0_R6_VS_R5_C2V001.json', None),
}
EARLIER_RECORD_DIRS = ('driver/out/GATE_RECORDS_V001', 'driver/out/GATE_RECORDS_V002_SCHEMA_C2V002',
                       'driver/out/GATE_RECORDS_V003_SCHEMA_C2V001', 'driver/out/GATE_RECORDS_V004_SCHEMA_C2V001',
                       'driver/out/GATE_RECORDS_V005_SCHEMA_C2V002', 'driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V001',
                       'driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002')
EARLIER_RECORD_GATES = ('B0', 'B0prime_DRY', 'B0_FA', 'B0_N3')

# FIELDS_R11 'B3 (pass verdict PASS)' table (also the compare's B3_TOL)
B3_TOL = (('value_rel', '<=', 1e-8), ('gradient_rel', '<=', 1e-7), ('hessian_rel', '<=', 1e-6), ('lapse_pair_rel', '<=', 1e-8),
          ('bd_z0_max_abs', '==', 0.0), ('facade_midplane_ratio_max_abs', '==', 0.0), ('angular_reads_rel', '<=', 1e-7),
          ('column_potential_rel', '<=', 1e-7), ('imag_max_abs', '==', 0.0), ('doubling_rel', '<=', 1e-10))


class Refuse(Exception):
    pass


def req(cond, what):
    if not cond:
        raise Refuse(what)


def _hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Refuse('DUPLICATE_JSON_KEY')
        out[k] = v
    return out


def _const(x):
    raise Refuse('NON_FINITE_JSON_CONSTANT:%s' % x)


def loads_strict(b):
    return json.loads(b, object_pairs_hook=_hook, parse_constant=_const)


class Inputs:
    """Each pinned file read once; its sha from those bytes; task pins verified (full value or stated prefix)."""

    def __init__(self):
        self.b, self.s, self.used = {}, {}, []

    def _load(self, role):
        if role not in self.b:
            path, want = PINS[role]
            with open(path, 'rb') as f:
                b = f.read()
            s = _sha_bytes(b)
            if want is not None:
                req(s == want if len(want) == 64 else s.startswith(want), 'PIN_MISMATCH:%s' % role)
            self.b[role], self.s[role] = b, s
        return self.b[role]

    def sha(self, role):
        self._load(role)
        return self.s[role]

    def path(self, role):
        return PINS[role][0]

    def json(self, role):
        return loads_strict(self._load(role))

    def text(self, role):
        return self._load(role).decode('utf-8')

    def pin(self, role):
        return {'path': self.path(role), 'sha256': self.sha(role)}

    def source(self, role, use):
        e = {'role': role, 'path': self.path(role), 'sha256': self.sha(role), 'use': use}
        if PINS[role][1] is not None:
            e['task_pinned'] = PINS[role][1]
        return e


def builder_pin():
    with open(__file__, 'rb') as f:
        return {'path': str(Path(__file__).resolve()), 'sha256': _sha_bytes(f.read())}


def num_ok(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0


# ============================================================================================ B3
def check_value(I, role, d, name, limit, exact):
    x = d['checks'][name]
    req(x.get('verdict') == 'PASS', 'B3_CHECK_NOT_PASS:%s' % name)
    req(float(x.get('limit')) == limit, 'B3_CHECK_LIMIT_NOT_THE_FIELDS_TOLERANCE:%s' % name)
    if exact is not None:
        req(x.get('exact') is exact, 'B3_CHECK_EXACT_FLAG:%s' % name)
    v = x['value']
    req(num_ok(v), 'B3_CHECK_VALUE_NOT_FINITE_NONNEG:%s' % name)
    return v, {'file_role': role, 'file_sha256': I.sha(role), 'check': name, 'value': v, 'limit': x['limit'], 'verdict': x['verdict']}


def import_names(src):
    import ast
    mods = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            mods |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add(n.module)
    return sorted(m for m in mods if m)


def c4r3_pin_from_compare(I):
    m = re.findall(r"'C4R3': \(CTRL \+ '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result\.json', '([0-9a-f]{64})'\)", I.text('COMPARE_R11'))
    req(len(m) == 1, 'COMPARE_PIN_R3_C4R3_NOT_FOUND_ONCE')
    return m[0]


def build_b3(I):
    c, rb, fsc = I.json('B3_COMPARE'), I.json('B3_TAP_REF_BODY'), I.json('B3_TAP_FSC')
    req(c.get('schema') == 'CLAUDE4_GATE_B3_COMPARE_V001', 'B3_COMPARE_SCHEMA')
    req(rb.get('schema') == 'CLAUDE4_B3_TAP_COMPARE_V001' and fsc.get('schema') == 'CLAUDE4_B3_TAP_COMPARE_V001', 'B3_TAP_SCHEMA')
    req(c['n_fail'] == 0 and c['n_pass'] == len(c['checks']) == 32, 'B3_COMPARE_COUNTS')
    req(rb['n_fail'] == 0 and rb['n_pass'] == len(rb['checks']) == 21, 'B3_TAP_REF_BODY_COUNTS')
    req(fsc['n_fail'] == 0 and fsc['n_pass'] == len(fsc['checks']) == 28, 'B3_TAP_FSC_COUNTS')
    req(sorted(rb['which']) == ['BODY', 'REF'] and fsc['which'] == ['FSC'], 'B3_TAP_WHICH')
    state = c['state']['result_sha256']
    c4r3 = c4r3_pin_from_compare(I)
    req(state == c4r3, 'B3_STATE_NOT_THE_COMPARE_PIN_R3_C4R3')
    ind_sha, pts_sha, tap_sha = I.sha('B3_TOOL_INDEPENDENT'), I.sha('B3_TOOL_POINTS'), I.sha('B3_TOOL_TAP')
    per_case_inputs = []
    for role in ('B3_IND_CUBE', 'B3_IND_CYL', 'B3_IND_CUBE_DOUBLE', 'B3_IND_CYL_DOUBLE'):
        m = I.json(role)
        req(m['result_sha256'] == state, 'B3_IND_STATE:%s' % role)
        req(m['script_sha256'] == ind_sha, 'B3_IND_SCRIPT_NOT_THE_INDEPENDENT_TOOL:%s' % role)
        per_case_inputs.append({'role': role, 'sha256': I.sha(role), 'case': m['case'], 'result_sha256': m['result_sha256'],
                                'script_sha256': m['script_sha256'], 'quad': m['quad'], 'imag_max_rel': m['imag_max_rel']})
    for t, role in ((rb, 'B3_TAP_REF_BODY'), (fsc, 'B3_TAP_FSC')):
        req(t['script_sha256'] == tap_sha, 'B3_TAP_SCRIPT:%s' % role)
        req(t['independent_sha256'] == {'b3_independent_v001.py': ind_sha, 'b3_points_v001.py': pts_sha}, 'B3_TAP_INDEPENDENT_SHAS:%s' % role)
    # independence: the compare's own scan of b3_independent_v001.py, plus the static imports of b3_points_v001.py and FORWARD
    ind = c['independence']
    req(ind['banned'] == [] and ind['pass_'] is True, 'B3_INDEPENDENCE_SCAN')
    req(ind['static_imports'] == import_names(I.text('B3_TOOL_INDEPENDENT')), 'B3_INDEPENDENCE_STATIC_IMPORTS_NOT_THE_TOOL_BYTES')
    req(len(ind['dynamic_import_lines']) == 1 and 'str(FORWARD)' in ind['dynamic_import_lines'][0], 'B3_DYNAMIC_IMPORT')
    fwd = re.findall(r"FORWARD = ROOT / '([^']+)'; FORWARD_SHA = '([0-9a-f]{64})'", I.text('B3_TOOL_INDEPENDENT'))
    req(len(fwd) == 1 and FCR + '/' + fwd[0][0] == I.path('B3_FORWARD') and fwd[0][1] == I.sha('B3_FORWARD'), 'B3_FORWARD_PIN')
    pts_imports, fwd_imports = import_names(I.text('B3_TOOL_POINTS')), import_names(I.text('B3_FORWARD'))
    banned_words = ('uv_tail', 'owned_uv', 'bessel', 'posix_libm', 'roster')
    req(not [m for m in pts_imports + fwd_imports if any(w in m for w in banned_words)], 'B3_POINTS_OR_FORWARD_IMPORTS_TAIL_LIBRARY')
    v_ind, p_ind = check_value(I, 'B3_COMPARE', c, 'INDEPENDENCE_no_tail_library_import', 0.0, True)
    req(v_ind == 0.0, 'B3_INDEPENDENCE_CHECK')
    hi, p_hi = check_value(I, 'B3_COMPARE', c, 'HI_v003_L67_68_condition_text', 0.0, True)
    mod_pin = re.findall(r"'owned_uv_tail_lapse_v001\.py': '([0-9a-f]{64})'", I.text('B3_TOOL_COMPARE'))
    req(len(mod_pin) == 1 and mod_pin[0] == I.sha('UV_TAIL_MODULE_V001'), 'B3_MODULE_UNDER_TEST_PIN')
    cases, prov = {}, {}
    for case, tag in (('cube_O8', 'cube8'), ('cylinder_O8', 'cyl8')):
        f, p = {}, {}

        def one(role, d, name, limit, exact):
            return check_value(I, role, d, name, limit, exact)

        for fld, chk, lim in (('value_rel', 'E1_value', 1e-8), ('gradient_rel', 'E1_gradient', 1e-7), ('hessian_rel', 'E1_hessian', 1e-6)):
            f[fld], q = one('B3_COMPARE', c, '%s_%s' % (tag, chk), lim, False)
            p[fld] = {'derivation': 'copied', 'inputs': [q]}
        lp = [one('B3_COMPARE', c, '%s_E2_b0_vs_independent_t0' % tag, 1e-8, False),
              one('B3_COMPARE', c, '%s_E2_bd_vs_independent_tz_minus_t0' % tag, 1e-8, False)]
        f['lapse_pair_rel'] = max(v for v, _ in lp)
        p['lapse_pair_rel'] = {'derivation': 'max over the two lapse-pair members b0 and bd (E2), each over max|t| (GATE_B3_C4_V002 '
                               'rows lapse pair b0 / bd)', 'inputs': [q for _, q in lp]}
        for fld, chk, why in (
                ('bd_z0_max_abs', 'E3_bd_z0_exact_zero_nonzero_count',
                 'E3 counts the module bd(z=0) entries that are not +0.0 (pd[0] != 0.0 or signbit), over 72 radii x 16 azimuths '
                 '(n 1152; b3_compare_v001.py); a count of 0.0 implies max|bd(z=0)| = 0.0 exactly'),
                ('facade_midplane_ratio_max_abs', 'E5_facade_midplane_log_ratio_exact_zero',
                 'E5 indicator: 0.0 iff the facade midplane log ratio at z = 0 is +0.0 on every one of the 8 lines (line v002, '
                 'b3_compare_v001.py); 0.0 implies max|ratio| = 0.0 exactly'),
                ('imag_max_abs', 'E6_imaginary_part_unchanged_bitwise_and_real_jets',
                 'E6 indicator: 0.0 iff the tail jets are real float64 and the line evaluation imaginary part is bitwise unchanged '
                 'by the tail (b3_compare_v001.py); 0.0 implies the tail imaginary contribution is 0.0 exactly')):
            v, q = one('B3_COMPARE', c, '%s_%s' % (tag, chk), 0.0, True)
            req(v == 0.0, 'B3_INDICATOR_NOT_ZERO:%s' % chk)
            f[fld] = 0.0
            p[fld] = {'derivation': why, 'inputs': [q]}
        ang = [one('B3_TAP_REF_BODY', rb, '%s_%s_tap_gradient_vs_independent_over_max_grad' % (w, tag), 1e-7, None) for w in ('REF', 'BODY')]
        f['angular_reads_rel'] = max(v for v, _ in ang)
        p['angular_reads_rel'] = {'derivation': 'max over the reference and body TailBoundary-tap grad-t reads, each over max|grad t| '
                                  '(registered B3 item; GATE_B3_C4_V002 bold rows); the tap t reads are reported only (below)',
                                  'inputs': [q for _, q in ang],
                                  'reported_only': [one('B3_TAP_REF_BODY', rb, '%s_%s_tap_value_vs_independent_over_max_t' % (w, tag), 1e-7, None)[1]
                                                    for w in ('REF', 'BODY')]}
        colp = [one('B3_TAP_FSC', fsc, 'FSC_%s_%s_potential_z_module_vs_independent_over_max_tail_potential_difference' % (tag, col), 1e-7, None)
                for col in ('col00', 'col30')]
        f['column_potential_rel'] = max(v for v, _ in colp)
        p['column_potential_rel'] = {'derivation': 'max over the fs-column potential(z) comparisons of columns 00 and 30, each over the max '
                                     'tail potential difference (registered B3 item; GATE_B3_C4_V002); V001 E7 was a proxy and is not used',
                                     'inputs': [q for _, q in colp]}
        dbl = [one('B3_COMPARE', c, '%s_IND_doubling_%s' % (tag, w), 1e-10, False) for w in ('value', 'gradient', 'hessian')]
        f['doubling_rel'] = max(v for v, _ in dbl)
        p['doubling_rel'] = {'derivation': 'max over the independent-lane doubling self-convergence of value, gradient and Hessian',
                             'inputs': [q for _, q in dbl]}
        req(hi == 0.0, 'B3_HI_L67')
        f['hi_v003_L67_pass'] = True
        p['hi_v003_L67_pass'] = {'derivation': 'the single HI v003 L67-68 condition-text check (one source file, the same for both '
                                 'outer cases; GATE_B3_C4_V002 "(same check)"): verdict PASS, value 0.0 -> true', 'inputs': [p_hi]}
        cases[case], prov[case] = f, p
    fails = []
    for case, f in cases.items():
        for k, op, t in B3_TOL:
            x = f[k]
            if (op == '<=' and x > t) or (op == '==' and x != t):
                fails.append('%s/%s' % (case, k))
        if f['hi_v003_L67_pass'] is not True:
            fails.append('%s/hi_v003_L67_pass' % case)
    rec = {
        'schema': SCHEMA, 'gate': 'B3', 'verdict': 'PASS' if not fails else 'FAIL', 'producer': builder_pin(),
        'independent_lane': 'Claude4', 'imports_tail_library': not ind['pass_'], 'state_result_sha256': state, 'cases': cases,
        'provenance': {
            'independent_lane': {'derivation': 'the producing lane of B3_COMPARE_V001 (schema CLAUDE4_GATE_B3_COMPARE_V001; '
                                 'gate_b3_c4 is the Claude4 lane folder; GATE_B3_C4_V002 header: Claude4 main session)',
                                 'inputs': [{'file_role': 'B3_COMPARE', 'file_sha256': I.sha('B3_COMPARE'), 'field': 'schema', 'value': c['schema']}]},
            'imports_tail_library': {'derivation': 'not B3_COMPARE independence.pass_ (its static-import scan of b3_independent_v001.py, '
                                     'banned [] , the single dynamic import being FORWARD); re-read here from bytes: the static imports '
                                     'of b3_independent_v001.py equal the recorded list, b3_points_v001.py imports %s, FORWARD '
                                     '(galaxy_baryonic_source_forward_v002.py) imports %s; none names a tail-library module'
                                     % (pts_imports, fwd_imports),
                                     'inputs': [p_ind, {'file_role': 'B3_COMPARE', 'field': 'independence', 'value': ind}]},
            'state_result_sha256': {'derivation': 'copied from B3_COMPARE state.result_sha256; equal to the compare r11 PIN_R3 C4R3 sha '
                                    '(read from the compare bytes) and to result_sha256 of all four per-case independent outputs',
                                    'inputs': [{'file_role': 'B3_COMPARE', 'field': 'state.result_sha256', 'value': state}]},
            'cases': prov},
        'per_case_independent_outputs': per_case_inputs,
        'module_under_test': {'path': I.path('UV_TAIL_MODULE_V001'), 'sha256': I.sha('UV_TAIL_MODULE_V001'),
                              'note': 'the tail library pinned by b3_compare_v001.py (module side of every comparison)'},
        'human_report': I.pin('B3_REPORT_V002'),
        'note': ('FIELDS_R11 B3 JSON record assembled by Claude4 (0598) from its own gate outputs; no number recomputed. '
                 'GATE_B3_C4_V002.md (465cb3c3) stays the human report (a Markdown file reads RECORD_DEFECT as a gate record). '
                 'DECLARED: B3 ran on tail module v001 c28d4209; the sealed driver r5 pins module v002 2026f2b6, which differs from v001 '
                 'only in TAIL_MEMORY_CAP_BYTES (driver_r5 BUILD.md sec 1; driver_r5/check (a)); B3 was not rerun on v002.'),
        'sources': [I.source(r, u) for r, u in (
            ('B3_COMPARE', 'E1/E2/E3/E5/E6/doubling/HI/independence/state values'),
            ('B3_TAP_REF_BODY', 'reference and body tap grad-t reads (angular_reads_rel)'),
            ('B3_TAP_FSC', 'fs-column potential(z) columns 00 and 30 (column_potential_rel)'),
            ('B3_IND_CUBE', 'per-case independent output (state, script)'), ('B3_IND_CYL', 'per-case independent output'),
            ('B3_IND_CUBE_DOUBLE', 'per-case doubled independent output'), ('B3_IND_CYL_DOUBLE', 'per-case doubled independent output'),
            ('B3_TOOL_COMPARE', 'computing tool of B3_COMPARE (checks definitions)'), ('B3_TOOL_TAP', 'computing tool of the tap compares'),
            ('B3_TOOL_INDEPENDENT', 'independent lane'), ('B3_TOOL_POINTS', 'independent lane (points)'),
            ('B3_FORWARD', 'the one dynamic import of the independent lane'), ('B3_REPORT_V002', 'human report: item mapping'),
            ('B3_REPORT_V001', 'human report V001'), ('COMPARE_R11', 'PIN_R3 C4R3 sha'), ('FIELDS_R11', 'field contract'))]}
    return rec, fails


# ============================================================================================ B0 family, driver v010 r5
def is_reg(p):
    try:
        return stat_mod.S_ISREG(os.lstat(p).st_mode)
    except FileNotFoundError:
        return False


def reports_nonempty(d):
    """stat only: DRYRUN_REPORT.json and DRYRUN_PLAN.txt are regular files of size > 0."""
    return all(is_reg(os.path.join(d, k)) and os.lstat(os.path.join(d, k)).st_size > 0 for k in ('DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'))


FORBIDDEN_NAME_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc', 'ngc3198', 'kmax_a2f10_c5h_run_v001')
FORBIDDEN_NAMES_LISTED = []          # names only (never opened): any listed path in a forbidden name class is reported


def rel_files(d):
    """names only (os.walk, no link followed): sorted relative paths of the regular files; a symlink refuses."""
    out = []
    for root, dirs, files in os.walk(d, followlinks=False):
        for n in list(dirs) + files:
            req(not stat_mod.S_ISLNK(os.lstat(os.path.join(root, n)).st_mode), 'SYMLINK_IN_DRY_DIR:%s' % d)
        for n in files:
            p = os.path.join(root, n)
            req(stat_mod.S_ISREG(os.lstat(p).st_mode), 'NON_REGULAR_FILE_IN_DRY_DIR:%s' % d)
            r = os.path.relpath(p, d)
            low = p.casefold()
            if any(w in low for w in FORBIDDEN_NAME_WORDS) or any(c.startswith('uvt_') for c in low.split(os.sep)):
                FORBIDDEN_NAMES_LISTED.append(p)
            out.append(r)
    return sorted(out)


def r5_link(I):
    d = I.json('B0_R5')
    req(d['schema'] == 'B0_R5_VS_R4_C2V001', 'B0_R5_SCHEMA')
    req(d['tool'] == [I.path('B0_R5_TOOL'), I.sha('B0_R5_TOOL')], 'B0_R5_TOOL_PIN')
    req(d['r5'] == [I.path('R5_DRIVER'), I.sha('R5_DRIVER')], 'B0_R5_DRIVER_PIN')
    req(d['r4'] == [I.path('R4_DRIVER'), I.sha('R4_DRIVER')], 'B0_R5_PREDECESSOR_PIN')
    req(d['declared_map'][:2] == [I.path('R5_CASCADE_MAP'), I.sha('R5_CASCADE_MAP')], 'B0_R5_MAP_PIN')
    req(d['p128_registry'] == [I.path('R5_P128_REGISTRY'), I.sha('R5_P128_REGISTRY')], 'B0_R5_P128_REGISTRY_PIN')
    req(d['r4_b0_tool'] == [I.path('R4_B0_TOOL'), I.sha('R4_B0_TOOL')], 'B0_R5_R4_TOOL_PIN')
    rows, s = d['rows'], d['summary']
    counted = sorted(n for n, r in rows.items() if r['counted'] is True)
    noev = sorted(n for n, r in rows.items() if r['counted'] is False)
    req(len(counted) + len(noev) == len(rows) == s['specs'] == 80, 'B0_R5_ROW_COUNT')
    req(len(counted) == s['counted_comparisons'] == s['n_pass'] == 64 and sorted(s['pass_plan_identical']) == counted, 'B0_R5_COUNTED')
    req(s['fail'] == [] and sorted(s['no_evidence_equal_early_failures']) == noev and s['n_no_evidence'] == len(noev) == 16, 'B0_R5_NO_EVIDENCE')
    req(s['verdict_B0'] == 'PASS_PLAN_IDENTICAL', 'B0_R5_VERDICT')
    checks = {}
    for n in counted:
        r, fz = rows[n], rows[n]['files']
        req(r['verdict'] == 'PASS_PLAN_IDENTICAL' and r['r4']['exit'] == 0 and r['r5']['exit'] == 0, 'B0_R5_COUNTED_ROW:%s' % n)
        req(fz['reports_nonempty'] is True and fz['identical'] is True and fz['differ'] == {} and fz['only_r4'] == [] == fz['only_r5'], 'B0_R5_FILES:%s' % n)
        req(fz['files_r4'] == fz['files_r5'] > 0 and fz['raw_equal'] + fz['equal_after_T'] == fz['files_r5'], 'B0_R5_FILE_COUNTS:%s' % n)
        d4, d5 = os.path.join(DRY5, 'R4_' + n), os.path.join(DRY5, 'R5_' + n)
        f4, f5 = rel_files(d4), rel_files(d5)
        req(reports_nonempty(d4) and reports_nonempty(d5), 'B0_R5_REPORTS_EMPTY_BY_STAT:%s' % n)
        req(f4 == f5 and len(f5) == fz['files_r5'], 'B0_R5_FILE_LIST_BY_NAME:%s' % n)
        checks[n] = f5
    noev_rows = []
    for n in noev:
        r = rows[n]
        req(r['verdict'] == 'NO_EVIDENCE_EQUAL_EARLY_FAILURE' and r['r4']['exit'] == r['r5']['exit'] != 0, 'B0_R5_NOEV_ROW:%s' % n)
        req(r['terminal_line_equal_after_T'] is True and r['files']['reports_nonempty'] is False and r['files']['identical'] is True, 'B0_R5_NOEV_FILES:%s' % n)
        if 'ngc3198' in n.casefold():
            by_stat = 'NOT_INSPECTED_NAME_CLASS'          # the dry directory is not listed (NGC3198 name class); JSON value copied
        else:
            by_stat = 'EMPTY_OR_ABSENT' if not (reports_nonempty(os.path.join(DRY5, 'R4_' + n)) or reports_nonempty(os.path.join(DRY5, 'R5_' + n))) else 'NONEMPTY_ONE_SIDE'
            req(by_stat == 'EMPTY_OR_ABSENT', 'B0_R5_NOEV_REPORT_PRESENT_BY_STAT:%s' % n)
        noev_rows.append({'label': n, 'sha256': r['spec_sha256'], 'origins': r['origins'], 'r4_exit': r['r4']['exit'], 'r5_exit': r['r5']['exit'],
                          'terminal_line_equal_after_T': r['terminal_line_equal_after_T'], 'reports_nonempty': r['files']['reports_nonempty'],
                          'reports_by_stat': by_stat, 'verdict': r['verdict']})
    counted_rows = [{'label': n, 'sha256': rows[n]['spec_sha256'], 'origins': rows[n]['origins'], 'files_compared': rows[n]['files']['files_r5'],
                     'raw_equal': rows[n]['files']['raw_equal'], 'equal_after_T': rows[n]['files']['equal_after_T'], 'verdict': rows[n]['verdict']}
                    for n in counted]
    return d, rows, counted_rows, noev_rows, checks


def r4_link(I):
    rec, ev = I.json('R4_B0_RECORD'), I.json('R4_B0_EVIDENCE')
    req(rec['schema'] == SCHEMA and rec['gate'] == 'B0' and rec['verdict'] == 'PASS_PLAN_IDENTICAL', 'R4_B0_RECORD_HEAD')
    req(rec['evidence'] == I.pin('R4_B0_EVIDENCE'), 'R4_B0_RECORD_EVIDENCE_PIN')
    req(rec['producer'] == I.pin('R4_B0_TOOL') and rec['record_writer'] == I.pin('R4_RECORD_WRITER'), 'R4_B0_RECORD_PRODUCER')
    req(os.path.realpath(rec['driver']['path']) == os.path.realpath(I.path('R4_DRIVER')) and rec['driver']['sha256'] == I.sha('R4_DRIVER'), 'R4_B0_RECORD_DRIVER')
    req(ev['schema'] == 'B0_PLAN_IDENTITY_C2V001' and ev['v010'][1] == I.sha('R4_DRIVER'), 'R4_B0_EVIDENCE_DRIVER')
    req(ev['parents']['EXT'] == [I.path('V009_EXT_DRIVER'), I.sha('V009_EXT_DRIVER')], 'R4_B0_EVIDENCE_EXT_PARENT')
    req(ev['parents']['GEO'] == [I.path('V009_GEO_DRIVER'), I.sha('V009_GEO_DRIVER')], 'R4_B0_EVIDENCE_GEO_PARENT')
    req(ev['summary']['verdict_B0'] == 'PASS_PLAN_IDENTICAL' and ev['summary']['fail'] == [], 'R4_B0_EVIDENCE_SUMMARY')
    req(rec['maps']['EXT']['pairs'] == ev['T_maps']['EXT'] and rec['maps']['GEO']['pairs'] == ev['T_maps']['GEO'], 'R4_B0_MAP_PAIRS')
    status = {}
    for n, s in ev['specs'].items():
        for par, v in s['vs'].items():
            fz = v['files']
            reasons = []
            if s['v010']['exit'] != 0:
                reasons.append('v010_r4_exit_%d' % s['v010']['exit'])
            if v['parent_run']['exit'] != 0:
                reasons.append('%s_parent_exit_%d' % (par, v['parent_run']['exit']))
            dv, dp = os.path.join(DRY4, 'V010_' + n), os.path.join(DRY4, par + '_' + n)
            nonempty = reports_nonempty(dv) and reports_nonempty(dp)
            if not nonempty:
                reasons.append('reports_empty_or_absent_by_stat')
            counted = not reasons
            if counted:
                req(v['verdict'] == 'PASS_PLAN_IDENTICAL' and fz['identical'] is True and fz['differ'] == {}, 'R4_COUNTED_NOT_IDENTICAL:%s:%s' % (n, par))
                fv, fp = rel_files(dv), rel_files(dp)
                req(fv == fp and len(fv) == fz['files_v010'] == fz['files_parent'], 'R4_FILE_LIST_BY_NAME:%s:%s' % (n, par))
            else:
                req(v['verdict'] == 'PASS_PLAN_IDENTICAL', 'R4_EARLY_FAILURE_VERDICT:%s:%s' % (n, par))   # recorded as pass, pre B0-EMPTY
            status[(n, par)] = {'counted': counted, 'reasons': reasons, 'spec_sha256': s['spec_sha256'],
                                'files': (rel_files(dv) if counted else None)}
    return rec, ev, status


def b0_family(I):
    d5, rows, counted_rows, noev_rows, r5files = r5_link(I)
    rec4, ev4, st4 = r4_link(I)
    sets, excluded = {'EXT': [], 'GEO': [], 'NGC': []}, {'EXT': [], 'GEO': [], 'NGC': []}
    for k in ('EXT', 'GEO', 'NGC'):
        for e in rec4['spec_sets'][k]:
            n, sh = e['label'], e['sha256']
            req(n in ev4['specs'], 'R4_SET_LABEL_NOT_IN_EVIDENCE:%s' % n)
            req(ev4['specs'][n]['spec_sha256'] == sh, 'R4_SET_SHA:%s' % n)
            pars = [k] if k in ('EXT', 'GEO') else sorted(ev4['specs'][n]['vs'])
            req(all(p in ev4['specs'][n]['vs'] for p in pars), 'R4_SET_PARENT:%s' % n)
            ok4 = all(st4[(n, p)]['counted'] for p in pars)
            r = rows.get(n)
            ok5 = r is not None and r['spec_sha256'] == sh and r['counted'] is True and r['verdict'] == 'PASS_PLAN_IDENTICAL'
            if ok4 and ok5:
                sets[k].append({'label': n, 'sha256': sh})
            else:
                excluded[k].append({'label': n, 'sha256': sh, 'r4_link_counted': ok4,
                                    'r4_link_reasons': sorted({x for p in pars for x in st4[(n, p)]['reasons']}),
                                    'r5_link_counted': bool(ok5), 'r5_link_verdict': None if r is None else r['verdict']})
    for k in sets:
        req(len({e['sha256'] for e in sets[k]}) == len(sets[k]), 'DUPLICATE_SHA_IN_SET:%s' % k)
    files_compared = set()
    per_spec_files = {}
    for k in ('EXT', 'GEO'):
        for e in sets[k]:
            n = e['label']
            f4 = st4[(n, k)]['files']
            files_compared |= set(f4) | set(r5files[n])
            per_spec_files.setdefault(n, {})['r4_link_%s' % k] = len(f4)
            per_spec_files[n]['r5_link'] = len(r5files[n])
    files_compared = sorted(files_compared)
    r4_counted = sorted('%s:%s' % kp for kp, v in st4.items() if v['counted'])
    r4_noev = sorted(({'label': kp[0], 'parent': kp[1], 'sha256': v['spec_sha256'], 'reasons': v['reasons']}
                      for kp, v in st4.items() if not v['counted']), key=lambda x: (x['label'], x['parent']))
    bm = [l for l in I.text('R5_BUILD').splitlines() if l.startswith('- **Declared map.**')]
    req(len(bm) == 1, 'R5_BUILD_DECLARED_MAP_LINE')
    drv = I.pin('R5_DRIVER')

    def link_maps(k):
        return {
            'composition': ('plan identity of the sealed v010 r5 against v009-%s on spec_sets/%s = link 1 (v009-%s -> v010 r4, r4 B0 run) '
                            'composed with link 2 (v010 r4 -> v010 r5, r5 B0 run); an entry is listed only when it is counted under '
                            'B0-EMPTY and PASS_PLAN_IDENTICAL at BOTH links (FORMAL: transitivity of plan identity under the declared '
                            'maps; each link TESTED by its own run)' % (k, k, k)),
            'link1_v009_to_r4': {'parent_driver': I.pin('V009_%s_DRIVER' % k), 'driver': I.pin('R4_DRIVER'),
                                 'pairs': rec4['maps'][k]['pairs'], 'rule': rec4['maps'][k]['rule'],
                                 'record': I.pin('R4_B0_RECORD'), 'evidence': I.pin('R4_B0_EVIDENCE'), 'tool': I.pin('R4_B0_TOOL'),
                                 'b0_empty': 'applied here from bytes: v010 r4 exit 0, parent exit 0, DRYRUN_REPORT.json and DRYRUN_PLAN.txt '
                                             'regular and non-empty on both sides (stat) -- the r5 tool rule'},
            'link2_r4_to_r5': {'predecessor_driver': I.pin('R4_DRIVER'), 'driver': drv,
                               'declared_map': {'path': d5['declared_map'][0], 'sha256': d5['declared_map'][1],
                                                'substitution_pairs': d5['declared_map'][2]},
                               'rule': bm[0], 'b0_empty_rule': d5['rule'], 'evidence': I.pin('B0_R5'), 'tool': I.pin('B0_R5_TOOL')}}

    maps = {'EXT': link_maps('EXT'), 'GEO': link_maps('GEO')}
    b0_empty = {
        'rule': d5['rule'],
        'ruling': 'V005 addendum (Codex2 SHOULD_FIX B0-EMPTY, ruled): B0 counts only comparisons whose expected reports are non-empty and '
                  'whose planning completes; equal early failures are listed separately as no evidence.',
        'r5_link': {'specs': d5['summary']['specs'], 'counted_comparisons': d5['summary']['counted_comparisons'],
                    'pass_plan_identical': d5['summary']['n_pass'], 'fail': d5['summary']['fail'],
                    'counted': counted_rows, 'no_evidence_equal_early_failures': noev_rows},
        'r4_link': {'comparisons_recorded': ev4['summary']['comparisons'], 'recorded_pass': ev4['summary']['pass'],
                    'counted_under_b0_empty': len(r4_counted), 'counted': r4_counted, 'no_evidence': r4_noev}}
    ok = (d5['summary']['verdict_B0'] == 'PASS_PLAN_IDENTICAL' and ev4['summary']['verdict_B0'] == 'PASS_PLAN_IDENTICAL'
          and d5['summary']['fail'] == [] and ev4['summary']['fail'] == [] and all(sets[k] for k in sets))
    common_sources = [I.source(r, u) for r, u in (
        ('B0_R5', 'link 2 (r4 -> r5) plan identity, B0-EMPTY counted / no-evidence rows'),
        ('B0_R5_TOOL', 'computing tool of link 2'),
        ('R4_B0_RECORD', 'link 1 maps and EXT/GEO/NGC classification'),
        ('R4_B0_EVIDENCE', 'link 1 per-spec exit codes, verdicts, file counts'),
        ('R4_B0_TOOL', 'computing tool of link 1'), ('R4_RECORD_WRITER', 'writer of the r4 records (precedent)'),
        ('R5_DRIVER', 'sealed driver v010 r5'), ('R4_DRIVER', 'predecessor v010 r4'),
        ('V009_EXT_DRIVER', 'parent v009-EXT'), ('V009_GEO_DRIVER', 'parent v009-GEO'),
        ('R5_CASCADE_MAP', 'link 2 declared map'), ('R5_BUILD', 'r5 BUILD (declared map text, sec 4)'),
        ('R5_P128_REGISTRY', 'P128 specs of link 2'), ('FIELDS_R11', 'field contract'), ('DISPATCH_0598', 'assignment'))]
    dry_note = ('report directories read by NAME and SIZE only (os.walk / lstat, no content opened): '
                '%s/{R4,R5}_<label> and %s/{V010,EXT,GEO}_<label>' % (DRY5, DRY4))
    b0 = {'schema': SCHEMA, 'gate': 'B0', 'verdict': 'PASS_PLAN_IDENTICAL' if ok else 'FAIL', 'producer': builder_pin(),
          'driver': drv, 'maps': maps, 'spec_sets': sets, 'excluded_from_spec_sets': excluded, 'b0_empty': b0_empty,
          'dry_dirs': dry_note, 'sources': common_sources,
          'note': ('B0 on the sealed driver v010 r5 (A87 / 0598), built from existing outputs only. The r5 run (B0_R5_VS_R4_C2V001) is '
                   'r5 against r4: 64 counted, 64 PASS_PLAN_IDENTICAL, 0 FAIL; 16 equal early failures listed as no evidence. The '
                   'EXT/GEO/NGC sets are the r4 record sets restricted to entries counted at both links.')}
    bdry = {'schema': SCHEMA, 'gate': 'B0prime_DRY', 'verdict': 'PASS_DRY_IDENTICAL' if ok else 'FAIL', 'producer': builder_pin(),
            'driver': drv, 'files_compared': files_compared, 'spec_sets': sets, 'per_spec_file_counts': per_spec_files,
            'maps': maps, 'b0_empty': {'rule': d5['rule'], 'note': 'the same counted dry runs as B0 at both links'},
            'dry_dirs': dry_note, 'sources': common_sources,
            'note': ('R1 L3: B0prime-SIM withdrawn; B0prime_DRY = the same dry runs as B0, every report file compared (DRYRUN_REPORT.json, '
                     'DRYRUN_PLAN.txt and every planned input). files_compared = the union of the relative paths present (by name) in '
                     'the counted report directories of both links; each directory pair has the same name list and the recorded count.')}
    req({'DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'} <= set(files_compared), 'B0prime_DRY_FILES')
    fa_cases, fa_fail = {}, []
    rec4fa = I.json('R4_B0_FA_RECORD')
    for n, key in (('FA_A1_NFP_EMPTY', 'A1'), ('FA_A2_NFP_ABSENT', 'A2'), ('FA_A4_CONV_EMPTY', 'A4')):
        r = rows[n]
        req(r['origins'] == ['r4 B0_FA set'] and r['r5']['exit'] != 0, 'B0_FA_ROW:%s' % n)
        tail = ' '.join(r['r5']['stderr_tail'])
        m = re.match(r'(\w+): (\w+)', tail)
        st = 'REFUSED' if (m and m.group(1) == 'Refusal') else 'OTHER'
        code = m.group(2) if m else 'NO_CODE_IN_TERMINAL_LINE'
        req(rec4fa['cases'][key]['spec_sha256'] == r['spec_sha256'], 'B0_FA_SPEC_NOT_THE_R4_FA_SPEC:%s' % key)
        fa_cases[key] = {'status': st, 'code': code, 'spec_sha256': r['spec_sha256'], 'r5_exit': r['r5']['exit'], 'terminal_line': tail,
                         'terminal_line_equal_after_T_r4_r5': r['terminal_line_equal_after_T'], 'r4_record_case': rec4fa['cases'][key]['code']}
        if not (st == 'REFUSED' and code == 'ROUTE_A_CHECKPOINT_MISSING'):
            fa_fail.append(key)
    bfa = {'schema': SCHEMA, 'gate': 'B0_FA', 'verdict': 'PASS' if not fa_fail else 'FAIL', 'producer': builder_pin(),
           'numbers_producer': I.pin('B0_R5_TOOL'), 'driver': drv, 'cases': fa_cases,
           'derivation': ('status/code from the r5 driver terminal line recorded by the r5 B0 run (rows FA_A1_NFP_EMPTY, FA_A2_NFP_ABSENT, '
                          'FA_A4_CONV_EMPTY): re.match(r"(\\w+): (\\w+)") -> status REFUSED iff the first token is Refusal, code = the '
                          'second token (the derivation of driver_r4/gates/write_gate_records_v007_c2v003.py); the r5 run executes the r5 '
                          'driver in dry-run (simulate) mode; the refusal precedes any stage'),
           'sources': [I.source(r, u) for r, u in (
               ('B0_R5', 'r5 terminal lines of the three FA specs'), ('B0_R5_TOOL', 'computing tool (numbers_producer)'),
               ('R5_DRIVER', 'sealed driver'), ('R4_B0_FA_RECORD', 'r4 B0_FA record: the same three specs (cross-check)'),
               ('R4_RECORD_WRITER', 'derivation precedent'), ('FIELDS_R11', 'field contract'), ('DISPATCH_0598', 'assignment'))],
           'note': ('B0_FA on the sealed driver v010 r5: the three R-A F-A specs end REFUSED (ROUTE_A_CHECKPOINT_MISSING) under r5. In the '
                    'B0 plan-identity count these three rows are equal early failures (no plan evidence), listed under B0-EMPTY; that '
                    'does not change the B0_FA reading, which is the refusal itself.')}
    return {'B0': b0, 'B0prime_DRY': bdry, 'B0_FA': bfa}, {'sets': {k: len(v) for k, v in sets.items()},
                                                          'excluded': {k: len(v) for k, v in excluded.items()},
                                                          'files_compared': len(files_compared), 'fa_fail': fa_fail}


# ============================================================================================ not built
def missing_runs(I):
    n3 = I.json('R4_B0_N3_RECORD')
    cm = I.json('R5_CASCADE_MAP')
    pm, sm = cm['declared_path_map'], cm['declared_sha_map']
    fp = {r['old_path']: r for r in cm['files']}
    rec_sha = {n3['driver']['path']: n3['driver']['sha256']}     # shas as the r4 N3 record carries them (no scanned file is opened:
    for c in n3['constructions']:                                # two of them are named uvt_*, which the fence refuses)
        if 'file_sha256' in c:
            rec_sha[c['file']] = c['file_sha256']
        if 'guard' in c:
            rec_sha[c['guard']['file']] = c['guard']['file_sha256']
    n3_targets = []
    for f in sorted(set(n3['files_scanned']) | {c['guard']['file'] for c in n3['constructions'] if 'guard' in c}):
        sh = rec_sha.get(f)
        req(sh is not None, 'R4_N3_FILE_SHA_NOT_IN_RECORD:%s' % os.path.basename(f))
        e = fp.get(f) or fp.get(os.path.realpath(f))
        if e is not None:
            req(e['old_sha256'] == sh, 'CASCADE_OLD_SHA:%s' % os.path.basename(f))
            r5f, r5s = e['new_path'], e['new_sha256']
        elif sh in sm:
            r5f, r5s = pm.get(f) or pm.get(os.path.realpath(f)) or 'SHA_REMAPPED_PATH_NOT_IN_MAP', sm[sh]
        else:
            r5f, r5s = 'UNCHANGED_NOT_IN_CASCADE_MAP', sh
        n3_targets.append({'r4_file': f, 'r4_sha256': sh, 'role': 'scanned' if f in n3['files_scanned'] else 'guard_only',
                           'r5_file': r5f, 'r5_sha256': r5s})
    earlier = []
    for dd in EARLIER_RECORD_DIRS:
        for g in EARLIER_RECORD_GATES:
            p = os.path.join(TSI, dd, 'GATE_%s.json' % g)
            with open(p, 'rb') as fh:
                b = fh.read()
            o = loads_strict(b)
            earlier.append({'gate': g, 'path': p, 'sha256': _sha_bytes(b), 'schema': o.get('schema'), 'verdict': o.get('verdict'),
                            'driver_sha256': (o.get('driver') or {}).get('sha256')})
    r6dir = TSI + '/driver_r6'
    return {
        'schema': 'CLAUDE4_SEAL_RECORDS_MISSING_RUNS_C4V001',
        'sealed_driver': I.pin('R5_DRIVER'),
        'not_built': {
            'B0_N3': {'status': 'NOT_BUILT_MISSING_RUN',
                      'missing': ('the RA8 static TailBoundary / TailState guard scan on the r5 tail-ON code: every construction and tail build '
                                  'site in the r5 driver and in the r5 cascade image of each file the r4 scan covered, each with its tail-OFF '
                                  'guard (the N3_SITES scan of write_gate_records_v007_c2v003.py, retargeted to the r5 paths and shas of '
                                  'CASCADE_MAP_R5_C2V001; the guard file RO1 worker c2v002 9f74d465 -> r5 fbe9ae79). No r5 N3 output exists.'),
                      'r5_scan_targets_from_the_r4_files_scanned': n3_targets,
                      'existing_outputs_not_on_the_sealed_driver': [I.source('R4_B0_N3_RECORD', 'r4 B0_N3 record (driver b9ae92d5)'),
                                                                     I.source('R4_RECORD_WRITER', 'r4 N3 scan producer')]},
            'B0_RO1': {'status': 'NOT_BUILT_MISSING_RUN',
                       'missing': ('(a) the r5 identity runs Z2 (spec 2d5e79d0), Z2_OFF_RO1 (894e5b3a) and B0prime_RERUN (4ac5527a) on driver '
                                   'b5cc62af (root launches, A55 item 3; SEAL_CHECKLIST A5), read by a B0_RO1 producer for result.json sha256 '
                                   'and route_a_outcome.ro1.fired false; (b) the RA5 (b) replay on the C6 iteration-8 checkpoint through the r5 '
                                   'RO1 custody (workers fbe9ae79 / 869ce387, binding 86af6198): ROUTE_A_READOUT_NO_CIRCULAR_BRANCH at query 3, '
                                   'handed to route B; (c) the part (c) cases OTHER_EXCEPTION and REFUSAL_BEFORE_CONVERGENCE (expected = '
                                   'observed = CALL_FAILED) on the same custody. No B0_RO1 gate record exists for any driver.'),
                       'existing_outputs_not_on_the_sealed_custody': [
                           I.source('RO1_TEST_C6_REPLAY', 'C6 replay on RO1 c2v001 workers fc698c3c / 867d2c87 and a v009 test vehicle'),
                           I.source('RO1_TEST_SYN', 'synthetic RO1 predicate tests'),
                           I.source('RO1_TEST_DRIVER_PATCH', 'RO1 driver patch on v009-EXT')]},
            'I4': {'status': 'NOT_BUILT_MISSING_RUN',
                   'missing': ('the I4 run "I4 at production (C2T N8 against N1)" (CHECK_V001 sec 10, listed UNTESTED there) on driver v010 r5 '
                               'b5cc62af with the tail ON: the same C2T spec at route_a.column_workers 8 and 1, compared bitwise outside custody '
                               '(declared token list TOKENS_I4_SERIAL_PARALLEL), with the V8c-F1 fix confirmed on the r5 parallel worker. The '
                               'only registered N1 pair is the r4 V007 registry C2T N8 / N1_FALLBACK templates (1348aed5 / 2cc67753, both '
                               'plan-identical r5 vs r4 in the r5 B0 run); the P128 registry SPECS_P128_R5_C2V001 carries no N1 spec. The pair '
                               'is root to fix. No I4 gate record exists for any driver.'),
                   'existing_outputs_not_on_the_sealed_driver': [
                       I.source('CHECK_V001', 'A51 final check: replay-level serial == parallel tail ON on driver v010 r3 4c14552f'),
                       I.source('TOKENS_I4', 'declared I4 custody token list (empty declared list)')]}},
        'r6': {'status': 'NOT_BUILT_BUILD_NOT_LANDED', 'build_md_present': os.path.exists(os.path.join(r6dir, 'BUILD.md')),
               'existing_outputs': [I.source('R6_B0', 'B0 r6 vs r5 (exists; not used: the r6 BUILD has not landed)')]},
        'earlier_b0_family_records_found': earlier}


# ============================================================================================ write
def canon_bytes(obj):
    s = json.dumps(obj, sort_keys=True, indent=1, allow_nan=False) + '\n'
    b = s.encode('ascii')
    loads_strict(b)                                 # re-parse strictly (duplicate key / NaN refuse)
    return b


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ('dry', 'write'):
        raise SystemExit(__doc__)
    mode, recdir, auxdir = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    I = Inputs()
    b3, b3_fails = build_b3(I)
    fam, fam_summary = b0_family(I)
    miss = missing_runs(I)
    recs = {'B3': ('B3_RECORD_C4V001.json', b3), 'B0': ('B0_R5_RECORD_C4V001.json', fam['B0']),
            'B0prime_DRY': ('B0prime_DRY_R5_RECORD_C4V001.json', fam['B0prime_DRY']),
            'B0_FA': ('B0_FA_R5_RECORD_C4V001.json', fam['B0_FA'])}
    out = {g: (fn, canon_bytes(o)) for g, (fn, o) in recs.items()}
    inputs_used = {r: {'path': I.path(r), 'sha256': I.s[r], 'task_pinned': PINS[r][1]} for r in sorted(I.s)}
    manifest = {'schema': 'CLAUDE4_SEAL_RECORDS_BUILD_MANIFEST_C4V001', 'ts_utc': os.environ.get('TS'), 'mode': mode,
                'builder': builder_pin(), 'fence': {'path': str(FENCE), 'sha256': FENCE_SHA},
                'python': sys.version.split()[0], 'inputs': inputs_used,
                'records': {g: {'file': fn, 'sha256': _sha_bytes(b), 'verdict': recs[g][1]['verdict']} for g, (fn, b) in out.items()},
                'b3_fails': b3_fails, 'b0_family_summary': fam_summary,
                'forbidden_class_names_listed_never_opened': sorted(set(FORBIDDEN_NAMES_LISTED)),
                'fence_blocked': list(FEN.BLOCKED)}
    aux = {'BUILD_MANIFEST_C4V001.json': canon_bytes(manifest), 'MISSING_RUNS_C4V001.json': canon_bytes(miss)}
    print(json.dumps({'mode': mode, 'records': manifest['records'], 'b3_fails': b3_fails, 'b0_family': fam_summary,
                      'missing': sorted(miss['not_built']), 'r6': miss['r6']['status'], 'fence_blocked': manifest['fence_blocked'],
                      'forbidden_class_names_listed': manifest['forbidden_class_names_listed_never_opened'],
                      'files_compared': fam['B0prime_DRY']['files_compared'],
                      'spec_sets': {k: [e['label'] for e in v] for k, v in fam['B0']['spec_sets'].items()},
                      'excluded': {k: [e['label'] for e in v] for k, v in fam['B0']['excluded_from_spec_sets'].items()}}, indent=1))
    if mode == 'dry':
        return 0
    for d in (recdir, auxdir):
        req(str(d).startswith(str(BUILD) + os.sep), 'OUTDIR_NOT_INSIDE_BUILD')
        d.mkdir(parents=True, exist_ok=True)
    for g, (fn, b) in out.items():
        with open(recdir / fn, 'xb') as f:
            f.write(b)
    for fn, b in aux.items():
        with open(auxdir / fn, 'xb') as f:
            f.write(b)
    for g, (fn, b) in out.items():
        with open(recdir / fn, 'rb') as f:
            req(_sha_bytes(f.read()) == _sha_bytes(b), 'WRITE_READBACK:%s' % fn)
    print('written', str(recdir), str(auxdir))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Refuse as exc:
        print('REFUSED: %s' % exc, file=sys.stderr)
        sys.exit(2)
