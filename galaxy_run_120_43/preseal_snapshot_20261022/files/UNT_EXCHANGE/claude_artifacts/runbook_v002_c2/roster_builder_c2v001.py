#!/usr/bin/env python3
"""roster_builder_c2v001: the RUNBOOK_V002 roster builder (A133 section 3 rule (a)) and its pre-target checks.

Target-free and deterministic. Run with `python3 -I -B`. Every file this tool reads is named, with its sha256, by a
pinned JSON input document (--input PATH --input-sha256 HEX); a missing key, an unreadable file or a pin whose
bytes do not hash to its sha256 refuses. Every output is written by exclusive create. No timestamps are written,
so a second run on the same input gives the same bytes (paths of the output directory aside).

Commands
  build            rosters for RUNBOOK step 4 (stages PLAN, MEMBERS, FULL), the M-15 gate-status list (FULL) and
                   the replay plan (rule (c) terminal classes, rule (f) caps and the v003g budgets); --out-dir DIR
  pass-record      a validity-only record of one v003g pass (step 2 pass one; step 7 pass k); --out FILE
  step7            compare pass k with pass one (RUNBOOK step 7, A133 rule (b)); --out-dir DIR
  sens-budget      the v003g sensitivity budget for a value-free sensitivity plan under a replay plan; --out FILE
  check-gate-list  GATE_STATUS_LIST_DEFECT check (M-15) over the six rosters; --out FILE
  seal-check       SEAL_SHA_MISMATCH check before RUNBOOK step 9 (M-6); --out FILE
  tsr-check        TSR_FLAG_TABLE_MISMATCH check of the root TSR flag record and the freeze input_files (M-7);
                   --out FILE
Exit codes: 0 built / pass; 2 refused (an input defect; nothing adoptable); 3 pre-target stop; 1 internal error.

What the builder never does: it never reads an NGC output value (result files are hashed, never parsed), never
chooses a cut, a gate, a member or a reference, never writes a successor roster at step 7 (rule (b)), and never
reads a target.
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

BUILDER_NAME = 'roster_builder_c2v001'
INPUT_SCHEMA = 'ROSTER_BUILDER_INPUT_C2V001'
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
CLASSES = ('FINISHED', 'FAILED', 'CAP', 'INFRA', 'PLANNED_STOP')
EVALUATED_DISPOSITIONS = ('EVALUATED', 'EVALUATED_FAILED')
M15_RECORD_SCHEMA = 'M15_PRE_LAUNCH_RECORD_C2V001'
GATE_LIST_SCHEMA = 'GATE_STATUS_LIST_C2V001'
REPLAY_PLAN_SCHEMA = 'REPLAY_PLAN_C2V001'
BUILD_RECORD_SCHEMA = 'ROSTER_BUILD_RECORD_C2V001'
PASS_RECORD_SCHEMA = 'FREEZE_PASS_RECORD_C2V001'
SERVE_LOG_SCHEMA = 'REPLAY_SERVE_LOG_C2V001'
STEP7_RESULT_SCHEMA = 'STEP7_RESULT_C2V001'
ALT_NAME_RE = re.compile(r'^[A-Za-z0-9_.\-]+$')
HEX64_RE = re.compile(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])')
ISO_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z$')

# M-7 production constants (pins verified from bytes by this build; r3a section 1.4 and section 11).
TSR_FLAG_SCHEMA = 'UNT_ROOT_TSR_FLAG_RECORD_C2V001'
TSR_RULE_ID = 'M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001'
PRODUCTION_TSR = {
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


def _read_regular(path, where):
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
    return raw, os.path.realpath(path)


def read_bytes_pin(pin, where):
    if not isinstance(pin, dict) or set(pin) != {'path', 'sha256'}:
        raise Refused('PIN_SHAPE', '%s: a pin is exactly {path, sha256}' % where)
    path, sha = pin['path'], pin['sha256']
    if not isinstance(path, str) or not os.path.isabs(path) or not _is_hex64(sha):
        raise Refused('PIN_SHAPE', '%s: absolute path and lowercase 64-hex sha256 required' % where)
    raw, real = _read_regular(path, where)
    if sha256_hex(raw) != sha:
        raise Refused('PIN_MISMATCH', where)
    return raw, {'path': real, 'sha256': sha}


def read_json_pin(pin, where):
    raw, norm = read_bytes_pin(pin, where)
    doc = strict_json(raw, where)
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


def _value_free_sensitivity(doc, ids, where):
    """A budget-0 evaluate_sensitivity output carries the exact plan thetas and no NGC value."""
    if not isinstance(doc, dict) or doc.get('ok') is not True or doc.get('budget') != 0 or \
            doc.get('evaluations_used') != 0:
        raise Refused('SENSITIVITY_PLAN_NOT_BUDGET0', where)
    ev = doc.get('evaluations')
    if not isinstance(ev, list):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where)
    out = []
    for e in ev:
        if not isinstance(e, dict) or e.get('evaluated') is not False or \
                any(x is not None for x in e.get('speeds_km_s', [0])) or \
                any(x is not None for x in e.get('delta_from_reference_km_s', [0])):
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE', where)
        if not isinstance(e.get('entry_id'), str) or type(e.get('skipped_zero_displacement')) is not bool:
            raise Refused('SENSITIVITY_PLAN_SHAPE', where)
        out.append((e['entry_id'], _theta_ok(e.get('theta_ngc'), where), e['skipped_zero_displacement']))
    if len(set(x[0] for x in out)) != len(out):
        raise Refused('SENSITIVITY_PLAN_SHAPE', where + ': duplicate entry_id')
    for row in doc.get('per_query', []):
        if isinstance(row, dict) and any(row.get(k) is not None for k in (
                'reference_speed_km_s', 'box_limited_band_low_km_s', 'box_limited_band_high_km_s')):
            # a budget-0 plan still carries the reference member's row values in per_query; refuse to read them
            raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE',
                          where + ': save the plan with per_query and per_target removed (RUNBOOK step 2b)')
    if doc.get('per_target'):
        raise Refused('SENSITIVITY_PLAN_NOT_VALUE_FREE',
                      where + ': save the plan with per_query and per_target removed (RUNBOOK step 2b)')
    return out


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

def _receipt(pin, cfg, where):
    doc, norm, _ = read_json_pin(pin, where)
    if not isinstance(doc, dict):
        raise Refused('RECEIPT_SHAPE', where)
    raw_status = doc.get(cfg['status'])
    if not isinstance(raw_status, str) or raw_status not in cfg['classes']:
        raise Refused('RECEIPT_STATUS_UNMAPPED', where)
    return norm, raw_status, cfg['classes'][raw_status], parse_utc_ns(doc.get(cfg['time_utc']), where)


def _terminal(attempts, cfg, where, allow_planned):
    if not isinstance(attempts, list) or not attempts:
        raise Refused('CALL_ATTEMPTS_REQUIRED', where)
    seen = []
    for i, a in enumerate(attempts):
        w = '%s.attempts[%d]' % (where, i)
        _keys(a, ('run_dir', 'receipt'), w)
        if not isinstance(a['run_dir'], str) or not os.path.isabs(a['run_dir']) or not os.path.isdir(a['run_dir']):
            raise Refused('RUN_DIR_INVALID', w)
        run_real = os.path.realpath(a['run_dir'])
        norm, raw_status, cls, t = _receipt(a['receipt'], cfg, w + '.receipt')
        if not _under(run_real, norm['path']):
            raise Refused('RECEIPT_NOT_IN_RUN_DIR', w)
        if seen and t < seen[-1]['time_ns']:
            raise Refused('ATTEMPT_ORDER', w)
        seen.append({'run_dir': run_real, 'receipt': norm, 'raw': raw_status, 'class': cls, 'time_ns': t})
    last = seen[-1]
    if last['class'] == 'INFRA':
        raise Refused('CALL_NOT_TERMINAL', where + ': the last attempt is INFRA; rule (c) retries it')
    if last['class'] == 'PLANNED_STOP' and not allow_planned:
        raise Refused('PLANNED_STOP_NOT_A_MEMBER_TERMINAL', where)
    if last['class'] in ('FAILED', 'CAP'):
        if len(seen) < 2 or seen[-2]['class'] != last['class'] or seen[-2]['raw'] != last['raw']:
            raise Refused('RULE_C_INCOMPLETE',
                          where + ': a FAILED or CAP terminal needs two identical non-INFRA attempts (A133 (c), (f))')
    return {'class': last['class'], 'raw_status': last['raw'], 'time_ns': last['time_ns'],
            'run_dir': last['run_dir'], 'receipt': last['receipt'], 'n_attempts': len(seen),
            'receipt_paths': [s['receipt']['path'] for s in seen]}


# --------------------------------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------------------------------

STAGE_KEYS = {
    'PLAN': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest'),
    'MEMBERS': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest', 'plan_outputs', 'calls',
                'gate_cutoff', 'gate_documents', 'receipt_keys', 'receipt_status_classes'),
    'FULL': ('schema', 'phase', 'stage', 'freeze_module', 'slots', 'query_manifest', 'plan_outputs', 'calls',
             'gate_cutoff', 'gate_documents', 'receipt_keys', 'receipt_status_classes', 'sensitivity_plan_output',
             'members_stage_rosters', 'm15', 'other_phase_calls'),
}


def _roster_doc(scope, alt, slots_pin, qm_pin, mapping, gates, contexts):
    return {'schema': ROSTER_SCHEMA, 'scope': scope, 'alternative': alt, 'slots': slots_pin,
            'query_manifest': qm_pin, 'query_mapping': mapping, 'root_gates': gates,
            'outer_cut': ({'mode': 'PER_THETA', 'contexts': contexts} if contexts else {'mode': 'NONE'})}


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
        files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V001', 'stage': 'PLAN', 'phase': phase,
                                                'row_registration_rosters': roster_pins_of(roster_bytes)})
        return files, checks, ids

    # ---------------- MEMBERS / FULL ----------------
    rk = doc['receipt_keys']
    _keys(rk, ('status', 'time_utc'), 'receipt_keys')
    classes = doc['receipt_status_classes']
    if not isinstance(classes, dict) or not classes or not all(v in CLASSES for v in classes.values()):
        raise Refused('RECEIPT_STATUS_CLASSES', 'each raw status maps to one of %s' % list(CLASSES))
    cfg = {'status': rk['status'], 'time_utc': rk['time_utc'], 'classes': classes}

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
    used_paths = {}
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
        term = _terminal(c['attempts'], cfg, w, allow_planned=False)
        result = None
        if c['result'] is not None:
            _rraw, result = read_bytes_pin(c['result'], w + '.result')   # hashed, never parsed (no value is read)
            if not _under(term['run_dir'], result['path']):
                raise Refused('RESULT_NOT_OF_ITS_CALL', '%s: the result lies outside the terminal run dir' % w)
        if term['class'] == 'FINISHED' and result is None:
            raise Refused('FINISHED_WITHOUT_RESULT', w)
        cut = None
        if c['cut_record'] is not None:
            cd, cut, _ = read_json_pin(c['cut_record'], w + '.cut_record')
            if not _under(term['run_dir'], cut['path']):
                raise Refused('CUT_RECORD_NOT_OF_ITS_CALL', '%s: the cut record lies outside its call run dir' % w)
            _cut_doc_ok(cd, w + '.cut_record', fm)
        disposition = {'FINISHED': 'EVALUATED', 'FAILED': 'EVALUATED_FAILED', 'CAP': 'UNEVALUATED_CAP'}[term['class']]
        rec = {'alternative': alt, 'kind': kind, 'key': key, 'theta': theta, 'theta_sha256': theta_sha256(theta),
               'terminal': term, 'result': result, 'cut': cut, 'disposition': disposition,
               'signature': canonical_bytes([c['attempts'], c['result'], c['cut_record']])}
        if fm._canonical_bytes(theta) != canonical_bytes(theta):
            raise Refused('CANONICAL_FORM_DIVERGES', w)
        resolved[(alt, kind, key)] = rec
    # one call per (alternative, exact theta); identical call records only (A133: an equal theta is the same call)
    by_theta = {}
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in by_theta and by_theta[k]['signature'] != rec['signature']:
            raise Refused('CONTEXT_CONFLICT', '%s: two different call records at one exact theta' % rec['alternative'])
        by_theta.setdefault(k, rec)
    for rec in by_theta.values():
        paths = list(rec['terminal']['receipt_paths'])
        if rec['result'] is not None:
            paths.append(rec['result']['path'])
        if rec['cut'] is not None:
            paths.append(rec['cut']['path'])
        for p in paths:
            owner = used_paths.setdefault(p, (rec['alternative'], rec['theta_sha256']))
            if owner != (rec['alternative'], rec['theta_sha256']):
                code = 'CUT_RECORD_BORROWED' if rec['cut'] is not None and p == rec['cut']['path'] else 'FILE_BORROWED'
                raise Refused(code, 'one run file serves two calls (RI45-11: never reuse another point\'s file)')
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
    files['ROSTER_PINS.json'] = dump_bytes({'schema': 'ROSTER_PINS_C2V001', 'stage': stage, 'phase': phase,
                                            'row_registration_rosters': rpins})

    # Phase-2 FULL: member contexts byte-identical to the MEMBERS stage (the step-7 D1 check holds by construction)
    pass_one_sha = {n: rpins[n]['sha256'] for n in names}
    if stage == 'FULL':
        msr = doc['members_stage_rosters']
        if phase == 'PHASE_1':
            if msr is not None:
                raise Refused('PHASE1_STAGE', 'Phase 1 has no MEMBERS-stage rosters')
        else:
            if not isinstance(msr, dict) or set(msr) != set(names):
                raise Refused('MEMBERS_STAGE_ROSTERS_REQUIRED', 'one MEMBERS-stage roster pin per alternative')
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
                else:
                    own, cls, nat = 'NOT_RUN_PHASE1_BUDGET0', None, 0
                if budget is None and own not in EVALUATED_DISPOSITIONS:
                    budget = idx
                a['members'].append({'member_id': m[0], 'log_index': m[1], 'theta_sha256': theta_sha256(m[3]),
                                     'own_disposition': own, 'terminal_class': cls, 'n_attempts': nat})
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
    plan = {'schema': REPLAY_PLAN_SCHEMA, 'builder': BUILDER_NAME, 'phase': phase, 'stage': stage,
            'primary': primary, 'predecessor_sha256': None,
            'registered_roster_sha256': {n: rpins[n]['sha256'] for n in names},
            'pass_one_roster_sha256': pass_one_sha,
            'plan_outputs': plan_out_pins, 'alternatives': alt_plan, 'sensitivity': sens,
            'replay_index': replay_index, 'rules': RULE_TEXT, 'step4': None, 'stage0_status': None}

    if stage == 'FULL':
        files['GATE_STATUS_LIST.json'] = dump_bytes(_gate_status_list(
            doc['m15'], gate_pins, roster_docs, names, cutoff_pin, cutoff_heads, head_names, cfg))
        plan['step4'] = _step4(phase, resolved, doc['other_phase_calls'], cfg)
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
         'cutoff V006 bytes; root pins them unedited (A133 3 (a))',
    'b': 'a step-7 discrepancy makes that member UNEVALUATED (command step7); no successor roster is ever made '
         '(A133 3 (b))',
    'c': 'a call is terminal when its last attempt is FINISHED, or FAILED/CAP twice with the identical raw status; '
         'an INFRA last attempt is not terminal (A133 3 (c))',
    'f': 'a CAP terminal leaves the member UNEVALUATED (A133 3 (f)); a FAILED terminal is a v003g failure record '
         '(MEMBER_INVALID)',
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
    out = {'schema': GATE_LIST_SCHEMA, 'builder': BUILDER_NAME,
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
            t = parse_utc_ns(ldoc.get(cfg['time_utc']) if isinstance(ldoc, dict) else None,
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


def _step4(phase, resolved, other_calls, cfg):
    if not isinstance(other_calls, list):
        raise Refused('OTHER_PHASE_CALLS', 'a list (possibly empty) of non-roster NGC calls of the phase')
    receipts, labels = [], set()
    seen = set()
    for rec in resolved.values():
        k = (rec['alternative'], rec['theta_sha256'])
        if k in seen:
            continue
        seen.add(k)
        receipts.append({'label': '%s:%s:%s' % (rec['alternative'], rec['kind'], rec['key']),
                         'class': rec['terminal']['class'], 'utc_ns': rec['terminal']['time_ns']})
    for i, oc in enumerate(other_calls):
        w = 'other_phase_calls[%d]' % i
        _keys(oc, ('label', 'attempts'), w)
        if not isinstance(oc['label'], str) or not oc['label'] or oc['label'] in labels:
            raise Refused('OTHER_CALL_LABEL', w)
        labels.add(oc['label'])
        term = _terminal(oc['attempts'], cfg, w, allow_planned=True)
        receipts.append({'label': 'OTHER:' + oc['label'], 'class': term['class'], 'utc_ns': term['time_ns']})
    if not receipts:
        raise Refused('STEP4_NO_RECEIPTS', 'no terminal receipt')
    receipts.sort(key=lambda r: (r['utc_ns'], r['label']))
    start = receipts[-1]['utc_ns']
    return {'rule': ('Phase 1: step 4 begins when every Phase-1 NGC call has a terminal receipt (A133 3)'
                     if phase == 'PHASE_1' else
                     'Phase 2: step 4 begins automatically when every registered Phase-2 step-5 call has a terminal '
                     'receipt under rule (c); the start is the write time of the last registered receipt, and a '
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
    files1, checks, ids = _assemble(doc, fm, out_real)
    files2, _c2, _i2 = _assemble(doc, fm, out_real)
    if files1 != files2:
        raise Refused('NONDETERMINISTIC_BUILD', 'two in-memory builds differ')
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
              'double_run': 'BYTE_EQUAL',
              'self_check': 'freeze module _load_row_roster on every roster, _row_contract on every evaluated theta'}
    write_exclusive(os.path.join(out_abs, 'BUILD_RECORD.json'), dump_bytes(record))
    if status != 'BUILT':
        raise Refused('V003G_SELF_CHECK', failure)
    return record


# --------------------------------------------------------------------------------------------------------------
# replay adapter (RUNBOOK step 6) and pass records (steps 2 and 7)
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
        raw, norm = read_bytes_pin(entry['result'], 'replay result')
        doc = strict_json(raw, 'replay result')
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


def pass_record(label, envelopes, reference, sensitivity, serve_log):
    """Validity-only record of one pass. envelopes: {alt: v003g evaluate_envelopes output}; reference: the
    select_reference_member output; sensitivity: the evaluate_sensitivity output; serve_log: the adapter log."""
    if label not in ('PASS_ONE', 'PASS_K'):
        raise Refused('PASS_LABEL', label)
    if not isinstance(serve_log, dict) or serve_log.get('schema') != SERVE_LOG_SCHEMA or \
            not isinstance(serve_log.get('entries'), list):
        raise Refused('SERVE_LOG_SCHEMA', label)
    log_entries = serve_log['entries']
    rec = {'schema': PASS_RECORD_SCHEMA, 'pass_label': label, 'alternatives': {}, 'reference': None,
           'sensitivity': None}
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


# --------------------------------------------------------------------------------------------------------------
# step 7 (A133 3 (b)) and the sensitivity budget
# --------------------------------------------------------------------------------------------------------------

VALIDITY_FIELDS = ('evaluated', 'forward_valid_flag', 'member_valid', 'row_valid', 'row_reasons', 'served')


def step7(replay_plan, pass_one, pass_k):
    """Compare pass k with pass one. Returns (result, successor_plan_or_None).

    A member whose validity record or served result differs is made UNEVALUATED. Nothing is resolved: no roster,
    cut, gate or reference is changed or chosen, and no successor roster is produced (A133 3 (b))."""
    for p, lab in ((pass_one, 'PASS_ONE'), (pass_k, 'PASS_K')):
        if not isinstance(p, dict) or p.get('schema') != PASS_RECORD_SCHEMA or p.get('pass_label') != lab:
            raise Refused('STEP7_PASS_RECORD', lab)
    if replay_plan.get('schema') != REPLAY_PLAN_SCHEMA or replay_plan.get('stage') != 'FULL':
        raise Refused('STEP7_REPLAY_PLAN', 'a FULL-stage replay plan (or its step-7 successor) is required')
    reg, p1r = replay_plan['registered_roster_sha256'], replay_plan['pass_one_roster_sha256']
    primary = replay_plan['primary']
    evaluated = [a['name'] for a in replay_plan['alternatives'] if a['slots_status'] == ALT_EVALUATED]
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
    stops, new = [], []
    plan_alts = {a['name']: a for a in replay_plan['alternatives']}
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
        if r1 == rk and pass_one['sensitivity']['plan'] != pass_k['sensitivity']['plan']:
            stops.append('STEP7_SENSITIVITY_PLAN_DIFFERS_WITH_EQUAL_D1')
    result = {'schema': STEP7_RESULT_SCHEMA, 'builder': BUILDER_NAME, 'replay_plan_sha256': None,
              'status': None, 'new_unevaluated': [{'alternative': a, 'member_id': m} for a, m in new],
              'stops': stops, 'resolution_by_successor_roster': 'NEVER (A133 3 (b))'}
    if stops:
        result['status'] = 'STOP_NOT_MECHANIZED'
        return result, None
    if not new:
        result['status'] = 'NO_NEW_DISCREPANCY'
        return result, None
    succ = json.loads(json.dumps(replay_plan))
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
                               'budget_rule': SENS_BUDGET_RULE + '; recompute with sens-budget from the plan of the '
                                                                 'new D1 before evaluate_sensitivity'}
    succ['predecessor_sha256'] = sha256_hex(dump_bytes(replay_plan))
    result['status'] = 'NEW_UNEVALUATED'
    return result, succ


def sensitivity_budget(replay_plan, sens_doc, ids=None):
    if replay_plan.get('schema') != REPLAY_PLAN_SCHEMA:
        raise Refused('SENS_BUDGET_REPLAY_PLAN', 'replay plan schema')
    if replay_plan['phase'] == 'PHASE_1':
        return {'schema': 'SENS_BUDGET_C2V001', 'budget': 0, 'entries': [], 'rule': 'Phase 1: budget 0 (A133 1.4)'}
    entries = _value_free_sensitivity(sens_doc, ids, 'sensitivity plan')
    index = {e['theta_sha256']: e for e in replay_plan['replay_index'].get(replay_plan['primary'], [])}
    out, budget, stopped = [], 0, False
    for entry_id, theta, skipped in entries:
        key = theta_sha256(theta)
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
    return {'schema': 'SENS_BUDGET_C2V001', 'budget': budget, 'entries': out, 'rule': SENS_BUDGET_RULE}


# --------------------------------------------------------------------------------------------------------------
# M-15 list check, M-6 seal check, M-7 TSR check
# --------------------------------------------------------------------------------------------------------------

def check_gate_list(roster_pins, gate_list_pin):
    """GATE_STATUS_LIST_DEFECT (r3a 1.1): every root-listed gate of the rosters must be on the list."""
    try:
        gl, _gnorm, _ = read_json_pin(gate_list_pin, 'gate_status_list')
    except Refused as exc:
        raise Stop('GATE_STATUS_LIST_DEFECT', 'the list is missing or unreadable: ' + exc.code)
    if not isinstance(gl, dict) or gl.get('schema') != GATE_LIST_SCHEMA or not isinstance(gl.get('gates'), list):
        raise Stop('GATE_STATUS_LIST_DEFECT', 'the list is malformed')
    listed = {}
    for g in gl['gates']:
        if not isinstance(g, dict) or not isinstance(g.get('gate'), dict) or g.get('status') not in ('ON_TIME', 'LATE'):
            raise Stop('GATE_STATUS_LIST_DEFECT', 'an entry is malformed')
        listed[g['gate'].get('sha256')] = g['status']
    if not isinstance(roster_pins, dict) or not roster_pins:
        raise Refused('ROSTER_PINS_REQUIRED', 'the six-entry roster mapping')
    missing = []
    for alt in sorted(roster_pins):
        rd, _rn, _ = read_json_pin(roster_pins[alt], 'roster ' + alt)
        for g in rd.get('root_gates', []):
            if g.get('sha256') not in listed:
                missing.append('%s:%s' % (alt, g.get('sha256')))
    if missing:
        raise Stop('GATE_STATUS_LIST_DEFECT', 'root-listed gates missing from the list: %s' % missing)
    return {'schema': 'GATE_LIST_CHECK_C2V001', 'verdict': 'PASS', 'n_listed': len(listed)}


def seal_check(v006_pin, objects):
    """SEAL_SHA_MISMATCH (M-6): each sealed object hashes, from bytes, to a sha256 the seal entry names."""
    raw, vnorm = read_bytes_pin(v006_pin, 'v006_copy')
    if not isinstance(objects, list) or not objects:
        raise Refused('SEAL_OBJECTS_REQUIRED', 'objects')
    roles = {}
    for i, o in enumerate(objects):
        _keys(o, ('role', 'path', 'sha256'), 'objects[%d]' % i)
        if not isinstance(o['role'], str) or not re.match(r'^[A-Z0-9_]+$', o['role']) or o['role'] in roles:
            raise Refused('SEAL_ROLE', 'objects[%d]' % i)
        roles[o['role']] = o
    missing = [r for r in SEAL_REQUIRED_ROLES if r not in roles]
    if missing:
        raise Stop('SEAL_SHA_MISMATCH', 'no sealed sha256 for %s' % missing)
    text = raw.decode('utf-8')
    lines = text.split('\n')
    prereg = roles['PREREG_TEXT']['sha256']
    start = next((i for i, ln in enumerate(lines) if ln.startswith('## ') and prereg in ln.lower()), None)
    if start is None:
        raise Stop('SEAL_SHA_MISMATCH', 'no V006 heading carries the sealed text sha256 (the seal entry, M-6)')
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    tokens = set(HEX64_RE.findall('\n'.join(lines[start:end]).lower()))
    details, bad = [], []
    for role in sorted(roles):
        o = roles[role]
        in_entry = _is_hex64(o['sha256']) and o['sha256'] in tokens
        actual = None
        if isinstance(o['path'], str) and os.path.isabs(o['path']):
            try:
                actual = sha256_hex(_read_regular(o['path'], role)[0])
            except Refused:
                actual = None
        ok = in_entry and actual == o['sha256']
        details.append({'role': role, 'path': o['path'], 'sealed_sha256': o['sha256'], 'actual_sha256': actual,
                        'named_in_seal_entry': in_entry, 'ok': ok})
        if not ok:
            bad.append(role)
    result = {'schema': 'SEAL_CHECK_C2V001', 'v006': vnorm, 'seal_entry_heading': lines[start][3:].strip(),
              'objects': details, 'verdict': 'STOP' if bad else 'PASS',
              'code': 'SEAL_SHA_MISMATCH' if bad else None}
    if bad:
        raise Stop('SEAL_SHA_MISMATCH', 'roles %s' % bad)
    return result


def tsr_check(flag_pin, freeze_manifest_pin=None, expected=None):
    """TSR_FLAG_TABLE_MISMATCH (r3a 1.1, M-7): the flag record, the compare, N1 and node pins, and the freeze
    manifest's input_files."""
    exp = PRODUCTION_TSR if expected is None else expected
    problems = []
    try:
        fr, fnorm, _ = read_json_pin(flag_pin, 'tsr flag record')
    except Refused as exc:
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'flag record: ' + exc.code)
    if not isinstance(fr, dict) or fr.get('schema') != TSR_FLAG_SCHEMA or fr.get('rule_id') != TSR_RULE_ID:
        raise Stop('TSR_FLAG_TABLE_MISMATCH', 'flag record schema or rule_id')
    flags = fr.get('flags')
    if not isinstance(flags, list) or [f.get('query_id') if isinstance(f, dict) else None for f in flags] != \
            exp['all_ids']:
        problems.append('FLAG_TABLE_IDS')
    else:
        if any(type(f.get('TRUNCATION_SHAPE_RESIDUAL')) is not bool for f in flags):
            problems.append('FLAG_TABLE_VALUES')
        elif [f['query_id'] for f in flags if f['TRUNCATION_SHAPE_RESIDUAL']] != exp['flagged_ids']:
            problems.append('FLAGGED_SET_NOT_EXACTLY_%s' % exp['flagged_ids'])
    if fr.get('flagged_query_ids') != exp['flagged_ids']:
        problems.append('FLAGGED_QUERY_IDS')
    pins = fr.get('pins') if isinstance(fr.get('pins'), dict) else {}
    docs = {}
    for key, sk in (('ntest_compare', 'compare_sha256'), ('n1_record', 'n1_sha256'), ('gl_node_record', 'node_sha256')):
        p = pins.get(key)
        if not isinstance(p, dict) or p.get('sha256') != exp[sk]:
            problems.append('PIN_%s' % key.upper())
            continue
        try:
            docs[key], _n, _ = read_json_pin(p, key)
        except Refused as exc:
            problems.append('PIN_%s_%s' % (key.upper(), exc.code))
    sup = fr.get('support') if isinstance(fr.get('support'), dict) else {}
    if sup.get('lower_kpc') != exp['lower_kpc'] or sup.get('upper_kpc') != exp['upper_kpc'] or \
            sup.get('lower_inclusive') is not False or sup.get('upper_inclusive') is not False or \
            sup.get('ring_ordinal') != exp['failing_ordinal']:
        problems.append('SUPPORT_BOUNDS')
    c = docs.get('ntest_compare')
    if c is not None:
        rings = c.get('failing_TRUNCATION_SHAPE_rings')
        if not isinstance(rings, list) or [r.get('ordinal') for r in rings if isinstance(r, dict)] != \
                [exp['failing_ordinal']] or len(rings) != 1:
            problems.append('COMPARE_FAILING_TS_RINGS_NOT_EXACTLY_%d' % exp['failing_ordinal'])
        elif canonical_bytes(rings[0]) != canonical_bytes(fr.get('failing_ring')):
            problems.append('FAILING_RING_NOT_VERBATIM')
        if c.get('failing_non_TRUNCATION_SHAPE_rings') != []:
            problems.append('COMPARE_NON_TS_FAILING_RING')
    n1, nd = docs.get('n1_record'), docs.get('gl_node_record')
    if n1 is not None:
        rr = n1.get('ring_radii_kpc')
        k = exp['failing_ordinal']
        if not isinstance(rr, list) or len(rr) <= k + 1 or rr[k - 1] != exp['lower_kpc'] or \
                rr[k + 1] != exp['upper_kpc']:
            problems.append('N1_NEIGHBOUR_RADII')
        elif c is not None and isinstance(fr.get('failing_ring'), dict) and rr[k] != fr['failing_ring'].get('R_kpc'):
            problems.append('N1_RING_RADIUS')
        if nd is not None:
            try:
                if nd['orders']['4']['radii_kpc'] != rr:
                    problems.append('NODE_RADII_NOT_N1')
            except (KeyError, TypeError):
                problems.append('NODE_SHAPE')
    if freeze_manifest_pin is not None:
        try:
            md, _mn, _ = read_json_pin(freeze_manifest_pin, 'freeze manifest')
            have = {(p['path'], p['sha256']) for p in md['pins']['input_files']}
        except (Refused, KeyError, TypeError):
            raise Stop('TSR_FLAG_TABLE_MISMATCH', 'freeze manifest input_files unreadable')
        want = [('TSR_FLAG_RECORD', fnorm)] + [(k.upper(), pins.get(k)) for k in
                                              ('ntest_compare', 'n1_record', 'gl_node_record')]
        for label, p in want:
            if not isinstance(p, dict) or (os.path.realpath(p['path']), p['sha256']) not in have:
                problems.append('FREEZE_INPUT_FILES_LACK_' + label)
    result = {'schema': 'TSR_CHECK_C2V001', 'flag_record': fnorm, 'problems': problems,
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


def main(argv):
    try:
        cmd, args = _parse_args(argv)
        need = ('--input', '--input-sha256', '--out-dir' if cmd in ('build', 'step7') else '--out')
        if set(args) != set(need):
            raise Refused('USAGE', '%s takes exactly %s' % (cmd, list(need)))
        if cmd == 'build':
            rec = build(os.path.abspath(args['--input']), args['--input-sha256'], args['--out-dir'])
            print(json.dumps({'status': rec['status'], 'outputs': rec['outputs']}, sort_keys=True))
            return 0
        if cmd == 'pass-record':
            d, _ = _cmd_input(args, 'PASS_RECORD_INPUT_C2V001')
            _keys(d, ('schema', 'pass_label', 'envelopes', 'reference', 'sensitivity', 'serve_log'), 'input')
            env = {a: read_json_pin(p, 'envelopes.' + a)[0] for a, p in sorted(d['envelopes'].items())}
            out = pass_record(d['pass_label'], env, read_json_pin(d['reference'], 'reference')[0],
                              read_json_pin(d['sensitivity'], 'sensitivity')[0],
                              read_json_pin(d['serve_log'], 'serve_log')[0])
        elif cmd == 'step7':
            d, _ = _cmd_input(args, 'STEP7_INPUT_C2V001')
            _keys(d, ('schema', 'replay_plan', 'pass_one', 'pass_k'), 'input')
            plan, pnorm, _ = read_json_pin(d['replay_plan'], 'replay_plan')
            res, succ = step7(plan, read_json_pin(d['pass_one'], 'pass_one')[0],
                              read_json_pin(d['pass_k'], 'pass_k')[0])
            res['replay_plan_sha256'] = pnorm['sha256']
            try:
                os.mkdir(args['--out-dir'])
            except FileExistsError:
                raise Refused('OUT_DIR_EXISTS', args['--out-dir'])
            write_exclusive(os.path.join(args['--out-dir'], 'STEP7_RESULT.json'), dump_bytes(res))
            if succ is not None:
                write_exclusive(os.path.join(args['--out-dir'], 'REPLAY_PLAN.json'), dump_bytes(succ))
            print(json.dumps({'status': res['status']}))
            return 3 if res['status'] == 'STOP_NOT_MECHANIZED' else 0
        elif cmd == 'sens-budget':
            d, _ = _cmd_input(args, 'SENS_BUDGET_INPUT_C2V001')
            _keys(d, ('schema', 'replay_plan', 'sensitivity_plan_output'), 'input')
            out = sensitivity_budget(read_json_pin(d['replay_plan'], 'replay_plan')[0],
                                     read_json_pin(d['sensitivity_plan_output'], 'sensitivity plan')[0])
        elif cmd == 'check-gate-list':
            d, _ = _cmd_input(args, 'CHECK_GATE_LIST_INPUT_C2V001')
            _keys(d, ('schema', 'roster_pins', 'gate_status_list'), 'input')
            out = check_gate_list(d['roster_pins'], d['gate_status_list'])
        elif cmd == 'seal-check':
            d, _ = _cmd_input(args, 'SEAL_CHECK_INPUT_C2V001')
            _keys(d, ('schema', 'v006_copy', 'objects'), 'input')
            out = seal_check(d['v006_copy'], d['objects'])
        elif cmd == 'tsr-check':
            d, _ = _cmd_input(args, 'TSR_CHECK_INPUT_C2V001')
            _keys(d, ('schema', 'flag_record', 'freeze_manifest'), 'input')
            out = tsr_check(d['flag_record'], d['freeze_manifest'])
        else:
            raise Refused('USAGE', 'unknown command ' + repr(cmd))
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
        print(json.dumps({'internal_error': type(exc).__name__, 'detail': str(exc)[:500]}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
