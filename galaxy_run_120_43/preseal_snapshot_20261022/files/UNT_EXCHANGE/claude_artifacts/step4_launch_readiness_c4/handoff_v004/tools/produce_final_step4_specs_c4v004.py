"""Claude4, step-4 final-spec producer v004 (root 0697; A134 Q5): v003 (b7fb4d530eaf552995626ea059a8e06c5df85862ce007d5dded2a65b3b6a5099)
with only the certificate-registry check moved to wrapper v002 (calibration_orchestrator_cx2v006r10_c4_q5b1.py
7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d): the guard pin is the b1 certificate guard (wrapper L30,
9e3fc109); the policy-review slot rule is POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE (wrapper L74); the lo
slot proof is LO_RHO_SLOT and the lo slot is the point's registered rho record (wrapper L148-175), with no
covers_all_consumed_states. The construction of the 29 spec byte strings, every other check, the fence, the reader and
the write protocol are v003's bytes.
---- v003 docstring follows ----
Claude4, step-4 readiness V003 BUILD: closes Claude3 0105 PR-SF1, PR-SF2, PR-SF3 and PR-SF5 (owner Claude4; 0616).
v003 = produce_final_step4_specs_c4v002.py (8e835ce322219599bebb5d82d73bc523758cdfc1fb3532a76622619cc9dbeb77) with a new
trust, write and input layer. The construction of the 29 spec byte strings is v002's, unchanged (TESTED again by
reproduction: 29/29 dry and 29/29 PROVISIONAL bitwise).
FIX stage (SF-R1, the REFUTE stage's one SHOULD_FIX): this file = the BUILD bytes 28921808ae4dca50e4d572ca8febd8364e92346d9764cf2b911a938542b88f85
with only the write-failure path changed (write_outputs, _scan_staging, _read_nofollow, WriteFailed, main, the manifest's
write_protocol text and this docstring) and the five wrapper line citations of the BUILD errata corrected (comments and one
refusal message; checked against 24abe3bc). Construction, checks, fence and reader are otherwise the BUILD's bytes.

Final-spec producer for the 29 tail-ON direct step-4 calls. It turns a root-published post-adoption config (C1) into the
exact launch bytes plus a manifest of every sha that Codex1's binder must pin.

Construction (FORMAL, read from the pinned native code; unchanged from v002):
  * base := A2F10 template (coordinate spec call_spec_mapping.template) with numerics := C1 numerics.block
    (v005 c75a889f Context L1759-1765; Codex1 direct adapter eee61ac6 L24-28).
  * MAPPER family (HEADLINE_TRIAL + 8 HEADLINE corners): the native Mapper.build of the probe points (v005
    Context.probe_points L2041-2053, Mapper.build L2195-2232; core a595c5c0 Mapper L240-266); label
    'DDO154 cx2v006 theta <theta_key16>; point <point_key16>'.
  * HAND family (TAIL_REANCHOR, WORKERS_8 candidate, 16 SENS corners, 2 SENS distance plans): base + physical update + label
    (make_step4_specs_c4v001.py b87076ac L95-141). Certificate slots come from the registry record of their point, because
    the wrapper certificate_check (24abe3bc) binds bundle.driver_certificate_bindings to the slots of EVERY tail-ON spec.
  * No spec byte names C1, the registry, the seal or any sha that depends on the spec.
  * Serialization = v005 json_bytes (L285-286): json.dumps(indent=1, sort_keys=True, allow_nan=False) + newline, UTF-8.

Modes (explicitly named; there is no flag that turns a look-alike into a final run):
  final        Refuses unless it verifies from bytes (PR-SF1):
                 1. the SEAL_RECORD (root-announced pin) and the verdict, by the fields guard007 adoption() reads (42bf0ce9
                    L154-173): sealed_by = root AUTHORITY; seal prereg and compare = C1 numerics.sealed_prereg and compare;
                    seal driver = r5; frozen_addendum pinned; verdict test_mode false, decision.tests_read true, outcome
                    ADOPT_TAIL, script_sha256 = the compare sha, prereg and case_block bound; the prereg binds the case
                    block; the reviewed adoption-policy successor's APPROVED_V007_SEALS (parsed by AST, never executed)
                    holds the exact tuple (compare, prereg, addendum, report schema, verdict);
                 2. the adoption-policy checks that need no run-tree read (7c726fa2 L52-102, L121-123);
                 3. root's C1 pinned by {path, sha256}: synthetic_test false and the r5 driver;
                 4. block_source tied to the case block of record 76309ae3: it must be the C4T FILLED spec de6d7d77 that the
                    case block's C4T entry names, and its numerics must equal C1 numerics.block as canonical JSON bytes;
                 5. the certificate registry read the way the wrapper certificate_check reads it (24abe3bc L79-161): per
                    point the record identity, the slot refs, the bundle (schema UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001,
                    identity, driver_certificate_bindings = the slots) and its EPS and LO_ENVELOPE proofs (schema, gate,
                    TESTED/PASS, point sha, driver certificate, approved producer, LO covering all consumed states);
                    no A70 anchor slot on any other point (F03: no anchor promotion);
                 6. LAST: no input path or document that declares itself synthetic or a look-alike, and no input inside
                    this producer's own folder.
               A pin is exactly {path, sha256} and counts only when it re-hashes from bytes; no self-declared field counts.
  provisional  The explicitly named dry/provisional mode: any config, an optional pinned registry for the slot fill.
               Labels, file names and the manifest say PROVISIONAL and never FINAL; its manifest carries no binder_pins.
               Synthetic look-alikes may be used here and only here.

Write protocol (PR-SF2): every check, the 29 spec byte strings and the manifest bytes (allow_nan=False) are built in memory
first. Only then: a free-space check, the exclusive mkdir of the fresh staging folder --outdir (a direct child of this
producer's folder), specs/<CASE>.json by exclusive create with read-back, and the manifest LAST. So a refusal can only
happen before the first write and leaves no output folder.
Write failures (SF-R1): each output path is recorded before it is created. Any failure inside the write phase (an OSError
at mkdir, create, write, fsync or close, a read-back mismatch, or a KeyboardInterrupt) ends in exit 5 with a failure
record: a directory scan of the staging folder and its specs/ subfolder, with the size and the sha of the bytes ON DISK of
every file found, each compared with its intended bytes (COMPLETE_EQUALS_INTENDED or DIFFERS_FROM_INTENDED, so a partial or
corrupted file is named), and every FINAL or PROVISIONAL manifest found named in manifests_present_not_for_binding. The
record is printed on stdout in every case, and is also written as WRITE_FAILED_MANIFEST_C4V003.json (exclusive create,
status WRITE_FAILED_NOT_FOR_BINDING, binder_pins {}) when the disk allows that last write. If that write fails too, the
record exists on stdout only. Nothing from a run that did not exit 0 may be bound, whatever the folder holds.

Inputs (PR-SF3, PR-SF5): fence_c4v003 is installed first and refuses protected paths on the literal path before any resolve.
Each input is opened once (O_NOFOLLOW, regular file, one link, size cap checked by fstat before any byte is read), its sha
is checked, and only those bytes are parsed, by a strict JSON reader with typed codes (JSON_DUPLICATE_KEY, JSON_NONFINITE,
JSON_INTEGER_TOO_LONG, JSON_TOO_DEEP, JSON_BOM, JSON_NOT_UTF8, JSON_NUL, JSON_SYNTAX). It imports no project module,
constructs no Context, starts no process and opens no observation region, coefficient file, run tree or target file.

Usage (python3 -I -B, single-thread BLAS; numpy not needed):
  final       : produce_final_step4_specs_c4v004.py final --config C1 --config-sha SHA --seal SEAL_RECORD --seal-sha SHA
                --adoption-policy POLICY --adoption-policy-sha SHA --outdir <this producer's folder>/<new name>
                --utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" [--cases A,B,...]
  provisional : produce_final_step4_specs_c4v004.py provisional --config CFG --config-sha SHA [--registry REG --registry-sha SHA]
                --outdir <this producer's folder>/<new name> --utc "..." [--cases A,B,...]
Exit codes: 0 written; 3 REFUSED (typed code; nothing written); 4 UNEXPECTED (typed; nothing written); 5 WRITE_FAILED
(the failure record on stdout; see above); 130 INTERRUPTED (a KeyboardInterrupt outside the write phase). An argparse usage
error exits 2 with usage text on stderr, before any input is read.
"""
import ast
import calendar
import copy
import hashlib
import itertools
import json
import math
import os
import re
import stat
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FENCE_PATH = os.path.join(HERE, 'fence_c4v003.py')
FENCE_SHA = '5851f42f259ab5b967c89ec0c66e7e1573353f1076bb498e5aae60ad04b42940'


def _sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def _install_fence():
    with open(FENCE_PATH, 'rb') as f:
        raw = f.read()
    if _sha_bytes(raw) != FENCE_SHA:
        raise SystemExit('FENCE_PIN_MISMATCH')
    import importlib.util
    spec = importlib.util.spec_from_file_location('fence_c4v003', FENCE_PATH)
    m = importlib.util.module_from_spec(spec)
    sys.modules['fence_c4v003'] = m
    exec(compile(raw, FENCE_PATH, 'exec'), m.__dict__)
    if getattr(m, 'VERSION', None) != 'FENCE_C4V003':
        raise SystemExit('FENCE_VERSION_MISMATCH')
    return m


FENCE = _install_fence()
with open(os.path.abspath(__file__), 'rb') as _f:          # the tool's own bytes, read once (the manifest pins them)
    TOOL_RAW = _f.read()
TOOL_PIN = {'path': os.path.abspath(__file__), 'sha256': _sha_bytes(TOOL_RAW)}
OPENS = []


def _log_hook(event, args):                                # logging only; the fence (installed first) decides
    if event == 'open' and args and not isinstance(args[0], int):
        try:
            OPENS.append(os.fsdecode(args[0]))
        except TypeError:
            pass


sys.addaudithook(_log_hook)

R5 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
      'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
V009GEO = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py',
           '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb')
TEMPLATE_SHA = 'a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b'
COORD_SHA = '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f'
ADDENDUM_SHA = '9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9'
PAIR_PLAN = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json',
             'cb42a5a3bf8e26d0aa2a3a4c35784c2301fde7ff6c60170da7536ba8cfd95656')
CONFIG_R9 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json',
             '721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e')
C4T_FILLED = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json',
              'de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738')
CASE_BLOCK = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
              '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
PKG = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans'
SPEC_INV = (PKG + '/specs_v001/SPEC_INVENTORY_C4V001.json', '362bb571f65f7b7568ac389941aa08b4ab61ccaf69e35cb9f715199393caedd1')
PROBE_REC = (PKG + '/post_adoption_probe_v001/POST_ADOPTION_PROBE_C4V001.json',
             '7d8bd472fb55bbbdbe853249c430d8fa68e53bcbc19028c2d2e0fbd60ce5f2aa')
ANCHOR_POINT_KEY = '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'   # TAIL_REANCHOR/W8/TRIAL (SPEC_HANDOFF_C4V002)
AUTHORITY = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}  # guard007 L9
SEAL_SCHEMA_PREFIX = 'UNT_V007_SEAL_RECORD_'               # seal tool 4 (UNT_V007_SEAL_RECORD_C4V003 and its successors)
REPORT_SCHEMA_PREFIX = 'UNT_KMAX_TAIL_COMPARISON_C2V007'   # adoption policy 7c726fa2 L67
BUNDLE_SCHEMA = 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'  # certificate guard b1 9e3fc109 L13 (same string as 5f1e49e6 L13)
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'          # certificate guard b1 9e3fc109 L14 (same string as 5f1e49e6 L14)
POLICY_REVIEW_SCHEMA = 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001'   # wrapper v002 7a6af535 L40 (POLICY_SCHEMA)
CERT_GUARD_SHA = '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'  # wrapper v002 L30 pin of the b1 certificate guard
DRIVER_SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'      # wrapper v002 L74
RHO_SCHEMA, RHO_GATE = 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'RHO_G'                  # wrapper v002 L168
CERT_ROOT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'  # certificate guard ART (L18): allowed root of the chain
CAP_DEFAULT = 16 * 1024 * 1024
CAP_CERT = 8 * 1024 * 1024                                  # certificate guard _read L50-51
MAX_JSON_DEPTH = 64
MAX_INT_DIGITS = 64
SYNTH_PATH_TOKENS = ('synthetic', 'lookalike', 'look-alike', 'look_alike', 'sandbox', 'producer_test')
UTC_RE = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ')
UTC_TOLERANCE_S = 900

SCHEMA_SPEC = 'DDO154_CALIBRATION_COORDINATE_SPEC_C2V001'
SPEC_MAPPING_ID = 'C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF'
SCHEMA_THETA_KEY = 'DDO154_CALIBRATION_THETA_KEY_C2V001'
MODE_D_FIXED = 'DDO154_DISTANCE_FIXED_AT_REGISTERED'
VARYING = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m')
HULL = [151250000.0, 317625000.0]
DECLARED = {'label', 'physical.common_scale_s', 'physical.gamma', 'physical.ell_F_m', 'physical.distance_Mpc'}
SLOT_PATHS = {'numerics.uv_tail.%s%s' % (s, leaf) for s in ('eps_certificate', 'lo_certificate')
              for leaf in ('', '.path', '.sha256')}
NOTE_DRY = '; C4 0587 dry-plan TEMPLATE (EPS/LO pending); not a launch spec'
NOTE_PROV = '; C4 0587 POST-ADOPTION PROVISIONAL (slots = C4T FILLED A70 records); not a launch spec'
NOTE_FINAL = '; C4 step-4 FINAL launch spec (0587/0616)'
NOTE_PROVMODE = '; C4 step-4 producer PROVISIONAL mode (inputs not verified as the sealed adoption); not a launch spec'
STEMS = {'TAIL_REANCHOR': 'DDO154 TAIL_REANCHOR A2F10 registered anchor, config numerics',
         'WORKERS_8_CANDIDATE_ANCHOR': 'DDO154 deciding workers_8 candidate at the A2F10 anchor point, config numerics'}
MANIFEST_FINAL = 'FINAL_SPECS_MANIFEST_C4V003.json'
MANIFEST_PROV = 'PROVISIONAL_SPECS_MANIFEST_C4V003.json'
MANIFEST_FAILED = 'WRITE_FAILED_MANIFEST_C4V003.json'


class Refuse(Exception):
    @property
    def code(self):
        return str(self).split(':', 1)[0].split(' ', 1)[0]


class WriteFailed(Refuse):                # SF-R1: a write-phase failure; it carries the failure record for stdout
    def __init__(self, msg, record):
        super().__init__(msg)
        self.record = record


def need(cond, code):
    if not cond:
        raise Refuse(code)


def canonical(obj):                       # v005 c75a889f L261-262 and core a595c5c0 L34-35
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def same(a, b):                           # equality as canonical JSON bytes: True != 1.0, 128.0 != 128 (no type-lax ==)
    try:
        return canonical(a) == canonical(b)
    except (TypeError, ValueError):
        return False


def json_bytes(obj):                      # v005 c75a889f L285-286
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


# ------------------------------------------------------------------------------------------- strict JSON (PR-SF5)
def _pairs(items):                        # guard007 L62-67: a duplicate key refuses (no last-wins)
    d = {}
    for k, v in items:
        if k in d:
            raise Refuse('JSON_DUPLICATE_KEY ' + repr(k)[:60])
        d[k] = v
    return d


def _float(s):                            # guard007 L68-69: non-finite refuses (1e999 overflows to inf)
    v = float(s)
    if not math.isfinite(v):
        raise Refuse('JSON_NONFINITE ' + s[:40])
    return v


def _int(s):                              # refuse before int() so the 4300-digit ValueError can never escape
    if len(s.lstrip('-')) > MAX_INT_DIGITS:
        raise Refuse('JSON_INTEGER_TOO_LONG (%d digits > %d)' % (len(s.lstrip('-')), MAX_INT_DIGITS))
    return int(s)


def _const(s):                            # NaN, Infinity, -Infinity (guard007 L71)
    raise Refuse('JSON_NONFINITE ' + s)


def _depth_ok(text):
    depth, in_str, esc = 0, False, False
    for ch in text:
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == '[' or ch == '{':
            depth += 1
            if depth > MAX_JSON_DEPTH:
                return False
        elif ch == ']' or ch == '}':
            depth -= 1
    return True


def strict_json(raw, label):
    need(isinstance(raw, (bytes, bytearray)), 'JSON_BYTES_REQUIRED: ' + label)
    raw = bytes(raw)
    need(raw[:3] != b'\xef\xbb\xbf', 'JSON_BOM: %s (UTF-8 BOM)' % label)
    need(raw[:2] not in (b'\xff\xfe', b'\xfe\xff') and raw[:4] != b'\x00\x00\xfe\xff', 'JSON_BOM: %s (UTF-16/32 BOM)' % label)
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise Refuse('JSON_NOT_UTF8: %s (byte %d)' % (label, exc.start))
    need('\x00' not in text, 'JSON_NUL: ' + label)
    need(_depth_ok(text), 'JSON_TOO_DEEP: %s (nesting > %d)' % (label, MAX_JSON_DEPTH))
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_float=_float, parse_int=_int, parse_constant=_const)
    except Refuse as exc:
        raise Refuse('%s: %s' % (exc, label))
    except RecursionError:
        raise Refuse('JSON_TOO_DEEP: %s (recursion)' % label)
    except ValueError as exc:             # json.JSONDecodeError is a ValueError
        raise Refuse('JSON_SYNTAX: %s (%s)' % (label, str(exc)[:80]))


# ------------------------------------------------------------------------------------------- pins and reads (PR-SF3)
HEX64 = re.compile('[0-9a-f]{64}')


def strict_pin(ref, label, extra_ok=()):
    need(isinstance(ref, dict), 'PIN_REQUIRED: ' + label)
    need(set(ref) - set(extra_ok) == {'path', 'sha256'}, 'PIN_MALFORMED: %s (keys must be exactly path, sha256)' % label)
    need(isinstance(ref['path'], str) and ref['path'].startswith('/'), 'PIN_MALFORMED: %s (absolute path required)' % label)
    need(isinstance(ref['sha256'], str) and HEX64.fullmatch(ref['sha256']) is not None,
         'PIN_MALFORMED: %s (sha256 must be 64 lowercase hex)' % label)
    need(ref['sha256'] != '0' * 64, 'PIN_SHA_ZERO: ' + label)
    return {'path': ref['path'], 'sha256': ref['sha256']}


class Reader:
    """Each input file is opened ONCE: O_NOFOLLOW on the fence-resolved path, regular file, st_nlink 1, size cap checked
    by fstat before any byte is read; then its sha is checked and only those bytes are returned (and parsed)."""

    def __init__(self):
        self.reads = {}                   # resolved path -> record (the bytes are kept in memory, not in the record)
        self.raws = {}
        self.order = []

    def raw(self, ref, label, cap=CAP_DEFAULT, extra_ok=(), root=None):
        p = strict_pin(ref, label, extra_ok)
        real = FENCE.safe_resolve(p['path'], 'read ' + label)       # literal-first; FenceRefusal before any probe
        if root is not None:
            need(real == root or real.startswith(root.rstrip(os.sep) + os.sep), 'INPUT_OUTSIDE_ALLOWED_ROOT: %s (%s)' % (label, root))
        rec = self.reads.get(real)
        if rec is not None:
            need(rec['sha256'] == p['sha256'], 'PIN_CONFLICT: %s (same file pinned with two shas)' % label)
            rec['labels'].append(label)
            rec['references'] += 1
            return self.raws[real]
        try:
            fd = os.open(real, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_CLOEXEC', 0))
        except FileNotFoundError:
            raise Refuse('PIN_UNREADABLE: %s (no such file)' % label)
        except OSError as exc:
            raise Refuse('PIN_UNREADABLE: %s (%s)' % (label, type(exc).__name__))
        try:
            st = os.fstat(fd)
            need(stat.S_ISREG(st.st_mode), 'INPUT_NOT_REGULAR_FILE: ' + label)
            need(st.st_size <= cap, 'INPUT_TOO_LARGE: %s (%d > %d bytes; refused before reading)' % (label, st.st_size, cap))
            need(st.st_nlink == 1, 'INPUT_HARD_LINKED: %s (st_nlink %d)' % (label, st.st_nlink))
            chunks, n = [], 0
            while True:
                b = os.read(fd, min(1 << 20, cap + 1 - n))
                if not b:
                    break
                n += len(b)
                need(n <= cap, 'INPUT_TOO_LARGE: %s (grew while reading)' % label)
                chunks.append(b)
        finally:
            os.close(fd)
        raw = b''.join(chunks)
        need(len(raw) == st.st_size, 'INPUT_CHANGED_WHILE_READING: ' + label)
        need(_sha_bytes(raw) == p['sha256'], 'PIN_MISMATCH: ' + label)
        self.reads[real] = {'path': real, 'pinned_path': p['path'], 'sha256': p['sha256'], 'bytes': len(raw),
                            'nlink': st.st_nlink, 'labels': [label], 'references': 1, 'physical_reads': 1}
        self.raws[real] = raw
        self.order.append(real)
        return raw

    def doc(self, ref, label, cap=CAP_DEFAULT, extra_ok=(), root=None):
        d = strict_json(self.raw(ref, label, cap, extra_ok, root), label)
        need(isinstance(d, dict), 'JSON_OBJECT_REQUIRED: ' + label)
        return d

    def log(self):
        return [dict(self.reads[p]) for p in self.order]


READER = Reader()


def read_pinned(pin, label):
    return READER.raw(pin, label)


def load_pinned(pin, label, extra_ok=()):
    return READER.doc(pin, label, extra_ok=extra_ok)


def diff_paths(a, b, prefix=''):          # v005 c75a889f L532-543
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = (prefix + '.' + str(k)) if prefix else str(k)
            if k not in a or k not in b:
                out.append(p)
            else:
                out.extend(diff_paths(a[k], b[k], p))
        return out
    return [] if canonical(a) == canonical(b) else [prefix or '$']


def validate_block(block):                # core a595c5c0 L212-231, verbatim conditions
    u = block.get('uv_tail', {})
    need(u.get('enabled') is True and u.get('source_rule') == 'continuum_v001', 'BLOCK: production continuum tail-ON required')
    need(block.get('truncation') == {'shape': 'cube'}, 'BLOCK: kept cube required')
    need(block['composite_grid_spec']['breaks_inverse_kpc'][-1] == 4, 'BLOCK: kept K must be 4')
    need(u.get('outer') == {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'BLOCK: A55 K_big 128 required')
    need(u.get('gas') == {'M_s': 128, 'interp': 'lagrange3_s_gl4'}, 'BLOCK: A57 gas M_s 128 required')
    need(u.get('lambda_scale') == 1.0 and u.get('lapse_only') is True, 'BLOCK: unrescaled lapse-only tail required')
    need(block['route_a'].get('column_workers') == 8 and 'ro1_workers' not in block['route_a'], 'BLOCK: route A workers 8')
    fs = block['brackets']['rule']['fs_absolute_overrides']
    need(set(fs) == {str(i) for i in range(72)} and all(v == HULL for v in fs.values()), 'BLOCK: full A32 hull on 72 columns')
    need('mode' not in u, 'BLOCK: uv_tail.mode is not part of the reviewed r5 schema (0623)')


def point_identity(spec):                 # core a595c5c0 L233-238
    n = copy.deepcopy(spec['numerics'])
    for k in ('eps_certificate', 'lo_certificate'):
        n['uv_tail'].pop(k, None)
    return {'driver_sha256': R5[1], 'physical': spec['physical'], 'coefficients': spec['coefficients'], 'numerics': n}


def digest(obj):
    return _sha_bytes(canonical(obj))


def theta_key(theta):                     # v005 c75a889f L523-529
    th = {str(k): float(v) for k, v in theta.items()}
    return _sha_bytes(canonical({'schema': SCHEMA_THETA_KEY, 'theta': th}))


class World:
    """The construction (unchanged from v002); everything it reads comes through READER, once, from pinned bytes."""

    def __init__(self, cfg, cfg_pin, label_note, registry_pin=None):
        self.cfg, self.cfg_pin, self.note = cfg, cfg_pin, label_note
        self.inputs = {'config': cfg_pin}
        need(same(cfg.get('driver'), {'path': R5[0], 'sha256': R5[1]}), 'CONFIG_DRIVER_NOT_R5')
        read_pinned(cfg['driver'], 'driver r5 (hashed, never imported)')
        need(isinstance(cfg.get('coordinate_spec'), dict) and cfg['coordinate_spec'].get('sha256') == COORD_SHA,
             'COORDINATE_SPEC_NOT_50e7288e')
        need(isinstance(cfg.get('coordinate_spec_addendum'), dict) and cfg['coordinate_spec_addendum'].get('sha256') == ADDENDUM_SHA,
             'COORDINATE_ADDENDUM_NOT_9962b2aa')
        self.coord = load_pinned(cfg['coordinate_spec'], 'coordinate spec')
        self.addendum = load_pinned(cfg['coordinate_spec_addendum'], 'coordinate addendum')
        need(self.coord.get('schema') == SCHEMA_SPEC and
             self.coord['call_spec_mapping'].get('mapping_id') == SPEC_MAPPING_ID, 'COORDINATE_SPEC_SCHEMA')
        need(self.addendum.get('applies_to_coordinate_spec_sha256') == COORD_SHA, 'ADDENDUM_TARGET')
        cm = self.addendum.get('coordinate_mode') or {}
        need(cm.get('mode') == MODE_D_FIXED and same(cm.get('fixed_engine_coordinates'), {'distance_Mpc': 4.04}) and
             tuple(cm.get('free_coordinates') or ()) == VARYING, 'COORDINATE_MODE_NOT_D_FIXED')
        tpin = self.coord['call_spec_mapping']['template']
        need(tpin.get('sha256') == TEMPLATE_SHA, 'TEMPLATE_NOT_A2F10_a93c95b9')
        self.template = load_pinned(tpin, 'A2F10 template', extra_ok=('schema',))
        self.inputs.update(coordinate_spec=strict_pin(cfg['coordinate_spec'], 'coordinate spec'),
                           coordinate_spec_addendum=strict_pin(cfg['coordinate_spec_addendum'], 'coordinate addendum'),
                           template={'path': tpin['path'], 'sha256': tpin['sha256']}, driver=strict_pin(cfg['driver'], 'driver'))
        incl = float(self.coord['ddo154_forward_constants']['inclination_deg']['value'])
        need(self.template.get('galaxy') == 'DDO154' and float(self.template['physical']['inclination_deg']) == incl,
             'TEMPLATE_INCLINATION')
        anchor = cfg.get('anchor') or {}
        need(same(anchor.get('physical'), self.template['physical']) and
             same(anchor.get('coefficients'), self.template['coefficients']) and anchor.get('driver_sha256') == R5[1],
             'CONFIG_ANCHOR_NOT_TEMPLATE_POINT')
        need(isinstance(cfg.get('numerics'), dict) and isinstance(cfg['numerics'].get('block'), dict), 'CONFIG_NUMERICS_BLOCK_REQUIRED')
        self.block = copy.deepcopy(cfg['numerics']['block'])
        validate_block(self.block)
        self.base = copy.deepcopy(self.template)
        self.base['numerics'] = copy.deepcopy(self.block)
        need(not [p for p in diff_paths(self.template, self.base) if not (p == 'numerics' or p.startswith('numerics.'))],
             'BASE_DIFFERS_OUTSIDE_NUMERICS')
        self.by = {c['name']: c for c in self.coord['engine_coordinates']}
        self.names = [c['name'] for c in self.coord['engine_coordinates']]
        self.trial = {nm: float(self.by[nm]['trial_value']) for nm in self.names}
        need(self.trial['distance_Mpc'] == 4.04, 'TRIAL_D_NOT_4.04')
        plan = load_pinned({'path': PAIR_PLAN[0], 'sha256': PAIR_PLAN[1]}, 'DIII pair plan')
        self.pair_keys = sorted(plan['pairs'])
        self.inputs['diii_pair_plan'] = {'path': PAIR_PLAN[0], 'sha256': PAIR_PLAN[1]}
        self.pair_plan = plan
        self.registry_pin = registry_pin
        self.registry = None
        if registry_pin is not None:
            self.registry = load_pinned(registry_pin, 'certificate registry')
            need(isinstance(self.registry.get('points'), dict), 'REGISTRY_POINTS_REQUIRED')
            self.inputs['certificate_registry'] = strict_pin(registry_pin, 'certificate registry')
        self.records = {}

    # -- constructions --------------------------------------------------------------------------------------------
    def probe_points(self):               # v005 L2041-2053 with es names/trial/lower/upper from the engine coordinates
        pts = [('trial', dict(self.trial))]
        for mask in range(1 << len(VARYING)):
            th = dict(self.trial)
            lab = []
            for j, nm in enumerate(VARYING):
                hi = (mask >> j) & 1
                th[nm] = float(self.by[nm]['upper' if hi else 'lower'])
                lab.append('%s=%s' % (nm, 'hi' if hi else 'lo'))
            pts.append(('corner ' + ','.join(lab), th))
        return pts

    def fill_slots(self, spec):
        ident = point_identity(spec)
        key = digest(ident)
        rec = None
        if self.registry is not None:
            rec = self.registry['points'].get(key)
            need(isinstance(rec, dict), 'REGISTRY_POINT_MISSING: ' + key)
            need(same(rec.get('identity'), ident), 'REGISTRY_IDENTITY_MISMATCH: ' + key)
            for field in ('eps_certificate', 'lo_certificate'):
                ref = strict_pin(rec.get(field), 'registry %s %s' % (field, key[:16]))
                READER.raw(ref, 'registry %s %s' % (field, key[:16]), cap=CAP_CERT)
                spec['numerics']['uv_tail'][field] = ref          # exactly {path, sha256}: no other byte reaches the spec
            self.records[key] = rec
        return ident, key, rec

    def mapper_spec(self, theta):         # v005 Mapper.build L2195-2232 + core Mapper.build L240-266
        need(sorted(theta) == sorted(self.names), 'THETA_NAMES')
        th = {k: float(v) for k, v in theta.items()}
        for nm, v in th.items():
            need(float(self.by[nm]['lower']) <= v <= float(self.by[nm]['upper']), 'THETA_OUTSIDE_BOX ' + nm)
            if nm not in VARYING:
                need(v == self.trial[nm], 'FIXED_COORDINATE_NOT_TRIAL ' + nm)
        spec = copy.deepcopy(self.base)
        ph = spec['physical']
        need(float(ph['Eref_J']) == th['Eref_base_J'] and float(ph['entropy_K_factor']) == th['entropy_K_factor'],
             'FIXED_TEMPLATE_CHECKS')
        key = theta_key(th)
        ph['common_scale_s'] = th['common_scale_s']
        ph['gamma'] = th['gamma_over_Eref'] * th['Eref_base_J']
        ph['ell_F_m'] = th['ell_F_m']
        ph['distance_Mpc'] = th['distance_Mpc']
        need(set(diff_paths(self.base, spec)) <= DECLARED, 'UNDECLARED_MAPPER_CHANGE')
        ident, pkey, rec = self.fill_slots(spec)
        spec['label'] = 'DDO154 cx2v006 theta %s; point %s' % (key[:16], pkey[:16])
        return spec, {'theta_key': key, 'point_key': pkey, 'theta': {k: th[k] for k in VARYING + ('distance_Mpc',)}}

    def hand_spec(self, update, stem):    # make_step4_specs_c4v001.py L95-100 (+ registry slots, see module doc)
        spec = copy.deepcopy(self.base)
        spec['physical'].update(update)
        ident, pkey, rec = self.fill_slots(spec)
        spec['label'] = stem + self.note
        return spec, {'point_key': pkey}

    def build_all(self):
        out = []
        for nm in ('TAIL_REANCHOR', 'WORKERS_8_CANDIDATE_ANCHOR'):
            s, meta = self.hand_spec({}, STEMS[nm])
            need(same(s['physical'], self.cfg['anchor']['physical']), 'REANCHOR_NOT_REGISTERED_POINT')
            out.append((nm, 'HEADLINE', 'TAIL_REANCHOR' if nm == 'TAIL_REANCHOR' else 'WORKERS_8', 'HAND_ANCHOR_TEMPLATE', s, meta))
        for label, th in self.probe_points():
            s, meta = self.mapper_spec(th)
            nm = 'HEADLINE_' + ('TRIAL' if label == 'trial' else 'CORNER_' + ''.join(
                '1' if '=hi' in part else '0' for part in label[len('corner '):].split(',')))
            meta['probe_label'] = label
            out.append((nm, 'HEADLINE', 'HEADLINE_CORNER', 'MAPPER_BUILD', s, meta))
        eref = float(self.by['Eref_base_J']['trial_value'])
        for bits in itertools.product((0, 1), repeat=3):
            th = {n: float(self.by[n]['upper' if b else 'lower']) for n, b in zip(VARYING, bits)}
            for mode, edge in (('LO', 'lower'), ('HI', 'upper')):
                d = float(self.by['distance_Mpc'][edge])
                s, meta = self.hand_spec({'common_scale_s': th['common_scale_s'], 'gamma': th['gamma_over_Eref'] * eref,
                                          'ell_F_m': th['ell_F_m'], 'distance_Mpc': d},
                                         'DDO154 sensitivity corner C%s D_%s' % (''.join(map(str, bits)), mode))
                meta['distance_hex'] = d.hex()
                out.append(('SENS_CORNER_C%s_D%s' % (''.join(map(str, bits)), mode), 'SENS_' + mode, 'SENS_CORNER',
                            'HAND_SENS_CORNER_EXACT_D', s, meta))
        for edge, mode in (('lower', 'LO'), ('upper', 'HI')):
            d = float(self.by['distance_Mpc'][edge])
            s, meta = self.hand_spec({'distance_Mpc': d}, 'DDO154 sensitivity distance plan D %s' % edge)
            meta['distance_hex'] = d.hex()
            out.append(('SENS_DISTANCE_%s' % edge.upper(), 'SENS_' + mode, 'SENS_DISTANCE', 'HAND_ANCHOR_TEMPLATE_EXACT_D', s, meta))
        # per-spec checks shared by all families
        rows = []
        for nm, batch, fam, cons, s, meta in out:
            validate_block(s['numerics'])
            bad = [p for p in diff_paths(self.base, s) if p not in DECLARED and p not in SLOT_PATHS]
            need(not bad, 'UNDECLARED_CHANGE %s %s' % (nm, bad))
            need(s.get('admit') == {} and s.get('galaxy') == 'DDO154', 'FRESH_DDO154 ' + nm)
            u = s['numerics']['uv_tail']
            need(u.get('enabled') is True and 'mode' not in u, 'UV_TAIL_SCHEMA ' + nm)
            d = s['physical']['distance_Mpc']
            if batch == 'HEADLINE':
                need(d == 4.04, 'HEADLINE_D_NOT_4.04 ' + nm)
            else:
                need(d.hex() in self.pair_keys and d != 4.04, 'SENS_D_NOT_PAIR_PLAN_KEY ' + nm)
                need((batch == 'SENS_LO') == (d < 4.04), 'SENS_BATCH_D ' + nm)
            raw = json_bytes(s)
            rows.append({'case': nm, 'batch': batch, 'family': fam, 'construction': cons, 'raw': raw,
                         'sha256': _sha_bytes(raw), 'bytes': len(raw), 'label': s['label'],
                         'slots': {k: u.get(k) for k in ('eps_certificate', 'lo_certificate')},
                         'distance_Mpc': d, 'distance_hex': d.hex(), **meta})
        need(len(rows) == 29 and len({r['case'] for r in rows}) == 29, 'ROSTER_NOT_29')
        return rows


# ------------------------------------------------------------------------------------------- final-mode verification
def _literal_constants(src, label):
    """Module-level literal assignments of a source file, by AST only (the file is never executed), as in adoption policy
    constants() (7c726fa2 L15-25); a frozenset/set/tuple/list call of one literal argument is read as that container."""
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        raise Refuse('SOURCE_NOT_PARSABLE: ' + label)
    out, seen = {}, {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            for t in targets:
                if not isinstance(t, ast.Name):
                    continue
                seen[t.id] = seen.get(t.id, 0) + 1
                try:
                    if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and
                            value.func.id in ('frozenset', 'set', 'tuple', 'list') and not value.keywords and len(value.args) <= 1):
                        inner = ast.literal_eval(value.args[0]) if value.args else ()
                        out[t.id] = {'frozenset': frozenset, 'set': frozenset, 'tuple': tuple, 'list': list}[value.func.id](inner)
                    elif value is not None:
                        out[t.id] = ast.literal_eval(value)
                except (ValueError, TypeError, SyntaxError, RecursionError):
                    pass
        elif isinstance(node, (ast.AugAssign,)) and isinstance(node.target, ast.Name):
            seen[node.target.id] = seen.get(node.target.id, 0) + 2
    return out, seen, tree


def verify_final_adoption(cfg, cfg_pin, seal_pin, policy_pin, checks):
    """PR-SF1 items 1-4. Every check appends its code to checks on success; any failure raises Refuse."""
    def ok(code):
        checks.append(code)

    need(cfg.get('synthetic_test') is False, 'C1_SYNTHETIC_TEST_MUST_BE_FALSE')
    ok('C1_SYNTHETIC_TEST_FALSE')
    need(same(cfg.get('driver'), {'path': R5[0], 'sha256': R5[1]}), 'CONFIG_DRIVER_NOT_R5')
    ok('C1_DRIVER_R5')
    n = cfg.get('numerics')
    need(isinstance(n, dict), 'C1_NUMERICS_REQUIRED')
    pins = {k: strict_pin(n.get(k), 'C1 numerics.' + k) for k in ('verdict_artifact', 'block_source', 'compare',
                                                                   'sealed_prereg', 'adopted_result')}
    ok('C1_ADOPTION_FIELDS_ARE_EXACT_PINS')
    sres = n.get('source_results')
    need(isinstance(sres, list), 'C1_SOURCE_RESULTS_LIST_REQUIRED')
    for i, e in enumerate(sres):
        need(isinstance(e, dict) and isinstance(e.get('case_id'), str), 'C1_SOURCE_RESULT_MALFORMED %d' % i)
        strict_pin(e.get('result'), 'C1 source_results[%d].result' % i)
    # 1. the SEAL_RECORD, by the fields guard007 adoption() reads (L156-159)
    seal = READER.doc(seal_pin, 'V007 SEAL_RECORD')
    need(isinstance(seal.get('schema'), str) and seal['schema'].startswith(SEAL_SCHEMA_PREFIX), 'SEAL_RECORD_SCHEMA')
    need(same(seal.get('sealed_by'), AUTHORITY), 'SEALED_ROOT_BINDING: sealed_by is not the root AUTHORITY (guard007 L158)')
    need(same(seal.get('prereg'), pins['sealed_prereg']) and same(seal.get('compare'), pins['compare']),
         'SEALED_ROOT_BINDING: seal prereg/compare differ from C1 sealed_prereg/compare (guard007 L158, L167)')
    sd = strict_pin(seal.get('driver'), 'SEAL_RECORD driver')
    need(sd['sha256'] == R5[1], 'SEALED_R5_BINDING: seal driver is not r5 (guard007 L159)')
    add_pin = strict_pin(seal.get('frozen_addendum'), 'SEAL_RECORD frozen_addendum')
    need(same(seal.get('case_block'), {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}), 'SEAL_CASE_BLOCK_NOT_76309ae3')
    ok('SEAL_RECORD_ROOT_R5_PREREG_COMPARE_CASE_BLOCK')
    # the verdict (guard007 L160-161; policy L63-89, L121-123)
    rep = READER.doc(pins['verdict_artifact'], 'V007 verdict report')
    dec = rep.get('decision') if isinstance(rep.get('decision'), dict) else {}
    need(rep.get('test_mode') is False and dec.get('tests_read') is True and dec.get('outcome') == 'ADOPT_TAIL',
         'SEALED_ADOPT_TAIL_REQUIRED (guard007 L160)')
    ok('VERDICT_READS_ADOPT_TAIL')
    need(rep.get('script_sha256') == pins['compare']['sha256'] and same(rep.get('prereg'), pins['sealed_prereg']) and
         same(rep.get('case_block'), {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}), 'VERDICT_BYTE_BINDING (guard007 L161)')
    need(isinstance(rep.get('schema'), str) and rep['schema'].startswith(REPORT_SCHEMA_PREFIX), 'V007_REPORT_SCHEMA_MISMATCH')
    c4t_in = (rep.get('inputs') or {}).get('C4T') if isinstance(rep.get('inputs'), dict) else None
    need(isinstance(c4t_in, dict) and c4t_in.get('result_sha256') == pins['adopted_result']['sha256'],
         'V007_C4T_RESULT_NOT_VERDICT_INPUT (policy L84)')
    val = (rep.get('validity') or {}).get('C4T') if isinstance(rep.get('validity'), dict) else None
    need(isinstance(val, dict) and val.get('valid_all') is True, 'V007_C4T_NOT_VALID (policy L81)')
    u = dec.get('carried_numerical_uncertainty_km_s')
    need(isinstance(u, dict) and u and all(type(x) in (int, float) and math.isfinite(x) and x >= 0 for x in u.values()),
         'V007_CARRIED_UNCERTAINTY_REQUIRED (policy L121-123)')
    for e in sres:
        need(((rep.get('inputs') or {}).get(e['case_id']) or {}).get('result_sha256') == e['result']['sha256'],
             'V007_SOURCE_RESULT_NOT_VERDICT_INPUT ' + e['case_id'])
    ok('VERDICT_BINDS_COMPARE_PREREG_CASE_BLOCK_C4T_RESULT_VALIDITY_UNCERTAINTY')
    # the prereg (guard007 L162; policy L76-77)
    pre = READER.doc(pins['sealed_prereg'], 'sealed V007 prereg')
    need(same((pre.get('binding_inputs') or {}).get('case_block'), {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}),
         'PREREG_CASE_BLOCK_REQUIRED (guard007 L162)')
    ok('PREREG_BINDS_CASE_BLOCK_76309ae3')
    # the sealed compare, by AST only (policy L50-69)
    csrc = READER.raw(pins['compare'], 'sealed compare source')
    consts, seen, _ = _literal_constants(csrc, 'sealed compare source')
    pv = consts.get('V007_PREREG_SHA256')
    need(isinstance(pv, str) and HEX64.fullmatch(pv) is not None, 'V007_COMPARE_NOT_SEALED (policy L52)')
    need(pv == pins['sealed_prereg']['sha256'], 'V007_SEALED_PREREG_MISMATCH (policy L54)')
    padd = consts.get('PIN_ADDENDUM_V005')
    # Two forms: the [path, sha] pair that adoption policy r7 L56-58 expects, and the bare sha string that compare r13 L172
    # carries once sealed (seen in the seal-assembly dry run). Either way its sha must be the SEAL_RECORD frozen_addendum sha.
    if isinstance(padd, str):
        need(HEX64.fullmatch(padd) is not None, 'V007_ADDENDUM_EXACT_BYTE_PIN_REQUIRED (compare PIN_ADDENDUM_V005)')
        add_sha, add_report, add_form = padd, padd, 'sha string (compare r13 L172 form)'
    else:
        need(isinstance(padd, (list, tuple)) and len(padd) == 2 and all(isinstance(v, str) for v in padd),
             'V007_ADDENDUM_EXACT_BYTE_PIN_REQUIRED (policy L57-58)')
        add_sha, add_report, add_form = padd[1], list(padd), '[path, sha] pair (policy r7 L56-58 form)'
    need(add_sha == add_pin['sha256'], 'SEAL_FROZEN_ADDENDUM_NOT_COMPARE_PIN (guard007 L159 + policy L56-60)')
    need(same((rep.get('pins_verified') or {}).get('V005_addendum'), add_report), 'V007_REPORT_ADDENDUM_PIN_MISMATCH (policy L63)')
    need(consts.get('PRODUCTION_K_BIG_A55') == 128.0 and type(consts.get('PRODUCTION_K_BIG_A55')) is float, 'V007_COMPARE_NOT_P128 (policy L65)')
    need(consts.get('SCHEMA_REPORT') == rep['schema'], 'V007_REPORT_SCHEMA_MISMATCH (policy L67)')
    for k in ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'SCHEMA_REPORT', 'PRODUCTION_K_BIG_A55'):
        need(seen.get(k) == 1, 'COMPARE_CONSTANT_NOT_SINGLE_LITERAL ' + k)
    ok('COMPARE_SEALED_PREREG_ADDENDUM_P128_SCHEMA')
    READER.raw(add_pin, 'frozen V005 addendum (SEAL_RECORD)')
    if not isinstance(padd, str) and padd[0] != add_pin['path']:
        READER.raw({'path': padd[0], 'sha256': padd[1]}, 'frozen V005 addendum (compare PIN_ADDENDUM_V005)')
    ok('FROZEN_ADDENDUM_BYTES')
    # the case block of record and block_source (task item 4; policy L78-80, L90-93)
    cb = READER.doc({'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}, 'case block 76309ae3')
    c4t = (cb.get('cases') or {}).get('C4T') or {}
    need(c4t.get('tail') is True and R5[1] in (c4t.get('drivers_allowed') or []), 'V007_C4T_DRIVER_OR_TAIL_MISMATCH (policy L79)')
    note = c4t.get('note') if isinstance(c4t.get('note'), str) else ''
    need(C4T_FILLED[0] in note and C4T_FILLED[1] in note, 'CASE_BLOCK_C4T_NOTE_DOES_NOT_NAME_C4T_FILLED')
    need(same(pins['block_source'], {'path': C4T_FILLED[0], 'sha256': C4T_FILLED[1]}),
         'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T (block_source must be the C4T FILLED de6d7d77 that case block 76309ae3 names)')
    src = READER.doc(pins['block_source'], 'adopted C4T call spec (block_source)')
    need(same(src.get('numerics'), n.get('block')), 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T (policy L90-91; canonical JSON bytes)')
    need(src.get('admit') == {}, 'ADOPTED_SOURCE_NOT_FRESH (policy L92-93)')
    bound = ((n.get('block') or {}).get('picard') or {}).get('speed_change_bound_km_s')
    need(type(bound) in (int, float) and math.isfinite(bound) and bound > 0, 'V007_FINITE_POSITIVE_PICARD_BOUND_REQUIRED (policy L100-102)')
    ok('BLOCK_SOURCE_IS_C4T_FILLED_NAMED_BY_CASE_BLOCK_76309ae3_AND_EQUALS_C1_BLOCK')
    # the reviewed adoption-policy successor: the exact seal tuple (guard007 L163-165), by AST only
    psrc = READER.raw(policy_pin, 'adoption policy successor')
    pconsts, pseen, ptree = _literal_constants(psrc, 'adoption policy successor')
    need(pseen.get('APPROVED_V007_SEALS') == 1 and isinstance(pconsts.get('APPROVED_V007_SEALS'), frozenset),
         'ADOPTION_POLICY_SEALS_NOT_A_SINGLE_LITERAL_FROZENSET')
    need(any(isinstance(x, ast.FunctionDef) and x.name == 'check_numerics' for x in ptree.body),
         'ADOPTION_POLICY_HAS_NO_CHECK_NUMERICS')
    key = (pins['compare']['sha256'], pins['sealed_prereg']['sha256'], add_pin['sha256'], rep['schema'],
           pins['verdict_artifact']['sha256'])
    need(key in pconsts['APPROVED_V007_SEALS'], 'REVIEWED_SEAL_TUPLE_PENDING (guard007 L165)')
    ok('SEAL_TUPLE_IN_REVIEWED_POLICY_ALLOWLIST')
    v007 = {'seal': strict_pin(seal_pin, 'seal'), 'verdict': pins['verdict_artifact'], 'prereg': pins['sealed_prereg'],
            'compare': pins['compare'], 'addendum': add_pin, 'case_block': {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}}
    docs = {'seal': seal, 'verdict': rep, 'prereg': pre, 'block_source': src}
    return {'pins': pins, 'v007': v007, 'docs': docs, 'seal_tuple': list(key), 'adoption_policy': strict_pin(policy_pin, 'policy'),
            'compare_addendum_pin_form': add_form}


def verify_final_registry(w, rows, readiness, checks):
    """PR-SF1 item 5: the registry read the way the wrapper certificate_check reads it (v004: wrapper v002 7a6af535 L79-175; v003 read 24abe3bc L79-161; guard007 L199-205)."""
    for k in ('certificate_registry', 'certificate_policy_review', 'custody_deriver', 'state_enumerator'):
        READER.raw(strict_pin(readiness.get(k), 'tail_readiness.' + k), 'tail_readiness.' + k)
    prods = readiness.get('approved_certificate_producers')
    need(isinstance(prods, list) and prods, 'CERTIFICATE_PRODUCERS_REQUIRED (guard007 L202-203)')
    prods = [strict_pin(p, 'approved certificate producer') for p in prods]
    for p in prods:
        READER.raw(p, 'approved certificate producer', cap=CAP_CERT, root=CERT_ROOT)
    checks.append('TAIL_READINESS_PINS_AND_PRODUCERS_VERIFIED')
    # certificate_policy_gate (v004: wrapper v002 7a6af535 L59-77 via core checked_gate L66-79), which certificate_check runs first
    review = READER.doc(readiness['certificate_policy_review'], 'tail_readiness.certificate_policy_review')
    need(review.get('schema') == POLICY_REVIEW_SCHEMA, 'CERTIFICATE_POLICY_REVIEW_SCHEMA (core checked_gate L72-73)')
    need(review.get('status') == 'TESTED' and review.get('ok') is True, 'CERTIFICATE_POLICY_REVIEW_NOT_TESTED_OK (core L74-75)')
    bindings = {'driver_sha256': R5[1], 'custody_deriver': strict_pin(readiness['custody_deriver'], 'custody deriver'),
                'state_enumerator': strict_pin(readiness['state_enumerator'], 'state enumerator'),
                'approved_certificate_producers': prods, 'guard_sha256': CERT_GUARD_SHA,
                'driver_slot_rule': DRIVER_SLOT_RULE,
                'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
    for k, v in bindings.items():
        need(same(review.get(k), v), 'CERTIFICATE_POLICY_REVIEW_BINDING %s (wrapper L70-75 bindings)' % k)
    checks.append('CERTIFICATE_POLICY_REVIEW_GATE_AS_THE_WRAPPER_READS_IT')
    docs = {'certificate_policy_review': review}
    a70 = {k: strict_pin(w.block['uv_tail'].get(k), 'C1 block A70 ' + k) for k in ('eps_certificate', 'lo_certificate')}
    anchor_keys = {r['point_key'] for r in rows if r['case'] in ('TAIL_REANCHOR', 'WORKERS_8_CANDIDATE_ANCHOR', 'HEADLINE_TRIAL')}
    need(anchor_keys == {ANCHOR_POINT_KEY}, 'ANCHOR_POINT_KEY_NOT_8ad6ca4e')
    summary = {}
    for key in sorted({r['point_key'] for r in rows}):
        rec = w.records[key]
        ident = rec['identity']
        need(key == digest(ident), 'REGISTRY_KEY_NOT_DIGEST_OF_IDENTITY ' + key)
        slots = {f: strict_pin(rec.get(f), 'registry %s %s' % (f, key[:16])) for f in ('eps_certificate', 'lo_certificate')}
        if key != ANCHOR_POINT_KEY:
            for f in slots:
                need(not same(slots[f], a70[f]), 'A70_SLOT_OUTSIDE_ANCHOR_POINT (F03 no anchor promotion) %s %s' % (f, key[:16]))
        bpin = strict_pin(rec.get('bundle'), 'registry bundle ' + key[:16])
        bundle = READER.doc(bpin, 'point certificate bundle ' + key[:16], cap=CAP_CERT, root=CERT_ROOT)
        docs['bundle ' + key[:16]] = bundle
        need(bundle.get('schema') == BUNDLE_SCHEMA and same(bundle.get('identity'), ident),
             'BUNDLE_SCHEMA_OR_IDENTITY_MISMATCH ' + key[:16])
        need(same(bundle.get('driver_certificate_bindings'), slots), 'BUNDLE_DOES_NOT_BIND_THE_SLOTS (wrapper L145-147) ' + key[:16])
        pre = bundle.get('prelaunch')
        need(isinstance(pre, dict), 'BUNDLE_PRELAUNCH_REQUIRED ' + key[:16])
        proofs = {}
        for slot, gate in (('eps_certificate', 'EPS'), ('lo_certificate', 'LO_RHO_SLOT')):   # wrapper v002 L148
            ppin = strict_pin(pre.get(gate), 'bundle %s proof %s' % (gate, key[:16]))
            proof = READER.doc(ppin, '%s proof %s' % (gate, key[:16]), cap=CAP_CERT, root=CERT_ROOT)
            docs['%s proof %s' % (gate, key[:16])] = proof
            need(proof.get('schema') == PROOF_SCHEMA and proof.get('gate') == gate, 'PROOF_SCHEMA_OR_GATE_MISMATCH %s %s' % (gate, key[:16]))
            need(proof.get('status') == 'TESTED' and proof.get('verdict') == 'PASS', 'PROOF_NOT_TESTED_PASS %s %s' % (gate, key[:16]))
            need(proof.get('point_sha256') == key, 'PROOF_POINT_MISMATCH %s %s' % (gate, key[:16]))
            need(same(proof.get('driver_certificate'), slots[slot]), 'PROOF_DRIVER_CERTIFICATE_NOT_THE_SLOT %s %s' % (gate, key[:16]))
            prod = strict_pin(proof.get('producer'), '%s proof producer %s' % (gate, key[:16]))
            need(any(same(prod, p) for p in prods), 'PROOF_PRODUCER_NOT_APPROVED %s %s' % (gate, key[:16]))
            if gate == 'LO_RHO_SLOT':
                # wrapper v002 L160-172 (A134 Q5): the lo slot is the point's registered rho record; its proof never
                # carries covers_all_consumed_states, because LO is decided per consumed state at post-run acceptance.
                need('covers_all_consumed_states' not in proof,
                     'LO_RHO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES (wrapper v002 L163-164) ' + key[:16])
                need(same(slots[slot], rec.get('lo_certificate')), 'LO_SLOT_NOT_THE_REGISTERED_RHO_RECORD (wrapper v002 L165-166) ' + key[:16])
                rho = READER.doc(slots[slot], 'registered rho record ' + key[:16], cap=CAP_CERT, root=CERT_ROOT)
                docs['rho record ' + key[:16]] = rho
                need(rho.get('schema') == RHO_SCHEMA and rho.get('gate') == RHO_GATE and rho.get('point_sha256') == key
                     and rho.get('settings') == 'registered' and rho.get('full_registered_search_executed') is True
                     and rho.get('coverage_complete') is True,
                     'LO_SLOT_NOT_THE_FULL_REGISTERED_RHO_RECORD (wrapper v002 L168-172) ' + key[:16])
                # The wrapper compares rho.custody with the deriver's custody at launch (L169). Without running the
                # deriver, this producer checks the same custody through the proof: digest(rho.custody) must equal the
                # LO_RHO_SLOT proof's custody_sha256, which the wrapper compares with digest(custody) (L150).
                need(isinstance(rho.get('custody'), dict) and digest(rho['custody']) == proof.get('custody_sha256'),
                     'RHO_CUSTODY_NOT_THE_PROOF_CUSTODY ' + key[:16])
            proofs[gate] = ppin
        for f in slots:
            READER.raw(slots[f], 'registry %s %s' % (f, key[:16]), cap=CAP_CERT, root=CERT_ROOT)
        summary[key] = {'slots': slots, 'bundle': bpin, 'proofs': proofs}
    checks.append('REGISTRY_POINTS_BUNDLES_PROOFS_AS_CERTIFICATE_CHECK_READS_THEM')
    checks.append('NO_A70_SLOT_OUTSIDE_THE_ANCHOR_POINT')
    return summary, docs


def synthetic_gate(docs):
    """PR-SF1 item 6, run LAST: refuse self-declared synthetic or look-alike inputs, and inputs inside this folder."""
    paths, inside, docmarks = [], [], []
    for rec in READER.log():
        for p in (rec['pinned_path'], rec['path']):
            low = p.casefold()
            hit = [t for t in SYNTH_PATH_TOKENS if t in low]
            if hit and p not in paths:
                paths.append(p)
            if (p == FENCE.REVIEW or p.startswith(FENCE.REVIEW + os.sep)) and p not in inside:
                inside.append(p)
    for nm, d in sorted(docs.items()):
        if not isinstance(d, dict):
            continue
        sch = d.get('schema')
        if ('synthetic' in d and d['synthetic'] is not False) or (
                isinstance(sch, str) and (any(t in sch.upper() for t in ('SYNTHETIC', 'LOOKALIKE', 'LOOK-ALIKE', 'LOOK_ALIKE'))
                                          or sch.upper().startswith('NOT_A'))):
            docmarks.append(nm)
    why = []
    if paths:
        why.append('%d input paths carry a synthetic/look-alike marker (first: %s)' % (len(paths), paths[0]))
    if docmarks:
        why.append('%d documents declare synthetic or a look-alike schema (first: %s)' % (len(docmarks), docmarks[0]))
    if inside:
        why.append('%d inputs inside the producer folder %s (first: %s)' % (len(inside), FENCE.REVIEW, inside[0]))
    need(not why, 'SYNTHETIC_INPUT_REFUSED_IN_FINAL_MODE: ' + '; '.join(why))


# ------------------------------------------------------------------------------------------- outputs (PR-SF2)
def _check_utc(utc):
    need(isinstance(utc, str) and UTC_RE.fullmatch(utc) is not None, 'UTC_FORMAT (date -u +%Y-%m-%dT%H:%M:%SZ required)')
    try:
        t = calendar.timegm(time.strptime(utc, '%Y-%m-%dT%H:%M:%SZ'))
    except ValueError:
        raise Refuse('UTC_FORMAT (not a valid date)')
    need(abs(time.time() - t) <= UTC_TOLERANCE_S, 'UTC_NOT_CURRENT (more than %d s from the tool clock)' % UTC_TOLERANCE_S)


def _outdir_preflight(outdir, total_bytes):
    need(isinstance(outdir, str) and outdir.startswith('/'), 'OUTDIR_ABSOLUTE_REQUIRED')
    parent, name = os.path.dirname(outdir), os.path.basename(outdir)
    need(parent == FENCE.REVIEW, 'OUTDIR_NOT_A_DIRECT_CHILD_OF_THE_PRODUCER_FOLDER (%s)' % FENCE.REVIEW)
    need(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,80}', name) is not None and name != 'tools', 'OUTDIR_NAME')
    need(FENCE.safe_resolve(parent, 'outdir parent') == parent and os.path.realpath(parent) == parent,
         'OUTDIR_PARENT_NOT_CANONICAL (no symlink in the parent chain)')
    need(not os.path.lexists(outdir), 'OUTDIR_EXISTS (a fresh staging folder is required; nothing is overwritten)')
    st = os.statvfs(parent)
    free = st.f_bavail * st.f_frsize
    need(free >= 2 * total_bytes + 64 * 1024 * 1024, 'INSUFFICIENT_FREE_SPACE (%d free, %d needed)' % (free, 2 * total_bytes + 64 * 1024 * 1024))


def _xwrite(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | getattr(os, 'O_CLOEXEC', 0), 0o644)
    try:
        view = memoryview(data)
        while view:
            k = os.write(fd, view)
            view = view[k:]
        os.fsync(fd)
    finally:
        os.close(fd)


def _readback(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_CLOEXEC', 0))
    try:
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
    finally:
        os.close(fd)
    return b''.join(chunks)


def _read_nofollow(path, cap):
    """SF-R1: the bytes on disk of one staging-folder file (O_NOFOLLOW; at most cap + 1 bytes are read)."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_CLOEXEC', 0))
    try:
        chunks, n = [], 0
        while n <= cap:
            b = os.read(fd, min(1 << 20, cap + 1 - n))
            if not b:
                break
            n += len(b)
            chunks.append(b)
    finally:
        os.close(fd)
    return b''.join(chunks)


def _scan_staging(outdir, intended):
    """SF-R1: what is actually on disk after a write-phase failure. os.listdir of the staging folder and of its specs/
    subfolder (the producer creates nothing else; no recursion beyond them), lstat of every entry, and for every regular
    file the size and the sha of its bytes on disk (read with O_NOFOLLOW), compared with the intended bytes. Never raises."""
    files, other, errors = [], [], []
    specs_dir = os.path.join(outdir, 'specs')
    for d in (outdir, specs_dir):
        try:
            names = sorted(os.listdir(d))
        except FileNotFoundError:
            continue
        except BaseException as exc:
            errors.append({'path': d, 'error': type(exc).__name__})
            continue
        for nm in names:
            p = os.path.join(d, nm)
            try:
                st = os.lstat(p)
                if p == specs_dir and stat.S_ISDIR(st.st_mode):
                    continue
                if not stat.S_ISREG(st.st_mode):
                    other.append({'path': p, 'kind': 'directory' if stat.S_ISDIR(st.st_mode) else
                                  'symlink' if stat.S_ISLNK(st.st_mode) else 'other'})
                    continue
                raw = _read_nofollow(p, CAP_DEFAULT)
                want = intended.get(p)
                if len(raw) > CAP_DEFAULT:
                    state, digest_on_disk = 'TOO_LARGE_NOT_HASHED', None
                else:
                    digest_on_disk = _sha_bytes(raw)
                    state = ('UNEXPECTED_FILE' if want is None else
                             'COMPLETE_EQUALS_INTENDED' if raw == want else 'DIFFERS_FROM_INTENDED')
                files.append({'path': p, 'bytes': st.st_size if digest_on_disk is None else len(raw), 'sha256': digest_on_disk, 'state': state,
                              'intended_sha256': _sha_bytes(want) if want is not None else None,
                              'intended_bytes': len(want) if want is not None else None,
                              'is_manifest': d == outdir and nm in (MANIFEST_FINAL, MANIFEST_PROV)})
            except BaseException as exc:
                errors.append({'path': p, 'error': type(exc).__name__})
    return {'files': files, 'other_entries': other, 'errors': errors}


def write_outputs(outdir, specs, manifest_name, manifest_raw, failed_template):
    """specs: list of (case, raw). Everything is already serialized. Specs first, the manifest LAST.
    SF-R1: each path is recorded before it is created; on any failure inside the write phase (BaseException, so a
    KeyboardInterrupt too) the failure record lists what a directory scan finds on disk, with on-disk shas, and names every
    FINAL or PROVISIONAL manifest found as not for binding. It goes to stdout (WriteFailed.record) and, when the disk allows,
    to WRITE_FAILED_MANIFEST_C4V003.json by exclusive create."""
    mp = os.path.join(outdir, manifest_name)
    order = [(os.path.join(outdir, 'specs', case + '.json'), raw) for case, raw in specs] + [(mp, manifest_raw)]
    intended = dict(order)
    attempted = []
    created = False
    try:
        attempted.append(outdir)
        os.mkdir(outdir)
        created = True                    # from here on the folder is ours (exclusive mkdir), never someone else's
        attempted.append(os.path.join(outdir, 'specs'))
        os.mkdir(os.path.join(outdir, 'specs'))
        for case, raw in specs:
            p = os.path.join(outdir, 'specs', case + '.json')
            attempted.append(p)           # recorded before the file is created
            _xwrite(p, raw)
            need(_readback(p) == raw, 'READBACK_MISMATCH ' + case)
        attempted.append(mp)
        _xwrite(mp, manifest_raw)
        need(_readback(mp) == manifest_raw, 'READBACK_MISMATCH manifest')
        return {'path': mp, 'sha256': _sha_bytes(manifest_raw)}
    except BaseException as exc:          # OSError, a read-back Refuse, KeyboardInterrupt: anything inside the write phase
        scan = _scan_staging(outdir, intended) if created else {'files': [], 'other_entries': [], 'errors': []}
        files = scan['files']
        rec = dict(failed_template)
        rec.update(status='WRITE_FAILED_NOT_FOR_BINDING', error='%s: %s' % (type(exc).__name__, str(exc)[:200]),
                   interrupted=isinstance(exc, KeyboardInterrupt), staging_folder_created=created, binder_pins={},
                   intended_files=[{'path': p, 'sha256': _sha_bytes(raw), 'bytes': len(raw)} for p, raw in order],
                   attempted_in_order=list(attempted),
                   written_before_failure=files,
                   manifests_present_not_for_binding=[{'path': f['path'], 'sha256': f['sha256'], 'bytes': f['bytes'],
                                                       'state': f['state']} for f in files if f['is_manifest']],
                   other_entries=scan['other_entries'], scan_errors=scan['errors'],
                   scan='written_before_failure = every regular file that os.listdir finds in the staging folder and its '
                        'specs/ subfolder after the failure; sha256 and bytes are those ON DISK; state compares them with the '
                        'intended bytes (DIFFERS_FROM_INTENDED = partial or different)',
                   rule='Nothing in this folder may be bound, including any FINAL or PROVISIONAL manifest it holds (listed in '
                        'manifests_present_not_for_binding). Re-run into a new fresh staging folder.')
        try:
            if created:
                _xwrite(os.path.join(outdir, MANIFEST_FAILED), json_bytes(rec))
                note = 'failure manifest written'
            else:
                note = 'no folder was created'
        except BaseException as exc2:
            note = ('failure manifest not completely written (%s; a partial file may exist); the complete failure record is on '
                    'stdout only' % type(exc2).__name__)
        raise WriteFailed('WRITE_FAILED: %s: %s (%s; files on disk: %d, not equal to the intended bytes: %d, manifests not for '
                          'binding: %d)' % (type(exc).__name__, str(exc)[:160], note, len(files),
                                        sum(1 for f in files if f['state'] != 'COMPLETE_EQUALS_INTENDED'),
                                        len(rec['manifests_present_not_for_binding'])), rec)


def strip(r):
    return {k: v for k, v in r.items() if k != 'raw'}


def binder_pins(rows, pins, plan):
    """The exact {spec, driver} pins Codex1's binder must carry per call (PRELAUNCH is generated afterwards by root)."""
    out = {}
    for r in rows:
        if r['case'] in pins:
            out[r['case']] = {'spec': pins[r['case']], 'driver': {'path': R5[0], 'sha256': R5[1]},
                              'driver_role': 'PRODUCTION_R5', 'batch': r['batch'], 'family': r['family'],
                              'distance_Mpc': r['distance_Mpc'], 'tail_on': True}
    for key, pair in sorted(plan['pairs'].items()):
        tag = 'HIGH' if pair['distance_mpc'] > 4.04 else 'LOW'
        for role, name, drole in (('reference', 'V009GEO', 'REFERENCE_V009GEO'), ('new', 'R5', 'NEW_R5')):
            out['DECIDING_III_%s_%s' % (tag, name)] = {'spec': strict_pin(pair[role]['spec'], 'pair plan spec'),
                                                       'driver': strict_pin(pair[role]['driver'], 'pair plan driver'),
                                                       'driver_role': drole, 'batch': 'DIII', 'family': 'DECIDING_III',
                                                       'distance_Mpc': pair['distance_mpc'], 'tail_on': False,
                                                       'note': 'FINAL NOW: registered v006r7 file, used unchanged; root tail_off_policy binds it'}
    return out


def provisional_comparison(rows):
    prov = READER.doc({'path': PROBE_REC[0], 'sha256': PROBE_REC[1]}, 'V001 post-adoption probe')
    a70 = prov['slots']
    for r in rows:
        p = prov['specs'].get(r['case'], {})
        r['provisional_v001'] = {'path': p.get('path'), 'sha256': p.get('sha256')}
        r['slots_are_a70_records'] = same(r['slots'], a70)
        r['equals_provisional_bytes'] = r['sha256'] == p.get('sha256')
        if p.get('path'):
            q = strict_json(READER.raw({'path': p['path'], 'sha256': p['sha256']}, 'provisional ' + r['case']), 'provisional ' + r['case'])
            mine = strict_json(r['raw'], 'own spec ' + r['case'])
            q.pop('label', None)
            mine.pop('label', None)
            r['equals_provisional_except_label'] = same(q, mine)


def _plan_and_write(a, w, rows, cases, kind, extra):
    pins = {}
    specs = []
    for r in rows:
        if cases is None or r['case'] in cases:
            p = os.path.join(a.outdir, 'specs', r['case'] + '.json')
            pins[r['case']] = {'path': p, 'sha256': r['sha256']}
            specs.append((r['case'], r['raw']))
    man = {'schema': 'C4_STEP4_%s_SPECS_MANIFEST_V003' % kind, 'mode': kind.lower(), 'utc_date_u': a.utc,
           'tool_clock_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'tool': TOOL_PIN,
           'fence': {'path': FENCE_PATH, 'sha256': FENCE_SHA, 'version': FENCE.VERSION, 'blocked': list(FENCE.BLOCKED)},
           'inputs': w.inputs, 'label_note': w.note,
           'cases': [strip(r) for r in rows if cases is None or r['case'] in cases],
           'reads': READER.log(), 'opens': sorted(set(x for x in OPENS if '/.cache/codex-runtimes/' not in x)),
           'launches_performed': 0, 'processes_started': 0,
           'write_protocol': 'every check and all bytes were built in memory before the first write; specs/<CASE>.json by '
                             'exclusive create with read-back, this manifest written LAST; a folder without this manifest, '
                             'or with ' + MANIFEST_FAILED + ', or from a run that did not exit 0 with this manifest\'s sha on '
                             'stdout, is never bound'}
    man.update(extra)
    if kind == 'FINAL':
        man['status'] = 'FINAL_SPEC_BYTES_FOR_ROOT_BINDING'
        man['binder_pins'] = binder_pins(rows, pins, w.pair_plan)
        name = MANIFEST_FINAL
    else:
        man['status'] = 'PROVISIONAL_NOT_LAUNCH_SPECS'
        man['provisional_pins_never_bind'] = pins
        name = MANIFEST_PROV
        need(all('FINAL' not in r['label'] for r in rows) and 'FINAL' not in w.note, 'PROVISIONAL_LABEL_SAYS_FINAL')
    try:
        manifest_raw = json_bytes(man)
    except (TypeError, ValueError) as exc:
        raise Refuse('MANIFEST_NOT_SERIALIZABLE: %s (refused before the first write)' % str(exc)[:120])
    strict_json(manifest_raw, 'own manifest')                     # the manifest must itself pass the strict reader
    failed_template = {'schema': 'C4_STEP4_WRITE_FAILED_MANIFEST_V003', 'mode': kind.lower(), 'utc_date_u': a.utc,
                       'tool': TOOL_PIN, 'inputs_config': w.inputs.get('config'), 'intended_manifest': name}
    total = sum(len(raw) for _, raw in specs) + len(manifest_raw)
    _outdir_preflight(a.outdir, total)                            # last refusal point: nothing has been written yet
    m = write_outputs(a.outdir, specs, name, manifest_raw, failed_template)
    print(json.dumps({'status': man['status'], 'written': len(specs), 'manifest': m, 'blocked': list(FENCE.BLOCKED)}))
    return 0


def _cases(a, rows):
    cases = set(a.cases.split(',')) if a.cases else None
    if cases is not None:
        need(cases <= {r['case'] for r in rows}, 'UNKNOWN_CASE')
    return cases


def cmd_final(a):
    need(a.config and a.config_sha and a.seal and a.seal_sha and a.adoption_policy and a.adoption_policy_sha and a.outdir,
         'FINAL_ARGS: final needs --config --config-sha --seal --seal-sha --adoption-policy --adoption-policy-sha --outdir')
    need(not getattr(a, 'registry', None), 'FINAL_REGISTRY_OVERRIDE_REFUSED (final mode reads C1 tail_readiness.certificate_registry)')
    _check_utc(a.utc)
    cfg_pin = strict_pin({'path': os.path.abspath(a.config), 'sha256': a.config_sha}, 'C1 config')
    cfg = READER.doc(cfg_pin, 'C1 config')
    checks = []
    ad = verify_final_adoption(cfg, cfg_pin,
                               strict_pin({'path': os.path.abspath(a.seal), 'sha256': a.seal_sha}, 'SEAL_RECORD'),
                               strict_pin({'path': os.path.abspath(a.adoption_policy), 'sha256': a.adoption_policy_sha}, 'adoption policy'),
                               checks)
    readiness = cfg.get('tail_readiness')
    need(isinstance(readiness, dict), 'C1_TAIL_READINESS_REQUIRED')
    reg_pin = strict_pin(readiness.get('certificate_registry'),
                         'C1 tail_readiness.certificate_registry (R-C1; a null registry is refused by the guarded PRELAUNCH)')
    w = World(cfg, cfg_pin, NOTE_FINAL, registry_pin=reg_pin)
    rows = w.build_all()
    checks.append('CONSTRUCTION_29_SPECS')
    reg_summary, reg_docs = verify_final_registry(w, rows, readiness, checks)
    provisional_comparison(rows)
    cases = _cases(a, rows)
    docs = dict(ad['docs'])
    docs.update(reg_docs)
    docs.update(c1=cfg, registry=w.registry)
    synthetic_gate(docs)
    checks.append('NO_SYNTHETIC_OR_LOOKALIKE_INPUT_AND_NONE_INSIDE_THE_PRODUCER_FOLDER')
    w.inputs.update(block_source=ad['pins']['block_source'], adopted_result_pin_not_read=ad['pins']['adopted_result'],
                    v007=ad['v007'], adoption_policy=ad['adoption_policy'],
                    tail_readiness={k: strict_pin(readiness[k], k) for k in ('certificate_registry', 'certificate_policy_review',
                                                                             'custody_deriver', 'state_enumerator')},
                    approved_certificate_producers=[strict_pin(p, 'producer') for p in readiness['approved_certificate_producers']])
    extra = {'adoption_checks_passed': checks, 'seal_tuple': ad['seal_tuple'], 'registry_points': reg_summary,
             'compare_addendum_pin_form': ad['compare_addendum_pin_form'],
             'checks': {'n_written': len(rows) if cases is None else len(cases), 'all_point_keys_registered': True,
                        'mapper_family_equals_provisional_when_a70': all(r['equals_provisional_bytes'] for r in rows
                                                                         if r['construction'] == 'MAPPER_BUILD' and r['slots_are_a70_records'])},
             'not_established_here': ['the authorship of root-announced pins (the producer verifies byte custody and every '
                                      'cross-binding; root announcement and the reviewed policy allowlist are the trust anchors)',
                                      'PRELAUNCH PASS (root runs guard native_preflight on these bytes under C1; it repeats '
                                      'adoption() with check_numerics and certificate_check with custody and verify_bundle)',
                                      'certificate scientific validity (R-C1 review)']}
    return _plan_and_write(a, w, rows, cases, 'FINAL', extra)


def cmd_provisional(a):
    need(a.config and a.config_sha and a.outdir, 'PROVISIONAL_ARGS: provisional needs --config --config-sha --outdir')
    need(not (a.seal or a.adoption_policy), 'PROVISIONAL_TAKES_NO_SEAL (use final)')
    _check_utc(a.utc)
    cfg_pin = strict_pin({'path': os.path.abspath(a.config), 'sha256': a.config_sha}, 'config')
    cfg = READER.doc(cfg_pin, 'config')
    reg_pin = None
    if a.registry or a.registry_sha:
        reg_pin = strict_pin({'path': os.path.abspath(a.registry or ''), 'sha256': a.registry_sha or ''}, 'registry')
    w = World(cfg, cfg_pin, NOTE_PROVMODE, registry_pin=reg_pin)
    rows = w.build_all()
    provisional_comparison(rows)
    cases = _cases(a, rows)
    extra = {'not_established_here': ['anything about the sealed adoption: provisional mode verifies no seal, verdict, '
                                      'policy, block_source tie or certificate chain; these bytes are never launch inputs']}
    return _plan_and_write(a, w, rows, cases, 'PROVISIONAL', extra)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=('final', 'provisional'))
    for k in ('--config', '--config-sha', '--seal', '--seal-sha', '--adoption-policy', '--adoption-policy-sha',
              '--registry', '--registry-sha', '--cases'):
        ap.add_argument(k)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--utc', required=True, help='date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ, recorded verbatim')
    a = ap.parse_args(argv)
    a.outdir = os.path.abspath(a.outdir)
    try:
        return cmd_final(a) if a.command == 'final' else cmd_provisional(a)
    except Refuse as exc:
        s = str(exc)
        out = {'status': 'WRITE_FAILED' if s.startswith('WRITE_FAILED') else 'REFUSED', 'code': exc.code,
               'reason': s[:800], 'blocked': list(FENCE.BLOCKED)}
        if getattr(exc, 'record', None) is not None:              # SF-R1: the failure record survives a failed last write
            out['failure_record'] = exc.record
        print(json.dumps(out))
        return 5 if s.startswith('WRITE_FAILED') else 3
    except PermissionError as exc:                # the fence: refused before the operation happened
        print(json.dumps({'status': 'REFUSED', 'code': 'FENCE_REFUSED', 'reason': str(exc)[:800], 'blocked': list(FENCE.BLOCKED)}))
        return 3
    except Exception as exc:                      # typed, never a traceback; nothing has been written at this point
        print(json.dumps({'status': 'UNEXPECTED', 'code': 'UNEXPECTED_' + type(exc).__name__, 'reason': str(exc)[:400],
                          'blocked': list(FENCE.BLOCKED)}))
        return 4
    except KeyboardInterrupt:                     # SF-R1: inside the write phase an interrupt is already WRITE_FAILED (exit 5)
        print(json.dumps({'status': 'INTERRUPTED', 'code': 'INTERRUPTED',
                          'reason': 'KeyboardInterrupt outside the write phase; a run that does not exit 0 is never posted '
                                    'or bound', 'blocked': list(FENCE.BLOCKED)}))
        return 130


if __name__ == '__main__':
    sys.exit(main())
