"""Run-output identity comparator for the V007 identity gates, c2v006 (Claude2 tail_scheme_impl_c2/gates_v006).
c2v006 = successor of gates_v005/run_identity_compare_c2v005.py (6f656c68) for root V005 addendum A69/A70 (Codex2 0436/0438
cross-lineage review of c2v005: review_comparator_c2v005_cx2/REVIEW.md 9317cd0d) and A71 (no last-wins anywhere).  Every
c2v004 / c2v005 check is kept unchanged in meaning (nothing is relaxed).  Changes:
  CX2-V5-B1 NORM_INJECTIVE.  Normalization must be injective on each side.  Side.norm rejects, at every object level, two raw
     keys that normalize to the same key (the check FAILs naming both raw keys and the object path; the normalized value becomes
     a COLLIDED sentinel that never compares equal; never last-wins).  Also FAIL: a raw key or string that already contains a
     normalizer output text (<RUN>, <JSONFILE:, <RA_PAYLOAD:, <RA_IDENTITY_SHA, NPZ:, NPZ_INVALID:, or any token label in use),
     two distinct 64-hex values mapped to one hexmap token (NPZ content tokens excepted: content equivalence is declared), and
     a token raw string paired with two different counterparts or a token label used for two pairs.  A sha that names several
     files maps to the sorted join of all their tokens (not last-wins).  The run root is replaced only when the next character
     is not [A-Za-z0-9_-] (a longer sibling name such as RUN_V0012 is not the run; RUN.receipt.json still normalizes).
  CX2-V5-S2 STRICT_PARSE.  Every JSON file and JSONL line is parsed with object_pairs_hook: a duplicate member FAILs naming the
     key and both values.  Non-UTF-8 or unparseable JSON FAILs.  The parsed value of a defective file is an UNPARSEABLE sentinel
     that never compares equal.  The checkpoint IDENTITY.json is read from the same bytes with the checkpoint module's own
     canonical-form rule (c2v003 _read) and cm.decode (which itself refuses duplicate record keys).
  CX2-V5-S3 STRICT_PARSE.  NPZ archives are opened from their bytes with zipfile; every central-directory member is listed:
     a duplicate member name, a member that is not NAME.npy, or two members with one logical key FAIL (naming both); every
     member is read by its own ZipInfo (never by name, which is last-wins in zipfile).
  CX2-V5-S1 + CX2-V5-N1 ARRAY_POLICY (declared): the identity of an array (a .npy file, or one .npz member) is the tuple
     (header descr exactly as written, dtype.str, itemsize, structured fields as (name, offset, format, shape) in order,
     shape, fortran_order from the header, sha256 of the logical C-order value bytes, sha256 of any trailing bytes).
     STORAGE ORDER IS PART OF IDENTITY for .npy AND .npz alike (c2v004 H2 compared it for .npy; it is not relaxed and is
     extended to .npz members).  Compression and member order inside an .npz are not part of identity.
  CX2-V5-S4 TREE_STABLE + single read.  Each run file is read once into memory; its sha256 and its parsed content come from
     those same bytes (JSON / NPZ / NPY parsed values and shas are cached; JSONL and raw files are hashed from the bytes that
     are compared).  The checkpoint module and the drivers are executed / AST-read from the same bytes that were hashed.  At the
     end every recorded file is re-hashed: any change between the read and the end FAILs TREE_STABLE.
  A71 NO_LAST_WINS: every list-to-mapping site has a guard: argv flags read by name (a repeated flag reads as DUPLICATE and
     FAILs), stage_records names, normalized pin keys (static pins, declared route-A pins), canonical inventory paths, driver
     table dict literals (AST).
  Own hardening: decoded numpy arrays keep dtype and shape in the normalized form (NDV), tuples stay tuples; a comparator
     exception writes a FAIL report (COMPARATOR_EXCEPTION) instead of crashing.
INERT on import; reads two completed run directories and pinned code (read-only); writes ONE report (exclusive create).

  python3 -I -B run_identity_compare_c2v006.py --gate GATE --driver r4|r5 --reference REF_RUN --new NEW_RUN --tokens T.json --out R.json
"""
import argparse
import ast
import copy
import hashlib
import io
import json
import os
import re
import struct
import sys
import traceback
import types
import zipfile
from pathlib import Path

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
REFERENCE_DRIVERS = {
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py':
        'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py':
        '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py':
        '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6',
    DRIVERS['r4'][0]: DRIVERS['r4'][1],
    DRIVERS['r5'][0]: DRIVERS['r5'][1],
}
MASK_KEYS_BASE = {'elapsed_seconds', 'ended_unix_ns', 'started_unix_ns', 'utc', 'pid'}
TAIL_KEYS = {'uv_tail', 'uv_tail_tap'}
MASK_KEYS = set(MASK_KEYS_BASE)  # set by main() from --gate
GATES = {'Z2': (True, 'ARMED', False), 'Z2_OFF_RO1': (False, 'ARMED', True), 'Z2_OFF': (False, 'OPTIONAL', False),
         'B0P_RERUN': (False, 'UNARMED', False)}
RETIRED_GATES = {'B0PRIME_RERUN': 'gate B0PRIME_RERUN is renamed B0P_RERUN in c2v003 (root V005 A52 ruling 1: ro1 armed false, fired false)'}
OFF_REQUEST_NAME = 'uv_tail_route_a_request_tail_off_ro1.json'
RECORD_DROP = {'attempt', 'payload_sha256', 'identity_sha256', 'iteration_start_sha256', 'checkpoint_identity_sha256'}
HEX = re.compile(r'[0-9a-f]{64}')
LOG_NAMES = ('stdout.txt', 'stderr.txt')
ATTEMPT_RE = re.compile(r'^(stages/[^/]+/checkpoint/attempts)/([^/]+)\.(start|end)\.json$')
STAGE_RE = re.compile(r'^(\d\d)_([a-z0-9_]+)$')
TEST_ONLY = 'NONE_TEST_ONLY'  # driver L349 UVT_TEST_ONLY
TAIL_FLAGS = ('--uv-tail-config', '--uv-tail-config-sha256', '--uv-tail-admit-test-only', '--route-a-tail-manifest',
              '--route-a-tail-manifest-sha256', '--uv-tail-truncation', '--uv-tail-source-rotation-directory', '--eps-certificate',
              '--eps-certificate-sha256', '--lo-certificate', '--lo-certificate-sha256', '--uv-tail-sidecar-directory')
STAGE_RECORD_EXTRA = {'elapsed_seconds', 'executed', 'exit_code', 'request_path', 'request_sha256', 'stage_dir'}
NAME_KIND = {'route_a': 'route_a', 'route_a_tail_manifest': 'route_a_tail_manifest', 'reference': 'reference', 'body': 'body',
             'offset': 'offset'}
NORMALIZER_MARKERS = ('<RUN>', '<JSONFILE:', '<RA_PAYLOAD:', '<RA_IDENTITY_SHA', 'NPZ:', 'NPZ_INVALID:', '<COLLIDED', '<UNPARSEABLE')
ARRAY_POLICY = ('ARRAY_IDENTITY_C2V006: an array (a .npy file or one .npz member) is identical iff (header descr as written, dtype.str, '
                'itemsize, structured fields (name, offset, format, shape) in order, shape, header fortran_order, sha256 of the logical '
                'C-order value bytes, sha256 of trailing bytes) are equal.  Storage order (fortran_order) IS part of identity for .npy '
                'and .npz alike.  NPZ compression and member order are not.  allow_pickle is False (object arrays are unparseable).')
# H1: declared new-only files per gate (canonical relative paths), with their source.
DECLARED_NEW_ONLY = {
    'Z2': [
        (r'inputs/uv_tail_config\.json', 'driver L1091 ctx.write_input(uv_tail_config.json)'),
        (r'inputs/uv_tail_route_a_request\.json', 'driver L1092 ctx.write_input(uv_tail_route_a_request.json)'),
        (r'stages/route_a/uv_tail_sidecar/(SIDECAR_IDENTITY\.json|iteration_\d{4}\.json|elements_\d{4}\.npz|finish_\d{3,4}\.json)',
         'driver L2845 --uv-tail-sidecar-directory; written by the driver AUX_UVT controller'),
        (r'stages/route_a_tail_manifest/(request\.json|stdout\.txt|stderr\.txt)', 'driver L2919-2941 (stage route_a_tail_manifest)'),
        (r'stages/route_a_tail_manifest/manifest/(ROUTE_A_TAIL_MANIFEST\.json|finish\.json|route_a_tail_state\.npz|route_a_gas_it_roster\.npz)',
         'driver AUX_UVT manifest_writer outputs'),
    ],
    'Z2_OFF_RO1': [(r'inputs/' + re.escape(OFF_REQUEST_NAME), 'driver L2847 ctx.write_input (D1)')],
    'Z2_OFF': [],
    'B0P_RERUN': [],
}
DECLARED_EXTRA_STAGES = {'Z2': ('route_a_tail_manifest',), 'Z2_OFF_RO1': (), 'Z2_OFF': (), 'B0P_RERUN': ()}
TABLE_NAMES = ('SCRIPTS', 'AUX', 'PARALLEL_ROUTE_A', 'RO1_ROUTE_A', 'SCRIPTS_UVT', 'AUX_UVT', 'NODES_ROUTE_A', 'SCRIPTS_UVT_NODES')
PIN_DICTS = ('code_pins', 'input_pins', 'dependency_pins', 'source_pins', 'static_pins', 'pins', 'module_pins')
IMPL_KIND_PAIRS = {  # driver L2872-2878: route-A implementation kind (reference kind -> new kind) per gate
    'Z2': (('PARALLEL_C2V001', 'UVTAIL_RO1_PARALLEL_C2V001'), ('REVIEWED_SERIAL', 'UVTAIL_RO1_SERIAL_C2V001')),
    'Z2_OFF_RO1': (('PARALLEL_C2V001', 'TAIL_OFF_RO1_PARALLEL_C2V010R4'), ('REVIEWED_SERIAL', 'TAIL_OFF_RO1_SERIAL_C2V010R4')),
}
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
    """A decoded numpy array / scalar in normalized form: dtype and shape kept (own hardening)."""
    def __init__(self, dtype_str, shape, values):
        self.dtype_str, self.shape, self.values = dtype_str, shape, values

    def __repr__(self):
        return 'NDV(%s,%s,%s)' % (self.dtype_str, self.shape, str(self.values)[:80])
    __str__ = __repr__


# ---------------------------------------------------------------- strict JSON (CX2-V5-S2)
class DuplicateKey(ValueError):
    pass


def _pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise DuplicateKey('DUPLICATE_JSON_KEY %r: first %s, second %s' % (k, _show(d[k]), _show(v)))
        d[k] = v
    return d


def jloads(b):
    return json.loads(b.decode('utf-8') if isinstance(b, (bytes, bytearray)) else b, object_pairs_hook=_pairs)


# ---------------------------------------------------------------- arrays (CX2-V5-S1, S3, N1)
def _npy_header(b):
    import numpy as np
    fp = io.BytesIO(b)
    major, minor = np.lib.format.read_magic(fp)
    if (major, minor) == (1, 0):
        hl = struct.unpack('<H', fp.read(2))[0]
        enc = 'latin1'
    elif (major, minor) in ((2, 0), (3, 0)):
        hl = struct.unpack('<I', fp.read(4))[0]
        enc = 'latin1' if major == 2 else 'utf8'
    else:
        raise ValueError('NPY_VERSION %s.%s' % (major, minor))
    hdr = fp.read(hl)
    if len(hdr) != hl:
        raise ValueError('NPY_HEADER_TRUNCATED')
    d = ast.literal_eval(hdr.decode(enc))
    if not isinstance(d, dict) or sorted(d) != ['descr', 'fortran_order', 'shape']:
        raise ValueError('NPY_HEADER_KEYS %r' % (sorted(d) if isinstance(d, dict) else type(d).__name__))
    return d


def npy_identity_bytes(b):
    """ARRAY_POLICY identity of one .npy payload (bytes)."""
    import numpy as np
    d = _npy_header(b)
    fp = io.BytesIO(b)
    a = np.lib.format.read_array(fp, allow_pickle=False)
    rest = b[fp.tell():]
    dt = a.dtype
    fields = None
    if dt.names is not None:
        fields = [[n, int(dt.fields[n][1]), dt.fields[n][0].str, list(dt.fields[n][0].shape)] for n in dt.names]
    return {'descr': repr(d['descr']), 'dtype_str': dt.str, 'itemsize': int(dt.itemsize), 'fields': fields,
            'shape': [int(x) for x in d['shape']], 'fortran_order': bool(d['fortran_order']),
            'values_sha256': sha_b(np.ascontiguousarray(a).tobytes()), 'trailing_sha256': sha_b(rest) if rest else None}


def npz_identity_bytes(b):
    """{logical key: identity} of an .npz payload; raises ValueError on duplicate / non-.npy members (named)."""
    z = zipfile.ZipFile(io.BytesIO(b))
    infos = z.infolist()
    seen, keys, out, probs = {}, {}, {}, []
    for i, info in enumerate(infos):
        n = info.filename
        if n in seen:
            probs.append('DUPLICATE_NPZ_MEMBER %r (central-directory entries %d and %d)' % (n, seen[n], i))
            continue
        seen[n] = i
        if not n.endswith('.npy') or n.endswith('/'):
            probs.append('NPZ_MEMBER_NOT_NPY %r (entry %d)' % (n, i))
            continue
        k = n[:-4]
        if k in keys:
            probs.append('DUPLICATE_NPZ_LOGICAL_KEY %r (members %r and %r)' % (k, keys[k], n))
            continue
        keys[k] = n
        out[k] = npy_identity_bytes(z.read(info))
    if probs:
        raise ValueError('; '.join(probs))
    return out


def npz_digest(members):
    return sha_b(json.dumps(sorted(members.items()), sort_keys=True).encode())


# ---------------------------------------------------------------- one-read file store (CX2-V5-S4)
class Store:
    """Every run file is read once; its sha and parsed value come from the same bytes.  JSON / NPZ / NPY values are cached.
    A file read again (JSONL / raw compare / scan) is checked against the first sha; verify() re-hashes everything at the end."""

    def __init__(self, root, tag):
        self.root, self.tag = Path(root), tag
        self.sha, self.unstable, self.problems = {}, [], []
        self._json, self._arr, self._raw = {}, {}, {}

    def _record(self, p, h):
        k = str(p)
        if k in self.sha and self.sha[k] != h:
            self.unstable.append({'side': self.tag, 'file': k, 'first_sha256': self.sha[k], 'later_sha256': h})
        self.sha.setdefault(k, h)

    def rel(self, p):
        try:
            return str(Path(p).relative_to(self.root))
        except ValueError:
            return str(p)

    def read(self, p):
        with open(p, 'rb') as f:
            b = f.read()
        self._record(p, sha_b(b))
        return b

    def raw(self, p):
        k = str(p)
        return self._raw[k] if k in self._raw else self.read(p)

    def sha_of(self, p):
        k = str(p)
        if k in self.sha:
            return self.sha[k]
        h = sha_file(p)
        self._record(p, h)
        return h

    def json(self, p):
        k = str(p)
        if k not in self._json:
            b = self.read(p)
            if '/checkpoint/' in k:  # small checkpoint records: the raw bytes are kept for cm_read (same single read)
                self._raw[k] = b
            try:
                self._json[k] = jloads(b)
            except (ValueError, UnicodeDecodeError) as e:
                self.problems.append({'side': self.tag, 'file': self.rel(p), 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
                self._json[k] = Unparseable('%s %s' % (self.rel(p), e))
        return self._json[k]

    def jsonl(self, p):
        out = []
        for i, line in enumerate(self.read(p).split(b'\n')):
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
            b = self.read(p)
            try:
                self._arr[k] = ('npz', npz_identity_bytes(b)) if k.endswith('.npz') else ('npy', npy_identity_bytes(b))
            except Exception as e:  # zipfile.BadZipFile, ValueError, OSError from numpy parsing
                self.problems.append({'side': self.tag, 'file': self.rel(p), 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
                self._arr[k] = ('invalid', '%s %s' % (type(e).__name__, str(e)[:200]))
        return self._arr[k]

    def scan(self, p, needle):
        """Byte scan (stray uv_tail in JSONL) hashed from the scanned bytes."""
        h, hit, tail = hashlib.sha256(), False, b''
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 22), b''):
                h.update(b)
                if not hit and needle in tail + b:
                    hit = True
                tail = b[-16:]
        self._record(p, h.hexdigest())
        return hit

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
    """CX2-V5-S4: hash and execute the checkpoint module from one read of its bytes."""
    raw = Path(CKPT[0]).read_bytes()
    if sha_b(raw) != CKPT[1]:
        raise SystemExit('checkpoint module pin')
    m = types.ModuleType('ckpt_cmp_c2v006')
    m.__file__ = CKPT[0]
    exec(compile(raw, CKPT[0], 'exec'), m.__dict__)
    return m


def driver_raw():
    """The selected driver's bytes, read once per selection and verified against the pin (CX2-V5-S4)."""
    if DRIVER_RAW[0] is None or DRIVER_RAW[1] != DRIVER[0]:
        DRIVER_RAW[0], DRIVER_RAW[1] = Path(DRIVER[0]).read_bytes(), DRIVER[0]
    if sha_b(DRIVER_RAW[0]) != DRIVER[1]:
        raise SystemExit('driver pin')
    return DRIVER_RAW[0]


def load_driver():
    """The selected pinned driver, executed from the verified bytes (module body: constants and defs only)."""
    raw = driver_raw()
    m = types.ModuleType('v010_cmp_c2v006')
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
            if kk in out:  # A71: a duplicate key in a driver dict literal is never resolved last-wins here
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


def driver_tables(raw, path=None):
    """Tables from the given (already verified) source bytes; the comparator never re-reads a hashed file.  A bare path
    (external harnesses, c2v005 call form) is read once here."""
    if path is None and isinstance(raw, (str, Path)) and not isinstance(raw, bytes) and Path(raw).is_file():
        path, raw = str(raw), Path(raw).read_bytes()
    tree = ast.parse(raw.decode('utf-8') if isinstance(raw, bytes) else raw, filename=str(path or '<driver>'))
    env = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            try:
                env[st.targets[0].id] = _ev(st.value, env)
            except (_Unsafe, KeyError, TypeError):
                continue
    out = {}
    for t in TABLE_NAMES:
        v = env.get(t)
        if isinstance(v, dict):
            out[t] = {k: (str(x[0]), x[1]) for k, x in v.items() if isinstance(x, tuple) and len(x) == 2 and isinstance(x[1], str)}
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
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((path + '/' + k, 'ONLY_' + ('NEW' if k in b else 'REF')))
            else:
                diffs(a[k], b[k], path + '/' + k, out, limit)
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
        for k, v in zip(argv[::2], argv[1::2]):
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


# ---------------------------------------------------------------- B1: the run tree by real path
class Tree:
    """Every file / symlink of a run by its real relative path, and the stage directory table."""

    def __init__(self, run):
        self.run = Path(run)
        self.files, self.links = [], []
        for dp, dns, fns in os.walk(self.run, followlinks=False):
            for n in list(dns):
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    self.links.append(os.path.relpath(p, self.run))
                    dns.remove(n)
            for n in fns:
                p = os.path.join(dp, n)
                (self.links if os.path.islink(p) else self.files).append(os.path.relpath(p, self.run))
        self.files.sort()
        self.links.sort()
        self.problems, self.order, self.dir2name, self.stages = [], [], {}, {}
        sd = self.run / 'stages'
        if sd.is_symlink():
            self.problems.append(('stages', 'SYMLINK'))
        elif sd.is_dir():
            names, nums, ok = {}, {}, []
            for e in sorted(os.listdir(sd)):
                p = sd / e
                m = STAGE_RE.match(e)
                if p.is_symlink() or not p.is_dir() or not m:
                    self.problems.append(('stages/' + e, 'NOT_A_NN_NAME_STAGE_DIRECTORY'))
                    continue
                names.setdefault(m.group(2), []).append(e)
                nums.setdefault(m.group(1), []).append(e)
                ok.append((m.group(1), m.group(2), e))
            dup_names = {n for n, l in names.items() if len(l) > 1}
            dup_nums = {n for n, l in nums.items() if len(l) > 1}
            for n in sorted(dup_names):
                self.problems.append((['stages/' + x for x in names[n]], 'DUPLICATE_STAGE_NAME'))
            for n in sorted(dup_nums):
                self.problems.append((['stages/' + x for x in nums[n]], 'DUPLICATE_STAGE_NUMBER'))
            for num, name, e in sorted(ok):
                if name in dup_names or num in dup_nums:
                    continue
                self.order.append(name)
                self.dir2name[e] = name
                self.stages[name] = sd / e
        self.inv, self.inv_collisions = {}, []
        for r in self.files:  # A71: the canonical inventory never keeps one of two colliding raw paths
            c = self.canon(r)
            if c in self.inv:
                self.inv_collisions.append({'canonical': c, 'raw_paths': [str(self.inv[c].relative_to(self.run)), r]})
                LAST_WINS.append({'where': 'inventory canonical path', 'canonical': c, 'raw_paths': [str(self.inv[c].relative_to(self.run)), r]})
                continue
            self.inv[c] = self.run / r

    def canon(self, rel):
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0] == 'stages' and parts[1] in self.dir2name:
            return '/'.join(['stages', self.dir2name[parts[1]]] + parts[2:])
        return rel

    def inventory(self):
        return dict(self.inv)


class Side:
    def __init__(self, tree, store, tokens, markers):
        self.run = tree.run
        self.store = store
        self.tokens = sorted(tokens, key=lambda t: -len(t[0]))
        self.markers = tuple(markers)
        self.collisions = []
        self.fired = {}
        self.run_re = re.compile(re.escape(str(self.run)) + r'(?=/|$|[^A-Za-z0-9_\-])')  # boundary: not a longer sibling name
        cand = {}  # sha -> set of tokens (CX2-V5-B1: never last-wins; joined)
        for rel in tree.files:
            p = self.run / rel
            if rel.endswith('.npz'):
                kind, v = store.array(p)
                tok = 'NPZ:' + npz_digest(v) if kind == 'npz' else 'NPZ_INVALID:' + store.sha_of(p)
                cand.setdefault(store.sha_of(p), set()).add(tok)
            elif rel.endswith('.json'):
                store.json(p)
                cand.setdefault(store.sha_of(p), set()).add('<JSONFILE:%s>' % re.sub(r'^stages/\d\d_', 'stages/NN_', rel))
            elif rel.endswith('.npy') and not re.match(r'^stages/\d\d_route_a/checkpoint/blobs/', rel):
                store.array(p)  # checkpoint blobs are compared by their raw bytes (RA_BLOBS), never parsed
        for rel in tree.files:
            if not re.match(r'^stages/\d\d_route_a/checkpoint/.*\.json$', rel):
                continue
            body = store.json(self.run / rel)
            r2 = re.sub(r'^stages/\d\d_', 'stages/NN_', rel)
            if isinstance(body, dict) and not isinstance(body, Unparseable):
                if HEX.fullmatch(str(body.get('payload_sha256', ''))):
                    cand.setdefault(body['payload_sha256'], set()).add('<RA_PAYLOAD:%s>' % r2)
                if HEX.fullmatch(str(body.get('identity_sha256', ''))):
                    cand.setdefault(body['identity_sha256'], set()).add('<RA_IDENTITY_SHA>')
        self.hexmap = {h: '|'.join(sorted(v)) for h, v in cand.items()}
        self.hex_multi = {h: sorted(v) for h, v in cand.items() if len(v) > 1}
        inv = {}
        for h, t in self.hexmap.items():
            inv.setdefault(t, []).append(h)
        for t, hs in sorted(inv.items()):
            if len(hs) > 1 and not t.startswith('NPZ:'):
                self.collisions.append({'kind': 'HEXMAP_MANY_TO_ONE', 'token': t, 'distinct_sha256': sorted(hs)[:6], 'n': len(hs)})

    def s(self, v, at=''):
        if '<' in v or 'NPZ' in v:
            hit = [m for m in self.markers if m in v]
            if hit:
                self.collisions.append({'kind': 'RAW_TEXT_CONTAINS_NORMALIZER_TOKEN', 'at': at, 'markers': hit[:6], 'raw': v[:200]})
        for a, tok in self.tokens:
            if a in v:
                self.fired[tok] = self.fired.get(tok, 0) + v.count(a)
                v = v.replace(a, tok)
        if str(self.run) in v:
            v = self.run_re.sub('<RUN>', v)
        v = re.sub(r'<RUN>/stages/\d\d_', '<RUN>/stages/NN_', v)
        return HEX.sub(lambda m: self.hexmap.get(m.group(0), m.group(0)), v)

    def norm(self, o, drop=(), at=''):
        if isinstance(o, (Unparseable, Collided, Dup)):
            return o
        if hasattr(o, 'tolist') and hasattr(o, 'dtype') and not isinstance(o, (str, bytes)):
            shp = list(o.shape) if getattr(o, 'ndim', 0) or type(o).__name__ == 'ndarray' else None
            return NDV(o.dtype.str, shp, self.norm(o.tolist(), drop, at))
        if isinstance(o, tuple):
            return tuple(self.norm(x, drop, '%s[%d]' % (at, i)) for i, x in enumerate(o))
        if isinstance(o, dict):
            out, src = {}, {}
            for k, x in o.items():
                if k in MASK_KEYS or k in drop:
                    continue
                nk = self.s(k, at + '/<key>') if isinstance(k, str) else k
                if nk in out:  # CX2-V5-B1: two raw keys normalize to one key -> FAIL naming both; never last-wins
                    self.collisions.append({'kind': 'KEY_COLLISION', 'at': at, 'normalized_key': str(nk)[:200],
                                            'raw_keys': [str(src[nk])[:200], str(k)[:200]]})
                    out[nk] = Collided([src[nk], k])
                    continue
                src[nk] = k
                out[nk] = self.norm(x, drop, at + '/' + str(nk))
            return out
        if isinstance(o, list):
            return [self.norm(x, drop, '%s[%d]' % (at, i)) for i, x in enumerate(o)]
        if isinstance(o, str):
            return self.s(o, at)
        return o


def build_tokens(tok_all):
    """CX2-V5-B1 / A71: the ref<->new token relation must be one-to-one; a pair with several labels gets the sorted join."""
    bad, r2n, n2r, labels, lab2pair = [], {}, {}, {}, {}
    for r, n, t in tok_all:
        r2n.setdefault(r, set()).add(n)
        n2r.setdefault(n, set()).add(r)
        labels.setdefault((r, n), set()).add(t)
        lab2pair.setdefault(t, set()).add((r, n))
    for r, ns in sorted(r2n.items()):
        if len(ns) > 1:
            bad.append({'kind': 'TOKEN_REFERENCE_RAW_PAIRED_TWICE', 'reference_raw': r[:200], 'new_raws': sorted(x[:200] for x in ns)})
    for n, rs in sorted(n2r.items()):
        if len(rs) > 1:
            bad.append({'kind': 'TOKEN_NEW_RAW_PAIRED_TWICE', 'new_raw': n[:200], 'reference_raws': sorted(x[:200] for x in rs)})
    for t, ps in sorted(lab2pair.items()):
        if len(ps) > 1:
            bad.append({'kind': 'TOKEN_LABEL_USED_FOR_TWO_PAIRS', 'label': t, 'pairs': sorted([a[:120], b[:120]] for a, b in ps)})
    pairs = [(r, n, '|'.join(sorted(ls))) for (r, n), ls in sorted(labels.items())]
    joined = {'|'.join(sorted(ls)): sorted(ls) for ls in labels.values() if len(ls) > 1}
    return pairs, bad, joined


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


def apply_declared(x, y, rules):
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
        for k in sorted(set(a) & set(b)):
            if k in PIN_DICTS and isinstance(a[k], dict) and isinstance(b[k], dict):
                ref_only = sorted(set(a[k]) - set(b[k]))
                new_only = sorted(set(b[k]) - set(a[k]))
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
                strict_pins(a[k], b[k], path + '/' + k, allowed_new, notes, violations)
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
    k = req.get('kind')
    return k if isinstance(k, str) else NAME_KIND.get(name)


def workers_of(req):
    v = argv_map(req.get('argv') or [], 'route_a --column-workers').get('--column-workers', '1')
    try:
        return int(v)
    except (TypeError, ValueError):
        return -1


def auto_custody(gate, ref, new, sr, sn, new_t, uvt_kinds, SR, SN):
    rep = {'reference_driver': None, 'pairs': [], 'inadmissible': []}
    st_r, st_n = SR.json(ref / 'start.json'), SN.json(new / 'start.json')
    rdrv, rsha = st_r.get('driver'), st_r.get('driver_sha256')
    ref_t, rd_ok = {}, False
    if isinstance(rdrv, str) and REFERENCE_DRIVERS.get(rdrv) == rsha and Path(rdrv).is_file():
        raw = Path(rdrv).read_bytes()  # CX2-V5-S4: tables from the bytes that were hashed
        if sha_b(raw) == rsha:
            ref_t, rd_ok = driver_tables(raw, rdrv), True
    rep['reference_driver'] = {'path': rdrv, 'sha256': rsha, 'declared_and_verified_from_bytes': rd_ok, 'tables': sorted(ref_t)}
    admitted = []
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
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
                    for i, k in enumerate(('--SOLVER', '--SOLVER_SHA256')):
                        if gr[i] != gn[i]:
                            admitted.append([gr[i], gn[i], '<ROUTE_A%s>' % k.replace('-', '_')])
                else:
                    rep['inadmissible'].append(row)
    nd = (st_n.get('driver'), st_n.get('driver_sha256'))
    if (rdrv, rsha) != nd:
        ok = rd_ok and list(nd) == DRIVER and sha_b(driver_raw()) == DRIVER[1]
        row = {'what': 'driver', 'reference': [rdrv, rsha], 'new': list(nd), 'expected_new': list(DRIVER), 'admitted': ok}
        rep['pairs'].append(row)
        if ok:
            admitted += [[rdrv, nd[0], '<DRIVER_DRIVER>'], [rsha, nd[1], '<DRIVER_DRIVER_SHA256>']]
        else:
            rep['inadmissible'].append(row)
    return admitted, rep


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


def tokens_policy(gate, tok, drv):
    bad, det = [], {}
    if any(not (isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) for x in t)) for t in tok):
        bad.append('declared tokens must be [ref, new, token] string triples')
    news = {t[1] for t in tok if isinstance(t, list) and len(t) == 3}
    base = {}
    succ = {}
    for k in drv.UVT_TAIL_KINDS:
        bp, bs = drv.SCRIPTS[k]
        up, us = drv.SCRIPTS_UVT[k]
        base[k] = {str(bp), bs, Path(bp).name}
        succ[k] = {str(up), us, Path(up).name}
    if gate == 'Z2':
        mapped_base = {k: sorted(v & news) for k, v in base.items() if v & news}
        missing_succ = {k: sorted({str(drv.SCRIPTS_UVT[k][0]), drv.SCRIPTS_UVT[k][1]} - news) for k in drv.UVT_TAIL_KINDS
                        if {str(drv.SCRIPTS_UVT[k][0]), drv.SCRIPTS_UVT[k][1]} - news}
        det['A59_base_on_new_side'] = mapped_base
        det['A59_successor_missing_on_new_side'] = missing_succ
        if mapped_base:
            bad.append('A59: declared tokens map a gal_c2v005 base on the NEW side (append mode); replace mode required')
        if missing_succ:
            bad.append('A59: a SCRIPTS_UVT successor (path, sha) is not a declared NEW side')
    else:
        hit = {k: sorted(v & news) for k, v in succ.items() if v & news}
        det['successor_on_new_side'] = hit
        if hit:
            bad.append('tail-OFF gate: a declared NEW side is a SCRIPTS_UVT successor')
    det['reasons'] = bad
    return not bad, det


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
    m = re.match(r'^le(\d+)_(columns_\d\d|rotation)$', name)
    if m:
        p = int(m.group(1))
        return 'fs_rotation' if p == 1 else 'le%d_rotation' % (p - 1)
    return None


def expected_tail_blocks(gate, drv, new, sn, rec, SN):
    """Raw expected tail argv per new stage name ('*' for every other stage = []), plus the UV_TAIL_RECORD cross-check."""
    def sha_or(p):
        return SN.sha_of(p) if Path(p).is_file() else 'MISSING_FILE(%s)' % p
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
            if name in ('route_a', 'route_a_tail_manifest') or not (d / 'request.json').is_file():
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
            blocks[name] = b
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


def check_requests(gate, R, N, sr, sn, blocks):
    bad, n, inserted = [], 0, {}
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
            if qr.is_file() != qn.is_file():
                bad.append((name, 'request.json present on one side only'))
            continue
        n += 1
        a, b = R.norm(R.store.json(qr), at='stages/%s/request.json' % name), N.norm(N.store.json(qn), at='stages/%s/request.json' % name)
        block = N.norm(blocks.get(name, []), at='<driver tail block %s>' % name)
        ra, rb = a.get('argv') or [], b.get('argv') or []
        why = check_argv(name, ra, rb, block, suffix=(name == 'route_a'))
        if why:
            bad.append((name, why[:6]))
        elif block:
            inserted[name] = block
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
    if d is None or not (d / 'request.json').is_file():
        return False, {'reason': 'no route_a_tail_manifest request'}
    q = SN.json(d / 'request.json')
    mw = drv.AUX_UVT['manifest_writer']
    det = {'script': q.get('script') == str(mw[0]) and q.get('script_sha256') == mw[1] and file_ok(str(mw[0]), mw[1]),
           'kind_and_name': q.get('kind') == 'route_a_tail_manifest' and q.get('name') == 'route_a_tail_manifest'}
    exp = None
    if ra is not None and (ra / 'request.json').is_file():
        am = argv_map(SN.json(ra / 'request.json').get('argv') or [], 'new route_a (manifest expectation)')
        req = new / 'inputs/uv_tail_route_a_request.json'
        exp = ['--seed', am.get('--seed'), '--seed-sha256', am.get('--seed-sha256'), '--attempt-directory', am.get('--outdir'),
               '--checkpoint-directory', am.get('--checkpoint-directory'), '--checkpoint-module', str(drv.AUX['checkpoint_module'][0]),
               '--checkpoint-module-sha256', drv.AUX['checkpoint_module'][1], '--uv-tail-request', str(req),
               '--uv-tail-request-sha256', SN.sha_of(req) if req.is_file() else 'MISSING_FILE', '--outdir', str(d / 'manifest')]
        if any(isinstance(x, Dup) for x in exp):
            exp = None
    det['argv'] = exp is not None and q.get('argv') == exp
    if not det['argv']:
        det['argv_found'], det['argv_expected'] = q.get('argv'), (None if exp is None else [str(x) for x in exp])
    return all(v is True for k, v in det.items() if k in ('script', 'kind_and_name', 'argv')), det


# ---------------------------------------------------------------- tail-off declared records (c2v004 unchanged)
def route_a_facts(run, stages, S):
    d = stages.get('route_a')
    if d is None or not (d / 'request.json').is_file():
        return None
    req = S.json(d / 'request.json')
    atts = sorted(x.name for x in d.glob('attempt_*') if x.is_dir() and not x.is_symlink())
    st = d / 'attempt_000' / 'start.json'
    return {'dir': d, 'request': req, 'argv': argv_map(req.get('argv') or [], '%s route_a' % S.tag), 'attempts': atts,
            'start': S.json(st) if st.is_file() else None}


def check_declared_off(drv, new_run, fn, cn_raw, SN):
    raw = off_request_bytes(drv)
    E = sha_b(raw)
    d1 = new_run / 'inputs' / OFF_REQUEST_NAME
    det = {'expected_request_sha256': E}
    det['D1_request_file'] = d1.is_file() and SN.sha_of(d1) == E and seq(SN.json(d1), jloads(raw)) and SN.json(d1) == drv.ro1_off_request()
    if fn is None:
        det['route_a'] = 'NO_COMPUTED_ROUTE_A'
        return False, det, None, set(), E
    side = fn['dir'] / 'uv_tail_sidecar'
    rec = {'request': {'path': str(d1.resolve()), 'sha256': E}, 'enabled': False, 'sidecar_directory': str(side.resolve())}
    am = fn['argv']
    g = {k: am.get(k) for k in ('--uv-tail-config', '--uv-tail-config-sha256', '--eps-certificate', '--eps-certificate-sha256',
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
    det['sidecar_absent'] = not side.exists()
    if not det['D2_start_json_record']:
        det['D2_found'] = st.get('uv_tail', '<ABSENT>')
    if not det['D3_caller_record']:
        det['D3_found'] = caller_rec
    rel_start = str((fn['dir'] / 'attempt_000' / 'start.json').relative_to(new_run))
    expected = {'inputs/%s/uv_tail' % OFF_REQUEST_NAME, rel_start + '/uv_tail'}
    ok = all(det[k] for k in ('D1_request_file', 'argv_flags', 'single_attempt', 'D2_start_json_record', 'D3_caller_record', 'sidecar_absent'))
    return ok, det, rec, expected, E


def stray_uv_tail(tree, S):
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
        if rel.endswith('.json') and '/checkpoint/' not in '/' + rel:
            o = S.json(run / rel)
            if isinstance(o, Unparseable):
                out.append({'at': rel + ':UNPARSEABLE', 'enabled': None})
                continue
            walk(o, rel)
    for rel in tree.files:
        if rel.endswith('.jsonl') and S.scan(run / rel, b'"uv_tail'):
            out.append({'at': rel + ':JSONL_TEXT', 'enabled': None})
    return out


def ro1_block(rn):
    return (rn.get('route_a_outcome') or {}).get('ro1') if isinstance(rn, dict) else None


def check_ro1_armed(ro1, expected_worker, binding_sha):
    ok = (isinstance(ro1, dict) and ro1.get('rule') == 'RO1' and ro1.get('armed') is True and ro1.get('fired') is False
          and ro1.get('events') == [] and 'inadmissible_record' not in ro1
          and ro1.get('worker_sha256') == expected_worker and ro1.get('binding_sha256') == binding_sha)
    return ok, {'new_ro1': ro1, 'expected_worker_sha256': expected_worker, 'expected_binding_sha256': binding_sha}


def check_ro1_unarmed(ro1):
    ok = (isinstance(ro1, dict) and ro1.get('rule') == 'RO1' and ro1.get('armed') is False and ro1.get('fired') is False
          and ro1.get('events') == [] and ro1.get('worker_sha256') is None and ro1.get('binding_sha256') is None
          and 'inadmissible_record' not in ro1)
    return ok, {'new_ro1': ro1}


def ro1_expectations(drv, fn):
    n = workers_of(fn['request']) if fn else 1
    w = drv.RO1_ROUTE_A['worker' if n == 1 else 'worker_parallel']
    return n, (str(w[0]), w[1])


def check_custody(drv, tok_all, fr, fn, worker):
    news = {}
    for r, n, t in tok_all:
        news.setdefault(n, []).append((r, t))
    bind, fac = drv.RO1_ROUTE_A['binding'], drv.AUX_UVT['facade']
    need = {'worker_path': worker[0], 'worker_sha256': worker[1], 'binding_path': str(bind[0]), 'binding_sha256': bind[1],
            'facade_path': str(fac[0]), 'facade_sha256': fac[1]}
    present = {k: (v in news) for k, v in need.items()}
    ref_pins = ((fr or {}).get('start') or {}).get('input_pins') or {}
    consistent = {}
    for what in ('binding', 'facade'):
        rp = [r for r, _ in news.get(need[what + '_path'], [])]
        rs = [r for r, _ in news.get(need[what + '_sha256'], [])]
        consistent[what] = any(ref_pins.get(p) == s for p in rp for s in rs)
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
    items.append((req, N.store.sha_of(req) if req.is_file() else 'MISSING_FILE(%s)' % req))
    for p, s in items:
        k = N.s(str(Path(p).resolve()), '<declared route-A pin key>')
        if k in exp:  # A71
            LAST_WINS.append({'where': 'declared route-A new-only pins', 'normalized_key': k})
            exp[k] = Collided([str(p)])
            continue
        exp[k] = N.s(s, '<declared route-A pin value>')
    return exp


def static_pin_verifier(N):
    """top-level start.json static_pins: a NEW-only pin is admitted only when the raw path's bytes hash to the raw value."""
    rev = {}

    def ok(key_norm, val_norm):
        raw = rev.get(key_norm)
        return isinstance(raw, tuple) and file_ok(raw[0], raw[1])
    return ok, rev


def compare_json_file(rel, p, q, R, N, rules, pin_allow):
    x = R.norm(R.store.json(p), at=rel)
    y = N.norm(N.store.json(q), at=rel)
    notes, viol = [], []
    if pin_allow is not None:
        strict_pins(x, y, rel, pin_allow, notes, viol)
    x, y, rep, bad = apply_declared(x, y, rules)
    ok = seq(x, y) and not viol and not bad
    det = None
    if not ok:
        det = {'file': rel, 'differing': diffs(x, y)[:4], 'pin_violations': viol[:6], 'rule_violations': bad[:4]}
    return ok, det, rep, notes


def compare_jsonl(rel, p, q, R, N, extra_mask=(), drop_new_stage=()):
    x = [R.norm(o, drop=extra_mask, at='%s:%d' % (rel, i)) for i, o in enumerate(R.store.jsonl(p))]
    y = [N.norm(o, drop=extra_mask, at='%s:%d' % (rel, i)) for i, o in enumerate(N.store.jsonl(q))]
    dropped = 0
    if drop_new_stage:
        keep = []
        for e in y:
            if isinstance(e, dict) and e.get('stage') in drop_new_stage:
                dropped += 1
            else:
                keep.append(e)
        y = keep
    ok = seq(x, y) and (not drop_new_stage or dropped == 2 * len(drop_new_stage))
    return ok, (None if ok else {'file': rel, 'n': [len(x), len(y)], 'dropped_declared': dropped, 'differing': diffs(x, y)[:4]})


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    for k in ('reference', 'new', 'tokens', 'out', 'driver'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--gate', required=True)
    ap.add_argument('--require-ro1-armed', action='store_true')
    a = ap.parse_args(argv)
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
    DRIVER[:] = list(DRIVERS[a.driver])
    DRIVER_RAW[0] = DRIVER_RAW[1] = None
    driver_raw()
    me_raw = Path(__file__).read_bytes()
    tok_raw = Path(a.tokens).read_bytes()
    try:
        tok = jloads(tok_raw)['declared']
    except (ValueError, KeyError, TypeError) as e:
        raise SystemExit('REFUSED: tokens file %s: %s' % (a.tokens, e))
    if os.path.lexists(a.out):
        raise SystemExit('REFUSED: --out exists (exclusive create): %s' % a.out)
    MASK_KEYS.clear()
    MASK_KEYS.update(MASK_KEYS_BASE | (TAIL_KEYS if tail_on else set()))
    del LAST_WINS[:]
    ref, new = Path(a.reference).resolve(), Path(a.new).resolve()
    checks = {}
    head = {'schema': 'RUN_IDENTITY_COMPARE_C2V006', 'gate': a.gate, 'driver_selected': a.driver, 'driver_pin': list(DRIVER),
            'tail_on': tail_on, 'ro1_requirement': ro1_req, 'declared_tail_off_records': declared_off,
            'require_ro1_armed_flag': bool(a.require_ro1_armed), 'masked_keys': sorted(MASK_KEYS), 'array_policy': ARRAY_POLICY,
            'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_b(me_raw)},
            'reference': str(ref), 'new': str(new), 'tokens': {'path': str(Path(a.tokens).resolve()), 'sha256': sha_b(tok_raw)}}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
    extra, hold = {}, {}
    try:
        _compare(a, ref, new, tok, tail_on, ro1_req, declared_off, put, extra, hold)
    except Exception as e:  # own hardening: never crash without a report; an exception is a FAIL
        put('COMPARATOR_EXCEPTION', False, {'type': type(e).__name__, 'message': str(e)[:500],
                                            'traceback': traceback.format_exc()[-4000:]})
        if 'SR' in hold and 'STRICT_PARSE' not in checks:
            _strict_puts(put, hold, partial=True)
    rep = dict(head, **extra)
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
        {'rule': 'duplicate JSON members, duplicate / non-.npy NPZ members, unparseable JSON / JSONL / NPZ / NPY all FAIL (CX2-V5-S2, S3)',
         'partial_after_exception': partial, 'reference': SR.problems[:12], 'new': SN.problems[:12], 'n': [len(SR.problems), len(SN.problems)],
         'files_parsed': [len(SR._json) + len(SR._arr), len(SN._json) + len(SN._arr)]})
    put('NORM_INJECTIVE', not rc and not nc and not tok_bad,
        {'rule': 'normalization must be injective on each side (CX2-V5-B1): no two raw keys to one key, no raw normalizer text, '
                 'no many-to-one hexmap token (NPZ content tokens excepted), one-to-one token pairing',
         'partial_after_exception': partial, 'reference': rc[:12], 'new': nc[:12], 'n': [len(rc), len(nc)], 'tokens': tok_bad[:12],
         'hexmap_shared_sha_joined': {'reference': len(R.hex_multi) if R else None, 'new': len(N.hex_multi) if N else None}})
    put('NO_LAST_WINS', not LAST_WINS, {'rule': 'A71: every list-to-mapping site rejects duplicates (argv flags read by name, stage_records, '
                                                'normalized pin keys, canonical inventory paths, driver table literals)',
                                        'partial_after_exception': partial, 'hits': LAST_WINS[:20]})
    unstable = SR.unstable + SN.unstable + SR.verify() + SN.verify()
    put('TREE_STABLE', not unstable, {'rule': 'CX2-V5-S4: each file hashed and compared from one in-memory read; every recorded file re-hashed at the end',
                                      'partial_after_exception': partial, 'files_recorded': [len(SR.sha), len(SN.sha)], 'changed': unstable[:12]})


def _compare(a, ref, new, tok, tail_on, ro1_req, declared_off, put, extra, hold):
    new_t = driver_tables(driver_raw(), DRIVER[0])
    drv = load_driver()
    TR, TN = Tree(ref), Tree(new)
    SR, SN = Store(ref, 'reference'), Store(new, 'new')
    hold.update(SR=SR, SN=SN)
    sr, sn = TR.stages, TN.stages
    # ---------------- B1 stage set / order
    extras = DECLARED_EXTRA_STAGES[a.gate]
    on = [x for x in TN.order if x not in extras]
    ord_ok = TR.order == on and not any(x in extras for x in TR.order)
    ex_det = {}
    for x in extras:
        cnt = TN.order.count(x)
        pos_ok = cnt == 1 and ('route_a' not in TN.order or TN.order.index(x) == TN.order.index('route_a') + 1)
        ex_det[x] = {'count': cnt, 'immediately_after_route_a': pos_ok}
        ord_ok = ord_ok and pos_ok
    put('STAGE_SET', not TR.problems and not TN.problems and ord_ok,
        {'reference_problems': TR.problems[:12], 'new_problems': TN.problems[:12], 'order_reference': TR.order, 'order_new': TN.order,
         'order_equal_after_declared_extras': TR.order == on, 'declared_extra_stages': ex_det})
    # ---------------- tokens: declared + automatic custody + attempt ledger
    ok, det = tokens_policy(a.gate, tok, drv)
    put('TOKENS_POLICY', ok, det)
    auto, auto_rep = auto_custody(a.gate, ref, new, sr, sn, new_t, tuple(drv.UVT_TAIL_KINDS), SR, SN)
    put('AUTO_CUSTODY', not auto_rep['inadmissible'], auto_rep)
    inv_r, inv_n = TR.inventory(), TN.inventory()
    led_r, led_n = {}, {}
    for inv, led in ((inv_r, led_r), (inv_n, led_n)):
        for rel in list(inv):
            m = ATTEMPT_RE.match(rel)
            if m:
                led.setdefault(m.group(1), {}).setdefault(m.group(2), {})[m.group(3)] = inv.pop(rel)
    led_tokens, lbad = [], []
    for d in sorted(set(led_r) | set(led_n)):
        tr_, tn_ = sorted((led_r.get(d) or {}).items()), sorted((led_n.get(d) or {}).items())
        if len(tr_) != len(tn_):
            lbad.append({'dir': d, 'tokens': [len(tr_), len(tn_)]})
            continue
        for i, ((ta, _), (tb, _)) in enumerate(zip(tr_, tn_)):
            led_tokens.append([ta, tb, '<ATTEMPT_TOKEN_%s_%d>' % (d.split('/')[1].upper(), i)])
    tok_valid = [t for t in tok if isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) for x in t)]
    tok_all = tok_valid + auto + led_tokens
    pairs, tok_bad, joined = build_tokens(tok_all)
    labels = sorted({t for _, _, t in tok_all})
    markers = NORMALIZER_MARKERS + tuple(labels)
    hold['tok_bad'] = tok_bad
    R = Side(TR, SR, [(r, t) for r, n, t in pairs], markers)
    hold['R'] = R
    N = Side(TN, SN, [(n, t) for r, n, t in pairs], markers)
    hold['N'] = N
    extra.update({'auto_tokens_admitted': auto, 'attempt_tokens': led_tokens, 'token_labels_joined': joined})
    cm = load_cm()
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
                x = R.norm(SR.json(ka[k]), RECORD_DROP, at='%s/%s.%s.json' % (d, ta, k))
                y = N.norm(SN.json(kb[k]), RECORD_DROP, at='%s/%s.%s.json' % (d, tb, k))
                if not seq(x, y):
                    lbad.append({'dir': d, 'record': k, 'differing': diffs(x, y)[:4]})
    put('ATTEMPT_LEDGER', not lbad, {'directories': {d: [len(led_r.get(d) or {}), len(led_n.get(d) or {})] for d in sorted(set(led_r) | set(led_n))},
                                     'tokens': [t[2] for t in led_tokens], 'differing': lbad[:8]})
    # ---------------- INVENTORY (real paths; symlinks fail; canonical collisions fail)
    ref_only = sorted(set(inv_r) - set(inv_n))
    new_only = sorted(set(inv_n) - set(inv_r))
    pats = [(re.compile(p + r'\Z'), why) for p, why in DECLARED_NEW_ONLY[a.gate]]
    adm_new, undeclared = {}, []
    for rel in new_only:
        hit = [why for rx, why in pats if rx.match(rel)]
        (adm_new.setdefault(hit[0], []).append(rel)) if hit else undeclared.append(rel)
    put('INVENTORY', not ref_only and not undeclared and not TR.links and not TN.links and not TR.inv_collisions and not TN.inv_collisions,
        {'n_files': [len(TR.files), len(TN.files)], 'reference_only': ref_only[:20], 'n_reference_only': len(ref_only),
         'new_only_undeclared': undeclared[:20], 'n_new_only_undeclared': len(undeclared),
         'new_only_declared': {k: {'n': len(v), 'first': v[:6]} for k, v in adm_new.items()},
         'symlinks': {'reference': TR.links[:10], 'new': TN.links[:10]},
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
        if not (d / 'request.json').is_file():
            continue
        q = SN.json(d / 'request.json')
        kind, exp = planned_script(a.gate, name, q, drv)
        got = (q.get('script'), q.get('script_sha256'))
        ok = exp is not None and got == (str(exp[0]), exp[1]) and file_ok(str(exp[0]), exp[1])
        sc_rows[name] = {'kind': kind, 'script_sha256': got[1], 'planned_sha256': exp[1] if exp else None, 'ok': ok}
        if not ok:
            sc_bad.append({'stage': name, 'kind': kind, 'got': list(got), 'planned': [str(exp[0]), exp[1]] if exp else None})
    put('SCRIPT_CUSTODY', not sc_bad, {'rule': 'A59: every new stage runs the driver-planned script for gate %s, hashed from bytes' % a.gate,
                                       'stages': sc_rows, 'violations': sc_bad[:12]})
    # ---------------- route A
    fr, fn = route_a_facts(ref, sr, SR), route_a_facts(new, sn, SN)
    cn_raw, declared_rec, expected_stray, E = None, None, set(), None
    ra_r, ra_n = sr.get('route_a'), sn.get('route_a')
    if ra_n is not None and (ra_n / 'checkpoint/IDENTITY.json').is_file():
        cn_raw = cm.decode(cm_read(cm, SN, ra_n / 'checkpoint/IDENTITY.json', 'identity')['identity']['caller']['record'])
    if declared_off:
        ok, det, declared_rec, expected_stray, E = check_declared_off(drv, new, fn, cn_raw, SN)
        put('UV_TAIL_DECLARED', ok, det)
    extra['expected_tail_off_request_sha256'] = E
    exp_ra_pins = ra_new_pins(a.gate, drv, N, new)
    if ra_r is not None and ra_n is not None:
        pre = 'stages/route_a/checkpoint/blobs/'
        fr_b = {k[len(pre):]: SR.sha_of(v) for k, v in inv_r.items() if k.startswith(pre)}
        fn_b = {k[len(pre):]: SN.sha_of(v) for k, v in inv_n.items() if k.startswith(pre)}
        compared.update(pre + k for k in fr_b)
        put('RA_BLOBS', fr_b == fn_b and bool(fr_b), {'n': [len(fr_b), len(fn_b)], 'differing': sorted(set(fr_b) ^ set(fn_b) | {k for k in fr_b if fn_b.get(k) != fr_b[k]})[:10]})
        bad, n = [], 0
        it_re = re.compile(r'^stages/route_a/checkpoint/iteration_[^/]+/[^/]+\.json$')
        ref_it = sorted(k for k in inv_r if it_re.match(k))
        new_it = sorted(k for k in inv_n if it_re.match(k))
        for rel in ref_it:
            n += 1
            compared.add(rel)
            if rel not in inv_n:
                bad.append(rel + ' MISSING')
                continue
            x, y = R.norm(SR.json(inv_r[rel]), RECORD_DROP, at=rel), N.norm(SN.json(inv_n[rel]), RECORD_DROP, at=rel)
            if not seq(x, y):
                bad.append((rel, diffs(x, y)[:3]))
        put('RA_RECORDS', not bad and n == len(new_it) and n > 0, {'n': [n, len(new_it)], 'differing': bad[:8]})
        ir = cm_read(cm, SR, ra_r / 'checkpoint/IDENTITY.json', 'identity')['identity']
        compared.add('stages/route_a/checkpoint/IDENTITY.json')
        cr = caller_norm(cm.decode(ir['caller']['record']), tail_on)
        if cn_raw is None:
            raise SystemExit('NEW route-A checkpoint IDENTITY.json missing: %s' % ra_n)
        cn = caller_norm(cn_raw, tail_on, declared_rec)
        x, y = R.norm(cr, at='IDENTITY/caller'), N.norm(cn, at='IDENTITY/caller')
        if a.gate in ('Z2', 'Z2_OFF_RO1'):
            xp, yp = x.get('code_pins') or {}, y.get('code_pins') or {}
            r_only, n_only = sorted(set(xp) - set(yp)), sorted(set(yp) - set(xp))
            put('RA_PINSET', not r_only and set(n_only) == set(exp_ra_pins) and all(seq(yp.get(k), v) for k, v in exp_ra_pins.items()),
                {'reference_only': r_only, 'new_only': n_only, 'expected_new_only': sorted(exp_ra_pins),
                 'value_mismatch': sorted(k for k, v in exp_ra_pins.items() if k in yp and not seq(yp[k], v))})
        notes, viol = [], []
        strict_pins({'caller': x}, {'caller': y}, 'IDENTITY', exp_ra_pins, notes, viol)
        put('RA_IDENTITY', seq(x, y) and not viol, {'differing': diffs(x, y)[:8], 'pin_violations': viol[:8], 'declared_new_only_pins': notes})
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
    compared.update('stages/%s/request.json' % k for k in set(sr) & set(sn) if (sr[k] / 'request.json').is_file() and (sn[k] / 'request.json').is_file())
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
            with_req = [x for x in T.order if (T.stages[x] / 'request.json').is_file()]
            if names != with_req:
                sr_bad.append({'side': tag, 'why': 'stage_records names != stage directories with a request, in order', 'records': names, 'stages': with_req})
            per[tag] = {}
            for r in recs:
                if not isinstance(r, dict):
                    sr_bad.append({'side': tag, 'why': 'stage record is not an object'})
                    continue
                nm = r.get('name')
                if nm not in T.stages or not (T.stages[nm] / 'request.json').is_file():
                    continue
                if nm in per[tag]:  # A71
                    LAST_WINS.append({'where': 'result.json stage_records', 'side': tag, 'name': nm})
                    sr_bad.append({'side': tag, 'stage': nm, 'why': 'DUPLICATE_STAGE_RECORD_NAME'})
                    continue
                q = S.store.json(T.stages[nm] / 'request.json')
                core = {k: v for k, v in r.items() if k not in STAGE_RECORD_EXTRA}
                if not seq(core, q) or not set(r) - set(core) <= STAGE_RECORD_EXTRA:
                    sr_bad.append({'side': tag, 'stage': nm, 'why': 'record != own request.json', 'differing': diffs(q, core)[:4]})
                per[tag][nm] = S.norm({k: v for k, v in r.items() if k in STAGE_RECORD_EXTRA}, at='result.json/stage_records/%s' % nm)
        for nm in sorted(set(per['reference']) & set(per['new'])):
            if not seq(per['reference'][nm], per['new'][nm]):
                sr_bad.append({'stage': nm, 'why': 'record execution fields differ', 'differing': diffs(per['reference'][nm], per['new'][nm])[:4]})
        sr_det['n'] = [len(rr_raw['stage_records']), len(rn_raw['stage_records'])]
    put('STAGE_RECORDS', not sr_bad, dict(sr_det, present=has, violations=sr_bad[:10]))
    # ---------------- declared rules (B2): per canonical file
    spec_rules = [{'path': ('label',), 'rule': 'MASK', 'why': 'spec label (custody text)'}]
    if a.gate == 'Z2_OFF_RO1':
        spec_rules.append({'path': ('numerics', 'route_a', 'ro1_workers'), 'rule': 'NEW_ONLY', 'value': True, 'why': 'the Z2_OFF_RO1 spec leaf (A47 I6)'})

    def under(prefix, rules):
        return [dict(r, path=prefix + r['path']) for r in rules]
    res_rules = under(('normalized_spec',), spec_rules) + [
        {'path': ('stage_records',), 'rule': 'COVERED', 'check': 'STAGE_RECORDS + REQUEST', 'why': 'request copies plus execution fields'},
        {'path': ('route_a_outcome', 'ro1'), 'rule': 'NEW_ONLY_OR_EQUAL', 'why': 'RO1 block (checked by RO1)'},
        {'path': ('identity', 'route_a', 'outcome', 'ro1'), 'rule': 'NEW_ONLY_OR_EQUAL', 'why': 'RO1 block (checked by RO1; equals route_a_outcome.ro1)'}]
    if a.gate in IMPL_KIND_PAIRS:
        res_rules.append({'path': ('identity', 'route_a', 'implementation', 'kind'), 'rule': 'PAIR', 'pairs': IMPL_KIND_PAIRS[a.gate],
                          'why': 'driver L2872-2878 implementation kind'})
    if a.gate == 'Z2_OFF_RO1':
        res_rules.append({'path': ('identity', 'route_a', 'implementation', 'ro1_workers'), 'rule': 'NEW_ONLY', 'value': True, 'why': 'driver L2879'})
    file_rules = {'inputs/call_spec.json': spec_rules, 'start.json': under(('normalized_spec',), spec_rules), 'result.json': res_rules}
    if declared_off and declared_rec is not None:
        file_rules['stages/route_a/attempt_000/start.json'] = [{'path': ('uv_tail',), 'rule': 'NEW_ONLY', 'value': N.norm(declared_rec, at='<declared D2 record>'),
                                                                 'why': 'D2 declared tail-off record (driver R5)'}]
    sp_ok, sp_rev = static_pin_verifier(N)
    for k, v in ((st_n.get('static_pins') or {}) if isinstance(st_n.get('static_pins'), dict) else {}).items():
        nk = N.s(k, 'start.json/static_pins/<key>')
        if nk in sp_rev:  # A71
            LAST_WINS.append({'where': 'start.json static_pins normalized key', 'normalized_key': nk, 'raw_keys': [sp_rev[nk][0], k]})
            sp_rev[nk] = Collided([sp_rev[nk][0], k])
            continue
        sp_rev[nk] = (k, v)
    # ---------------- RESULT
    x, y = R.norm(rr_raw, at='result.json'), N.norm(rn_raw, at='result.json')
    ro1_cross = True
    h1, v1 = _get(y, ('route_a_outcome', 'ro1'))
    h2, v2 = _get(y, ('identity', 'route_a', 'outcome', 'ro1'))
    if h1 and h2:
        ro1_cross = seq(v1, v2)
    notes, viol = [], []
    strict_pins(x, y, 'result.json', {}, notes, viol)
    x2, y2, rep_res, bad_res = apply_declared(x, y, res_rules)
    put('RESULT', seq(x2, y2) and not viol and not bad_res and ro1_cross and rr_raw.get('status') == 'COMPLETED',
        {'differing': diffs(x2, y2)[:12], 'declared_rules_applied': rep_res, 'rule_violations': bad_res, 'pin_violations': viol[:6],
         'ro1_blocks_equal': ro1_cross, 'status': [rr_raw.get('status'), rn_raw.get('status')]})
    compared.add('result.json')
    # ---------------- every other both-side file (S3)
    groups = {'FILES_INPUTS': [], 'FILES_TOP': [], 'FILES_ROUTE_A': [], 'STAGES': []}
    counts = {g: 0 for g in groups}
    applied = []
    pin_notes = []
    both = sorted(set(inv_r) & set(inv_n))
    for rel in both:
        if rel in compared:
            continue
        p, q = inv_r[rel], inv_n[rel]
        nm = Path(rel).name
        if rel.startswith('stages/') and nm in LOG_NAMES:
            continue
        if rel.startswith('inputs/'):
            g = 'FILES_INPUTS'
        elif '/' not in rel:
            g = 'FILES_TOP'
        elif rel.startswith('stages/route_a/'):
            g = 'FILES_ROUTE_A'
        else:
            g = 'STAGES'
        if rel.startswith('stages/route_a/checkpoint/') and (rel.startswith('stages/route_a/checkpoint/blobs/') or rel.endswith('IDENTITY.json')):
            continue
        counts[g] += 1
        compared.add(rel)
        suf = p.suffix
        if suf in ('.npz', '.npy'):
            ka, va = SR.array(p)
            kb, vb = SN.array(q)
            if ka == 'invalid' or kb == 'invalid' or ka != kb or va != vb:
                groups[g].append((rel, ('NPZ' if suf == '.npz' else 'NPY') + '_CONTENT',
                                  ([k for k in sorted(set(va) | set(vb)) if va.get(k) != vb.get(k)][:6] if ka == kb == 'npz' else None)))
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
            if SR.read(p) != SN.read(q):
                groups[g].append((rel, 'RAW_BYTES'))
    for g, bad in groups.items():
        det = {'compared': counts[g], 'differing': bad[:12], 'n_differing': len(bad)}
        if g == 'FILES_TOP':
            det.update({'declared_rules_applied': applied, 'declared_new_only_pins': pin_notes[:20]})
        put(g, not bad, det)
    if not tail_on:
        sr_, sn_ = stray_uv_tail(TR, SR), stray_uv_tail(TN, SN)
        new_at = {s['at'] for s in sn_}
        admitted = sorted(new_at & expected_stray)
        undeclared = [s for s in sn_ if s['at'] not in expected_stray]
        put('STRAY_UV_TAIL', not sr_ and not undeclared and new_at >= expected_stray,
            {'reference': sr_[:12], 'new_undeclared': undeclared[:12], 'new_admitted_declared': admitted,
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
        put('RO1', isinstance(ro1, dict) and ro1.get('armed') is True and ro1.get('fired') is False, {'new_ro1': ro1})
    elif ro1_req == 'UNARMED':
        ok, det = check_ro1_unarmed(ro1_block(rn_raw))
        put('RO1', ok, det)
    # ---------------- coverage (a gate check since c2v005)
    unc = sorted(x for x in both if x not in compared and not (x.startswith('stages/') and Path(x).name in LOG_NAMES)
                 and not (x.startswith('stages/route_a/checkpoint/blobs/') or x == 'stages/route_a/checkpoint/IDENTITY.json'))
    logs = sorted(x for x in both if x.startswith('stages/') and Path(x).name in LOG_NAMES)
    put('COVERAGE', not unc, {'files_both_sides': len(both), 'logs_skipped': len(logs), 'not_compared_non_log': unc[:20],
                              'new_only_declared_not_compared': sum(len(v) for v in adm_new.values()),
                              'note': 'every both-side file except stage stdout/stderr is content-compared; new-only declared files have no counterpart '
                                      '(they are still strictly parsed: STRICT_PARSE)'})
    # ---------------- c2v006 strictness checks
    _strict_puts(put, hold)
    extra['tokens_fired'] = {'reference': R.fired, 'new': N.fired}


if __name__ == '__main__':
    raise SystemExit(main())
