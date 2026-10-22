"""Run-output identity comparator for the V007 identity gates, c2v007 (Claude2 tail_scheme_impl_c2/gates_v007).
c2v007 = successor of gates_v006/run_identity_compare_c2v006.py (097286d7) for root V005 addendum A74 (c2v007 design), A73 (SF1, SF2,
SF3, N3, N6), A71 (no last-wins anywhere), A67 N1 and A59, and for the findings that reached the build: Codex2 0445 (NPY header
duplicates, joined token labels, repeated triples), Codex2 0446 (attempt-ledger newline alias) and the c2v006 workflow's own
checker CK002 (non-existent stage numbers, Unicode stage digits, label-like raw text, IDENTITY body outside caller, comparator
argv last-wins, empty extra directories, special files).  Every c2v006 check keeps its meaning; nothing is relaxed.  Changes:
  EQUAL BYTES FIRST (A74).  Every file of both trees is compared by raw sha256 (BYTES_EQUAL).  The only files allowed to differ
     are the CLOSED, DECLARED list DECLARED_DIFFER below (literal; derived from c2v006's declared-difference classes on the three
     r4 pairs: run paths, stage numbers, cited shas of differing files, timestamps/pids, the driver and script custody pins).  An
     undeclared byte difference FAILs naming the file; a file present on one side only FAILs unless it is a declared new-only file
     (c2v006 H1 list, unchanged) or an attempt-ledger file (paired by ATTEMPT_LEDGER).  Stage logs are compared by bytes too.
  STRICT PARSE OF THE DECLARED FILES ONLY.  The store parses a file only when it is a declared file (PARSE_SURFACE); every other
     file is bytes.  JSON / JSONL use object_pairs_hook (a duplicate FAILs even when equal).  NPY headers are parsed with ast.parse:
     a non-literal, a non-dict, a non-string key or a duplicate key FAILs before any value is evaluated; NPZ members are read through
     ZipInfo (c2v006), data before the first member FAILs.  Special files (FIFO, socket, device) are never opened.
  DECLARED CLASSES.  Each declared entry names the normalizations allowed in its files; a normalization class that fires in a file
     whose entry does not allow it FAILs (DECLARED_CLASSES).  Masked keys must be present at the same paths on both sides.
  TOKENS (A73 SF2, A74).  The comparator derives the A59 token triples itself from the reference driver (the reference run's
     start.json driver, verified in REFERENCE_DRIVERS from bytes) and the selected driver (both read as restricted AST from the hashed
     bytes): SCRIPTS (route_a excluded; Z2 replaces the 8 UVT kinds by SCRIPTS_UVT, A59 F1), GALAXY_CONFIG_FILES, GC_SCHEMA and
     GC_SCHEMA_NAME as path / sha / basename forms, plus the RO1 route-A binding and facade pins for the RO1 gates.  The supplied
     list must equal the derivation exactly.  Labels must match <[A-Z0-9_]+> with no delimiter; a repeated triple is a RECORD_DEFECT;
     a raw that is not a custody form (absolute code path whose bytes hash to the paired sha, 64-hex sha, code basename, schema id)
     refuses.  Any token defect refuses the comparison (a FAIL report; nothing further is compared).  Labels are never joined.
  INJECTIVE NORMALIZATION.  One left-to-right pass replaces token raws, the run root (only at path boundaries; a stage directory
     only when it is an actual stage directory of this tree with a unique name) and 64-hex shas of this tree's files and checkpoint
     records; every other '<' is escaped as '<~'.  Every output is self-delimiting ('<RUN>', '<STAGE:name>', '<SHA:' length-prefixed
     names '>', a label), so the map is invertible: decode(N(v)) == v is checked for every normalized string (NORM_INJECTIVE).
     Raw text that contains normalizer output still FAILs NORM_INJECTIVE (c2v006 policy, kept).
  SF1 RO1 blocks must have exactly the registered key set.  SF3 a new-only static pin is admitted only when it is a (path, sha)
     entry of the selected driver's tables and its bytes hash to the sha.  N3 run paths are resolved through a containment guard that
     catches firmlink (/System/Volumes/Data) and NFC/NFD/case aliases of the registered C5H directory by parent inode + NFC casefold,
     inode aliases (/.vol) by the registered (st_dev, st_ino) from the parent listing, symlinks to any of those spellings (component
     walk) and '..' after a link; an unavailable registered identity refuses (A79.3).  A79.4: an extensionless NPZ member refuses.
  A71 everywhere: the CLI is parsed strictly (each flag exactly once, no abbreviation, no --flag=value); the attempt ledger uses
     fullmatch and the checkpoint token format; every list-to-mapping site is listed in BUILD.md with its guard (tag A71[...]).
  IDENTITY: the whole checkpoint identity body is compared (caller decoded, code, controls, environment, inputs, shapes), and
     identity_sha256 / caller.sha256 are verified as the checkpoint module's digests of the compared content on each side.
INERT on import; reads two completed run directories and pinned code (read-only); writes ONE report (exclusive create).

  python3 -I -B run_identity_compare_c2v007.py --gate GATE --driver r4|r5 --reference REF_RUN --new NEW_RUN --tokens T.json --out R.json
"""
import ast
import contextlib
import copy
import hashlib
import io
import json
import os
import re
import stat
import struct
import sys
import traceback
import types
import unicodedata
import zipfile
from pathlib import Path

SCHEMA = 'RUN_IDENTITY_COMPARE_C2V007'
CKPT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',
        '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
DRIVERS = {
    'r4': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
           'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'),
    'r5': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
           'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'),
}
DRIVER = [None, None]  # set by main() from --driver
DRIVER_RAW = [None, None]  # [verified driver bytes (one read), the path they were read from]
REFERENCE_DRIVERS = {  # A71[FIXED_KEYS]: five distinct paths, asserted below
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py':
        'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py':
        '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py':
        '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6',
    DRIVERS['r4'][0]: DRIVERS['r4'][1],
    DRIVERS['r5'][0]: DRIVERS['r5'][1],
}
assert len(REFERENCE_DRIVERS) == 5  # A71[FIXED_KEYS]: no two reference-driver paths collide (never last-wins)
_HR = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit'
# A59 derivation, RO1 gates: reference sides of the RO1 route-A binding / facade pairs (c2v003 TOKENS_Z2 ed799dc5 entries
# <ROUTE_A_BINDING_*> / <ROUTE_A_FACADE_*>; the reference run's own attempt input_pins; CK001 verified them from bytes).
RO1_REFERENCE_PINS = (('BINDING', _HR + '/ddo_composite_stable_cached_binding_v002.py',
                       'd81b24b7150c846a5b70c82a8668daaaef53335ced062763980a33cdbc90b6d5'),
                      ('FACADE', _HR + '/owned_stable_lapse_hi_facade_v001.py',
                       '2caca496183cdee6e95f9d0c9e3234734aa49b4ba08d0b0b50f02908f84beeb7'))
C5H_REGISTERED = ('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
                  'CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001')
C5H_MARKER = 'kmax_a2f10_c5h'
MASK_KEYS_BASE = {'elapsed_seconds', 'ended_unix_ns', 'started_unix_ns', 'utc', 'pid'}
TAIL_KEYS = {'uv_tail', 'uv_tail_tap'}
MASK_KEYS = set(MASK_KEYS_BASE)  # set by main() from --gate
GATES = {'Z2': (True, 'ARMED', False), 'Z2_OFF_RO1': (False, 'ARMED', True), 'Z2_OFF': (False, 'OPTIONAL', False),
         'B0P_RERUN': (False, 'UNARMED', False)}
RETIRED_GATES = {'B0PRIME_RERUN': 'gate B0PRIME_RERUN is renamed B0P_RERUN in c2v003 (root V005 A52 ruling 1: ro1 armed false, fired false)'}
RO1_GATES = ('Z2', 'Z2_OFF_RO1')
OFF_REQUEST_NAME = 'uv_tail_route_a_request_tail_off_ro1.json'
RECORD_DROP = {'attempt', 'payload_sha256', 'identity_sha256', 'iteration_start_sha256', 'checkpoint_identity_sha256'}
RO1_KEYS = frozenset({'rule', 'armed', 'fired', 'events', 'worker_sha256', 'binding_sha256'})  # A49 record; SF1 (exact key set)
HEX = re.compile(r'[0-9a-f]{64}')
SHA_RE = re.compile(r'[0-9a-f]{64}')
LABEL_RE = re.compile(r'<[A-Z0-9_]+>')  # A74: closed label grammar (fullmatch); no '|' or any other delimiter
RESERVED_LABELS = frozenset({'<RUN>', '<COLLIDED>', '<UNPARSEABLE>'})
ATTEMPT_RE = re.compile(r'(stages/[a-z0-9_]+/checkpoint/attempts)/([A-Za-z0-9_-]+)\.(start|end)\.json', re.ASCII)  # fullmatch (0446)
ATTEMPT_TOKEN_RE = re.compile(r'[0-9]{20}-[0-9]+-[0-9a-f]{8}', re.ASCII)  # the checkpoint module's token format (c2v003 L478)
STAGE_RE = re.compile(r'([0-9]{2})_([a-z0-9_]+)', re.ASCII)  # fullmatch; ASCII digits only (CK002 N10)
TEST_ONLY = 'NONE_TEST_ONLY'  # driver UVT_TEST_ONLY
TAIL_FLAGS = ('--uv-tail-config', '--uv-tail-config-sha256', '--uv-tail-admit-test-only', '--route-a-tail-manifest',
              '--route-a-tail-manifest-sha256', '--uv-tail-truncation', '--uv-tail-source-rotation-directory', '--eps-certificate',
              '--eps-certificate-sha256', '--lo-certificate', '--lo-certificate-sha256', '--uv-tail-sidecar-directory')
STAGE_RECORD_EXTRA = {'elapsed_seconds', 'executed', 'exit_code', 'request_path', 'request_sha256', 'stage_dir'}
NAME_KIND = {'route_a': 'route_a', 'route_a_tail_manifest': 'route_a_tail_manifest', 'reference': 'reference', 'body': 'body',
             'offset': 'offset'}
NORMALIZER_MARKERS = ('<RUN>', '<STAGE:', '<SHA:', '<~', '<COLLIDED', '<UNPARSEABLE', '<DUPLICATE_ARGV')
ARRAY_POLICY = ('ARRAY_IDENTITY_C2V007: arrays are compared by raw file bytes (equal bytes first).  A declared .npy / .npz is parsed '
                'strictly (header dict literal through ast.parse: duplicate keys, non-literals and non-dicts FAIL before evaluation; '
                'NPZ members by ZipInfo; data before the first member FAILs; allow_pickle False).  The c2v006 identity tuple (descr as '
                'written, dtype.str, itemsize, structured fields, shape, fortran_order, value sha256, trailing sha256) is the parsed form.')
CLASSES = ('RUN_PATH', 'STAGE_DIR', 'FILE_SHA', 'RA_SHA', 'MASKED_KEY', 'TAIL_KEY', 'DRIVER_TOKEN', 'CUSTODY_TOKEN', 'LEDGER_TOKEN',
           'RECORD_DROP', 'DECLARED_RULE')
G_ALL = ('Z2', 'Z2_OFF_RO1', 'Z2_OFF', 'B0P_RERUN')
G_A2 = ('Z2', 'Z2_OFF_RO1', 'Z2_OFF')  # the A2F10 route-A + route-B identity runs
# ---------------------------------------------------------------- A74: the CLOSED declared list (literal; BUILD.md table)
# (id, gates, canonical-path regex (fullmatch), allowed normalization classes, why).  Derived from the byte differences of the three
# r4 pairs (c2v006 r4 runs; gates_v007 BUILD.md) and the c2v006 declared-difference classes; nothing else may differ.
DECLARED_DIFFER = (
    ('D01', G_ALL, r'start\.json', ('CUSTODY_TOKEN', 'DECLARED_RULE', 'DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'TAIL_KEY'),
     'top-level start record: run paths, driver path / sha, static pins, timestamps'),
    ('D02', G_ALL, r'result\.json', ('CUSTODY_TOKEN', 'DECLARED_RULE', 'DRIVER_TOKEN', 'FILE_SHA', 'LEDGER_TOKEN', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'),
     'top-level result: run paths, cited shas of differing files, driver sha, stage records, timestamps'),
    ('D03', G_ALL, r'finish\.json', ('FILE_SHA', 'MASKED_KEY', 'RUN_PATH'), 'top-level finish: result path / sha, elapsed'),
    ('D04', G_ALL, r'progress\.jsonl', ('FILE_SHA', 'MASKED_KEY'), 'top-level progress: timestamps, elapsed'),
    ('D05', G_ALL, r'inputs/(fs|le[0-9])_manifest\.json', ('FILE_SHA', 'RUN_PATH', 'STAGE_DIR'), 'stage manifests: run directories, finish shas'),
    ('D06', G_ALL, r'inputs/galaxy_config_((columns|feedback|rotation)_v[0-9]{3}|column_mean_v[0-9]{3}_le[0-9])\.json',
     ('DRIVER_TOKEN', 'FILE_SHA', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'), 'per-stage galaxy configs: custody shas / paths of earlier stages'),
    ('D07', G_ALL, r'stages/[a-z0-9_]+/request\.json', ('CUSTODY_TOKEN', 'DRIVER_TOKEN', 'FILE_SHA', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'),
     'stage requests: argv run paths, config shas, script custody'),
    ('D08', G_ALL, r'stages/(fs_columns_[0-9]{2}|rfs_columns_[0-9]{2}|le[0-9]_columns_[0-9]{2})/columns/(column_[0-9]{4}|start|finish)\.json',
     ('DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'), 'column stage records: paths, cited shas, elapsed'),
    ('D09', G_ALL, r'stages/(fs|le[0-9])_feedback/feedback/((start|finish)\.json|progress\.jsonl)',
     ('DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'), 'feedback stage records'),
    ('D10', G_ALL, r'stages/(fs|le[0-9])_rotation/rotation/((start|finish)\.json|progress\.jsonl)',
     ('DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'), 'rotation stage records'),
    ('D11', G_ALL, r'stages/le[0-9]_column_mean/observation/result\.json',
     ('DRIVER_TOKEN', 'FILE_SHA', 'RUN_PATH', 'STAGE_DIR'), 'column-mean observation records'),
    ('D12', G_ALL, r'stages/offset/offset/((start|finish)\.json|progress\.jsonl)',
     ('DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'), 'offset stage records'),
    ('D13', G_A2, r'inputs/call_spec\.json', ('DECLARED_RULE', 'TAIL_KEY'), 'call spec: label (custody text), uv_tail'),
    ('D14', G_A2, r'inputs/galaxy_config_(body|offset|reference)\.json', ('DRIVER_TOKEN', 'FILE_SHA', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'),
     'reference / body / offset galaxy configs'),
    ('D15', G_A2, r'stages/(body/body|reference/reference)/((radius_[0-9]{4}|start|finish)\.json|progress\.jsonl)',
     ('DRIVER_TOKEN', 'FILE_SHA', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'), 'reference / body stage records'),
    ('D16', G_A2, r'stages/route_a/attempt_[0-9]{3}/((start|finish|result)\.json|progress\.jsonl)',
     ('CUSTODY_TOKEN', 'DECLARED_RULE', 'DRIVER_TOKEN', 'FILE_SHA', 'LEDGER_TOKEN', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR', 'TAIL_KEY'),
     'route-A attempt records: pins, paths, timestamps, the D2 tail-off record'),
    ('D17', G_A2, r'stages/route_a/checkpoint/IDENTITY\.json',
     ('CUSTODY_TOKEN', 'DRIVER_TOKEN', 'FILE_SHA', 'RUN_PATH'),
     'checkpoint identity: caller record paths / pins, code pins (digests verified)'),
    ('D18', G_A2, r'stages/route_a/checkpoint/iteration_[0-9]{4}/(COMPLETED|START|column_[0-9]{5})\.json', ('FILE_SHA', 'RECORD_DROP'),
     'checkpoint iteration records: identity / payload digests and the attempt token (RECORD_DROP)'),
)
LEDGER_CLASSES = ('MASKED_KEY', 'RECORD_DROP')
for _e in DECLARED_DIFFER:  # A76 N5 / A74: only JSON and JSONL records can be declared; every array file is compared by raw bytes
    assert re.sub(r'\\\.', '.', _e[2]).endswith(('.json', '.jsonl', '.json)', 'jsonl)')) and set(_e[3]) <= set(CLASSES), _e[0]  # checkpoint attempt ledger records (paired by order)
# H1: declared new-only files per gate (canonical relative paths), with their source (c2v006, unchanged).
DECLARED_NEW_ONLY = {
    'Z2': [
        (r'inputs/uv_tail_config\.json', 'driver L1091 ctx.write_input(uv_tail_config.json)'),
        (r'inputs/uv_tail_route_a_request\.json', 'driver L1092 ctx.write_input(uv_tail_route_a_request.json)'),
        (r'stages/route_a/uv_tail_sidecar/(SIDECAR_IDENTITY\.json|iteration_[0-9]{4}\.json|elements_[0-9]{4}\.npz|finish_[0-9]{3,4}\.json)',
         'driver L2845 --uv-tail-sidecar-directory; written by the driver AUX_UVT controller'),
        (r'stages/route_a_tail_manifest/(request\.json|stdout\.txt|stderr\.txt)', 'driver L2919-2941 (stage route_a_tail_manifest)'),
        (r'stages/route_a_tail_manifest/manifest/(ROUTE_A_TAIL_MANIFEST\.json|finish\.json|route_a_tail_state\.npz|route_a_gas_it_roster\.npz)',
         'driver AUX_UVT manifest_writer outputs'),
    ],
    'Z2_OFF_RO1': [(r'inputs/' + re.escape(OFF_REQUEST_NAME), 'driver L2847 ctx.write_input (D1)')],
    'Z2_OFF': [],
    'B0P_RERUN': [],
}
DECLARED_NEW_ONLY_DIRS = {'Z2': (r'stages/route_a_tail_manifest', r'stages/route_a_tail_manifest/manifest', r'stages/route_a/uv_tail_sidecar'),
                          'Z2_OFF_RO1': (), 'Z2_OFF': (), 'B0P_RERUN': ()}
DECLARED_EXTRA_STAGES = {'Z2': ('route_a_tail_manifest',), 'Z2_OFF_RO1': (), 'Z2_OFF': (), 'B0P_RERUN': ()}
TABLE_NAMES = ('SCRIPTS', 'AUX', 'PARALLEL_ROUTE_A', 'RO1_ROUTE_A', 'SCRIPTS_UVT', 'AUX_UVT', 'NODES_ROUTE_A', 'SCRIPTS_UVT_NODES')
PIN_DICTS = ('code_pins', 'input_pins', 'dependency_pins', 'source_pins', 'static_pins', 'pins', 'module_pins')
IMPL_KIND_PAIRS = {  # driver L2872-2878: route-A implementation kind (reference kind -> new kind) per gate
    'Z2': (('PARALLEL_C2V001', 'UVTAIL_RO1_PARALLEL_C2V001'), ('REVIEWED_SERIAL', 'UVTAIL_RO1_SERIAL_C2V001')),
    'Z2_OFF_RO1': (('PARALLEL_C2V001', 'TAIL_OFF_RO1_PARALLEL_C2V010R4'), ('REVIEWED_SERIAL', 'TAIL_OFF_RO1_SERIAL_C2V010R4')),
}
TOKEN_FILE_KEYS = frozenset({'declared', 'mode', 'driver', 'note', 'gate', 'reference_driver', 'derivation'})
VERDICT_WORDS = frozenset({'PASS', 'FAIL', 'CONVERGED', 'NOT_CONVERGED', 'COMPLETED', 'FAILED', 'REFUSED', 'RECORD_DEFECT', 'NO_RUN',
                           'PROVISIONAL', 'PASS_BITWISE_EQUAL', 'TRUE', 'FALSE', 'NONE', 'NULL', 'NAN', 'INF', 'INFINITY'})
LAST_WINS = []  # A71 guard hits (reset by main)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def file_ok(path, sha):
    """Hash-only custody of a code file outside the runs (its content is not used)."""
    return isinstance(path, str) and isinstance(sha, str) and Path(path).is_file() and sha_file(path) == sha


# ---------------------------------------------------------------- sentinels (never equal to anything)
class Unparseable(dict):
    def __init__(self, why):
        super().__init__()
        self.why = why

    def __repr__(self):
        return '<UNPARSEABLE %s>' % self.why[:120]
    __str__ = __repr__


class Collided:
    def __init__(self, raw_keys):
        self.raw_keys = raw_keys

    def __repr__(self):
        return '<COLLIDED %s>' % (self.raw_keys,)
    __str__ = __repr__


class Dup:
    def __init__(self, flag, values):
        self.flag, self.values = flag, values

    def __repr__(self):
        return '<DUPLICATE_ARGV %s %s>' % (self.flag, self.values)
    __str__ = __repr__


class NDV:
    """A decoded numpy array / scalar in normalized form: dtype and shape kept."""
    def __init__(self, dtype_str, shape, values):
        self.dtype_str, self.shape, self.values = dtype_str, shape, values

    def __repr__(self):
        return 'NDV(%s,%s,%s)' % (self.dtype_str, self.shape, str(self.values)[:80])
    __str__ = __repr__


# ---------------------------------------------------------------- strict CLI (A71; CK002 A04-A06)
CLI_VALUE = ('--gate', '--driver', '--reference', '--new', '--tokens', '--out')
CLI_BOOL = ('--require-ro1-armed',)


def parse_cli(argv):
    """Each flag exactly once, exact spelling (no abbreviation, no --flag=value, no positional argument): never last-wins."""
    argv = list(sys.argv[1:] if argv is None else argv)
    seen, out, i = {}, {}, 0  # A71[CLI]: a repeated flag refuses before the mapping is built
    while i < len(argv):
        f = argv[i]
        if not isinstance(f, str) or f not in CLI_VALUE + CLI_BOOL:
            raise SystemExit('REFUSED: CLI argument %r at position %d is not one of the exact flags %s (no abbreviation, no '
                             '--flag=value, no positional)' % (f, i, list(CLI_VALUE + CLI_BOOL)))
        if f in seen:
            raise SystemExit('REFUSED: CLI flag %s given twice (positions %d and %d; A71: never last-wins)' % (f, seen[f], i))
        seen[f] = i  # A71[CLI]
        if f in CLI_BOOL:
            out[f] = True  # A71[CLI]
            i += 1
            continue
        if i + 1 >= len(argv) or not isinstance(argv[i + 1], str) or argv[i + 1].startswith('--'):
            raise SystemExit('REFUSED: CLI flag %s has no value' % f)
        out[f] = argv[i + 1]  # A71[CLI]
        i += 2
    miss = [f for f in CLI_VALUE if f not in out]
    if miss:
        raise SystemExit('REFUSED: missing CLI flags %s' % miss)
    return types.SimpleNamespace(gate=out['--gate'], driver=out['--driver'], reference=out['--reference'], new=out['--new'],
                                 tokens=out['--tokens'], out=out['--out'], require_ro1_armed=bool(out.get('--require-ro1-armed')))


# ---------------------------------------------------------------- N3 containment (A73 N3)
def _fold(s):
    return unicodedata.normalize('NFC', s).casefold()


def _same_inode(a, b):
    try:
        x, y = os.stat(a), os.stat(b)
    except OSError:
        return False
    return (x.st_dev, x.st_ino) == (y.st_dev, y.st_ino)


def registered_parts(registered):
    """(realpath of the registered directory's PARENT, its name): the registered directory itself is never touched."""
    reg = os.path.abspath(registered)
    return os.path.realpath(os.path.dirname(reg)), os.path.basename(reg)


def _is_registered(p, reg_parent, reg_name):
    """p names the registered directory iff its last component equals the registered name under NFC + casefold (APFS is
    normalization- and case-insensitive) and its parent is the registered parent by (st_dev, st_ino): this catches the
    /System/Volumes/Data firmlink and every other alias of the parent, without stat-ing the registered directory."""
    parent, name = os.path.split(p)
    return _fold(name) == _fold(reg_name) and _same_inode(parent or os.sep, reg_parent)


def registered_identity(reg_parent, reg_name):
    """(st_dev, st_ino) of the registered directory from its parent's listing (DirEntry.inode() comes from readdir; the registered
    directory itself is not stat-ed or opened), or None when it is absent."""
    try:
        dev = os.stat(reg_parent).st_dev
        with os.scandir(reg_parent) as it:
            for e in it:
                if _fold(e.name) == _fold(reg_name):
                    return (dev, e.inode())
    except OSError:
        return None
    return None


def _same_as_registered(p, reg_id):
    if reg_id is None:
        return False
    try:
        x = os.lstat(p)
    except OSError:
        return False
    return (x.st_dev, x.st_ino) == reg_id


def _inside_lexical(p, reg):
    a, b = _fold(os.path.normcase(p)), _fold(os.path.normcase(reg))
    return a == b or a.startswith(b.rstrip('/') + '/')


def guarded_resolve(path, registered=C5H_REGISTERED, marker=C5H_MARKER):
    """Resolve `path` component by component; return (real path, None) or (None, refusal reason).  Before each partial path is
    looked up it is tested against the registered directory three ways: marker in the NFC-casefolded component, lexical NFC-casefold
    containment in realpath(parent)/name, and parent-inode + folded-name identity (firmlink and Unicode aliases).  Symlinks are
    followed with os.readlink (at most 40 hops; a marker in a target refuses)."""
    reg_parent, reg_name = registered_parts(registered)
    reg = os.path.join(reg_parent, reg_name)
    mk = _fold(marker)
    # never os.path.abspath: it collapses 'link/..' lexically, which is not what the OS resolves (A79.5); '..' is applied by the walk
    absp = os.fspath(path) if os.path.isabs(os.fspath(path)) else os.path.join(os.getcwd(), os.fspath(path))
    if any(mk in _fold(x) for x in Path(absp).parts):
        return None, 'MARKER in the given path (%s)' % marker
    reg_id = registered_identity(reg_parent, reg_name)
    if reg_id is None:  # root V005 A79.3: an unavailable registered identity is a refusal, never a silent drop
        return None, 'REGISTERED_IDENTITY_UNAVAILABLE (%s cannot be identified from its parent listing)' % reg
    queue = list(Path(absp).parts[1:])
    cur, hops = os.sep, 0
    while queue:
        name = queue.pop(0)
        if name in ('', '.'):
            continue
        if name == '..':
            cur = os.path.dirname(cur) or os.sep
            continue
        nxt = os.path.join(cur, name)
        if mk in _fold(name):
            return None, 'MARKER in a resolved component (%s)' % name
        if _inside_lexical(nxt, reg) or _is_registered(nxt, reg_parent, reg_name):
            return None, 'REGISTERED directory reached (%s is %s by containment, firmlink or Unicode alias)' % (nxt, reg)
        if _same_as_registered(nxt, reg_id):
            return None, 'REGISTERED directory reached (%s has the registered (st_dev, st_ino): an inode alias such as /.vol)' % nxt
        if os.path.islink(nxt):
            hops += 1
            if hops > 40:
                return None, 'SYMLINK_LOOP'
            t = os.readlink(nxt)
            if mk in _fold(t):
                return None, 'MARKER in a symlink target (%s -> %s)' % (nxt, t)
            parts = list(Path(t).parts)
            if os.path.isabs(t):
                cur, parts = os.sep, parts[1:]
            queue = parts + queue
            continue
        cur = nxt
    if _inside_lexical(cur, reg) or _is_registered(cur, reg_parent, reg_name) or _same_as_registered(cur, reg_id):
        return None, 'REGISTERED directory reached (%s)' % cur
    return cur, None


# ---------------------------------------------------------------- strict JSON (A71)
class DuplicateKey(ValueError):
    pass


def _pairs(pairs):
    d = {}
    for k, v in pairs:  # A71[JSON]: object_pairs_hook; a duplicate member refuses even when the values are equal
        if k in d:
            raise DuplicateKey('DUPLICATE_JSON_KEY %r: first %s, second %s' % (k, _show(d[k]), _show(v)))
        d[k] = v
    return d


def jloads(b):
    return json.loads(b.decode('utf-8') if isinstance(b, (bytes, bytearray)) else b, object_pairs_hook=_pairs)


# ---------------------------------------------------------------- arrays: strict header AST (Codex2 0445 item 1)
def npy_header_dict(text):
    """The .npy header text as a dict, parsed with ast.parse: the body must be one dict display whose keys are string literals with no
    duplicate (refused naming both entries, even when the values are equal) and whose values are literals.  Values are evaluated one
    by one only after the key checks, so no last-wins evaluation ever happens (A71)."""
    try:
        node = ast.parse(text, mode='eval').body
    except SyntaxError as e:
        raise ValueError('NPY_HEADER_NOT_A_LITERAL %s' % e)
    if not isinstance(node, ast.Dict):
        raise ValueError('NPY_HEADER_NOT_A_DICT %s' % type(node).__name__)
    seen = {}
    for k, v in zip(node.keys, node.values):  # A71[NPY_HEADER]: duplicate header keys refuse before any value is evaluated
        if k is None or not isinstance(k, ast.Constant) or not isinstance(k.value, str):
            raise ValueError('NPY_HEADER_KEY_NOT_A_STRING_LITERAL')
        if k.value in seen:
            raise DuplicateKey('DUPLICATE_NPY_HEADER_KEY %r: first %s, second %s' % (k.value, ast.unparse(seen[k.value])[:80],
                                                                                    ast.unparse(v)[:80]))
        seen[k.value] = v  # A71[NPY_HEADER]
    if sorted(seen) != ['descr', 'fortran_order', 'shape']:
        raise ValueError('NPY_HEADER_KEYS %r' % sorted(seen))
    out = {}
    for k in ('descr', 'fortran_order', 'shape'):
        try:
            out[k] = ast.literal_eval(seen[k])  # A71[FIXED_KEYS]
        except (ValueError, SyntaxError, TypeError) as e:
            raise ValueError('NPY_HEADER_VALUE_NOT_A_LITERAL %s %s' % (k, e))
    if type(out['fortran_order']) is not bool or not isinstance(out['shape'], tuple) or \
            not all(type(x) is int and x >= 0 for x in out['shape']) or not isinstance(out['descr'], (str, list)):
        raise ValueError('NPY_HEADER_VALUE_TYPES')
    return out


def _npy_header(b):
    if b[:6] != b'\x93NUMPY' or len(b) < 10:
        raise ValueError('NPY_MAGIC')
    major, minor = b[6], b[7]
    if (major, minor) == (1, 0):
        hl, off, enc = struct.unpack('<H', b[8:10])[0], 10, 'latin1'
    elif (major, minor) in ((2, 0), (3, 0)):
        if len(b) < 12:
            raise ValueError('NPY_HEADER_TRUNCATED')
        hl, off, enc = struct.unpack('<I', b[8:12])[0], 12, ('latin1' if major == 2 else 'utf8')
    else:
        raise ValueError('NPY_VERSION %s.%s' % (major, minor))
    hdr = b[off:off + hl]
    if len(hdr) != hl:
        raise ValueError('NPY_HEADER_TRUNCATED')
    return npy_header_dict(hdr.decode(enc))


def npy_identity_bytes(b):
    """Strictly parsed identity of one .npy payload (the c2v006 tuple)."""
    import numpy as np
    d = _npy_header(b)
    fp = io.BytesIO(b)
    a = np.lib.format.read_array(fp, allow_pickle=False)
    rest = b[fp.tell():]
    dt = a.dtype
    if list(a.shape) != list(d['shape']):
        raise ValueError('NPY_HEADER_ARRAY_MISMATCH')
    fields = None
    if dt.names is not None:
        fields = [[n, int(dt.fields[n][1]), dt.fields[n][0].str, list(dt.fields[n][0].shape)] for n in dt.names]
    return {'descr': repr(d['descr']), 'dtype_str': dt.str, 'itemsize': int(dt.itemsize), 'fields': fields,
            'shape': [int(x) for x in d['shape']], 'fortran_order': bool(d['fortran_order']),
            'values_sha256': sha_b(np.ascontiguousarray(a).tobytes()), 'trailing_sha256': sha_b(rest) if rest else None}


def npz_identity_bytes(b):
    """{logical key: identity} of an .npz payload; raises ValueError naming every defect (duplicate / non-.npy members, data before
    the first member, an NPY header defect)."""
    z = zipfile.ZipFile(io.BytesIO(b))
    infos = z.infolist()
    seen, keys, out, probs = {}, {}, {}, []
    if infos and min(i.header_offset for i in infos) != 0:
        probs.append('NPZ_DATA_BEFORE_FIRST_MEMBER (first local header at %d)' % min(i.header_offset for i in infos))
    if z.comment:
        probs.append('NPZ_ARCHIVE_COMMENT (%d bytes; A76 N5: container bytes are not ignored)' % len(z.comment))
    for i, info in enumerate(infos):  # A71[NPZ]: member names and logical keys refuse duplicates; reads by ZipInfo only
        n = info.filename
        if n in seen:
            probs.append('DUPLICATE_NPZ_MEMBER %r (central-directory entries %d and %d)' % (n, seen[n], i))
            continue
        seen[n] = i  # A71[NPZ]
        if not n.endswith('.npy') or n.endswith('/'):
            probs.append('NPZ_MEMBER_NOT_NPY %r (entry %d)' % (n, i))
            continue
        k = n[:-4]
        if k in keys:
            probs.append('DUPLICATE_NPZ_LOGICAL_KEY %r (members %r and %r)' % (k, keys[k], n))
            continue
        keys[k] = n  # A71[NPZ]
        try:
            out[k] = npy_identity_bytes(z.read(info))  # A71[NPZ]
        except ValueError as e:
            probs.append('NPZ_MEMBER %r: %s' % (n, e))
    if probs:
        raise ValueError('; '.join(probs))
    return out


# ---------------------------------------------------------------- one-read file store with a declared parse surface
class Store:
    """Every run file is hashed once (stream; with byte scans for the needles), and a declared file is read once more into memory for
    parsing: the sha of the parsed bytes must equal the first sha (TREE_STABLE).  Only regular files of the tree are ever opened;
    only declared files are ever parsed (PARSE_SURFACE).  verify() re-hashes everything recorded at the end."""

    def __init__(self, root, tag, tree=None):
        self.root, self.tag = Path(root), tag
        self.regular = None if tree is None else {str(self.root / r) for r in tree.files}  # A71[INVENTORY]: tree.files are unique raw paths
        self.allow = None  # None: every regular file may be parsed (unit use); a set: the declared parse surface
        self.sha, self.unstable, self.problems, self.surface = {}, [], [], []
        self._json, self._arr, self._raw = {}, {}, {}
        self.hits = {}

    def rel(self, p):
        try:
            return str(Path(p).relative_to(self.root))
        except ValueError:
            return str(p)

    def has(self, p):
        return Path(p).is_file() if self.regular is None else str(p) in self.regular

    def _record(self, p, h):
        k = str(p)
        if k in self.sha and self.sha[k] != h:
            self.unstable.append({'side': self.tag, 'file': k, 'first_sha256': self.sha[k], 'later_sha256': h})
        self.sha.setdefault(k, h)

    def _gate(self, p, why):
        if not self.has(p):
            self.surface.append({'side': self.tag, 'file': self.rel(p), 'why': why})
            return False
        return True

    def read(self, p):
        if not self._gate(p, 'READ_OF_A_PATH_THAT_IS_NOT_A_REGULAR_FILE_OF_THE_TREE'):
            return None
        with open(p, 'rb') as f:
            b = f.read()
        self._record(p, sha_b(b))
        return b

    def hash_scan(self, p, needles=()):
        """Stream sha256 with byte scans (stray uv_tail; cross-run root); recorded as the file's first sha."""
        if not self._gate(p, 'HASH_OF_A_PATH_THAT_IS_NOT_A_REGULAR_FILE_OF_THE_TREE'):
            return None, set()
        h, hit, tail = hashlib.sha256(), set(), b''
        keep = max([len(x) for x in needles] + [1]) - 1
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 22), b''):
                h.update(b)
                w = tail + b
                for nd in needles:
                    if nd not in hit and nd in w:
                        hit.add(nd)
                tail = w[-keep:] if keep else b''
        d = h.hexdigest()
        self._record(p, d)
        if hit:
            self.hits[str(p)] = hit
        return d, hit

    def sha_of(self, p):
        k = str(p)
        if k in self.sha:
            return self.sha[k]
        return self.hash_scan(p)[0]

    def parse_ok(self, p):
        if self.allow is not None and str(p) not in self.allow:
            self.surface.append({'side': self.tag, 'file': self.rel(p), 'why': 'PARSE_OF_AN_UNDECLARED_FILE'})
            return False
        return True

    def raw(self, p):
        k = str(p)
        return self._raw[k] if k in self._raw else self.read(p)

    def json(self, p):
        k = str(p)
        if k not in self._json:
            if not self.parse_ok(p):
                self._json[k] = Unparseable('PARSE_SURFACE %s' % self.rel(p))
                return self._json[k]
            b = self.read(p)
            if b is None:
                self._json[k] = Unparseable('NOT_A_REGULAR_FILE %s' % self.rel(p))
                return self._json[k]
            if '/checkpoint/' in k:  # small checkpoint records: raw bytes kept for cm_read (same single read)
                self._raw[k] = b
            try:
                self._json[k] = jloads(b)
            except (ValueError, UnicodeDecodeError) as e:
                self.problems.append({'side': self.tag, 'file': self.rel(p), 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
                self._json[k] = Unparseable('%s %s' % (self.rel(p), e))
        return self._json[k]

    def jsonl(self, p):
        out = []
        if not self.parse_ok(p):
            return [Unparseable('PARSE_SURFACE %s' % self.rel(p))]
        b = self.read(p)
        if b is None:
            return [Unparseable('NOT_A_REGULAR_FILE %s' % self.rel(p))]
        for i, line in enumerate(b.split(b'\n')):
            if not line.strip():
                continue
            try:
                out.append(jloads(line))
            except (ValueError, UnicodeDecodeError) as e:
                self.problems.append({'side': self.tag, 'file': self.rel(p), 'line': i + 1, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
                out.append(Unparseable('%s:%d %s' % (self.rel(p), i + 1, e)))
        return out

    def array(self, p):
        """('npz', {key: identity}) / ('npy', identity); ('invalid', why) on a parse problem (recorded)."""
        k = str(p)
        if k not in self._arr:
            if not self.parse_ok(p):
                self._arr[k] = ('invalid', 'PARSE_SURFACE')
                return self._arr[k]
            b = self.read(p)
            try:
                if b is None:
                    raise ValueError('NOT_A_REGULAR_FILE')
                self._arr[k] = ('npz', npz_identity_bytes(b)) if k.endswith('.npz') else ('npy', npy_identity_bytes(b))
            except Exception as e:  # zipfile.BadZipFile, ValueError, OSError from numpy parsing
                self.problems.append({'side': self.tag, 'file': self.rel(p), 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
                self._arr[k] = ('invalid', '%s %s' % (type(e).__name__, str(e)[:200]))
        return self._arr[k]

    def verify(self):
        bad = []
        for k, h in sorted(self.sha.items()):
            try:
                now = sha_file(k)
            except OSError as e:
                now = 'UNREADABLE %s' % type(e).__name__
            if now != h:
                bad.append({'side': self.tag, 'file': k, 'read_sha256': h, 'end_sha256': now})
        return bad


def cm_read(cm, store, path, kind):
    """The checkpoint module's _read (c2v003 L208-220) applied to the store's single read of the file."""
    raw = store.raw(path)
    if raw is None:
        raise cm.CheckpointError('NOT_A_REGULAR_FILE ' + str(path))
    try:
        body = json.loads(raw.decode('ascii'), object_pairs_hook=_pairs)
    except (UnicodeDecodeError, ValueError) as e:
        raise cm.CheckpointError('UNREADABLE_RECORD %s %s' % (type(e).__name__, path)) from None
    if type(body) is not dict or body.get('format') != cm.FORMAT or body.get('kind') != kind:
        raise cm.CheckpointError('WRONG_RECORD_KIND ' + str(path))
    claimed = body.pop('payload_sha256', None)
    if claimed != cm._sha(cm._canonical(body)):
        raise cm.CheckpointError('RECORD_INTEGRITY_FAILURE ' + str(path))
    body['payload_sha256'] = claimed
    if raw != cm._canonical(body) + b'\n':
        raise cm.CheckpointError('NONCANONICAL_RECORD ' + str(path))
    return body


def load_cm():
    """Hash and execute the checkpoint module from one read of its bytes."""
    raw = Path(CKPT[0]).read_bytes()
    if sha_b(raw) != CKPT[1]:
        raise SystemExit('checkpoint module pin')
    m = types.ModuleType('ckpt_cmp_c2v007')
    m.__file__ = CKPT[0]
    exec(compile(raw, CKPT[0], 'exec'), m.__dict__)
    return m


def driver_raw():
    """The selected driver's bytes, read once per selection and verified against the pin."""
    if DRIVER_RAW[0] is None or DRIVER_RAW[1] != DRIVER[0]:
        DRIVER_RAW[0], DRIVER_RAW[1] = Path(DRIVER[0]).read_bytes(), DRIVER[0]
    if sha_b(DRIVER_RAW[0]) != DRIVER[1]:
        raise SystemExit('driver pin')
    return DRIVER_RAW[0]


def load_driver():
    """The selected pinned driver, executed from the verified bytes (module body: constants and defs only)."""
    raw = driver_raw()
    m = types.ModuleType('v010_cmp_c2v007')
    m.__file__ = DRIVER[0]
    exec(compile(raw, DRIVER[0], 'exec'), m.__dict__)
    return m


# ---------------------------------------------------------------- restricted AST evaluation of a driver's tables (c2v004)
class _Unsafe(Exception):
    pass


def _ev(node, env):
    if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float, bool, type(None))):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise _Unsafe(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        a, b = _ev(node.left, env), _ev(node.right, env)
        if isinstance(a, Path) and isinstance(b, (str, Path)):
            return a / b
        raise _Unsafe('div')
    if isinstance(node, ast.Tuple):
        return tuple(_ev(x, env) for x in node.elts)
    if isinstance(node, ast.List):
        return [_ev(x, env) for x in node.elts]
    if isinstance(node, ast.Dict):
        if any(k is None for k in node.keys):
            raise _Unsafe('dict splat')
        out = {}
        for k, v in zip(node.keys, node.values):
            kk = _ev(k, env)
            if kk in out:  # A71[DRIVER_AST]: a duplicate key in a driver dict literal is never resolved last-wins here
                LAST_WINS.append({'where': 'driver table dict literal', 'line': k.lineno, 'key': str(kk)})
                raise _Unsafe('duplicate dict key %r' % (kk,))
            out[kk] = _ev(v, env)
        return out
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Path' and not node.keywords \
            and len(node.args) == 1:
        v = _ev(node.args[0], env)
        if isinstance(v, str):
            return Path(v)
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in env:
        k = _ev(node.slice, env)
        return env[node.value.id][k]
    raise _Unsafe(type(node).__name__)


def driver_env(raw, path=None):
    """Module-level constants of a driver from its (already verified) bytes, by restricted AST evaluation (no code executed)."""
    if path is None and isinstance(raw, (str, Path)) and not isinstance(raw, bytes) and Path(raw).is_file():
        path, raw = str(raw), Path(raw).read_bytes()
    tree = ast.parse(raw.decode('utf-8') if isinstance(raw, bytes) else raw, filename=str(path or '<driver>'))
    env = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            try:
                env[st.targets[0].id] = _ev(st.value, env)  # A71[DRIVER_ENV]: module rebinding is Python's own order (driver semantics)
            except (_Unsafe, KeyError, TypeError):
                continue
    return env


def driver_tables(raw, path=None):
    """The (path, sha) tables TABLE_NAMES of a driver (c2v006 interface)."""
    env = driver_env(raw, path)
    out = {}
    for t in TABLE_NAMES:
        v = env.get(t)
        if isinstance(v, dict):
            out[t] = {k: (str(x[0]), x[1]) for k, x in v.items() if isinstance(x, tuple) and len(x) == 2 and isinstance(x[1], str)}  # A71[DRIVER_AST]
    return out


def driver_pin_entries(env):
    """SF3: every (path, sha) tuple anywhere in the driver's module-level constants (dicts, lists and tuples, recursively)."""
    out = set()

    def walk(v, depth=0):
        if depth > 6:
            return
        if isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], (str, Path)) and isinstance(v[1], str) and SHA_RE.fullmatch(v[1]):
            out.add((str(v[0]), v[1]))
            return
        if isinstance(v, dict):
            for x in v.values():
                walk(x, depth + 1)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x, depth + 1)
    for v in env.values():
        walk(v)
    return out


# ---------------------------------------------------------------- strict JSON equality (H5)
def seq(a, b):
    if isinstance(a, (Unparseable, Collided, Dup)) or isinstance(b, (Unparseable, Collided, Dup)):
        return False
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        return struct.pack('<d', a) == struct.pack('<d', b)
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(seq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(seq(x, y) for x, y in zip(a, b))
    if isinstance(a, NDV):
        return a.dtype_str == b.dtype_str and a.shape == b.shape and seq(a.values, b.values)
    return a == b


def _show(v):
    return '%s:%s' % (type(v).__name__, (v.hex() if isinstance(v, float) else str(v))[:160])


def diffs(a, b, path='', out=None, limit=12):
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if isinstance(a, dict) and isinstance(b, dict) and not isinstance(a, Unparseable) and not isinstance(b, Unparseable):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append((path + '/' + str(k), 'ONLY_' + ('NEW' if k in b else 'REF')))
            else:
                diffs(a[k], b[k], path + '/' + str(k), out, limit)
    elif isinstance(a, (list, tuple)) and type(a) is type(b) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            diffs(x, y, '%s[%d]' % (path, i), out, limit)
    elif not seq(a, b):
        out.append((path, _show(a), _show(b)))
    return out


def argv_map(argv, where=''):
    """A71: flag -> value; a flag given more than once reads as a Dup sentinel when it is read (and is recorded)."""
    return StrictArgv(argv, where)


class StrictArgv:
    def __init__(self, argv, where):
        self.where, self.m = where, {}
        for k, v in zip(argv[::2], argv[1::2]):  # A71[ARGV]: multimap; a repeated flag reads as Dup (never last-wins)
            self.m.setdefault(k, []).append(v)

    def get(self, k, default=None):
        v = self.m.get(k)
        if v is None:
            return default
        if len(v) > 1:
            LAST_WINS.append({'where': 'argv %s' % self.where, 'flag': k, 'values': [str(x)[:120] for x in v]})
            return Dup(k, v)
        return v[0]

    def __contains__(self, k):
        return k in self.m

    def __getitem__(self, k):
        v = self.get(k)
        if v is None:
            raise KeyError(k)
        return v


# ---------------------------------------------------------------- the run tree by real path (lstat; never follows a link)
class Tree:
    """Every regular file, directory, symlink and special file of a run by its real relative path, and the stage directory table."""

    def __init__(self, run):
        self.run = Path(run)
        self.files, self.links, self.dirs, self.special = [], [], [], []
        for dp, dns, fns in os.walk(self.run, followlinks=False):
            for n in list(dns):
                p = os.path.join(dp, n)
                r = os.path.relpath(p, self.run)
                m = os.lstat(p).st_mode
                if stat.S_ISLNK(m):
                    self.links.append(r)
                    dns.remove(n)
                elif stat.S_ISDIR(m):
                    self.dirs.append(r)
                else:
                    self.special.append((r, stat.S_IFMT(m)))
                    dns.remove(n)
            for n in fns:
                p = os.path.join(dp, n)
                r = os.path.relpath(p, self.run)
                m = os.lstat(p).st_mode
                if stat.S_ISLNK(m):
                    self.links.append(r)
                elif stat.S_ISREG(m):
                    self.files.append(r)
                else:
                    self.special.append((r, stat.S_IFMT(m)))  # FIFO / socket / device: never opened (CK002 E06)
        self.files.sort()
        self.links.sort()
        self.dirs.sort()
        self.special.sort()
        self.problems, self.order, self.dir2name, self.name2dir, self.stages = [], [], {}, {}, {}
        sd = self.run / 'stages'
        if os.path.lexists(sd) and stat.S_ISLNK(os.lstat(sd).st_mode):
            self.problems.append(('stages', 'SYMLINK'))
        elif sd.is_dir():
            names, nums, ok = {}, {}, []
            for e in sorted(os.listdir(sd)):
                p = sd / e
                m = STAGE_RE.fullmatch(e)
                mode = os.lstat(p).st_mode
                if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode) or not m:
                    self.problems.append(('stages/' + e, 'NOT_A_NN_NAME_STAGE_DIRECTORY'))
                    continue
                names.setdefault(m.group(2), []).append(e)  # A71[STAGE_DIRS]: grouped; duplicates excluded below, never last-wins
                nums.setdefault(m.group(1), []).append(e)
                ok.append((m.group(1), m.group(2), e))
            dup_names = {n for n, l in names.items() if len(l) > 1}
            dup_nums = {n for n, l in nums.items() if len(l) > 1}  # A71[STAGE_DIRS]
            for n in sorted(dup_names):
                self.problems.append((['stages/' + x for x in names[n]], 'DUPLICATE_STAGE_NAME'))
            for n in sorted(dup_nums):
                self.problems.append((['stages/' + x for x in nums[n]], 'DUPLICATE_STAGE_NUMBER'))
            for num, name, e in sorted(ok):
                if name in dup_names or num in dup_nums:
                    continue
                self.order.append(name)
                self.dir2name[e] = name  # A71[STAGE_DIRS]
                self.name2dir[name] = e  # A71[STAGE_DIRS]
                self.stages[name] = sd / e  # A71[STAGE_DIRS]
        self.inv, self.inv_collisions, self.dinv = {}, [], {}
        for r in self.files:  # A71[INVENTORY]: the canonical inventory never keeps one of two colliding raw paths
            c = self.canon(r)
            if c in self.inv:
                self.inv_collisions.append({'canonical': c, 'raw_paths': [str(self.inv[c].relative_to(self.run)), r]})
                LAST_WINS.append({'where': 'inventory canonical path', 'canonical': c, 'raw_paths': [str(self.inv[c].relative_to(self.run)), r]})
                continue
            self.inv[c] = self.run / r  # A71[INVENTORY]
        for r in self.dirs:  # A71[DIR_INVENTORY]
            c = self.canon(r)
            if c in self.dinv:
                self.inv_collisions.append({'canonical_dir': c, 'raw_paths': [self.dinv[c], r]})
                LAST_WINS.append({'where': 'directory inventory canonical path', 'canonical': c, 'raw_paths': [self.dinv[c], r]})
                continue
            self.dinv[c] = r  # A71[DIR_INVENTORY]

    def canon(self, rel):
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0] == 'stages' and parts[1] in self.dir2name:
            return '/'.join(['stages', self.dir2name[parts[1]]] + parts[2:])
        return rel

    def inventory(self):
        return dict(self.inv)

    def subdirs(self, stage_dir):
        """Names of the directories directly under an absolute stage directory (from the walk, no lookup)."""
        base = os.path.relpath(stage_dir, self.run)
        return sorted(r.split('/')[-1] for r in self.dirs if os.path.dirname(r) == base)

    def has_under(self, rel_dir):
        pre = rel_dir.rstrip('/') + '/'
        return any(r == rel_dir or r.startswith(pre) for r in self.files + self.dirs + self.links + [x for x, _ in self.special])


# ---------------------------------------------------------------- declared list helpers
def declared_entries(gate):
    return [(i, re.compile(rx), tuple(cl), why) for i, gs, rx, cl, why in DECLARED_DIFFER if gate in gs]


def declared_entry(entries, rel):
    hit = [(i, cl) for i, rx, cl, _ in entries if rx.fullmatch(rel)]
    if len(hit) > 1:  # A71[DECLARED_LIST]: a path matched by two entries is a defect of the list itself, never first-wins
        LAST_WINS.append({'where': 'declared list', 'path': rel, 'entries': [h[0] for h in hit]})
        return ('AMBIGUOUS', ())
    return hit[0] if hit else None


# ---------------------------------------------------------------- the injective normalizer
_DEC_LABEL = re.compile(r'<([A-Z0-9_]+)>')
_DEC_STAGE = re.compile(r'<STAGE:([a-z0-9_]+)>')


def sha_token(names):
    """'<SHA:' + length-prefixed sorted names + '>': injective in the name set (no joined text)."""
    return '<SHA:' + ''.join('%d:%s' % (len(n), n) for n in sorted(names)) + '>'


class Side:
    """One side's normalizer.  tokens: (raw, label) or (raw, label, class) items; markers: raw-text markers to flag."""

    def __init__(self, tree, store, tokens, markers, extra_names=None):
        self.run = Path(tree.run)
        self.tree = tree
        self.store = store
        self.markers = tuple(markers)
        self.collisions = []
        self.fired = {}
        self.fired_tok = {}
        self.cur = None
        self.n_strings = 0
        self.n_roundtrip = 0
        self.roundtrip_bad = []
        toks = []
        for t in tokens:
            raw, lab = t[0], t[1]
            toks.append((raw, lab, t[2] if len(t) > 2 else 'DRIVER_TOKEN'))
        self.tok = {r: (l, c) for r, l, c in toks}  # A71[SIDE_TOKENS]: one label per raw, enforced by build_tokens upstream
        self.label_inv = {l: r for r, l, c in toks}
        if len(self.tok) != len(toks) or len(self.label_inv) != len(toks):
            self.collisions.append({'kind': 'TOKEN_MAP_NOT_BIJECTIVE', 'n': len(toks), 'raws': len(self.tok), 'labels': len(self.label_inv)})
        self.dir2name, self.name2dir = dict(tree.dir2name), dict(tree.name2dir)
        names = {}
        for rel in tree.files:  # every file of this side: sha -> the canonical paths with that content
            h = store.sha_of(self.run / rel)
            if h:
                names.setdefault(h, set()).add('F:' + tree.canon(rel))  # A71[HEXMAP]: grouped into a set, never last-wins
        for h, extra in (extra_names or {}).items():
            names.setdefault(h, set()).update(extra)
        self.hexmap = {h: sha_token(v) for h, v in names.items()}
        self.hexkind = {h: ('RA_SHA' if any(x == 'I' or x.startswith('P:') for x in v) else 'FILE_SHA') for h, v in names.items()}
        self.hexinv = {}
        for h, t in sorted(self.hexmap.items()):  # A71[HEXINV]: many-to-one refuses (only the RA identity name can repeat)
            if t in self.hexinv:
                self.collisions.append({'kind': 'HEXMAP_MANY_TO_ONE', 'token': t[:200], 'distinct_sha256': [self.hexinv[t], h]})
                continue
            self.hexinv[t] = h  # A71[HEXINV]
        alts = []
        if self.tok:
            alts.append('(?P<tok>' + '|'.join(re.escape(r) for r in sorted(self.tok, key=lambda x: (-len(x), x))) + ')')
        else:
            alts.append('(?P<tok>(?!))')  # no token: the group exists and never matches
        alts.append('(?<![A-Za-z0-9_./-])(?P<run>' + re.escape(str(self.run)) + r')(?:(?P<st>/stages/)(?P<dir>[0-9]{2}_[a-z0-9_]+)(?![a-z0-9_]))?'
                    r'(?![A-Za-z0-9_-])')
        alts.append('(?P<hex>[0-9a-f]{64})')
        self.rx = re.compile('|'.join(alts))

    @contextlib.contextmanager
    def at_file(self, rel):
        old, self.cur = self.cur, rel
        try:
            yield
        finally:
            self.cur = old

    def _fire(self, cls, tok=None):
        if self.cur is not None:
            self.fired.setdefault(self.cur, set()).add(cls)
        if tok is not None:
            self.fired_tok[tok] = self.fired_tok.get(tok, 0) + 1

    def s(self, v, at=''):
        if '<' in v:
            hit = [m for m in self.markers if m in v]
            if hit:
                self.collisions.append({'kind': 'RAW_TEXT_CONTAINS_NORMALIZER_TOKEN', 'at': at, 'file': self.cur, 'markers': hit[:6], 'raw': v[:200]})
        out, pos = [], 0
        for m in self.rx.finditer(v):
            out.append(v[pos:m.start()].replace('<', '<~'))
            if m.group('tok') is not None:
                lab, cls = self.tok[m.group('tok')]
                out.append(lab)
                self._fire(cls, lab)
            elif m.group('run') is not None:
                d = m.group('dir')
                if d is not None and d in self.dir2name:
                    out.append('<RUN>/stages/<STAGE:%s>' % self.dir2name[d])
                    self._fire('RUN_PATH')
                    self._fire('STAGE_DIR')
                else:
                    out.append('<RUN>' + ((m.group('st') + d) if d is not None else ''))
                    self._fire('RUN_PATH')
            else:
                h = m.group('hex')
                t = self.hexmap.get(h)
                if t is None:
                    out.append(h)
                else:
                    out.append(t)
                    self._fire(self.hexkind[h])
            pos = m.end()
        out.append(v[pos:].replace('<', '<~'))
        n = ''.join(out)
        self.n_strings += 1
        try:
            back = self.decode(n)
        except (ValueError, KeyError, IndexError) as e:
            back = '<UNDECODABLE %s>' % e
        if back == v:
            self.n_roundtrip += 1
        elif len(self.roundtrip_bad) < 12:
            self.roundtrip_bad.append({'at': at, 'file': self.cur, 'raw': v[:200], 'normalized': n[:200], 'decoded': back[:200]})
        return n

    def decode(self, n):
        """Inverse of s(): every '<' starts '<~' (escaped raw), '<RUN>', '<STAGE:name>', '<SHA:...>' or a label."""
        out, i = [], 0
        while True:
            j = n.find('<', i)
            if j < 0:
                out.append(n[i:])
                return ''.join(out)
            out.append(n[i:j])
            if n.startswith('<~', j):
                out.append('<')
                i = j + 2
            elif n.startswith('<RUN>', j):
                out.append(str(self.run))
                i = j + 5
            elif n.startswith('<STAGE:', j):
                m = _DEC_STAGE.match(n, j)
                out.append(self.name2dir[m.group(1)])
                i = m.end()
            elif n.startswith('<SHA:', j):
                k = j + 5
                while n[k] != '>':
                    c = n.index(':', k)
                    k = c + 1 + int(n[k:c])
                tok = n[j:k + 1]
                out.append(self.hexinv[tok])
                i = k + 1
            else:
                m = _DEC_LABEL.match(n, j)
                if m is None:
                    raise ValueError('UNDECODABLE_AT_%d' % j)
                out.append(self.label_inv[m.group(0)])
                i = m.end()

    def norm(self, o, drop=(), at='', rec=None):
        if isinstance(o, (Unparseable, Collided, Dup)):
            return o
        if hasattr(o, 'tolist') and hasattr(o, 'dtype') and not isinstance(o, (str, bytes)):
            shp = list(o.shape) if getattr(o, 'ndim', 0) or type(o).__name__ == 'ndarray' else None
            return NDV(o.dtype.str, shp, self.norm(o.tolist(), drop, at, rec))
        if isinstance(o, tuple):
            return tuple(self.norm(x, drop, '%s[%d]' % (at, i), rec) for i, x in enumerate(o))
        if isinstance(o, dict):
            out, src = {}, {}
            for k, x in o.items():
                if k in MASK_KEYS or k in drop:
                    if k in TAIL_KEYS:
                        self._fire('TAIL_KEY')
                    else:
                        self._fire('RECORD_DROP' if (k not in MASK_KEYS and k in RECORD_DROP) else 'MASKED_KEY')
                        if rec is not None:
                            rec.append(at + '/' + str(k))
                    continue
                nk = self.s(k, at + '/<key>') if isinstance(k, str) else k
                if nk in out:  # A71[NORM_KEYS]: two raw keys to one normalized key FAIL naming both (impossible: s() is injective)
                    self.collisions.append({'kind': 'KEY_COLLISION', 'at': at, 'normalized_key': str(nk)[:200],
                                            'raw_keys': [str(src[nk])[:200], str(k)[:200]]})
                    out[nk] = Collided([src[nk], k])
                    continue
                src[nk] = k
                out[nk] = self.norm(x, drop, at + '/' + str(nk), rec)
            return out
        if isinstance(o, list):
            return [self.norm(x, drop, '%s[%d]' % (at, i), rec) for i, x in enumerate(o)]
        if isinstance(o, str):
            return self.s(o, at)
        return o


# ---------------------------------------------------------------- tokens: A59 derivation, grammar, protected forms (A73 SF2, A74)
def _forms(a, b):
    """(form, ref raw, new raw) for one table entry pair: path, sha and basename, each only when it differs."""
    if a is None or b is None:
        return []
    (ap, as_), (bp, bs) = (str(a[0]), a[1]), (str(b[0]), b[1])
    out = []
    if ap != bp:
        out.append(('PATH', ap, bp))
    if as_ != bs:
        out.append(('SHA', as_, bs))
    if Path(ap).name != Path(bp).name:
        out.append(('NAME', Path(ap).name, Path(bp).name))
    return out


def _lab(*parts):
    return '<' + '_'.join(re.sub(r'[^A-Z0-9]+', '_', str(p).upper()).strip('_') for p in parts) + '>'


def derive_tokens(gate, ref_env, sel_env, check_bytes=True):
    """The A59 driver derivation: (triples, groups, problems).  ref_env / sel_env are driver_env() of the reference run's driver and the
    selected driver.  Groups keep, per table entry, the two (path, sha) pins so that every sha form is the bytes-sha of its path form."""
    trip, groups, probs = [], [], []
    rs, ns = ref_env.get('SCRIPTS') or {}, sel_env.get('SCRIPTS') or {}
    uvt = tuple(sel_env.get('UVT_TAIL_KINDS') or ())
    su = sel_env.get('SCRIPTS_UVT') or {}
    for k in sorted(set(rs) & set(ns)):
        if k == 'route_a':
            continue  # route A custody is AUTO_CUSTODY / RO1_CUSTODY, never a declared token
        nb = su.get(k) if (gate == 'Z2' and k in uvt) else ns[k]
        if gate == 'Z2' and k in uvt:
            base = ns[k]
            if nb is None:
                probs.append('A59: no SCRIPTS_UVT successor for %s' % k)
                continue
            if check_bytes:
                try:
                    ub = Path(str(nb[0])).read_bytes()
                except OSError:
                    ub = b''
                need = ('successor of %s (sha256 %s)' % (Path(str(base[0])).name, base[1])).encode()
                if sha_b(ub) != nb[1] or need not in ub:
                    probs.append('A59 rule L1193-1194: successor %s does not hash to its pin or does not name its base %s' % (nb[0], base[0]))
        groups.append(('SCRIPT', k, rs[k], nb))
        trip += [[r, n, _lab('DRV', 'SCRIPT', k, f)] for f, r, n in _forms(rs[k], nb)]
    rg, ng = ref_env.get('GALAXY_CONFIG_FILES') or {}, sel_env.get('GALAXY_CONFIG_FILES') or {}
    for k in sorted(set(rg) | set(ng), key=str):
        key = '_'.join(k) if isinstance(k, tuple) else str(k)
        a, b = rg.get(k), ng.get(k)
        if a is not None and b is not None:
            groups.append(('GCFILE', key, a, b))
        trip += [[r, n, _lab('DRV', 'GCFILE', key, f)] for f, r, n in _forms(a, b)]
    a, b = ref_env.get('GC_SCHEMA'), sel_env.get('GC_SCHEMA')
    if a is not None and b is not None:
        groups.append(('GCSCHEMA', 'SCHEMA', a, b))
    trip += [[r, n, _lab('DRV', 'GCSCHEMA', f)] for f, r, n in _forms(a, b)]
    a, b = ref_env.get('GC_SCHEMA_NAME'), sel_env.get('GC_SCHEMA_NAME')
    if isinstance(a, str) and isinstance(b, str) and a != b:
        trip.append([a, b, _lab('DRV', 'GCSCHEMA', 'ID')])
    if gate in RO1_GATES:
        sel = {'BINDING': (sel_env.get('RO1_ROUTE_A') or {}).get('binding'), 'FACADE': (sel_env.get('AUX_UVT') or {}).get('facade')}
        for what, rp, rsha in RO1_REFERENCE_PINS:
            nb = sel[what]
            if nb is None:
                probs.append('RO1 %s pin missing in the selected driver' % what)
                continue
            groups.append(('RO1', what, (rp, rsha), nb))
            trip += [[r, n, _lab('RO1', what, f)] for f, r, n in _forms((rp, rsha), nb) if f != 'NAME']
    if check_bytes:
        for kind, key, a, b in groups:
            for side, pin in (('reference', a), ('new', b)):
                p = str(pin[0])
                if 'ngc3198' in p.lower():
                    continue  # never opened (no NGC3198 file is read); the pin stays a driver-table derivation
                if not file_ok(p, pin[1]):
                    probs.append('DERIVATION_PIN_BYTES %s %s %s side: %s does not hash to %s' % (kind, key, side, p, pin[1][:12]))
    return trip, groups, probs


def raw_form_ok(x):
    """A token raw must be a custody form: an absolute path, a 64-hex sha, a code basename or a schema id; never a verdict word or a
    number (A73 SF2: a token that could rewrite a verdict, number or result field refuses)."""
    if not isinstance(x, str) or not x or '<' in x or '>' in x or '\n' in x or '|' in x:
        return False
    if x.upper() in VERDICT_WORDS:
        return False
    try:
        float(x)
        return False
    except ValueError:
        pass
    return bool(x.startswith('/') or SHA_RE.fullmatch(x) or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.\-]*\.(py|json)', x)
                or re.fullmatch(r'[A-Z][A-Z0-9_]*_SCHEMA_V[0-9]{3}', x))


def label_ok(lab):
    return isinstance(lab, str) and LABEL_RE.fullmatch(lab) is not None and lab not in RESERVED_LABELS


def token_file_defects(tok):
    """Grammar of the supplied list: [ref, new, label] string triples, label grammar, protected raws, no repeated triple (A71 / A74:
    a repeat is a RECORD_DEFECT naming both entries)."""
    bad, seen = [], {}
    if not isinstance(tok, list):
        return [{'kind': 'DECLARED_NOT_A_LIST'}]
    for i, t in enumerate(tok):
        if not (isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) for x in t)):
            bad.append({'kind': 'NOT_A_STRING_TRIPLE', 'index': i, 'entry': str(t)[:200]})
            continue
        key = tuple(t)
        if key in seen:  # A71[TOKEN_TRIPLES]: a repeated triple is a RECORD_DEFECT naming both entries
            bad.append({'kind': 'RECORD_DEFECT_REPEATED_TRIPLE', 'indexes': [seen[key], i], 'entry': [x[:120] for x in t]})
            LAST_WINS.append({'where': 'declared token triples', 'indexes': [seen[key], i], 'label': t[2][:80]})
            continue
        seen[key] = i  # A71[TOKEN_TRIPLES]
        if not label_ok(t[2]):
            bad.append({'kind': 'LABEL_GRAMMAR', 'index': i, 'label': t[2][:120], 'grammar': LABEL_RE.pattern})
        for side, x in (('reference', t[0]), ('new', t[1])):
            if not raw_form_ok(x):
                bad.append({'kind': 'RAW_NOT_A_CUSTODY_FORM', 'index': i, 'side': side, 'raw': x[:120]})
    return bad


def build_tokens(tok_all):
    """A71 / 0445 item 2: the ref<->new relation must be one-to-one, each pair has exactly ONE label and each label ONE pair.  Labels
    are never joined: a pair with two labels is a defect.  Identical triples are grouped (internal custody lists repeat a pair per
    stage); a repeated SUPPLIED triple is caught earlier by token_file_defects.  Returns (pairs, bad, {})."""
    bad, r2n, n2r, labels, lab2pair = [], {}, {}, {}, {}
    for t in tok_all:  # A71[TOKEN_RELATION]: every relation is a multimap; any fan-out is reported, never resolved
        r, n, lab = t[0], t[1], t[2]
        r2n.setdefault(r, set()).add(n)
        n2r.setdefault(n, set()).add(r)
        labels.setdefault((r, n), set()).add(lab)  # A71[TOKEN_RELATION]
        lab2pair.setdefault(lab, set()).add((r, n))  # A71[TOKEN_RELATION]
    for r, ns in sorted(r2n.items()):
        if len(ns) > 1:
            bad.append({'kind': 'TOKEN_REFERENCE_RAW_PAIRED_TWICE', 'reference_raw': r[:200], 'new_raws': sorted(x[:200] for x in ns)})
    for n, rs in sorted(n2r.items()):
        if len(rs) > 1:
            bad.append({'kind': 'TOKEN_NEW_RAW_PAIRED_TWICE', 'new_raw': n[:200], 'reference_raws': sorted(x[:200] for x in rs)})
    for p, ls in sorted(labels.items()):
        if len(ls) > 1:
            bad.append({'kind': 'TOKEN_PAIR_WITH_TWO_LABELS', 'pair': [p[0][:120], p[1][:120]], 'labels': sorted(ls)})
    for lab, ps in sorted(lab2pair.items()):
        if len(ps) > 1:
            bad.append({'kind': 'TOKEN_LABEL_USED_FOR_TWO_PAIRS', 'label': lab, 'pairs': sorted([a[:120], b[:120]] for a, b in ps)})
        if not label_ok(lab):
            bad.append({'kind': 'LABEL_GRAMMAR', 'label': lab[:120]})
    pairs = [(r, n, sorted(ls)[0]) for (r, n), ls in sorted(labels.items()) if len(ls) == 1 and label_ok(sorted(ls)[0])]
    return pairs, bad, {}


def tokens_policy(gate, tok, drv, ref_env=None, sel_env=None):
    """TOKENS_POLICY: the supplied list must be well formed and equal the A59 derivation exactly (A73 SF2, A74).  `drv` is the
    executed selected driver (c2v006 signature); ref_env defaults to the reference driver the gate is registered with."""
    det = {}
    bad = token_file_defects(tok)
    if sel_env is None:
        sel_env = driver_env(driver_raw(), DRIVER[0])
    if ref_env is None:
        ref_env = {}
        dp = DEFAULT_REFERENCE_DRIVER.get(gate)
        if dp is not None:
            rb = Path(dp).read_bytes()
            ref_env = driver_env(rb, dp) if sha_b(rb) == REFERENCE_DRIVERS.get(dp) else {}
    derived, groups, probs = derive_tokens(gate, ref_env, sel_env)
    det['derivation_problems'] = probs
    if probs:
        bad.append({'kind': 'DERIVATION_FAILED', 'problems': probs[:8]})
    sup = {tuple(t) for t in tok if isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) for x in t)} if isinstance(tok, list) else set()
    der = {tuple(t) for t in derived}
    det['n_supplied'], det['n_derived'] = len(tok) if isinstance(tok, list) else None, len(derived)
    extra, missing = sorted(sup - der), sorted(der - sup)
    if extra:
        bad.append({'kind': 'SUPPLIED_TRIPLE_NOT_DERIVABLE', 'n': len(extra), 'first': [[x[:100] for x in t] for t in extra[:6]]})
    if missing:
        bad.append({'kind': 'DERIVED_TRIPLE_NOT_SUPPLIED', 'n': len(missing), 'first': [[x[:100] for x in t] for t in missing[:6]]})
    news = {t[1] for t in derived}
    if gate == 'Z2':
        base = {f for k in (sel_env.get('UVT_TAIL_KINDS') or ()) for f in (str(sel_env['SCRIPTS'][k][0]), sel_env['SCRIPTS'][k][1],
                                                                             Path(str(sel_env['SCRIPTS'][k][0])).name)}
        det['A59_base_on_new_side'] = sorted(base & {t[1] for t in sup})
        if det['A59_base_on_new_side']:
            bad.append({'kind': 'A59_BASE_ON_NEW_SIDE', 'values': det['A59_base_on_new_side'][:6]})
        succ = {f for k in (sel_env.get('UVT_TAIL_KINDS') or ()) for f in (str(sel_env['SCRIPTS_UVT'][k][0]), sel_env['SCRIPTS_UVT'][k][1])}
        det['A59_successor_missing_on_new_side'] = sorted(succ - {t[1] for t in sup})
        if det['A59_successor_missing_on_new_side']:
            bad.append({'kind': 'A59_SUCCESSOR_MISSING', 'values': det['A59_successor_missing_on_new_side'][:6]})
    else:
        succ = {f for k in (sel_env.get('UVT_TAIL_KINDS') or ()) for f in (str(sel_env['SCRIPTS_UVT'][k][0]), sel_env['SCRIPTS_UVT'][k][1],
                                                                            Path(str(sel_env['SCRIPTS_UVT'][k][0])).name)} if sel_env.get('SCRIPTS_UVT') else set()
        det['successor_on_new_side'] = sorted(succ & ({t[1] for t in sup} | news))
        if det['successor_on_new_side']:
            bad.append({'kind': 'TAIL_OFF_SUCCESSOR_ON_NEW_SIDE', 'values': det['successor_on_new_side'][:6]})
    det['defects'] = bad
    det['reasons'] = [b['kind'] for b in bad]
    return not bad, det


DEFAULT_REFERENCE_DRIVER = {  # the gate records' registered references (B1 / B1_OFF: v008 run 883b37a0; B0prime_RERUN: v009 f33eb362)
    'Z2': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py',
    'Z2_OFF_RO1': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py',
    'Z2_OFF': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py',
    'B0P_RERUN': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py',
}


# ---------------------------------------------------------------- declared rules (B2)
def _get(o, path):
    for k in path:
        if not isinstance(o, dict) or k not in o:
            return False, None
        o = o[k]
    return True, o


def _del(o, path):
    for k in path[:-1]:
        o = o[k]
    del o[path[-1]]


def apply_declared(x, y, rules, fire=None):
    """Apply declared rules to normalized copies x (reference), y (new).  Returns (x, y, report, violations)."""
    x, y = copy.deepcopy(x), copy.deepcopy(y)
    rep, bad = [], []
    for r in rules:
        path, kind = r['path'], r['rule']
        hx, vx = _get(x, path)
        hy, vy = _get(y, path)
        row = {'path': '/' + '/'.join(path), 'rule': kind, 'present': [hx, hy], 'why': r.get('why')}
        ok = True
        if kind == 'MASK':
            row['values'] = [_show(vx) if hx else None, _show(vy) if hy else None]
            ok = hx == hy
        elif kind == 'NEW_ONLY':
            ok = (not hx) and hy and seq(vy, r['value'])
            row['new_value'] = _show(vy) if hy else None
        elif kind == 'NEW_ONLY_OR_EQUAL':  # absent on both: no-op; else new present, reference absent or strictly equal
            ok = (not hx and not hy) or (hy and (not hx or seq(vx, vy)))
            if ok and r.get('keys') is not None and hy:  # SF1: the excused block must have exactly the registered key set
                ok = isinstance(vy, dict) and set(vy) == set(r['keys'])
                row['key_set_exact'] = ok
        elif kind == 'PAIR':
            ok = (not hx and not hy) or (hx and hy and any(seq(vx, a) and seq(vy, b) for a, b in r['pairs']))
            row['values'] = [vx if hx else None, vy if hy else None]
        elif kind == 'COVERED':  # compared by another named check
            ok = hx == hy
            row['covered_by'] = r['check']
        else:
            raise SystemExit('rule kind %s' % kind)
        row['ok'] = bool(ok)
        rep.append(row)
        if ok:
            if (hx or hy) and fire:
                fire('DECLARED_RULE')
            if hx:
                _del(x, path)
            if hy:
                _del(y, path)
        else:
            bad.append(row)
    return x, y, rep, bad


def strict_pins(a, b, path, allowed_new, notes, violations):
    """Pin dictionaries: common keys stay (compared by seq); a one-side key is allowed only when it is NEW-only and in
    allowed_new (normalized key -> normalized value, exact), or allowed_new is the callable verifier.  Removes allowed keys."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) & set(b), key=str):
            if k in PIN_DICTS and isinstance(a[k], dict) and isinstance(b[k], dict):
                ref_only = sorted(set(a[k]) - set(b[k]), key=str)
                new_only = sorted(set(b[k]) - set(a[k]), key=str)
                for key in ref_only:
                    violations.append({'at': path + '/' + k, 'pin': key, 'why': 'REFERENCE_ONLY_PIN'})
                okk = []
                for key in new_only:
                    good = allowed_new(key, b[k][key]) if callable(allowed_new) else (key in allowed_new and seq(allowed_new[key], b[k][key]))
                    if good:
                        okk.append(key)
                    else:
                        violations.append({'at': path + '/' + k, 'pin': key, 'value': str(b[k][key])[:80], 'why': 'UNDECLARED_NEW_ONLY_PIN'})
                if okk:
                    notes.append({'at': path + '/' + k, 'declared_new_only': okk})
                for key in okk:
                    del b[k][key]
            else:
                strict_pins(a[k], b[k], path + '/' + str(k), allowed_new, notes, violations)
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            strict_pins(x, y, '%s[%d]' % (path, i), allowed_new, notes, violations)


# ---------------------------------------------------------------- driver map (AUTO_CUSTODY, c2v004 with the selected driver)
def expected_scripts(gate, kind, workers, ref_t, new_t, uvt_kinds):
    par = workers > 1
    if kind == 'route_a':
        r = (ref_t.get('PARALLEL_ROUTE_A', {}).get('worker') if par else ref_t.get('SCRIPTS', {}).get('route_a'))
        if gate in ('Z2', 'Z2_OFF_RO1'):
            n = new_t['RO1_ROUTE_A'].get('worker_parallel' if par else 'worker')
        else:
            n = new_t['PARALLEL_ROUTE_A'].get('worker') if par else new_t['SCRIPTS'].get('route_a')
        return r, n
    r = ref_t.get('SCRIPTS', {}).get(kind)
    if gate == 'Z2' and kind in uvt_kinds:
        n = new_t['SCRIPTS_UVT'].get(kind)
    else:
        n = new_t['SCRIPTS'].get(kind)
    return r, n


def expected_solver(gate, workers, ref_t, new_t):
    par = workers > 1
    r = ref_t.get('PARALLEL_ROUTE_A', {}).get('solver') if par else ref_t.get('AUX', {}).get('solver')
    if gate == 'Z2':
        n = new_t['AUX_UVT'].get('solver_parallel' if par else 'solver')
    else:
        n = new_t['PARALLEL_ROUTE_A'].get('solver') if par else new_t['AUX'].get('solver')
    return r, n


def stage_kind(name, req):
    k = req.get('kind') if isinstance(req, dict) else None
    return k if isinstance(k, str) else NAME_KIND.get(name)


def workers_of(req):
    v = argv_map((req.get('argv') if isinstance(req, dict) else None) or [], 'route_a --column-workers').get('--column-workers', '1')
    try:
        return int(v)
    except (TypeError, ValueError):
        return -1


def reference_driver_of(st_r):
    """(path, sha, verified bytes or None) of the reference run's start.json driver (REFERENCE_DRIVERS, from bytes)."""
    rdrv, rsha = st_r.get('driver'), st_r.get('driver_sha256')
    raw = None
    if isinstance(rdrv, str) and REFERENCE_DRIVERS.get(rdrv) == rsha and Path(rdrv).is_file():
        b = Path(rdrv).read_bytes()
        if sha_b(b) == rsha:
            raw = b
    return rdrv, rsha, raw


def auto_custody(gate, ref, new, sr, sn, new_t, uvt_kinds, SR, SN, ref_raw=None, declared_pairs=()):
    """c2v006 AUTO_CUSTODY.  c2v007: a pair already declared (A59 derivation) adds no custody token; identical pairs of several stages
    are grouped under ONE label (grouping keeps every stage row; never a conflicting overwrite)."""
    rep = {'reference_driver': None, 'pairs': [], 'inadmissible': []}
    st_r, st_n = SR.json(ref / 'start.json'), SN.json(new / 'start.json')
    rdrv, rsha, raw = reference_driver_of(st_r) if ref_raw is None else (st_r.get('driver'), st_r.get('driver_sha256'), ref_raw)
    ref_t, rd_ok = ({}, False) if raw is None else (driver_tables(raw, rdrv), True)
    rep['reference_driver'] = {'path': rdrv, 'sha256': rsha, 'declared_and_verified_from_bytes': rd_ok, 'tables': sorted(ref_t)}
    admitted = []
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (SR.has(qr) and SN.has(qn)):
            continue
        a, b = SR.json(qr), SN.json(qn)
        if not (a.get('script') == b.get('script') and a.get('script_sha256') == b.get('script_sha256')):
            ka, kb = stage_kind(name, a), stage_kind(name, b)
            kind = ka if ka == kb else None
            workers = workers_of(b) if name == 'route_a' else 1
            exp_r, exp_n = expected_scripts(gate, kind, workers, ref_t, new_t, uvt_kinds) if (kind and rd_ok) else (None, None)
            got_r, got_n = (a.get('script'), a.get('script_sha256')), (b.get('script'), b.get('script_sha256'))
            ok = (rd_ok and kind is not None and exp_r is not None and exp_n is not None and tuple(got_r) == tuple(exp_r)
                  and tuple(got_n) == tuple(exp_n) and file_ok(*exp_n))
            row = {'stage': name, 'kind': kind, 'what': 'script', 'reference': list(got_r), 'new': list(got_n),
                   'expected_reference': list(exp_r) if exp_r else None, 'expected_new': list(exp_n) if exp_n else None, 'admitted': ok}
            rep['pairs'].append(row)
            if ok:
                for i, k in enumerate(('PATH', 'SHA')):
                    if got_r[i] != got_n[i]:
                        admitted.append([got_r[i], got_n[i], '<SCRIPT_%s_%s>' % (name.upper(), k)])
            else:
                rep['inadmissible'].append(row)
        if name == 'route_a':
            ma, mb = argv_map(a.get('argv') or [], 'reference route_a'), argv_map(b.get('argv') or [], 'new route_a')
            gr, gn = (ma.get('--solver'), ma.get('--solver-sha256')), (mb.get('--solver'), mb.get('--solver-sha256'))
            if any(isinstance(x, Dup) for x in gr + gn):
                row = {'stage': name, 'what': 'solver', 'reference': [str(x) for x in gr], 'new': [str(x) for x in gn],
                       'admitted': False, 'why': 'DUPLICATE_ARGV'}
                rep['pairs'].append(row)
                rep['inadmissible'].append(row)
            elif gr != gn:
                exp_r, exp_n = expected_solver(gate, workers_of(b), ref_t, new_t) if rd_ok else (None, None)
                ok = (rd_ok and exp_r is not None and exp_n is not None and tuple(gr) == tuple(exp_r) and tuple(gn) == tuple(exp_n)
                      and file_ok(*exp_n))
                row = {'stage': name, 'what': 'solver', 'reference': list(gr), 'new': list(gn),
                       'expected_reference': list(exp_r) if exp_r else None, 'expected_new': list(exp_n) if exp_n else None, 'admitted': ok}
                rep['pairs'].append(row)
                if ok:
                    for i, k in enumerate(('SOLVER', 'SOLVER_SHA256')):
                        if gr[i] != gn[i]:
                            admitted.append([gr[i], gn[i], '<ROUTE_A_%s>' % k])
                else:
                    rep['inadmissible'].append(row)
    nd = (st_n.get('driver'), st_n.get('driver_sha256'))
    if (rdrv, rsha) != nd:
        ok = rd_ok and list(nd) == DRIVER and sha_b(driver_raw()) == DRIVER[1]
        row = {'what': 'driver', 'reference': [rdrv, rsha], 'new': list(nd), 'expected_new': list(DRIVER), 'admitted': ok}
        rep['pairs'].append(row)
        if ok:
            admitted += [[rdrv, nd[0], '<DRIVER_PATH>'], [rsha, nd[1], '<DRIVER_SHA256>']]
        else:
            rep['inadmissible'].append(row)
    decl = {(t[0], t[1]) for t in declared_pairs}
    grouped, order = {}, []
    for r, n, lab in admitted:  # A71[CUSTODY_GROUP]: identical (ref, new) pairs grouped with all their stage labels
        if (r, n) in decl:
            continue
        if (r, n) not in grouped:
            grouped[(r, n)] = []  # A71[CUSTODY_GROUP]
            order.append((r, n))
        grouped[(r, n)].append(lab)
    out = [[r, n, sorted(grouped[(r, n)])[0], 'CUSTODY_TOKEN'] for r, n in order]
    rep['grouped_labels'] = {sorted(v)[0]: sorted(v) for v in grouped.values() if len(v) > 1}  # A71[CUSTODY_GROUP]
    rep['skipped_as_declared'] = sum(1 for r, n, lab in admitted if (r, n) in decl)
    return out, rep


def planned_script(gate, name, req, drv):
    """A59 raw custody: the (script, sha) the selected driver plans for this new stage (driver L2609, L2852-2861, L1821)."""
    kind = stage_kind(name, req)
    if kind == 'route_a':
        w = workers_of(req)
        if gate in ('Z2', 'Z2_OFF_RO1'):
            p = drv.RO1_ROUTE_A['worker' if w == 1 else 'worker_parallel']
        else:
            p = drv.SCRIPTS['route_a'] if w == 1 else drv.PARALLEL_ROUTE_A['worker']
        return kind, p
    if kind == 'route_a_tail_manifest':
        return kind, drv.AUX_UVT['manifest_writer'] if gate == 'Z2' else None
    if gate == 'Z2' and kind in drv.UVT_TAIL_KINDS:
        return kind, drv.SCRIPTS_UVT[kind]
    return kind, drv.SCRIPTS.get(kind)


# ---------------------------------------------------------------- tail argv expectations (S1/S2)
def caller_norm(c, tail_on, declared_record=None):
    c = dict(c)
    if tail_on:
        nc = dict(c.get('numerical_controls') or {})
        nc.pop('uv_tail', None)
        c['numerical_controls'] = nc
        bp = c.get('boundary_prescription')
        if isinstance(bp, str) and ' UV-TAIL' in bp:
            c['boundary_prescription'] = bp.split(' UV-TAIL')[0]
    elif declared_record is not None:
        nc = dict(c.get('numerical_controls') or {})
        if 'uv_tail' in nc and nc['uv_tail'] == declared_record:
            nc.pop('uv_tail')
            c['numerical_controls'] = nc
    return c


def source_rotation_stage(name):
    """driver L3168 (rfs: fs_rot), L3172/L3276 (le p: le(p-1) rotation; le1: fs_rot)."""
    if name.startswith('rfs_columns'):
        return 'fs_rotation'
    m = re.fullmatch(r'le([0-9]+)_(columns_[0-9]{2}|rotation)', name)
    if m:
        p = int(m.group(1))
        return 'fs_rotation' if p == 1 else 'le%d_rotation' % (p - 1)
    return None


def expected_tail_blocks(gate, drv, new, sn, rec, SN):
    """Raw expected tail argv per new stage name ('*' for every other stage = []), plus the UV_TAIL_RECORD cross-check."""
    def sha_or(p):
        return SN.sha_of(p) if SN.has(p) else 'MISSING_FILE(%s)' % p
    blocks, rc = {}, None
    if gate == 'Z2':
        req = new / 'inputs/uv_tail_route_a_request.json'
        cfg = new / 'inputs/uv_tail_config.json'
        man_dir = sn.get('route_a_tail_manifest')
        man = (man_dir / 'manifest/ROUTE_A_TAIL_MANIFEST.json') if man_dir is not None else None
        ra = sn.get('route_a')
        if ra is not None:
            blocks['route_a'] = ['--uv-tail-config', str(req), '--uv-tail-config-sha256', sha_or(req),
                                 '--eps-certificate', TEST_ONLY, '--eps-certificate-sha256', TEST_ONLY,
                                 '--lo-certificate', TEST_ONLY, '--lo-certificate-sha256', TEST_ONLY,
                                 '--uv-tail-sidecar-directory', str(ra / 'uv_tail_sidecar')]
        trunc = rec.get('truncation_argv') if isinstance(rec, dict) else None
        rc = {'record_present': isinstance(rec, dict)}
        if isinstance(rec, dict):
            rc.update({
                'enabled_true': rec.get('enabled') is True,
                'config_is_inputs_file_from_bytes': (rec.get('config') or {}).get('path') == str(cfg) and (rec.get('config') or {}).get('sha256') == sha_or(cfg),
                'request_is_inputs_file_from_bytes': (rec.get('request') or {}).get('path') == str(req) and (rec.get('request') or {}).get('sha256') == sha_or(req),
                'manifest_is_stage_file_from_bytes': man is not None and (rec.get('manifest') or {}).get('path') == str(man) and (rec.get('manifest') or {}).get('sha256') == sha_or(man),
                'admissibility_test_only': rec.get('admissibility') == 'test_only',
                'test_only_flag': rec.get('test_only_flag') == ['--uv-tail-admit-test-only'],
                'certificates_test_only': rec.get('certificates') == {'eps_certificate': [TEST_ONLY, TEST_ONLY], 'lo_certificate': [TEST_ONLY, TEST_ONLY]},
                'route_a_argv_equals_driver_block': ra is not None and rec.get('route_a_argv') == blocks['route_a'][:-2],
                'truncation_argv_null_or_json': trunc is None or (isinstance(trunc, str) and _is_json(trunc)),
            })
        for name, d in sn.items():
            if name in ('route_a', 'route_a_tail_manifest') or not SN.has(d / 'request.json'):
                continue
            kind = stage_kind(name, SN.json(d / 'request.json'))
            if kind not in drv.UVT_TAIL_KINDS:
                continue
            bk = drv.UVT_BINDING_KIND[kind]
            b = ['--uv-tail-config', str(cfg), '--uv-tail-config-sha256', sha_or(cfg), '--uv-tail-admit-test-only']
            if bk in ('reference', 'body', 'offset'):
                b += ['--route-a-tail-manifest', str(man) if man else 'MISSING_MANIFEST_STAGE',
                      '--route-a-tail-manifest-sha256', sha_or(man) if man else 'MISSING_MANIFEST_STAGE']
            if bk not in ('reference', 'body') and trunc is not None:
                b += ['--uv-tail-truncation', trunc]
            if bk in ('rfs_columns', 'le_columns', 'le_rotation'):
                src = source_rotation_stage(name)
                b += ['--uv-tail-source-rotation-directory', str(sn[src] / 'rotation') if src in sn else 'MISSING_SOURCE_ROTATION(%s)' % name]
            blocks[name] = b  # A71[STAGE_KEYED]
    elif gate == 'Z2_OFF_RO1':
        ra = sn.get('route_a')
        if ra is not None:
            off = new / 'inputs' / OFF_REQUEST_NAME
            E = sha_b(off_request_bytes(drv))
            blocks['route_a'] = ['--uv-tail-config', str(off), '--uv-tail-config-sha256', E, '--eps-certificate', TEST_ONLY,
                                 '--eps-certificate-sha256', TEST_ONLY, '--lo-certificate', TEST_ONLY, '--lo-certificate-sha256', TEST_ONLY,
                                 '--uv-tail-sidecar-directory', str(ra / 'uv_tail_sidecar')]
    return blocks, rc


def _is_json(s):
    try:
        jloads(s)
        return True
    except ValueError:
        return False


def check_argv(name, ra, rb, block, suffix):
    """S1/S2: rb must be ra with `block` inserted once, contiguously (at the end when suffix), and no other tail flag."""
    why = []
    if not isinstance(ra, list) or not isinstance(rb, list):
        return ['argv not a list']
    for f in TAIL_FLAGS:
        if ra.count(f):
            why.append('tail flag %s on the reference side' % f)
        nb, ne = rb.count(f), block.count(f)
        if nb != ne:
            why.append('tail flag %s occurs %d times, the driver emits it %d times on this stage' % (f, nb, ne))
    if not block:
        if not seq(ra, rb):
            why.append(('argv', diffs(ra, rb)[:4]))
        return why
    L = len(block)
    try:
        i = rb.index(block[0])
    except ValueError:
        return why + ['tail block absent']
    if suffix and i != len(ra):
        why.append('tail block not at the end of the route-A argv (driver L2845/L2848)')
    if not (seq(rb[:i], ra[:i]) and seq(rb[i:i + L], block) and seq(rb[i + L:], ra[i:])):
        why.append(('argv is not the reference argv plus exactly the driver tail block', {'new_at_block': rb[i:i + L], 'expected_block': block}))
    return why


def off_request_bytes(drv):
    return (json.dumps(drv._jsonable(drv.ro1_off_request()), indent=1, allow_nan=False) + '\n').encode()


def pair_norm(R, N, a, b, rel, drop=()):
    """Normalize one file's two parsed values with the per-file class context; returns the masked-key paths of each side."""
    mr, mn = [], []
    with R.at_file(rel):
        x = R.norm(a, drop, at=rel, rec=mr)
    with N.at_file(rel):
        y = N.norm(b, drop, at=rel, rec=mn)
    return x, y, mr, mn


def mask_cmp(mr, mn, rel, applied=()):
    """Masked keys must sit at the same paths on both sides, except under a subtree an applied declared rule excused."""
    pre = [rel + r['path'] for r in applied if r.get('ok') and any(r.get('present') or ())]

    def keep(ps):
        return sorted(p for p in ps if not any(p == q or p.startswith(q + '/') or p.startswith(q + '[') for q in pre))
    a, b = keep(mr), keep(mn)
    return a == b, {'reference_only': sorted(set(a) - set(b))[:6], 'new_only': sorted(set(b) - set(a))[:6]}


def check_requests(gate, R, N, sr, sn, blocks):
    bad, n, inserted = [], 0, {}
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (R.store.has(qr) and N.store.has(qn)):
            if R.store.has(qr) != N.store.has(qn):
                bad.append((name, 'request.json present on one side only'))
            continue
        n += 1
        rel = 'stages/%s/request.json' % name
        a, b, mr_, mn_ = pair_norm(R, N, R.store.json(qr), N.store.json(qn), rel)
        mok, mdet = mask_cmp(mr_, mn_, rel)
        if not mok:
            bad.append((name, 'masked keys at different paths', mdet))
        with N.at_file(rel):
            block = N.norm(blocks.get(name, []), at='<driver tail block %s>' % name)
        if not isinstance(a, dict) or not isinstance(b, dict):
            bad.append((name, 'request.json is not an object'))
            continue
        ra, rb = a.get('argv') or [], b.get('argv') or []
        why = check_argv(name, ra, rb, block, suffix=(name == 'route_a'))
        if why:
            bad.append((name, why[:6]))
        elif block:
            inserted[name] = block  # A71[STAGE_KEYED]
        a2, b2 = dict(a), dict(b)
        a2.pop('argv', None)
        b2.pop('argv', None)
        if not seq(a2, b2):
            bad.append((name, diffs(a2, b2)[:4]))
    missing_block = sorted(k for k in blocks if k not in sr or k not in sn)
    if missing_block:
        bad.append(('expected tail-ON stages without a reference/new request pair', missing_block))
    return not bad, {'requests_compared': n, 'differing': bad[:16], 'tail_blocks_inserted': inserted}


def check_manifest_stage(gate, drv, new, sn, SN):
    """Z2: the route_a_tail_manifest request is the driver's (L2930-2934, L1821): script = AUX_UVT manifest_writer (from bytes)."""
    d = sn.get('route_a_tail_manifest')
    ra = sn.get('route_a')
    if d is None or not SN.has(d / 'request.json'):
        return False, {'reason': 'no route_a_tail_manifest request'}
    q = SN.json(d / 'request.json')
    mw = drv.AUX_UVT['manifest_writer']
    det = {'script': q.get('script') == str(mw[0]) and q.get('script_sha256') == mw[1] and file_ok(str(mw[0]), mw[1]),
           'kind_and_name': q.get('kind') == 'route_a_tail_manifest' and q.get('name') == 'route_a_tail_manifest'}
    exp = None
    if ra is not None and SN.has(ra / 'request.json'):
        am = argv_map(SN.json(ra / 'request.json').get('argv') or [], 'new route_a (manifest expectation)')
        req = new / 'inputs/uv_tail_route_a_request.json'
        exp = ['--seed', am.get('--seed'), '--seed-sha256', am.get('--seed-sha256'), '--attempt-directory', am.get('--outdir'),
               '--checkpoint-directory', am.get('--checkpoint-directory'), '--checkpoint-module', str(drv.AUX['checkpoint_module'][0]),
               '--checkpoint-module-sha256', drv.AUX['checkpoint_module'][1], '--uv-tail-request', str(req),
               '--uv-tail-request-sha256', SN.sha_of(req) if SN.has(req) else 'MISSING_FILE', '--outdir', str(d / 'manifest')]
        if any(isinstance(x, Dup) for x in exp):
            exp = None
    det['argv'] = exp is not None and q.get('argv') == exp
    if not det['argv']:
        det['argv_found'], det['argv_expected'] = q.get('argv'), (None if exp is None else [str(x) for x in exp])
    return all(v is True for k, v in det.items() if k in ('script', 'kind_and_name', 'argv')), det


# ---------------------------------------------------------------- tail-off declared records (c2v004 unchanged)
def route_a_facts(run, stages, S, T):
    d = stages.get('route_a')
    if d is None or not S.has(d / 'request.json'):
        return None
    req = S.json(d / 'request.json')
    atts = [x for x in T.subdirs(d) if x.startswith('attempt_')]
    st = d / 'attempt_000' / 'start.json'
    return {'dir': d, 'request': req, 'argv': argv_map(req.get('argv') or [], '%s route_a' % S.tag), 'attempts': atts,
            'start': S.json(st) if S.has(st) else None}


def check_declared_off(drv, new_run, fn, cn_raw, SN, TN):
    raw = off_request_bytes(drv)
    E = sha_b(raw)
    d1 = new_run / 'inputs' / OFF_REQUEST_NAME
    det = {'expected_request_sha256': E}
    det['D1_request_file'] = SN.has(d1) and SN.sha_of(d1) == E and seq(SN.json(d1), jloads(raw)) and SN.json(d1) == drv.ro1_off_request()
    if fn is None:
        det['route_a'] = 'NO_COMPUTED_ROUTE_A'
        return False, det, None, set(), E
    side = fn['dir'] / 'uv_tail_sidecar'
    rec = {'request': {'path': str(d1.resolve()), 'sha256': E}, 'enabled': False, 'sidecar_directory': str(side.resolve())}
    am = fn['argv']
    g = {k: am.get(k) for k in ('--uv-tail-config', '--uv-tail-config-sha256', '--eps-certificate', '--eps-certificate-sha256',  # A71[FIXED_KEYS]
                                '--lo-certificate', '--lo-certificate-sha256', '--uv-tail-sidecar-directory')}
    det['argv_flags'] = (not any(isinstance(v, Dup) for v in g.values())
                         and g['--uv-tail-config'] is not None and str(Path(g['--uv-tail-config']).resolve()) == str(d1.resolve())
                         and g['--uv-tail-config-sha256'] == E
                         and all(g[k] == drv.UVT_TEST_ONLY for k in ('--eps-certificate', '--eps-certificate-sha256', '--lo-certificate', '--lo-certificate-sha256'))
                         and g['--uv-tail-sidecar-directory'] is not None and str(Path(g['--uv-tail-sidecar-directory']).resolve()) == str(side.resolve()))
    det['attempts'] = fn['attempts']
    det['single_attempt'] = fn['attempts'] == ['attempt_000']
    st = fn['start'] or {}
    det['D2_start_json_record'] = seq(st.get('uv_tail'), rec)
    caller_rec = ((cn_raw or {}).get('numerical_controls') or {}).get('uv_tail', '<ABSENT>')
    det['D3_observed'] = 'ABSENT' if caller_rec == '<ABSENT>' else ('DECLARED_RECORD' if caller_rec == rec else 'OTHER')
    det['D3_caller_record'] = det['D3_observed'] in ('ABSENT', 'DECLARED_RECORD')
    det['sidecar_absent'] = not TN.has_under(os.path.relpath(side, new_run))
    if not det['D2_start_json_record']:
        det['D2_found'] = st.get('uv_tail', '<ABSENT>')
    if not det['D3_caller_record']:
        det['D3_found'] = caller_rec
    rel_start = TN.canon(str((fn['dir'] / 'attempt_000' / 'start.json').relative_to(new_run)))
    expected = {'inputs/%s/uv_tail' % OFF_REQUEST_NAME, rel_start + '/uv_tail'}
    ok = all(det[k] for k in ('D1_request_file', 'argv_flags', 'single_attempt', 'D2_start_json_record', 'D3_caller_record', 'sidecar_absent'))
    return ok, det, rec, expected, E


def stray_uv_tail(tree, S):
    """Declared JSON files (outside checkpoints; S.declared): key walk on the parsed value; every other JSON / JSONL file: the phase-1
    byte scan.  (The c2v006 two-argument signature is kept.)"""
    declared_rels = getattr(S, 'declared', ())
    out = []

    def walk(o, where):
        if isinstance(o, dict):
            for k, x in o.items():
                if k in TAIL_KEYS:
                    out.append({'at': where + '/' + k, 'enabled': x.get('enabled') if isinstance(x, dict) else None})
                walk(x, where + '/' + k)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, '%s[%d]' % (where, i))
    run = tree.run
    for rel in tree.files:
        c = tree.canon(rel)
        if '/checkpoint/' in '/' + c or not (c.endswith('.json') or c.endswith('.jsonl')):
            continue
        if c.endswith('.json') and c in declared_rels:
            o = S.json(run / rel)
            if isinstance(o, Unparseable):
                out.append({'at': c + ':UNPARSEABLE', 'enabled': None})
                continue
            walk(o, c)
        elif b'"uv_tail' in S.hits.get(str(run / rel), ()):
            out.append({'at': c + (':JSONL_TEXT' if c.endswith('.jsonl') else ':BYTE_SCAN'), 'enabled': None})
    return out


def ro1_block(rn):
    return (rn.get('route_a_outcome') or {}).get('ro1') if isinstance(rn, dict) else None


def check_ro1_armed(ro1, expected_worker, binding_sha):
    ok = (isinstance(ro1, dict) and set(ro1) == RO1_KEYS and ro1.get('rule') == 'RO1' and ro1.get('armed') is True
          and ro1.get('fired') is False and ro1.get('events') == [] and ro1.get('worker_sha256') == expected_worker
          and ro1.get('binding_sha256') == binding_sha)
    det = {'new_ro1': ro1, 'expected_worker_sha256': expected_worker, 'expected_binding_sha256': binding_sha,
           'key_set_exact': isinstance(ro1, dict) and set(ro1) == RO1_KEYS, 'registered_keys': sorted(RO1_KEYS)}
    if isinstance(ro1, dict) and set(ro1) != RO1_KEYS:
        det['extra_keys'], det['missing_keys'] = sorted(set(ro1) - RO1_KEYS), sorted(RO1_KEYS - set(ro1))
    return ok, det


def check_ro1_unarmed(ro1):
    ok = (isinstance(ro1, dict) and set(ro1) == RO1_KEYS and ro1.get('rule') == 'RO1' and ro1.get('armed') is False
          and ro1.get('fired') is False and ro1.get('events') == [] and ro1.get('worker_sha256') is None and ro1.get('binding_sha256') is None)
    det = {'new_ro1': ro1, 'key_set_exact': isinstance(ro1, dict) and set(ro1) == RO1_KEYS, 'registered_keys': sorted(RO1_KEYS)}
    if isinstance(ro1, dict) and set(ro1) != RO1_KEYS:
        det['extra_keys'], det['missing_keys'] = sorted(set(ro1) - RO1_KEYS), sorted(RO1_KEYS - set(ro1))
    return ok, det


def ro1_expectations(drv, fn):
    n = workers_of(fn['request']) if fn else 1
    w = drv.RO1_ROUTE_A['worker' if n == 1 else 'worker_parallel']
    return n, (str(w[0]), w[1])


def check_custody(drv, tok_all, fr, fn, worker):
    news = {}
    for t in tok_all:  # A71[RO1_CUSTODY]: multimap new raw -> [(ref raw, label)]
        news.setdefault(t[1], []).append((t[0], t[2]))
    bind, fac = drv.RO1_ROUTE_A['binding'], drv.AUX_UVT['facade']
    need = {'worker_path': worker[0], 'worker_sha256': worker[1], 'binding_path': str(bind[0]), 'binding_sha256': bind[1],
            'facade_path': str(fac[0]), 'facade_sha256': fac[1]}
    present = {k: (v in news) for k, v in need.items()}  # A71[FIXED_KEYS]
    ref_pins = ((fr or {}).get('start') or {}).get('input_pins') or {}
    consistent = {}
    for what in ('binding', 'facade'):
        rp = [r for r, _ in news.get(need[what + '_path'], [])]
        rs = [r for r, _ in news.get(need[what + '_sha256'], [])]
        consistent[what] = any(ref_pins.get(p) == s for p in rp for s in rs)  # A71[FIXED_KEYS]
    new_pins = ((fn or {}).get('start') or {}).get('input_pins') or {}
    new_ok = {'binding': new_pins.get(str(Path(bind[0]).resolve())) == bind[1], 'facade': new_pins.get(str(Path(fac[0]).resolve())) == fac[1],
              'worker_pin': ((fn or {}).get('start') or {}).get('worker_pin') == worker[1],
              'request_script': bool(fn) and fn['request'].get('script') == worker[0] and fn['request'].get('script_sha256') == worker[1]}
    ok = all(present.values()) and all(consistent.values()) and all(new_ok.values())
    return ok, {'declared_entries_present': present, 'reference_side_is_reference_pin': consistent, 'new_attempt_pins': new_ok}


# ---------------------------------------------------------------- generic file comparison (S3)
def ra_new_pins(gate, drv, N, new):
    """Declared new-only route-A pins (normalized key -> normalized value): the tail code the RO1 workers pin (driver
    ro1_off_pins L966-975 / AUX_UVT controller, UVT_LIB) and the route-A tail request input."""
    if gate not in ('Z2', 'Z2_OFF_RO1'):
        return {}
    exp = {}
    req = new / 'inputs' / ('uv_tail_route_a_request.json' if gate == 'Z2' else OFF_REQUEST_NAME)
    items = [(p, s) for p, s in (drv.AUX_UVT['controller'], drv.UVT_LIB['lib'], drv.UVT_LIB['roster'], drv.UVT_LIB['provider'])]
    items.append((req, N.store.sha_of(req) if N.store.has(req) else 'MISSING_FILE(%s)' % req))
    for p, s in items:
        k = N.s(str(Path(p).resolve()), '<declared route-A pin key>')
        if k in exp:  # A71[RA_PINS]
            LAST_WINS.append({'where': 'declared route-A new-only pins', 'normalized_key': k})
            exp[k] = Collided([str(p)])
            continue
        exp[k] = N.s(s, '<declared route-A pin value>')  # A71[RA_PINS]
    return exp


SELECTED_PIN_ENTRIES = [None, None]  # SF3: [the selected driver's (path, sha) table entries, the driver sha they came from]


def static_pin_verifier(N):
    """top-level start.json static_pins (SF3): a NEW-only pin is admitted only when (raw path, raw sha) is an entry of the selected
    driver's tables (from its hashed bytes) AND the path's bytes hash to the sha."""
    rev = {}
    if SELECTED_PIN_ENTRIES[0] is None or SELECTED_PIN_ENTRIES[1] != DRIVER[1]:
        SELECTED_PIN_ENTRIES[:] = [driver_pin_entries(driver_env(driver_raw(), DRIVER[0])), DRIVER[1]]
    entries = SELECTED_PIN_ENTRIES[0]

    def ok(key_norm, val_norm):
        raw = rev.get(key_norm)
        return isinstance(raw, tuple) and (str(raw[0]), raw[1]) in entries and file_ok(raw[0], raw[1])
    return ok, rev


def compare_json_file(rel, p, q, R, N, rules, pin_allow):
    x, y, mr_, mn_ = pair_norm(R, N, R.store.json(p), N.store.json(q), rel)
    notes, viol = [], []
    if pin_allow is not None:
        strict_pins(x, y, rel, pin_allow, notes, viol)
    with N.at_file(rel):
        x, y, rep, bad = apply_declared(x, y, rules, fire=N._fire)
    mok, mdet = mask_cmp(mr_, mn_, rel, rep)
    ok = seq(x, y) and not viol and not bad and mok
    det = None
    if not ok:
        det = {'file': rel, 'differing': diffs(x, y)[:4], 'pin_violations': viol[:6], 'rule_violations': bad[:4],
               'masked_key_paths_equal': mok, 'masked_key_paths': mdet if not mok else None}
    return ok, det, rep, notes


def compare_jsonl(rel, p, q, R, N, extra_mask=(), drop_new_stage=()):
    lr, ln = R.store.jsonl(p), N.store.jsonl(q)
    xs, ys, mrs, mns = [], [], [], []
    for i, o in enumerate(lr):
        mr = []
        with R.at_file(rel):
            xs.append(R.norm(o, drop=extra_mask, at='%s:%d' % (rel, i), rec=mr))
        mrs.append(sorted(m.split(':', 1)[1].split('/', 1)[-1] for m in mr))
    for i, o in enumerate(ln):
        mn = []
        with N.at_file(rel):
            ys.append(N.norm(o, drop=extra_mask, at='%s:%d' % (rel, i), rec=mn))
        mns.append(sorted(m.split(':', 1)[1].split('/', 1)[-1] for m in mn))
    dropped = 0
    if drop_new_stage:
        keep, keepm = [], []
        for e, m in zip(ys, mns):
            if isinstance(e, dict) and e.get('stage') in drop_new_stage:
                dropped += 1
            else:
                keep.append(e)
                keepm.append(m)
        ys, mns = keep, keepm
    mok = mrs == mns
    ok = seq(xs, ys) and (not drop_new_stage or dropped == 2 * len(drop_new_stage)) and mok
    return ok, (None if ok else {'file': rel, 'n': [len(xs), len(ys)], 'dropped_declared': dropped, 'differing': diffs(xs, ys)[:4],
                                 'masked_key_paths_equal': mok})


# ---------------------------------------------------------------- main
def main(argv=None):
    a = parse_cli(argv)
    if a.gate in RETIRED_GATES:
        raise SystemExit('REFUSED: ' + RETIRED_GATES[a.gate])
    if a.gate not in GATES:
        raise SystemExit('REFUSED: unknown gate %r (one of %s)' % (a.gate, sorted(GATES)))
    if a.driver not in DRIVERS:
        raise SystemExit('REFUSED: --driver must be one of %s' % sorted(DRIVERS))
    tail_on, ro1_req, declared_off = GATES[a.gate]
    if ro1_req == 'UNARMED' and a.require_ro1_armed:
        raise SystemExit('REFUSED: --require-ro1-armed contradicts gate %s (A52.1: ro1 armed false, fired false)' % a.gate)
    if ro1_req == 'OPTIONAL' and a.require_ro1_armed:
        ro1_req = 'ARMED_BLOCK_ONLY'
    # N3: both run paths through the containment guard before anything under them is opened
    resolved = {}
    for k in ('reference', 'new'):
        real, why = guarded_resolve(getattr(a, k))
        if why:
            raise SystemExit('REFUSED: --%s path guard: %s' % (k, why))
        resolved[k] = Path(real)  # A71[FIXED_KEYS]
    ref, new = resolved['reference'], resolved['new']
    if not ref.is_dir() or not new.is_dir():
        raise SystemExit('REFUSED: --reference and --new must be directories')
    if ref == new or str(new).startswith(str(ref) + '/') or str(ref).startswith(str(new) + '/'):
        raise SystemExit('REFUSED: the reference and new runs must be distinct, non-nested directories')
    outp = Path(os.path.abspath(a.out))
    for r in (ref, new):
        op = str(Path(os.path.realpath(outp.parent)))
        if str(outp).startswith(str(r) + '/') or op == str(r) or op.startswith(str(r) + '/'):
            raise SystemExit('REFUSED: --out must not be inside a compared run')
    DRIVER[:] = list(DRIVERS[a.driver])
    DRIVER_RAW[0] = DRIVER_RAW[1] = None
    SELECTED_PIN_ENTRIES[:] = [None, None]
    driver_raw()
    me_raw = Path(__file__).read_bytes()
    tok_raw = Path(a.tokens).read_bytes()
    try:
        tok_doc = jloads(tok_raw)
        if not isinstance(tok_doc, dict) or 'declared' not in tok_doc:
            raise ValueError('tokens file must be an object with a "declared" list')
        if set(tok_doc) - TOKEN_FILE_KEYS:
            raise ValueError('tokens file has unknown keys %s' % sorted(set(tok_doc) - TOKEN_FILE_KEYS))
        tok = tok_doc['declared']
    except (ValueError, KeyError, TypeError) as e:
        raise SystemExit('REFUSED: tokens file %s: %s' % (a.tokens, e))
    if os.path.lexists(a.out):
        raise SystemExit('REFUSED: --out exists (exclusive create): %s' % a.out)
    MASK_KEYS.clear()
    MASK_KEYS.update(MASK_KEYS_BASE | (TAIL_KEYS if tail_on else set()))
    del LAST_WINS[:]
    checks = {}
    head = {'schema': SCHEMA, 'gate': a.gate, 'driver_selected': a.driver, 'driver_pin': list(DRIVER),
            'tail_on': tail_on, 'ro1_requirement': ro1_req, 'declared_tail_off_records': declared_off,
            'require_ro1_armed_flag': bool(a.require_ro1_armed), 'masked_keys': sorted(MASK_KEYS), 'array_policy': ARRAY_POLICY,
            'declared_differ': [[i, rx, list(cl)] for i, gs, rx, cl, why in DECLARED_DIFFER if a.gate in gs],
            'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_b(me_raw)},
            'reference': str(ref), 'new': str(new), 'tokens': {'path': str(Path(a.tokens).resolve()), 'sha256': sha_b(tok_raw)}}

    def put(name, ok, detail):
        if name in checks:  # A71[CHECKS]: a check reported twice keeps both reports and FAILs (never last-wins)
            LAST_WINS.append({'where': 'check reported twice', 'check': name})
            checks[name] = {'pass': False, 'detail': {'why': 'A71: check reported twice', 'first': checks[name], 'second': {'pass': bool(ok), 'detail': detail}}}
            return
        checks[name] = {'pass': bool(ok), 'detail': detail}  # A71[CHECKS]
    extra, hold = {}, {}
    try:
        _compare(a, ref, new, tok, tok_doc, tail_on, ro1_req, declared_off, put, extra, hold)
    except Exception as e:  # never crash without a report; an exception is a FAIL
        put('COMPARATOR_EXCEPTION', False, {'type': type(e).__name__, 'message': str(e)[:500],
                                            'traceback': traceback.format_exc()[-4000:]})
        if 'SR' in hold and 'STRICT_PARSE' not in checks:
            _strict_puts(put, hold, partial=True)
    clash = sorted(set(head) & set(extra))
    if clash:  # A71[REPORT_MERGE]: report sections never overwrite each other
        LAST_WINS.append({'where': 'report merge', 'keys': clash})
        checks['REPORT_MERGE'] = {'pass': False, 'detail': {'clashing_keys': clash}}
    rep = dict(head, **{k: v for k, v in extra.items() if k not in head})  # A71[REPORT_MERGE]
    rep['checks'] = checks
    rep['verdict'] = 'PASS_BITWISE_EQUAL' if checks and all(c['pass'] for c in checks.values()) else 'FAIL'
    rep['failing'] = [k for k, c in checks.items() if not c['pass']]
    rep['comparator_sha256_at_end'] = sha_file(__file__)
    if rep['comparator_sha256_at_end'] != head['comparator']['sha256']:
        rep['verdict'] = 'FAIL'
        rep['failing'].append('COMPARATOR_SOURCE_CHANGED_DURING_RUN')
    with open(a.out, 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({'verdict': rep['verdict'], 'failing': rep['failing']}))
    return 0 if rep['verdict'] == 'PASS_BITWISE_EQUAL' else 1


def _strict_puts(put, h, partial=False):
    SR, SN, R, N, tok_bad = h['SR'], h['SN'], h.get('R'), h.get('N'), h.get('tok_bad', [])
    rc = R.collisions if R else []
    nc = N.collisions if N else []
    put('STRICT_PARSE', not SR.problems and not SN.problems,
        {'rule': 'duplicate JSON members (equal values too), duplicate NPY header keys, duplicate / non-.npy NPZ members, data before the '
                 'first NPZ member, unparseable JSON / JSONL / NPZ / NPY: all FAIL (A71, A74)',
         'partial_after_exception': partial, 'reference': SR.problems[:12], 'new': SN.problems[:12], 'n': [len(SR.problems), len(SN.problems)],
         'files_parsed': [len(SR._json) + len(SR._arr), len(SN._json) + len(SN._arr)]})
    put('PARSE_SURFACE', not SR.surface and not SN.surface,
        {'rule': 'only declared files are parsed; only regular files of the tree are opened (A74)', 'partial_after_exception': partial,
         'violations': (SR.surface + SN.surface)[:12], 'n': [len(SR.surface), len(SN.surface)]})
    rt = {'reference': [R.n_roundtrip, R.n_strings] if R else None, 'new': [N.n_roundtrip, N.n_strings] if N else None}
    rt_bad = (R.roundtrip_bad if R else []) + (N.roundtrip_bad if N else [])
    put('NORM_INJECTIVE', not rc and not nc and not tok_bad and not rt_bad and bool(R) and bool(N),
        {'rule': 'normalization is injective: one-pass replacement with self-delimiting outputs and every other "<" escaped; each '
                 'normalized string decodes back to its raw string; raw text with normalizer output, many-to-one sha tokens and any '
                 'non-bijective token relation FAIL',
         'partial_after_exception': partial, 'reference': rc[:12], 'new': nc[:12], 'n': [len(rc), len(nc)], 'tokens': tok_bad[:12],
         'roundtrip_ok_of_strings': rt, 'roundtrip_failures': rt_bad[:12]})
    put('NO_LAST_WINS', not LAST_WINS, {'rule': 'A71: every list-to-mapping site rejects duplicates (BUILD.md A71 table)',
                                        'partial_after_exception': partial, 'hits': LAST_WINS[:20]})
    unstable = SR.unstable + SN.unstable + SR.verify() + SN.verify()
    put('TREE_STABLE', not unstable, {'rule': 'each file hashed once (stream) and a declared file parsed from bytes whose sha equals it; '
                                              'every recorded file re-hashed at the end', 'partial_after_exception': partial,
                                      'files_recorded': [len(SR.sha), len(SN.sha)], 'changed': unstable[:12]})


def _compare(a, ref, new, tok, tok_doc, tail_on, ro1_req, declared_off, put, extra, hold):
    sel_raw = driver_raw()
    sel_env = driver_env(sel_raw, DRIVER[0])
    new_t = driver_tables(sel_raw, DRIVER[0])
    drv = load_driver()
    TR, TN = Tree(ref), Tree(new)
    SR, SN = Store(ref, 'reference', TR), Store(new, 'new', TN)
    hold.update(SR=SR, SN=SN)
    sr, sn = TR.stages, TN.stages
    entries = declared_entries(a.gate)
    inv_r, inv_n = TR.inventory(), TN.inventory()
    # ---------------- phase 1: every file hashed once (stream), with the stray-uv_tail and cross-run byte scans
    root_r, root_n = str(ref).encode(), str(new).encode()
    for T, S, other in ((TR, SR, root_n), (TN, SN, root_r)):
        for rel in T.files:
            c = T.canon(rel)
            nd = [other]
            if (c.endswith('.json') or c.endswith('.jsonl')) and '/checkpoint/' not in '/' + c:
                nd.append(b'"uv_tail')
            S.hash_scan(T.run / rel, tuple(nd))
    # ---------------- attempt ledger grouping (0446: fullmatch, token format, explicit grouped-key guard before any removal)
    led_r, led_n, lbad = {}, {}, []
    for T, inv, led in ((TR, inv_r, led_r), (TN, inv_n, led_n)):
        seen = {}
        for rel in sorted(inv):
            m = ATTEMPT_RE.fullmatch(rel)
            if not m:
                continue
            key = (m.group(1), m.group(2), m.group(3))
            if key in seen:  # A71[LEDGER]: two raw paths with one grouped key; both named, neither removed
                lbad.append({'kind': 'LEDGER_GROUPED_KEY_COLLISION', 'raw_paths': [seen[key], rel]})
                LAST_WINS.append({'where': 'attempt ledger grouping', 'raw_paths': [seen[key], rel]})
                continue
            seen[key] = rel  # A71[LEDGER]
        for key, rel in sorted(seen.items()):
            led.setdefault(key[0], {}).setdefault(key[1], {})[key[2]] = inv.pop(rel)  # A71[LEDGER]
    led_tokens = []
    for d in sorted(set(led_r) | set(led_n)):
        tr_, tn_ = sorted((led_r.get(d) or {}).items()), sorted((led_n.get(d) or {}).items())
        if len(tr_) != len(tn_):
            lbad.append({'dir': d, 'tokens': [len(tr_), len(tn_)]})
            continue
        for i, ((ta, _), (tb, _)) in enumerate(zip(tr_, tn_)):
            if not (ATTEMPT_TOKEN_RE.fullmatch(ta) and ATTEMPT_TOKEN_RE.fullmatch(tb)):
                lbad.append({'dir': d, 'kind': 'ATTEMPT_TOKEN_FORMAT', 'tokens': [ta, tb], 'format': ATTEMPT_TOKEN_RE.pattern})
                continue
            if ta != tb:
                led_tokens.append([ta, tb, '<ATTEMPT_TOKEN_%s_%d>' % (d.split('/')[1].upper(), i), 'LEDGER_TOKEN'])
    led_files = {str(p) for led in (led_r, led_n) for v in led.values() for kk in v.values() for p in kk.values()}
    # ---------------- BYTES_EQUAL (A74): equal bytes first; a declared file may differ; nothing else
    ref_only = sorted(set(inv_r) - set(inv_n))
    new_only = sorted(set(inv_n) - set(inv_r))
    pats = [(re.compile(p), why) for p, why in DECLARED_NEW_ONLY[a.gate]]
    adm_new, undeclared = {}, []
    for rel in new_only:
        hit = [why for rx, why in pats if rx.fullmatch(rel)]
        (adm_new.setdefault(hit[0], []).append(rel)) if hit else undeclared.append(rel)  # A71[NEW_ONLY_GROUP]
    new_only_decl = {rel for v in adm_new.values() for rel in v}
    both = sorted(set(inv_r) & set(inv_n))
    equal, declared_diff, undeclared_diff, decl_rel = [], [], [], {}
    for rel in both:
        e = declared_entry(entries, rel)
        if e is not None:
            decl_rel[rel] = e  # A71[DECLARED_LIST]
        if SR.sha[str(inv_r[rel])] == SN.sha[str(inv_n[rel])]:
            equal.append(rel)
        elif e is not None and e[0] != 'AMBIGUOUS':
            declared_diff.append(rel)
        else:
            undeclared_diff.append(rel)
    put('BYTES_EQUAL', not undeclared_diff and not ref_only and not undeclared,
        {'rule': 'A74: every file of both trees compared by raw sha256; only the closed DECLARED_DIFFER list may differ (then compared '
                 'semantically); a file on one side only FAILs unless it is a declared new-only or attempt-ledger file',
         'files_both_sides': len(both), 'equal_bytes': len(equal), 'declared_differing': len(declared_diff),
         'declared_differing_by_entry': {i: sum(1 for r in declared_diff if decl_rel[r][0] == i) for i in sorted({decl_rel[r][0] for r in declared_diff})},
         'undeclared_differing': undeclared_diff[:30], 'n_undeclared_differing': len(undeclared_diff),
         'reference_only': ref_only[:20], 'new_only_undeclared': undeclared[:20],
         'new_only_declared': len(new_only_decl), 'attempt_ledger_files': len(led_files)})
    # parse surface: declared both-side files (whatever their bytes), declared new-only files, ledger files
    SR.allow = {str(inv_r[r]) for r in decl_rel} | {p for p in led_files if p.startswith(str(ref) + '/')}
    SN.allow = {str(inv_n[r]) for r in decl_rel} | {str(inv_n[r]) for r in new_only_decl} | {p for p in led_files if p.startswith(str(new) + '/')}
    # ---------------- STAGE_SET (ASCII digits; c2v006 rules)
    extras = DECLARED_EXTRA_STAGES[a.gate]
    on = [x for x in TN.order if x not in extras]
    ord_ok = TR.order == on and not any(x in extras for x in TR.order)
    ex_det = {}
    for x in extras:
        cnt = TN.order.count(x)
        pos_ok = cnt == 1 and ('route_a' not in TN.order or TN.order.index(x) == TN.order.index('route_a') + 1)
        ex_det[x] = {'count': cnt, 'immediately_after_route_a': pos_ok}  # A71[STAGE_KEYED]
        ord_ok = ord_ok and pos_ok
    put('STAGE_SET', not TR.problems and not TN.problems and ord_ok,
        {'reference_problems': TR.problems[:12], 'new_problems': TN.problems[:12], 'order_reference': TR.order, 'order_new': TN.order,
         'order_equal_after_declared_extras': TR.order == on, 'declared_extra_stages': ex_det})
    # ---------------- TOKENS (A73 SF2 / A74): the supplied list must equal the A59 derivation; any defect refuses the comparison
    st_r = SR.json(ref / 'start.json') if SR.has(ref / 'start.json') else Unparseable('no start.json')
    rdrv, rsha, rraw = reference_driver_of(st_r)
    ref_env = driver_env(rraw, rdrv) if rraw is not None else {}
    ok, det = tokens_policy(a.gate, tok, drv, ref_env, sel_env)
    det['reference_driver'] = [rdrv, rsha, rraw is not None]
    if rraw is None:
        ok = False
        det['defects'].append({'kind': 'REFERENCE_DRIVER_NOT_REGISTERED_OR_BYTES_DIFFER', 'driver': [rdrv, rsha]})
    meta = {k: tok_doc.get(k) for k in ('gate', 'driver', 'reference_driver') if k in tok_doc}
    if 'gate' in meta and meta['gate'] != a.gate:
        ok = False
        det['defects'].append({'kind': 'TOKENS_FILE_GATE_MISMATCH', 'file': meta['gate']})
    if 'driver' in meta and meta['driver'] != list(DRIVER):
        ok = False
        det['defects'].append({'kind': 'TOKENS_FILE_DRIVER_MISMATCH', 'file': meta['driver']})
    if 'reference_driver' in meta and meta['reference_driver'] != [rdrv, rsha]:
        ok = False
        det['defects'].append({'kind': 'TOKENS_FILE_REFERENCE_DRIVER_MISMATCH', 'file': meta['reference_driver']})
    put('TOKENS_POLICY', ok, det)
    if not ok:
        rep_kinds = {d.get('kind') for d in det['defects']}
        put('COMPARISON_REFUSED', False, {'why': 'a token defect refuses the comparison (A73 SF2, A74); nothing further was compared',
                                          'defects': sorted(x for x in rep_kinds if x)})
        if 'RECORD_DEFECT_REPEATED_TRIPLE' in rep_kinds:
            put('NO_LAST_WINS', False, {'rule': 'A71', 'hits': LAST_WINS[:20]})
        return
    declared_tok = [[t[0], t[1], t[2], 'DRIVER_TOKEN'] for t in tok]
    auto, auto_rep = auto_custody(a.gate, ref, new, sr, sn, new_t, tuple(drv.UVT_TAIL_KINDS), SR, SN, rraw, declared_tok)
    put('AUTO_CUSTODY', not auto_rep['inadmissible'], auto_rep)
    tok_all = declared_tok + auto + led_tokens
    for t in auto:  # custody raws must be custody forms too (A73 SF2)
        if not (raw_form_ok(t[0]) and raw_form_ok(t[1])):
            auto_rep['inadmissible'].append({'what': 'custody token raw form', 'pair': [t[0][:120], t[1][:120]]})
    pairs, tok_bad, _ = build_tokens(tok_all)
    cls_of = {}
    for t in tok_all:  # A71[TOKEN_CLASS]: (ref, new) -> class; the pair is unique after build_tokens (defects otherwise)
        cls_of.setdefault((t[0], t[1]), t[3])
    labels = sorted({t[2] for t in tok_all})
    markers = NORMALIZER_MARKERS + tuple(labels)
    hold['tok_bad'] = tok_bad
    cm = load_cm()
    # checkpoint record shas for the sha tokens (RA payload / identity); records parsed strictly (declared files)
    ra_names = {'reference': {}, 'new': {}}
    for tag, T, S in (('reference', TR, SR), ('new', TN, SN)):
        for rel in T.files:
            c = T.canon(rel)
            if not re.fullmatch(r'stages/route_a/checkpoint/.*\.json', c):
                continue
            if str(T.run / rel) not in S.allow:
                continue
            body = S.json(T.run / rel)
            if isinstance(body, dict) and not isinstance(body, Unparseable):
                ps, ids = body.get('payload_sha256', ''), body.get('identity_sha256', '')
                if isinstance(ps, str) and SHA_RE.fullmatch(ps):
                    ra_names[tag].setdefault(ps, set()).add('P:' + c)  # A71[HEXMAP]
                if isinstance(ids, str) and SHA_RE.fullmatch(ids):
                    ra_names[tag].setdefault(ids, set()).add('I')  # A71[HEXMAP]
    R = Side(TR, SR, [(r, l, cls_of[(r, n)]) for r, n, l in pairs], markers, ra_names['reference'])
    hold['R'] = R
    N = Side(TN, SN, [(n, l, cls_of[(r, n)]) for r, n, l in pairs], markers, ra_names['new'])
    hold['N'] = N
    extra.update({'auto_tokens_admitted': auto, 'attempt_tokens': led_tokens, 'declared_tokens_n': len(declared_tok)})
    compared = set()
    # ---------------- attempt ledger content
    for d in sorted(set(led_r) & set(led_n)):
        tr_, tn_ = sorted(led_r[d].items()), sorted(led_n[d].items())
        if len(tr_) != len(tn_):
            continue
        for (ta, ka), (tb, kb) in zip(tr_, tn_):
            if set(ka) != set(kb):
                lbad.append({'dir': d, 'kinds': [sorted(ka), sorted(kb)]})
                continue
            for k in sorted(ka):
                rel = '%s/<attempt>.%s.json' % (d, k)
                x, y, mr_, mn_ = pair_norm(R, N, SR.json(ka[k]), SN.json(kb[k]), rel, RECORD_DROP)
                mok, _ = mask_cmp(mr_, mn_, rel)
                if not seq(x, y) or not mok:
                    lbad.append({'dir': d, 'record': k, 'differing': diffs(x, y)[:4], 'masked_key_paths_equal': mok})
    put('ATTEMPT_LEDGER', not lbad, {'directories': {d: [len(led_r.get(d) or {}), len(led_n.get(d) or {})] for d in sorted(set(led_r) | set(led_n))},
                                     'tokens': [t[2] for t in led_tokens], 'differing': lbad[:8]})
    # ---------------- INVENTORY (files, directories, symlinks, special files, canonical collisions)
    dr, dn = set(TR.dinv), set(TN.dinv)
    dpats = [re.compile(p) for p in DECLARED_NEW_ONLY_DIRS[a.gate]]
    d_ref_only = sorted(dr - dn)
    d_new_only = sorted(x for x in dn - dr if not any(p.fullmatch(x) for p in dpats))
    put('INVENTORY', not ref_only and not undeclared and not TR.links and not TN.links and not TR.special and not TN.special
        and not TR.inv_collisions and not TN.inv_collisions and not d_ref_only and not d_new_only,
        {'n_files': [len(TR.files), len(TN.files)], 'n_dirs': [len(TR.dirs), len(TN.dirs)], 'reference_only': ref_only[:20],
         'n_reference_only': len(ref_only), 'new_only_undeclared': undeclared[:20], 'n_new_only_undeclared': len(undeclared),
         'new_only_declared': {k: {'n': len(v), 'first': v[:6]} for k, v in adm_new.items()},
         'directories_reference_only': d_ref_only[:12], 'directories_new_only_undeclared': d_new_only[:12],
         'symlinks': {'reference': TR.links[:10], 'new': TN.links[:10]},
         'special_files': {'reference': [list(x) for x in TR.special[:10]], 'new': [list(x) for x in TN.special[:10]]},
         'canonical_path_collisions': {'reference': TR.inv_collisions[:6], 'new': TN.inv_collisions[:6]}})
    # ---------------- NEW_DRIVER_PIN (A67 N1) and SCRIPT_CUSTODY (A59 raw)
    st_n = SN.json(new / 'start.json')
    rn_raw = SN.json(new / 'result.json')
    rr_raw = SR.json(ref / 'result.json')
    put('NEW_DRIVER_PIN', [st_n.get('driver'), st_n.get('driver_sha256')] == DRIVER and rn_raw.get('driver_sha256') == DRIVER[1]
        and sha_b(driver_raw()) == DRIVER[1],
        {'selected': a.driver, 'pin': list(DRIVER), 'start_json': [st_n.get('driver'), st_n.get('driver_sha256')],
         'result_json_driver_sha256': rn_raw.get('driver_sha256', '<ABSENT>')})
    sc_bad, sc_rows = [], {}
    for name, d in sn.items():
        if not SN.has(d / 'request.json'):
            continue
        q = SN.json(d / 'request.json')
        kind, exp = planned_script(a.gate, name, q, drv)
        got = (q.get('script'), q.get('script_sha256'))
        ok = exp is not None and got == (str(exp[0]), exp[1]) and file_ok(str(exp[0]), exp[1])
        sc_rows[name] = {'kind': kind, 'script_sha256': got[1], 'planned_sha256': exp[1] if exp else None, 'ok': ok}  # A71[STAGE_KEYED]
        if not ok:
            sc_bad.append({'stage': name, 'kind': kind, 'got': list(got), 'planned': [str(exp[0]), exp[1]] if exp else None})
    put('SCRIPT_CUSTODY', not sc_bad, {'rule': 'A59: every new stage runs the driver-planned script for gate %s, hashed from bytes' % a.gate,
                                       'stages': sc_rows, 'violations': sc_bad[:12]})
    # ---------------- route A
    fr, fn = route_a_facts(ref, sr, SR, TR), route_a_facts(new, sn, SN, TN)
    cn_raw, declared_rec, expected_stray, E = None, None, set(), None
    ra_r, ra_n = sr.get('route_a'), sn.get('route_a')
    id_err = {}
    if ra_n is not None and SN.has(ra_n / 'checkpoint/IDENTITY.json'):
        try:
            cn_raw = cm.decode(cm_read(cm, SN, ra_n / 'checkpoint/IDENTITY.json', 'identity')['identity']['caller']['record'])
        except (cm.CheckpointError, KeyError, TypeError, ValueError) as e:  # a malformed record FAILs RA_IDENTITY, never a crash
            id_err.setdefault('new', []).append('%s: %s' % (type(e).__name__, str(e)[:300]))  # A71[ACCUMULATOR]
    if declared_off:
        ok, det, declared_rec, expected_stray, E = check_declared_off(drv, new, fn, cn_raw, SN, TN)
        put('UV_TAIL_DECLARED', ok, det)
    extra['expected_tail_off_request_sha256'] = E
    exp_ra_pins = ra_new_pins(a.gate, drv, N, new)
    if ra_r is not None and ra_n is not None:
        pre = 'stages/route_a/checkpoint/blobs/'
        fr_b = {k[len(pre):]: SR.sha_of(v) for k, v in inv_r.items() if k.startswith(pre)}  # A71[BLOBS]: injective prefix projection
        fn_b = {k[len(pre):]: SN.sha_of(v) for k, v in inv_n.items() if k.startswith(pre)}
        compared.update(pre + k for k in fr_b)
        put('RA_BLOBS', fr_b == fn_b and bool(fr_b), {'n': [len(fr_b), len(fn_b)], 'differing': sorted(set(fr_b) ^ set(fn_b) | {k for k in fr_b if fn_b.get(k) != fr_b[k]})[:10]})
        bad, n = [], 0
        it_re = re.compile(r'stages/route_a/checkpoint/iteration_[^/]+/[^/]+\.json')
        ref_it = sorted(k for k in inv_r if it_re.fullmatch(k))
        new_it = sorted(k for k in inv_n if it_re.fullmatch(k))
        for rel in ref_it:
            n += 1
            compared.add(rel)
            if rel not in inv_n:
                bad.append(rel + ' MISSING')
                continue
            x, y, mr_, mn_ = pair_norm(R, N, SR.json(inv_r[rel]), SN.json(inv_n[rel]), rel, RECORD_DROP)
            mok, _ = mask_cmp(mr_, mn_, rel)
            if not seq(x, y) or not mok:
                bad.append((rel, diffs(x, y)[:3], mok))
        put('RA_RECORDS', not bad and n == len(new_it) and n > 0, {'n': [n, len(new_it)], 'differing': bad[:8]})
        # RA_IDENTITY: the whole identity body; identity_sha256 and caller.sha256 verified as digests of the compared content
        compared.add('stages/route_a/checkpoint/IDENTITY.json')
        idr = idn = None
        for tag, S_, d_ in (('reference', SR, ra_r), ('new', SN, ra_n)):
            try:
                b_ = cm_read(cm, S_, d_ / 'checkpoint/IDENTITY.json', 'identity')
                cm.decode(b_['identity']['caller']['record'])
                if tag == 'reference':
                    idr = b_
                else:
                    idn = b_
            except (cm.CheckpointError, KeyError, TypeError, ValueError) as e:
                id_err.setdefault(tag, []).append('%s: %s' % (type(e).__name__, str(e)[:300]))  # A71[ACCUMULATOR]
    if ra_r is not None and ra_n is not None and (idr is None or idn is None or cn_raw is None):
        put('RA_IDENTITY', False, {'unreadable_checkpoint_identity': id_err or {'new': 'caller record unreadable'}})
        if a.gate in ('Z2', 'Z2_OFF_RO1'):
            put('RA_PINSET', False, {'unreadable_checkpoint_identity': id_err})
    elif ra_r is not None and ra_n is not None:
        dig = {}
        top_r, top_n = sorted(idr), sorted(idn)
        ck_r = sorted(idr['identity'].get('caller') or {})
        for tag, body in (('reference', idr), ('new', idn)):
            ident = body['identity']
            caller = ident.get('caller') or {}
            dig[tag] = {  # a digest that is present must be the checkpoint module's digest of the compared content (CK002 I04) A71[FIXED_KEYS]
                'identity_sha256_is_digest_of_identity': ('identity_sha256' not in body) or cm._sha(cm._canonical(ident)) == body.get('identity_sha256'),
                'caller_sha256_is_digest_of_caller': ('sha256' not in caller) or caller.get('sha256') == cm.digest(cm.decode(caller['record'])),
                'top_level_keys_registered_and_equal_both_sides': top_r == top_n and set(body) <= {'format', 'identity', 'identity_sha256', 'kind', 'payload_sha256'},
                'caller_keys_registered_and_equal_both_sides': set(caller) <= {'record', 'sha256'} and sorted(caller) == ck_r}
        cr = caller_norm(cm.decode(idr['identity']['caller']['record']), tail_on)
        cn = caller_norm(cn_raw, tail_on, declared_rec)
        br = dict(idr['identity'], caller=cr)  # A71[IDENTITY_CALLER]: the encoded caller replaced by its decoded content
        bn = dict(idn['identity'], caller=cn)  # A71[IDENTITY_CALLER]
        x, y, mr_, mn_ = pair_norm(R, N, br, bn, 'stages/route_a/checkpoint/IDENTITY.json')
        mok, _ = mask_cmp(mr_, mn_, 'stages/route_a/checkpoint/IDENTITY.json')
        if a.gate in ('Z2', 'Z2_OFF_RO1'):
            xp, yp = (x.get('caller') or {}).get('code_pins') or {}, (y.get('caller') or {}).get('code_pins') or {}
            r_only, n_only = sorted(set(xp) - set(yp)), sorted(set(yp) - set(xp))
            put('RA_PINSET', not r_only and set(n_only) == set(exp_ra_pins) and all(seq(yp.get(k), v) for k, v in exp_ra_pins.items()),
                {'reference_only': r_only, 'new_only': n_only, 'expected_new_only': sorted(exp_ra_pins),
                 'value_mismatch': sorted(k for k, v in exp_ra_pins.items() if k in yp and not seq(yp[k], v))})
        notes, viol = [], []
        strict_pins({'identity': x}, {'identity': y}, 'IDENTITY', exp_ra_pins, notes, viol)
        dig_ok = all(all(v.values()) for v in dig.values())
        put('RA_IDENTITY', seq(x, y) and not viol and mok and dig_ok,
            {'compared': 'the whole checkpoint identity body (caller decoded; code, controls, environment, fixed_source, format, inputs, '
                         'shapes); identity_sha256 and caller.sha256 verified per side as the checkpoint module digests of that body',
             'differing': diffs(x, y)[:8], 'pin_violations': viol[:8], 'declared_new_only_pins': notes, 'digests': dig,
             'masked_key_paths_equal': mok})
    else:
        put('RA_PRESENT', ra_r is None and ra_n is None and not declared_off and a.gate != 'Z2', {'reference': str(ra_r), 'new': str(ra_n)})
    # ---------------- requests (H3, S1, S2)
    blocks, rc = expected_tail_blocks(a.gate, drv, new, sn, (rn_raw.get('uv_tail') if isinstance(rn_raw, dict) else None), SN)
    if a.gate == 'Z2':
        put('UV_TAIL_RECORD', rc is not None and all(v is True for v in rc.values()), rc)
        ok, det = check_manifest_stage(a.gate, drv, new, sn, SN)
        put('MANIFEST_STAGE', ok, det)
    ok, det = check_requests(a.gate, R, N, sr, sn, blocks)
    put('REQUEST', ok, det)
    compared.update('stages/%s/request.json' % k for k in set(sr) & set(sn) if SR.has(sr[k] / 'request.json') and SN.has(sn[k] / 'request.json'))  # A71[ACCUMULATOR]
    # ---------------- STAGE_RECORDS (result.json stage_records tied to the run's own requests)
    sr_bad, sr_det = [], {}
    has = [isinstance(rr_raw, dict) and 'stage_records' in rr_raw, isinstance(rn_raw, dict) and 'stage_records' in rn_raw]
    if has[0] != has[1]:
        sr_bad.append('stage_records present on one side only')
    elif has[0]:
        per = {}
        for tag, raw, T, S in (('reference', rr_raw, TR, R), ('new', rn_raw, TN, N)):
            recs = raw['stage_records'] if isinstance(raw['stage_records'], list) else []
            names = [r.get('name') if isinstance(r, dict) else None for r in recs]
            with_req = [x for x in T.order if S.store.has(T.stages[x] / 'request.json')]
            if names != with_req:
                sr_bad.append({'side': tag, 'why': 'stage_records names != stage directories with a request, in order', 'records': names, 'stages': with_req})
            per[tag] = {}  # A71[FIXED_KEYS]
            for r in recs:
                if not isinstance(r, dict):
                    sr_bad.append({'side': tag, 'why': 'stage record is not an object'})
                    continue
                nm = r.get('name')
                if nm not in T.stages or not S.store.has(T.stages[nm] / 'request.json'):
                    continue
                if nm in per[tag]:  # A71[STAGE_RECORDS]
                    LAST_WINS.append({'where': 'result.json stage_records', 'side': tag, 'name': nm})
                    sr_bad.append({'side': tag, 'stage': nm, 'why': 'DUPLICATE_STAGE_RECORD_NAME'})
                    continue
                q = S.store.json(T.stages[nm] / 'request.json')
                core = {k: v for k, v in r.items() if k not in STAGE_RECORD_EXTRA}
                if not seq(core, q) or not set(r) - set(core) <= STAGE_RECORD_EXTRA:
                    sr_bad.append({'side': tag, 'stage': nm, 'why': 'record != own request.json', 'differing': diffs(q, core)[:4]})
                with S.at_file('result.json'):
                    per[tag][nm] = S.norm({k: v for k, v in r.items() if k in STAGE_RECORD_EXTRA}, at='result.json/stage_records/%s' % nm)  # A71[STAGE_RECORDS]
        for nm in sorted(set(per['reference']) & set(per['new'])):
            if not seq(per['reference'][nm], per['new'][nm]):
                sr_bad.append({'stage': nm, 'why': 'record execution fields differ', 'differing': diffs(per['reference'][nm], per['new'][nm])[:4]})
        sr_det['n'] = [len(rr_raw['stage_records']), len(rn_raw['stage_records'])]
    put('STAGE_RECORDS', not sr_bad, dict(sr_det, present=has, violations=sr_bad[:10]))  # A71[FIXED_KEYS]
    # ---------------- declared rules (B2): per canonical file
    spec_rules = [{'path': ('label',), 'rule': 'MASK', 'why': 'spec label (custody text)'}]
    if a.gate == 'Z2_OFF_RO1':
        spec_rules.append({'path': ('numerics', 'route_a', 'ro1_workers'), 'rule': 'NEW_ONLY', 'value': True, 'why': 'the Z2_OFF_RO1 spec leaf (A47 I6)'})

    def under(prefix, rules):
        return [dict(r, path=prefix + r['path']) for r in rules]
    res_rules = under(('normalized_spec',), spec_rules) + [
        {'path': ('stage_records',), 'rule': 'COVERED', 'check': 'STAGE_RECORDS + REQUEST', 'why': 'request copies plus execution fields'},
        {'path': ('route_a_outcome', 'ro1'), 'rule': 'NEW_ONLY_OR_EQUAL', 'keys': RO1_KEYS, 'why': 'RO1 block (checked by RO1; exact key set, SF1)'},
        {'path': ('identity', 'route_a', 'outcome', 'ro1'), 'rule': 'NEW_ONLY_OR_EQUAL', 'keys': RO1_KEYS,
         'why': 'RO1 block (checked by RO1; equals route_a_outcome.ro1; exact key set, SF1)'}]
    if a.gate in IMPL_KIND_PAIRS:
        res_rules.append({'path': ('identity', 'route_a', 'implementation', 'kind'), 'rule': 'PAIR', 'pairs': IMPL_KIND_PAIRS[a.gate],
                          'why': 'driver L2872-2878 implementation kind'})
    if a.gate == 'Z2_OFF_RO1':
        res_rules.append({'path': ('identity', 'route_a', 'implementation', 'ro1_workers'), 'rule': 'NEW_ONLY', 'value': True, 'why': 'driver L2879'})
    file_rules = {'inputs/call_spec.json': spec_rules, 'start.json': under(('normalized_spec',), spec_rules), 'result.json': res_rules}
    if declared_off and declared_rec is not None:
        with N.at_file('stages/route_a/attempt_000/start.json'):
            d2 = N.norm(declared_rec, at='<declared D2 record>')
        file_rules['stages/route_a/attempt_000/start.json'] = [{'path': ('uv_tail',), 'rule': 'NEW_ONLY', 'value': d2,
                                                                 'why': 'D2 declared tail-off record (driver R5)'}]
    sp_ok, sp_rev = static_pin_verifier(N)
    spins = (st_n.get('static_pins') or {}) if isinstance(st_n.get('static_pins'), dict) else {}
    for k, v in spins.items():
        nk = N.s(k, 'start.json/static_pins/<key>')
        if nk in sp_rev:  # A71[STATIC_PINS]
            LAST_WINS.append({'where': 'start.json static_pins normalized key', 'normalized_key': nk, 'raw_keys': [sp_rev[nk][0], k]})
            sp_rev[nk] = Collided([sp_rev[nk][0], k])
            continue
        sp_rev[nk] = (k, v)  # A71[STATIC_PINS]
    # ---------------- RESULT
    x, y, mr_, mn_ = pair_norm(R, N, rr_raw, rn_raw, 'result.json')
    ro1_cross = True
    h1, v1 = _get(y, ('route_a_outcome', 'ro1'))
    h2, v2 = _get(y, ('identity', 'route_a', 'outcome', 'ro1'))
    if h1 and h2:
        ro1_cross = seq(v1, v2)
    notes, viol = [], []
    strict_pins(x, y, 'result.json', {}, notes, viol)
    with N.at_file('result.json'):
        x2, y2, rep_res, bad_res = apply_declared(x, y, res_rules, fire=N._fire)
    mok, mdet = mask_cmp(mr_, mn_, 'result.json', rep_res)
    put('RESULT', seq(x2, y2) and not viol and not bad_res and ro1_cross and rr_raw.get('status') == 'COMPLETED' and mok,
        {'differing': diffs(x2, y2)[:12], 'declared_rules_applied': rep_res, 'rule_violations': bad_res, 'pin_violations': viol[:6],
         'ro1_blocks_equal': ro1_cross, 'status': [rr_raw.get('status'), rn_raw.get('status')], 'masked_key_paths_equal': mok,
         'masked_key_paths': mdet if not mok else None})
    compared.add('result.json')
    # ---------------- every other both-side file (S3): equal bytes, or a declared file compared semantically, or a FAIL
    groups = {'FILES_INPUTS': [], 'FILES_TOP': [], 'FILES_ROUTE_A': [], 'STAGES': []}
    counts = {g: 0 for g in groups}
    by = {g: {'equal_bytes': 0, 'declared_semantic': 0} for g in groups}
    applied, pin_notes = [], []
    for rel in both:
        if rel in compared:
            continue
        p, q = inv_r[rel], inv_n[rel]
        if rel.startswith('inputs/'):
            g = 'FILES_INPUTS'
        elif '/' not in rel:
            g = 'FILES_TOP'
        elif rel.startswith('stages/route_a/'):
            g = 'FILES_ROUTE_A'
        else:
            g = 'STAGES'
        counts[g] += 1
        compared.add(rel)
        e = decl_rel.get(rel)
        if e is None or e[0] == 'AMBIGUOUS':
            if SR.sha[str(p)] == SN.sha[str(q)]:
                by[g]['equal_bytes'] += 1
            else:
                groups[g].append((rel, 'UNDECLARED_BYTE_DIFFERENCE', [SR.sha[str(p)][:16], SN.sha[str(q)][:16]]))
            continue
        by[g]['declared_semantic'] += 1
        suf = Path(rel).suffix
        if suf in ('.npz', '.npy'):
            ka, va = SR.array(p)
            kb, vb = SN.array(q)
            if ka == 'invalid' or kb == 'invalid' or ka != kb or va != vb:
                groups[g].append((rel, 'ARRAY_CONTENT'))
        elif suf == '.jsonl':
            if rel == 'progress.jsonl':
                ok, det = compare_jsonl(rel, p, q, R, N, extra_mask=('elapsed',), drop_new_stage=DECLARED_EXTRA_STAGES[a.gate])
            else:
                ok, det = compare_jsonl(rel, p, q, R, N)
            if not ok:
                groups[g].append(det)
        elif suf == '.json':
            if rel == 'start.json':
                pin_allow = sp_ok
            elif rel.startswith('stages/route_a/'):
                pin_allow = exp_ra_pins
            else:
                pin_allow = {}
            ok, det, rep, pn = compare_json_file(rel, p, q, R, N, file_rules.get(rel, []), pin_allow)
            if rep:
                applied.append({'file': rel, 'rules': rep})
            if pn:
                pin_notes.append(pn)
            if not ok:
                groups[g].append(det)
        else:
            groups[g].append((rel, 'DECLARED_ENTRY_FOR_A_NON_JSON_FILE'))
    for g, bad in groups.items():
        det = {'compared': counts[g], 'by_kind': by[g], 'differing': bad[:12], 'n_differing': len(bad)}
        if g == 'FILES_TOP':
            det.update({'declared_rules_applied': applied, 'declared_new_only_pins': pin_notes[:20]})
        put(g, not bad, det)
    # new-only declared files: strictly parsed (no counterpart)
    for rel in sorted(new_only_decl):
        q = inv_n[rel]
        if rel.endswith('.json'):
            SN.json(q)
        elif rel.endswith('.jsonl'):
            SN.jsonl(q)
        elif rel.endswith('.npz') or rel.endswith('.npy'):
            SN.array(q)
    if not tail_on:
        SR.declared = SN.declared = set(decl_rel) | new_only_decl
        sr_, sn_ = stray_uv_tail(TR, SR), stray_uv_tail(TN, SN)
        new_at = {s['at'] for s in sn_}
        admitted = sorted(new_at & expected_stray)
        undeclared_s = [s for s in sn_ if s['at'] not in expected_stray]
        put('STRAY_UV_TAIL', not sr_ and not undeclared_s and new_at >= expected_stray,
            {'reference': sr_[:12], 'new_undeclared': undeclared_s[:12], 'new_admitted_declared': admitted,
             'declared_missing': sorted(expected_stray - new_at)})
    if ro1_req == 'ARMED':
        n_workers, worker = ro1_expectations(drv, fn)
        ok, det = check_ro1_armed(ro1_block(rn_raw), worker[1], drv.RO1_ROUTE_A['binding'][1])
        det['route_a_column_workers'] = n_workers
        put('RO1', ok, det)
        ok, det = check_custody(drv, tok_all, fr, fn, worker)
        put('RO1_CUSTODY', ok, det)
    elif ro1_req == 'ARMED_BLOCK_ONLY':
        ro1 = ro1_block(rn_raw)
        put('RO1', isinstance(ro1, dict) and set(ro1) == RO1_KEYS and ro1.get('armed') is True and ro1.get('fired') is False, {'new_ro1': ro1})
    elif ro1_req == 'UNARMED':
        ok, det = check_ro1_unarmed(ro1_block(rn_raw))
        put('RO1', ok, det)
    # ---------------- cross-run byte scan: a NEW file naming the reference run root (a copied record) FAILs
    cross = sorted(TN.canon(os.path.relpath(k, new)) for k, v in SN.hits.items() if root_r in v)
    cross_r = sorted(TR.canon(os.path.relpath(k, ref)) for k, v in SR.hits.items() if root_n in v)
    put('CROSS_RUN_REFERENCE', not cross and not cross_r, {'rule': 'no file of one run contains the other run root (byte scan)',
                                                          'new_files_naming_reference_root': cross[:12], 'reference_files_naming_new_root': cross_r[:12]})
    # ---------------- declared classes: each normalization class fires only in files whose entry allows it
    allowed = {}
    for rel, e in decl_rel.items():
        allowed[rel] = set(e[1])  # A71[DECLARED_LIST]
    led_rels = {'%s/<attempt>.%s.json' % (d, k) for d in set(led_r) | set(led_n) for k in ('start', 'end')}  # A71[LEDGER]
    cls_bad = []
    for S in (R, N):
        for rel, fired in sorted(S.fired.items()):
            allow = set(LEDGER_CLASSES) if rel in led_rels else allowed.get(rel)
            if allow is None:
                cls_bad.append({'side': S.store.tag, 'file': rel, 'classes': sorted(fired), 'why': 'NORMALIZED_FILE_WITHOUT_DECLARED_ENTRY'})
            elif fired - allow:
                cls_bad.append({'side': S.store.tag, 'file': rel, 'entry': decl_rel[rel][0] if rel in decl_rel else 'LEDGER',
                                'classes_not_allowed': sorted(fired - allow)})
    put('DECLARED_CLASSES', not cls_bad, {'rule': 'a normalization class may fire only in a file whose declared entry allows it',
                                          'violations': cls_bad[:16], 'n': len(cls_bad)})
    # ---------------- coverage (a gate check since c2v005): every both-side file compared (no log is skipped in c2v007)
    unc = sorted(x for x in both if x not in compared)
    put('COVERAGE', not unc, {'files_both_sides': len(both), 'not_compared': unc[:20], 'new_only_declared_parsed': len(new_only_decl),
                              'note': 'every both-side file is compared: equal bytes, or a declared file compared semantically'})
    _strict_puts(put, hold)
    extra['tokens_fired'] = {'reference': R.fired_tok, 'new': N.fired_tok}
    agg = {}
    for S in (R, N):
        for rel, fired in S.fired.items():
            eid = decl_rel[rel][0] if rel in decl_rel else ('LEDGER' if rel in led_rels else 'NONE')
            agg.setdefault(eid, set()).update(fired)  # A71[ACCUMULATOR]
    extra['classes_fired_by_entry'] = {k: sorted(v) for k, v in sorted(agg.items())}
    extra['roundtrip'] = {'reference': [R.n_roundtrip, R.n_strings], 'new': [N.n_roundtrip, N.n_strings]}


if __name__ == '__main__':
    raise SystemExit(main())
