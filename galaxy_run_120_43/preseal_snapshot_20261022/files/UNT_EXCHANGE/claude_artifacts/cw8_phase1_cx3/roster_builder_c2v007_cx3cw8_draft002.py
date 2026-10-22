#!/usr/bin/env python3
"""roster_builder_c2v007: A223/A226/A248–A253 immutable review candidate.

Commands: build, pass, step7, custody, sens-budget, verify-registry, phase1-snapshot,
check-gate-list, seal-check, tsr-record, tsr-support, tsr-check.
Inputs and outputs are pinned/exclusive-create. No launch command exists.

The reviewed c2v006 implementation is retained below, followed by explicit
c2v007 components. The last definitions are the effective public interface;
saved predecessor helpers implement the unchanged registration/ledger rules.
See RUNBOOK_V002_C2V007.md and README_C2V007.md for the current contracts.
Production operation is UNTESTED in this lane; synthetic evidence is separate.
"""

import datetime
import hashlib
import json
import math
import os
import re
import stat
import sys
import types

BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v001'
# c2v004 to c2v006 change no input schema and no schema of the builder's own records, so the c2v003 schema names are
# kept (c2v006 adds `schema` to classifier A's two records, whose contract names are A's); each BUILD_RECORD names the
# builder sha256, and a build record of another builder version is refused (BUILD_RECORD_OTHER_BUILDER)
INPUT_SCHEMA = 'ROSTER_BUILDER_INPUT_C2V003'
ROSTER_SCHEMA = 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001'
GATE_SCHEMA = 'REGISTERED_INVALID_ROW_GATE_CX3V001'
CUT_SCHEMA = 'NGC_CANDIDATE_ROSTER_CUT_CX3V001'
BUILTIN_REASONS = frozenset({'QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT',
                             'QUERY_OUTSIDE_RETAINED_SUPPORT'})
ALT_EVALUATED = 'EVALUATED_BEFORE_FREEZE'
ALT_NOT_EVALUATED = 'NOT_EVALUATED_BEFORE_FREEZE'
STAGE0_NAME = 'STAGE0_GRID_OUTER'
PHASES = ('PHASE_1', 'PHASE_2')
STAGES = ('PLAN', 'MEMBERS', 'FULL')
CUTOFF_KIND = {'PHASE_1': 'PHASE1_STEP4_START', 'PHASE_2': 'PHASE1_SCORE'}
CLASSES = ('FINISHED', 'FAILED', 'CAP', 'OUTPUT_CAP', 'INFRA', 'PLANNED_STOP')
FAILURE_CLASSES = ('FAILED', 'CAP', 'OUTPUT_CAP')
DISPOSITION_OF = {'FINISHED': 'EVALUATED', 'FAILED': 'EVALUATED_FAILED', 'CAP': 'UNEVALUATED_CAP',
                  'OUTPUT_CAP': 'UNEVALUATED_CAP'}
EVALUATED_DISPOSITIONS = ('EVALUATED', 'EVALUATED_FAILED')
# receipt key roles: root names, once per receipt producer, the receipt key that carries each role (G13, G25, G27).
# theta_sha256 (new in c2v003) carries the sha256 of the v003g canonical bytes of the call's exact theta_ngc.
RECEIPT_KEY_ROLES = ('status', 'time_utc', 'spec_sha256', 'theta_sha256', 'rss_cap_bytes', 'wall_cap_s',
                     'host_ram_bytes', 'other_ngc_processes_max', 'output_cap_bytes')
EVIDENCE_ROLES = ('spec_sha256', 'rss_cap_bytes', 'wall_cap_s', 'host_ram_bytes', 'other_ngc_processes_max',
                  'output_cap_bytes')
BINDING_ROLES = ('theta_sha256', 'spec_sha256')
M15_RECORD_SCHEMA = 'M15_PRE_LAUNCH_RECORD_C2V001'
GATE_REPORT_SCHEMA = 'GATE_STATUS_REPORT_C2V003'
REPLAY_PLAN_SCHEMA = 'REPLAY_PLAN_C2V003'
BUILD_RECORD_SCHEMA = 'ROSTER_BUILD_RECORD_C2V003'
PASS_RECORD_SCHEMA = 'FREEZE_PASS_RECORD_C2V003'
PASS_INPUT_SCHEMA = 'PASS_INPUT_C2V003'
SENS_PLAN_SCHEMA_NOTE = 'VALUE_FREE_SENSITIVITY_PLAN_C2V003'
SERVE_LOG_SCHEMA = 'REPLAY_SERVE_LOG_C2V003'
STEP7_RESULT_SCHEMA = 'STEP7_RESULT_C2V003'
LAUNCH_REGISTRY_SCHEMA = 'STEP5_LAUNCH_REGISTRY_C2V003'
LAUNCH_REGISTRY_ENTRY_KEYS = ('alternative', 'kind', 'key', 'theta_sha256', 'spec_sha256')
LAUNCH_KINDS = ('MEMBER', 'SENSITIVITY', 'OTHER')
# R3: the step-7 ledger is <step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>/; a STEP7_LEDGER directory beside the
# build record (the c2v002 location) is a second ledger and refuses
STEP7_LEDGER_DIR = 'STEP7_LEDGER'
LEDGER_DIR_PREFIX = 'STEP7_LEDGER_'
LEDGER_GENESIS_NAME = 'LEDGER_GENESIS.json'
LEDGER_GENESIS_SCHEMA = 'STEP7_LEDGER_GENESIS_C2V003'
# classifier A's root-written input contracts, from the bytes of classifier_a_c4v004.py (e92aa30e): every root-written
# record carries `schema` set to its contract name, and its key set is exact (root ruling A173 on OI-A1, ruling (a)).
# Gate list: check_gate_list L734, entries L739. TSR record: check_tsr L679-681, flags L699.
A_GATE_LIST_NAME = 'GATE_STATUS_LIST_C4V001'
A_GATE_LIST_KEYS = ('schema', 'gates')
A_GATE_ENTRY_KEYS = ('gate_sha256', 'status', 'pinned_by_entry')
A_GATE_STATUSES = ('ON-TIME', 'LATE')
A_TSR_NAME = 'TSR_FLAG_RECORD_C4V001'
A_TSR_KEYS = ('schema', 'target_free', 'rule', 'failing_ring_ordinal', 'ntest_compare_pin', 'n1_record_pin',
              'gl_node_record_pin', 'flags')
A_TSR_FLAG_KEYS = ('query_id', 'TRUNCATION_SHAPE_RESIDUAL')
# classifier A's 17 bundle input roles: which this builder writes, and who writes every other one
A_INPUTS_PRODUCED = {
    'gate_status_list': 'build (FULL stage): GATE_STATUS_LIST.json, schema GATE_STATUS_LIST_C4V001; check-gate-list '
                        'binds it to the build',
    'tsr_flag_record': 'tsr-record: ROOT_TSR_FLAG_RECORD_V003.json, schema TSR_FLAG_RECORD_C4V001 (projection of the '
                       'pinned V001); tsr-check verifies it',
}
A_INPUTS_NOT_PRODUCED = {
    'phase_inputs': 'root writes PHASE_INPUTS_C4V001 (phase named by the score entry, both registry roots, run '
                    'status and code, the Phase-1 header B_P1 / u_A log index / Phase-1 record and L1 shas, the '
                    'absent-reason); none of these is a builder input',
    'stage0_status': 'root writes STAGE0_STATUS_RECORD_C4V003 as an exact projection of the frozen manifest '
                     'stage0_status block of the STAGE0 successor (A154); the replay plan stage0_status is not it',
    'commitment_status': 'root writes PHASE2_COMMITMENT_STATUS_C4V001 with the Phase-2 score entry',
    'fallback': 'root writes FALLBACK_RECORD_C4V001',
    'field_map': 'root writes KEY_FIELD_MAP_C4V001 only if a key rename is needed',
    'root_disclosures': 'root writes it (D-4 values, attestation, V005/V006 shas, RUNBOOK_V002 and builder shas, '
                        'window changes, outer_gas_cut_report)',
    'freeze_manifest': 'v003g write_freeze_manifest, run by the step-8 freeze script (G26)',
    'score': 'v003g score_after_freeze (step 9)',
    'slots': 'the sealed slots (V003, or the M-14 successor), pinned as is',
    'tsr_support_record': 'UNT_ROOT_TSR_SUPPORT_CX3V001; does not exist; root ruling G7',
    'ntest_compare': 'the N-test compare of record (6f095f64), pinned as is',
    'agree_record': 'the pinned phase1 tool agree command (A133 agree record, OC-02)',
    'phase1_classification': 'classifier A itself (its Phase-1 output)',
    'l1_record': 'the pinned phase1 tool band command (L1_C2V001.json)',
    'c3_record': 'the M-13 record',
}
ALT_NAME_RE = re.compile(r'^[A-Za-z0-9_.\-]+$')
HEX64_RE = re.compile(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])')
ISO_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z$')
LEDGER_RESULT_RE = re.compile(r'^STEP7_(\d{4})\.json$')
LEDGER_PLAN_RE = re.compile(r'^PLAN_([0-9a-f]{64})\.json$')
LEDGER_PASS_RE = re.compile(r'^PASS_([0-9a-f]{64})\.json$')
# M-6 seal entry format proposed under G17: a `## ` heading carrying SEAL_ENTRY and the sealed text's full sha256,
# then one line per sealed object of the exact form "- ROLE: `<64-hex>`" (free text may follow the closing backtick)
SEAL_ENTRY_TOKEN = 'SEAL_ENTRY'
SEAL_ROLE_LINE_RE = re.compile(r'^- ([A-Z][A-Z0-9_]*): `([0-9a-f]{64})`(.*)$')

# M-7 production constants (pins verified from bytes; r3a section 1.4 and section 11). c2v006 pins the flag record
# ROOT_TSR_FLAG_RECORD_V003.json (classifier A's schema with its `schema` key, A173; derived by `tsr-record` from V001
# by projection; V002 c9d8ab45 lacks the key and is superseded) and keeps the V001 sha as the only admissible
# derivation input.
TSR_FLAG_SCHEMA = 'UNT_ROOT_TSR_FLAG_RECORD_C2V001'      # the V001 schema (derivation input only)
TSR_RULE_ID = 'M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001'
PRODUCTION_TSR = {
    'flag_record_sha256': '7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070',
    'v001_flag_record_sha256': '61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc',
    'compare_sha256': '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9',
    'n1_sha256': '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70',
    'node_sha256': 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d',
    'failing_ordinal': 15,
    'lower_kpc': 9.901810628740723,
    'upper_kpc': 10.911721936765339,
    'flagged_ids': ['NGC3198-Q25'],
    'all_ids': ['NGC3198-Q%02d' % i for i in range(1, 44)],
}
SEAL_REQUIRED_ROLES = ('PREREG_TEXT', 'CLASSIFIER', 'TSR_FLAG_RECORD')


class Refused(Exception):
    """An input defect: nothing produced by this call may be adopted."""

    def __init__(self, code, detail=''):
        super().__init__('%s: %s' % (code, detail))
        self.code = code
        self.detail = detail


class Stop(Exception):
    """A pre-target stop condition (r3a section 1.1)."""

    def __init__(self, code, detail=''):
        super().__init__('%s: %s' % (code, detail))
        self.code = code
        self.detail = detail


# --------------------------------------------------------------------------------------------------------------
# bytes, pins and strict JSON
# --------------------------------------------------------------------------------------------------------------

def _is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def sha256_hex(raw):
    return hashlib.sha256(raw).hexdigest()


def _no_duplicate_keys(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Refused('JSON_DUPLICATE_KEY', repr(k))
        out[k] = v
    return out


def _reject_constant(name):
    raise Refused('JSON_NONFINITE_CONSTANT', name)


def strict_json(raw, where):
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_no_duplicate_keys, parse_constant=_reject_constant)
    except Refused:
        raise
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise Refused('JSON_PARSE_FAILED', '%s: %s' % (where, type(exc).__name__))


def canonical_bytes(obj):
    """Equal to v003g _canonical_bytes on JSON-native objects (checked against it at every build)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def dump_bytes(obj):
    return (json.dumps(obj, sort_keys=True, indent=1, allow_nan=False) + '\n').encode('utf-8')


def theta_sha256(theta):
    return sha256_hex(canonical_bytes(theta))


def _read_regular(path, where, ident_out=None):
    """The bytes of a regular file and its realpath. ident_out (a list), when given, receives the file identity
    (st_dev, st_ino) from the fstat of the same descriptor whose bytes are returned (c2v004)."""
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise Refused('PIN_UNREADABLE', '%s: %s' % (where, type(exc).__name__))
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Refused('PIN_NOT_REGULAR_FILE', where)
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
    finally:
        os.close(fd)
    raw = b''.join(chunks)
    if not raw:
        raise Refused('PIN_EMPTY_FILE', where)
    if ident_out is not None:
        ident_out.append((st.st_dev, st.st_ino))
    return raw, os.path.realpath(path)


def read_bytes_pin_ident(pin, where):
    """read_bytes_pin plus the file identity (st_dev, st_ino) of the bytes read: a hard link is the same file under
    another path, which a realpath never shows (c2v004). The identity is never written to an output."""
    if not isinstance(pin, dict) or set(pin) != {'path', 'sha256'}:
        raise Refused('PIN_SHAPE', '%s: a pin is exactly {path, sha256}' % where)
    path, sha = pin['path'], pin['sha256']
    if not isinstance(path, str) or not os.path.isabs(path) or not _is_hex64(sha):
        raise Refused('PIN_SHAPE', '%s: absolute path and lowercase 64-hex sha256 required' % where)
    ident = []
    raw, real = _read_regular(path, where, ident)
    if sha256_hex(raw) != sha:
        raise Refused('PIN_MISMATCH', where)
    return raw, {'path': real, 'sha256': sha}, ident[0]


def read_bytes_pin(pin, where):
    raw, norm, _ident = read_bytes_pin_ident(pin, where)
    return raw, norm


def read_json_pin_ident(pin, where):
    raw, norm, ident = read_bytes_pin_ident(pin, where)
    doc = strict_json(raw, where)
    return doc, norm, raw, ident


def read_json_pin(pin, where):
    doc, norm, raw, _ident = read_json_pin_ident(pin, where)
    return doc, norm, raw


def _keys(doc, required, where, optional=()):
    if not isinstance(doc, dict):
        raise Refused('INPUT_SHAPE', '%s must be an object' % where)
    missing = sorted(k for k in required if k not in doc)
    if missing:
        raise Refused('INPUT_KEY_MISSING', '%s: %s' % (where, missing))
    extra = sorted(k for k in doc if k not in required and k not in optional)
    if extra:
        raise Refused('INPUT_KEY_UNKNOWN', '%s: %s' % (where, extra))


def _under(directory_real, file_real):
    try:
        return file_real != directory_real and os.path.commonpath([directory_real, file_real]) == directory_real
    except ValueError:
        return False


def write_exclusive(path, data):
    with open(path, 'xb') as f:
        f.write(data)


def own_pin():
    real = os.path.realpath(__file__)
    with open(real, 'rb') as f:
        return {'path': real, 'sha256': sha256_hex(f.read())}


def load_freeze_module(pin):
    """Execute the pinned freeze module from its verified bytes (no bytecode is written)."""
    raw, norm = read_bytes_pin(pin, 'freeze_module')
    mod = types.ModuleType('freeze_module_' + norm['sha256'][:16])
    mod.__file__ = norm['path']
    exec(compile(raw, norm['path'], 'exec'), mod.__dict__)
    return mod


# --------------------------------------------------------------------------------------------------------------
# time (machine-written stamps: `date -u` output or ISO-8601 UTC)
# --------------------------------------------------------------------------------------------------------------

def parse_utc_ns(s, where):
    """Return integer nanoseconds since the epoch. Accepts YYYY-MM-DDTHH:MM:SS[.f]Z or `date -u` output."""
    if not isinstance(s, str):
        raise Refused('TIME_UNPARSEABLE', where)
    m = ISO_RE.match(s)
    if m:
        y, mo, d, h, mi, se, frac = m.groups()
        try:
            dt = datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(se), tzinfo=datetime.timezone.utc)
        except ValueError:
            raise Refused('TIME_UNPARSEABLE', where)
        ns = int((frac or '0').ljust(9, '0'))
    else:
        try:
            dt = datetime.datetime.strptime(s.strip(), '%a %b %d %H:%M:%S UTC %Y').replace(
                tzinfo=datetime.timezone.utc)
        except ValueError:
            raise Refused('TIME_UNPARSEABLE', where)
        ns = 0
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = dt - epoch
    return (delta.days * 86400 + delta.seconds) * 10 ** 9 + ns


def format_utc_ns(ns):
    sec, frac = divmod(ns, 10 ** 9)
    dt = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=sec)
    base = dt.strftime('%Y-%m-%dT%H:%M:%S')
    return base + ('.%09d' % frac).rstrip('0') + 'Z' if frac else base + 'Z'


# --------------------------------------------------------------------------------------------------------------
# V006 bytes: full-sha tokens and the heading that first pins each
# --------------------------------------------------------------------------------------------------------------

def v006_index(raw):
    text = raw.decode('utf-8', errors='strict').lower()
    first_heading = {}
    heading = 'PREAMBLE'
    for line in text.split('\n'):
        if line.startswith('## '):
            heading = line[3:].strip()
        for tok in HEX64_RE.findall(line):
            first_heading.setdefault(tok, heading)
    return first_heading


def _original_headings(raw):
    """Map a lowercased heading back to its original spelling (for reporting)."""
    out = {}
    for line in raw.decode('utf-8').split('\n'):
        if line.startswith('## '):
            out.setdefault(line[3:].strip().lower(), line[3:].strip())
    return out


# --------------------------------------------------------------------------------------------------------------
# validation helpers shared by the commands
# --------------------------------------------------------------------------------------------------------------

def _theta_ok(theta, where):
    if not isinstance(theta, dict) or not theta:
        raise Refused('THETA_INVALID', where)
    for k, v in theta.items():
        if not isinstance(k, str) or not k or type(v) is not float or not math.isfinite(v):
            raise Refused('THETA_NOT_EXACT_FLOAT', '%s: every theta value must be a finite JSON float' % where)
    return theta


def _value_free_members(doc, ids, where):
    """A budget-0 evaluate_envelopes output carries exact member thetas and no NGC value."""
    if not isinstance(doc, dict) or doc.get('ok') is not True or doc.get('budget') != 0 or \
            doc.get('evaluations_used') != 0 or doc.get('query_ids') != ids:
        raise Refused('PLAN_OUTPUT_NOT_BUDGET0', where)
    members = doc.get('members')
    if not isinstance(members, list) or not members:
        raise Refused('PLAN_OUTPUT_NO_MEMBERS', where)
    out = []
    for m in members:
        if not isinstance(m, dict):
            raise Refused('PLAN_OUTPUT_MEMBER_SHAPE', where)
        speeds, rv, regs = m.get('speeds_km_s'), m.get('row_valid'), m.get('row_registration')
        if m.get('evaluated') is not False or m.get('forward_valid_flag') is not None or \
                m.get('member_valid') is not False or \
                not isinstance(speeds, list) or len(speeds) != len(ids) or any(x is not None for x in speeds) or \
                not isinstance(rv, list) or len(rv) != len(ids) or any(x is not False for x in rv) or \
                not isinstance(regs, list) or len(regs) != len(ids) or any(x is not None for x in regs):
            raise Refused('PLAN_OUTPUT_NOT_VALUE_FREE', where)
        if not isinstance(m.get('member_id'), str) or type(m.get('log_index')) is not int:
            raise Refused('PLAN_OUTPUT_MEMBER_SHAPE', where)
        out.append((m['member_id'], m['log_index'], m.get('role'), _theta_ok(m.get('theta_ngc'), where)))
    if len(set(x[0] for x in out)) != len(out):
        raise Refused('PLAN_OUTPUT_MEMBER_SHAPE', where + ': duplicate member_id')
    return out


# the whitelist of a saved value-free sensitivity plan (RUNBOOK step 2b; c2v002 replaces c2v001's blacklist)
SENS_PLAN_TOP_KEYS = ('ok', 'status', 'stage', 'budget', 'evaluations_used', 'reference_member_id',
                      'null_direction_rule', 'evaluations', 'per_query', 'per_target', 'label',
                      'row_registration_roster', 'reasons', 'value_free_plan')
SENS_PLAN_ENTRY_KEYS = ('entry_id', 'kind', 'target', 'side', 'displacement', 'displacement_units', 'limited_by',
                        'u_displaced', 'theta_ngc', 'skipped_zero_displacement', 'linearised_ddo_shift_sigma',
                        'evaluated', 'forward_valid_flag', 'row_valid', 'speeds_km_s', 'row_registration',
                        'delta_from_reference_km_s', 'reasons', 'exception')


def _value_free_sensitivity(doc, ids, where):
    """A saved budget-0 evaluate_sensitivity plan: whitelisted keys only, exact thetas, no NGC value."""
    if not isinstance(doc, dict) or doc.get('ok') is not True or doc.get('budget') != 0 or \
            doc.get('evaluations_used') != 0:
        raise Refused('SENSITIVITY_PLAN_NOT_BUDGET0', where)
    extra = sorted(k for k in doc if k not in SENS_PLAN_TOP_KEYS)
    if extra or doc.get('per_query') != [] or doc.get('per_target') != []:
        raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE',
                      where + ': save only the whitelisted keys, with per_query and per_target empty (RUNBOOK '
                              'step 2b; the pass command writes this form)')
    ev = doc.get('evaluations')
    if not isinstance(ev, list):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where)
    out = []
    for e in ev:
        if not isinstance(e, dict) or any(k not in SENS_PLAN_ENTRY_KEYS for k in e):
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', where + ': an entry carries a key outside the whitelist')
        if e.get('evaluated') is not False or e.get('forward_valid_flag') is not None or \
                e.get('exception') is not None or \
                any(x is not None for x in e.get('speeds_km_s', [0])) or \
                any(x is not None for x in e.get('delta_from_reference_km_s', [0])) or \
                any(x is not False for x in e.get('row_valid', [True])) or \
                any(x is not None for x in e.get('row_registration', [0])):
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', where)
        if not isinstance(e.get('entry_id'), str) or type(e.get('skipped_zero_displacement')) is not bool:
            raise Refused('SENSITIVITY_PLAN_SHAPE', where)
        out.append((e['entry_id'], _theta_ok(e.get('theta_ngc'), where), e['skipped_zero_displacement']))
    if len(set(x[0] for x in out)) != len(out):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where + ': duplicate entry_id')
    return out


def value_free_sensitivity_plan(sens, n_ids):
    """Extract the whitelisted value-free plan from an in-memory budget-0 evaluate_sensitivity output."""
    if not isinstance(sens, dict) or sens.get('ok') is not True or sens.get('budget') != 0 or \
            sens.get('evaluations_used') != 0:
        raise Refused('SENSITIVITY_PLAN_NOT_BUDGET0', 'only a budget-0 sensitivity output is a plan')
    top = {k: sens.get(k) for k in SENS_PLAN_TOP_KEYS if k not in ('evaluations', 'per_query', 'per_target',
                                                                   'value_free_plan')}
    entries = []
    for e in sens.get('evaluations', []):
        if e.get('evaluated') is not False:
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', 'an evaluated entry in a budget-0 plan')
        x = {k: e.get(k) for k in SENS_PLAN_ENTRY_KEYS}
        x.update({'forward_valid_flag': None, 'row_valid': [False] * n_ids, 'speeds_km_s': [None] * n_ids,
                  'row_registration': [None] * n_ids, 'delta_from_reference_km_s': [None] * n_ids,
                  'exception': None})
        entries.append(x)
    top.update({'evaluations': entries, 'per_query': [], 'per_target': [], 'value_free_plan': SENS_PLAN_SCHEMA_NOTE})
    _value_free_sensitivity(top, None, 'value-free sensitivity plan (self-check)')
    return top


def _gate_doc_ok(gd, ids, where, fm):
    try:
        fm._root_target_screen(gd, where)
    except ValueError:
        raise Refused('GATE_TARGET_FIELDS_REFUSED', where)
    if gd.get('schema') != GATE_SCHEMA or gd.get('registration_status') != 'REGISTERED':
        raise Refused('GATE_REGISTRATION_REQUIRED', where)
    for key in ('registered_reasons', 'query_ids'):
        v = gd.get(key)
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v) or \
                len(set(v)) != len(v):
            raise Refused('GATE_EXACT_STRING_LIST_REQUIRED', '%s.%s' % (where, key))
    if any(q not in ids for q in gd['query_ids']):
        raise Refused('GATE_UNKNOWN_QUERY', where)
    if any(r in BUILTIN_REASONS for r in gd['registered_reasons']):
        raise Refused('GATE_BUILTIN_REASON_MUST_DERIVE_FROM_RULE', where)


def _cut_doc_ok(cd, where, fm):
    try:
        fm._root_target_screen(cd, where)
    except ValueError:
        raise Refused('CUT_RECORD_TARGET_FIELDS_REFUSED', where)
    if cd.get('schema') != CUT_SCHEMA or cd.get('confinement_status') != 'CERTIFIED_UNCONFINED' or \
            not isinstance(cd.get('classification_evidence'), dict) or not cd['classification_evidence']:
        raise Refused('CUT_RECORD_NOT_REGISTERED_SCHEMA', where)
    r = cd.get('first_unconfined_R_kpc')
    if isinstance(r, bool) or not isinstance(r, (int, float)) or not math.isfinite(float(r)) or r <= 0:
        raise Refused('CUT_RECORD_RADIUS_INVALID', where)


# --------------------------------------------------------------------------------------------------------------
# receipts and rule (c)
# --------------------------------------------------------------------------------------------------------------

RULE_C_TEXT = ('A133 3 (c), step-5 NGC call: "rerun the identical spec with the RSS cap at RAM and the wall cap '
               'doubled. It is marked invalid only after two identical deterministic failures that are not INFRA, '
               'with no other NGC process running." "There is never a deadline-based abandonment." A141 L1: an '
               'OUTPUT_CAP stop is rerun with the output cap raised.')


def _receipt_cfg(rk, classes):
    _keys(rk, RECEIPT_KEY_ROLES, 'receipt_keys')
    vals = [rk[r] for r in RECEIPT_KEY_ROLES]
    if not all(isinstance(v, str) and v for v in vals) or len(set(vals)) != len(vals):
        raise Refused('RECEIPT_KEYS', 'each role names one distinct non-empty receipt key')
    if not isinstance(classes, dict) or not classes or not all(v in CLASSES for v in classes.values()):
        raise Refused('RECEIPT_STATUS_CLASSES', 'each raw status maps to one of %s' % list(CLASSES))
    return {'keys': dict(rk), 'classes': dict(classes)}


def _receipt(pin, cfg, where):
    doc, norm, _, ident = read_json_pin_ident(pin, where)
    if not isinstance(doc, dict):
        raise Refused('RECEIPT_SHAPE', where)
    raw_status = doc.get(cfg['keys']['status'])
    if not isinstance(raw_status, str) or raw_status not in cfg['classes']:
        raise Refused('RECEIPT_STATUS_UNMAPPED', where)
    t = parse_utc_ns(doc.get(cfg['keys']['time_utc']), where)
    evidence = {r: doc.get(cfg['keys'][r]) for r in EVIDENCE_ROLES}
    binding = {r: doc.get(cfg['keys'][r]) for r in BINDING_ROLES}
    return norm, raw_status, cfg['classes'][raw_status], t, evidence, binding, ident


def _launch_registry(pin, phase):
    """The pinned step-5 launch registry (G27, proposed schema): one entry per launched call, with the call's exact
    theta key and the spec sha registered at launch (A135 item 9). Returns {(alternative, kind, key): entry}."""
    reg, norm, _ = read_json_pin(pin, 'launch_registry')
    _keys(reg, ('schema', 'phase', 'calls'), 'launch_registry')
    if reg['schema'] != LAUNCH_REGISTRY_SCHEMA:
        raise Refused('LAUNCH_REGISTRY_SCHEMA', 'schema must be ' + LAUNCH_REGISTRY_SCHEMA)
    if reg['phase'] != phase:
        raise Refused('LAUNCH_REGISTRY_PHASE', 'the registry is of %r; the build is %s' % (reg['phase'], phase))
    if not isinstance(reg['calls'], list):
        raise Refused('LAUNCH_REGISTRY_SHAPE', 'calls must be a list')
    entries, spec_of_call = {}, {}
    for i, e in enumerate(reg['calls']):
        w = 'launch_registry.calls[%d]' % i
        _keys(e, LAUNCH_REGISTRY_ENTRY_KEYS, w)
        if e['kind'] not in LAUNCH_KINDS or not isinstance(e['key'], str) or not e['key'] or \
                not _is_hex64(e['theta_sha256']) or not _is_hex64(e['spec_sha256']):
            raise Refused('LAUNCH_REGISTRY_SHAPE', w)
        if e['kind'] == 'OTHER':
            if e['alternative'] is not None:
                raise Refused('LAUNCH_REGISTRY_SHAPE', w + ': an OTHER call names no alternative')
        elif not isinstance(e['alternative'], str) or not e['alternative']:
            raise Refused('LAUNCH_REGISTRY_SHAPE', w + ': a roster call names its alternative')
        k = (e['alternative'], e['kind'], e['key'])
        if k in entries:
            raise Refused('LAUNCH_REGISTRY_DUPLICATE', w)
        entries[k] = e
        if e['kind'] != 'OTHER':
            ck = (e['alternative'], e['theta_sha256'])
            if spec_of_call.setdefault(ck, e['spec_sha256']) != e['spec_sha256']:
                raise Refused('LAUNCH_REGISTRY_CONFLICT', '%s: one call (alternative, exact theta) is registered with '
                                                          'two spec shas' % w)
    return entries, norm


def _pos_int(v):
    return type(v) is int and v > 0


def _evidence_problem(ev, need_output_cap):
    if not _is_hex64(ev.get('spec_sha256')):
        return 'spec_sha256'
    for k in ('rss_cap_bytes', 'host_ram_bytes'):
        if not _pos_int(ev.get(k)):
            return k
    w = ev.get('wall_cap_s')
    if isinstance(w, bool) or not isinstance(w, (int, float)) or not math.isfinite(w) or w <= 0:
        return 'wall_cap_s'
    o = ev.get('other_ngc_processes_max')
    if type(o) is not int or o < 0:
        return 'other_ngc_processes_max'
    if need_output_cap and not _pos_int(ev.get('output_cap_bytes')):
        return 'output_cap_bytes'
    return None


def _rule_c_problem(prefix):
    """None when the last two attempts of `prefix` are a rule-(c) terminal pair (FAILED, CAP or OUTPUT_CAP); else
    (code, detail). Only the attempts up to and including the pair are read (R1: a later attempt never decides
    whether an earlier pair was terminal).

    Mechanizes A133 3 (c) for a step-5 NGC call: two identical (same raw status) non-INFRA failures, the identical
    spec on every evidenced attempt, both counted attempts with no other NGC process running, and the counted rerun
    (the last attempt) with the RSS cap at host RAM and the wall cap at twice the call's first attempt (A141 L1: an
    OUTPUT_CAP rerun also has the output cap raised above the first attempt's)."""
    i = len(prefix) - 1
    cur = prefix[i]
    if i == 0:
        return ('RULE_C_INCOMPLETE', 'one failure; rule (c) reruns it (A133 3 (c), (f))')
    prev = prefix[i - 1]
    if prev['class'] != cur['class'] or prev['raw'] != cur['raw']:
        return ('RULE_C_INCOMPLETE', 'the last two attempts are not two identical non-INFRA failures (A133 3 (c))')
    need_out = cur['class'] == 'OUTPUT_CAP'
    for j in sorted({0, i - 1, i}):
        p = _evidence_problem(prefix[j]['evidence'], need_out)
        if p:
            return ('RULE_C_EVIDENCE_MISSING', 'attempt %d receipt lacks valid %s (G25)' % (j, p))
    specs = {canonical_bytes(s['evidence'].get('spec_sha256')) for s in prefix
             if s['evidence'].get('spec_sha256') is not None}
    if len(specs) != 1:
        return ('RULE_C_SPEC_NOT_IDENTICAL', 'rule (c) reruns the identical spec')
    if prev['evidence']['other_ngc_processes_max'] != 0 or cur['evidence']['other_ngc_processes_max'] != 0:
        return ('RULE_C_NOT_SOLO', 'both counted failures must run with no other NGC process running')
    first, ev = prefix[0]['evidence'], cur['evidence']
    if ev['rss_cap_bytes'] != ev['host_ram_bytes']:
        return ('RULE_C_RERUN_CAPS', 'the rerun RSS cap is not at RAM')
    if ev['wall_cap_s'] != 2 * first['wall_cap_s']:
        return ('RULE_C_RERUN_CAPS', 'the rerun wall cap is not twice the first attempt\'s')
    if need_out and not ev['output_cap_bytes'] > first['output_cap_bytes']:
        return ('RULE_C_RERUN_CAPS', 'the OUTPUT_CAP rerun did not raise the output cap (A141 L1)')
    return None


def _terminal(attempts, cfg, where, allow_planned, binding):
    """The terminal attempt of one call under rule (c). binding: {'theta_sha256', 'spec_sha256'} of this call (the
    launch registry entry); every receipt of the call must carry exactly these (R2)."""
    if not isinstance(attempts, list) or not attempts:
        raise Refused('CALL_ATTEMPTS_REQUIRED', where)
    seen, run_dirs, receipt_paths, receipt_shas = [], [], set(), set()
    for i, a in enumerate(attempts):
        w = '%s.attempts[%d]' % (where, i)
        _keys(a, ('run_dir', 'receipt'), w)
        if not isinstance(a['run_dir'], str) or not os.path.isabs(a['run_dir']) or not os.path.isdir(a['run_dir']):
            raise Refused('RUN_DIR_INVALID', w)
        run_real = os.path.realpath(a['run_dir'])
        if run_real in run_dirs:
            raise Refused('ATTEMPT_RUN_DIR_REPEATED', '%s: one run directory (by realpath) serves two attempts' % w)
        if any(_under(d, run_real) or _under(run_real, d) for d in run_dirs):
            raise Refused('ATTEMPT_RUN_DIR_NESTED', '%s: attempt run directories must be disjoint' % w)
        norm, raw_status, cls, t, evidence, rbind, ident = _receipt(a['receipt'], cfg, w + '.receipt')
        if norm['path'] in receipt_paths or norm['sha256'] in receipt_shas:
            raise Refused('ATTEMPT_RECEIPT_REPEATED', '%s: one receipt (by realpath or sha256) serves two attempts' % w)
        if not _under(run_real, norm['path']):
            raise Refused('RECEIPT_NOT_IN_RUN_DIR', w)
        if seen and t <= seen[-1]['time_ns']:
            raise Refused('ATTEMPT_ORDER', '%s: receipt times must strictly increase' % w)
        run_dirs.append(run_real)
        receipt_paths.add(norm['path'])
        receipt_shas.add(norm['sha256'])
        seen.append({'run_dir': run_real, 'receipt': norm, 'raw': raw_status, 'class': cls, 'time_ns': t,
                     'evidence': evidence, 'binding': rbind, 'ident': ident})
    # R1: the call is terminal at the first terminal prefix; each pair is judged on its own prefix only, so a later
    # attempt (of any spec) can never un-terminate an earlier pair and re-roll the call
    for i in range(len(seen) - 1):
        c = seen[i]['class']
        if c in ('FINISHED', 'PLANNED_STOP') or (c in FAILURE_CLASSES and _rule_c_problem(seen[:i + 1]) is None):
            raise Refused('ATTEMPT_AFTER_TERMINAL', '%s.attempts[%d]: the call was already terminal at attempt %d; '
                                                    'a later attempt would re-roll it' % (where, i + 1, i))
    # R1: one call, one spec ("rerun the identical spec"): its attempts carry at most one spec_sha256
    specs = {canonical_bytes(s['evidence']['spec_sha256']) for s in seen if s['evidence']['spec_sha256'] is not None}
    if len(specs) > 1:
        raise Refused('RULE_C_SPEC_NOT_IDENTICAL', '%s: the attempts carry more than one spec_sha256; rule (c) '
                                                   'reruns the identical spec' % where)
    # R2: every receipt is bound to this call (exact-theta key, then the spec sha the launch registry records)
    for i, s in enumerate(seen):
        for role, code in (('theta_sha256', 'RECEIPT_THETA_NOT_OF_CALL'), ('spec_sha256', 'RECEIPT_SPEC_NOT_REGISTERED')):
            v = s['binding'].get(role)
            if v is None:
                raise Refused('RECEIPT_CALL_BINDING_MISSING', '%s.attempts[%d]: the receipt carries no %s (G27)'
                              % (where, i, role))
            if v != binding[role]:
                raise Refused(code, '%s.attempts[%d]: the receipt\'s %s is not this call\'s' % (where, i, role))
    last = seen[-1]
    if last['class'] == 'INFRA':
        raise Refused('CALL_NOT_TERMINAL', where + ': the last attempt is INFRA; rule (c) retries it')
    if last['class'] == 'PLANNED_STOP' and not allow_planned:
        raise Refused('PLANNED_STOP_NOT_A_MEMBER_TERMINAL', where)
    rule_c = None
    if last['class'] in FAILURE_CLASSES:
        p = _rule_c_problem(seen)
        if p:
            raise Refused(p[0], '%s: %s' % (where, p[1]))
        n = len(seen)
        rule_c = {'counted_attempts': [n - 2, n - 1], 'raw_status': last['raw'],
                  'spec_sha256': last['evidence']['spec_sha256'],
                  'other_ngc_processes_max': [seen[-2]['evidence']['other_ngc_processes_max'],
                                              last['evidence']['other_ngc_processes_max']],
                  'first_wall_cap_s': seen[0]['evidence']['wall_cap_s'],
                  'rerun_wall_cap_s': last['evidence']['wall_cap_s'],
                  'rerun_rss_cap_bytes': last['evidence']['rss_cap_bytes'],
                  'host_ram_bytes': last['evidence']['host_ram_bytes']}
        if last['class'] == 'OUTPUT_CAP':
            rule_c.update({'first_output_cap_bytes': seen[0]['evidence']['output_cap_bytes'],
                           'rerun_output_cap_bytes': last['evidence']['output_cap_bytes']})
    return {'class': last['class'], 'raw_status': last['raw'], 'time_ns': last['time_ns'],
            'run_dir': last['run_dir'], 'receipt': last['receipt'], 'n_attempts': len(seen),
            'receipt_paths': [s['receipt']['path'] for s in seen],
            'receipt_shas': [s['receipt']['sha256'] for s in seen],
            'receipt_idents': [s['ident'] for s in seen], 'run_dirs': [s['run_dir'] for s in seen],
            'rule_c': rule_c}


def _cross_call_receipts(idents):
    """R2: one receipt (by realpath, by file identity (st_dev, st_ino) or by sha256) serves one call. idents:
    [(call identity, terminal)], where a call is (alternative, exact theta) for a roster call (A133: an equal theta
    is the same call) or the label of an OTHER call. c2v004 adds the file identity (a hard link)."""
    by_path, by_ino, by_sha = {}, {}, {}
    for ident, term in idents:
        for p, fi, s in zip(term['receipt_paths'], term['receipt_idents'], term['receipt_shas']):
            for owners, k, how in ((by_path, p, 'realpath'), (by_ino, fi, 'file identity (st_dev, st_ino)'),
                                   (by_sha, s, 'sha256')):
                if owners.setdefault(k, ident) != ident:
                    raise Refused('RECEIPT_REUSED_ACROSS_CALLS', 'one receipt (by %s) serves %s and %s'
                                  % (how, list(owners[k]), list(ident)))


# c2v005: the run files of a call are, for a roster call, its receipts, its result and its cut record, and, for an
# OTHER call, its receipts (other_phase_calls carry no result or cut record). Every one of them is identified across
# the calls by realpath and file identity. Content (sha256) is one call's only for the result of a FINISHED call
# (C38); cut records may be byte-identical across calls and are bound to their call by residence (root ruling G29)


def _roster_call_files(rec):
    """[(role, realpath, (st_dev, st_ino), sha256, finished_result)] of one roster call record: its receipts, result
    and cut record. finished_result: the file is the result of a FINISHED call, whose sha256 may belong to this call
    only (C38)."""
    t = rec['terminal']
    out = [('receipt', p, fi, s, False)
           for p, fi, s in zip(t['receipt_paths'], t['receipt_idents'], t['receipt_shas'])]
    if rec['result'] is not None:
        out.append(('result', rec['result']['path'], rec['result_ident'], rec['result']['sha256'],
                    t['class'] == 'FINISHED'))
    if rec['cut'] is not None:
        out.append(('cut_record', rec['cut']['path'], rec['cut_ident'], rec['cut']['sha256'], False))
    return out


def _other_call_files(term):
    """The run files of one OTHER call (other_phase_calls): its receipts."""
    return [('receipt', p, fi, s, False)
            for p, fi, s in zip(term['receipt_paths'], term['receipt_idents'], term['receipt_shas'])]


def _borrow_code(role_a, role_b):
    return 'CUT_RECORD_BORROWED' if 'cut_record' in (role_a, role_b) else 'FILE_BORROWED'


def _cross_call_files(calls):
    """RI45-11 ("never reuse another point's file"), c2v005: one run file serves one call. calls: [(call identity,
    files)] for every call of the build input, roster calls (alternative, exact theta) and OTHER calls (label), with
    files as _roster_call_files / _other_call_files give them. Refuses
      - when a file of one call is, by realpath or by file identity (st_dev, st_ino; a hard link), a file of another
        call, whatever the two roles (receipt, result, cut record); and
      - when the result of a FINISHED call has the sha256 of another call's cut record or result (C38; a byte copy),
        checked over all pairs of calls, so the outcome does not depend on the order of the calls.
    CUT_RECORD_BORROWED when either file is a cut record, else FILE_BORROWED. Byte-identical cut records of distinct
    calls pass, and so do byte-identical failure records of FAILED calls (G29). Receipt-to-receipt reuse (realpath,
    file identity, sha256) is refused before this, by _cross_call_receipts."""
    by_path, by_ino, by_sha = {}, {}, {}
    for ident, files in calls:
        for role, p, fi, s, finished in files:
            for owners, k, how in ((by_path, p, 'realpath'), (by_ino, fi, 'file identity (st_dev, st_ino)')):
                owner = owners.setdefault(k, (ident, role))
                if owner[0] != ident:
                    raise Refused(_borrow_code(role, owner[1]),
                                  'one run file (by %s) serves two calls: the %s of %s is the %s of %s '
                                  '(RI45-11: never reuse another point\'s file)'
                                  % (how, role, list(ident), owner[1], list(owner[0])))
            if role != 'receipt':
                by_sha.setdefault(s, []).append((ident, role, finished))
    for s, entries in by_sha.items():
        for i, (ident, role, finished) in enumerate(entries):
            for o_ident, o_role, o_finished in entries[:i]:
                if o_ident != ident and (finished or o_finished):
                    raise Refused(_borrow_code(role, o_role),
                                  'one run file content (by sha256) serves two calls: the %s of %s has the bytes of '
                                  'the %s of %s, and one of the two is a FINISHED call\'s result (a byte copy; '
                                  'RI45-11; C38)' % (role, list(ident), o_role, list(o_ident)))


def _cut_record_residence(calls):
    """G29 (c2v005): a cut record is bound to its call by residence. It lies inside its own call's terminal run
    directory (checked per call: CUT_RECORD_NOT_OF_ITS_CALL) and inside no run directory (of any attempt) of any
    other call of the build input, roster or OTHER (CUT_RECORD_IN_OTHER_CALL_RUN_DIR). calls: [(call identity,
    terminal, cut pin or None)]."""
    dirs = [(ident, d) for ident, term, _cut in calls for d in term['run_dirs']]
    for ident, _term, cut in calls:
        if cut is None:
            continue
        for o_ident, d in dirs:
            if o_ident != ident and _under(d, cut['path']):
                raise Refused('CUT_RECORD_IN_OTHER_CALL_RUN_DIR',
                              'the cut record of %s lies inside a run directory of %s (G29: a cut record is bound to '
                              'its call by residence)' % (list(ident), list(o_ident)))


# --------------------------------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------------------------------

STAGE_KEYS = {
    'PLAN': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest'),
    'MEMBERS': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest', 'plan_outputs', 'calls',
                'gate_cutoff', 'gate_documents', 'receipt_keys', 'receipt_status_classes', 'launch_registry'),
    'FULL': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest', 'plan_outputs', 'calls',
             'gate_cutoff', 'gate_documents', 'receipt_keys', 'receipt_status_classes', 'launch_registry',
             'sensitivity_plan_output', 'members_stage_rosters', 'members_stage_build_record', 'm15',
             'other_phase_calls', 'step7_ledger_root'),
}


def _roster_doc(scope, alt, slots_pin, qm_pin, mapping, gates, contexts):
    return {'schema': ROSTER_SCHEMA, 'scope': scope, 'alternative': alt, 'slots': slots_pin,
            'query_manifest': qm_pin, 'query_mapping': mapping, 'root_gates': gates,
            'outer_cut': ({'mode': 'PER_THETA', 'contexts': contexts} if contexts else {'mode': 'NONE'})}


def _build_record_of(pin, where, stage=None, phase=None):
    """A BUILT build record of this builder (by sha256), optionally of a given stage and phase."""
    rec, norm, _ = read_json_pin(pin, where)
    if not isinstance(rec, dict) or rec.get('schema') != BUILD_RECORD_SCHEMA or rec.get('status') != 'BUILT':
        raise Refused('BUILD_RECORD_NOT_BUILT', where)
    b = rec.get('builder')
    if not isinstance(b, dict) or b.get('sha256') != own_pin()['sha256']:
        raise Refused('BUILD_RECORD_OTHER_BUILDER', '%s: built by another builder version' % where)
    outs = rec.get('outputs')
    if not isinstance(outs, dict) or not _is_hex64(outs.get('REPLAY_PLAN.json')) or \
            not _is_hex64(outs.get('ROSTER_PINS.json')):
        raise Refused('BUILD_RECORD_SHAPE', where)
    if (stage is not None and rec.get('stage') != stage) or (phase is not None and rec.get('phase') != phase):
        raise Refused('BUILD_RECORD_STAGE', '%s: %s/%s required' % (where, phase, stage))
    return rec, norm


def _assemble(doc, fm, out_real):
    phase, stage = doc['phase'], doc['stage']
    slots, slots_pin, _ = read_json_pin(doc['slots'], 'slots')
    try:
        alts = slots['alternatives']
        declared, primary = alts['declared'], alts['primary']
        rows = slots['query_block']['rows']
    except (KeyError, TypeError):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared/primary and query_block.rows are required')
    if not isinstance(declared, list) or not declared or not all(isinstance(a, dict) for a in declared):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared')
    names = [a.get('name') for a in declared]
    if not all(isinstance(n, str) and ALT_NAME_RE.match(n) for n in names) or len(set(names)) != len(names):
        raise Refused('SLOTS_ALTERNATIVE_NAMES', 'names must be unique file-safe strings')
    if any(a.get('status') not in (ALT_EVALUATED, ALT_NOT_EVALUATED) for a in declared):
        raise Refused('SLOTS_ALTERNATIVE_STATUS', 'every status is EVALUATED_ or NOT_EVALUATED_BEFORE_FREEZE')
    by_name = {a['name']: a for a in declared}
    if primary not in by_name or by_name[primary]['status'] != ALT_EVALUATED:
        raise Refused('SLOTS_PRIMARY', 'the primary must be declared EVALUATED_BEFORE_FREEZE')
    _qraw, qm_pin = read_bytes_pin(doc['query_manifest'], 'query_manifest')
    qm = fm.load_query_manifest(path=qm_pin['path'], expected_sha256=qm_pin['sha256'])
    if not isinstance(qm, dict) or not qm.get('ok'):
        raise Refused('QUERY_MANIFEST_REFUSED', 'load_query_manifest did not accept the pinned manifest')
    ids = list(qm['query_ids'])
    if len(ids) != 43 or not isinstance(rows, list) or len(rows) != 43:
        raise Refused('QUERY_COUNT', '43 query ids and 43 slots query rows are required')
    scope = 'PROGRAM' if qm_pin['sha256'] == fm.PROGRAM_QUERY_MANIFEST_SHA256 else 'SYNTHETIC_FIXTURE'
    mapping = [{'query_id': q, 'slots_query_id': s.get('query_id') if isinstance(s, dict) else None}
               for q, s in zip(ids, rows)]
    if scope == 'PROGRAM' and any(m['query_id'] != m['slots_query_id'] for m in mapping):
        raise Refused('PROGRAM_QUERY_ID_MISMATCH', 'program scope requires equal query ids')
    evaluated = [n for n in names if by_name[n]['status'] == ALT_EVALUATED]
    if phase == 'PHASE_1' and STAGE0_NAME in evaluated:
        raise Refused('PHASE1_STAGE0_NOT_IN_PHASE_1', 'Phase 1 runs under slots in which STAGE0 is not evaluated')
    run_alts = [primary] if phase == 'PHASE_1' else list(evaluated)
    roster_files = {n: 'ROSTER_%s.json' % n for n in names}
    files = {}
    checks = []

    def roster_pins_of(roster_bytes):
        return {n: {'path': os.path.join(out_real, roster_files[n]), 'sha256': sha256_hex(roster_bytes[n])}
                for n in names}

    if stage == 'PLAN':
        roster_bytes = {n: dump_bytes(_roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, [], []))
                        for n in names}
        for n in names:
            files[roster_files[n]] = roster_bytes[n]
            checks.append((n, roster_files[n], []))
        files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': 'PLAN', 'phase': phase,
                                                'row_registration_rosters': roster_pins_of(roster_bytes)})
        return files, checks, ids

    # ---------------- MEMBERS / FULL ----------------
    cfg = _receipt_cfg(doc['receipt_keys'], doc['receipt_status_classes'])
    registry, registry_pin = _launch_registry(doc['launch_registry'], phase)
    used_entries = set()

    # gates: pinned in the phase's cutoff V006 bytes, never chosen here
    gc = doc['gate_cutoff']
    _keys(gc, ('kind', 'v006_copy'), 'gate_cutoff')
    if gc['kind'] != CUTOFF_KIND[phase]:
        raise Refused('GATE_CUTOFF_KIND', 'phase %s requires cutoff %s' % (phase, CUTOFF_KIND[phase]))
    cut_raw, cutoff_pin = read_bytes_pin(gc['v006_copy'], 'gate_cutoff.v006_copy')
    cutoff_heads = v006_index(cut_raw)
    head_names = _original_headings(cut_raw)
    if not isinstance(doc['gate_documents'], list):
        raise Refused('GATE_LIST_REQUIRED', 'gate_documents must be a list (possibly empty)')
    gate_pins, pairs, gate_seen = [], set(), set()
    for i, gp in enumerate(doc['gate_documents']):
        w = 'gate_documents[%d]' % i
        gd, gnorm, _ = read_json_pin(gp, w)
        if gnorm['sha256'] in gate_seen:
            raise Refused('GATE_DUPLICATE', w)
        gate_seen.add(gnorm['sha256'])
        _gate_doc_ok(gd, ids, w, fm)
        if gnorm['sha256'] not in cutoff_heads:
            raise Refused('GATE_NOT_PINNED_IN_CUTOFF_V006',
                          '%s: its full sha256 is not in the phase cutoff V006 bytes; it is not a builder input' % w)
        for q in gd['query_ids']:
            for r in gd['registered_reasons']:
                if (q, r) in pairs:
                    raise Refused('GATE_AMBIGUOUS', '%s: (%s, %s) is listed twice' % (w, q, r))
                pairs.add((q, r))
        gate_pins.append(gnorm)
    gate_pins.sort(key=lambda p: (p['sha256'], p['path']))

    # exact thetas from the value-free plan outputs
    po = doc['plan_outputs']
    if not isinstance(po, dict) or set(po) != set(evaluated):
        raise Refused('PLAN_OUTPUTS_SET', 'one budget-0 evaluate_envelopes output per EVALUATED alternative')
    plan_members, plan_out_pins = {}, {}
    for n in evaluated:
        pdoc, pnorm, _ = read_json_pin(po[n], 'plan_outputs.' + n)
        plan_members[n] = _value_free_members(pdoc, ids, 'plan_outputs.' + n)
        plan_out_pins[n] = pnorm
    ref_list = [(m[0], m[1], m[2]) for m in plan_members[primary]]
    for n in evaluated:
        if [(m[0], m[1], m[2]) for m in plan_members[n]] != ref_list:
            raise Refused('PLAN_MEMBER_LISTS_DIFFER', n + ': every evaluated alternative has the PRIMARY members (D2)')
    sens_entries = []
    sens_pin = None
    if stage == 'FULL':
        spo = doc['sensitivity_plan_output']
        if phase == 'PHASE_1':
            if spo is not None:
                raise Refused('PHASE1_SENSITIVITY_NOT_RUN', 'Phase 1 runs sensitivity at budget 0 (A133 1.4)')
        else:
            if spo is None:
                raise Refused('SENSITIVITY_PLAN_REQUIRED', 'Phase-2 FULL needs the budget-0 sensitivity plan')
            sdoc, sens_pin, _ = read_json_pin(spo, 'sensitivity_plan_output')
            sens_entries = _value_free_sensitivity(sdoc, ids, 'sensitivity_plan_output')
    if stage == 'MEMBERS' and phase == 'PHASE_1':
        raise Refused('PHASE1_STAGE', 'Phase 1 builds FULL directly (no sensitivity calls exist in Phase 1)')

    # calls: rule (c) terminal receipts, rule (f) caps, run-produced cut records
    if not isinstance(doc['calls'], list):
        raise Refused('CALLS_REQUIRED', 'calls must be a list')
    member_theta = {(n, m[0]): m[3] for n in evaluated for m in plan_members[n]}
    sens_theta = {e[0]: e[1] for e in sens_entries if not e[2]}
    resolved = {}
    for i, c in enumerate(doc['calls']):
        w = 'calls[%d]' % i
        if not isinstance(c, dict):
            raise Refused('CALL_SHAPE', w)
        if 'cut_record' not in c:
            raise Refused('CUT_CONTEXT_MISSING',
                          '%s: every evaluated call carries its own cut record pin or an explicit null' % w)
        _keys(c, ('alternative', 'kind', 'key', 'attempts', 'result', 'cut_record'), w)
        alt, kind, key = c['alternative'], c['kind'], c['key']
        if alt not in run_alts:
            raise Refused('CALL_NOT_REGISTERED_FOR_PHASE', '%s: %r is not run in %s' % (w, alt, phase))
        if kind == 'MEMBER':
            if (alt, key) not in member_theta:
                raise Refused('CALL_NOT_A_PLANNED_MEMBER', w)
            theta = member_theta[(alt, key)]
        elif kind == 'SENSITIVITY':
            if phase != 'PHASE_2' or stage != 'FULL' or alt != primary or key not in sens_theta:
                raise Refused('CALL_NOT_A_PLANNED_SENSITIVITY_ENTRY', w)
            theta = sens_theta[key]
        else:
            raise Refused('CALL_KIND', w)
        if (alt, kind, key) in resolved:
            raise Refused('CALL_DUPLICATE', w)
        entry = registry.get((alt, kind, key))
        if entry is None:
            raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no entry for %s %s %s'
                          % (w, alt, kind, key))
        if entry['theta_sha256'] != theta_sha256(theta):
            raise Refused('LAUNCH_REGISTRY_THETA_MISMATCH', '%s: the registry\'s theta key is not the call\'s exact '
                                                            'theta (PLAN output)' % w)
        used_entries.add((alt, kind, key))
        term = _terminal(c['attempts'], cfg, w, allow_planned=False,
                         binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256']})
        result, result_ident = None, None
        if c['result'] is not None:
            # hashed, never parsed (no value is read); its file identity is kept for the cross-call check (c2v004/5)
            _rraw, result, result_ident = read_bytes_pin_ident(c['result'], w + '.result')
            if not _under(term['run_dir'], result['path']):
                raise Refused('RESULT_NOT_OF_ITS_CALL', '%s: the result lies outside the terminal run dir' % w)
        if term['class'] == 'FINISHED' and result is None:
            raise Refused('FINISHED_WITHOUT_RESULT', w)
        cut, cut_ident = None, None
        if c['cut_record'] is not None:
            cd, cut, _, cut_ident = read_json_pin_ident(c['cut_record'], w + '.cut_record')
            if not _under(term['run_dir'], cut['path']):
                raise Refused('CUT_RECORD_NOT_OF_ITS_CALL', '%s: the cut record lies outside its call\'s terminal run '
                                                            'dir (G29: bound to its call by residence)' % w)
            _cut_doc_ok(cd, w + '.cut_record', fm)
        disposition = DISPOSITION_OF[term['class']]
        rec = {'alternative': alt, 'kind': kind, 'key': key, 'theta': theta, 'theta_sha256': theta_sha256(theta),
               'terminal': term, 'result': result, 'cut': cut, 'disposition': disposition,
               'result_ident': result_ident, 'cut_ident': cut_ident,
               'signature': canonical_bytes([c['attempts'], c['result'], c['cut_record']])}
        if fm._canonical_bytes(theta) != canonical_bytes(theta):
            raise Refused('CANONICAL_FORM_DIVERGES', w)
        resolved[(alt, kind, key)] = rec
    # the phase's non-roster NGC calls (F points, the identity twin): FULL only; bound to the registry like any call
    others = []
    if stage == 'FULL':
        oc_list = doc['other_phase_calls']
        if not isinstance(oc_list, list):
            raise Refused('OTHER_PHASE_CALLS', 'a list (possibly empty) of non-roster NGC calls of the phase')
        labels = set()
        for i, oc in enumerate(oc_list):
            w = 'other_phase_calls[%d]' % i
            _keys(oc, ('label', 'attempts'), w)
            if not isinstance(oc['label'], str) or not oc['label'] or oc['label'] in labels:
                raise Refused('OTHER_CALL_LABEL', w)
            labels.add(oc['label'])
            entry = registry.get((None, 'OTHER', oc['label']))
            if entry is None:
                raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no OTHER entry %r'
                              % (w, oc['label']))
            used_entries.add((None, 'OTHER', oc['label']))
            term = _terminal(oc['attempts'], cfg, w, allow_planned=True,
                             binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256']})
            others.append({'label': oc['label'], 'terminal': term})
    unused = sorted('%s:%s:%s' % k for k in registry if k not in used_entries)
    if unused:
        raise Refused('LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL', 'registry entries with no call record in this build '
                                                            'input: %s' % unused[:5])
    # one call per (alternative, exact theta); identical call records only (A133: an equal theta is the same call)
    by_theta = {}
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in by_theta and by_theta[k]['signature'] != rec['signature']:
            raise Refused('CONTEXT_CONFLICT', '%s: two different call records at one exact theta' % rec['alternative'])
        by_theta.setdefault(k, rec)
    # R2: one receipt serves one call, across every roster and non-roster call of this build input
    _cross_call_receipts([(('CALL', k[0], k[1]), rec['terminal']) for k, rec in sorted(by_theta.items())] +
                         [(('OTHER', o['label']), o['terminal']) for o in others])
    # c2v005: one run file (by realpath or file identity) serves one call, across every roster AND OTHER call of this
    # build input; one FINISHED-result content (by sha256) serves one call (C38)
    _cross_call_files([(('CALL', k[0], k[1]), _roster_call_files(rec)) for k, rec in sorted(by_theta.items())] +
                      [(('OTHER', o['label']), _other_call_files(o['terminal'])) for o in others])
    # c2v005 (G29): a cut record lies in no run directory of another call (its own terminal run directory was checked
    # per call above)
    _cut_record_residence([(('CALL', k[0], k[1]), rec['terminal'], rec['cut']) for k, rec in sorted(by_theta.items())]
                          + [(('OTHER', o['label']), o['terminal'], None) for o in others])
    # completeness: every call the phase registers has a terminal receipt before step 4
    for n in run_alts:
        for m in plan_members[n]:
            if (n, 'MEMBER', m[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', '%s %s has no terminal call record' % (n, m[0]))
    if phase == 'PHASE_2' and stage == 'FULL':
        for e in sens_entries:
            if not e[2] and (primary, 'SENSITIVITY', e[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', 'sensitivity %s has no terminal call record' % e[0])

    # contexts (members in member order, then sensitivity entries in plan order; equal thetas once)
    contexts = {n: [] for n in names}
    ctx_theta = {n: [] for n in names}
    for n in run_alts:
        seen = set()
        order = [resolved[(n, 'MEMBER', m[0])] for m in plan_members[n]]
        if n == primary and stage == 'FULL' and phase == 'PHASE_2':
            order += [resolved[(n, 'SENSITIVITY', e[0])] for e in sens_entries if not e[2]]
        for rec in order:
            if rec['disposition'] not in EVALUATED_DISPOSITIONS or rec['theta_sha256'] in seen:
                continue
            seen.add(rec['theta_sha256'])
            contexts[n].append({'theta_ngc': rec['theta'], 'cut': rec['cut']})
            ctx_theta[n].append(rec['theta'])
    roster_docs = {n: _roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, list(gate_pins), contexts[n])
                   for n in names}
    roster_bytes = {n: dump_bytes(roster_docs[n]) for n in names}
    for n in names:
        files[roster_files[n]] = roster_bytes[n]
        checks.append((n, roster_files[n], ctx_theta[n]))
    rpins = roster_pins_of(roster_bytes)
    files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': stage, 'phase': phase,
                                            'row_registration_rosters': rpins})

    # Phase-2 FULL: member contexts byte-identical to the MEMBERS stage (the step-7 D1 check holds by construction),
    # and the MEMBERS-stage build record binds the pass-one replay plan (step 7 checks pass one against it)
    pass_one_sha = {n: rpins[n]['sha256'] for n in names}
    pass_one_members_plan = None
    if stage == 'FULL':
        msr, mbr = doc['members_stage_rosters'], doc['members_stage_build_record']
        if phase == 'PHASE_1':
            if msr is not None or mbr is not None:
                raise Refused('PHASE1_STAGE', 'Phase 1 has no MEMBERS-stage rosters or build record')
        else:
            if not isinstance(msr, dict) or set(msr) != set(names):
                raise Refused('MEMBERS_STAGE_ROSTERS_REQUIRED', 'one MEMBERS-stage roster pin per alternative')
            mrec, mrnorm = _build_record_of(mbr, 'members_stage_build_record', 'MEMBERS', 'PHASE_2')
            for n in names:
                if not isinstance(msr[n], dict) or mrec['outputs'].get(roster_files[n]) != msr[n].get('sha256'):
                    raise Refused('MEMBERS_STAGE_ROSTERS_NOT_OF_RECORD', n)
            mplan, mpnorm, _ = read_json_pin(
                {'path': os.path.join(os.path.dirname(mrnorm['path']), 'REPLAY_PLAN.json'),
                 'sha256': mrec['outputs']['REPLAY_PLAN.json']}, 'members-stage REPLAY_PLAN.json')
            pass_one_members_plan = {
                'stage': 'MEMBERS', 'build_record_sha256': mrnorm['sha256'],
                'replay_plan_sha256': mpnorm['sha256'],
                'member_budget': {a['name']: a['member_budget'] for a in mplan['alternatives']
                                  if a['slots_status'] == ALT_EVALUATED},
                'sensitivity_budget': mplan['sensitivity']['budget']}
            for n in names:
                mdoc, mnorm, _ = read_json_pin(msr[n], 'members_stage_rosters.' + n)
                full = roster_docs[n]
                for k in ('schema', 'scope', 'alternative', 'slots', 'query_manifest', 'query_mapping', 'root_gates'):
                    if mdoc.get(k) != full[k]:
                        raise Refused('MEMBER_CONTEXTS_CHANGED', '%s: %s differs from the MEMBERS stage' % (n, k))
                mc = mdoc.get('outer_cut', {}).get('contexts', []) if isinstance(mdoc.get('outer_cut'), dict) else None
                fc = full['outer_cut'].get('contexts', [])
                if mc is None or len(mc) > len(fc) or \
                        any(canonical_bytes(a) != canonical_bytes(b) for a, b in zip(mc, fc)):
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member contexts must be byte-identical')
                n_member_ctx = sum(1 for _ in contexts_member_prefix(resolved, plan_members, n))
                if len(mc) != n_member_ctx:
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member context count differs')
                pass_one_sha[n] = mnorm['sha256']

    # replay plan (rules (b), (c), (f))
    alt_plan, replay_index = [], {}
    for n in names:
        a = {'name': n, 'slots_status': by_name[n]['status'], 'run_in_phase': n in run_alts,
             'mode': roster_docs[n]['outer_cut']['mode'], 'member_budget': None, 'members': []}
        if n in evaluated:
            budget = None
            for idx, m in enumerate(plan_members[n]):
                if n in run_alts:
                    rec = resolved[(n, 'MEMBER', m[0])]
                    own, cls, nat = rec['disposition'], rec['terminal']['class'], rec['terminal']['n_attempts']
                    rule_c = rec['terminal']['rule_c']
                else:
                    own, cls, nat, rule_c = 'NOT_RUN_PHASE1_BUDGET0', None, 0, None
                if budget is None and own not in EVALUATED_DISPOSITIONS:
                    budget = idx
                a['members'].append({'member_id': m[0], 'log_index': m[1], 'theta_sha256': theta_sha256(m[3]),
                                     'own_disposition': own, 'terminal_class': cls, 'n_attempts': nat,
                                     'rule_c': rule_c})
            a['member_budget'] = len(plan_members[n]) if budget is None else budget
            _effective(a)
        alt_plan.append(a)
        if n in run_alts:
            idx_entries, seen = [], {}
            for rec in resolved.values():
                if rec['alternative'] != n:
                    continue
                key = rec['theta_sha256']
                if key in seen:
                    seen[key]['call_keys'].append('%s:%s' % (rec['kind'], rec['key']))
                    seen[key]['call_keys'].sort()
                    continue
                e = {'theta_sha256': key, 'call_keys': ['%s:%s' % (rec['kind'], rec['key'])],
                     'disposition': rec['disposition'], 'result': rec['result']}
                seen[key] = e
                idx_entries.append(e)
            idx_entries.sort(key=lambda e: e['theta_sha256'])
            replay_index[n] = idx_entries
    if phase == 'PHASE_1' or stage == 'MEMBERS':
        sens = {'budget': 0, 'entries': [],
                'budget_rule': ('Phase 1: budget 0 (A133 1.4 and 1.6 step 5)' if phase == 'PHASE_1' else
                                'Phase-2 pass one: budget 0 (the plan exists only after D1; RUNBOOK step 2b)')}
    else:
        entries, budget, stopped = [], 0, False
        for e in sens_entries:
            if e[2]:
                entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': True,
                                'own_disposition': 'SKIPPED_ZERO_DISPLACEMENT', 'effective_disposition':
                                'SKIPPED_ZERO_DISPLACEMENT'})
                continue
            own = resolved[(primary, 'SENSITIVITY', e[0])]['disposition']
            if not stopped and own in EVALUATED_DISPOSITIONS:
                budget += 1
                eff = own
            elif not stopped:
                eff, stopped = own, True
            else:
                eff = 'UNEVALUATED_BY_ORDER_TRUNCATION' if own in EVALUATED_DISPOSITIONS else own
            entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': False,
                            'own_disposition': own, 'effective_disposition': eff})
        sens = {'budget': budget, 'entries': entries, 'plan_output': sens_pin,
                'budget_rule': SENS_BUDGET_RULE}
    pass_one = None
    if stage == 'FULL':
        pass_one = pass_one_members_plan or {
            'stage': 'FULL', 'build_record_sha256': None, 'replay_plan_sha256': None,
            'member_budget': {a['name']: a['member_budget'] for a in alt_plan if a['slots_status'] == ALT_EVALUATED},
            'sensitivity_budget': sens['budget'],
            'note': 'Phase 1: pass one runs under this build\'s own (chain-root) replay plan; null shas mean that plan'}
    plan = {'schema': REPLAY_PLAN_SCHEMA, 'builder': BUILDER_NAME, 'phase': phase, 'stage': stage,
            'primary': primary, 'predecessor_sha256': None,
            'registered_roster_sha256': {n: rpins[n]['sha256'] for n in names},
            'pass_one_roster_sha256': pass_one_sha, 'pass_one': pass_one,
            'plan_outputs': plan_out_pins, 'launch_registry': registry_pin, 'alternatives': alt_plan,
            'sensitivity': sens, 'replay_index': replay_index, 'rules': RULE_TEXT, 'step4': None,
            'stage0_status': None}

    if stage == 'FULL':
        report = _gate_status_list(doc['m15'], gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names,
                                   cfg)
        files['GATE_STATUS_REPORT.json'] = dump_bytes(report)
        files['GATE_STATUS_LIST.json'] = dump_bytes(a_gate_status_list(report))
        plan['step4'] = _step4(phase, resolved, others)
        plan['stage0_status'] = _stage0_status(phase, by_name, resolved, plan['step4'])
    files['REPLAY_PLAN.json'] = dump_bytes(plan)
    return files, checks, ids


def contexts_member_prefix(resolved, plan_members, n):
    seen = set()
    for m in plan_members.get(n, []):
        rec = resolved.get((n, 'MEMBER', m[0]))
        if rec is None or rec['disposition'] not in EVALUATED_DISPOSITIONS or rec['theta_sha256'] in seen:
            continue
        seen.add(rec['theta_sha256'])
        yield rec


SENS_BUDGET_RULE = ('budget = the number of leading non-skipped plan entries (plan order) whose exact theta has an '
                    'EVALUATED or EVALUATED_FAILED call in the PRIMARY replay index; v003g budgets are prefixes, so '
                    'every later entry is UNEVALUATED_BY_ORDER_TRUNCATION (A133 (b), (f); FREEZE_INCOMPLETE)')
RULE_TEXT = {
    'a': 'rosters come from this builder, from run-produced cut records and gate documents pinned in the phase '
         'cutoff V006 bytes; root pins them unedited (A133 3 (a)). A run file (a receipt, result or cut record of a '
         'roster call; a receipt of an OTHER call) serves one call of the build input, by realpath and by file '
         'identity (st_dev, st_ino); a receipt (among receipts) and a FINISHED call\'s result (against every other '
         'call\'s cut record and result) also by sha256. A cut record is bound to its call by residence: inside its '
         'terminal run directory and inside no run directory of another call; byte-identical cut records of distinct '
         'calls are allowed (RI45-11; c2v005; G29 as ruled)',
    'b': 'a step-7 discrepancy makes that member UNEVALUATED (command step7); no successor roster is ever made; a '
         'pass is admitted only under the BUILD_RECORD replay plan or a step-7 successor verified through the '
         'append-only step-7 ledger at <step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>/ (outside the build '
         'directory; created with its genesis entry by the FULL build), at that plan\'s budgets; a plan with a '
         'NEW_UNEVALUATED successor is never compared again (A133 3 (b))',
    'c': RULE_C_TEXT + ' Mechanized here (G25 names the receipt evidence, G27 the launch registry): a call is '
         'terminal when its last attempt is FINISHED (or PLANNED_STOP for a non-roster call), or when its last two '
         'attempts are FAILED, CAP or OUTPUT_CAP with the identical raw status and the receipts show the identical '
         'spec_sha256 on every evidenced attempt, other_ngc_processes_max 0 on both counted attempts, and on the '
         'counted rerun an RSS cap equal to host RAM and a wall cap equal to twice the first attempt\'s (and, for '
         'OUTPUT_CAP, an output cap above the first attempt\'s). An INFRA last attempt is not terminal. Attempts are '
         'distinct (run directory, receipt path and receipt sha256), disjoint, strictly increasing in receipt time, '
         'and none follows the first terminal prefix (a pair is judged on its own prefix). The attempts of a call '
         'carry one spec_sha256; every receipt carries the call\'s registered spec_sha256 and exact-theta key; one '
         'receipt never serves two calls. The campaign-halt branch of (c) is the DDO campaign\'s, not a roster '
         'call\'s',
    'f': 'a CAP or OUTPUT_CAP terminal leaves the member UNEVALUATED (A133 3 (f)); a FAILED terminal is a v003g '
         'failure record (MEMBER_INVALID)',
    'budget': 'unchanged v003g evaluates members and sensitivity entries in order up to a budget, so an UNEVALUATED '
              'call truncates every later call of its list (UNEVALUATED_BY_ORDER_TRUNCATION; gap G2)',
}


def _effective(a):
    b = a['member_budget']
    for i, m in enumerate(a['members']):
        own = m['own_disposition']
        if i < b:
            m['effective_disposition'] = own
        elif own in EVALUATED_DISPOSITIONS:
            m['effective_disposition'] = 'UNEVALUATED_BY_ORDER_TRUNCATION'
        else:
            m['effective_disposition'] = own


def _gate_status_list(m15, gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names, cfg):
    rosters_of = {}
    for n in names:
        for g in roster_docs[n]['root_gates']:
            rosters_of.setdefault(g['sha256'], []).append(n)
    out = {'schema': GATE_REPORT_SCHEMA, 'builder': BUILDER_NAME,
           'rule': ('M-15 (a)+(1), A142: ON_TIME iff the full gate sha256 occurs in the V006 bytes logged by the '
                    'pre-launch record and the record time is not after the earliest identity-pair launch receipt '
                    '(same second counts as preceding); every other root-listed gate is LATE. The record list is '
                    'checked for consistency and reported per gate; it does not decide the status'),
           'cutoff_v006': cutoff_pin, 'pre_launch_record': None, 'logged_v006': None, 'launch_receipts': [],
           'pre_launch_record_utc': None, 'earliest_launch_receipt_utc': None, 'record_precedes_launch': None,
           'gates': []}
    rec_set, logged_heads, precedes = set(), {}, False
    if m15 is None:
        reason_off = 'NO_PRE_LAUNCH_RECORD'
    else:
        _keys(m15, ('pre_launch_record', 'logged_v006_copy', 'launch_receipts'), 'm15')
        rdoc, rnorm, _ = read_json_pin(m15['pre_launch_record'], 'm15.pre_launch_record')
        _keys(rdoc, ('schema', 'date_u', 'v006_sha256', 'gate_document_sha256s'), 'm15.pre_launch_record')
        if rdoc['schema'] != M15_RECORD_SCHEMA:
            raise Refused('M15_RECORD_SCHEMA', 'pre_launch_record')
        lraw, lnorm = read_bytes_pin(m15['logged_v006_copy'], 'm15.logged_v006_copy')
        if lnorm['sha256'] != rdoc['v006_sha256']:
            raise Refused('M15_LOGGED_V006_MISMATCH', 'the V006 copy is not the bytes the record logs')
        logged_heads = v006_index(lraw)
        gl = rdoc['gate_document_sha256s']
        if not isinstance(gl, list) or not all(_is_hex64(x) for x in gl) or len(set(gl)) != len(gl):
            raise Refused('M15_RECORD_SHAPE', 'gate_document_sha256s')
        if any(x not in logged_heads for x in gl):
            raise Refused('M15_RECORD_INCONSISTENT', 'a recorded gate sha256 is not in the logged V006 bytes')
        rec_set = set(gl)
        rec_t = parse_utc_ns(rdoc['date_u'], 'm15.pre_launch_record.date_u')
        lrs = m15['launch_receipts']
        if not isinstance(lrs, list) or not lrs:
            raise Refused('M15_LAUNCH_RECEIPT_REQUIRED', 'at least the serial identity-pair receipt')
        times = []
        for i, lp in enumerate(lrs):
            ldoc, lpn, _ = read_json_pin(lp, 'm15.launch_receipts[%d]' % i)
            t = parse_utc_ns(ldoc.get(cfg['keys']['time_utc']) if isinstance(ldoc, dict) else None,
                             'm15.launch_receipts[%d]' % i)
            times.append(t)
            out['launch_receipts'].append({'receipt': lpn, 'utc': format_utc_ns(t)})
        earliest = min(times)
        precedes = rec_t <= earliest
        out.update({'pre_launch_record': rnorm, 'logged_v006': lnorm, 'pre_launch_record_utc': format_utc_ns(rec_t),
                    'earliest_launch_receipt_utc': format_utc_ns(earliest), 'record_precedes_launch': precedes})
        reason_off = None
    for g in gate_pins:
        if m15 is None:
            status, reason = 'LATE', reason_off
        elif not precedes:
            status, reason = 'LATE', 'PRE_LAUNCH_RECORD_AFTER_LAUNCH_RECEIPT'
        elif g['sha256'] in logged_heads:
            status, reason = 'ON_TIME', 'PINNED_IN_LOGGED_PRE_LAUNCH_V006'
        else:
            status, reason = 'LATE', 'NOT_PINNED_IN_LOGGED_PRE_LAUNCH_V006'
        head = cutoff_heads.get(g['sha256'])
        out['gates'].append({'gate': g, 'status': status, 'reason': reason,
                             'in_pre_launch_record_list': (g['sha256'] in rec_set) if m15 is not None else None,
                             'pinned_by_entry': head_names.get(head, head),
                             'rosters': sorted(rosters_of.get(g['sha256'], []))})
    return out


def a_gate_status_list(report):
    """The M-15 list in classifier A's GATE_STATUS_LIST_C4V001 schema: exactly {schema, gates}, each exactly
    {gate_sha256, status ON-TIME|LATE, pinned_by_entry}, one per gate document sha256, no repeats; an exact projection
    of the builder's GATE_STATUS_REPORT."""
    gates, seen = [], set()
    for g in report['gates']:
        s = g['gate']['sha256']
        entry = g['pinned_by_entry']
        if s in seen or not isinstance(entry, str) or not entry or g['status'] not in ('ON_TIME', 'LATE'):
            raise Refused('GATE_STATUS_LIST_SELF_CHECK', s)
        seen.add(s)
        gates.append({'gate_sha256': s, 'status': 'ON-TIME' if g['status'] == 'ON_TIME' else 'LATE',
                      'pinned_by_entry': entry})
    out = {'schema': A_GATE_LIST_NAME, 'gates': gates}
    _a_gate_list_problem(out, strict=True)
    return out


def _a_gate_list_problem(gl, strict=False):
    """None when gl is in the GATE_STATUS_LIST_C4V001 schema; else a reason."""
    if not isinstance(gl, dict) or set(gl) != set(A_GATE_LIST_KEYS) or gl['schema'] != A_GATE_LIST_NAME or \
            not isinstance(gl['gates'], list):
        reason = 'not the %s schema (exactly {schema, gates}, schema %s)' % (A_GATE_LIST_NAME, A_GATE_LIST_NAME)
    else:
        reason, seen = None, set()
        for g in gl['gates']:
            if not isinstance(g, dict) or set(g) != set(A_GATE_ENTRY_KEYS) or not _is_hex64(g['gate_sha256']) or \
                    g['status'] not in A_GATE_STATUSES or not isinstance(g['pinned_by_entry'], str) or \
                    not g['pinned_by_entry']:
                reason = 'an entry is not exactly {gate_sha256, status ON-TIME|LATE, pinned_by_entry}'
                break
            if g['gate_sha256'] in seen:
                reason = 'a gate sha256 is listed twice'
                break
            seen.add(g['gate_sha256'])
    if reason and strict:
        raise Refused('GATE_STATUS_LIST_SELF_CHECK', reason)
    return reason


def _step4(phase, resolved, others):
    receipts = []
    seen = set()
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in seen:
            continue
        seen.add(k)
        receipts.append({'label': '%s:%s:%s' % (rec['alternative'], rec['kind'], rec['key']),
                         'class': rec['terminal']['class'], 'utc_ns': rec['terminal']['time_ns']})
    for o in others:
        receipts.append({'label': 'OTHER:' + o['label'], 'class': o['terminal']['class'],
                         'utc_ns': o['terminal']['time_ns']})
    if not receipts:
        raise Refused('STEP4_NO_RECEIPTS', 'no terminal receipt')
    receipts.sort(key=lambda r: (r['utc_ns'], r['label']))
    start = receipts[-1]['utc_ns']
    return {'rule': ('Phase 1: step 4 begins when every Phase-1 NGC call has a terminal receipt (A133 3)'
                     if phase == 'PHASE_1' else
                     'Phase 2: step 4 begins when every registered Phase-2 step-5 call has a terminal or schedule-ceiling '
                     'closure; the start is the latest terminal time including the adopted ceiling, and a '
                     'receipt written at that instant counts as before (A133 3; r3a 6.3)'),
            'start_utc': format_utc_ns(start),
            'receipts': [{'label': r['label'], 'class': r['class'], 'utc': format_utc_ns(r['utc_ns'])}
                         for r in receipts]}


def _stage0_status(phase, by_name, resolved, step4):
    if phase == 'PHASE_1':
        return {'status': ALT_NOT_EVALUATED, 'reasons': ['NOT_IN_PHASE_1'], 'receipts': [],
                'step4_start_utc': step4['start_utc']}
    alt = by_name.get(STAGE0_NAME)
    registered = alt is not None and alt.get('status') == ALT_EVALUATED
    recs = sorted((r for r in resolved.values() if r['alternative'] == STAGE0_NAME), key=lambda r: r['key'])
    reasons = []
    if not registered:
        reasons.append('NO_SEALED_SUCCESSOR')
    if registered and any(r['terminal']['class'] != 'FINISHED' for r in recs):
        reasons.append('STAGE0_RECEIPT_NOT_FINISHED')
    return {'status': ALT_EVALUATED if not reasons else ALT_NOT_EVALUATED, 'reasons': reasons,
            'note': ('EVALUATED_BEFORE_FREEZE here is subject to EVALUATED_REFUSED by the pinned successor at the '
                     'freeze (M-14); a receipt after the step-4 start cannot occur, because the start is the last '
                     'registered receipt'),
            'receipts': [{'member': r['key'], 'class': r['terminal']['class'],
                          'utc': format_utc_ns(r['terminal']['time_ns'])} for r in recs],
            'step4_start_utc': step4['start_utc']}


def build(input_path, input_sha256, out_dir):
    doc, ipin, _ = read_json_pin({'path': input_path, 'sha256': input_sha256}, 'builder input')
    if not isinstance(doc, dict) or doc.get('schema') != INPUT_SCHEMA:
        raise Refused('INPUT_SCHEMA', 'schema must be ' + INPUT_SCHEMA)
    if doc.get('phase') not in PHASES or doc.get('stage') not in STAGES:
        raise Refused('INPUT_PHASE_STAGE', 'phase in %s, stage in %s' % (list(PHASES), list(STAGES)))
    _keys(doc, STAGE_KEYS[doc['stage']], 'builder input')
    fm = load_freeze_module(doc['freeze_module'])
    out_abs = os.path.abspath(out_dir)
    out_real = os.path.join(os.path.realpath(os.path.dirname(out_abs)), os.path.basename(out_abs))
    ledger_root = None
    if doc['stage'] == 'FULL':
        # R3: root fixes the ledger's absolute location; the BUILD_RECORD records it, so its sha256 binds it
        lr = doc['step7_ledger_root']
        if not isinstance(lr, str) or not os.path.isabs(lr) or not os.path.isdir(lr):
            raise Refused('STEP7_LEDGER_ROOT_INVALID', 'step7_ledger_root: an existing absolute directory')
        ledger_root = os.path.realpath(lr)
        if ledger_root == out_real or _under(out_real, ledger_root):
            raise Refused('STEP7_LEDGER_ROOT_INSIDE_BUILD_DIR', 'the ledger lies outside the build directory')
    files1, checks, ids = _assemble(doc, fm, out_real)
    files2, _c2, _i2 = _assemble(doc, fm, out_real)
    if files1 != files2:
        raise Refused('NONDETERMINISTIC_BUILD', 'two in-memory builds differ')
    if ledger_root is not None:
        plan_sha = sha256_hex(files1['REPLAY_PLAN.json'])
        prior = _ledgered_plans(ledger_root).get(plan_sha)
        if prior is not None:
            raise Refused('STEP7_LEDGER_PLAN_ALREADY_LEDGERED', 'this replay plan already has a step-7 ledger under '
                                                                'the ledger root (%s); a rebuild never resets it (R3)'
                          % os.path.basename(prior))
    try:
        os.mkdir(out_abs)
    except FileExistsError:
        raise Refused('OUT_DIR_EXISTS', out_abs)
    for name in sorted(files1):
        write_exclusive(os.path.join(out_abs, name), files1[name])
    # self-check: the pinned freeze module accepts every roster and every evaluated exact theta
    status, failure = 'BUILT', None
    try:
        for n, fname, thetas in checks:
            pin = {'path': os.path.join(out_real, fname), 'sha256': sha256_hex(files1[fname])}
            r = fm._load_row_roster(pin, ids)
            for th in thetas:
                fm._row_contract(r, th)
    except (ValueError, KeyError, TypeError) as exc:
        status, failure = 'REFUSED', 'V003G_SELF_CHECK: %s' % exc
    record = {'schema': BUILD_RECORD_SCHEMA, 'status': status, 'failure': failure, 'builder': own_pin(),
              'input': ipin, 'phase': doc['phase'], 'stage': doc['stage'], 'freeze_module': doc['freeze_module'],
              'outputs': {k: sha256_hex(v) for k, v in sorted(files1.items())},
              'double_run': 'BYTE_EQUAL', 'step7_ledger_root': ledger_root,
              'self_check': 'freeze module _load_row_roster on every roster, _row_contract on every evaluated theta'}
    rec_raw = dump_bytes(record)
    if status == 'BUILT' and ledger_root is not None:
        # R3: the FULL build creates its ledger (genesis entry) at the root-fixed path keyed by this record's sha256
        ldir = ledger_dir_of(record, sha256_hex(rec_raw))
        try:
            os.mkdir(ldir)
        except FileExistsError:
            raise Refused('STEP7_LEDGER_EXISTS', ldir)
        write_exclusive(os.path.join(ldir, LEDGER_GENESIS_NAME),
                        _genesis_bytes(sha256_hex(rec_raw), sha256_hex(files1['REPLAY_PLAN.json'])))
    write_exclusive(os.path.join(out_abs, 'BUILD_RECORD.json'), rec_raw)
    if status != 'BUILT':
        raise Refused('V003G_SELF_CHECK', failure)
    return record


# --------------------------------------------------------------------------------------------------------------
# replay adapter (RUNBOOK step 6), pass records and the in-memory pass driver (steps 2 and 7)
# --------------------------------------------------------------------------------------------------------------

class ReplayNoSavedResult(Exception):
    pass


class ReplayUnknownKey(Exception):
    pass


def make_replay_adapter(replay_plan, alternative, serve_log, context):
    """forward_ngc for v003g: returns only the saved, byte-verified raw result of (alternative, exact theta).

    It never launches a solver, never substitutes another point and never invents a result: a key with no saved
    result raises, and v003g records the exception for that call."""
    index = {e['theta_sha256']: e for e in replay_plan['replay_index'].get(alternative, [])}

    def forward_ngc(theta):
        key = theta_sha256(theta)
        entry = index.get(key)
        if entry is None:
            serve_log.append({'alternative': alternative, 'context': context, 'theta_sha256': key,
                              'outcome': 'UNKNOWN_KEY', 'result': None})
            raise ReplayUnknownKey('no registered call at this exact theta')
        if entry['disposition'] not in EVALUATED_DISPOSITIONS or entry['result'] is None:
            serve_log.append({'alternative': alternative, 'context': context, 'theta_sha256': key,
                              'outcome': 'NO_SAVED_RESULT', 'result': None})
            raise ReplayNoSavedResult('the terminal attempt left no saved result (%s)' % entry['disposition'])
        try:
            raw, norm = read_bytes_pin(entry['result'], 'replay result')
            doc = strict_json(raw, 'replay result')
        except Refused:
            # a registered result whose bytes no longer verify is a custody breach, not a validity outcome; the
            # pass driver refuses the whole pass (PASS_RESULT_CUSTODY_BREACH)
            serve_log.append({'alternative': alternative, 'context': context, 'theta_sha256': key,
                              'outcome': 'RESULT_CUSTODY_BREACH', 'result': entry['result']})
            raise ReplayNoSavedResult('the registered result does not verify from bytes')
        serve_log.append({'alternative': alternative, 'context': context, 'theta_sha256': key,
                          'outcome': 'SERVED', 'result': norm})
        return doc
    return forward_ngc


def _validity(m, served):
    regs = m.get('row_registration') or []
    return {'evaluated': m.get('evaluated'), 'forward_valid_flag': m.get('forward_valid_flag'),
            'member_valid': m.get('member_valid'), 'row_valid': m.get('row_valid'),
            'row_reasons': [r.get('reason') if isinstance(r, dict) else None for r in regs],
            'served': served}


def _served(log_entries, alt, context, key):
    hits = [e for e in log_entries if (alt is None or e['alternative'] == alt) and e['context'] == context and
            e['theta_sha256'] == key]
    outs = {canonical_bytes([e['outcome'], e['result']]) for e in hits}
    if len(outs) > 1:
        raise Refused('PASS_SERVE_LOG_INCONSISTENT', '%s: one theta served two ways' % alt)
    return {'outcome': hits[0]['outcome'], 'result': hits[0]['result']} if hits else None


PASS_BINDING_KEYS = ('phase', 'plan_stage', 'replay_plan_sha256', 'build_record_sha256', 'builder_sha256',
                     'freeze_module_sha256', 'selection_sha256', 'spec_sha256', 'null_direction_rule',
                     'sensitivity_budget_source')


def pass_record(label, envelopes, reference, sensitivity, serve_log, binding):
    """Validity-only record of one pass (no NGC output value). envelopes: {alt: v003g evaluate_envelopes output};
    reference: the select_reference_member output; sensitivity: the evaluate_sensitivity output; serve_log: the
    adapter log; binding: the plan, build record, builder and inputs the pass ran under."""
    if label not in ('PASS_ONE', 'PASS_K'):
        raise Refused('PASS_LABEL', label)
    _keys(binding, PASS_BINDING_KEYS, 'pass binding')
    if not isinstance(serve_log, dict) or serve_log.get('schema') != SERVE_LOG_SCHEMA or \
            not isinstance(serve_log.get('entries'), list):
        raise Refused('SERVE_LOG_SCHEMA', label)
    log_entries = serve_log['entries']
    rec = {'schema': PASS_RECORD_SCHEMA, 'pass_label': label, 'alternatives': {}, 'reference': None,
           'sensitivity': None}
    rec.update(binding)
    for alt in sorted(envelopes):
        ev = envelopes[alt]
        if not isinstance(ev, dict) or ev.get('ok') is not True or not isinstance(ev.get('members'), list):
            raise Refused('PASS_OUTPUT_NOT_OK', alt)
        members = []
        for m in ev['members']:
            key = theta_sha256(m['theta_ngc'])
            served = _served(log_entries, alt, 'ENVELOPES', key) if m.get('evaluated') else None
            if m.get('evaluated') and served is None:
                raise Refused('PASS_SERVE_LOG_INCONSISTENT', '%s %s evaluated but not served' % (alt, m['member_id']))
            v = _validity(m, served)
            v.update({'member_id': m['member_id'], 'log_index': m['log_index'], 'theta_sha256': key})
            members.append(v)
        rec['alternatives'][alt] = {'roster': ev.get('row_registration_roster'), 'status': ev.get('status'),
                                    'budget': ev.get('budget'), 'members': members}
    if not isinstance(reference, dict) or reference.get('ok') is not True:
        raise Refused('PASS_REFERENCE_NOT_OK', label)
    rec['reference'] = {'member_id': reference['member_id'], 'log_index': reference['log_index']}
    if not isinstance(sensitivity, dict) or sensitivity.get('ok') is not True:
        raise Refused('PASS_SENSITIVITY_NOT_OK', label)
    plan, entries = [], []
    for e in sensitivity.get('evaluations', []):
        key = theta_sha256(e['theta_ngc'])
        plan.append({'entry_id': e['entry_id'], 'theta_sha256': key, 'skipped': e['skipped_zero_displacement']})
        served = _served(log_entries, None, 'SENSITIVITY', key) if e.get('evaluated') else None
        if e.get('evaluated') and served is None:
            raise Refused('PASS_SERVE_LOG_INCONSISTENT', 'sensitivity %s evaluated but not served' % e['entry_id'])
        v = _validity(e, served)
        v['entry_id'] = e['entry_id']
        entries.append(v)
    rec['sensitivity'] = {'roster': sensitivity.get('row_registration_roster'),
                          'reference_member_id': sensitivity.get('reference_member_id'),
                          'budget': sensitivity.get('budget'), 'plan': plan, 'entries': entries}
    return rec


def _never(theta):
    raise ReplayUnknownKey('a budget-0 plan call evaluated a point')


PASS_INPUT_KEYS = ('schema', 'pass_label', 'freeze_module', 'build_record', 'replay_plan', 'roster_pins',
                   'selection', 'spec', 'null_direction_rule')


def pass_driver(fm, doc):
    """The in-memory pass (RUNBOOK steps 2 and 7). Returns (validity-only pass record, value-free sensitivity plan or
    None, in-memory outputs). Only the first two may be written; the in-memory outputs exist for an in-process
    caller (the step-8 freeze script, after the seal) and are never written or printed by this tool."""
    _keys(doc, PASS_INPUT_KEYS, 'pass input')
    label = doc['pass_label']
    if label not in ('PASS_ONE', 'PASS_K'):
        raise Refused('PASS_LABEL', repr(label))
    ctx = _plan_context(doc['build_record'], doc['replay_plan'], 'pass')
    plan, rec = ctx['plan'], ctx['record']
    if ctx['superseded']:
        raise Refused('PASS_PLAN_SUPERSEDED', 'this replay plan already has a NEW_UNEVALUATED step-7 successor')
    if not isinstance(doc['freeze_module'], dict) or rec.get('freeze_module') != doc['freeze_module']:
        raise Refused('PASS_FREEZE_MODULE_NOT_OF_BUILD', 'the pass runs the build record\'s freeze module pin')
    phase, stage = plan['phase'], plan['stage']
    if label == 'PASS_ONE':
        if ctx['plan_sha'] != ctx['root_sha']:
            raise Refused('PASS_ONE_UNDER_A_SUCCESSOR', 'pass one runs under the build record\'s own replay plan')
        if (phase == 'PHASE_1' and stage != 'FULL') or (phase == 'PHASE_2' and stage != 'MEMBERS'):
            raise Refused('PASS_ONE_STAGE', 'pass one: Phase 1 FULL, Phase 2 MEMBERS')
    elif stage != 'FULL':
        raise Refused('PASS_K_STAGE', 'pass k runs under a FULL replay plan or its step-7 successor')
    rp_doc, rp_norm, _ = read_json_pin(doc['roster_pins'], 'roster_pins')
    if rp_norm['sha256'] != rec['outputs']['ROSTER_PINS.json']:
        raise Refused('PASS_ROSTER_PINS_NOT_OF_BUILD', 'ROSTER_PINS.json is not the build record\'s')
    pins = rp_doc.get('row_registration_rosters') if isinstance(rp_doc, dict) else None
    if not isinstance(pins, dict) or set(pins) != set(plan['registered_roster_sha256']):
        raise Refused('PASS_ROSTER_PINS_SHAPE', 'one roster pin per alternative')
    for alt, sha in plan['registered_roster_sha256'].items():
        if not isinstance(pins[alt], dict) or pins[alt].get('sha256') != sha:
            raise Refused('PASS_ROSTER_NOT_REGISTERED', alt)
    sel, snorm, _ = read_json_pin(doc['selection'], 'selection')
    spec, spnorm, _ = read_json_pin(doc['spec'], 'spec')
    if not isinstance(sel, dict) or not isinstance(sel.get('points'), list) or not sel['points']:
        raise Refused('PASS_SELECTION_SHAPE', 'the saved select_representative_points output (with its points)')
    primary = plan['primary']
    proster, _pn, _ = read_json_pin(pins[primary], 'primary roster')
    qpin = proster.get('query_manifest') if isinstance(proster, dict) else None
    if not isinstance(qpin, dict):
        raise Refused('PASS_ROSTER_SHAPE', 'primary roster query_manifest')
    qm = fm.load_query_manifest(path=qpin.get('path'), expected_sha256=qpin.get('sha256'))
    if not isinstance(qm, dict) or not qm.get('ok'):
        raise Refused('QUERY_MANIFEST_REFUSED', 'the roster\'s query manifest')
    ids = list(qm['query_ids'])
    log = []
    envs = {}
    for a in plan['alternatives']:
        if a['slots_status'] != ALT_EVALUATED:
            continue
        ev = fm.evaluate_envelopes(forward_ngc=make_replay_adapter(plan, a['name'], log, 'ENVELOPES'),
                                   points=sel['points'], spec=spec, query_ids=ids, budget=a['member_budget'],
                                   row_registration_roster=pins[a['name']])
        if not isinstance(ev, dict) or ev.get('ok') is not True:
            raise Refused('PASS_ENVELOPES_NOT_OK', a['name'])
        envs[a['name']] = ev
    ref = fm.select_reference_member(selection=sel, evaluation=envs[primary])
    if not isinstance(ref, dict) or ref.get('ok') is not True:
        raise Refused('PASS_NO_REFERENCE_MEMBER', 'select_reference_member did not return a reference')
    sb, source = plan['sensitivity']['budget'], 'REPLAY_PLAN'
    if sb is None:
        s0 = fm.evaluate_sensitivity(forward_ngc=_never, reference=ref, selection=sel, spec=spec, query_ids=ids,
                                     null_direction_rule=doc['null_direction_rule'], budget=0,
                                     row_registration_roster=pins[primary])
        if not isinstance(s0, dict) or s0.get('ok') is not True:
            raise Refused('PASS_SENSITIVITY_NOT_OK', 'budget-0 plan')
        entries = [(e['entry_id'], theta_sha256(e['theta_ngc']), e['skipped_zero_displacement'])
                   for e in s0['evaluations']]
        sb, source = _sens_budget_rule(plan, entries)['budget'], 'SENS_BUDGET_RULE'
    sens = fm.evaluate_sensitivity(forward_ngc=make_replay_adapter(plan, primary, log, 'SENSITIVITY'), reference=ref,
                                   selection=sel, spec=spec, query_ids=ids,
                                   null_direction_rule=doc['null_direction_rule'], budget=sb,
                                   row_registration_roster=pins[primary])
    if not isinstance(sens, dict) or sens.get('ok') is not True:
        raise Refused('PASS_SENSITIVITY_NOT_OK', label)
    if any(e['outcome'] == 'RESULT_CUSTODY_BREACH' for e in log):
        raise Refused('PASS_RESULT_CUSTODY_BREACH', 'a registered result no longer verifies from bytes (step 5 '
                                                    'retains them byte-identical); root rules (G16)')
    binding = {'phase': phase, 'plan_stage': stage, 'replay_plan_sha256': ctx['plan_sha'],
               'build_record_sha256': ctx['record_pin']['sha256'], 'builder_sha256': own_pin()['sha256'],
               'freeze_module_sha256': doc['freeze_module']['sha256'], 'selection_sha256': snorm['sha256'],
               'spec_sha256': spnorm['sha256'], 'null_direction_rule': doc['null_direction_rule'],
               'sensitivity_budget_source': source}
    record = pass_record(label, envs, ref, sens, {'schema': SERVE_LOG_SCHEMA, 'entries': log}, binding)
    plan_extract = None
    if label == 'PASS_ONE' and phase == 'PHASE_2':
        plan_extract = value_free_sensitivity_plan(sens, len(ids))
    return record, plan_extract, {'envelopes': envs, 'reference': ref, 'sensitivity': sens}


# --------------------------------------------------------------------------------------------------------------
# step 7 (A133 3 (b)): plan chain, ledger, comparison; the sensitivity budget
# --------------------------------------------------------------------------------------------------------------

VALIDITY_FIELDS = ('evaluated', 'forward_valid_flag', 'member_valid', 'row_valid', 'row_reasons', 'served')


def _sens_budget_rule(replay_plan, plan_entries):
    """plan_entries: [(entry_id, theta_sha256, skipped)] in plan order."""
    index = {e['theta_sha256']: e for e in replay_plan['replay_index'].get(replay_plan['primary'], [])}
    out, budget, stopped = [], 0, False
    for entry_id, key, skipped in plan_entries:
        if skipped:
            out.append({'entry_id': entry_id, 'theta_sha256': key, 'skipped': True, 'disposition': 'SKIPPED'})
            continue
        e = index.get(key)
        ok = not stopped and e is not None and e['disposition'] in EVALUATED_DISPOSITIONS
        if ok:
            budget += 1
            disp = e['disposition']
        else:
            disp = ('NO_SAVED_CALL_AT_THIS_THETA' if e is None else e['disposition']) if not stopped else \
                'UNEVALUATED_BY_ORDER_TRUNCATION'
            stopped = True
        out.append({'entry_id': entry_id, 'theta_sha256': key, 'skipped': False, 'disposition': disp})
    return {'budget': budget, 'entries': out}


def _apply_unevaluated(plan, plan_sha, new):
    """The only change step 7 makes: the members in `new` become UNEVALUATED_STEP7_DISCREPANCY (budget prefix)."""
    new = {(a, m) for a, m in new}
    succ = json.loads(json.dumps(plan))
    for a in succ['alternatives']:
        for m in a['members']:
            if (a['name'], m['member_id']) in new:
                m['own_disposition'] = 'UNEVALUATED_STEP7_DISCREPANCY'
        for e in succ['replay_index'].get(a['name'], []):
            if any((a['name'], k.split(':', 1)[1]) in new for k in e['call_keys'] if k.startswith('MEMBER:')):
                e['disposition'] = 'UNEVALUATED_STEP7_DISCREPANCY'
        if a['member_budget'] is not None:
            b = next((i for i, m in enumerate(a['members']) if m['own_disposition'] not in EVALUATED_DISPOSITIONS),
                     len(a['members']))
            a['member_budget'] = min(a['member_budget'], b)
            _effective(a)
    if succ['phase'] == 'PHASE_2':
        succ['sensitivity'] = {'budget': None, 'entries': [], 'plan_output': None,
                               'budget_rule': SENS_BUDGET_RULE + '; the pass driver recomputes it from the budget-0 '
                                                                 'plan of the pass\'s own D1 (step 7 re-derives it)'}
    succ['predecessor_sha256'] = plan_sha
    return succ


def _pass_budget_checks(p, lab, member_budget, sens_budget):
    for alt, b in sorted(member_budget.items()):
        rec = p['alternatives'][alt]
        if type(rec.get('budget')) is not int or rec['budget'] != b:
            raise Refused('STEP7_PASS_BUDGET_MISMATCH', '%s %s ran at budget %r; the plan says %r'
                          % (lab, alt, rec.get('budget'), b))
        for i, m in enumerate(rec['members']):
            if (i < b) != (m.get('evaluated') is True):
                raise Refused('STEP7_PASS_BUDGET_MISMATCH', '%s %s %s evaluated past or short of the budget'
                              % (lab, alt, m.get('member_id')))
    s = p['sensitivity']
    if type(s.get('budget')) is not int or s['budget'] != sens_budget:
        raise Refused('STEP7_PASS_BUDGET_MISMATCH', '%s sensitivity ran at budget %r; required %r'
                      % (lab, s.get('budget'), sens_budget))
    active = [e for pl, e in zip(s['plan'], s['entries']) if not pl['skipped']]
    if any((i < sens_budget) != (e.get('evaluated') is True) for i, e in enumerate(active)) or \
            any(e.get('evaluated') for pl, e in zip(s['plan'], s['entries']) if pl['skipped']):
        raise Refused('STEP7_PASS_BUDGET_MISMATCH', '%s sensitivity entries evaluated past or short of the budget' % lab)


def _compare(plan, plan_sha, root_sha, build_sha, pass_one, pass_k):
    """Pure step-7 comparison. Returns (status, new_unevaluated, stops, checks); raises Refused on a binding defect."""
    own = own_pin()['sha256']
    if not isinstance(plan, dict) or plan.get('schema') != REPLAY_PLAN_SCHEMA or plan.get('stage') != 'FULL':
        raise Refused('STEP7_REPLAY_PLAN', 'a FULL-stage replay plan (or its step-7 successor) is required')
    for p, lab in ((pass_one, 'PASS_ONE'), (pass_k, 'PASS_K')):
        if not isinstance(p, dict) or p.get('schema') != PASS_RECORD_SCHEMA or p.get('pass_label') != lab:
            raise Refused('STEP7_PASS_RECORD', lab)
        if p.get('builder_sha256') != own:
            raise Refused('STEP7_PASS_OTHER_BUILDER', lab)
        if p.get('phase') != plan['phase']:
            raise Refused('STEP7_PASS_PHASE', lab)
    po = plan['pass_one']
    p1_plan = po['replay_plan_sha256'] or root_sha
    p1_build = po['build_record_sha256'] or build_sha
    if pass_k.get('replay_plan_sha256') != plan_sha or pass_k.get('build_record_sha256') != build_sha:
        raise Refused('STEP7_PASS_NOT_OF_THIS_PLAN', 'PASS_K ran under another replay plan or build record')
    if pass_one.get('replay_plan_sha256') != p1_plan or pass_one.get('build_record_sha256') != p1_build:
        raise Refused('STEP7_PASS_NOT_OF_THIS_PLAN', 'PASS_ONE did not run under the pass-one plan of record')
    reg, p1r = plan['registered_roster_sha256'], plan['pass_one_roster_sha256']
    primary = plan['primary']
    evaluated = [a['name'] for a in plan['alternatives'] if a['slots_status'] == ALT_EVALUATED]
    for p, ref, lab in ((pass_k, reg, 'STEP7_ROSTER_NOT_REGISTERED'), (pass_one, p1r, 'STEP7_PASS_ONE_ROSTER')):
        if sorted(p['alternatives']) != sorted(evaluated):
            raise Refused('STEP7_ALTERNATIVE_SET', p['pass_label'])
        for alt, rec in p['alternatives'].items():
            if not isinstance(rec.get('roster'), dict) or rec['roster'].get('sha256') != ref.get(alt):
                raise Refused(lab, '%s %s ran under a roster that is not the recorded one; a root successor '
                                   'roster is never admitted (A133 3 (b))' % (p['pass_label'], alt))
        sr = p['sensitivity']['roster']
        if not isinstance(sr, dict) or sr.get('sha256') != ref.get(primary):
            raise Refused(lab, p['pass_label'] + ' sensitivity')
    plan_alts = {a['name']: a for a in plan['alternatives']}
    k_budget = {alt: plan_alts[alt]['member_budget'] for alt in evaluated}
    # sensitivity budget of pass k: the plan's, or (successor in Phase 2) re-derived from pass k's own plan entries
    k_plan_entries = [(e['entry_id'], e['theta_sha256'], e['skipped']) for e in pass_k['sensitivity']['plan']]
    if plan['sensitivity']['budget'] is not None:
        k_sens, source = plan['sensitivity']['budget'], 'REPLAY_PLAN'
        if plan['phase'] == 'PHASE_2':
            reg_entries = [(e['entry_id'], e['theta_sha256'], e['skipped']) for e in plan['sensitivity']['entries']]
            if k_plan_entries != reg_entries:
                raise Refused('STEP7_SENSITIVITY_PLAN_NOT_REGISTERED',
                              'PASS_K sensitivity plan is not the registered plan of this replay plan')
    else:
        k_sens, source = _sens_budget_rule(plan, k_plan_entries)['budget'], 'SENS_BUDGET_RULE'
    if pass_k.get('sensitivity_budget_source') != source:
        raise Refused('STEP7_PASS_BUDGET_MISMATCH', 'PASS_K sensitivity budget source')
    _pass_budget_checks(pass_k, 'PASS_K', k_budget, k_sens)
    _pass_budget_checks(pass_one, 'PASS_ONE', {alt: po['member_budget'][alt] for alt in evaluated},
                        po['sensitivity_budget'])
    checks = {'pass_k_member_budget': k_budget, 'pass_k_sensitivity_budget': k_sens,
              'pass_k_sensitivity_budget_source': source,
              'pass_one_member_budget': {alt: po['member_budget'][alt] for alt in evaluated},
              'pass_one_sensitivity_budget': po['sensitivity_budget'],
              'pass_one_replay_plan_sha256': p1_plan}
    stops, new = [], []
    for alt in evaluated:
        pa = plan_alts[alt]
        m1, mk = pass_one['alternatives'][alt]['members'], pass_k['alternatives'][alt]['members']
        ident = [(m['member_id'], m['log_index'], m['theta_sha256']) for m in pa['members']]
        if [(m['member_id'], m['log_index'], m['theta_sha256']) for m in m1] != ident or \
                [(m['member_id'], m['log_index'], m['theta_sha256']) for m in mk] != ident:
            stops.append('STEP7_SELECTION_DIFFERS: ' + alt)
            continue
        for pm, a1, ak in zip(pa['members'], m1, mk):
            if pm['effective_disposition'] not in EVALUATED_DISPOSITIONS:
                continue
            if any(a1[f] != ak[f] for f in VALIDITY_FIELDS):
                new.append((alt, pm['member_id']))
    if not stops and not new:
        r1, rk = pass_one['reference'], pass_k['reference']
        d1 = next((m for m in plan_alts[primary]['members'] if m['member_id'] == r1['member_id']), None)
        if d1 is None:
            stops.append('STEP7_PASS_ONE_D1_NOT_A_PLANNED_MEMBER')
        elif d1['effective_disposition'] in EVALUATED_DISPOSITIONS and r1 != rk:
            stops.append('STEP7_D1_DIFFERS_WITHOUT_MEMBER_DISCREPANCY')
        if r1 == rk and \
                [(e['entry_id'], e['theta_sha256'], e['skipped']) for e in pass_one['sensitivity']['plan']] != \
                k_plan_entries:
            stops.append('STEP7_SENSITIVITY_PLAN_DIFFERS_WITH_EQUAL_D1')
    status = 'STOP_NOT_MECHANIZED' if stops else ('NEW_UNEVALUATED' if new else 'NO_NEW_DISCREPANCY')
    return status, ([] if stops else new), stops, checks


def ledger_dir_of(record, build_sha):
    """R3: the step-7 ledger of a FULL build record: <step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>. It
    depends only on the record's bytes, never on where a copy of the build directory sits. None for PLAN/MEMBERS."""
    if record.get('stage') != 'FULL':
        return None
    root = record.get('step7_ledger_root')
    if not isinstance(root, str) or not os.path.isabs(root):
        raise Refused('BUILD_RECORD_SHAPE', 'a FULL build record names its absolute step7_ledger_root')
    return os.path.join(root, LEDGER_DIR_PREFIX + build_sha)


def _genesis_bytes(build_sha, plan_sha):
    return dump_bytes({'schema': LEDGER_GENESIS_SCHEMA, 'builder': BUILDER_NAME, 'build_record_sha256': build_sha,
                       'replay_plan_sha256': plan_sha,
                       'rule': 'append-only step-7 ledger of this BUILD_RECORD (A133 3 (b)); every entry by exclusive '
                               'create; created by the FULL build; the only ledger of this record and, under this '
                               'ledger root, of this replay plan'})


def _ledgered_plans(ledger_root):
    """{replay_plan_sha256: ledger dir} of every ledger already under the root-fixed ledger root (R3: a rebuild of
    the same plan into a new directory is a new BUILD_RECORD and must not get a second, empty ledger)."""
    out = {}
    for nm in sorted(os.listdir(ledger_root)):
        if not (nm.startswith(LEDGER_DIR_PREFIX) and _is_hex64(nm[len(LEDGER_DIR_PREFIX):])):
            continue
        gp = os.path.join(ledger_root, nm, LEDGER_GENESIS_NAME)
        if not os.path.lexists(gp):
            raise Refused('STEP7_LEDGER_ROOT_UNREADABLE', '%s has no genesis entry' % nm)
        g = strict_json(_read_regular(gp, 'ledger genesis ' + nm)[0], 'ledger genesis ' + nm)
        if not isinstance(g, dict) or not _is_hex64(g.get('replay_plan_sha256')):
            raise Refused('STEP7_LEDGER_ROOT_UNREADABLE', nm)
        out.setdefault(g['replay_plan_sha256'], os.path.join(ledger_root, nm))
    return out


def _ledger_files(ledger_dir, build_sha, plan_sha):
    if not os.path.lexists(ledger_dir):
        raise Refused('STEP7_LEDGER_MISSING', '%s: the FULL build created this ledger; it is absent (R3)' % ledger_dir)
    if os.path.islink(ledger_dir) or not os.path.isdir(ledger_dir):
        raise Refused('STEP7_LEDGER_NOT_A_DIRECTORY', ledger_dir)
    results, plans, passes, genesis = {}, {}, {}, None
    for nm in sorted(os.listdir(ledger_dir)):
        p = os.path.join(ledger_dir, nm)
        if os.path.islink(p):
            raise Refused('STEP7_LEDGER_FOREIGN_FILE', nm)
        m_r, m_pl, m_ps = LEDGER_RESULT_RE.match(nm), LEDGER_PLAN_RE.match(nm), LEDGER_PASS_RE.match(nm)
        if nm == LEDGER_GENESIS_NAME:
            genesis = _read_regular(p, 'ledger ' + nm)[0]
            continue
        if not (m_r or m_pl or m_ps):
            raise Refused('STEP7_LEDGER_FOREIGN_FILE', nm)
        raw, _real = _read_regular(p, 'ledger ' + nm)
        if m_r:
            results[int(m_r.group(1))] = raw
        else:
            sha = (m_pl or m_ps).group(1)
            if sha256_hex(raw) != sha:
                raise Refused('STEP7_LEDGER_BROKEN', '%s: bytes do not hash to its name' % nm)
            (plans if m_pl else passes)[sha] = raw
    if genesis != _genesis_bytes(build_sha, plan_sha):
        raise Refused('STEP7_LEDGER_BROKEN', 'the genesis entry is missing or is not this BUILD_RECORD\'s')
    return results, plans, passes


def _read_ledger(record, build_sha, root_sha, root_raw):
    """Verify the append-only step-7 ledger of this build record (R3: at its root-fixed path keyed by the record's
    sha256) and return the verified plan chain.

    Every result is re-derived: its pass records (stored in the ledger) are compared again under its predecessor
    plan, and each successor plan must equal, byte for byte, what step 7 makes from its predecessor."""
    ledger_dir = ledger_dir_of(record, build_sha)
    out = {'dir': ledger_dir, 'n': 0, 'last_sha': None, 'results': [], 'plans': {root_sha: root_raw},
           'superseded': []}
    if ledger_dir is None:
        return out
    results, plans, passes = _ledger_files(ledger_dir, build_sha, root_sha)
    seqs = sorted(results)
    if seqs != list(range(1, len(seqs) + 1)):
        raise Refused('STEP7_LEDGER_BROKEN', 'result sequence is not 1..n')
    plan_docs = {root_sha: strict_json(root_raw, 'root replay plan')}
    superseded = set()
    prev = None
    for s in seqs:
        raw = results[s]
        r = strict_json(raw, 'ledger result %d' % s)
        try:
            if r.get('schema') != STEP7_RESULT_SCHEMA or r.get('seq') != s or \
                    r.get('previous_result_sha256') != prev or r.get('build_record_sha256') != build_sha:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d header' % s)
            pred = r.get('replay_plan_sha256')
            if pred not in plan_docs or pred in superseded:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d compares a plan outside the chain or superseded' % s)
            p1raw, pkraw = passes.get(r.get('pass_one_sha256')), passes.get(r.get('pass_k_sha256'))
            if p1raw is None or pkraw is None:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d: a pass record copy is missing' % s)
            status, new, stops, checks = _compare(plan_docs[pred], pred, root_sha, build_sha,
                                                  strict_json(p1raw, 'ledger pass'), strict_json(pkraw, 'ledger pass'))
            if status != r.get('status') or [{'alternative': a, 'member_id': m} for a, m in new] != \
                    r.get('new_unevaluated') or stops != r.get('stops') or checks != r.get('checks'):
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d does not re-derive from its stored passes' % s)
            if status == 'NEW_UNEVALUATED':
                succ_raw = dump_bytes(_apply_unevaluated(plan_docs[pred], pred, new))
                ssha = sha256_hex(succ_raw)
                if r.get('successor_replay_plan_sha256') != ssha or plans.get(ssha) != succ_raw:
                    raise Refused('STEP7_LEDGER_BROKEN', 'result %d successor is not step 7\'s own change' % s)
                plan_docs[ssha] = strict_json(succ_raw, 'successor')
                out['plans'][ssha] = succ_raw
                superseded.add(pred)
            elif r.get('successor_replay_plan_sha256') is not None:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d names a successor without NEW_UNEVALUATED' % s)
        except Refused as exc:
            if exc.code == 'STEP7_LEDGER_BROKEN':
                raise
            raise Refused('STEP7_LEDGER_BROKEN', 'result %d: %s' % (s, exc.code))
        out['results'].append(r)
        prev = sha256_hex(raw)
    out.update({'n': len(seqs), 'last_sha': prev, 'superseded': sorted(superseded)})
    return out


def _plan_context(build_record_pin, replay_plan_pin, where):
    rec, rnorm = _build_record_of(build_record_pin, where + ' build_record')
    build_dir = os.path.dirname(rnorm['path'])
    if os.path.lexists(os.path.join(build_dir, STEP7_LEDGER_DIR)):
        raise Refused('STEP7_LEDGER_SECOND_LEDGER', 'a STEP7_LEDGER beside the build record; the only ledger is the '
                                                    'one under the record\'s step7_ledger_root (R3)')
    root_raw, root_norm = read_bytes_pin({'path': os.path.join(build_dir, 'REPLAY_PLAN.json'),
                                          'sha256': rec['outputs']['REPLAY_PLAN.json']}, 'build REPLAY_PLAN.json')
    plan_raw, pnorm = read_bytes_pin(replay_plan_pin, where + ' replay_plan')
    ledger = _read_ledger(rec, rnorm['sha256'], root_norm['sha256'], root_raw)
    if pnorm['sha256'] not in ledger['plans']:
        raise Refused('PLAN_NOT_OF_BUILD_RECORD',
                      'the replay plan is neither the build record\'s REPLAY_PLAN.json nor a step-7 successor '
                      'verified through its step-7 ledger')
    superseded = pnorm['sha256'] in ledger.get('superseded', [])
    return {'record': rec, 'record_pin': rnorm, 'build_dir': build_dir, 'root_sha': root_norm['sha256'],
            'plan': strict_json(plan_raw, 'replay plan'), 'plan_sha': pnorm['sha256'], 'ledger': ledger,
            'superseded': superseded}


def step7_run(build_record_pin, replay_plan_pin, pass_one_pin, pass_k_pin):
    """RUNBOOK step 7. Returns (result, result_bytes, successor_bytes_or_None) and appends to the build record's
    step-7 ledger (<step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>)."""
    ctx = _plan_context(build_record_pin, replay_plan_pin, 'step7')
    if ctx['superseded']:
        raise Refused('STEP7_PLAN_SUPERSEDED', 'this replay plan already has a NEW_UNEVALUATED successor; a later '
                                               'agreeing pass never resolves it (A133 3 (b))')
    p1_raw, p1n = read_bytes_pin(pass_one_pin, 'pass_one')
    pk_raw, pkn = read_bytes_pin(pass_k_pin, 'pass_k')
    build_sha = ctx['record_pin']['sha256']
    status, new, stops, checks = _compare(ctx['plan'], ctx['plan_sha'], ctx['root_sha'], build_sha,
                                          strict_json(p1_raw, 'pass_one'), strict_json(pk_raw, 'pass_k'))
    succ_raw = None
    if status == 'NEW_UNEVALUATED':
        succ_raw = dump_bytes(_apply_unevaluated(ctx['plan'], ctx['plan_sha'], new))
    ledger = ctx['ledger']
    result = {'schema': STEP7_RESULT_SCHEMA, 'builder': BUILDER_NAME, 'seq': ledger['n'] + 1,
              'previous_result_sha256': ledger['last_sha'], 'build_record_sha256': build_sha,
              'replay_plan_sha256': ctx['plan_sha'], 'pass_one_sha256': p1n['sha256'],
              'pass_k_sha256': pkn['sha256'], 'status': status,
              'new_unevaluated': [{'alternative': a, 'member_id': m} for a, m in new], 'stops': stops,
              'checks': checks, 'successor_replay_plan_sha256': sha256_hex(succ_raw) if succ_raw else None,
              'resolution_by_successor_roster': 'NEVER (A133 3 (b))'}
    res_raw = dump_bytes(result)
    d = ledger['dir']
    if d is None:
        raise Refused('STEP7_REPLAY_PLAN', 'step 7 runs under a FULL build record only')
    for raw, sha, kind in ((p1_raw, p1n['sha256'], 'PASS'), (pk_raw, pkn['sha256'], 'PASS'),
                           (succ_raw, result['successor_replay_plan_sha256'], 'PLAN')):
        if raw is None:
            continue
        p = os.path.join(d, '%s_%s.json' % (kind, sha))
        if not os.path.lexists(p):
            write_exclusive(p, raw)
    write_exclusive(os.path.join(d, 'STEP7_%04d.json' % result['seq']), res_raw)   # the commit point
    return result, res_raw, succ_raw


def sensitivity_budget(replay_plan, sens_doc, ids=None):
    if replay_plan.get('schema') != REPLAY_PLAN_SCHEMA:
        raise Refused('SENS_BUDGET_REPLAY_PLAN', 'replay plan schema')
    if replay_plan['phase'] == 'PHASE_1':
        return {'schema': 'SENS_BUDGET_C2V003', 'budget': 0, 'entries': [], 'rule': 'Phase 1: budget 0 (A133 1.4)'}
    entries = _value_free_sensitivity(sens_doc, ids, 'sensitivity plan')
    r = _sens_budget_rule(replay_plan, [(e[0], theta_sha256(e[1]), e[2]) for e in entries])
    return {'schema': 'SENS_BUDGET_C2V003', 'budget': r['budget'], 'entries': r['entries'], 'rule': SENS_BUDGET_RULE}


# --------------------------------------------------------------------------------------------------------------
# M-15 list check, M-6 seal check, M-7 TSR check
# --------------------------------------------------------------------------------------------------------------

def check_gate_list(roster_pins, gate_list_pin, build_record_pin):
    """GATE_STATUS_LIST_DEFECT (r3a 1.1, M-15): the list is in classifier A's GATE_STATUS_LIST_C4V001 schema, every
    root-listed gate of the rosters is on it, and it is, byte for byte, the GATE_STATUS_LIST.json of the FULL build
    whose rosters these are (so no status is edited after the build)."""
    try:
        gl, gnorm, _ = read_json_pin(gate_list_pin, 'gate_status_list')
    except Refused as exc:
        raise Stop('GATE_STATUS_LIST_DEFECT', 'the list is missing or unreadable: ' + exc.code)
    reason = _a_gate_list_problem(gl)
    if reason:
        raise Stop('GATE_STATUS_LIST_DEFECT', reason)
    listed = {g['gate_sha256']: g['status'] for g in gl['gates']}
    if not isinstance(roster_pins, dict) or not roster_pins:
        raise Refused('ROSTER_PINS_REQUIRED', 'the six-entry roster mapping')
    rec, rnorm = _build_record_of(build_record_pin, 'build_record', stage='FULL')
    missing = []
    for alt in sorted(roster_pins):
        if not isinstance(roster_pins[alt], dict) or \
                rec['outputs'].get('ROSTER_%s.json' % alt) != roster_pins[alt].get('sha256'):
            raise Refused('ROSTER_PINS_NOT_OF_BUILD', '%s: not the roster of the FULL build record' % alt)
        rd, _rn, _ = read_json_pin(roster_pins[alt], 'roster ' + alt)
        for g in rd.get('root_gates', []):
            if g.get('sha256') not in listed:
                missing.append('%s:%s' % (alt, g.get('sha256')))
    if missing:
        raise Stop('GATE_STATUS_LIST_DEFECT', 'root-listed gates missing from the list: %s' % missing)
    if rec['outputs'].get('GATE_STATUS_LIST.json') != gnorm['sha256']:
        raise Stop('GATE_STATUS_LIST_DEFECT', 'the list is not the FULL build\'s GATE_STATUS_LIST.json (an edited or '
                                              'foreign list)')
    return {'schema': 'GATE_LIST_CHECK_C2V003', 'verdict': 'PASS', 'n_listed': len(listed),
            'list_schema': A_GATE_LIST_NAME, 'gate_status_list': gnorm, 'build_record': rnorm}


def _manifest_input_files(freeze_manifest_pin, code):
    try:
        md, mnorm, _ = read_json_pin(freeze_manifest_pin, 'freeze manifest')
        have = {(p['path'], p['sha256']) for p in md['pins']['input_files']}
    except (Refused, KeyError, TypeError):
        raise Stop(code, 'freeze manifest input_files unreadable')
    return have, mnorm


def seal_check(v006_pin, objects, freeze_manifest_pin, expected_tsr_sha256=None):
    """SEAL_SHA_MISMATCH (M-6): each sealed object hashes, from bytes, to the sha256 on its own role line of the seal
    entry (format proposed under G17); roles are distinct objects; the seal entry names exactly the supplied roles;
    the sealed TSR flag record is the pinned production record and is in the freeze manifest's input_files."""
    exp_tsr = PRODUCTION_TSR['flag_record_sha256'] if expected_tsr_sha256 is None else expected_tsr_sha256
    raw, vnorm = read_bytes_pin(v006_pin, 'v006_copy')
    if not isinstance(objects, list) or not objects:
        raise Refused('SEAL_OBJECTS_REQUIRED', 'objects')
    roles = {}
    for i, o in enumerate(objects):
        _keys(o, ('role', 'path', 'sha256'), 'objects[%d]' % i)
        if not isinstance(o['role'], str) or not re.match(r'^[A-Z][A-Z0-9_]*$', o['role']) or o['role'] in roles:
            raise Refused('SEAL_ROLE', 'objects[%d]' % i)
        if not isinstance(o['path'], str) or not os.path.isabs(o['path']) or not _is_hex64(o['sha256']):
            raise Refused('SEAL_OBJECT_SHAPE', 'objects[%d]: absolute path and 64-hex sha256' % i)
        roles[o['role']] = o
    missing = [r for r in SEAL_REQUIRED_ROLES if r not in roles]
    if missing:
        raise Stop('SEAL_SHA_MISMATCH', 'no sealed sha256 for %s' % missing)
    shas = [o['sha256'] for o in roles.values()]
    paths = [os.path.realpath(o['path']) for o in roles.values()]
    if len(set(shas)) != len(shas) or len(set(paths)) != len(paths):
        raise Stop('SEAL_SHA_MISMATCH', 'two roles name one sha256 or one file; every sealed role is its own object')
    lines = raw.decode('utf-8').split('\n')
    prereg = roles['PREREG_TEXT']['sha256']
    start = next((i for i, ln in enumerate(lines) if ln.startswith('## ') and SEAL_ENTRY_TOKEN in ln and
                  prereg in ln.lower()), None)
    if start is None:
        raise Stop('SEAL_SHA_MISMATCH', 'no V006 heading carries %s and the sealed text sha256 (M-6, G17)'
                   % SEAL_ENTRY_TOKEN)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    entry = {}
    for ln in lines[start + 1:end]:
        m = SEAL_ROLE_LINE_RE.match(ln)
        if m:
            if m.group(1) in entry:
                raise Stop('SEAL_SHA_MISMATCH', 'the seal entry names role %s twice' % m.group(1))
            entry[m.group(1)] = m.group(2)
    if entry.get('PREREG_TEXT') != prereg:
        raise Stop('SEAL_SHA_MISMATCH', 'the seal entry\'s PREREG_TEXT line is not the heading\'s text sha256')
    if set(entry) != set(roles):
        raise Stop('SEAL_SHA_MISMATCH', 'the seal entry names roles %s; supplied %s'
                   % (sorted(entry), sorted(roles)))
    details, bad = [], []
    for role in sorted(roles):
        o = roles[role]
        try:
            actual = sha256_hex(_read_regular(o['path'], role)[0])
        except Refused:
            actual = None
        ok = entry[role] == o['sha256'] and actual == o['sha256']
        details.append({'role': role, 'path': o['path'], 'sealed_sha256': entry[role],
                        'supplied_sha256': o['sha256'], 'actual_sha256': actual, 'ok': ok})
        if not ok:
            bad.append(role)
    tsr = roles['TSR_FLAG_RECORD']
    tsr_problems = []
    if tsr['sha256'] != exp_tsr:
        tsr_problems.append('SEALED_TSR_FLAG_RECORD_NOT_THE_PINNED_RECORD')
    have, mnorm = _manifest_input_files(freeze_manifest_pin, 'SEAL_SHA_MISMATCH')
    if (os.path.realpath(tsr['path']), tsr['sha256']) not in have:
        tsr_problems.append('FREEZE_INPUT_FILES_LACK_SEALED_TSR_FLAG_RECORD')
    result = {'schema': 'SEAL_CHECK_C2V003', 'v006': vnorm, 'freeze_manifest': mnorm,
              'seal_entry_heading': lines[start][3:].strip(), 'objects': details, 'tsr_problems': tsr_problems,
              'verdict': 'STOP' if bad or tsr_problems else 'PASS',
              'code': 'SEAL_SHA_MISMATCH' if bad or tsr_problems else None}
    if bad or tsr_problems:
        raise Stop('SEAL_SHA_MISMATCH', 'roles %s; %s' % (bad, tsr_problems))
    return result


def tsr_record_v003(v001_pin):
    """ROOT_TSR_FLAG_RECORD_V003: the pinned V001 record projected onto classifier A's TSR_FLAG_RECORD_C4V001
    schema (exactly schema, target_free, rule, failing_ring_ordinal, the three pins and the 43 flags in manifest
    order). Nothing is recomputed: every value is V001's, verbatim; `schema` is the contract name (A173). Returns the
    record bytes."""
    raw, norm = read_bytes_pin(v001_pin, 'flag_record_v001')
    if norm['sha256'] != PRODUCTION_TSR['v001_flag_record_sha256']:
        raise Refused('TSR_V001_NOT_THE_PINNED_RECORD', 'the derivation input is the pinned V001 record only')
    v1 = strict_json(raw, 'flag_record_v001')
    if not isinstance(v1, dict) or v1.get('schema') != TSR_FLAG_SCHEMA or v1.get('rule_id') != TSR_RULE_ID:
        raise Refused('TSR_V001_SCHEMA', 'V001 schema or rule_id')
    try:
        pins = v1['pins']
        rec = {'schema': A_TSR_NAME, 'target_free': True, 'rule': v1['rule'],
               'failing_ring_ordinal': v1['failing_ring']['ordinal'],
               'ntest_compare_pin': {'path': pins['ntest_compare']['path'],
                                     'sha256': pins['ntest_compare']['sha256']},
               'n1_record_pin': {'path': pins['n1_record']['path'], 'sha256': pins['n1_record']['sha256']},
               'gl_node_record_pin': {'path': pins['gl_node_record']['path'],
                                      'sha256': pins['gl_node_record']['sha256']},
               'flags': [{'query_id': f['query_id'], 'TRUNCATION_SHAPE_RESIDUAL': f['TRUNCATION_SHAPE_RESIDUAL']}
                         for f in v1['flags']]}
    except (KeyError, TypeError):
        raise Refused('TSR_V001_SCHEMA', 'V001 lacks a field the projection reads')
    if set(rec) != set(A_TSR_KEYS):
        raise Refused('TSR_RECORD_SELF_CHECK', 'keys')
    return dump_bytes(rec)


def tsr_check(flag_pin, freeze_manifest_pin=None, expected=None):
    """TSR_FLAG_TABLE_MISMATCH (r3a 1.1, M-7): the flag record (classifier A's TSR_FLAG_RECORD_C4V001 schema, by its
    pinned sha256), the compare, N1 and node pins, and the freeze manifest's input_files."""
    exp = PRODUCTION_TSR if expected is None else expected
    problems = []
    try:
        fr, fnorm, _ = read_json_pin(flag_pin, 'tsr flag record')
    except Refused as exc:
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'flag record: ' + exc.code)
    if exp.get('flag_record_sha256') is not None and fnorm['sha256'] != exp['flag_record_sha256']:
        problems.append('FLAG_RECORD_NOT_THE_PINNED_RECORD')
    if not isinstance(fr, dict) or set(fr) != set(A_TSR_KEYS) or fr['schema'] != A_TSR_NAME:
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'the flag record is not in the %s schema (exactly %s, schema %s)'
                   % (A_TSR_NAME, list(A_TSR_KEYS), A_TSR_NAME))
    if fr['target_free'] is not True:
        problems.append('TARGET_FREE_NOT_TRUE')
    if not isinstance(fr['rule'], str) or not fr['rule'] or \
            (exp.get('rule') is not None and fr['rule'] != exp['rule']):
        problems.append('RULE_TEXT')
    if type(fr['failing_ring_ordinal']) is not int or fr['failing_ring_ordinal'] != exp['failing_ordinal']:
        problems.append('FAILING_RING_ORDINAL')
    flags = fr['flags']
    if not isinstance(flags, list) or any(not isinstance(f, dict) or set(f) != set(A_TSR_FLAG_KEYS) for f in flags) \
            or [f['query_id'] for f in flags] != exp['all_ids']:
        problems.append('FLAG_TABLE_IDS')
    elif any(type(f['TRUNCATION_SHAPE_RESIDUAL']) is not bool for f in flags):
        problems.append('FLAG_TABLE_VALUES')
    elif [f['query_id'] for f in flags if f['TRUNCATION_SHAPE_RESIDUAL']] != exp['flagged_ids']:
        problems.append('FLAGGED_SET_NOT_EXACTLY_%s' % exp['flagged_ids'])
    pins, docs = {}, {}
    for key, sk in (('ntest_compare_pin', 'compare_sha256'), ('n1_record_pin', 'n1_sha256'),
                    ('gl_node_record_pin', 'node_sha256')):
        p = fr[key]
        if not isinstance(p, dict) or set(p) != {'path', 'sha256'} or p['sha256'] != exp[sk]:
            problems.append('PIN_%s' % key.upper())
            continue
        pins[key] = p
        try:
            docs[key], _n, _ = read_json_pin(p, key)
        except Refused as exc:
            problems.append('PIN_%s_%s' % (key.upper(), exc.code))
    k = exp['failing_ordinal']
    c = docs.get('ntest_compare_pin')
    ring = None
    if c is not None:
        rings = c.get('failing_TRUNCATION_SHAPE_rings')
        if not isinstance(rings, list) or [r.get('ordinal') for r in rings if isinstance(r, dict)] != [k] or \
                len(rings) != 1:
            problems.append('COMPARE_FAILING_TS_RINGS_NOT_EXACTLY_%d' % k)
        else:
            ring = rings[0]
        if c.get('failing_non_TRUNCATION_SHAPE_rings') != []:
            problems.append('COMPARE_NON_TS_FAILING_RING')
    n1, nd = docs.get('n1_record_pin'), docs.get('gl_node_record_pin')
    if n1 is not None:
        rr = n1.get('ring_radii_kpc')
        if not isinstance(rr, list) or len(rr) <= k + 1 or rr[k - 1] != exp['lower_kpc'] or \
                rr[k + 1] != exp['upper_kpc']:
            problems.append('N1_NEIGHBOUR_RADII')
        elif ring is not None and rr[k] != ring.get('R_kpc'):
            problems.append('N1_RING_RADIUS')
        if nd is not None:
            try:
                if nd['orders']['4']['radii_kpc'] != rr:
                    problems.append('NODE_RADII_NOT_N1')
            except (KeyError, TypeError):
                problems.append('NODE_SHAPE')
    if freeze_manifest_pin is not None:
        have, _mn = _manifest_input_files(freeze_manifest_pin, 'TSR_FLAG_TABLE_MISMATCH')
        want = [('TSR_FLAG_RECORD', fnorm)] + [(k2[:-4].upper(), fr[k2]) for k2 in
                                              ('ntest_compare_pin', 'n1_record_pin', 'gl_node_record_pin')]
        for label, p in want:
            if not isinstance(p, dict) or not isinstance(p.get('path'), str) or \
                    (os.path.realpath(p['path']), p.get('sha256')) not in have:
                problems.append('FREEZE_INPUT_FILES_LACK_' + label)
    result = {'schema': 'TSR_CHECK_C2V003', 'flag_record': fnorm, 'record_schema': A_TSR_NAME, 'problems': problems,
              'verdict': 'STOP' if problems else 'PASS', 'code': 'TSR_FLAG_TABLE_MISMATCH' if problems else None}
    if problems:
        raise Stop('TSR_FLAG_TABLE_MISMATCH', '%s' % problems)
    return result


# --------------------------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------------------------

def _cmd_input(args, schema):
    doc, norm, _ = read_json_pin({'path': os.path.abspath(args['--input']), 'sha256': args['--input-sha256']},
                                 'command input')
    if not isinstance(doc, dict) or doc.get('schema') != schema:
        raise Refused('INPUT_SCHEMA', 'schema must be ' + schema)
    return doc, norm


def _parse_args(argv):
    if not argv:
        raise Refused('USAGE', __doc__.split('\n\n')[1])
    cmd, rest, args = argv[0], argv[1:], {}
    while rest:
        if len(rest) < 2 or not rest[0].startswith('--'):
            raise Refused('USAGE', 'arguments are --name value pairs')
        args[rest[0]] = rest[1]
        rest = rest[2:]
    return cmd, args


COMMANDS = ('build', 'pass', 'step7', 'sens-budget', 'check-gate-list', 'seal-check', 'tsr-record', 'tsr-check')


def _new_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        raise Refused('OUT_DIR_EXISTS', path)


def main(argv):
    cmd, args = None, {}
    try:
        cmd, args = _parse_args(argv)
        if cmd not in COMMANDS:
            raise Refused('USAGE', 'unknown command %r; commands: %s' % (cmd, list(COMMANDS)))
        need = ('--input', '--input-sha256', '--out-dir' if cmd in ('build', 'step7', 'pass') else '--out')
        if set(args) != set(need):
            raise Refused('USAGE', '%s takes exactly %s' % (cmd, list(need)))
        if cmd == 'build':
            rec = build(os.path.abspath(args['--input']), args['--input-sha256'], args['--out-dir'])
            print(json.dumps({'status': rec['status'], 'outputs': rec['outputs']}, sort_keys=True))
            return 0
        if cmd == 'pass':
            d, _ = _cmd_input(args, PASS_INPUT_SCHEMA)
            _keys(d, PASS_INPUT_KEYS, 'pass input')
            fm = load_freeze_module(d['freeze_module'])
            record, extract, _in_memory = pass_driver(fm, d)
            del _in_memory                      # never written, never printed
            _new_dir(args['--out-dir'])
            names = ['PASS_RECORD.json']
            write_exclusive(os.path.join(args['--out-dir'], 'PASS_RECORD.json'), dump_bytes(record))
            if extract is not None:
                names.append('SENSITIVITY_PLAN_VALUE_FREE.json')
                write_exclusive(os.path.join(args['--out-dir'], 'SENSITIVITY_PLAN_VALUE_FREE.json'),
                                dump_bytes(extract))
            print(json.dumps({'status': 'WRITTEN', 'files': names}))
            return 0
        if cmd == 'step7':
            d, _ = _cmd_input(args, 'STEP7_INPUT_C2V003')
            _keys(d, ('schema', 'build_record', 'replay_plan', 'pass_one', 'pass_k'), 'input')
            res, res_raw, succ_raw = step7_run(d['build_record'], d['replay_plan'], d['pass_one'], d['pass_k'])
            _new_dir(args['--out-dir'])
            write_exclusive(os.path.join(args['--out-dir'], 'STEP7_RESULT.json'), res_raw)
            if succ_raw is not None:
                write_exclusive(os.path.join(args['--out-dir'], 'REPLAY_PLAN.json'), succ_raw)
            print(json.dumps({'status': res['status'], 'ledger_seq': res['seq']}))
            return 3 if res['status'] == 'STOP_NOT_MECHANIZED' else 0
        if cmd == 'sens-budget':
            d, _ = _cmd_input(args, 'SENS_BUDGET_INPUT_C2V003')
            _keys(d, ('schema', 'replay_plan', 'sensitivity_plan_output'), 'input')
            plan, pnorm, _ = read_json_pin(d['replay_plan'], 'replay_plan')
            sdoc, snorm, _ = read_json_pin(d['sensitivity_plan_output'], 'sensitivity plan')
            out = sensitivity_budget(plan, sdoc)
            out.update({'replay_plan_sha256': pnorm['sha256'], 'sensitivity_plan_sha256': snorm['sha256']})
        elif cmd == 'check-gate-list':
            d, _ = _cmd_input(args, 'CHECK_GATE_LIST_INPUT_C2V003')
            _keys(d, ('schema', 'roster_pins', 'gate_status_list', 'build_record'), 'input')
            out = check_gate_list(d['roster_pins'], d['gate_status_list'], d['build_record'])
        elif cmd == 'seal-check':
            d, _ = _cmd_input(args, 'SEAL_CHECK_INPUT_C2V003')
            _keys(d, ('schema', 'v006_copy', 'objects', 'freeze_manifest'), 'input')
            out = seal_check(d['v006_copy'], d['objects'], d['freeze_manifest'])
        elif cmd == 'tsr-record':
            d, _ = _cmd_input(args, 'TSR_RECORD_INPUT_C2V003')
            _keys(d, ('schema', 'flag_record_v001'), 'input')
            raw = tsr_record_v003(d['flag_record_v001'])
            write_exclusive(args['--out'], raw)
            print(json.dumps({'status': 'WRITTEN', 'sha256': sha256_hex(raw), 'schema': A_TSR_NAME}))
            return 0
        else:
            d, _ = _cmd_input(args, 'TSR_CHECK_INPUT_C2V003')
            _keys(d, ('schema', 'flag_record', 'freeze_manifest'), 'input')
            out = tsr_check(d['flag_record'], d['freeze_manifest'])
        write_exclusive(args['--out'], dump_bytes(out))
        print(json.dumps({'verdict': out.get('verdict', 'WRITTEN')}))
        return 0
    except Stop as exc:
        print(json.dumps({'stop': exc.code, 'detail': exc.detail}), file=sys.stderr)
        if cmd in ('seal-check', 'tsr-check', 'check-gate-list') and '--out' in args:
            try:
                write_exclusive(args['--out'], dump_bytes({'verdict': 'STOP', 'code': exc.code,
                                                           'detail': exc.detail}))
            except OSError:
                pass
        return 3
    except Refused as exc:
        print(json.dumps({'refused': exc.code, 'detail': exc.detail}), file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        # the pass command handles in-memory NGC outputs: its internal errors print the exception type only
        detail = '' if cmd == 'pass' else str(exc)[:500]
        print(json.dumps({'internal_error': type(exc).__name__, 'detail': detail}), file=sys.stderr)
        return 1





# Component: snapshot_scope_draft002.py
"""c2v007 component: one guarded byte snapshot per immutable file per command.

This component is assembled into the builder after its baseline definitions.
It is not a standalone tool. TESTED status is supplied by the completed suite.
"""

import functools
import contextlib

_ACTIVE_SNAPSHOT = None
_LAST_SNAPSHOT_AUDIT = None


class CommandSnapshot:
    def __init__(self):
        self.paths = {}
        self.identities = {}
        self.reads = {}
        self.requests = {}

    def read(self, path, where, ident_out=None, require_nonempty=True):
        if not isinstance(path, str) or not path:
            raise Refused('PIN_SHAPE', where)
        real = os.path.realpath(path)
        self.requests[real] = self.requests.get(real, 0) + 1
        cached = self.paths.get(real)
        if cached is None:
            try:
                before = os.stat(real)
            except OSError as exc:
                raise Refused('PIN_UNREADABLE', '%s: %s' % (where, type(exc).__name__))
            if not stat.S_ISREG(before.st_mode):
                raise Refused('PIN_NOT_REGULAR_FILE', where)
            identity = (before.st_dev, before.st_ino)
            cached = self.identities.get(identity)
            if cached is None:
                flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0)
                try:
                    fd = os.open(real, flags)
                except OSError as exc:
                    raise Refused('PIN_UNREADABLE', '%s: %s' % (where, type(exc).__name__))
                try:
                    opened = os.fstat(fd)
                    if not stat.S_ISREG(opened.st_mode):
                        raise Refused('PIN_NOT_REGULAR_FILE', where)
                    identity = (opened.st_dev, opened.st_ino)
                    if identity != (before.st_dev, before.st_ino):
                        raise Refused('PIN_CHANGED_DURING_READ', where)
                    chunks = []
                    while True:
                        chunk = os.read(fd, 1 << 20)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    after = os.fstat(fd)
                    if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (
                            after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                        raise Refused('PIN_CHANGED_DURING_READ', where)
                finally:
                    os.close(fd)
                raw = b''.join(chunks)
                cached = (raw, identity)
                self.identities[identity] = cached
                self.reads[real] = self.reads.get(real, 0) + 1
            self.paths[real] = cached
        raw, identity = cached
        if require_nonempty and not raw:
            raise Refused('PIN_EMPTY_FILE', where)
        if ident_out is not None:
            ident_out.append(identity)
        return raw, real

    def audit(self):
        return {
            'rule': 'one guarded byte snapshot per immutable file per command',
            'byte_reads': dict(sorted(self.reads.items())),
            'requests': dict(sorted(self.requests.items())),
            'distinct_file_identities': len(self.identities),
            'violations': [p for p, n in sorted(self.reads.items()) if n != 1],
        }


@contextlib.contextmanager
def snapshot_scope():
    global _ACTIVE_SNAPSHOT, _LAST_SNAPSHOT_AUDIT
    outer = _ACTIVE_SNAPSHOT is None
    if outer:
        _ACTIVE_SNAPSHOT = CommandSnapshot()
    try:
        yield _ACTIVE_SNAPSHOT
    finally:
        if outer:
            _LAST_SNAPSHOT_AUDIT = _ACTIVE_SNAPSHOT.audit()
            _ACTIVE_SNAPSHOT = None


def command_snapshot(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        with snapshot_scope():
            return function(*args, **kwargs)
    return wrapped


def _read_regular(path, where, ident_out=None):
    # Low-level calls made outside a public operation still have a guarded read.
    if _ACTIVE_SNAPSHOT is None:
        with snapshot_scope() as snapshot:
            return snapshot.read(path, where, ident_out)
    return _ACTIVE_SNAPSHOT.read(path, where, ident_out)


def own_pin():
    raw, real = _read_regular(__file__, 'builder source')
    return {'path': real, 'sha256': sha256_hex(raw)}


def share_freeze_snapshot(module):
    """The freeze module consumes the same buffer used for builder pin checks."""
    def freeze_read(path, require_nonempty):
        try:
            with snapshot_scope() as snapshot:
                raw, real = snapshot.read(path, 'freeze module input',
                                          require_nonempty=require_nonempty)
            return raw, real, None
        except Refused as exc:
            return None, None, exc.code
    module._read_regular = freeze_read
    return module


def load_freeze_module(pin):
    raw, norm = read_bytes_pin(pin, 'freeze_module')
    module = types.ModuleType('freeze_module_' + norm['sha256'][:16])
    module.__file__ = norm['path']
    exec(compile(raw, norm['path'], 'exec'), module.__dict__)
    return share_freeze_snapshot(module)


# Component: receipt_rules_draft001.py
"""c2v007 component: A223 status and sample rules.
Pure rule definitions ported from P112 CX2V003 source bytes
sha256 8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9.
No P112 module execution or launch operation is imported.
"""

STATUS_CLASSES = {
    "FINISHED|COMPLETED": "FINISHED",
    "FINISHED|COMPLETED_INVALID": "FINISHED",
    "CHILD_FAILED|FAILED": "FAILED",
    "CHILD_FAILED|FAILED_AT_STAGE": "FAILED",
    "CHILD_FAILED|ROUTE_A_NO_FIXED_POINT": "FAILED",
    "CHILD_FAILED|NONE|EXIT": "FAILED",
    "STOPPED_WALL_CAP|COMPLETED": "CAP",
    "STOPPED_WALL_CAP|COMPLETED_INVALID": "CAP",
    "STOPPED_WALL_CAP|FAILED": "CAP",
    "STOPPED_WALL_CAP|FAILED_AT_STAGE": "CAP",
    "STOPPED_WALL_CAP|ROUTE_A_NO_FIXED_POINT": "CAP",
    "STOPPED_WALL_CAP|REFUSED": "CAP",
    "STOPPED_WALL_CAP|BLOCKED": "CAP",
    "STOPPED_WALL_CAP|UNREADABLE_FINISH": "CAP",
    "STOPPED_WALL_CAP|RESULT_HASH_MISMATCH": "CAP",
    "STOPPED_WALL_CAP|NONE": "CAP",
    "STOPPED_RSS_CAP|COMPLETED": "CAP",
    "STOPPED_RSS_CAP|COMPLETED_INVALID": "CAP",
    "STOPPED_RSS_CAP|FAILED": "CAP",
    "STOPPED_RSS_CAP|FAILED_AT_STAGE": "CAP",
    "STOPPED_RSS_CAP|ROUTE_A_NO_FIXED_POINT": "CAP",
    "STOPPED_RSS_CAP|REFUSED": "CAP",
    "STOPPED_RSS_CAP|BLOCKED": "CAP",
    "STOPPED_RSS_CAP|UNREADABLE_FINISH": "CAP",
    "STOPPED_RSS_CAP|RESULT_HASH_MISMATCH": "CAP",
    "STOPPED_RSS_CAP|NONE": "CAP",
    "STOPPED_OUTPUT_CAP|COMPLETED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|COMPLETED_INVALID": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|FAILED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|FAILED_AT_STAGE": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|ROUTE_A_NO_FIXED_POINT": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|REFUSED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|BLOCKED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|UNREADABLE_FINISH": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|RESULT_HASH_MISMATCH": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|NONE": "OUTPUT_CAP",
    "CHILD_FAILED|REFUSED": "INFRA",
    "CHILD_FAILED|BLOCKED": "INFRA",
    "CHILD_FAILED|NONE|SIGNAL": "INFRA",
    "CHILD_FAILED|UNREADABLE_FINISH": "INFRA",
    "CHILD_FAILED|RESULT_HASH_MISMATCH": "INFRA",
    "CHILD_FAILED|COMPLETED": "INFRA",
    "CHILD_FAILED|COMPLETED_INVALID": "INFRA",
    "FINISHED|NONE": "INFRA",
    "FINISHED|UNREADABLE_FINISH": "INFRA",
    "FINISHED|RESULT_HASH_MISMATCH": "INFRA",
    "FINISHED|FAILED": "INFRA",
    "FINISHED|FAILED_AT_STAGE": "INFRA",
    "FINISHED|ROUTE_A_NO_FIXED_POINT": "INFRA",
    "FINISHED|REFUSED": "INFRA",
    "FINISHED|BLOCKED": "INFRA",
    "MISLAUNCH": "INFRA",
    "MONITOR_REFUSED": "INFRA",
    "TWIN_PLANNED_STOP": "PLANNED_STOP",
}

STATUS_MAP_SHA = "c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54"

MONITOR_SCHEMA = "UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001"

TWIN = "S0_SEED_CW8_TWIN"

DECLARED_TOOLS = [{'tool': 'galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py', 'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377', 'driver_only': True}, {'tool': 'eps_ngc_point_c4v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/eps_ngc_point_c4v002.py', 'sha256': '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235', 'driver_only': False}, {'tool': 'gq_binding_c4v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/gq_binding_c4v002.py', 'sha256': 'f4ee064d9da414d9b98581ff6c1e374aab566950d9faf2e978342bc9a5dba0b1', 'driver_only': False}, {'tool': 'ngc_rho_producer_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_producer_c3v003.py', 'sha256': 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4', 'driver_only': False}, {'tool': 'ngc_rho_stage_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_stage_c3v003.py', 'sha256': '496d2a215145fb25aadbc4623b8930134cc2679cf1fe8097c65bf84cab450090', 'driver_only': False}, {'tool': 'ngc_lo_slot_proof_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_lo_slot_proof_c3v003.py', 'sha256': 'ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a', 'driver_only': False}, {'tool': 'ngc_acceptance_handoff_c2v005', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py', 'sha256': '7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1', 'driver_only': False}, {'tool': 'ngc_lo_state_adapter_c2v003a', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_lo_state_adapter_c2v003a.py', 'sha256': '9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2', 'driver_only': False}, {'tool': 'ngc_roster_recipes_c2v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_roster_recipes_c2v002.py', 'sha256': 'c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e', 'driver_only': False}, {'tool': 'ngc_acceptance_handoff_c2v003a', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v003a.py', 'sha256': '7c54fd6fcc3defbc6728a35fd5125eb0d2fba23b735a38af6ac8de2094c04427', 'driver_only': False}, {'tool': 'values_writer_c2v004_cx2v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py', 'sha256': '26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e', 'driver_only': False}, {'tool': 'extract_carriers_cx3v005', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/tools/extract_carriers_cx3v005.py', 'sha256': '50c7db5fbc2eb2cce17dcbb53ba1186bfdbc635a4098b0eb33ebd1402829732f', 'driver_only': False}, {'tool': 'extract_carriers_c2v001', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/extract_carriers_c2v001.py', 'sha256': '8acd21c7b8c2c1d96038a6d1eee9cbf68c25e556ae4da59bea8b70f09c1c602a', 'driver_only': False}]

DECLARED_LIST_SHA = sha256_hex(canonical_bytes(DECLARED_TOOLS))
if len(STATUS_CLASSES) != 54 or sha256_hex(canonical_bytes(STATUS_CLASSES)) != STATUS_MAP_SHA:
    raise RuntimeError('STATUS_MAP_BYTES')
EXACT_RECEIPT_KEYS = {k: k for k in RECEIPT_KEY_ROLES}
EXACT_RECEIPT_KEYS['status'] = 'raw_status'


def _receipt_need(condition, code, detail=None):
    if not condition:
        raise Refused(code, '' if detail is None else str(detail))


def _monitor_timestamp(value, whole=False):
    ns = parse_utc_ns(value, 'monitor/sample timestamp')
    if whole and ns % 1000000000:
        raise Refused('MONITOR_TIME_NOT_WHOLE_SECONDS')
    return ns / 1000000000


def monitor_receipt(raw):
    rec = strict_json(raw, 'monitor receipt')
    _receipt_need(type(rec) is dict and rec.get("schema") == MONITOR_SCHEMA, "MONITOR_RECEIPT_SCHEMA")
    core = {k: v for k, v in rec.items() if k != "receipt_sha256"}
    _receipt_need(rec.get("receipt_sha256") == sha256_hex(canonical_bytes(core)), "MONITOR_RECEIPT_SELF_HASH")
    # Deliberately not root_monitor.verify_receipt: it opens result.json.
    return rec


def raw_status(rec, *, name, attempt, outdir, receipt, launch_pin, child_pid,
               mislaunch=None, stop=None):
    if mislaunch is not None:
        bound = (mislaunch.get("name") == name and mislaunch.get("attempt") == attempt and
                 mislaunch.get("outdir") == outdir and mislaunch.get("receipt") == receipt)
        lj = mislaunch.get("launch_json") or {}
        if lj.get("sha256") is not None:
            bound = bound and lj["sha256"] == launch_pin["sha256"]
        if lj.get("child_pid") is not None:
            bound = bound and lj["child_pid"] == child_pid
        _receipt_need(bound, "MISLAUNCH_NOT_BOUND")
        return "MISLAUNCH", "INFRA"
    if name == TWIN:
        if stop is not None:
            _receipt_need(stop.get("reason") == "ITERATION_0001_COMPLETED_AND_SIDECAR" and
                 stop.get("outdir") == outdir and
                 (stop.get("launch_json") or {}).get("sha256") == launch_pin["sha256"],
                 "TWIN_STOP_NOT_BOUND")
        if stop is not None or str(rec.get("status", "")).startswith("STOPPED_"):
            return "TWIN_PLANNED_STOP", "PLANNED_STOP"
    driver = rec.get("driver_status")
    _receipt_need(driver is None or isinstance(driver, str), "DRIVER_STATUS_FORM")
    raw = str(rec.get("status")) + "|" + (driver if driver is not None else "NONE")
    if raw == "CHILD_FAILED|NONE":
        _receipt_need(type(rec.get("exit_code")) is int, "EXIT_CODE_FORM")
        raw += "|SIGNAL" if rec["exit_code"] < 0 else "|EXIT"
    _receipt_need(raw in STATUS_CLASSES, "RECEIPT_STATUS_UNMAPPED", raw)
    return raw, STATUS_CLASSES[raw]


def sample_value(sample, rec):
    if not isinstance(sample, dict):
        return None
    if sample.get("complete") is not True:
        return None
    try:
        p = sample["poll_s"]
        gap = sample["largest_gap_s"]
        _receipt_need(type(p) in (int, float) and math.isfinite(p) and 0 < p <= 10, "SAMPLE_POLL")
        _receipt_need(type(gap) in (int, float) and math.isfinite(gap) and gap >= 0, "SAMPLE_GAP")
        if gap > 2 * p:
            return None
        if math.floor(_monitor_timestamp(sample["first_utc"])) >= _monitor_timestamp(rec["utc_start"], whole=True):
            return None
        if math.floor(_monitor_timestamp(sample["last_utc"])) <= _monitor_timestamp(rec["utc_end"], whole=True):
            return None
        count = sample["max_other_ngc_processes"]
        _receipt_need(type(count) is int and count >= 0, "SAMPLE_COUNT")
        _receipt_need(type(sample["n_samples"]) is int and sample["n_samples"] >= 2, "SAMPLE_N")
        return count
    except (KeyError, TypeError, ValueError, Refused):
        return None


def _receipt_cfg(rk, classes):
    _keys(rk, RECEIPT_KEY_ROLES, 'receipt_keys')
    if rk != EXACT_RECEIPT_KEYS:
        raise Refused('RECEIPT_KEYS', 'A223 G25 fixes all nine role keys')
    if not isinstance(classes, dict) or classes != STATUS_CLASSES:
        raise Refused('RECEIPT_STATUS_CLASSES', 'A223 G13 requires the exact 54-key map')
    return {'keys': dict(rk), 'classes': dict(classes), 'facts': {}}


# Component: receipt_validation_draft002.py
"""c2v007 component: re-derive attempt facts from their pinned producer records."""


def _receipt(pin, cfg, where):
    doc, norm, _, ident = read_json_pin_ident(pin, where)
    _receipt_need(isinstance(doc, dict) and doc.get('schema') == 'STEP5_ATTEMPT_RECEIPT_C2V001',
                  'RECEIPT_SHAPE', where)
    run_dir = doc.get('run_dir')
    _receipt_need(isinstance(run_dir, str) and os.path.isabs(run_dir),
                  'RUN_DIR_INVALID', where)
    run_real = os.path.realpath(run_dir)
    _receipt_need(norm['path'] == run_real + '.attempt_receipt.json',
                  'RECEIPT_NOT_AT_REGISTERED_SIDECAR', where)
    call = doc.get('call')
    _receipt_need(isinstance(call, dict) and isinstance(call.get('name'), str),
                  'RECEIPT_CALL_BINDING_MISSING', where)
    name, k = call['name'], doc.get('attempt')
    _receipt_need(type(k) is int and k >= 1, 'RECEIPT_ATTEMPT_NUMBER', where)
    pins = doc.get('pins')
    _receipt_need(isinstance(pins, dict), 'RECEIPT_PINS_REQUIRED', where)
    raw, monitor_pin = read_bytes_pin(pins.get('monitor_receipt'), where + '.monitor_receipt')
    monitor = monitor_receipt(raw)
    _receipt_need(monitor_pin['path'] == run_real + '.receipt.json',
                  'MONITOR_RECEIPT_RESIDENCE', where)
    launch, launch_pin, _ = read_json_pin(pins.get('launch_json'), where + '.launch_json')
    record, record_pin, _ = read_json_pin(pins.get('launch_record'), where + '.launch_record')
    entry, entry_pin, _ = read_json_pin(pins.get('registry_entry'), where + '.registry_entry')
    _receipt_need(all(isinstance(x, dict) for x in (launch, record, entry)),
                  'RECEIPT_SOURCE_SHAPE', where)
    _receipt_need(launch_pin['path'] == run_real + '.receipt.json.launch.json',
                  'LAUNCH_JSON_RESIDENCE', where)
    _receipt_need(record.get('name') == name and record.get('attempt') == k and
                  record.get('outdir') == run_real and record.get('receipt') == monitor_pin['path'],
                  'LAUNCH_RECORD_NOT_BOUND', where)
    outcome = record.get('outcome')
    _receipt_need(outcome in ('LAUNCH', 'MISLAUNCH'), 'LAUNCH_RECORD_OUTCOME', where)
    recorded_launch = record.get('launch_json')
    _receipt_need(isinstance(recorded_launch, dict) and
                  os.path.realpath(recorded_launch.get('path', '')) == launch_pin['path'] and
                  recorded_launch.get('sha256') in (None, launch_pin['sha256']),
                  'LAUNCH_JSON_RECORD_PIN', where)
    _receipt_need(type(monitor.get('child_pid')) is int and monitor['child_pid'] > 0 and
                  monitor['child_pid'] == launch.get('child_pid'),
                  'MONITOR_CHILD_BINDING', where)
    monitor_pins = monitor.get('pins')
    launch_pins = launch.get('pins')
    _receipt_need(isinstance(monitor_pins, dict) and isinstance(launch_pins, dict),
                  'MONITOR_PINS_FORM', where)
    spec = monitor_pins.get('spec')
    _receipt_need(isinstance(spec, dict) and _is_hex64(spec.get('sha256')) and
                  entry.get('spec') == spec and launch_pins.get('spec') == spec and
                  doc.get('spec_sha256') == spec['sha256'],
                  'RECEIPT_SPEC_SOURCE_MISMATCH', where)
    _receipt_need(entry.get('name') == name, 'REGISTRY_CALL_BINDING', where)
    if entry.get('schema') == 'UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001':
        _receipt_need(entry.get('point_key') == doc.get('point_key') and
                      entry.get('theta_sha256') == doc.get('theta_sha256') and
                      all(entry.get(key) == call.get(key) for key in ('alternative', 'kind', 'key')),
                      'REGISTRY_CALL_BINDING', where)
    else:
        _receipt_need(entry.get('schema') == 'UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A' and
                      entry.get('theta_key') == doc.get('point_key'),
                      'REGISTRY_CALL_BINDING', where)
    caps = monitor.get('caps')
    _receipt_need(isinstance(caps, dict), 'MONITOR_CAPS_FORM', where)
    for key in ('rss_cap_bytes', 'wall_cap_s', 'output_cap_bytes'):
        _receipt_need(key in caps and doc.get(key) == caps[key],
                      'RECEIPT_CAP_SOURCE_MISMATCH', where + '.' + key)
    _receipt_need(doc.get('time_utc') == monitor.get('utc_end'),
                  'RECEIPT_TIME_SOURCE_MISMATCH', where)
    _monitor_timestamp(monitor.get('utc_start'), whole=True)
    _monitor_timestamp(monitor.get('utc_end'), whole=True)
    _receipt_need(doc.get('launch_utc') == launch.get('utc'),
                  'RECEIPT_LAUNCH_TIME_SOURCE_MISMATCH', where)
    _monitor_timestamp(launch.get('utc'), whole=True)
    stop = None
    if pins.get('stop_record') is not None:
        stop, _, _ = read_json_pin(pins['stop_record'], where + '.stop_record')
        _receipt_need(isinstance(stop, dict), 'TWIN_STOP_NOT_BOUND', where)
    status, cls = raw_status(monitor, name=name, attempt=k, outdir=run_real,
                            receipt=monitor_pin['path'], launch_pin=launch_pin,
                            child_pid=monitor['child_pid'],
                            mislaunch=record if outcome == 'MISLAUNCH' else None, stop=stop)
    _receipt_need(doc.get('raw_status') == status and doc.get('status_class') == cls,
                  'RECEIPT_STATUS_NOT_REDERIVED', where)
    _receipt_need(pins.get('status_map_sha256') == STATUS_MAP_SHA,
                  'RECEIPT_STATUS_MAP_SHA', where)
    _receipt_need(doc.get('solo_mode') is record.get('solo_mode', False) and
                  type(doc.get('solo_mode')) is bool,
                  'RECEIPT_SOLO_MODE_SOURCE_MISMATCH', where)
    sample = None
    sample_pin = pins.get('solo_sample')
    if sample_pin is not None:
        # A missing sample is one of G25's five null cases. A present but
        # unverified sample is a pin refusal, never accepted evidence of zero.
        if not isinstance(sample_pin, dict) or set(sample_pin) != {'path', 'sha256'}:
            raise Refused('PIN_SHAPE', where + '.solo_sample')
        if not isinstance(sample_pin['path'], str) or not os.path.isabs(sample_pin['path']) or \
                not _is_hex64(sample_pin['sha256']):
            raise Refused('PIN_SHAPE', where + '.solo_sample')
        if os.path.lexists(sample_pin['path']):
            sample, sample_norm, _ = read_json_pin(sample_pin, where + '.solo_sample')
            _receipt_need(isinstance(sample, dict) and
                          sample.get('schema') == 'STEP5_SOLO_SAMPLE_CX2V001' and
                          sample.get('name') == name and sample.get('attempt') == k and
                          sample.get('outdir') == run_real and
                          sample.get('declared_list_sha256') == DECLARED_LIST_SHA and
                          sample.get('monitor_receipt') == monitor_pin and
                          sample_norm['path'] == run_real + '.solo.json',
                          'SOLO_SAMPLE_BINDING', where)
    count = sample_value(sample, monitor)
    _receipt_need(doc.get('other_ngc_processes_max') == count and
                  (doc.get('other_ngc_processes_max') is None or
                   type(doc['other_ngc_processes_max']) is int),
                  'SOLO_SAMPLE_VALUE_NOT_REDERIVED', where)
    host_ram = doc.get('host_ram_bytes')
    _receipt_need(type(host_ram) is int and host_ram > 0, 'HOST_RAM_FORM', where)
    if entry.get('schema') == 'UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001':
        _receipt_need('host_ram_bytes' in record, 'HOST_RAM_SOURCE_MISSING', where)
    if 'host_ram_bytes' in record:
        _receipt_need(record['host_ram_bytes'] == host_ram, 'HOST_RAM_SOURCE_MISMATCH', where)
    else:
        _receipt_need(host_ram == 137438953472, 'HOST_RAM_SOURCE_MISMATCH', where)
    _receipt_need(pins.get('result') == monitor.get('result'),
                  'RECEIPT_RESULT_SOURCE_MISMATCH', where)
    evidence = {r: doc.get(cfg['keys'][r]) for r in EVIDENCE_ROLES}
    evidence.update({'call_name': name, 'solo_mode': doc['solo_mode'],
                     'column_workers': _cw8_receipt_workers(doc, entry, entry_pin, record, where)})
    binding = {r: doc.get(cfg['keys'][r]) for r in BINDING_ROLES}
    cfg['facts'][norm['path']] = {
        'call': call, 'attempt': k, 'run_dir': run_real,
        'monitor_receipt': monitor_pin, 'launch_json': launch_pin,
        'launch_record': record_pin, 'registry_entry': entry_pin,
        'result': monitor.get('result'), 'receipt': norm,
    }
    return (norm, status, cls, parse_utc_ns(doc['time_utc'], where),
            evidence, binding, ident)


# Component: terminal_rules_draft002.py
"""c2v007 terminal and counted-pair changes; baseline function bodies retained otherwise."""

DISPOSITION_OF['INFRA_REPEAT'] = 'UNEVALUATED_INFRA_REPEAT'

def _positive_number(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0

def _infra_repeat_problem(prefix):
    if len(prefix) < 2:
        return 'PAIR_MISSING'
    a, b = prefix[-2:]
    if a['raw'] != b['raw'] or b['raw'] not in ('CHILD_FAILED|REFUSED', 'CHILD_FAILED|BLOCKED'):
        return 'RAW_STATUS'
    if len({s['evidence'].get('spec_sha256') for s in prefix}) != 1:
        return 'SPEC'
    for x in (a, b):
        ev = x['evidence']
        if _evidence_problem(ev, True) or ev.get('solo_mode') is not True or ev['other_ngc_processes_max'] != 0:
            return 'SOLO_EVIDENCE'
    for key in ('rss_cap_bytes', 'wall_cap_s', 'output_cap_bytes'):
        if a['evidence'][key] != b['evidence'][key]:
            return 'CAPS'
    return None

def _rule_c_problem(prefix):
    """None when the last two attempts of `prefix` are a rule-(c) terminal pair (FAILED, CAP or OUTPUT_CAP); else
    (code, detail). Only the attempts up to and including the pair are read (R1: a later attempt never decides
    whether an earlier pair was terminal).

    Mechanizes A133 3 (c) for a step-5 NGC call: two identical (same raw status) non-INFRA failures, the identical
    spec on every evidenced attempt, both counted attempts with no other NGC process running, and the counted rerun
    (the last attempt) with the RSS cap at host RAM and the wall cap at twice the call's first attempt (A141 L1: an
    OUTPUT_CAP rerun also has the output cap raised above the first attempt's)."""
    i = len(prefix) - 1
    cur = prefix[i]
    if i == 0:
        return ('RULE_C_INCOMPLETE', 'one failure; rule (c) reruns it (A133 3 (c), (f))')
    prev = prefix[i - 1]
    if prev['class'] != cur['class'] or prev['raw'] != cur['raw']:
        return ('RULE_C_INCOMPLETE', 'the last two attempts are not two identical non-INFRA failures (A133 3 (c))')
    need_out = cur['class'] == 'OUTPUT_CAP'
    for j in (i - 1, i):
        p = _evidence_problem(prefix[j]['evidence'], need_out)
        if p:
            return ('RULE_C_EVIDENCE_MISSING', 'attempt %d receipt lacks valid %s (G25)' % (j, p))
    if i - 1 != 0:
        first = prefix[0]['evidence']
        if not _is_hex64(first.get('spec_sha256')) or not _positive_number(first.get('wall_cap_s')) or (need_out and not _pos_int(first.get('output_cap_bytes'))):
            return ('RULE_C_EVIDENCE_MISSING', 'attempt 0 lacks the G25 minimum evidence')
    specs = {canonical_bytes(s['evidence'].get('spec_sha256')) for s in prefix
             if s['evidence'].get('spec_sha256') is not None}
    if len(specs) != 1:
        return ('RULE_C_SPEC_NOT_IDENTICAL', 'rule (c) reruns the identical spec')
    if prev['evidence']['other_ngc_processes_max'] != 0 or cur['evidence']['other_ngc_processes_max'] != 0:
        return ('RULE_C_NOT_SOLO', 'both counted failures must run with no other NGC process running')
    first, ev = prefix[0]['evidence'], cur['evidence']
    if ev['rss_cap_bytes'] != ev['host_ram_bytes'] * (11 if ev.get('call_name') == TWIN else 1):
        return ('RULE_C_RERUN_CAPS', 'the rerun RSS cap is not at RAM')
    if ev['wall_cap_s'] != 2 * first['wall_cap_s']:
        return ('RULE_C_RERUN_CAPS', 'the rerun wall cap is not twice the first attempt\'s')
    if need_out and not ev['output_cap_bytes'] > first['output_cap_bytes']:
        return ('RULE_C_RERUN_CAPS', 'the OUTPUT_CAP rerun did not raise the output cap (A141 L1)')
    return None

def _terminal(attempts, cfg, where, allow_planned, binding):
    """The terminal attempt of one call under rule (c). binding: {'theta_sha256', 'spec_sha256'} of this call (the
    launch registry entry); every receipt of the call must carry exactly these (R2)."""
    if not isinstance(attempts, list) or not attempts:
        raise Refused('CALL_ATTEMPTS_REQUIRED', where)
    seen, run_dirs, receipt_paths, receipt_shas = [], [], set(), set()
    for i, a in enumerate(attempts):
        w = '%s.attempts[%d]' % (where, i)
        _keys(a, ('run_dir', 'receipt'), w)
        if not isinstance(a['run_dir'], str) or not os.path.isabs(a['run_dir']) or not os.path.isdir(a['run_dir']):
            raise Refused('RUN_DIR_INVALID', w)
        run_real = os.path.realpath(a['run_dir'])
        if run_real in run_dirs:
            raise Refused('ATTEMPT_RUN_DIR_REPEATED', '%s: one run directory (by realpath) serves two attempts' % w)
        if any(_under(d, run_real) or _under(run_real, d) for d in run_dirs):
            raise Refused('ATTEMPT_RUN_DIR_NESTED', '%s: attempt run directories must be disjoint' % w)
        norm, raw_status, cls, t, evidence, rbind, ident = _receipt(a['receipt'], cfg, w + '.receipt')
        if norm['path'] in receipt_paths or norm['sha256'] in receipt_shas:
            raise Refused('ATTEMPT_RECEIPT_REPEATED', '%s: one receipt (by realpath or sha256) serves two attempts' % w)
        if norm['path'] != run_real + '.attempt_receipt.json':
            raise Refused('RECEIPT_NOT_AT_REGISTERED_SIDECAR', w)
        facts = cfg['facts'][norm['path']]
        if facts['run_dir'] != run_real:
            raise Refused('RECEIPT_RUN_DIR_NOT_OF_CALL', w)
        alias = (binding.get('kind') == 'SENSITIVITY' and
                 facts['call'].get('kind') in ('MEMBER', 'SENSITIVITY') and
                 facts['call'].get('alternative') == binding.get('alternative'))
        for role in ('alternative', 'kind', 'key'):
            if role in binding and facts['call'].get(role) != binding[role] and not (
                    alias and role in ('kind', 'key')):
                raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and facts['call']['name'] != seen[-1]['evidence']['call_name']:
            raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and t <= seen[-1]['time_ns']:
            raise Refused('ATTEMPT_ORDER', '%s: receipt times must strictly increase' % w)
        run_dirs.append(run_real)
        receipt_paths.add(norm['path'])
        receipt_shas.add(norm['sha256'])
        seen.append({'run_dir': run_real, 'receipt': norm, 'raw': raw_status, 'class': cls, 'time_ns': t,
                     'evidence': evidence, 'binding': rbind, 'ident': ident})
    # R1: the call is terminal at the first terminal prefix; each pair is judged on its own prefix only, so a later
    # attempt (of any spec) can never un-terminate an earlier pair and re-roll the call
    for i in range(len(seen) - 1):
        c = seen[i]['class']
        if c in ('FINISHED', 'PLANNED_STOP') or (c in FAILURE_CLASSES and _rule_c_problem(seen[:i + 1]) is None) or (c == 'INFRA' and _infra_repeat_problem(seen[:i + 1]) is None):
            raise Refused('ATTEMPT_AFTER_TERMINAL', '%s.attempts[%d]: the call was already terminal at attempt %d; '
                                                    'a later attempt would re-roll it' % (where, i + 1, i))
    # R1: one call, one spec ("rerun the identical spec"): its attempts carry at most one spec_sha256
    specs = {canonical_bytes(s['evidence']['spec_sha256']) for s in seen if s['evidence']['spec_sha256'] is not None}
    if len(specs) > 1:
        raise Refused('RULE_C_SPEC_NOT_IDENTICAL', '%s: the attempts carry more than one spec_sha256; rule (c) '
                                                   'reruns the identical spec' % where)
    # R2: every receipt is bound to this call (exact-theta key, then the spec sha the launch registry records)
    for i, s in enumerate(seen):
        for role, code in (('theta_sha256', 'RECEIPT_THETA_NOT_OF_CALL'), ('spec_sha256', 'RECEIPT_SPEC_NOT_REGISTERED')):
            v = s['binding'].get(role)
            if v is None:
                raise Refused('RECEIPT_CALL_BINDING_MISSING', '%s.attempts[%d]: the receipt carries no %s (G27)'
                              % (where, i, role))
            if v != binding[role]:
                raise Refused(code, '%s.attempts[%d]: the receipt\'s %s is not this call\'s' % (where, i, role))
    last = seen[-1]
    if last['class'] == 'INFRA' and _infra_repeat_problem(seen) is not None:
        raise Refused('CALL_NOT_TERMINAL', where + ': the last attempt is INFRA; rule (c) retries it')
    if last['class'] == 'PLANNED_STOP' and not allow_planned:
        raise Refused('PLANNED_STOP_NOT_A_MEMBER_TERMINAL', where)
    rule_c = None
    if last['class'] in FAILURE_CLASSES:
        p = _rule_c_problem(seen)
        if p:
            raise Refused(p[0], '%s: %s' % (where, p[1]))
        n = len(seen)
        rule_c = {'counted_attempts': [n - 2, n - 1], 'raw_status': last['raw'],
                  'spec_sha256': last['evidence']['spec_sha256'],
                  'other_ngc_processes_max': [seen[-2]['evidence']['other_ngc_processes_max'],
                                              last['evidence']['other_ngc_processes_max']],
                  'first_wall_cap_s': seen[0]['evidence']['wall_cap_s'],
                  'rerun_wall_cap_s': last['evidence']['wall_cap_s'],
                  'rerun_rss_cap_bytes': last['evidence']['rss_cap_bytes'],
                  'host_ram_bytes': last['evidence']['host_ram_bytes']}
        if last['class'] == 'OUTPUT_CAP':
            rule_c.update({'first_output_cap_bytes': seen[0]['evidence']['output_cap_bytes'],
                           'rerun_output_cap_bytes': last['evidence']['output_cap_bytes']})
    return {'class': ('INFRA_REPEAT' if last['class'] == 'INFRA' else last['class']), 'raw_status': last['raw'], 'time_ns': last['time_ns'],
            'run_dir': last['run_dir'], 'receipt': last['receipt'], 'n_attempts': len(seen),
            'receipt_paths': [s['receipt']['path'] for s in seen],
            'receipt_shas': [s['receipt']['sha256'] for s in seen],
            'receipt_idents': [s['ident'] for s in seen], 'run_dirs': [s['run_dir'] for s in seen],
            'rule_c': rule_c, 'source_facts': [cfg['facts'][s['receipt']['path']] for s in seen]}


# Component: m15_rules_draft001.py
"""c2v007 component: G15 kit M15 form and launch-side timing."""

M15_RECORD_SCHEMA = 'UNT_M15_PRELAUNCH_RECORD_C2V001'
M15_KIT_KEYS = ('schema', 'date_u', 'date_u_epoch_s', 'date_u_iso', 'v006',
                'gate_documents_pinned_in_v006', 'root_listed_row_gates',
                'root_listed_row_gates_entries', 'required_pins', 'first_launch',
                'v006_write_freeze', 'on_time_rule', 'rules', 'writer', 'written_by')

def _gate_status_list(m15, gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names, cfg):
    rosters_of = {}
    for n in names:
        for g in roster_docs[n]['root_gates']:
            rosters_of.setdefault(g['sha256'], []).append(n)
    out = {'schema': GATE_REPORT_SCHEMA, 'builder': BUILDER_NAME,
           'rule': ('M-15 (a)+(1), A142: ON_TIME iff the full gate sha256 occurs in the V006 bytes logged by the '
                    'pre-launch record and the record time is not after the earliest identity-pair launch receipt '
                    '(same second counts as preceding); every other root-listed gate is LATE. The record list is '
                    'checked for consistency and reported per gate; it does not decide the status'),
           'cutoff_v006': cutoff_pin, 'pre_launch_record': None, 'logged_v006': None, 'launch_receipts': [],
           'pre_launch_record_utc': None, 'earliest_launch_receipt_utc': None, 'record_precedes_launch': None,
           'gates': []}
    rec_set, logged_heads, precedes = set(), {}, False
    if m15 is None:
        reason_off = 'NO_PRE_LAUNCH_RECORD'
    else:
        _keys(m15, ('pre_launch_record', 'logged_v006_copy', 'launch_receipts'), 'm15')
        rdoc, rnorm, _ = read_json_pin(m15['pre_launch_record'], 'm15.pre_launch_record')
        _keys(rdoc, M15_KIT_KEYS, 'm15.pre_launch_record')
        if rdoc['schema'] != M15_RECORD_SCHEMA:
            raise Refused('M15_RECORD_SCHEMA', 'pre_launch_record')
        lraw, lnorm = read_bytes_pin(m15['logged_v006_copy'], 'm15.logged_v006_copy')
        if not isinstance(rdoc['v006'], dict) or lnorm['sha256'] != rdoc['v006'].get('sha256') or len(lraw) != rdoc['v006'].get('bytes'):
            raise Refused('M15_LOGGED_V006_MISMATCH', 'the V006 copy is not the bytes the record logs')
        logged_heads = v006_index(lraw)
        gl_rows = rdoc['gate_documents_pinned_in_v006']
        if not isinstance(gl_rows, list) or not all(isinstance(x, dict) for x in gl_rows):
            raise Refused('M15_RECORD_SHAPE', 'gate_documents_pinned_in_v006')
        gl = [x.get('sha256_from_bytes') for x in gl_rows]
        if not isinstance(gl, list) or not all(_is_hex64(x) for x in gl) or len(set(gl)) != len(gl):
            raise Refused('M15_RECORD_SHAPE', 'gate_document_sha256s')
        if any(x not in logged_heads for x in gl):
            raise Refused('M15_RECORD_INCONSISTENT', 'a recorded gate sha256 is not in the logged V006 bytes')
        rec_set = set(gl)
        rec_t = parse_utc_ns(rdoc['date_u'], 'm15.pre_launch_record.date_u')
        if type(rdoc['date_u_epoch_s']) is not int or rec_t != rdoc['date_u_epoch_s'] * 1000000000:
            raise Refused('M15_RECORD_TIME_MISMATCH', 'date_u and date_u_epoch_s disagree')
        lrs = m15['launch_receipts']
        if not isinstance(lrs, list) or not lrs:
            raise Refused('M15_LAUNCH_RECEIPT_REQUIRED', 'at least the serial identity-pair receipt')
        times = []
        for i, lp in enumerate(lrs):
            ldoc, lpn, _ = read_json_pin(lp, 'm15.launch_receipts[%d]' % i)
            t = parse_utc_ns(ldoc.get('utc') if isinstance(ldoc, dict) else None,
                             'm15.launch_receipts[%d]' % i)
            times.append(t)
            out['launch_receipts'].append({'receipt': lpn, 'utc': format_utc_ns(t)})
        earliest = min(times)
        precedes = rec_t <= earliest
        out.update({'pre_launch_record': rnorm, 'logged_v006': lnorm, 'pre_launch_record_utc': format_utc_ns(rec_t),
                    'earliest_launch_receipt_utc': format_utc_ns(earliest), 'record_precedes_launch': precedes})
        reason_off = None
    for g in gate_pins:
        if m15 is None:
            status, reason = 'LATE', reason_off
        elif not precedes:
            status, reason = 'LATE', 'PRE_LAUNCH_RECORD_AFTER_LAUNCH_RECEIPT'
        elif g['sha256'] in logged_heads:
            status, reason = 'ON_TIME', 'PINNED_IN_LOGGED_PRE_LAUNCH_V006'
        else:
            status, reason = 'LATE', 'NOT_PINNED_IN_LOGGED_PRE_LAUNCH_V006'
        head = cutoff_heads.get(g['sha256'])
        out['gates'].append({'gate': g, 'status': status, 'reason': reason,
                             'in_pre_launch_record_list': (g['sha256'] in rec_set) if m15 is not None else None,
                             'pinned_by_entry': head_names.get(head, head),
                             'rosters': sorted(rosters_of.get(g['sha256'], []))})
    return out


# Component: geometry_rules_draft002.py
"""c2v007 component: A223 VN1's registered in-memory exception and DN5."""

GEOMETRY_DISPOSITION = 'GEOMETRY_NOT_EXPOSED_IN_MEMORY'
SENS_NGC_KIND = 'NGC3198_NUISANCE'  # pinned v003g's SENS_NGC constant
INCOMPLETE_DISPOSITIONS = frozenset({
    'UNEVALUATED_CAP', 'UNEVALUATED_STEP7_DISCREPANCY',
    'UNEVALUATED_INFRA_REPEAT', 'UNEVALUATED_CUSTODY_BREACH',
})


def registered_geometry(spec, freeze_module):
    reasons = []
    parsed = freeze_module._spec_from(spec, reasons)
    if reasons or not isinstance(parsed, dict):
        raise Refused('SPEC_OF_RECORD_INVALID', 'coordinate spec does not validate')
    geometry = {
        c['name']: float(c['trial_value']) for c in spec['coordinates']
        if c.get('scope') == 'ngc3198_nuisance'
    }
    if not geometry or any(not math.isfinite(v) for v in geometry.values()):
        raise Refused('SPEC_OF_RECORD_GEOMETRY_MISSING')
    return geometry


def geometry_differs(theta, geometry):
    _theta_ok(theta, 'geometry comparison')
    if any(k not in theta for k in geometry):
        raise Refused('GEOMETRY_COORDINATE_MISSING')
    return any(theta[k].hex() != v.hex() for k, v in geometry.items())


def geometry_exemptions(entries, geometry):
    """entries: (entry id, theta, skipped, kind), from a pinned value-free plan."""
    exemptions = {}
    for entry_id, theta, skipped, kind in entries:
        if not geometry_differs(theta, geometry):
            continue
        if kind != SENS_NGC_KIND:
            raise Refused('NONREGISTERED_GEOMETRY_ON_OTHER_KIND', entry_id)
        if skipped:
            continue
        key = theta_sha256(theta)
        exemptions.setdefault(key, []).append(entry_id)
    return exemptions


def allow_incomplete_value(plan):
    if plan['phase'] == 'PHASE_1':
        return True
    for alternative in plan['alternatives']:
        if alternative['slots_status'] != ALT_EVALUATED:
            continue
        if any(m['own_disposition'] in INCOMPLETE_DISPOSITIONS
               for m in alternative['members']):
            return True
    primary = next((a for a in plan['alternatives'] if a['name'] == plan['primary']), None)
    return bool(primary is not None and primary['slots_status'] == ALT_EVALUATED and
                any(e['own_disposition'] in INCOMPLETE_DISPOSITIONS
                    for e in plan['sensitivity']['entries']))


def geometry_answer():
    return {
        'valid': False,
        'reasons': ['GEOMETRY_NOT_EXPOSED'],
        'rows': None,
        'speeds_km_s': None,
    }


_saved_make_replay_adapter = make_replay_adapter


def make_replay_adapter(replay_plan, alternative, serve_log, context):
    saved = _saved_make_replay_adapter(replay_plan, alternative, serve_log, context)
    geometry = replay_plan.get('registered_geometry', {})
    allowed = replay_plan.get('geometry_not_exposed', {})

    def forward_ngc(theta):
        key = theta_sha256(theta)
        if geometry and geometry_differs(theta, geometry):
            if context != 'SENSITIVITY' or alternative != replay_plan['primary'] or key not in allowed:
                raise ReplayUnknownKey('non-registered geometry outside the A223 VN1 exception')
            serve_log.append({
                'alternative': alternative, 'context': context,
                'theta_sha256': key, 'outcome': GEOMETRY_DISPOSITION, 'result': None,
            })
            return geometry_answer()
        return saved(theta)
    return forward_ngc


@contextlib.contextmanager
def geometry_runtime(freeze_module, replay_plan):
    """Apply only VN1's registered no-context, no-valid-row answer in memory.

    v003g checks a roster context even for invalid results. A223 exempts these
    specific sensitivity entries from contexts. This scoped check recognizes
    the exact invalid answer at an exempt key; every other result uses the
    unchanged pinned module's check.
    """
    previous = freeze_module._root_result_rows
    previous_frozen = freeze_module._root_frozen_rows
    allowed = replay_plan.get('geometry_not_exposed', {})
    geometry = replay_plan.get('registered_geometry', {})

    def row_check(result, ids, roster, theta):
        key = theta_sha256(theta)
        if key in allowed and geometry and geometry_differs(theta, geometry) and \
                canonical_bytes(result) == canonical_bytes(geometry_answer()):
            return []
        return previous(result, ids, roster, theta)


    def frozen_check(entry, ids, roster):
        if not entry.get('evaluated'):
            return previous_frozen(entry, ids, roster)
        theta = entry.get('theta_ngc')
        key = theta_sha256(theta)
        exempt = (entry.get('kind') == SENS_NGC_KIND and key in allowed and
                  geometry and geometry_differs(theta, geometry))
        if not exempt:
            return previous_frozen(entry, ids, roster)
        expected_reasons = [
            'forward_ngc reason: GEOMETRY_NOT_EXPOSED',
            'forward_ngc valid flag is not True',
        ]
        if entry.get('forward_valid_flag') is not False or entry.get('exception') is not None or \
                entry.get('reasons') != expected_reasons or \
                entry.get('row_valid') != [False] * len(ids) or \
                any(entry.get(k) != [None] * len(ids) for k in
                    ('speeds_km_s', 'row_registration', 'delta_from_reference_km_s')):
            raise Refused('VN1_FROZEN_ANSWER_NOT_EXACT')
        return None

    freeze_module._root_result_rows = row_check
    freeze_module._root_frozen_rows = frozen_check
    try:
        yield
    finally:
        freeze_module._root_result_rows = previous
        freeze_module._root_frozen_rows = previous_frozen


# Component: sensitivity_budget_draft001.py
"""c2v007 sensitivity budgeting includes the registered in-memory answers."""


def _sens_budget_rule(replay_plan, plan_entries):
    index = {e['theta_sha256']: e
             for e in replay_plan['replay_index'].get(replay_plan['primary'], [])}
    exemptions = replay_plan.get('geometry_not_exposed', {})
    out, budget, stopped = [], 0, False
    for entry_id, key, skipped in plan_entries:
        if skipped:
            out.append({'entry_id': entry_id, 'theta_sha256': key,
                        'skipped': True, 'disposition': 'SKIPPED'})
            continue
        entry = index.get(key)
        own = (GEOMETRY_DISPOSITION if key in exemptions else
               entry['disposition'] if entry is not None else 'NO_SAVED_CALL_AT_THIS_THETA')
        evaluated = own in EVALUATED_DISPOSITIONS or own == GEOMETRY_DISPOSITION
        if not stopped and evaluated:
            budget += 1
            disposition = own
        else:
            disposition = own if not stopped else 'UNEVALUATED_BY_ORDER_TRUNCATION'
            stopped = True
        out.append({'entry_id': entry_id, 'theta_sha256': key,
                    'skipped': False, 'disposition': disposition})
    return {'budget': budget, 'entries': out}


_saved_pass_record = pass_record


def pass_record(label, envelopes, reference, sensitivity, serve_log, binding):
    record = _saved_pass_record(label, envelopes, reference, sensitivity, serve_log, binding)
    record['in_memory_geometry_answers'] = [
        {
            'alternative': entry['alternative'],
            'context': entry['context'],
            'theta_sha256': entry['theta_sha256'],
            'outcome': entry['outcome'],
            'valid': False,
            'valid_rows': 0,
        }
        for entry in serve_log['entries'] if entry['outcome'] == GEOMETRY_DISPOSITION
    ]
    return record


# Component: custody_rules_draft002.py
"""c2v007 component: G16 custody checks and machine-derived successors.

Restoration remains root's recorded procedure. This tool never overwrites a
registered result or any other file.
"""


def require_run_volumes(volumes):
    if not isinstance(volumes, list) or not volumes:
        raise Refused('CUSTODY_RUN_VOLUMES_REQUIRED')
    for volume in volumes:
        if not isinstance(volume, str) or not os.path.isabs(volume) or \
                os.path.realpath(volume) != volume or os.path.islink(volume) or \
                not os.path.ismount(volume):
            raise Refused('RUN_VOLUME_NOT_MOUNTED', str(volume))


def custody_copy_inventory(root):
    if not isinstance(root, str) or not os.path.isabs(root) or \
            os.path.realpath(root) != root or not os.path.isdir(root):
        raise Refused('CUSTODY_ROOT_INVALID')
    contents = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs):
            if os.path.islink(os.path.join(directory, name)):
                raise Refused('CUSTODY_DIRECTORY_SYMLINK')
        for name in sorted(files):
            path = os.path.join(directory, name)
            if os.path.islink(path):
                raise Refused('CUSTODY_COPY_SYMLINK')
            try:
                raw, real = _read_regular(path, 'custody copy')
            except Refused as exc:
                if exc.code == 'PIN_EMPTY_FILE':
                    continue
                raise
            contents.setdefault(sha256_hex(raw), []).append(real)
    return contents


def check_custody_inputs(custody, resolved, others):
    _keys(custody, ('root', 'run_volumes', 'copies'), 'custody')
    require_run_volumes(custody['run_volumes'])
    root = custody['root']
    all_terminals = [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]
    run_dirs = [d for terminal in all_terminals for d in terminal['run_dirs']]
    if not isinstance(root, str) or not os.path.isabs(root) or os.path.realpath(root) != root or \
            not os.path.isdir(root) or any(root == d or _under(d, root) or _under(root, d) for d in run_dirs):
        raise Refused('CUSTODY_ROOT_IN_RUN_TREE')
    if any(not any(d == v or _under(v, d) for v in custody['run_volumes']) for d in run_dirs):
        raise Refused('CUSTODY_RUN_VOLUME_BINDING')
    required = {}
    for terminal in all_terminals:
        facts = terminal['source_facts'][-1]
        for key in ('receipt', 'monitor_receipt', 'result'):
            pin = facts.get(key)
            if pin is not None:
                required[(pin['path'], pin['sha256'])] = pin
    for rec in resolved.values():
        for key in ('result', 'cut'):
            pin = rec.get(key)
            if pin is not None:
                required[(pin['path'], pin['sha256'])] = pin
    copies = custody['copies']
    if not isinstance(copies, list):
        raise Refused('CUSTODY_COPIES_REQUIRED')
    seen, normalized = set(), []
    for item in copies:
        _keys(item, ('source', 'copy'), 'custody copy')
        raw, source, source_id = read_bytes_pin_ident(item['source'], 'custody source')
        copied, copy, copy_id = read_bytes_pin_ident(item['copy'], 'custody copy')
        key = (source['path'], source['sha256'])
        if key in seen or key not in required:
            raise Refused('CUSTODY_SOURCE_SET')
        if not _under(root, copy['path']) or any(
                copy['path'] == d or _under(d, copy['path']) for d in run_dirs):
            raise Refused('CUSTODY_COPY_IN_RUN_TREE')
        if raw != copied or source['sha256'] != copy['sha256']:
            raise Refused('CUSTODY_COPY_BYTES')
        # A custody copy must survive loss of the registered file itself.
        if source_id == copy_id:
            raise Refused('CUSTODY_COPY_IS_SOURCE')
        seen.add(key)
        normalized.append({'source': source, 'copy': copy})
    if seen != set(required):
        raise Refused('CUSTODY_SOURCE_SET')
    return {
        'root': root,
        'run_volumes': sorted(set(custody['run_volumes'])),
        'copies': sorted(normalized, key=lambda x: (x['source']['path'], x['source']['sha256'])),
    }


def custody_conditions(plan):
    custody = plan.get('custody')
    if not isinstance(custody, dict):
        raise Refused('CUSTODY_RECORD_REQUIRED')
    require_run_volumes(custody.get('run_volumes'))
    inventory = custody_copy_inventory(custody.get('root'))
    new, restorable = set(), []
    for alternative, entries in plan['replay_index'].items():
        for entry in entries:
            if entry['disposition'] == 'UNEVALUATED_CUSTODY_BREACH':
                continue
            pin = entry.get('result')
            if pin is None:
                continue
            try:
                read_bytes_pin(pin, 'registered custody result')
                good = True
            except Refused as exc:
                if exc.code not in ('PIN_UNREADABLE', 'PIN_MISMATCH', 'PIN_EMPTY_FILE',
                                    'PIN_NOT_REGULAR_FILE', 'PIN_CHANGED_DURING_READ'):
                    raise
                good = False
            if good:
                continue
            if pin['sha256'] in inventory:
                restorable.append({'result': pin, 'copies': inventory[pin['sha256']]})
                continue
            members = [k.split(':', 1)[1] for k in entry['call_keys'] if k.startswith('MEMBER:')]
            if not members:
                raise Refused('CUSTODY_PHASE2_SENSITIVITY_FORM_OPEN')
            new.update((alternative, member) for member in members)
    return sorted(new), restorable


_saved_apply_unevaluated = _apply_unevaluated


def _apply_unevaluated(plan, plan_sha, new):
    successor = _saved_apply_unevaluated(plan, plan_sha, new)
    successor['allow_incomplete'] = allow_incomplete_value(successor)
    return successor


def apply_custody_unevaluated(plan, plan_sha, new):
    successor = _saved_apply_unevaluated(plan, plan_sha, new)
    selected = set(new)
    for alternative in successor['alternatives']:
        for member in alternative['members']:
            if (alternative['name'], member['member_id']) in selected:
                member['own_disposition'] = 'UNEVALUATED_CUSTODY_BREACH'
        for entry in successor['replay_index'].get(alternative['name'], []):
            if any((alternative['name'], key.split(':', 1)[1]) in selected
                   for key in entry['call_keys'] if key.startswith('MEMBER:')):
                entry['disposition'] = 'UNEVALUATED_CUSTODY_BREACH'
        if alternative['member_budget'] is not None:
            _effective(alternative)
    successor['allow_incomplete'] = allow_incomplete_value(successor)
    return successor


def custody_derivation(plan, plan_sha):
    new, restorable = custody_conditions(plan)
    if restorable:
        raise Refused('CUSTODY_RESTORE_AVAILABLE', 'root restores from the verified copy under G16 3(a)')
    if not new:
        raise Refused('CUSTODY_NO_BREACH')
    successor = apply_custody_unevaluated(plan, plan_sha, new)
    checks = {
        'rule': 'G16 3(b): registered result fails verification and no same-sha custody copy exists',
        'calls': [{'alternative': a, 'member_id': m} for a, m in new],
    }
    return new, dump_bytes(successor), checks


def custody_run(build_record_pin, replay_plan_pin):
    ctx = _plan_context(build_record_pin, replay_plan_pin, 'custody')
    if ctx['superseded']:
        raise Refused('STEP7_PLAN_SUPERSEDED')
    new, successor, checks = custody_derivation(ctx['plan'], ctx['plan_sha'])
    ledger = ctx['ledger']
    if ledger['dir'] is None:
        raise Refused('STEP7_REPLAY_PLAN', 'custody requires a FULL build')
    successor_sha = sha256_hex(successor)
    result = {
        'schema': STEP7_RESULT_SCHEMA, 'kind': 'CUSTODY', 'builder': BUILDER_NAME,
        'seq': ledger['n'] + 1, 'previous_result_sha256': ledger['last_sha'],
        'build_record_sha256': ctx['record_pin']['sha256'],
        'replay_plan_sha256': ctx['plan_sha'],
        'pass_one_sha256': None, 'pass_k_sha256': None, 'status': 'NEW_UNEVALUATED',
        'new_unevaluated': [{'alternative': a, 'member_id': m} for a, m in new],
        'stops': [], 'checks': checks, 'successor_replay_plan_sha256': successor_sha,
        'resolution_by_successor_roster': 'NEVER (A133 3 (b))',
    }
    raw = dump_bytes(result)
    plan_path = os.path.join(ledger['dir'], 'PLAN_' + successor_sha + '.json')
    if not os.path.lexists(plan_path):
        write_exclusive(plan_path, successor)
    write_exclusive(os.path.join(ledger['dir'], 'STEP7_%04d.json' % result['seq']), raw)
    return result, raw, successor


# Component: ledger_reader_draft001.py
"""c2v007 ledger reader: CUSTODY entries are re-derived, never trusted."""

def _read_ledger(record, build_sha, root_sha, root_raw):
    """Verify the append-only step-7 ledger of this build record (R3: at its root-fixed path keyed by the record's
    sha256) and return the verified plan chain.

    Every result is re-derived: its pass records (stored in the ledger) are compared again under its predecessor
    plan, and each successor plan must equal, byte for byte, what step 7 makes from its predecessor."""
    ledger_dir = ledger_dir_of(record, build_sha)
    out = {'dir': ledger_dir, 'n': 0, 'last_sha': None, 'results': [], 'plans': {root_sha: root_raw},
           'superseded': []}
    if ledger_dir is None:
        return out
    results, plans, passes = _ledger_files(ledger_dir, build_sha, root_sha)
    seqs = sorted(results)
    if seqs != list(range(1, len(seqs) + 1)):
        raise Refused('STEP7_LEDGER_BROKEN', 'result sequence is not 1..n')
    plan_docs = {root_sha: strict_json(root_raw, 'root replay plan')}
    superseded = set()
    prev = None
    for s in seqs:
        raw = results[s]
        r = strict_json(raw, 'ledger result %d' % s)
        try:
            if r.get('schema') != STEP7_RESULT_SCHEMA or r.get('seq') != s or \
                    r.get('previous_result_sha256') != prev or r.get('build_record_sha256') != build_sha:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d header' % s)
            pred = r.get('replay_plan_sha256')
            if pred not in plan_docs or pred in superseded:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d compares a plan outside the chain or superseded' % s)
            custody_successor = None
            if r.get('kind') == 'CUSTODY':
                new, custody_successor, checks = custody_derivation(plan_docs[pred], pred)
                status, stops = 'NEW_UNEVALUATED', []
                if r.get('pass_one_sha256') is not None or r.get('pass_k_sha256') is not None:
                    raise Refused('STEP7_LEDGER_BROKEN', 'a CUSTODY entry carries no pass records')
            else:
                if r.get('kind') not in (None, 'COMPARE'):
                    raise Refused('STEP7_LEDGER_BROKEN', 'unknown ledger entry kind')
                p1raw, pkraw = passes.get(r.get('pass_one_sha256')), passes.get(r.get('pass_k_sha256'))
                if p1raw is None or pkraw is None:
                    raise Refused('STEP7_LEDGER_BROKEN', 'result %d: a pass record copy is missing' % s)
                status, new, stops, checks = _compare(
                    plan_docs[pred], pred, root_sha, build_sha,
                    strict_json(p1raw, 'ledger pass'), strict_json(pkraw, 'ledger pass'))
            if status != r.get('status') or [{'alternative': a, 'member_id': m} for a, m in new] != \
                    r.get('new_unevaluated') or stops != r.get('stops') or checks != r.get('checks'):
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d does not re-derive from its stored passes' % s)
            if status == 'NEW_UNEVALUATED':
                succ_raw = custody_successor if custody_successor is not None else dump_bytes(_apply_unevaluated(plan_docs[pred], pred, new))
                ssha = sha256_hex(succ_raw)
                if r.get('successor_replay_plan_sha256') != ssha or plans.get(ssha) != succ_raw:
                    raise Refused('STEP7_LEDGER_BROKEN', 'result %d successor is not step 7\'s own change' % s)
                plan_docs[ssha] = strict_json(succ_raw, 'successor')
                out['plans'][ssha] = succ_raw
                superseded.add(pred)
            elif r.get('successor_replay_plan_sha256') is not None:
                raise Refused('STEP7_LEDGER_BROKEN', 'result %d names a successor without NEW_UNEVALUATED' % s)
        except Refused as exc:
            if exc.code in ('STEP7_LEDGER_BROKEN', 'RUN_VOLUME_NOT_MOUNTED'):
                raise
            raise Refused('STEP7_LEDGER_BROKEN', 'result %d: %s' % (s, exc.code))
        out['results'].append(r)
        prev = sha256_hex(raw)
    out.update({'n': len(seqs), 'last_sha': prev, 'superseded': sorted(superseded)})
    return out


# Component: cutoff_rules_draft001.py
"""c2v007 component: machine cutoff bytes and builder-derived terminal time."""

_ENTRY_ISO_STAMP = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z')
_ENTRY_DATE_U_STAMP = re.compile(
    r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+'
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+'
    r'\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+UTC\s+\d{4}')


def cutoff_entry_stamps(raw):
    entries = []
    for line in raw.decode('utf-8').splitlines():
        if not line.startswith('## '):
            continue
        heading = line[3:].strip()
        stamps = _ENTRY_ISO_STAMP.findall(heading) + _ENTRY_DATE_U_STAMP.findall(heading)
        times = {parse_utc_ns(s, 'cutoff entry timestamp') for s in stamps}
        if len(times) > 1:
            raise Refused('GATE_CUTOFF_ENTRY_TIME_AMBIGUOUS', heading)
        entries.append({
            'heading': heading,
            'time_ns': next(iter(times)) if times else None,
        })
    return entries


def _terminal_receipt_pins(resolved, others):
    unique = {}
    for terminal in [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]:
        pin = terminal['receipt']
        unique[(pin['path'], pin['sha256'])] = pin
    return [unique[k] for k in sorted(unique)]


def check_cutoff(doc, resolved, others, cut_raw, cutoff_pin, gate_pins, files):
    if doc['phase'] != 'PHASE_1' or doc['stage'] != 'FULL':
        return None
    supplied = doc['gate_cutoff'].get('record')
    record, norm, _ = read_json_pin(supplied, 'gate_cutoff.record')
    if not isinstance(record, dict) or record.get('schema') != 'STEP4_CUTOFF_RECORD_C2V001':
        raise Refused('GATE_CUTOFF_RECORD_SCHEMA')
    step4 = _step4(doc['phase'], resolved, others)
    terminal_time = parse_utc_ns(step4['start_utc'], 'derived terminal time')
    record_time = parse_utc_ns(record.get('date_u'), 'cutoff record date_u')
    if record_time < terminal_time:
        raise Refused('GATE_CUTOFF_BEFORE_T', step4['start_utc'])
    copy = record.get('copy')
    if not isinstance(copy, dict) or copy.get('sha256') != cutoff_pin['sha256'] or \
            copy.get('bytes') != len(cut_raw) or \
            not isinstance(copy.get('path'), str) or \
            os.path.realpath(copy['path']) != cutoff_pin['path']:
        raise Refused('GATE_CUTOFF_COPY_BINDING')
    expected_pins = _terminal_receipt_pins(resolved, others)
    receipts = record.get('terminal_attempt_receipts')
    if not isinstance(receipts, list) or \
            sorted(canonical_bytes(p) for p in receipts) != \
            sorted(canonical_bytes(p) for p in expected_pins):
        raise Refused('GATE_CUTOFF_TERMINAL_RECEIPTS')
    if record.get('supersedes') is not None:
        previous, previous_pin, _ = read_json_pin(record['supersedes'], 'cutoff predecessor')
        if not isinstance(previous, dict) or previous.get('schema') != 'STEP4_CUTOFF_RECORD_C2V001' or \
                previous.get('supersedes') is not None or \
                previous_pin == norm or \
                parse_utc_ns(previous.get('date_u'), 'cutoff predecessor date_u') >= terminal_time:
            raise Refused('GATE_CUTOFF_SUCCESSOR_NOT_SINGLE')
        if record.get('T') != step4['start_utc']:
            # A successor is root's correction using the builder's exact T.
            if parse_utc_ns(record.get('T'), 'cutoff successor T') != terminal_time:
                raise Refused('GATE_CUTOFF_SUCCESSOR_T')
    stamps = cutoff_entry_stamps(cut_raw)
    after = [e for e in stamps if e['time_ns'] is not None and e['time_ns'] > terminal_time]
    after_heads = {e['heading'].lower() for e in after}
    first = v006_index(cut_raw)
    for gate in gate_pins:
        if first.get(gate['sha256']) in after_heads:
            raise Refused('GATE_FIRST_PIN_AFTER_TERMINAL_T', gate['sha256'])
    # The output copy is the same buffer that passed its pin and record checks.
    files['GATE_CUTOFF_V006_COPY.md'] = cut_raw
    return {
        'record': norm,
        'T': step4['start_utc'],
        'record_date_u': record['date_u'],
        'terminal_attempt_receipts': expected_pins,
        'v006_copy': cutoff_pin,
        'after_T_entries': [
            {'heading': e['heading'], 'utc': format_utc_ns(e['time_ns'])} for e in after
        ],
        'unstamped_headings': [e['heading'] for e in stamps if e['time_ns'] is None],
        'rule': 'T is re-derived from every terminal attempt; later-stamped first gate pins are excluded',
    }


# Component: registry_rules_draft004.py
"""c2v007 component: source-derived launch registry verification.

Phase 1 invokes only the pinned P112 read-only verification path. Its writing
functions are disabled. Phase 2 checks the same registry's five-key entries
against the ordered, pinned per-call source entries.
"""

P112_REVIEWED_SHA = '7a4fefede8551176c6973a08b0a0f36b4d88b57b61e84e841c7dee283c9b6284'
P112_REVIEWED_SHAS = frozenset((P112_REVIEWED_SHA,
    '8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9'))


def _registry_context_factory(module, config_pin):
    return module.Context(config_pin)


def _p112_verifier_module(pin):
    raw, norm = read_bytes_pin(pin, 'registry verifier')
    if norm['sha256'] not in P112_REVIEWED_SHAS:
        raise Refused('REGISTRY_VERIFIER_PIN')
    module = types.ModuleType('p112_registry_verifier_' + norm['sha256'][:16])
    module.__file__ = norm['path']
    exec(compile(raw, norm['path'], 'exec'), module.__dict__)

    def read_and_pin(path, decode=True):
        path = str(path)
        module.guard_read(path)
        with snapshot_scope() as snapshot:
            raw, _ = snapshot.read(path, 'P112 registry input', require_nonempty=False)
        actual = {'path': path, 'sha256': sha256_hex(raw)}
        return actual, module.strict_json(raw) if decode else raw

    def observe_file(path, kind, *, v006=False):
        path = str(path)
        if v006 and path == module.V006:
            module.need(os.path.realpath(path) == path, 'V006_PATH')
        else:
            module.guard_record(path)
        with snapshot_scope() as snapshot:
            raw, _ = snapshot.read(path, 'P112 registry observation', require_nonempty=False)
        actual = {'path': path, 'sha256': sha256_hex(raw)}
        context = module._READ_CONTEXT.get()
        if context is not None:
            report = context['observations']
            report['counts'][kind] = report['counts'].get(kind, 0) + 1
            report['last_observation'][kind] = {
                'kind': kind, 'pin': actual, 'bytes': len(raw),
            }
        return raw, actual

    def no_write(*args, **kwargs):
        raise Refused('REGISTRY_VERIFIER_WRITE_REFUSED')

    module.read_and_pin = read_and_pin
    module.observe_file = observe_file
    module.write_x = no_write
    module.write_x_bytes = no_write
    return module


@command_snapshot
def verify_launch_registry(doc):
    phase = doc['phase']
    registry_raw, registry_pin = read_bytes_pin(doc['launch_registry'], 'launch registry verify')
    verification = doc.get('registry_verification')
    if phase == 'PHASE_1':
        _keys(verification, ('launcher', 'config', 'assembly_record'), 'registry_verification')
        module = _p112_verifier_module(verification['launcher'])
        try:
            ctx = _registry_context_factory(module, verification['config'])
            with snapshot_scope():
                checked = module.assemble_registry(ctx, verify=True)
                derived_raw, derived = module.registry_bytes(ctx)
        except module.Refusal as exc:
            raise Refused(exc.code, str(exc.detail)) from None
        if checked['registry'] != registry_pin or derived_raw != registry_raw:
            raise Refused('REGISTRY_BYTE_VERIFY')
        assembly, assembly_pin, _ = read_json_pin(
            verification['assembly_record'], 'registry assembly record')
        if not isinstance(assembly, dict) or \
                assembly.get('schema') != 'STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001' or \
                assembly.get('registry') != registry_pin:
            raise Refused('REGISTRY_ASSEMBLY_RECORD')
        stable = ('sources', 'plan_output_primary', 'fdplan', 'selection', 'plan_build_record',
                  's0_member_mappings', 'excluded_serials', 'nonattempts')
        if any(assembly.get(key) != derived.get(key) for key in stable):
            raise Refused('REGISTRY_ASSEMBLY_NOT_REDERIVED')
        if assembly['plan_output_primary'] != doc['plan_outputs'].get(ctx.cfg.get('primary', 'BR_A_F10_PRIMARY')):
            raise Refused('REGISTRY_PLAN_OUTPUT_BINDING')
        for pin in assembly['sources']:
            read_bytes_pin(pin, 'registry assembly source')
        # G15 includes every seed/twin launch JSON, including non-attempt
        # and RESIDUAL_RETRY records. Files absent at launch add no receipt.
        m15_launch_receipts = {}
        for name in ('S0_SEED_SERIAL', module.TWIN):
            for record in ctx.records(name):
                launch_pin = record.get('launch_json')
                if launch_pin is None:
                    continue
                path = launch_pin.get('path') if isinstance(launch_pin, dict) else None
                if not isinstance(path, str) or not os.path.isabs(path):
                    raise Refused('M15_LAUNCH_SOURCE_PIN')
                if not os.path.lexists(path):
                    continue
                launch_raw, real = _read_regular(path, 'seed/twin launch JSON')
                actual = {'path': real, 'sha256': sha256_hex(launch_raw)}
                if launch_pin.get('sha256') not in (None, actual['sha256']):
                    raise Refused('M15_LAUNCH_SOURCE_PIN')
                launch = strict_json(launch_raw, 'seed/twin launch JSON')
                parse_utc_ns(launch.get('utc'), 'seed/twin launch JSON utc')
                m15_launch_receipts[real] = actual
        return {
            'mode': 'P112_READ_ONLY_VERIFY',
            'fdplan': assembly['fdplan'],
            'm15_launch_receipts': [m15_launch_receipts[k] for k in sorted(m15_launch_receipts)],
            'registry': registry_pin,
            'assembly_record': assembly_pin,
            'sources': assembly['sources'],
            'nonattempts': assembly['nonattempts'],
            's0_member_mappings': assembly['s0_member_mappings'],
            'verdict': 'BYTE_EQUAL',
        }
    _keys(verification, ('entries',), 'registry_verification')
    if not isinstance(verification['entries'], list):
        raise Refused('REGISTRY_SOURCES_REQUIRED')
    _launch_registry(doc['launch_registry'], phase)
    registered = strict_json(registry_raw, 'phase-2 launch registry')['calls']
    if len(registered) != len(verification['entries']):
        raise Refused('REGISTRY_SOURCE_COUNT')
    calls, sources = [], []
    source_calls = {}
    for declared, pin in zip(registered, verification['entries']):
        entry, norm, _ = read_json_pin(pin, 'registry source entry')
        if not isinstance(entry, dict) or entry.get('schema') != 'UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001':
            raise Refused('REGISTRY_SOURCE_SCHEMA')
        spec = entry.get('spec')
        if not isinstance(spec, dict) or not _is_hex64(spec.get('sha256')):
            raise Refused('REGISTRY_SOURCE_SPEC')
        source = {
            'alternative': entry.get('alternative'), 'kind': entry.get('kind'),
            'key': entry.get('key'), 'theta_sha256': entry.get('theta_sha256'),
            'spec_sha256': spec['sha256'],
        }
        alias = (declared['kind'] == 'SENSITIVITY' and
                 source['kind'] in ('MEMBER', 'SENSITIVITY') and
                 all(declared[k] == source[k] for k in
                     ('alternative', 'theta_sha256', 'spec_sha256')))
        if declared != source and not alias:
            raise Refused('REGISTRY_SOURCE_CALL_BINDING')
        # The originating call itself must also be in this phase's registry.
        # The sensitivity plan independently fixes the alias id and theta.
        if alias and source not in registered:
            raise Refused('REGISTRY_ALIAS_ORIGIN_MISSING')
        previous = source_calls.setdefault(norm['path'], source)
        if previous != source:
            raise Refused('REGISTRY_SOURCE_CALL_BINDING')
        calls.append(dict(declared))
        if norm not in sources:
            sources.append(norm)
    rebuilt = dump_bytes({'schema': LAUNCH_REGISTRY_SCHEMA, 'phase': phase, 'calls': calls})
    if rebuilt != registry_raw:
        raise Refused('REGISTRY_BYTE_VERIFY')
    return {
        'mode': 'ORDERED_SOURCE_ENTRIES', 'registry': registry_pin,
        'sources': sources, 'nonattempts': [], 's0_member_mappings': [],
        'verdict': 'BYTE_EQUAL',
    }


# Component: assemble_draft005.py
def _assemble(doc, fm, out_real):
    phase, stage = doc['phase'], doc['stage']
    slots, slots_pin, _ = read_json_pin(doc['slots'], 'slots')
    try:
        alts = slots['alternatives']
        declared, primary = alts['declared'], alts['primary']
        rows = slots['query_block']['rows']
    except (KeyError, TypeError):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared/primary and query_block.rows are required')
    if not isinstance(declared, list) or not declared or not all(isinstance(a, dict) for a in declared):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared')
    names = [a.get('name') for a in declared]
    if not all(isinstance(n, str) and ALT_NAME_RE.match(n) for n in names) or len(set(names)) != len(names):
        raise Refused('SLOTS_ALTERNATIVE_NAMES', 'names must be unique file-safe strings')
    if any(a.get('status') not in (ALT_EVALUATED, ALT_NOT_EVALUATED) for a in declared):
        raise Refused('SLOTS_ALTERNATIVE_STATUS', 'every status is EVALUATED_ or NOT_EVALUATED_BEFORE_FREEZE')
    by_name = {a['name']: a for a in declared}
    if primary not in by_name or by_name[primary]['status'] != ALT_EVALUATED:
        raise Refused('SLOTS_PRIMARY', 'the primary must be declared EVALUATED_BEFORE_FREEZE')
    _qraw, qm_pin = read_bytes_pin(doc['query_manifest'], 'query_manifest')
    qm = fm.load_query_manifest(path=qm_pin['path'], expected_sha256=qm_pin['sha256'])
    if not isinstance(qm, dict) or not qm.get('ok'):
        raise Refused('QUERY_MANIFEST_REFUSED', 'load_query_manifest did not accept the pinned manifest')
    ids = list(qm['query_ids'])
    if len(ids) != 43 or not isinstance(rows, list) or len(rows) != 43:
        raise Refused('QUERY_COUNT', '43 query ids and 43 slots query rows are required')
    scope = 'PROGRAM' if qm_pin['sha256'] == fm.PROGRAM_QUERY_MANIFEST_SHA256 else 'SYNTHETIC_FIXTURE'
    mapping = [{'query_id': q, 'slots_query_id': s.get('query_id') if isinstance(s, dict) else None}
               for q, s in zip(ids, rows)]
    if scope == 'PROGRAM' and any(m['query_id'] != m['slots_query_id'] for m in mapping):
        raise Refused('PROGRAM_QUERY_ID_MISMATCH', 'program scope requires equal query ids')
    evaluated = [n for n in names if by_name[n]['status'] == ALT_EVALUATED]
    if phase == 'PHASE_1' and STAGE0_NAME in evaluated:
        raise Refused('PHASE1_STAGE0_NOT_IN_PHASE_1', 'Phase 1 runs under slots in which STAGE0 is not evaluated')
    spec, spec_pin, _ = read_json_pin(doc['spec_of_record'], 'spec_of_record')
    geometry = registered_geometry(spec, fm)
    geometry_answers = {}
    run_alts = [primary] if phase == 'PHASE_1' else list(evaluated)
    roster_files = {n: 'ROSTER_%s.json' % n for n in names}
    files = {}
    checks = []

    def roster_pins_of(roster_bytes):
        return {n: {'path': os.path.join(out_real, roster_files[n]), 'sha256': sha256_hex(roster_bytes[n])}
                for n in names}

    if stage == 'PLAN':
        roster_bytes = {n: dump_bytes(_roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, [], []))
                        for n in names}
        for n in names:
            files[roster_files[n]] = roster_bytes[n]
            checks.append((n, roster_files[n], []))
        files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': 'PLAN', 'phase': phase,
                                                'row_registration_rosters': roster_pins_of(roster_bytes)})
        return files, checks, ids

    # ---------------- MEMBERS / FULL ----------------
    cfg = _receipt_cfg(doc['receipt_keys'], doc['receipt_status_classes'])
    registry, registry_pin = _launch_registry(doc['launch_registry'], phase)
    registry_proof = verify_launch_registry(doc)
    if phase == 'PHASE_1' and stage == 'FULL' and doc.get('m15') is not None:
        supplied_launches = doc['m15'].get('launch_receipts')
        expected_launches = registry_proof['m15_launch_receipts']
        if not isinstance(supplied_launches, list):
            raise Refused('M15_LAUNCH_RECEIPT_REQUIRED')
        actual_launches = [read_bytes_pin(p, 'm15 launch coverage')[1] for p in supplied_launches]
        if sorted(canonical_bytes(p) for p in actual_launches) != sorted(
                canonical_bytes(p) for p in expected_launches):
            raise Refused('M15_LAUNCH_SET_NOT_COMPLETE')
    used_entries = set()

    # gates: pinned in the phase's cutoff V006 bytes, never chosen here
    gc = doc['gate_cutoff']
    _keys(gc, ('kind', 'v006_copy'), 'gate_cutoff',
          optional=('record',) if phase == 'PHASE_1' and stage == 'FULL' else ())
    if gc['kind'] != CUTOFF_KIND[phase]:
        raise Refused('GATE_CUTOFF_KIND', 'phase %s requires cutoff %s' % (phase, CUTOFF_KIND[phase]))
    cut_raw, cutoff_pin = read_bytes_pin(gc['v006_copy'], 'gate_cutoff.v006_copy')
    cutoff_heads = v006_index(cut_raw)
    head_names = _original_headings(cut_raw)
    if not isinstance(doc['gate_documents'], list):
        raise Refused('GATE_LIST_REQUIRED', 'gate_documents must be a list (possibly empty)')
    gate_pins, pairs, gate_seen = [], set(), set()
    for i, gp in enumerate(doc['gate_documents']):
        w = 'gate_documents[%d]' % i
        gd, gnorm, _ = read_json_pin(gp, w)
        if gnorm['sha256'] in gate_seen:
            raise Refused('GATE_DUPLICATE', w)
        gate_seen.add(gnorm['sha256'])
        _gate_doc_ok(gd, ids, w, fm)
        if gnorm['sha256'] not in cutoff_heads:
            raise Refused('GATE_NOT_PINNED_IN_CUTOFF_V006',
                          '%s: its full sha256 is not in the phase cutoff V006 bytes; it is not a builder input' % w)
        for q in gd['query_ids']:
            for r in gd['registered_reasons']:
                if (q, r) in pairs:
                    raise Refused('GATE_AMBIGUOUS', '%s: (%s, %s) is listed twice' % (w, q, r))
                pairs.add((q, r))
        gate_pins.append(gnorm)
    gate_pins.sort(key=lambda p: (p['sha256'], p['path']))

    # exact thetas from the value-free plan outputs
    po = doc['plan_outputs']
    if not isinstance(po, dict) or set(po) != set(evaluated):
        raise Refused('PLAN_OUTPUTS_SET', 'one budget-0 evaluate_envelopes output per EVALUATED alternative')
    plan_members, plan_out_pins = {}, {}
    for n in evaluated:
        pdoc, pnorm, _ = read_json_pin(po[n], 'plan_outputs.' + n)
        plan_members[n] = _value_free_members(pdoc, ids, 'plan_outputs.' + n)
        plan_out_pins[n] = pnorm
    ref_list = [(m[0], m[1], m[2]) for m in plan_members[primary]]
    for n in evaluated:
        if [(m[0], m[1], m[2]) for m in plan_members[n]] != ref_list:
            raise Refused('PLAN_MEMBER_LISTS_DIFFER', n + ': every evaluated alternative has the PRIMARY members (D2)')
    sens_entries = []
    sens_pin = None
    if stage == 'FULL':
        spo = doc['sensitivity_plan_output']
        if phase == 'PHASE_1':
            if spo is not None:
                raise Refused('PHASE1_SENSITIVITY_NOT_RUN', 'Phase 1 runs sensitivity at budget 0 (A133 1.4)')
        else:
            if spo is None:
                raise Refused('SENSITIVITY_PLAN_REQUIRED', 'Phase-2 FULL needs the budget-0 sensitivity plan')
            sdoc, sens_pin, _ = read_json_pin(spo, 'sensitivity_plan_output')
            sens_entries = _value_free_sensitivity(sdoc, ids, 'sensitivity_plan_output')
            geometry_answers = geometry_exemptions(sens_entries, geometry)
    if stage == 'MEMBERS' and phase == 'PHASE_1':
        raise Refused('PHASE1_STAGE', 'Phase 1 builds FULL directly (no sensitivity calls exist in Phase 1)')

    # calls: rule (c) terminal receipts, rule (f) caps, run-produced cut records
    if not isinstance(doc['calls'], list):
        raise Refused('CALLS_REQUIRED', 'calls must be a list')
    member_theta = {(n, m[0]): m[3] for n in evaluated for m in plan_members[n]}
    if any(geometry_differs(theta, geometry) for theta in member_theta.values()):
        raise Refused('NONREGISTERED_GEOMETRY_ON_OTHER_KIND', 'planned member')
    sens_theta = {e[0]: e[1] for e in sens_entries
                  if not e[2] and theta_sha256(e[1]) not in geometry_answers}
    resolved = {}
    for i, c in enumerate(doc['calls']):
        w = 'calls[%d]' % i
        if not isinstance(c, dict):
            raise Refused('CALL_SHAPE', w)
        if 'cut_record' not in c:
            raise Refused('CUT_CONTEXT_MISSING',
                          '%s: every evaluated call carries its own cut record pin or an explicit null' % w)
        _keys(c, ('alternative', 'kind', 'key', 'attempts', 'result', 'cut_record'), w)
        alt, kind, key = c['alternative'], c['kind'], c['key']
        if alt not in run_alts:
            raise Refused('CALL_NOT_REGISTERED_FOR_PHASE', '%s: %r is not run in %s' % (w, alt, phase))
        if kind == 'MEMBER':
            if (alt, key) not in member_theta:
                raise Refused('CALL_NOT_A_PLANNED_MEMBER', w)
            theta = member_theta[(alt, key)]
        elif kind == 'SENSITIVITY':
            if phase != 'PHASE_2' or stage != 'FULL' or alt != primary or key not in sens_theta:
                raise Refused('CALL_NOT_A_PLANNED_SENSITIVITY_ENTRY', w)
            theta = sens_theta[key]
        else:
            raise Refused('CALL_KIND', w)
        if (alt, kind, key) in resolved:
            raise Refused('CALL_DUPLICATE', w)
        entry = registry.get((alt, kind, key))
        if entry is None:
            raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no entry for %s %s %s'
                          % (w, alt, kind, key))
        if entry['theta_sha256'] != theta_sha256(theta):
            raise Refused('LAUNCH_REGISTRY_THETA_MISMATCH', '%s: the registry\'s theta key is not the call\'s exact '
                                                            'theta (PLAN output)' % w)
        used_entries.add((alt, kind, key))
        term = _terminal(c['attempts'], cfg, w, allow_planned=False,
                         binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256'],
                                  'alternative': alt, 'kind': kind, 'key': key})
        result, result_ident = None, None
        if c['result'] is not None:
            # hashed, never parsed (no value is read); its file identity is kept for the cross-call check (c2v004/5)
            _rraw, result, result_ident = read_bytes_pin_ident(c['result'], w + '.result')
            if not _under(term['run_dir'], result['path']):
                raise Refused('RESULT_NOT_OF_ITS_CALL', '%s: the result lies outside the terminal run dir' % w)
        monitor_result = term['source_facts'][-1]['result']
        if result != monitor_result:
            raise Refused('RESULT_NOT_MONITOR_PIN', w)
        if term['class'] == 'FINISHED' and result is None:
            raise Refused('FINISHED_WITHOUT_RESULT', w)
        cut, cut_ident = None, None
        if c['cut_record'] is not None:
            cd, cut, _, cut_ident = read_json_pin_ident(c['cut_record'], w + '.cut_record')
            if not _under(term['run_dir'], cut['path']):
                raise Refused('CUT_RECORD_NOT_OF_ITS_CALL', '%s: the cut record lies outside its call\'s terminal run '
                                                            'dir (G29: bound to its call by residence)' % w)
            _cut_doc_ok(cd, w + '.cut_record', fm)
        disposition = DISPOSITION_OF[term['class']]
        rec = {'alternative': alt, 'kind': kind, 'key': key, 'theta': theta, 'theta_sha256': theta_sha256(theta),
               'terminal': term, 'result': result, 'cut': cut, 'disposition': disposition,
               'result_ident': result_ident, 'cut_ident': cut_ident,
               'signature': canonical_bytes([c['attempts'], c['result'], c['cut_record']])}
        if fm._canonical_bytes(theta) != canonical_bytes(theta):
            raise Refused('CANONICAL_FORM_DIVERGES', w)
        resolved[(alt, kind, key)] = rec
    # the phase's non-roster NGC calls (F points, the identity twin): FULL only; bound to the registry like any call
    others = []
    if stage == 'FULL':
        oc_list = doc['other_phase_calls']
        if not isinstance(oc_list, list):
            raise Refused('OTHER_PHASE_CALLS', 'a list (possibly empty) of non-roster NGC calls of the phase')
        labels = set()
        for i, oc in enumerate(oc_list):
            w = 'other_phase_calls[%d]' % i
            _keys(oc, ('label', 'attempts'), w)
            if not isinstance(oc['label'], str) or not oc['label'] or oc['label'] in labels:
                raise Refused('OTHER_CALL_LABEL', w)
            labels.add(oc['label'])
            entry = registry.get((None, 'OTHER', oc['label']))
            if entry is None:
                raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no OTHER entry %r'
                              % (w, oc['label']))
            used_entries.add((None, 'OTHER', oc['label']))
            term = _terminal(oc['attempts'], cfg, w, allow_planned=True,
                             binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256'],
                                      'alternative': None, 'kind': 'OTHER', 'key': oc['label']})
            others.append({'label': oc['label'], 'terminal': term})
    source_entries = {canonical_bytes(p) for p in registry_proof['sources']}
    for terminal in [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]:
        for facts in terminal['source_facts']:
            if canonical_bytes(facts['registry_entry']) not in source_entries:
                raise Refused('RECEIPT_REGISTRY_SOURCE_NOT_ASSEMBLED')
    unused = sorted('%s:%s:%s' % k for k in registry if k not in used_entries)
    if unused:
        raise Refused('LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL', 'registry entries with no call record in this build '
                                                            'input: %s' % unused[:5])
    # one call per (alternative, exact theta); identical call records only (A133: an equal theta is the same call)
    by_theta = {}
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in by_theta and by_theta[k]['signature'] != rec['signature']:
            raise Refused('CONTEXT_CONFLICT', '%s: two different call records at one exact theta' % rec['alternative'])
        by_theta.setdefault(k, rec)
    # R2: one receipt serves one call, across every roster and non-roster call of this build input
    _cross_call_receipts([(('CALL', k[0], k[1]), rec['terminal']) for k, rec in sorted(by_theta.items())] +
                         [(('OTHER', o['label']), o['terminal']) for o in others])
    # c2v005: one run file (by realpath or file identity) serves one call, across every roster AND OTHER call of this
    # build input; one FINISHED-result content (by sha256) serves one call (C38)
    _cross_call_files([(('CALL', k[0], k[1]), _roster_call_files(rec)) for k, rec in sorted(by_theta.items())] +
                      [(('OTHER', o['label']), _other_call_files(o['terminal'])) for o in others])
    # c2v005 (G29): a cut record lies in no run directory of another call (its own terminal run directory was checked
    # per call above)
    _cut_record_residence([(('CALL', k[0], k[1]), rec['terminal'], rec['cut']) for k, rec in sorted(by_theta.items())]
                          + [(('OTHER', o['label']), o['terminal'], None) for o in others])
    # completeness: every call the phase registers has a terminal receipt before step 4
    for n in run_alts:
        for m in plan_members[n]:
            if (n, 'MEMBER', m[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', '%s %s has no terminal call record' % (n, m[0]))
    if phase == 'PHASE_2' and stage == 'FULL':
        for e in sens_entries:
            if not e[2] and theta_sha256(e[1]) not in geometry_answers and (primary, 'SENSITIVITY', e[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', 'sensitivity %s has no terminal call record' % e[0])

    # contexts (members in member order, then sensitivity entries in plan order; equal thetas once)
    contexts = {n: [] for n in names}
    ctx_theta = {n: [] for n in names}
    for n in run_alts:
        seen = set()
        order = [resolved[(n, 'MEMBER', m[0])] for m in plan_members[n]]
        if n == primary and stage == 'FULL' and phase == 'PHASE_2':
            order += [resolved[(n, 'SENSITIVITY', e[0])] for e in sens_entries
                      if not e[2] and theta_sha256(e[1]) not in geometry_answers]
        for rec in order:
            if rec['disposition'] not in EVALUATED_DISPOSITIONS or rec['theta_sha256'] in seen:
                continue
            seen.add(rec['theta_sha256'])
            contexts[n].append({'theta_ngc': rec['theta'], 'cut': rec['cut']})
            ctx_theta[n].append(rec['theta'])
    roster_docs = {n: _roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, list(gate_pins), contexts[n])
                   for n in names}
    roster_bytes = {n: dump_bytes(roster_docs[n]) for n in names}
    for n in names:
        files[roster_files[n]] = roster_bytes[n]
        checks.append((n, roster_files[n], ctx_theta[n]))
    rpins = roster_pins_of(roster_bytes)
    files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': stage, 'phase': phase,
                                            'row_registration_rosters': rpins})

    # Phase-2 FULL: member contexts byte-identical to the MEMBERS stage (the step-7 D1 check holds by construction),
    # and the MEMBERS-stage build record binds the pass-one replay plan (step 7 checks pass one against it)
    pass_one_sha = {n: rpins[n]['sha256'] for n in names}
    pass_one_members_plan = None
    if stage == 'FULL':
        msr, mbr = doc['members_stage_rosters'], doc['members_stage_build_record']
        if phase == 'PHASE_1':
            if msr is not None or mbr is not None:
                raise Refused('PHASE1_STAGE', 'Phase 1 has no MEMBERS-stage rosters or build record')
        else:
            if not isinstance(msr, dict) or set(msr) != set(names):
                raise Refused('MEMBERS_STAGE_ROSTERS_REQUIRED', 'one MEMBERS-stage roster pin per alternative')
            mrec, mrnorm = _build_record_of(mbr, 'members_stage_build_record', 'MEMBERS', 'PHASE_2')
            for n in names:
                if not isinstance(msr[n], dict) or mrec['outputs'].get(roster_files[n]) != msr[n].get('sha256'):
                    raise Refused('MEMBERS_STAGE_ROSTERS_NOT_OF_RECORD', n)
            mplan, mpnorm, _ = read_json_pin(
                {'path': os.path.join(os.path.dirname(mrnorm['path']), 'REPLAY_PLAN.json'),
                 'sha256': mrec['outputs']['REPLAY_PLAN.json']}, 'members-stage REPLAY_PLAN.json')
            pass_one_members_plan = {
                'stage': 'MEMBERS', 'build_record_sha256': mrnorm['sha256'],
                'replay_plan_sha256': mpnorm['sha256'],
                'member_budget': {a['name']: a['member_budget'] for a in mplan['alternatives']
                                  if a['slots_status'] == ALT_EVALUATED},
                'sensitivity_budget': mplan['sensitivity']['budget']}
            for n in names:
                mdoc, mnorm, _ = read_json_pin(msr[n], 'members_stage_rosters.' + n)
                full = roster_docs[n]
                for k in ('schema', 'scope', 'alternative', 'slots', 'query_manifest', 'query_mapping', 'root_gates'):
                    if mdoc.get(k) != full[k]:
                        raise Refused('MEMBER_CONTEXTS_CHANGED', '%s: %s differs from the MEMBERS stage' % (n, k))
                mc = mdoc.get('outer_cut', {}).get('contexts', []) if isinstance(mdoc.get('outer_cut'), dict) else None
                fc = full['outer_cut'].get('contexts', [])
                if mc is None or len(mc) > len(fc) or \
                        any(canonical_bytes(a) != canonical_bytes(b) for a, b in zip(mc, fc)):
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member contexts must be byte-identical')
                n_member_ctx = sum(1 for _ in contexts_member_prefix(resolved, plan_members, n))
                if len(mc) != n_member_ctx:
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member context count differs')
                pass_one_sha[n] = mnorm['sha256']

    # replay plan (rules (b), (c), (f))
    alt_plan, replay_index = [], {}
    for n in names:
        a = {'name': n, 'slots_status': by_name[n]['status'], 'run_in_phase': n in run_alts,
             'mode': roster_docs[n]['outer_cut']['mode'], 'member_budget': None, 'members': []}
        if n in evaluated:
            budget = None
            for idx, m in enumerate(plan_members[n]):
                if n in run_alts:
                    rec = resolved[(n, 'MEMBER', m[0])]
                    own, cls, nat = rec['disposition'], rec['terminal']['class'], rec['terminal']['n_attempts']
                    rule_c = rec['terminal']['rule_c']
                else:
                    own, cls, nat, rule_c = 'NOT_RUN_PHASE1_BUDGET0', None, 0, None
                if budget is None and own not in EVALUATED_DISPOSITIONS:
                    budget = idx
                a['members'].append({'member_id': m[0], 'log_index': m[1], 'role': m[2], 'order': idx, 'theta_sha256': theta_sha256(m[3]),
                                     'own_disposition': own, 'terminal_class': cls, 'n_attempts': nat,
                                     'rule_c': rule_c})
            a['member_budget'] = len(plan_members[n]) if budget is None else budget
            _effective(a)
        alt_plan.append(a)
        if n in run_alts:
            idx_entries, seen = [], {}
            for rec in resolved.values():
                if rec['alternative'] != n:
                    continue
                key = rec['theta_sha256']
                if key in seen:
                    seen[key]['call_keys'].append('%s:%s' % (rec['kind'], rec['key']))
                    seen[key]['call_keys'].sort()
                    continue
                e = {'theta_sha256': key, 'call_keys': ['%s:%s' % (rec['kind'], rec['key'])],
                     'disposition': rec['disposition'], 'result': rec['result']}
                seen[key] = e
                idx_entries.append(e)
            idx_entries.sort(key=lambda e: e['theta_sha256'])
            replay_index[n] = idx_entries
    if phase == 'PHASE_1' or stage == 'MEMBERS':
        sens = {'budget': 0, 'entries': [],
                'budget_rule': ('Phase 1: budget 0 (A133 1.4 and 1.6 step 5)' if phase == 'PHASE_1' else
                                'Phase-2 pass one: budget 0 (the plan exists only after D1; RUNBOOK step 2b)')}
    else:
        entries, budget, stopped = [], 0, False
        for e in sens_entries:
            if e[2]:
                entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': True,
                                'own_disposition': 'SKIPPED_ZERO_DISPLACEMENT', 'effective_disposition':
                                'SKIPPED_ZERO_DISPLACEMENT'})
                continue
            own = (GEOMETRY_DISPOSITION if theta_sha256(e[1]) in geometry_answers else
                   resolved[(primary, 'SENSITIVITY', e[0])]['disposition'])
            if not stopped and (own in EVALUATED_DISPOSITIONS or own == GEOMETRY_DISPOSITION):
                budget += 1
                eff = own
            elif not stopped:
                eff, stopped = own, True
            else:
                eff = 'UNEVALUATED_BY_ORDER_TRUNCATION' if own in EVALUATED_DISPOSITIONS else own
            entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': False,
                            'own_disposition': own, 'effective_disposition': eff})
        sens = {'budget': budget, 'entries': entries, 'plan_output': sens_pin,
                'budget_rule': SENS_BUDGET_RULE}
    pass_one = None
    if stage == 'FULL':
        pass_one = pass_one_members_plan or {
            'stage': 'FULL', 'build_record_sha256': None, 'replay_plan_sha256': None,
            'member_budget': {a['name']: a['member_budget'] for a in alt_plan if a['slots_status'] == ALT_EVALUATED},
            'sensitivity_budget': sens['budget'],
            'note': 'Phase 1: pass one runs under this build\'s own (chain-root) replay plan; null shas mean that plan'}
    plan = {'schema': REPLAY_PLAN_SCHEMA, 'builder': BUILDER_NAME, 'phase': phase, 'stage': stage,
            'primary': primary, 'predecessor_sha256': None,
            'registered_roster_sha256': {n: rpins[n]['sha256'] for n in names},
            'pass_one_roster_sha256': pass_one_sha, 'pass_one': pass_one,
            'plan_outputs': plan_out_pins, 'launch_registry': registry_pin, 'alternatives': alt_plan,
            'sensitivity': sens, 'replay_index': replay_index, 'rules': RULE_TEXT, 'step4': None,
            'stage0_status': None,
            'registered_geometry': geometry, 'geometry_not_exposed': geometry_answers,
            'spec_of_record': spec_pin, 'registry_verification': registry_proof,
            'custody': check_custody_inputs(doc['custody'], resolved, others)}

    if stage == 'FULL':
        report = _gate_status_list(doc['m15'], gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names,
                                   cfg)
        files['GATE_STATUS_REPORT.json'] = dump_bytes(report)
        files['GATE_STATUS_LIST.json'] = dump_bytes(a_gate_status_list(report))
        plan['step4'] = _step4(phase, resolved, others)
        plan['stage0_status'] = _stage0_status(phase, by_name, resolved, plan['step4'])
    plan['allow_incomplete'] = allow_incomplete_value(plan)
    plan['gate_cutoff_evidence'] = check_cutoff(
        doc, resolved, others, cut_raw, cutoff_pin, gate_pins, files)
    files['REPLAY_PLAN.json'] = dump_bytes(plan)
    return files, checks, ids

def _value_free_sensitivity(doc, ids, where):
    """A saved budget-0 evaluate_sensitivity plan: whitelisted keys only, exact thetas, no NGC value."""
    if not isinstance(doc, dict) or doc.get('ok') is not True or doc.get('budget') != 0 or \
            doc.get('evaluations_used') != 0:
        raise Refused('SENSITIVITY_PLAN_NOT_BUDGET0', where)
    extra = sorted(k for k in doc if k not in SENS_PLAN_TOP_KEYS)
    if extra or doc.get('per_query') != [] or doc.get('per_target') != []:
        raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE',
                      where + ': save only the whitelisted keys, with per_query and per_target empty (RUNBOOK '
                              'step 2b; the pass command writes this form)')
    ev = doc.get('evaluations')
    if not isinstance(ev, list):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where)
    out = []
    for e in ev:
        if not isinstance(e, dict) or any(k not in SENS_PLAN_ENTRY_KEYS for k in e):
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', where + ': an entry carries a key outside the whitelist')
        if e.get('evaluated') is not False or e.get('forward_valid_flag') is not None or \
                e.get('exception') is not None or \
                any(x is not None for x in e.get('speeds_km_s', [0])) or \
                any(x is not None for x in e.get('delta_from_reference_km_s', [0])) or \
                any(x is not False for x in e.get('row_valid', [True])) or \
                any(x is not None for x in e.get('row_registration', [0])):
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', where)
        if not isinstance(e.get('entry_id'), str) or type(e.get('skipped_zero_displacement')) is not bool:
            raise Refused('SENSITIVITY_PLAN_SHAPE', where)
        if not isinstance(e.get('kind'), str):
            raise Refused('SENSITIVITY_PLAN_KIND', where)
        out.append((e['entry_id'], _theta_ok(e.get('theta_ngc'), where),
                    e['skipped_zero_displacement'], e['kind']))
    if len(set(x[0] for x in out)) != len(out):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where + ': duplicate entry_id')
    return out


# Component: pass_driver_draft005.py
def pass_driver(fm, doc):
    """The in-memory pass (RUNBOOK steps 2 and 7). Returns (validity-only pass record, value-free sensitivity plan or
    None, in-memory outputs). Only the first two may be written; the in-memory outputs exist for an in-process
    caller (the step-8 freeze script, after the seal) and are never written or printed by this tool."""
    _keys(doc, PASS_INPUT_KEYS, 'pass input')
    label = doc['pass_label']
    if label not in ('PASS_ONE', 'PASS_K'):
        raise Refused('PASS_LABEL', repr(label))
    ctx = _plan_context(doc['build_record'], doc['replay_plan'], 'pass')
    plan, rec = ctx['plan'], ctx['record']
    share_freeze_snapshot(fm)
    if plan.get('allow_incomplete') is not allow_incomplete_value(plan):
        raise Refused('PLAN_ALLOW_INCOMPLETE_NOT_REDERIVED')
    if ctx['superseded']:
        raise Refused('PASS_PLAN_SUPERSEDED', 'this replay plan already has a NEW_UNEVALUATED step-7 successor')
    if not isinstance(doc['freeze_module'], dict) or rec.get('freeze_module') != doc['freeze_module']:
        raise Refused('PASS_FREEZE_MODULE_NOT_OF_BUILD', 'the pass runs the build record\'s freeze module pin')
    phase, stage = plan['phase'], plan['stage']
    if label == 'PASS_ONE':
        if ctx['plan_sha'] != ctx['root_sha']:
            raise Refused('PASS_ONE_UNDER_A_SUCCESSOR', 'pass one runs under the build record\'s own replay plan')
        if (phase == 'PHASE_1' and stage != 'FULL') or (phase == 'PHASE_2' and stage != 'MEMBERS'):
            raise Refused('PASS_ONE_STAGE', 'pass one: Phase 1 FULL, Phase 2 MEMBERS')
    elif stage != 'FULL':
        raise Refused('PASS_K_STAGE', 'pass k runs under a FULL replay plan or its step-7 successor')
    rp_doc, rp_norm, _ = read_json_pin(doc['roster_pins'], 'roster_pins')
    if rp_norm['sha256'] != rec['outputs']['ROSTER_PINS.json']:
        raise Refused('PASS_ROSTER_PINS_NOT_OF_BUILD', 'ROSTER_PINS.json is not the build record\'s')
    pins = rp_doc.get('row_registration_rosters') if isinstance(rp_doc, dict) else None
    if not isinstance(pins, dict) or set(pins) != set(plan['registered_roster_sha256']):
        raise Refused('PASS_ROSTER_PINS_SHAPE', 'one roster pin per alternative')
    for alt, sha in plan['registered_roster_sha256'].items():
        if not isinstance(pins[alt], dict) or pins[alt].get('sha256') != sha:
            raise Refused('PASS_ROSTER_NOT_REGISTERED', alt)
    sel, snorm, _ = read_json_pin(doc['selection'], 'selection')
    spec, spnorm, _ = read_json_pin(doc['spec'], 'spec')
    if spnorm != plan.get('spec_of_record'):
        raise Refused('PASS_SPEC_NOT_OF_RECORD')
    if not isinstance(sel, dict) or not isinstance(sel.get('points'), list) or not sel['points']:
        raise Refused('PASS_SELECTION_SHAPE', 'the saved select_representative_points output (with its points)')
    primary = plan['primary']
    proster, _pn, _ = read_json_pin(pins[primary], 'primary roster')
    qpin = proster.get('query_manifest') if isinstance(proster, dict) else None
    if not isinstance(qpin, dict):
        raise Refused('PASS_ROSTER_SHAPE', 'primary roster query_manifest')
    qm = fm.load_query_manifest(path=qpin.get('path'), expected_sha256=qpin.get('sha256'))
    if not isinstance(qm, dict) or not qm.get('ok'):
        raise Refused('QUERY_MANIFEST_REFUSED', 'the roster\'s query manifest')
    ids = list(qm['query_ids'])
    log = []
    envs = {}
    for a in plan['alternatives']:
        if a['slots_status'] != ALT_EVALUATED:
            continue
        ev = fm.evaluate_envelopes(forward_ngc=make_replay_adapter(plan, a['name'], log, 'ENVELOPES'),
                                   points=sel['points'], spec=spec, query_ids=ids, budget=a['member_budget'],
                                   row_registration_roster=pins[a['name']])
        if not isinstance(ev, dict) or ev.get('ok') is not True:
            raise Refused('PASS_ENVELOPES_NOT_OK', a['name'])
        envs[a['name']] = ev
    ref = fm.select_reference_member(selection=sel, evaluation=envs[primary])
    if not isinstance(ref, dict) or ref.get('ok') is not True:
        raise Refused('PASS_NO_REFERENCE_MEMBER', 'select_reference_member did not return a reference')
    sb, source = plan['sensitivity']['budget'], 'REPLAY_PLAN'
    if sb is None:
        s0 = fm.evaluate_sensitivity(forward_ngc=_never, reference=ref, selection=sel, spec=spec, query_ids=ids,
                                     null_direction_rule=doc['null_direction_rule'], budget=0,
                                     row_registration_roster=pins[primary])
        if not isinstance(s0, dict) or s0.get('ok') is not True:
            raise Refused('PASS_SENSITIVITY_NOT_OK', 'budget-0 plan')
        entries = [(e['entry_id'], theta_sha256(e['theta_ngc']), e['skipped_zero_displacement'])
                   for e in s0['evaluations']]
        plan = json.loads(json.dumps(plan))
        plan['geometry_not_exposed'] = geometry_exemptions(
            [(e['entry_id'], e['theta_ngc'], e['skipped_zero_displacement'], e['kind'])
             for e in s0['evaluations']], plan['registered_geometry'])
        sb, source = _sens_budget_rule(plan, entries)['budget'], 'SENS_BUDGET_RULE'
    with geometry_runtime(fm, plan):
        sens = fm.evaluate_sensitivity(forward_ngc=make_replay_adapter(plan, primary, log, 'SENSITIVITY'), reference=ref,
                                       selection=sel, spec=spec, query_ids=ids,
                                       null_direction_rule=doc['null_direction_rule'], budget=sb,
                                       row_registration_roster=pins[primary])
    if not isinstance(sens, dict) or sens.get('ok') is not True:
        raise Refused('PASS_SENSITIVITY_NOT_OK', label)
    if any(e['outcome'] == 'RESULT_CUSTODY_BREACH' for e in log):
        raise Refused('PASS_RESULT_CUSTODY_BREACH', 'a registered result no longer verifies from bytes (step 5 '
                                                    'retains them byte-identical); root rules (G16)')
    binding = {'phase': phase, 'plan_stage': stage, 'replay_plan_sha256': ctx['plan_sha'],
               'build_record_sha256': ctx['record_pin']['sha256'], 'builder_sha256': own_pin()['sha256'],
               'freeze_module_sha256': doc['freeze_module']['sha256'], 'selection_sha256': snorm['sha256'],
               'spec_sha256': spnorm['sha256'], 'null_direction_rule': doc['null_direction_rule'],
               'sensitivity_budget_source': source}
    record = pass_record(label, envs, ref, sens, {'schema': SERVE_LOG_SCHEMA, 'entries': log}, binding)
    plan_extract = None
    if label == 'PASS_ONE' and phase == 'PHASE_2':
        plan_extract = value_free_sensitivity_plan(sens, len(ids))
    return record, plan_extract, {'envelopes': envs, 'reference': ref, 'sensitivity': sens}


# Component: tsr_support_draft002.py
"""G7 machine projection. The policy's slots pin is copied, never opened here."""

TSR_SUPPORT_SCHEMA = 'UNT_ROOT_TSR_SUPPORT_CX3V001'
TSR_SUPPORT_INPUT_SCHEMA = 'TSR_SUPPORT_INPUT_C2V007'
TSR_SUPPORT_INPUT_KEYS = (
    'schema', 'build_record', 'replay_plan', 'pass_record', 'fdplan',
    'extractor_policy', 'compare',
)
TSR_SUPPORT_KEYS = (
    'schema', 'mode', 'target_free', 'before_target_access', 'slots_pin',
    'ntest_compare_pin', 'rings', 'point_key', 'rule_id',
)


def _spelling_pin(pin, where):
    _keys(pin, ('path', 'sha256'), where)
    if not isinstance(pin['path'], str) or not os.path.isabs(pin['path']) or \
            not _is_hex64(pin['sha256']):
        raise Refused('PIN_SHAPE', where)
    return dict(pin)


def _tsr_support_projection(policy, compare, compare_pin, fdplan, plan, pass_record):
    """Pure projection, also used after the command's ledger and pin checks."""
    if not isinstance(policy, dict):
        raise Refused('TSR_EXTRACTOR_POLICY_SHAPE')
    slots_pin = _spelling_pin(policy.get('slots'), 'extractor_policy.slots')
    compare_pin = _spelling_pin(compare_pin, 'compare')
    rings = compare.get('failing_TRUNCATION_SHAPE_rings') if isinstance(compare, dict) else None
    if not isinstance(rings, list) or len(rings) != 1 or not isinstance(rings[0], dict) or \
            type(rings[0].get('ordinal')) is not int or rings[0]['ordinal'] != 15 or \
            compare.get('failing_non_TRUNCATION_SHAPE_rings') != []:
        raise Refused('TSR_SUPPORT_COMPARE_RING')
    if not isinstance(fdplan, dict) or fdplan.get('schema') != 'PHASE1_FDPLAN_C2V001' or \
            not isinstance(fdplan.get('members'), list):
        raise Refused('TSR_SUPPORT_FDPLAN')
    reference = pass_record.get('reference') if isinstance(pass_record, dict) else None
    primary = next((a for a in plan['alternatives'] if a['name'] == plan['primary']), None)
    members = [] if primary is None or not isinstance(reference, dict) else [
        m for m in primary['members'] if m['member_id'] == reference.get('member_id')]
    if len(members) != 1 or members[0]['log_index'] != reference.get('log_index'):
        raise Refused('TSR_SUPPORT_D1_MEMBER')
    member = members[0]
    identity = member['log_index'], member.get('role'), member.get('order')
    if type(identity[2]) is not int or not isinstance(identity[1], str):
        raise Refused('TSR_SUPPORT_PLAN_IDENTITY')
    matches = [
        m for order, m in enumerate(fdplan['members'])
        if (m.get('log_index'), m.get('role'), m.get('order', order)) == identity
    ]
    if len(matches) != 1 or not _is_hex64(matches[0].get('key')):
        raise Refused('TSR_SUPPORT_POINT_KEY')
    return {
        'schema': TSR_SUPPORT_SCHEMA,
        'mode': 'SAVED_TARGET_FREE',
        'target_free': True,
        'before_target_access': True,
        'slots_pin': slots_pin,
        'ntest_compare_pin': compare_pin,
        'rings': [{
            'native_ring': rings[0],
            'lower_kpc': 9.901810628740723,
            'upper_kpc': 10.911721936765339,
            'lower_inclusive': False,
            'upper_inclusive': False,
        }],
        'point_key': matches[0]['key'],
        'rule_id': 'M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001',
    }


@command_snapshot
def tsr_support(doc):
    _keys(doc, TSR_SUPPORT_INPUT_KEYS, 'tsr-support input')
    if doc['schema'] != TSR_SUPPORT_INPUT_SCHEMA:
        raise Refused('INPUT_SCHEMA', TSR_SUPPORT_INPUT_SCHEMA)
    ctx = _plan_context(doc['build_record'], doc['replay_plan'], 'tsr-support')
    results = ctx['ledger']['results']
    if ctx['superseded'] or not results:
        raise Refused('TSR_SUPPORT_STEP7_NOT_CLEARED')
    head = results[-1]
    if head.get('status') != 'NO_NEW_DISCREPANCY' or head.get('replay_plan_sha256') != ctx['plan_sha']:
        raise Refused('TSR_SUPPORT_STEP7_NOT_CLEARED')
    passed, pass_pin, _ = read_json_pin(doc['pass_record'], 'tsr-support ledger-head pass')
    if pass_pin['sha256'] != head.get('pass_k_sha256') or passed.get('pass_label') != 'PASS_K':
        raise Refused('TSR_SUPPORT_NOT_HEAD_PASS')
    fdplan, fd_pin, _ = read_json_pin(doc['fdplan'], 'tsr-support fdplan')
    registered_fd = ctx['plan'].get('registry_verification', {}).get('fdplan')
    if registered_fd is not None and fd_pin != registered_fd:
        raise Refused('TSR_SUPPORT_FDPLAN_NOT_REGISTERED')
    policy, _, _ = read_json_pin(doc['extractor_policy'], 'tsr-support adopted policy')
    compare, _, _ = read_json_pin(doc['compare'], 'tsr-support compare')
    return _tsr_support_projection(policy, compare, doc['compare'], fdplan, ctx['plan'], passed)


_check_tsr_flag = tsr_check


@command_snapshot
def tsr_check(flag_pin, freeze_manifest_pin=None, expected=None, *, support=None):
    if not isinstance(support, dict):
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'TSR_SUPPORT_REQUIRED')
    _keys(support, ('record', 'projection_input'), 'tsr support check')
    doc, record_pin, _ = read_json_pin(support['record'], 'tsr support record')
    projected = tsr_support(support['projection_input'])
    if not isinstance(doc, dict) or set(doc) != set(TSR_SUPPORT_KEYS) or \
            canonical_bytes(doc) != canonical_bytes(projected):
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'TSR_SUPPORT_NOT_EXACT_PROJECTION')
    flag, _, _ = read_json_pin(flag_pin, 'tsr flag')
    if canonical_bytes(flag.get('ntest_compare_pin')) != canonical_bytes(doc['ntest_compare_pin']):
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'TSR_SUPPORT_COMPARE_NOT_FLAG_COMPARE')
    if freeze_manifest_pin is not None:
        have, _ = _manifest_input_files(freeze_manifest_pin, 'TSR_FLAG_TABLE_MISMATCH')
        if (record_pin['path'], record_pin['sha256']) not in have:
            raise Stop('TSR_FLAG_TABLE_MISMATCH', 'FREEZE_INPUT_FILES_LACK_TSR_SUPPORT')
    result = _check_tsr_flag(flag_pin, freeze_manifest_pin, expected)
    result['support_record'] = record_pin
    result['support_rule'] = 'G7: exact machine projection of the adopted policy, compare, and ledger-head D1'
    return result


A_INPUTS_PRODUCED = dict(A_INPUTS_PRODUCED,
    tsr_support_record='tsr-support: G7 machine projection after a cleared ledger head')
A_INPUTS_NOT_PRODUCED = {k: v for k, v in A_INPUTS_NOT_PRODUCED.items()
                         if k != 'tsr_support_record'}


# Component: cli_draft001.py
"""c2v007 command extensions. Every output is exclusive-create."""

_parent_main = main
_PARENT_COMMANDS = COMMANDS
COMMANDS = _PARENT_COMMANDS + ('custody', 'verify-registry', 'tsr-support')


def main(argv):
    try:
        cmd, args = _parse_args(argv)
        if cmd not in ('custody', 'verify-registry', 'tsr-support', 'tsr-check'):
            return _parent_main(argv)
        directory_output = cmd == 'custody'
        needed = ('--input', '--input-sha256', '--out-dir' if directory_output else '--out')
        if set(args) != set(needed):
            raise Refused('USAGE', '%s takes exactly %s' % (cmd, list(needed)))
        if cmd == 'custody':
            doc, _ = _cmd_input(args, 'CUSTODY_INPUT_C2V007')
            _keys(doc, ('schema', 'build_record', 'replay_plan'), 'custody input')
            if os.path.lexists(args['--out-dir']):
                raise Refused('OUT_DIR_EXISTS', args['--out-dir'])
            result, raw, successor = custody_run(doc['build_record'], doc['replay_plan'])
            _new_dir(args['--out-dir'])
            write_exclusive(os.path.join(args['--out-dir'], 'CUSTODY_RESULT.json'), raw)
            write_exclusive(os.path.join(args['--out-dir'], 'REPLAY_PLAN.json'), successor)
            print(json.dumps({'status': result['status'], 'ledger_seq': result['seq']}))
            return 0
        if cmd == 'verify-registry':
            doc, _ = _cmd_input(args, INPUT_SCHEMA)
            result = verify_launch_registry(doc)
        elif cmd == 'tsr-support':
            doc, _ = _cmd_input(args, TSR_SUPPORT_INPUT_SCHEMA)
            result = tsr_support(doc)
        else:
            doc, _ = _cmd_input(args, 'TSR_CHECK_INPUT_C2V007')
            _keys(doc, ('schema', 'flag_record', 'freeze_manifest', 'support'), 'tsr-check input')
            result = tsr_check(doc['flag_record'], doc['freeze_manifest'], support=doc['support'])
        write_exclusive(args['--out'], dump_bytes(result))
        print(json.dumps({'verdict': result.get('verdict', 'WRITTEN')}))
        return 0
    except Stop as exc:
        print(json.dumps({'stop': exc.code, 'detail': exc.detail}), file=sys.stderr)
        return 3
    except Refused as exc:
        print(json.dumps({'refused': exc.code, 'detail': exc.detail}), file=sys.stderr)
        return 2


def raw_status(rec, *, name, attempt, outdir, receipt, launch_pin, child_pid,
               mislaunch=None, stop=None):
    if mislaunch is not None:
        bound = (mislaunch.get("name") == name and mislaunch.get("attempt") == attempt and
                 mislaunch.get("outdir") == outdir and mislaunch.get("receipt") == receipt)
        lj = mislaunch.get("launch_json") or {}
        if lj.get("sha256") is not None:
            bound = bound and lj["sha256"] == launch_pin["sha256"]
        if lj.get("child_pid") is not None:
            bound = bound and lj["child_pid"] == child_pid
        _receipt_need(bound, "MISLAUNCH_NOT_BOUND")
        return "MISLAUNCH", "INFRA"
    if name == TWIN and stop is not None:
        _receipt_need(type(stop) is dict and stop.get('schema') == 'UNT_S0_TWIN_KILL_RECORD_C2V003A' and
             stop.get('reason') == 'ITERATION_0001_COMPLETED_AND_SIDECAR' and
             stop.get('outdir') == outdir and stop.get('launch_json') == launch_pin and
             type(stop.get('pgid')) is int and stop['pgid'] == child_pid and
             stop.get('result') in ('KILLED_TERM', 'KILLED_KILL') and
             isinstance(stop.get('date_u'), str) and bool(stop['date_u']), 'TWIN_STOP_NOT_BOUND')
        return 'TWIN_PLANNED_STOP', 'PLANNED_STOP'
    # A248: STOPPED_* by itself is never evidence of the designed twin stop.
    driver = rec.get("driver_status")
    _receipt_need(driver is None or isinstance(driver, str), "DRIVER_STATUS_FORM")
    raw = str(rec.get("status")) + "|" + (driver if driver is not None else "NONE")
    if raw == "CHILD_FAILED|NONE":
        _receipt_need(type(rec.get("exit_code")) is int, "EXIT_CODE_FORM")
        raw += "|SIGNAL" if rec["exit_code"] < 0 else "|EXIT"
    _receipt_need(raw in STATUS_CLASSES, "RECEIPT_STATUS_UNMAPPED", raw)
    return raw, STATUS_CLASSES[raw]

"""A248/A249 value-free cause inputs. No finish/result selector or run-content read."""
INTERRUPTION_POLICY_SCHEMA = 'INTERRUPTION_POLICY_C2V002'
CEILING_SCHEMA = 'SCHEDULE_CEILING_CLOSURE_C2V002'
ROOT_STOP_SCHEMA = 'ROOT_NONPHYSICS_STOP_C2V001'
CAUSE_KEYS = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site',
              'bound_shas', 'model_outcome', 'model_outcome_reason')
CAUSE_SHA_KEYS = ('receipt', 'result', 'finish', 'spec', 'driver')
MODEL_FAILURE_CODES = frozenset({'ROUTE_A_NO_FIXED_POINT', 'ITERATION_BUDGET_EXHAUSTED'})
KNOWN_NONPHYSICS_CAUSES = frozenset({'NONPHYSICS_OR_NOT_FAILED', 'SIGNAL_OR_EXIT_UNAUTHENTICATED',
                                  'A248_EXCLUDED_SOURCE_PREPARATION', 'SIGNAL_KILLED_STAGE'})
DISPOSITION_OF.pop('INFRA_REPEAT', None)
DISPOSITION_OF['SCHEDULE_CEILING'] = 'UNEVALUATED_SCHEDULE_CEILING'
INCOMPLETE_DISPOSITIONS = frozenset({'UNEVALUATED_STEP7_DISCREPANCY',
    'UNEVALUATED_CUSTODY_BREACH', 'UNEVALUATED_SCHEDULE_CEILING'})


def _policy_pin(pin, where):
    _keys(pin, ('path', 'sha256'), where)
    if not isinstance(pin['path'], str) or not os.path.isabs(pin['path']) or not _is_hex64(pin['sha256']):
        raise Refused('PIN_SHAPE', where)
    return {'path': os.path.realpath(pin['path']), 'sha256': pin['sha256']}


def _policy_key(pin):
    return canonical_bytes(_policy_pin(pin, 'policy receipt'))


def interruption_policy(pin, phase):
    doc, norm, _ = read_json_pin(pin, 'interruption_policy')
    _keys(doc, ('schema', 'phase', 'cause_producer', 'deadline_utc',
                'deadline_registration', 'attempts', 'closures'), 'interruption_policy')
    if doc['schema'] != INTERRUPTION_POLICY_SCHEMA or doc['phase'] != phase:
        raise Refused('INTERRUPTION_POLICY_SCHEMA')
    deadline = parse_utc_ns(doc['deadline_utc'], 'schedule ceiling')
    registered_ceiling = {'PHASE_1': '2026-11-06T05:59:00Z',
                          'PHASE_2': '2026-12-01T05:59:00Z'}.get(phase)
    if registered_ceiling is None or deadline != parse_utc_ns(registered_ceiling, 'adopted ceiling'):
        raise Refused('SCHEDULE_CEILING_NOT_ADOPTED')

    deadline_doc, deadline_pin, _ = read_json_pin(doc['deadline_registration'], 'schedule ceiling registration')
    _keys(deadline_doc, ('schema', 'phase', 'deadline_utc', 'date_u'), 'schedule ceiling registration')
    if deadline_doc['schema'] != 'SCHEDULE_CEILING_REGISTRATION_C2V001' or deadline_doc['phase'] != phase or \
            parse_utc_ns(deadline_doc['deadline_utc'], 'registered deadline') != deadline or \
            parse_utc_ns(deadline_doc['date_u'], 'deadline registration date') > deadline:
        raise Refused('SCHEDULE_CEILING_REGISTRATION')
    producer = None
    if doc['cause_producer'] is not None:
        _, producer = read_bytes_pin(doc['cause_producer'], 'reviewed value-free cause producer source')
    attempts = {}
    if not isinstance(doc['attempts'], list) or not isinstance(doc['closures'], list):
        raise Refused('INTERRUPTION_POLICY_SHAPE')
    for row in doc['attempts']:
        _keys(row, ('receipt', 'cause', 'root_stop'), 'interruption attempt')
        key = _policy_key(row['receipt'])
        if key in attempts:
            raise Refused('INTERRUPTION_ATTEMPT_DUPLICATE')
        for name in ('cause', 'root_stop'):
            if row[name] is not None:
                _policy_pin(row[name], name)
        if row['cause'] is not None and producer is None:
            raise Refused('CAUSE_PRODUCER_PIN_REQUIRED')
        attempts[key] = row
    # A253 closures bind the registered call; last_receipt may be null.
    closures = {}
    for pin in doc['closures']:
        closure, cpin, _ = read_json_pin(pin, 'schedule ceiling closure')
        _keys(closure, ('schema', 'phase', 'date_u', 'deadline_utc',
                       'deadline_registration', 'call', 'last_receipt'), 'schedule ceiling closure')
        if closure['schema'] != CEILING_SCHEMA or closure['phase'] != phase:
            raise Refused('SCHEDULE_CEILING_SCHEMA')
        if parse_utc_ns(closure['deadline_utc'], 'closure deadline') != deadline or \
                parse_utc_ns(closure['date_u'], 'closure date') < deadline:
            raise Refused('SCHEDULE_CEILING_TOO_EARLY')
        if _policy_pin(closure['deadline_registration'], 'closure registration') != deadline_pin:
            raise Refused('SCHEDULE_CEILING_REGISTRATION')
        _keys(closure['call'], ('alternative', 'kind', 'key', 'theta_sha256', 'spec_sha256'), 'closure call')
        if closure['last_receipt'] is not None:
            _policy_pin(closure['last_receipt'], 'last receipt')
        key = _call_key(closure['call'])
        if key in closures:
            raise Refused('SCHEDULE_CEILING_DUPLICATE')
        closures[key] = {'document': closure, 'pin': cpin}
    return {'phase': phase, 'pin': norm, 'cause_producer': producer, 'deadline_registration': deadline_pin,
            'deadline_utc': doc['deadline_utc'], 'deadline_ns': deadline,
            'attempts': attempts, 'closures': closures}


_a223_receipt = _receipt


def _receipt(pin, cfg, where):
    parsed = list(_a223_receipt(pin, cfg, where))
    norm, raw, cls, stamp, evidence = parsed[:5]
    facts = cfg['facts'][norm['path']]
    policy = cfg.get('interruption_policy')
    monitor_raw, _ = read_bytes_pin(facts['monitor_receipt'], where + '.monitor evidence')
    monitor = monitor_receipt(monitor_raw)
    evidence.update(model_outcome=None, cause_record=None, monitor_receipt_sha256=facts['monitor_receipt']['sha256'],
                    cause_producer=None if policy is None else policy['cause_producer'],
                    failure_evidence='UNAUTHENTICATED_MODEL_CAUSE', cause_authenticated=False)
    row = None if policy is None else policy['attempts'].get(_policy_key(norm))
    if row is not None and row['root_stop'] is not None:
        stop, stop_pin, _ = read_json_pin(row['root_stop'], where + '.root_stop')
        _keys(stop, ('schema', 'date_u', 'call', 'launch_json', 'registration'), 'root stop')
        if stop['schema'] != ROOT_STOP_SCHEMA or stop['call'] != facts['call'] or \
                _policy_pin(stop['launch_json'], 'root stop launch') != facts['launch_json']:
            raise Refused('ROOT_STOP_NOT_BOUND', where)
        launch, _, _ = read_json_pin(facts['launch_json'], where + '.root stop launch')
        if not parse_utc_ns(launch['utc'], 'launch utc') <= parse_utc_ns(stop['date_u'], 'root stop date') <= stamp:
            raise Refused('ROOT_STOP_OUTSIDE_ATTEMPT', where)
        _, registration = read_bytes_pin(stop['registration'], where + '.root stop registration')
        facts['root_stop'] = {'record': stop_pin, 'registration': registration}
        parsed[2] = 'INFRA'
        evidence.update(failure_evidence='ROOT_STOP_NONPHYSICS', cause_authenticated=True)
        return tuple(parsed)
    ex = monitor.get('exit_code')
    if cls == 'PLANNED_STOP':
        return tuple(parsed)
    if raw == 'CHILD_FAILED|NONE|EXIT' or type(ex) is not int or ex < 0 or ex in (137, 143) or \
            monitor.get('stop_reason') is not None:
        if cls in ('FAILED', 'FINISHED'):
            parsed[2] = 'INFRA'
        evidence.update(failure_evidence='MONITOR_NONPHYSICS', cause_authenticated=True)
        return tuple(parsed)
    if cls != 'FAILED' or row is None or row['cause'] is None:
        return tuple(parsed)
    cause, cause_pin, _ = read_json_pin(row['cause'], where + '.value_free_cause')
    _keys(cause, CAUSE_KEYS, 'value-free cause')
    _keys(cause['bound_shas'], CAUSE_SHA_KEYS, 'cause bindings')
    if type(cause['model_outcome']) is not bool or not isinstance(cause['model_outcome_reason'], str):
        raise Refused('CAUSE_FORM', where)
    for key in ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site'):
        if cause[key] is not None and not isinstance(cause[key], str):
            raise Refused('CAUSE_FORM', key)
    bound = cause['bound_shas']
    if any(v is not None and not _is_hex64(v) for v in bound.values()):
        raise Refused('CAUSE_SHA_FORM', where)
    driver = (monitor.get('pins') or {}).get('driver')
    launch, _, _ = read_json_pin(facts['launch_json'], where + '.cause launch')
    if not isinstance(driver, dict) or (launch.get('pins') or {}).get('driver') != driver:
        raise Refused('MODEL_DRIVER_BINDING', where)
    if bound['receipt'] != facts['monitor_receipt']['sha256'] or \
            bound['spec'] != evidence['spec_sha256'] or bound['driver'] != driver['sha256'] or \
            cause['status'] != monitor.get('driver_status'):
        raise Refused('CAUSE_MONITOR_BINDING', where)
    if bound['result'] is not None and (facts['result'] is None or bound['result'] != facts['result']['sha256']):
        raise Refused('CAUSE_RESULT_BINDING', where)
    facts['cause_record'] = cause_pin
    evidence['cause_record'] = cause_pin
    if not cause['model_outcome']:
        if cause['model_outcome_reason'] in KNOWN_NONPHYSICS_CAUSES:
            parsed[2] = 'INFRA'
            evidence.update(failure_evidence='AUTHENTICATED_NONPHYSICS', cause_authenticated=True)
        return tuple(parsed)
    if not all(_is_hex64(bound[k]) for k in CAUSE_SHA_KEYS):
        raise Refused('CAUSE_BOUND_SHA_MISSING', where)
    if cause['failure_code'] not in MODEL_FAILURE_CODES or cause['status'] != 'ROUTE_A_NO_FIXED_POINT' or \
            any(not isinstance(cause[k], str) or not cause[k] for k in ('failing_stage', 'exception_class', 'raise_site')):
        raise Refused('CAUSE_MODEL_IDENTITY', where)
    if monitor.get('status') != 'CHILD_FAILED' or ex <= 0:
        raise Refused('CAUSE_NONPHYSICS_END', where)
    evidence['model_outcome'] = (bound['spec'], bound['driver']) + tuple(
        cause[k] for k in ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site'))
    evidence.update(failure_evidence='AUTHENTICATED_MODEL_OUTCOME', cause_authenticated=True)
    return tuple(parsed)


def _infra_repeat_problem(prefix):
    return 'HELD_FOR_ROOT_FIX_NEVER_TERMINAL'


def _rule_c_problem(prefix):
    if len(prefix) < 2:
        return ('RULE_C_INCOMPLETE', 'two reproduced model outcomes are required')
    prev, cur = prefix[-2:]
    if prev['class'] != 'FAILED' or cur['class'] != 'FAILED':
        return ('RULE_C_NONPHYSICS', 'CAP and nonphysics never count')
    a, b = prev['evidence'], cur['evidence']
    if not a.get('model_outcome') or a.get('model_outcome') != b.get('model_outcome') or \
            prev['raw'] != cur['raw'] or a.get('cause_producer') != b.get('cause_producer') or \
            a.get('cause_producer') is None or not a.get('cause_record') or not b.get('cause_record'):
        return ('RULE_C_MODEL_NOT_REPRODUCED', 'same authenticated stage/status/code/class/site/spec/driver required')
    if a.get('monitor_receipt_sha256') == b.get('monitor_receipt_sha256'):
        return ('RULE_C_MODEL_NOT_REPRODUCED', 'distinct monitor receipts required')
    for e in (a, b):
        problem = _evidence_problem(e, False)
        if problem:
            return ('RULE_C_EVIDENCE_MISSING', problem)
        if e.get('solo_mode') is not True or e['other_ngc_processes_max'] != 0:
            return ('RULE_C_NOT_SOLO', 'both counted model failures must be solo')
    first = prefix[0]['evidence']
    if not _is_hex64(first.get('spec_sha256')) or not _positive_number(first.get('wall_cap_s')):
        return ('RULE_C_EVIDENCE_MISSING', 'attempt zero minimum')
    if len({x['evidence'].get('spec_sha256') for x in prefix
            if x['evidence'].get('spec_sha256') is not None}) != 1:
        return ('RULE_C_SPEC_NOT_IDENTICAL', 'identical science spec required')
    if b['rss_cap_bytes'] != b['host_ram_bytes'] * (11 if b.get('call_name') == TWIN or b.get('column_workers') == 8 else 1):
        return ('RULE_C_RERUN_CAPS', 'RSS equals RAM; identity twin and authorized full cw8 use eleven RAM')
    return None


def _ceiling_or_hold(seen, cfg, binding, where):
    policy = cfg.get('interruption_policy')
    last = seen[-1] if seen else None
    closure = None if policy is None else policy['closures'].get(_call_key(binding))
    if closure is None:
        if len(seen) >= 2 and seen[-2]['raw'] == last['raw']:
            if last['raw'] in ('CHILD_FAILED|REFUSED', 'CHILD_FAILED|BLOCKED'):
                raise Refused('HELD_FOR_FIX', where)
            if all(x['class'] == 'FAILED' and x['evidence'].get('solo_mode') is True and
                   type(x['evidence'].get('other_ngc_processes_max')) is int and
                   x['evidence']['other_ngc_processes_max'] == 0 for x in seen[-2:]) and \
                    any(not x['evidence'].get('cause_authenticated') for x in seen[-2:]):
                raise Refused('HELD_FOR_CAUSE', where)
        raise Refused('CALL_NOT_TERMINAL', where)
    if closure['document']['call'] != binding:
        raise Refused('SCHEDULE_CEILING_CALL_BINDING', where)
    if closure['document']['last_receipt'] != (last['receipt'] if last else None):
        raise Refused('SCHEDULE_CEILING_LAST_RECEIPT', where)
    if last is not None and parse_utc_ns(closure['document']['date_u'], 'closure date') < last['time_ns']:
        raise Refused('SCHEDULE_CEILING_BEFORE_ATTEMPT_END', where)
    return closure


def _terminal(attempts, cfg, where, allow_planned, binding):
    """The terminal attempt of one call under rule (c). binding: {'theta_sha256', 'spec_sha256'} of this call (the
    launch registry entry); every receipt of the call must carry exactly these (R2)."""
    if not isinstance(attempts, list):
        raise Refused('CALL_ATTEMPTS_REQUIRED', where)
    state = cfg.get('snapshot_call_states', {}).get(_call_key(binding))
    if state is not None and attempts != state['attempts']:
        raise Refused('SNAPSHOT_BUILD_ATTEMPTS', where)
    if not attempts:
        if state is None or cfg['interruption_policy']['phase'] != 'PHASE_1':
            raise Refused('CALL_ATTEMPTS_REQUIRED', where)
        closure = _ceiling_or_hold([], cfg, binding, where)
        return {'class': 'SCHEDULE_CEILING', 'raw_status': None,
                'time_ns': cfg['interruption_policy']['deadline_ns'], 'run_dir': None, 'receipt': None,
                'n_attempts': 0, 'receipt_paths': [], 'receipt_shas': [], 'receipt_idents': [],
                'run_dirs': [], 'rule_c': None, 'schedule_ceiling': closure, 'source_facts': []}
    seen, run_dirs, receipt_paths, receipt_shas = [], [], set(), set()
    for i, a in enumerate(attempts):
        w = '%s.attempts[%d]' % (where, i)
        _keys(a, ('run_dir', 'receipt'), w)
        if not isinstance(a['run_dir'], str) or not os.path.isabs(a['run_dir']) or not os.path.isdir(a['run_dir']):
            raise Refused('RUN_DIR_INVALID', w)
        run_real = os.path.realpath(a['run_dir'])
        if run_real in run_dirs:
            raise Refused('ATTEMPT_RUN_DIR_REPEATED', '%s: one run directory (by realpath) serves two attempts' % w)
        if any(_under(d, run_real) or _under(run_real, d) for d in run_dirs):
            raise Refused('ATTEMPT_RUN_DIR_NESTED', '%s: attempt run directories must be disjoint' % w)
        norm, raw_status, cls, t, evidence, rbind, ident = _receipt(a['receipt'], cfg, w + '.receipt')
        if norm['path'] in receipt_paths or norm['sha256'] in receipt_shas:
            raise Refused('ATTEMPT_RECEIPT_REPEATED', '%s: one receipt (by realpath or sha256) serves two attempts' % w)
        if norm['path'] != run_real + '.attempt_receipt.json':
            raise Refused('RECEIPT_NOT_AT_REGISTERED_SIDECAR', w)
        if cfg.get('interruption_policy', {}).get('phase') == 'PHASE_1' and t > cfg['interruption_policy']['deadline_ns']:
            raise Refused('PHASE1_RECEIPT_AFTER_CEILING', w)
        facts = cfg['facts'][norm['path']]
        if facts['run_dir'] != run_real:
            raise Refused('RECEIPT_RUN_DIR_NOT_OF_CALL', w)
        alias = (binding.get('kind') == 'SENSITIVITY' and
                 facts['call'].get('kind') in ('MEMBER', 'SENSITIVITY') and
                 facts['call'].get('alternative') == binding.get('alternative'))
        for role in ('alternative', 'kind', 'key'):
            if role in binding and facts['call'].get(role) != binding[role] and not (
                    alias and role in ('kind', 'key')):
                raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and facts['call']['name'] != seen[-1]['evidence']['call_name']:
            raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and t <= seen[-1]['time_ns']:
            raise Refused('ATTEMPT_ORDER', '%s: receipt times must strictly increase' % w)
        run_dirs.append(run_real)
        receipt_paths.add(norm['path'])
        receipt_shas.add(norm['sha256'])
        seen.append({'run_dir': run_real, 'receipt': norm, 'raw': raw_status, 'class': cls, 'time_ns': t,
                     'evidence': evidence, 'binding': rbind, 'ident': ident})
    # R1: the call is terminal at the first terminal prefix; each pair is judged on its own prefix only, so a later
    # attempt (of any spec) can never un-terminate an earlier pair and re-roll the call
    for i in range(len(seen) - 1):
        c = seen[i]['class']
        if c in ('FINISHED', 'PLANNED_STOP') or (c in FAILURE_CLASSES and _rule_c_problem(seen[:i + 1]) is None):
            raise Refused('ATTEMPT_AFTER_TERMINAL', '%s.attempts[%d]: the call was already terminal at attempt %d; '
                                                    'a later attempt would re-roll it' % (where, i + 1, i))
    # R1: one call, one spec ("rerun the identical spec"): its attempts carry at most one spec_sha256
    specs = {canonical_bytes(s['evidence']['spec_sha256']) for s in seen if s['evidence']['spec_sha256'] is not None}
    if len(specs) > 1:
        raise Refused('RULE_C_SPEC_NOT_IDENTICAL', '%s: the attempts carry more than one spec_sha256; rule (c) '
                                                   'reruns the identical spec' % where)
    # R2: every receipt is bound to this call (exact-theta key, then the spec sha the launch registry records)
    for i, s in enumerate(seen):
        for role, code in (('theta_sha256', 'RECEIPT_THETA_NOT_OF_CALL'), ('spec_sha256', 'RECEIPT_SPEC_NOT_REGISTERED')):
            v = s['binding'].get(role)
            if v is None:
                raise Refused('RECEIPT_CALL_BINDING_MISSING', '%s.attempts[%d]: the receipt carries no %s (G27)'
                              % (where, i, role))
            if v != binding[role]:
                raise Refused(code, '%s.attempts[%d]: the receipt\'s %s is not this call\'s' % (where, i, role))
    last = seen[-1]
    if last['class'] == 'PLANNED_STOP' and not allow_planned:
        raise Refused('PLANNED_STOP_NOT_A_MEMBER_TERMINAL', where)
    rule_c, closure = None, None
    if last['class'] not in ('FINISHED', 'PLANNED_STOP'):
        problem = _rule_c_problem(seen)
        if problem is None:
            n = len(seen)
            rule_c = {
                'counted_attempts': [n - 2, n - 1], 'raw_status': last['raw'],
                'spec_sha256': last['evidence']['spec_sha256'],
                'model_outcome': list(last['evidence']['model_outcome']),
                'cause_producer': last['evidence']['cause_producer'],
                'cause_records': [seen[-2]['evidence']['cause_record'], last['evidence']['cause_record']],
                'first_wall_cap_s': seen[0]['evidence']['wall_cap_s'],
                'rerun_wall_cap_s': last['evidence']['wall_cap_s'],
                'rerun_rss_cap_bytes': last['evidence']['rss_cap_bytes'],
                'host_ram_bytes': last['evidence']['host_ram_bytes'],
                'other_ngc_processes_max': [
                    seen[-2]['evidence']['other_ngc_processes_max'],
                    last['evidence']['other_ngc_processes_max']],
            }
        else:
            closure = _ceiling_or_hold(seen, cfg, binding, where)
    terminal_class = 'SCHEDULE_CEILING' if closure is not None else last['class']
    terminal_time = (cfg['interruption_policy']['deadline_ns']
                     if closure is not None else last['time_ns'])
    return {'class': terminal_class, 'raw_status': last['raw'], 'time_ns': terminal_time,
            'run_dir': last['run_dir'], 'receipt': last['receipt'], 'n_attempts': len(seen),
            'receipt_paths': [s['receipt']['path'] for s in seen],
            'receipt_shas': [s['receipt']['sha256'] for s in seen],
            'receipt_idents': [s['ident'] for s in seen], 'run_dirs': [s['run_dir'] for s in seen],
            'rule_c': rule_c, 'schedule_ceiling': closure, 'source_facts': [cfg['facts'][s['receipt']['path']] for s in seen]}

def _assemble(doc, fm, out_real):
    phase, stage = doc['phase'], doc['stage']
    slots, slots_pin, _ = read_json_pin(doc['slots'], 'slots')
    try:
        alts = slots['alternatives']
        declared, primary = alts['declared'], alts['primary']
        rows = slots['query_block']['rows']
    except (KeyError, TypeError):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared/primary and query_block.rows are required')
    if not isinstance(declared, list) or not declared or not all(isinstance(a, dict) for a in declared):
        raise Refused('SLOTS_SHAPE', 'alternatives.declared')
    names = [a.get('name') for a in declared]
    if not all(isinstance(n, str) and ALT_NAME_RE.match(n) for n in names) or len(set(names)) != len(names):
        raise Refused('SLOTS_ALTERNATIVE_NAMES', 'names must be unique file-safe strings')
    if any(a.get('status') not in (ALT_EVALUATED, ALT_NOT_EVALUATED) for a in declared):
        raise Refused('SLOTS_ALTERNATIVE_STATUS', 'every status is EVALUATED_ or NOT_EVALUATED_BEFORE_FREEZE')
    by_name = {a['name']: a for a in declared}
    if primary not in by_name or by_name[primary]['status'] != ALT_EVALUATED:
        raise Refused('SLOTS_PRIMARY', 'the primary must be declared EVALUATED_BEFORE_FREEZE')
    _qraw, qm_pin = read_bytes_pin(doc['query_manifest'], 'query_manifest')
    qm = fm.load_query_manifest(path=qm_pin['path'], expected_sha256=qm_pin['sha256'])
    if not isinstance(qm, dict) or not qm.get('ok'):
        raise Refused('QUERY_MANIFEST_REFUSED', 'load_query_manifest did not accept the pinned manifest')
    ids = list(qm['query_ids'])
    if len(ids) != 43 or not isinstance(rows, list) or len(rows) != 43:
        raise Refused('QUERY_COUNT', '43 query ids and 43 slots query rows are required')
    scope = 'PROGRAM' if qm_pin['sha256'] == fm.PROGRAM_QUERY_MANIFEST_SHA256 else 'SYNTHETIC_FIXTURE'
    mapping = [{'query_id': q, 'slots_query_id': s.get('query_id') if isinstance(s, dict) else None}
               for q, s in zip(ids, rows)]
    if scope == 'PROGRAM' and any(m['query_id'] != m['slots_query_id'] for m in mapping):
        raise Refused('PROGRAM_QUERY_ID_MISMATCH', 'program scope requires equal query ids')
    evaluated = [n for n in names if by_name[n]['status'] == ALT_EVALUATED]
    if phase == 'PHASE_1' and STAGE0_NAME in evaluated:
        raise Refused('PHASE1_STAGE0_NOT_IN_PHASE_1', 'Phase 1 runs under slots in which STAGE0 is not evaluated')
    spec, spec_pin, _ = read_json_pin(doc['spec_of_record'], 'spec_of_record')
    geometry = registered_geometry(spec, fm)
    geometry_answers = {}
    run_alts = [primary] if phase == 'PHASE_1' else list(evaluated)
    roster_files = {n: 'ROSTER_%s.json' % n for n in names}
    files = {}
    checks = []

    def roster_pins_of(roster_bytes):
        return {n: {'path': os.path.join(out_real, roster_files[n]), 'sha256': sha256_hex(roster_bytes[n])}
                for n in names}

    if stage == 'PLAN':
        roster_bytes = {n: dump_bytes(_roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, [], []))
                        for n in names}
        for n in names:
            files[roster_files[n]] = roster_bytes[n]
            checks.append((n, roster_files[n], []))
        files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': 'PLAN', 'phase': phase,
                                                'row_registration_rosters': roster_pins_of(roster_bytes)})
        return files, checks, ids

    # ---------------- MEMBERS / FULL ----------------
    cfg = _receipt_cfg(doc['receipt_keys'], doc['receipt_status_classes'])
    interruption = interruption_policy(doc['interruption_policy'], phase)
    cfg['interruption_policy'] = interruption
    registry, registry_pin = _launch_registry(doc['launch_registry'], phase)
    registry_proof = verify_launch_registry(doc)
    if registry_proof['mode'] == 'P112_SAVED_PHASE1_SNAPSHOT':
        cfg['snapshot_call_states'] = {_call_key(row['call']): row for row in registry_proof['call_states']}
    if phase == 'PHASE_1' and stage == 'FULL' and doc.get('m15') is not None:
        supplied_launches = doc['m15'].get('launch_receipts')
        expected_launches = registry_proof['m15_launch_receipts']
        if not isinstance(supplied_launches, list):
            raise Refused('M15_LAUNCH_RECEIPT_REQUIRED')
        actual_launches = [read_bytes_pin(p, 'm15 launch coverage')[1] for p in supplied_launches]
        if sorted(canonical_bytes(p) for p in actual_launches) != sorted(
                canonical_bytes(p) for p in expected_launches):
            raise Refused('M15_LAUNCH_SET_NOT_COMPLETE')
    used_entries = set()

    # gates: pinned in the phase's cutoff V006 bytes, never chosen here
    gc = doc['gate_cutoff']
    _keys(gc, ('kind', 'v006_copy'), 'gate_cutoff',
          optional=('record',) if phase == 'PHASE_1' and stage == 'FULL' else ())
    if gc['kind'] != CUTOFF_KIND[phase]:
        raise Refused('GATE_CUTOFF_KIND', 'phase %s requires cutoff %s' % (phase, CUTOFF_KIND[phase]))
    cut_raw, cutoff_pin = read_bytes_pin(gc['v006_copy'], 'gate_cutoff.v006_copy')
    cutoff_heads = v006_index(cut_raw)
    head_names = _original_headings(cut_raw)
    if not isinstance(doc['gate_documents'], list):
        raise Refused('GATE_LIST_REQUIRED', 'gate_documents must be a list (possibly empty)')
    gate_pins, pairs, gate_seen = [], set(), set()
    for i, gp in enumerate(doc['gate_documents']):
        w = 'gate_documents[%d]' % i
        gd, gnorm, _ = read_json_pin(gp, w)
        if gnorm['sha256'] in gate_seen:
            raise Refused('GATE_DUPLICATE', w)
        gate_seen.add(gnorm['sha256'])
        _gate_doc_ok(gd, ids, w, fm)
        if gnorm['sha256'] not in cutoff_heads:
            raise Refused('GATE_NOT_PINNED_IN_CUTOFF_V006',
                          '%s: its full sha256 is not in the phase cutoff V006 bytes; it is not a builder input' % w)
        for q in gd['query_ids']:
            for r in gd['registered_reasons']:
                if (q, r) in pairs:
                    raise Refused('GATE_AMBIGUOUS', '%s: (%s, %s) is listed twice' % (w, q, r))
                pairs.add((q, r))
        gate_pins.append(gnorm)
    gate_pins.sort(key=lambda p: (p['sha256'], p['path']))

    # exact thetas from the value-free plan outputs
    po = doc['plan_outputs']
    if not isinstance(po, dict) or set(po) != set(evaluated):
        raise Refused('PLAN_OUTPUTS_SET', 'one budget-0 evaluate_envelopes output per EVALUATED alternative')
    plan_members, plan_out_pins = {}, {}
    for n in evaluated:
        pdoc, pnorm, _ = read_json_pin(po[n], 'plan_outputs.' + n)
        plan_members[n] = _value_free_members(pdoc, ids, 'plan_outputs.' + n)
        plan_out_pins[n] = pnorm
    ref_list = [(m[0], m[1], m[2]) for m in plan_members[primary]]
    for n in evaluated:
        if [(m[0], m[1], m[2]) for m in plan_members[n]] != ref_list:
            raise Refused('PLAN_MEMBER_LISTS_DIFFER', n + ': every evaluated alternative has the PRIMARY members (D2)')
    sens_entries = []
    sens_pin = None
    if stage == 'FULL':
        spo = doc['sensitivity_plan_output']
        if phase == 'PHASE_1':
            if spo is not None:
                raise Refused('PHASE1_SENSITIVITY_NOT_RUN', 'Phase 1 runs sensitivity at budget 0 (A133 1.4)')
        else:
            if spo is None:
                raise Refused('SENSITIVITY_PLAN_REQUIRED', 'Phase-2 FULL needs the budget-0 sensitivity plan')
            sdoc, sens_pin, _ = read_json_pin(spo, 'sensitivity_plan_output')
            sens_entries = _value_free_sensitivity(sdoc, ids, 'sensitivity_plan_output')
            geometry_answers = geometry_exemptions(sens_entries, geometry)
    if stage == 'MEMBERS' and phase == 'PHASE_1':
        raise Refused('PHASE1_STAGE', 'Phase 1 builds FULL directly (no sensitivity calls exist in Phase 1)')

    # calls: rule (c) terminal receipts, rule (f) caps, run-produced cut records
    if not isinstance(doc['calls'], list):
        raise Refused('CALLS_REQUIRED', 'calls must be a list')
    member_theta = {(n, m[0]): m[3] for n in evaluated for m in plan_members[n]}
    if any(geometry_differs(theta, geometry) for theta in member_theta.values()):
        raise Refused('NONREGISTERED_GEOMETRY_ON_OTHER_KIND', 'planned member')
    sens_theta = {e[0]: e[1] for e in sens_entries
                  if not e[2] and theta_sha256(e[1]) not in geometry_answers}
    resolved = {}
    for i, c in enumerate(doc['calls']):
        w = 'calls[%d]' % i
        if not isinstance(c, dict):
            raise Refused('CALL_SHAPE', w)
        if 'cut_record' not in c:
            raise Refused('CUT_CONTEXT_MISSING',
                          '%s: every evaluated call carries its own cut record pin or an explicit null' % w)
        _keys(c, ('alternative', 'kind', 'key', 'attempts', 'result', 'cut_record'), w)
        alt, kind, key = c['alternative'], c['kind'], c['key']
        if alt not in run_alts:
            raise Refused('CALL_NOT_REGISTERED_FOR_PHASE', '%s: %r is not run in %s' % (w, alt, phase))
        if kind == 'MEMBER':
            if (alt, key) not in member_theta:
                raise Refused('CALL_NOT_A_PLANNED_MEMBER', w)
            theta = member_theta[(alt, key)]
        elif kind == 'SENSITIVITY':
            if phase != 'PHASE_2' or stage != 'FULL' or alt != primary or key not in sens_theta:
                raise Refused('CALL_NOT_A_PLANNED_SENSITIVITY_ENTRY', w)
            theta = sens_theta[key]
        else:
            raise Refused('CALL_KIND', w)
        if (alt, kind, key) in resolved:
            raise Refused('CALL_DUPLICATE', w)
        entry = registry.get((alt, kind, key))
        if entry is None:
            raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no entry for %s %s %s'
                          % (w, alt, kind, key))
        if entry['theta_sha256'] != theta_sha256(theta):
            raise Refused('LAUNCH_REGISTRY_THETA_MISMATCH', '%s: the registry\'s theta key is not the call\'s exact '
                                                            'theta (PLAN output)' % w)
        used_entries.add((alt, kind, key))
        term = _terminal(c['attempts'], cfg, w, allow_planned=False,
                         binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256'],
                                  'alternative': alt, 'kind': kind, 'key': key})
        if term['class'] == 'SCHEDULE_CEILING' and (c['result'] is not None or c['cut_record'] is not None):
            raise Refused('SCHEDULE_CEILING_HAS_RESULT_OR_CUT', w)
        result, result_ident = None, None
        if c['result'] is not None:
            # hashed, never parsed (no value is read); its file identity is kept for the cross-call check (c2v004/5)
            _rraw, result, result_ident = read_bytes_pin_ident(c['result'], w + '.result')
            if not _under(term['run_dir'], result['path']):
                raise Refused('RESULT_NOT_OF_ITS_CALL', '%s: the result lies outside the terminal run dir' % w)
        monitor_result = None if term['class'] == 'SCHEDULE_CEILING' else term['source_facts'][-1]['result']
        if result != monitor_result:
            raise Refused('RESULT_NOT_MONITOR_PIN', w)
        if term['class'] == 'FINISHED' and result is None:
            raise Refused('FINISHED_WITHOUT_RESULT', w)
        cut, cut_ident = None, None
        if c['cut_record'] is not None:
            cd, cut, _, cut_ident = read_json_pin_ident(c['cut_record'], w + '.cut_record')
            if not _under(term['run_dir'], cut['path']):
                raise Refused('CUT_RECORD_NOT_OF_ITS_CALL', '%s: the cut record lies outside its call\'s terminal run '
                                                            'dir (G29: bound to its call by residence)' % w)
            _cut_doc_ok(cd, w + '.cut_record', fm)
        disposition = DISPOSITION_OF[term['class']]
        rec = {'alternative': alt, 'kind': kind, 'key': key, 'theta': theta, 'theta_sha256': theta_sha256(theta),
               'terminal': term, 'result': result, 'cut': cut, 'disposition': disposition,
               'result_ident': result_ident, 'cut_ident': cut_ident,
               'signature': canonical_bytes([c['attempts'], c['result'], c['cut_record']])}
        if fm._canonical_bytes(theta) != canonical_bytes(theta):
            raise Refused('CANONICAL_FORM_DIVERGES', w)
        resolved[(alt, kind, key)] = rec
    # the phase's non-roster NGC calls (F points, the identity twin): FULL only; bound to the registry like any call
    others = []
    if stage == 'FULL':
        oc_list = doc['other_phase_calls']
        if not isinstance(oc_list, list):
            raise Refused('OTHER_PHASE_CALLS', 'a list (possibly empty) of non-roster NGC calls of the phase')
        labels = set()
        for i, oc in enumerate(oc_list):
            w = 'other_phase_calls[%d]' % i
            _keys(oc, ('label', 'attempts'), w)
            if not isinstance(oc['label'], str) or not oc['label'] or oc['label'] in labels:
                raise Refused('OTHER_CALL_LABEL', w)
            labels.add(oc['label'])
            entry = registry.get((None, 'OTHER', oc['label']))
            if entry is None:
                raise Refused('LAUNCH_REGISTRY_ENTRY_MISSING', '%s: the launch registry has no OTHER entry %r'
                              % (w, oc['label']))
            used_entries.add((None, 'OTHER', oc['label']))
            term = _terminal(oc['attempts'], cfg, w, allow_planned=True,
                             binding={'theta_sha256': entry['theta_sha256'], 'spec_sha256': entry['spec_sha256'],
                                      'alternative': None, 'kind': 'OTHER', 'key': oc['label']})
            others.append({'label': oc['label'], 'terminal': term})
    source_entries = {canonical_bytes(p) for p in registry_proof['sources']}
    for terminal in [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]:
        for facts in terminal['source_facts']:
            if canonical_bytes(facts['registry_entry']) not in source_entries:
                raise Refused('RECEIPT_REGISTRY_SOURCE_NOT_ASSEMBLED')
    unused = sorted('%s:%s:%s' % k for k in registry if k not in used_entries)
    if unused:
        raise Refused('LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL', 'registry entries with no call record in this build '
                                                            'input: %s' % unused[:5])
    # one call per (alternative, exact theta); identical call records only (A133: an equal theta is the same call)
    by_theta = {}
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in by_theta and by_theta[k]['signature'] != rec['signature']:
            raise Refused('CONTEXT_CONFLICT', '%s: two different call records at one exact theta' % rec['alternative'])
        by_theta.setdefault(k, rec)
    # R2: one receipt serves one call, across every roster and non-roster call of this build input
    _cross_call_receipts([(('CALL', k[0], k[1]), rec['terminal']) for k, rec in sorted(by_theta.items())] +
                         [(('OTHER', o['label']), o['terminal']) for o in others])
    # c2v005: one run file (by realpath or file identity) serves one call, across every roster AND OTHER call of this
    # build input; one FINISHED-result content (by sha256) serves one call (C38)
    _cross_call_files([(('CALL', k[0], k[1]), _roster_call_files(rec)) for k, rec in sorted(by_theta.items())] +
                      [(('OTHER', o['label']), _other_call_files(o['terminal'])) for o in others])
    # c2v005 (G29): a cut record lies in no run directory of another call (its own terminal run directory was checked
    # per call above)
    _cut_record_residence([(('CALL', k[0], k[1]), rec['terminal'], rec['cut']) for k, rec in sorted(by_theta.items())]
                          + [(('OTHER', o['label']), o['terminal'], None) for o in others])
    # completeness: every call the phase registers has a terminal receipt before step 4
    for n in run_alts:
        for m in plan_members[n]:
            if (n, 'MEMBER', m[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', '%s %s has no terminal call record' % (n, m[0]))
    if phase == 'PHASE_2' and stage == 'FULL':
        for e in sens_entries:
            if not e[2] and theta_sha256(e[1]) not in geometry_answers and (primary, 'SENSITIVITY', e[0]) not in resolved:
                raise Refused('CALL_RECORD_MISSING', 'sensitivity %s has no terminal call record' % e[0])

    # contexts (members in member order, then sensitivity entries in plan order; equal thetas once)
    contexts = {n: [] for n in names}
    ctx_theta = {n: [] for n in names}
    for n in run_alts:
        seen = set()
        order = [resolved[(n, 'MEMBER', m[0])] for m in plan_members[n]]
        if n == primary and stage == 'FULL' and phase == 'PHASE_2':
            order += [resolved[(n, 'SENSITIVITY', e[0])] for e in sens_entries
                      if not e[2] and theta_sha256(e[1]) not in geometry_answers]
        for rec in order:
            if rec['disposition'] not in EVALUATED_DISPOSITIONS or rec['theta_sha256'] in seen:
                continue
            seen.add(rec['theta_sha256'])
            contexts[n].append({'theta_ngc': rec['theta'], 'cut': rec['cut']})
            ctx_theta[n].append(rec['theta'])
    roster_docs = {n: _roster_doc(scope, by_name[n], slots_pin, qm_pin, mapping, list(gate_pins), contexts[n])
                   for n in names}
    roster_bytes = {n: dump_bytes(roster_docs[n]) for n in names}
    for n in names:
        files[roster_files[n]] = roster_bytes[n]
        checks.append((n, roster_files[n], ctx_theta[n]))
    rpins = roster_pins_of(roster_bytes)
    files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V003', 'stage': stage, 'phase': phase,
                                            'row_registration_rosters': rpins})

    # Phase-2 FULL: member contexts byte-identical to the MEMBERS stage (the step-7 D1 check holds by construction),
    # and the MEMBERS-stage build record binds the pass-one replay plan (step 7 checks pass one against it)
    pass_one_sha = {n: rpins[n]['sha256'] for n in names}
    pass_one_members_plan = None
    if stage == 'FULL':
        msr, mbr = doc['members_stage_rosters'], doc['members_stage_build_record']
        if phase == 'PHASE_1':
            if msr is not None or mbr is not None:
                raise Refused('PHASE1_STAGE', 'Phase 1 has no MEMBERS-stage rosters or build record')
        else:
            if not isinstance(msr, dict) or set(msr) != set(names):
                raise Refused('MEMBERS_STAGE_ROSTERS_REQUIRED', 'one MEMBERS-stage roster pin per alternative')
            mrec, mrnorm = _build_record_of(mbr, 'members_stage_build_record', 'MEMBERS', 'PHASE_2')
            for n in names:
                if not isinstance(msr[n], dict) or mrec['outputs'].get(roster_files[n]) != msr[n].get('sha256'):
                    raise Refused('MEMBERS_STAGE_ROSTERS_NOT_OF_RECORD', n)
            mplan, mpnorm, _ = read_json_pin(
                {'path': os.path.join(os.path.dirname(mrnorm['path']), 'REPLAY_PLAN.json'),
                 'sha256': mrec['outputs']['REPLAY_PLAN.json']}, 'members-stage REPLAY_PLAN.json')
            pass_one_members_plan = {
                'stage': 'MEMBERS', 'build_record_sha256': mrnorm['sha256'],
                'replay_plan_sha256': mpnorm['sha256'],
                'member_budget': {a['name']: a['member_budget'] for a in mplan['alternatives']
                                  if a['slots_status'] == ALT_EVALUATED},
                'sensitivity_budget': mplan['sensitivity']['budget']}
            for n in names:
                mdoc, mnorm, _ = read_json_pin(msr[n], 'members_stage_rosters.' + n)
                full = roster_docs[n]
                for k in ('schema', 'scope', 'alternative', 'slots', 'query_manifest', 'query_mapping', 'root_gates'):
                    if mdoc.get(k) != full[k]:
                        raise Refused('MEMBER_CONTEXTS_CHANGED', '%s: %s differs from the MEMBERS stage' % (n, k))
                mc = mdoc.get('outer_cut', {}).get('contexts', []) if isinstance(mdoc.get('outer_cut'), dict) else None
                fc = full['outer_cut'].get('contexts', [])
                if mc is None or len(mc) > len(fc) or \
                        any(canonical_bytes(a) != canonical_bytes(b) for a, b in zip(mc, fc)):
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member contexts must be byte-identical')
                n_member_ctx = sum(1 for _ in contexts_member_prefix(resolved, plan_members, n))
                if len(mc) != n_member_ctx:
                    raise Refused('MEMBER_CONTEXTS_CHANGED', n + ': member context count differs')
                pass_one_sha[n] = mnorm['sha256']

    # replay plan (rules (b), (c), (f))
    alt_plan, replay_index = [], {}
    for n in names:
        a = {'name': n, 'slots_status': by_name[n]['status'], 'run_in_phase': n in run_alts,
             'mode': roster_docs[n]['outer_cut']['mode'], 'member_budget': None, 'members': []}
        if n in evaluated:
            budget = None
            for idx, m in enumerate(plan_members[n]):
                if n in run_alts:
                    rec = resolved[(n, 'MEMBER', m[0])]
                    own, cls, nat = rec['disposition'], rec['terminal']['class'], rec['terminal']['n_attempts']
                    rule_c = rec['terminal']['rule_c']
                else:
                    own, cls, nat, rule_c = 'NOT_RUN_PHASE1_BUDGET0', None, 0, None
                if budget is None and own not in EVALUATED_DISPOSITIONS:
                    budget = idx
                a['members'].append({'member_id': m[0], 'log_index': m[1], 'role': m[2], 'order': idx, 'theta_sha256': theta_sha256(m[3]),
                                     'own_disposition': own, 'terminal_class': cls, 'n_attempts': nat,
                                     'rule_c': rule_c})
            a['member_budget'] = len(plan_members[n]) if budget is None else budget
            _effective(a)
        alt_plan.append(a)
        if n in run_alts:
            idx_entries, seen = [], {}
            for rec in resolved.values():
                if rec['alternative'] != n:
                    continue
                key = rec['theta_sha256']
                if key in seen:
                    seen[key]['call_keys'].append('%s:%s' % (rec['kind'], rec['key']))
                    seen[key]['call_keys'].sort()
                    continue
                e = {'theta_sha256': key, 'call_keys': ['%s:%s' % (rec['kind'], rec['key'])],
                     'disposition': rec['disposition'], 'result': rec['result']}
                seen[key] = e
                idx_entries.append(e)
            idx_entries.sort(key=lambda e: e['theta_sha256'])
            replay_index[n] = idx_entries
    if phase == 'PHASE_1' or stage == 'MEMBERS':
        sens = {'budget': 0, 'entries': [],
                'budget_rule': ('Phase 1: budget 0 (A133 1.4 and 1.6 step 5)' if phase == 'PHASE_1' else
                                'Phase-2 pass one: budget 0 (the plan exists only after D1; RUNBOOK step 2b)')}
    else:
        entries, budget, stopped = [], 0, False
        for e in sens_entries:
            if e[2]:
                entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': True,
                                'own_disposition': 'SKIPPED_ZERO_DISPLACEMENT', 'effective_disposition':
                                'SKIPPED_ZERO_DISPLACEMENT'})
                continue
            own = (GEOMETRY_DISPOSITION if theta_sha256(e[1]) in geometry_answers else
                   resolved[(primary, 'SENSITIVITY', e[0])]['disposition'])
            if not stopped and (own in EVALUATED_DISPOSITIONS or own == GEOMETRY_DISPOSITION):
                budget += 1
                eff = own
            elif not stopped:
                eff, stopped = own, True
            else:
                eff = 'UNEVALUATED_BY_ORDER_TRUNCATION' if own in EVALUATED_DISPOSITIONS else own
            entries.append({'entry_id': e[0], 'theta_sha256': theta_sha256(e[1]), 'skipped': False,
                            'own_disposition': own, 'effective_disposition': eff})
        sens = {'budget': budget, 'entries': entries, 'plan_output': sens_pin,
                'budget_rule': SENS_BUDGET_RULE}
    pass_one = None
    if stage == 'FULL':
        pass_one = pass_one_members_plan or {
            'stage': 'FULL', 'build_record_sha256': None, 'replay_plan_sha256': None,
            'member_budget': {a['name']: a['member_budget'] for a in alt_plan if a['slots_status'] == ALT_EVALUATED},
            'sensitivity_budget': sens['budget'],
            'note': 'Phase 1: pass one runs under this build\'s own (chain-root) replay plan; null shas mean that plan'}
    plan = {'schema': REPLAY_PLAN_SCHEMA, 'builder': BUILDER_NAME, 'phase': phase, 'stage': stage,
            'primary': primary, 'predecessor_sha256': None,
            'registered_roster_sha256': {n: rpins[n]['sha256'] for n in names},
            'pass_one_roster_sha256': pass_one_sha, 'pass_one': pass_one,
            'plan_outputs': plan_out_pins, 'launch_registry': registry_pin, 'alternatives': alt_plan,
            'sensitivity': sens, 'replay_index': replay_index, 'rules': RULE_TEXT, 'step4': None,
            'stage0_status': None,
            'registered_geometry': geometry, 'geometry_not_exposed': geometry_answers,
            'spec_of_record': spec_pin, 'registry_verification': registry_proof,
            'interruption_policy': {
                k: interruption[k] for k in ('pin', 'cause_producer',
                    'deadline_registration', 'deadline_utc')},

            'custody': check_custody_inputs(doc['custody'], resolved, others)}

    if stage == 'FULL':
        report = _gate_status_list(doc['m15'], gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names,
                                   cfg)
        files['GATE_STATUS_REPORT.json'] = dump_bytes(report)
        files['GATE_STATUS_LIST.json'] = dump_bytes(a_gate_status_list(report))
        plan['step4'] = _step4(phase, resolved, others)
        plan['stage0_status'] = _stage0_status(phase, by_name, resolved, plan['step4'])
    plan['allow_incomplete'] = allow_incomplete_value(plan)
    if interruption['cause_producer'] is not None:
        terminal_times = [r['terminal']['time_ns'] for r in resolved.values()] + [
            r['terminal']['time_ns'] for r in others]
        if not terminal_times:
            raise Refused('CAUSE_GATE_TERMINAL_TIME_REQUIRED')
        _snapshot_cause_gate(interruption, cut_raw, max(terminal_times))
    plan['gate_cutoff_evidence'] = check_cutoff(
        doc, resolved, others, cut_raw, cutoff_pin, gate_pins, files)
    files['REPLAY_PLAN.json'] = dump_bytes(plan)
    return files, checks, ids

def _terminal_receipt_pins(resolved, others):
    unique = {}
    for terminal in [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]:
        pin = terminal['receipt']
        if pin is not None:
            unique[(pin['path'], pin['sha256'])] = pin
    return [unique[k] for k in sorted(unique)]

def check_custody_inputs(custody, resolved, others):
    _keys(custody, ('root', 'run_volumes', 'copies'), 'custody')
    require_run_volumes(custody['run_volumes'])
    root = custody['root']
    all_terminals = [r['terminal'] for r in resolved.values()] + [o['terminal'] for o in others]
    run_dirs = [d for terminal in all_terminals for d in terminal['run_dirs']]
    if not isinstance(root, str) or not os.path.isabs(root) or os.path.realpath(root) != root or \
            not os.path.isdir(root) or any(root == d or _under(d, root) or _under(root, d) for d in run_dirs):
        raise Refused('CUSTODY_ROOT_IN_RUN_TREE')
    if any(not any(d == v or _under(v, d) for v in custody['run_volumes']) for d in run_dirs):
        raise Refused('CUSTODY_RUN_VOLUME_BINDING')
    required = {}
    for terminal in all_terminals:
        facts = terminal['source_facts'][-1] if terminal['source_facts'] else {}
        for key in ('receipt', 'monitor_receipt', 'result'):
            pin = facts.get(key)
            if pin is not None:
                required[(pin['path'], pin['sha256'])] = pin
    for rec in resolved.values():
        for key in ('result', 'cut'):
            pin = rec.get(key)
            if pin is not None:
                required[(pin['path'], pin['sha256'])] = pin
    copies = custody['copies']
    if not isinstance(copies, list):
        raise Refused('CUSTODY_COPIES_REQUIRED')
    seen, normalized = set(), []
    for item in copies:
        _keys(item, ('source', 'copy'), 'custody copy')
        raw, source, source_id = read_bytes_pin_ident(item['source'], 'custody source')
        copied, copy, copy_id = read_bytes_pin_ident(item['copy'], 'custody copy')
        key = (source['path'], source['sha256'])
        if key in seen or key not in required:
            raise Refused('CUSTODY_SOURCE_SET')
        if not _under(root, copy['path']) or any(
                copy['path'] == d or _under(d, copy['path']) for d in run_dirs):
            raise Refused('CUSTODY_COPY_IN_RUN_TREE')
        if raw != copied or source['sha256'] != copy['sha256']:
            raise Refused('CUSTODY_COPY_BYTES')
        # A custody copy must survive loss of the registered file itself.
        if source_id == copy_id:
            raise Refused('CUSTODY_COPY_IS_SOURCE')
        seen.add(key)
        normalized.append({'source': source, 'copy': copy})
    if seen != set(required):
        raise Refused('CUSTODY_SOURCE_SET')
    return {
        'root': root,
        'run_volumes': sorted(set(custody['run_volumes'])),
        'copies': sorted(normalized, key=lambda x: (x['source']['path'], x['source']['sha256'])),
    }

def _step4(phase, resolved, others):
    receipts = []
    seen = set()
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in seen:
            continue
        seen.add(k)
        receipts.append({'label': '%s:%s:%s' % (rec['alternative'], rec['kind'], rec['key']),
                         'class': rec['terminal']['class'], 'utc_ns': rec['terminal']['time_ns']})
    for o in others:
        receipts.append({'label': 'OTHER:' + o['label'], 'class': o['terminal']['class'],
                         'utc_ns': o['terminal']['time_ns']})
    if not receipts:
        raise Refused('STEP4_NO_RECEIPTS', 'no terminal receipt')
    receipts.sort(key=lambda r: (r['utc_ns'], r['label']))
    start = receipts[-1]['utc_ns']
    return {'rule': ('Phase 1 A253: latest terminal time when all calls finish before the ceiling, otherwise the ceiling'
                     if phase == 'PHASE_1' else
                     'Phase 2: step 4 begins when every registered Phase-2 step-5 call has a terminal or schedule-ceiling '
                     'closure; the start is the latest terminal time including the adopted ceiling, and a '
                     'receipt written at that instant counts as before (A133 3; r3a 6.3)'),
            'start_utc': format_utc_ns(start),
            'receipts': [{'label': r['label'], 'class': r['class'], 'utc': format_utc_ns(r['utc_ns'])}
                         for r in receipts]}

"""A253 snapshot primitives: fixed call identity and replayable saved custody."""
PHASE1_SNAPSHOT_SCHEMA = 'PHASE1_CEILING_SNAPSHOT_C2V007'
PHASE1_SNAPSHOT_INPUT_SCHEMA = 'PHASE1_SNAPSHOT_INPUT_C2V007'
PHASE1_CEILING_UTC = '2026-11-06T05:59:00Z'


def _call_binding(call):
    return {'alternative': call['alternative'], 'kind': call['kind'], 'key': call['key'],
            'theta_sha256': call['theta_sha256'], 'spec_sha256': call['spec']['sha256']}


def _call_key(binding):
    _keys(binding, ('alternative', 'kind', 'key', 'theta_sha256', 'spec_sha256'), 'snapshot call')
    if not _is_hex64(binding['theta_sha256']) or not _is_hex64(binding['spec_sha256']):
        raise Refused('SNAPSHOT_CALL_BINDING')
    return canonical_bytes(binding)


def _snapshot_prefix(seen, allow_planned):
    term = None
    for i, item in enumerate(seen):
        if item['class'] == 'PLANNED_STOP' and not allow_planned:
            raise Refused('PLANNED_STOP_NOT_A_MEMBER_TERMINAL')
        if term is not None:
            raise Refused('ATTEMPT_AFTER_TERMINAL')
        if item['class'] in ('FINISHED', 'PLANNED_STOP'):
            term = {'index': i, 'class': item['class'], 'time_ns': item['time_ns'],
                    'receipt': item['receipt']}
        elif item['class'] == 'FAILED' and _rule_c_problem(seen[:i+1]) is None:
            term = {'index': i, 'class': 'FAILED', 'time_ns': item['time_ns'],
                    'receipt': item['receipt']}
    return term


def _snapshot_t(states, created_ns, ceiling_ns):
    if not states:
        raise Refused('SNAPSHOT_CALLS_EMPTY')
    if all(row['terminal'] is not None for row in states):
        value = max(row['terminal']['time_ns'] for row in states)
        if value > ceiling_ns or value > created_ns:
            raise Refused('SNAPSHOT_TERMINAL_TIME')
        return 'ALL_TERMINAL', value
    if created_ns < ceiling_ns:
        raise Refused('SNAPSHOT_BEFORE_CEILING')
    return 'CEILING', ceiling_ns


def _snapshot_source_pin(path, raw):
    return {'path': os.path.abspath(path), 'sha256': sha256_hex(raw)}


def _snapshot_read_source(pin, module):
    norm = _policy_pin(pin, 'snapshot source')
    module.guard_read(norm['path'])
    with snapshot_scope() as snapshot:
        raw, real = snapshot.read(norm['path'], 'saved snapshot source', require_nonempty=False)
    if sha256_hex(raw) != norm['sha256']:
        raise Refused('SNAPSHOT_SOURCE_PIN', real)
    return raw


def _snapshot_cause_gate(policy, v006_raw, terminal_ns):
    producer = policy['cause_producer']
    if producer is None:
        return
    first = v006_index(v006_raw)
    if producer['sha256'] not in first:
        raise Refused('CAUSE_PRODUCER_NOT_ROOT_PINNED')
    late = {entry['heading'].lower() for entry in cutoff_entry_stamps(v006_raw)
            if entry['time_ns'] is not None and entry['time_ns'] > terminal_ns}
    if first[producer['sha256']] in late:
        raise Refused('CAUSE_PRODUCER_FIRST_PIN_AFTER_T')


def _validated_attempts(attempts, cfg, where, allow_planned, binding):
    """The terminal attempt of one call under rule (c). binding: {'theta_sha256', 'spec_sha256'} of this call (the
    launch registry entry); every receipt of the call must carry exactly these (R2)."""
    if not isinstance(attempts, list):
        raise Refused('CALL_ATTEMPTS_REQUIRED', where)
    seen, run_dirs, receipt_paths, receipt_shas = [], [], set(), set()
    for i, a in enumerate(attempts):
        w = '%s.attempts[%d]' % (where, i)
        _keys(a, ('run_dir', 'receipt'), w)
        if not isinstance(a['run_dir'], str) or not os.path.isabs(a['run_dir']) or not os.path.isdir(a['run_dir']):
            raise Refused('RUN_DIR_INVALID', w)
        run_real = os.path.realpath(a['run_dir'])
        if run_real in run_dirs:
            raise Refused('ATTEMPT_RUN_DIR_REPEATED', '%s: one run directory (by realpath) serves two attempts' % w)
        if any(_under(d, run_real) or _under(run_real, d) for d in run_dirs):
            raise Refused('ATTEMPT_RUN_DIR_NESTED', '%s: attempt run directories must be disjoint' % w)
        norm, raw_status, cls, t, evidence, rbind, ident = _receipt(a['receipt'], cfg, w + '.receipt')
        if norm['path'] in receipt_paths or norm['sha256'] in receipt_shas:
            raise Refused('ATTEMPT_RECEIPT_REPEATED', '%s: one receipt (by realpath or sha256) serves two attempts' % w)
        if norm['path'] != run_real + '.attempt_receipt.json':
            raise Refused('RECEIPT_NOT_AT_REGISTERED_SIDECAR', w)
        facts = cfg['facts'][norm['path']]
        if facts['run_dir'] != run_real:
            raise Refused('RECEIPT_RUN_DIR_NOT_OF_CALL', w)
        alias = (binding.get('kind') == 'SENSITIVITY' and
                 facts['call'].get('kind') in ('MEMBER', 'SENSITIVITY') and
                 facts['call'].get('alternative') == binding.get('alternative'))
        for role in ('alternative', 'kind', 'key'):
            if role in binding and facts['call'].get(role) != binding[role] and not (
                    alias and role in ('kind', 'key')):
                raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and facts['call']['name'] != seen[-1]['evidence']['call_name']:
            raise Refused('RECEIPT_CALL_NOT_REGISTERED', w)
        if seen and t <= seen[-1]['time_ns']:
            raise Refused('ATTEMPT_ORDER', '%s: receipt times must strictly increase' % w)
        run_dirs.append(run_real)
        receipt_paths.add(norm['path'])
        receipt_shas.add(norm['sha256'])
        seen.append({'run_dir': run_real, 'receipt': norm, 'raw': raw_status, 'class': cls, 'time_ns': t,
                     'evidence': evidence, 'binding': rbind, 'ident': ident})
    if len({item['evidence'].get('spec_sha256') for item in seen}) > 1:
        raise Refused('RULE_C_SPEC_NOT_IDENTICAL', where)
    for item in seen:
        for role, code in (('theta_sha256', 'RECEIPT_THETA_NOT_OF_CALL'), ('spec_sha256', 'RECEIPT_SPEC_NOT_REGISTERED')):
            if item['binding'].get(role) != binding[role]:
                raise Refused(code, where)
    return seen


@contextlib.contextmanager
def _snapshot_read_fence(pins):
    allowed = {}
    for pin in pins:
        norm = _policy_pin(pin, 'captured snapshot pin')
        if norm['path'] in allowed and allowed[norm['path']] != norm['sha256']:
            raise Refused('SNAPSHOT_SOURCE_CONFLICT')
        allowed[norm['path']] = norm['sha256']
    with snapshot_scope() as snapshot:
        original = snapshot.read
        def frozen_read(path, where, ident_out=None, require_nonempty=True):
            real = os.path.realpath(path)
            if real not in allowed:
                raise Refused('SNAPSHOT_SOURCE_NOT_CAPTURED', where)
            raw, real = original(path, where, ident_out, require_nonempty)
            if sha256_hex(raw) != allowed[real]:
                raise Refused('SNAPSHOT_SOURCE_PIN', where)
            return raw, real
        snapshot.read = frozen_read
        try:
            yield
        finally:
            snapshot.read = original


"""A253: exclusive root-gated capture, with no fabricated launch or attempt."""


def _snapshot_existing_entry(module, ctx, call):
    if call['origin'] == 'KIT':
        return module.registered_entry(ctx, call)[1]
    path = module.own_registry_path(ctx, call['name'])
    return module.registered_entry(ctx, call)[1] if os.path.isfile(path) else None


def _snapshot_attempts(rows):
    return [{'run_dir': row['run_dir'], 'receipt': row['receipt_pin']} for row in rows]


@command_snapshot
def phase1_snapshot(doc, out_dir):
    _keys(doc, ('schema', 'launcher', 'config', 'interruption_policy'), 'snapshot input')
    if doc['schema'] != PHASE1_SNAPSHOT_INPUT_SCHEMA:
        raise Refused('INPUT_SCHEMA')
    out_dir = os.path.abspath(out_dir)
    if os.path.lexists(out_dir):
        raise Refused('OUT_DIR_EXISTS', out_dir)
    if os.path.realpath(os.path.dirname(out_dir)) != os.path.dirname(out_dir):
        raise Refused('SNAPSHOT_OUTPUT_PARENT')
    module = _p112_verifier_module(doc['launcher'])
    try:
        saved_config, _, _ = read_json_pin(doc['config'], 'snapshot config')
        ctx = _registry_context_factory(module, doc['config'])
        if ctx.cfg != saved_config:
            raise Refused('SNAPSHOT_CONFIG_BINDING')
        ctx.gate()
        if ctx.config_pin != _policy_pin(doc['config'], 'snapshot config'):
            raise Refused('SNAPSHOT_CONFIG_BINDING')
        if ctx.cfg['phase1_ceiling_utc'] != PHASE1_CEILING_UTC:
            raise Refused('SNAPSHOT_CEILING')
        for origin in ('P112', 'KIT'):
            module.mount_first(ctx.cfg, origin, ctx.system)
        created_utc = ctx.system.utc()
        created_ns = parse_utc_ns(created_utc, 'snapshot creation')
        ceiling_ns = parse_utc_ns(PHASE1_CEILING_UTC, 'phase1 ceiling')
        date_u = module.date_u()
        policy = interruption_policy(doc['interruption_policy'], 'PHASE_1')
        base_doc, base_pin, _ = read_json_pin(doc['interruption_policy'], 'snapshot base policy')
        if policy['deadline_ns'] != ceiling_ns or base_doc['closures']:
            raise Refused('SNAPSHOT_BASE_POLICY')
        cfg = _receipt_cfg(EXACT_RECEIPT_KEYS, STATUS_CLASSES)
        cfg['interruption_policy'] = policy
        calls = ctx.calls()
        if not calls or len({_call_key(_call_binding(c)) for c in calls}) != len(calls):
            raise Refused('SNAPSHOT_CALL_SET')
        rows = ctx.system.processes()
        captured, states, sources, mappings = [], [], [], []
        for call in calls:
            binding = _call_binding(call)
            hist = module.history(ctx, call, rows=rows, inspect_next=True, allow_incomplete=True)
            for pending in hist['pending']:
                if pending['status'] == 'ATTEMPT_NEEDS_CLOSE':
                    monitor_raw, _ = read_bytes_pin(pending['monitor_receipt'], 'pending monitor')
                    if parse_utc_ns(monitor_receipt(monitor_raw)['utc_end'], 'pending end') <= ceiling_ns:
                        raise Refused('SNAPSHOT_NEEDS_PRECEILING_CLOSE', call['name'])
            attempts = _snapshot_attempts(hist['actual'])
            all_seen = _validated_attempts(attempts, cfg, call['name'], call['kind'] == 'OTHER', binding)
            for source_row, derived_row in zip(hist['actual'], all_seen):
                if source_row.get('_root_stop') is not None and not cfg['facts'][derived_row['receipt']['path']].get('root_stop'):
                    raise Refused('SNAPSHOT_ROOT_STOP_POLICY', call['name'])
            # A later attempt cannot undo an already terminal call.
            _snapshot_prefix(all_seen, call['kind'] == 'OTHER')
            eligible = [item for item in all_seen if item['time_ns'] <= ceiling_ns]
            terminal = _snapshot_prefix(eligible, call['kind'] == 'OTHER')
            if terminal is not None and hist['pending']:
                raise Refused('ATTEMPT_AFTER_TERMINAL', call['name'])
            entry = _snapshot_existing_entry(module, ctx, call)
            actual_pins = {item['receipt']['path'] for item in eligible}
            selected = [a for a in attempts if a['receipt']['path'] in actual_pins]
            row = {
                'name': call['name'], 'call': binding, 'origin': call['origin'],
                'spec': call['spec'], 'registry_entry': entry,
                'attempts': selected, 'terminal': terminal,
                'pending_at_capture': hist['pending'],
                'nonattempts': hist['nonattempts'],
                'launch_records': [r['record_pin'] for r in hist['records']],
                'after_ceiling_receipts': [r['receipt'] for r in all_seen if r['time_ns'] > ceiling_ns],
            }
            captured.append(row)
            states.append({'terminal': terminal})
            if entry is not None:
                sources.append(entry)
            sources.extend(row['launch_records'])
            sources.extend(a['receipt'] for a in selected)
            if call['origin'] == 'KIT' and call['kind'] == 'MEMBER':
                mappings.append({'name': call['name'], 'key': call['key'], 'theta_check': call['theta_check']})
        mode, terminal_ns = _snapshot_t(states, created_ns, ceiling_ns)
        _snapshot_cause_gate(policy, ctx.v006_raw, terminal_ns)
        if parse_utc_ns(date_u, 'snapshot date -u') < terminal_ns:
            raise Refused('SNAPSHOT_CREATION_BEFORE_T')
        kit = ctx.kit_entries()
        captured_kit = [{'name': name, 'entry': pin} for name, (_, pin) in sorted(kit.items())]
        excluded = []
        names = {c['name'] for c in calls}
        for name, (_, pin) in sorted(kit.items()):
            if name in names:
                continue
            stops = module.outside_stop_records(ctx, name)
            if not stops:
                raise Refused('OUTSIDE_SET_STOP_REQUIRED', name)
            excluded.append({'name': name, 'registry_entry': pin, 'stop_records': [p for _, p in stops]})
            sources.extend([pin] + [p for _, p in stops])
        launch_pins = {}
        for name in ('S0_SEED_SERIAL', module.TWIN):
            for record in ctx.records(name):
                pin = record.get('launch_json')
                if not isinstance(pin, dict) or not isinstance(pin.get('path'), str):
                    raise Refused('M15_LAUNCH_SOURCE_PIN')
                if not os.path.lexists(pin['path']):
                    continue
                checked, launch = module.read_record(pin['path'])
                if pin.get('sha256') not in (None, checked['sha256']):
                    raise Refused('M15_LAUNCH_SOURCE_PIN')
                if parse_utc_ns(launch['utc'], 'seed/twin launch') <= terminal_ns:
                    launch_pins[checked['path']] = checked
        writer = own_pin()
        # Inputs are captured from the shared read cache. The live mutable V006 is
        # replaced by its exact copied bytes, never revisited during verification.
        with snapshot_scope() as snapshot:
            frozen_sources = [
                {'path': path, 'sha256': sha256_hex(raw)}
                for path, (raw, _) in sorted(snapshot.paths.items())
                if path != os.path.realpath(ctx.cfg['v006'])
            ]
        buffers = {}

        def save(name, obj, raw=False):
            data = obj if raw else dump_bytes(obj)
            path = os.path.join(out_dir, name)
            buffers[path] = data
            return _snapshot_source_pin(path, data)

        v006 = save('GATE_CUTOFF_V006_C2V007.md', ctx.v006_raw, raw=True)
        registry = save('STEP5_LAUNCH_REGISTRY_PHASE1_SNAPSHOT_C2V007.json', {
            'schema': LAUNCH_REGISTRY_SCHEMA, 'phase': 'PHASE_1',
            'calls': [row['call'] for row in captured],
        })
        closures = []
        for i, row in enumerate(captured):
            if row['terminal'] is not None:
                row['ceiling_closure'] = None
                continue
            closure = {
                'schema': 'SCHEDULE_CEILING_CLOSURE_C2V002', 'phase': 'PHASE_1',
                'date_u': created_utc, 'deadline_utc': PHASE1_CEILING_UTC,
                'deadline_registration': policy['deadline_registration'], 'call': row['call'],
                'last_receipt': row['attempts'][-1]['receipt'] if row['attempts'] else None,
            }
            row['ceiling_closure'] = save('PHASE1_CEILING_CALL_%04d.json' % i, closure)
            closures.append(row['ceiling_closure'])
        final_policy = dict(base_doc, closures=closures)
        policy_pin = save('INTERRUPTION_POLICY_PHASE1_SNAPSHOT_C2V002.json', final_policy)
        snapshot_doc = {
            'schema': PHASE1_SNAPSHOT_SCHEMA, 'phase': 'PHASE_1', 'mode': mode,
            'created_utc': created_utc, 'date_u': date_u, 'T': format_utc_ns(terminal_ns),
            'deadline_utc': PHASE1_CEILING_UTC, 'writer': writer,
            'launcher': _policy_pin(doc['launcher'], 'snapshot launcher'), 'config': ctx.config_pin,
            'base_policy': base_pin, 'interruption_policy': policy_pin,
            'v006_copy': v006, 'registry': registry, 'calls': captured,
            'kit_entries': captured_kit, 'sources': frozen_sources,
            'registry_sources': sorted({canonical_bytes(p): p for p in sources}.values(),
                                       key=lambda p: (p['path'], p['sha256'])),
            'excluded_serials': excluded, 's0_member_mappings': mappings,
            'm15_launch_receipts': [launch_pins[k] for k in sorted(launch_pins)],
            'stop_requested': False,
            'negative_observation_custody': 'Root-trusted capture; later file appearance is not rechecked.',
        }
        snapshot_pin = save('PHASE1_CEILING_SNAPSHOT_C2V007.json', snapshot_doc)
        terminal_pins = [row['terminal']['receipt'] if row['terminal'] is not None else
                         row['attempts'][-1]['receipt'] if row['attempts'] else None for row in captured]
        terminal_pins = [pin for pin in terminal_pins if pin is not None]
        cutoff = save('STEP4_CUTOFF_RECORD_C2V001.json', {
            'schema': 'STEP4_CUTOFF_RECORD_C2V001', 'T': format_utc_ns(terminal_ns),
            'date_u': date_u, 'snapshot': snapshot_pin,
            'terminal_attempt_receipts': terminal_pins,
            'copy': dict(v006, bytes=len(ctx.v006_raw)),
            'advisory': False, 'stop_requested': False,
        })
        patch = {
            'schema': 'PHASE1_SNAPSHOT_BUILD_PATCH_C2V007', 'date_u': date_u,
            'launch_registry': registry, 'interruption_policy': policy_pin,
            'registry_verification': {'launcher': doc['launcher'], 'config': doc['config'], 'snapshot': snapshot_pin},
            'gate_cutoff': {'kind': CUTOFF_KIND['PHASE_1'], 'v006_copy': v006, 'record': cutoff},
            'call_attempts': [{'call': row['call'], 'attempts': row['attempts']} for row in captured],
        }
        patch_pin = save('PHASE1_SNAPSHOT_BUILD_PATCH_C2V007.json', patch)
        # No writes occur until all capture and time checks succeed.
        _new_dir(out_dir)
        for path, raw in sorted(buffers.items()):
            write_exclusive(path, raw)
        return {'snapshot': snapshot_pin, 'registry': registry, 'policy': policy_pin,
                'cutoff_record': cutoff, 'build_patch': patch_pin, 'T': snapshot_doc['T'], 'mode': mode}

    except module.Refusal as error:
        raise Refused(error.code, error.detail or '') from error


"""Verify only the root-captured Phase-1 evidence, never later run listings."""


def _snapshot_record(module, ctx, pin, name):
    path = _policy_pin(pin, 'snapshot launch record')['path']
    checked, doc = module.read_record(path)
    if checked != pin:
        raise Refused('SNAPSHOT_LAUNCH_RECORD_PIN')
    matches = []
    for origin, regex in (('P112', module.OWN_ATTEMPT_RE), ('KIT', module.KIT_ATTEMPT_RE)):
        match = regex.fullmatch(os.path.basename(path))
        if match:
            matches.append((origin, match))
    if len(matches) != 1:
        raise Refused('SNAPSHOT_LAUNCH_RECORD_NAME')
    origin, match = matches[0]
    schema = ('UNT_P112_' + match['kind'] + '_RECORD_CX2V001' if origin == 'P112' else
              'UNT_S0_' + match['kind'] + '_RECORD_C2V003A')
    if doc.get('name') != name or match['name'] != name or doc.get('attempt') != int(match['k']) or \
            doc.get('schema') != schema:
        raise Refused('SNAPSHOT_LAUNCH_RECORD_BINDING')
    record = dict(doc, origin=origin, outcome=match['kind'], record_pin=pin)
    module.validate_record_location(ctx, record)
    module.mount_first(ctx.cfg, origin, ctx.system)
    return record


@command_snapshot
def verify_phase1_snapshot(verification, registry_pin, policy_pin=None):
    _keys(verification, ('launcher', 'config', 'snapshot'), 'snapshot verification')
    saved, snapshot_pin, _ = read_json_pin(verification['snapshot'], 'phase1 snapshot')
    _keys(saved, (
        'schema', 'phase', 'mode', 'created_utc', 'date_u', 'T', 'deadline_utc', 'writer',
        'launcher', 'config', 'base_policy', 'interruption_policy', 'v006_copy', 'registry',
        'calls', 'kit_entries', 'sources', 'registry_sources', 'excluded_serials',
        's0_member_mappings', 'm15_launch_receipts', 'stop_requested', 'negative_observation_custody',
    ), 'phase1 snapshot')
    if saved['schema'] != PHASE1_SNAPSHOT_SCHEMA or saved['phase'] != 'PHASE_1' or \
            saved['launcher'] != _policy_pin(verification['launcher'], 'launcher') or \
            saved['config'] != _policy_pin(verification['config'], 'config') or \
            saved['registry'] != _policy_pin(registry_pin, 'registry') or \
            saved['deadline_utc'] != PHASE1_CEILING_UTC or saved['stop_requested'] is not False:
        raise Refused('SNAPSHOT_BINDING')
    if policy_pin is not None and saved['interruption_policy'] != _policy_pin(policy_pin, 'policy'):
        raise Refused('SNAPSHOT_POLICY_BINDING')
    if saved['writer'] != own_pin():
        raise Refused('SNAPSHOT_WRITER_PIN')
    if not isinstance(saved['calls'], list) or not isinstance(saved['sources'], list) or \
            not isinstance(saved['kit_entries'], list):
        raise Refused('SNAPSHOT_FORM')
    module = _p112_verifier_module(verification['launcher'])
    try:
        copy_raw, copy_pin = read_bytes_pin(saved['v006_copy'], 'frozen V006')
        config, _, _ = read_json_pin(saved['config'], 'frozen config')
        closures = [row['ceiling_closure'] for row in saved['calls'] if row.get('ceiling_closure') is not None]
        explicit = [saved[k] for k in ('writer', 'launcher', 'config', 'base_policy',
                                       'interruption_policy', 'v006_copy', 'registry')] + closures
        for pin in saved['sources'] + explicit:
            module.guard_read(_policy_pin(pin, 'snapshot source')['path'])
        with _snapshot_read_fence(saved['sources'] + explicit):
            for pin in saved['sources']:
                _snapshot_read_source(pin, module)
            original_v006 = module.read_v006

            def frozen_v006(path):
                if path != config['v006']:
                    raise Refused('SNAPSHOT_V006_BINDING')
                return copy_raw

            module.read_v006 = frozen_v006
            try:
                ctx = _registry_context_factory(module, verification['config'])
            finally:
                module.read_v006 = original_v006
            if ctx.cfg != config or ctx.config_pin != saved['config']:
                raise Refused('SNAPSHOT_CONFIG_BINDING')
            # Test contexts also receive the exact captured gate text.
            ctx.v006_raw, ctx.v006_text = copy_raw, copy_raw.decode()
            ctx.gate()
            for origin in ('P112', 'KIT'):
                module.mount_first(ctx.cfg, origin, ctx.system)
            kit = {}
            for row in saved['kit_entries']:
                _keys(row, ('name', 'entry'), 'captured kit entry')
                if row['name'] in kit:
                    raise Refused('SNAPSHOT_KIT_DUPLICATE')
                entry = module.read_pin(row['entry'])
                if entry.get('name') != row['name'] or entry.get('schema') != 'UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A':
                    raise Refused('SNAPSHOT_KIT_BINDING')
                kit[row['name']] = (entry, row['entry'])
            ctx.kit_entries = lambda: kit
            ctx._calls = None
            calls = ctx.calls()
            if len(calls) != len(saved['calls']):
                raise Refused('SNAPSHOT_CALL_SET')
            policy = interruption_policy(saved['interruption_policy'], 'PHASE_1')
            base, _, _ = read_json_pin(saved['base_policy'], 'snapshot base policy')
            final, _, _ = read_json_pin(saved['interruption_policy'], 'snapshot final policy')
            if base['closures'] or final != dict(base, closures=closures):
                raise Refused('SNAPSHOT_POLICY_BINDING')
            cfg = _receipt_cfg(EXACT_RECEIPT_KEYS, STATUS_CLASSES)
            cfg['interruption_policy'] = policy
            ceiling = parse_utc_ns(PHASE1_CEILING_UTC, 'ceiling')
            created = parse_utc_ns(saved['created_utc'], 'snapshot creation')
            derived_states, source_entries, derived_mappings = [], [], []
            states_by_call, names = {}, set()
            for call, row in zip(calls, saved['calls']):
                _keys(row, (
                    'name', 'call', 'origin', 'spec', 'registry_entry', 'attempts', 'terminal',
                    'pending_at_capture', 'nonattempts', 'launch_records', 'after_ceiling_receipts',
                    'ceiling_closure',
                ), 'snapshot call state')
                binding = _call_binding(call)
                if row['call'] != binding or row['name'] != call['name'] or row['origin'] != call['origin'] or \
                        row['spec'] != call['spec'] or row['name'] in names:
                    raise Refused('SNAPSHOT_CALL_BINDING')
                names.add(row['name'])
                if call['origin'] == 'KIT' and row['registry_entry'] is None:
                    raise Refused('SNAPSHOT_ENTRY_BINDING')
                if not isinstance(row['pending_at_capture'], list) or not isinstance(row['nonattempts'], list) or \
                        not isinstance(row['launch_records'], list) or not isinstance(row['after_ceiling_receipts'], list):
                    raise Refused('SNAPSHOT_CALL_FORM')
                if row['registry_entry'] is not None:
                    entry, checked = module.registered_entry(ctx, call)
                    if checked != row['registry_entry']:
                        raise Refused('SNAPSHOT_ENTRY_BINDING')
                    source_entries.append(checked)
                records = [_snapshot_record(module, ctx, pin, row['name']) for pin in row['launch_records']]
                if len({r['attempt'] for r in records}) != len(records):
                    raise Refused('SNAPSHOT_ATTEMPT_DUPLICATE')
                source_entries.extend(row['launch_records'])
                seen = _validated_attempts(row['attempts'], cfg, row['name'], call['kind'] == 'OTHER', binding)
                if any(item['time_ns'] > ceiling for item in seen):
                    raise Refused('SNAPSHOT_RECEIPT_AFTER_CEILING')
                for item in seen:
                    facts = cfg['facts'][item['receipt']['path']]
                    if facts['launch_record'] not in row['launch_records'] or \
                            facts['registry_entry'] != row['registry_entry']:
                        raise Refused('SNAPSHOT_ATTEMPT_SOURCE')
                terminal = _snapshot_prefix(seen, call['kind'] == 'OTHER')
                if terminal != row['terminal']:
                    raise Refused('SNAPSHOT_TERMINAL_NOT_REDERIVED')
                if terminal is not None and row['pending_at_capture']:
                    raise Refused('ATTEMPT_AFTER_TERMINAL')
                for pending in row['pending_at_capture']:
                    if pending.get('record') not in row['launch_records'] or \
                            pending.get('status') not in ('ATTEMPT_ACTIVE', 'MONITOR_ENDED_NO_RECEIPT', 'ATTEMPT_NEEDS_CLOSE'):
                        raise Refused('SNAPSHOT_PENDING_BINDING')
                source_entries.extend(a['receipt'] for a in row['attempts'])
                derived_states.append({'terminal': terminal})
                states_by_call[_call_key(binding)] = row
                if call['origin'] == 'KIT' and call['kind'] == 'MEMBER':
                    derived_mappings.append({'name': call['name'], 'key': call['key'], 'theta_check': call['theta_check']})
                closure = policy['closures'].get(_call_key(binding))
                if terminal is None:
                    if closure is None or closure['pin'] != row['ceiling_closure'] or \
                            closure['document']['last_receipt'] != (row['attempts'][-1]['receipt'] if row['attempts'] else None):
                        raise Refused('SNAPSHOT_CLOSURE_BINDING')
                elif row['ceiling_closure'] is not None or closure is not None:
                    raise Refused('SNAPSHOT_TERMINAL_HAS_CLOSURE')
            mode, terminal_ns = _snapshot_t(derived_states, created, ceiling)
            if saved['mode'] != mode or parse_utc_ns(saved['T'], 'saved T') != terminal_ns or \
                    parse_utc_ns(saved['date_u'], 'snapshot date -u') < terminal_ns:
                raise Refused('SNAPSHOT_T_NOT_REDERIVED')
            _snapshot_cause_gate(policy, copy_raw, terminal_ns)
            if derived_mappings != saved['s0_member_mappings']:
                raise Refused('SNAPSHOT_MEMBER_MAPPING')
            expected_excluded = set(kit) - names
            if {x['name'] for x in saved['excluded_serials']} != expected_excluded or \
                    len(saved['excluded_serials']) != len(expected_excluded):
                raise Refused('SNAPSHOT_EXCLUDED_SET')
            for excluded in saved['excluded_serials']:
                if excluded['registry_entry'] != kit[excluded['name']][1] or not excluded['stop_records']:
                    raise Refused('SNAPSHOT_EXCLUDED_BINDING')
                source_entries.append(excluded['registry_entry'])
                for pin in excluded['stop_records']:
                    stop = module.read_pin(pin)
                    if stop.get('schema') != 'S0_OUTSIDE_SET_STOP_RECORD_C2V001' or stop.get('name') != excluded['name'] or \
                            stop.get('plan_output_primary') != ctx.cfg['plan_output_primary'] or \
                            stop.get('fdplan') != ctx.cfg['fdplan']:
                        raise Refused('SNAPSHOT_OUTSIDE_STOP_BINDING')
                    source_entries.append(pin)
            expected_sources = sorted({canonical_bytes(p): p for p in source_entries}.values(),
                                      key=lambda p: (p['path'], p['sha256']))
            if expected_sources != saved['registry_sources']:
                raise Refused('SNAPSHOT_REGISTRY_SOURCES')
            registry_raw, checked_registry = read_bytes_pin(registry_pin, 'snapshot registry')
            derived_registry = dump_bytes({'schema': LAUNCH_REGISTRY_SCHEMA, 'phase': 'PHASE_1',
                                           'calls': [_call_binding(call) for call in calls]})
            if registry_raw != derived_registry:
                raise Refused('REGISTRY_BYTE_VERIFY')
            for pin in saved['m15_launch_receipts']:
                launch = module.read_pin(pin)
                if parse_utc_ns(launch['utc'], 'captured seed/twin launch') > terminal_ns:
                    raise Refused('SNAPSHOT_M15_AFTER_T')
        return {
            'mode': 'P112_SAVED_PHASE1_SNAPSHOT', 'verdict': 'BYTE_EQUAL',
            'registry': checked_registry, 'snapshot': snapshot_pin, 'T': saved['T'],
            'sources': saved['registry_sources'], 'captured_sources': saved['sources'],
            'nonattempts': [dict(n, name=row['name']) for row in saved['calls'] for n in row['nonattempts']],
            's0_member_mappings': saved['s0_member_mappings'], 'm15_launch_receipts': saved['m15_launch_receipts'],
            'fdplan': config['fdplan'], 'call_states': saved['calls'],
            'interruption_policy': saved['interruption_policy'], 'stop_requested': False,
        }

    except module.Refusal as error:
        raise Refused(error.code, error.detail or '') from error



_legacy_verify_launch_registry_a253 = verify_launch_registry

@command_snapshot
def verify_launch_registry(doc):
    verification = doc.get('registry_verification')
    if doc.get('phase') == 'PHASE_1' and isinstance(verification, dict) and 'snapshot' in verification:
        return verify_phase1_snapshot(verification, doc['launch_registry'], doc.get('interruption_policy'))
    return _legacy_verify_launch_registry_a253(doc)

_snapshot_parent_main_a253 = main
COMMANDS = COMMANDS + ('phase1-snapshot',)

def main(argv):
    if not argv or argv[0] != 'phase1-snapshot':
        return _snapshot_parent_main_a253(argv)
    try:
        command, args = _parse_args(argv)
        if set(args) != {'--input', '--input-sha256', '--out-dir'}:
            raise Refused('USAGE', 'phase1-snapshot requires --input, --input-sha256, --out-dir')
        doc, _ = _cmd_input(args, PHASE1_SNAPSHOT_INPUT_SCHEMA)
        result = phase1_snapshot(doc, args['--out-dir'])
        print(json.dumps(result, sort_keys=True))
        return 0
    except Stop as error:
        print(json.dumps({'stop': error.code, 'detail': error.detail}), file=sys.stderr)
        return 3
    except Refused as error:
        print(json.dumps({'refused': error.code, 'detail': error.detail}), file=sys.stderr)
        return 2


for _stage in STAGE_KEYS:
    STAGE_KEYS[_stage] = STAGE_KEYS[_stage] + ('spec_of_record',)
    if _stage != 'PLAN':
        STAGE_KEYS[_stage] += ('registry_verification', 'custody', 'interruption_policy')

for _operation in ('main', 'build', 'pass_driver', 'step7_run', 'custody_run',
                   'sensitivity_budget', 'check_gate_list', 'seal_check',
                   'tsr_record_v003', 'tsr_check'):
    globals()[_operation] = command_snapshot(globals()[_operation])

"""Current emitted rule text; predecessor wording above is historical only."""
RULE_C_TEXT = (
    'A248/A249: CAP and nonphysics outcomes never count as model failures. '
    'A counted pair consists of two distinct authenticated model failures with '
    'the same spec, driver, status, failing stage, failure code, exception class '
    'and raise site, both solo. Positive causes are ROUTE_A_NO_FIXED_POINT or '
    'clean ITERATION_BUDGET_EXHAUSTED, bound to monitor/result/finish/spec/driver '
    'hashes by the root-pinned value-free cause producer. The counted rerun RSS '
    'equals host RAM (eleven RAM for the twin or licensed full cw8). Wall caps are not doubled: '
    'the launcher uses remaining Phase-2 time; an output cap doubles on retry. '
    'Unresolved repeated solo failures are HELD_FOR_CAUSE; repeated REFUSED or '
    'BLOCKED are HELD_FOR_FIX. These holds do not constitute failure terminals.'
)
RULE_TEXT = dict(RULE_TEXT)
RULE_TEXT['c'] = RULE_C_TEXT + (
    ' FINISHED, a bound designed twin PLANNED_STOP, or the first counted model '
    'pair is terminal. Later attempts cannot undo a terminal prefix. Every '
    'actual receipt remains bound to its registered call, spec and exact theta. '
    'Attempt directories are distinct and disjoint; times strictly increase.'
)
RULE_TEXT['f'] = (
    'An authenticated model-failure terminal is EVALUATED_FAILED. CAP and '
    'nonphysics outcomes remain uncounted until the adopted schedule boundary. '
    'At that boundary an incomplete call becomes UNEVALUATED_SCHEDULE_CEILING '
    'in the phase snapshot, activating incomplete-freeze handling. The Phase-1 '
    'snapshot does not stop ongoing work for Phase 2.'
)
RULE_TEXT['phase1_snapshot'] = (
    'A253: root captures the complete planned call set and existing custody, '
    'including calls never launched. No entry, attempt or result is fabricated. '
    'The saved call-keyed closure may have last_receipt=null. T is the latest '
    'terminal time only when every call is terminal by the Phase-1 ceiling; '
    'otherwise T is 2026-11-06T05:59:00Z. Creation time is separate. '
    'An incomplete snapshot before the ceiling is refused. Later Phase-2 files '
    'are not read to reinterpret the saved Phase-1 snapshot.'
)
SENS_BUDGET_RULE = (
    'The sensitivity budget is the leading non-skipped prefix of evaluated '
    'calls or the exact V-N1 in-memory GEOMETRY_NOT_EXPOSED answers. Those '
    'geometry answers consume budget without a forward call, context or '
    'replay-index entry and do not trigger DN5. Later entries after an '
    'unevaluated call remain UNEVALUATED_BY_ORDER_TRUNCATION.'
)


"""Read-only full-cw8 receipt custody, composed into the roster builder."""


def _cw8_receipt_workers(doc, entry, entry_pin, record, where):
    role = entry.get("worker_role")
    name = entry.get("name")
    if role is None:
        # Existing entries are immutable. A new tool may close an old attempt
        # or make a retry, recording the baseline role explicitly. It must not
        # turn old serial custody into full cw8 or attach a new selection.
        baseline = {"kind": "IDENTITY_TWIN" if name == TWIN else "FULL",
                    "column_workers": 8 if name == TWIN else 1, "choice": None}
        for saved in (doc.get("worker_role"), record.get("worker_role")):
            _receipt_need(saved is None or saved == baseline, "CW8_ROLE_CUSTODY", where)
        return 8 if name == TWIN else 1
    _receipt_need(isinstance(role, dict) and
                  set(role) == {"kind", "column_workers", "choice"} and
                  type(role.get("column_workers")) is int and role["column_workers"] in (1, 8),
                  "CW8_ROLE_FORM", where)
    workers = role["column_workers"]
    _receipt_need(role["kind"] == ("IDENTITY_TWIN" if name == TWIN else "FULL") and
                  (name != TWIN or workers == 8) and
                  doc.get("worker_role") == role and record.get("worker_role") == role,
                  "CW8_ROLE_CUSTODY", where)
    spec, _, _ = read_json_pin(entry["spec"], where + ".worker_spec")
    try:
        leaf = spec["numerics"]["route_a"]["column_workers"]
    except (KeyError, TypeError):
        raise Refused("CW8_SPEC_LEAF", where) from None
    _receipt_need(type(leaf) is int and leaf == workers, "CW8_SPEC_LEAF", where)
    if name != TWIN:
        _receipt_need(record.get("watch_pid") is None, "CW8_FULL_CALL_TWIN_WATCHER", where)
    if role["choice"] is None:
        _receipt_need(workers == 1 or name == TWIN, "CW8_FULL_CALL_UNAUTHORIZED", where)
        return workers
    _receipt_need(name != TWIN and entry.get("schema") == "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001",
                  "CW8_CHOICE_SCOPE", where)
    choice, _, _ = read_json_pin(role["choice"], where + ".worker_choice")
    _receipt_need(isinstance(choice, dict) and
                  choice.get("schema") == "CW8_PHASE1_CHOICE_CX3V001",
                  "CW8_CHOICE_SCHEMA", where)
    module = _p112_verifier_module(choice.get("producer"))
    _receipt_need(hasattr(module, "cw8_check_attempt"), "CW8_LAUNCHER_VERSION", where)
    try:
        # Uses the same read-only single-buffer bridge as registry assembly.
        # Context rederives PLAN/F identity, root spec pins, the license and
        # immutable selection. Nothing from a new caller can set workers=8
        # without this independent reconstruction.
        ctx = _registry_context_factory(module, entry.get("config"))
        ctx.gate()
        call = ctx.call(name)
        saved_entry, saved_pin = module.registered_entry(ctx, call)
        module.need(saved_pin == entry_pin and saved_entry == entry, "CW8_ENTRY_RECONSTRUCTION")
        module.cw8_check_attempt(ctx, call, record, doc)
        module.need(module.cw8_role(call) == role, "CW8_ROLE_CUSTODY")
    except module.Refusal as exc:
        raise Refused(exc.code, str(exc.detail)) from None
    return workers


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
