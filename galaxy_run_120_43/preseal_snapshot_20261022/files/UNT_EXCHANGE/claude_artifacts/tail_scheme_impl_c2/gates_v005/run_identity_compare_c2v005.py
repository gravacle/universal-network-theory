"""Run-output identity comparator for the V007 identity gates, c2v005 (Claude2 tail_scheme_impl_c2/gates_v005).
c2v005 = successor of gates_v004/run_identity_compare_c2v004.py (e3d153b6) for root V005 addendum A68 (check of c2v004:
gates_v004/check/CHECK.md B1, B2, S1-S3, N2 is the fill tool's) and A59 (Z2 replace-mode tokens, successor custody as a gate
check), A67 N1 (identity runs carry the pinned driver sha).  Nothing of c2v004 is relaxed.  Changes:
  --driver r4|r5 (required).  The pinned driver of the NEW run (r4 b9ae92d5, r5 b5cc62af; from bytes).  Its tables drive
     AUTO_CUSTODY, SCRIPT_CUSTODY, RO1, RO1_CUSTODY, RA_PINSET and the tail-argv expectations.  r4 and r5 differ only in the
     pin tables (r4/r5 diff: lines 294-380 only), so every cited code line is the same in both.
  B1 STAGE_SET + INVENTORY by real path.  Every entry under stages/ must be a real directory named NN_<name> with a unique name
     and a unique number on its side; otherwise STAGE_SET fails and the offending directories keep their RAW relative paths in
     the inventory (so they are reference-only / new-only and fail INVENTORY too, and nothing is silently overwritten).  The
     stage order (by number) must equal the reference's after removing the gate's declared extra stage (Z2: exactly one
     route_a_tail_manifest, immediately after route_a; driver L2919-2941).  Renumbering alone is not a difference (stage
     numbers are a counter, driver L1786-1791).  Any symlink in either tree fails INVENTORY.
  B2 RESULT = the full result.json, normalized and strict (H5), with ONLY the declared custody items of DECLARED below
     (each a declared rule: MASK, NEW_ONLY with an exact value, PAIR of exact values; each application is reported).
     stage_records are tied to the run's own request.json files (STAGE_RECORDS) and compared across runs there.
  S1 a tail flag occurring more often than the driver emits it fails (REQUEST).
  S2 REQUEST: the new argv must equal the reference argv with exactly the driver's tail block inserted once, contiguous,
     on exactly the stage kinds where the driver emits it (r4/r5 uvt_argv L2949-2962; route A L2845, L2847-2850), and no tail
     flag anywhere else.  The block's values are built from the new run's own files (paths and shas from bytes) and the driver
     constants; the Z2 result.json uv_tail record (raw, masked in the comparison by the registered c2v002 semantics) is
     cross-checked against those bytes (UV_TAIL_RECORD).  The route_a_tail_manifest request is checked against the driver's
     margv (MANIFEST_STAGE, L2930-2934, script = the driver's AUX_UVT manifest_writer).
  S3 every file present on both sides is content-compared (FILES_* checks): inputs/*, top-level start/finish/progress, every
     route-A attempt file (result.json, finish.json, start.json, progress, node_diagnostics, arrays incl. .npy), checkpoint.lock,
     every stage file.  Only stdout.txt / stderr.txt are skipped; COVERAGE fails if any other both-side file is not compared.
     Pin dictionaries (PIN_DICTS) may differ only by the declared new-only pins (exact values); a reference-only pin fails.
  A59 TOKENS_POLICY (Z2): the declared token set must be replace-mode: no declared NEW side is a driver SCRIPTS[kind] base
     (path, sha or basename) of a UVT kind, and every SCRIPTS_UVT[kind] path and sha is a declared NEW side.  Tail-OFF gates:
     no declared NEW side is a SCRIPTS_UVT successor.  SCRIPT_CUSTODY (raw, untokenized): every new stage request runs the
     driver's planned (script, sha) for its gate and kind, hashed from bytes.
  A67 N1 NEW_DRIVER_PIN: new start.json driver/driver_sha256 and result.json driver_sha256 = the selected driver pin.
  Attempt-ledger tokens (time-pid-random, checkpoint module c2v003) are paired by sorted order and tokenized <ATTEMPT_TOKEN_i>.
Unchanged from c2v004: gates and their semantics (Z2 tail ON + RO1 ARMED + RO1_CUSTODY; Z2_OFF_RO1 declared tail-off records
D1-D3 + RA_PINSET + RO1; Z2_OFF; B0P_RERUN RO1 UNARMED), masking, the hexmap (npz -> content digest, a run JSON file's sha ->
<JSONFILE:path>), RECORD_DROP, the restricted AST table reader, strict JSON, AUTO_CUSTODY.
INERT on import; reads two completed run directories and pinned code (read-only); writes ONE report (exclusive create).

  python3 -I -B run_identity_compare_c2v005.py --gate GATE --driver r4|r5 --reference REF_RUN --new NEW_RUN --tokens T.json --out R.json
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import struct
import types
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


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def file_ok(path, sha):
    return isinstance(path, str) and isinstance(sha, str) and Path(path).is_file() and sha_file(path) == sha


def load_cm():
    if sha_file(CKPT[0]) != CKPT[1]:
        raise SystemExit('checkpoint module pin')
    s = importlib.util.spec_from_file_location('ckpt_cmp_c2v005', CKPT[0])
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def load_driver():
    """The selected pinned driver, executed from the verified bytes (module body: constants and defs only), as c2v004."""
    raw = Path(DRIVER[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != DRIVER[1]:
        raise SystemExit('driver pin')
    m = types.ModuleType('v010_cmp_c2v005')
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
        return {_ev(k, env): _ev(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Path' and not node.keywords \
            and len(node.args) == 1:
        v = _ev(node.args[0], env)
        if isinstance(v, str):
            return Path(v)
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in env:
        k = _ev(node.slice, env)
        return env[node.value.id][k]
    raise _Unsafe(type(node).__name__)


def driver_tables(path):
    tree = ast.parse(Path(path).read_text())
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
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        return struct.pack('<d', a) == struct.pack('<d', b)
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(seq(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(seq(x, y) for x, y in zip(a, b))
    return a == b


def _show(v):
    return '%s:%s' % (type(v).__name__, (v.hex() if isinstance(v, float) else str(v))[:160])


def diffs(a, b, path='', out=None, limit=12):
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((path + '/' + k, 'ONLY_' + ('NEW' if k in b else 'REF')))
            else:
                diffs(a[k], b[k], path + '/' + k, out, limit)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            diffs(x, y, '%s[%d]' % (path, i), out, limit)
    elif not seq(a, b):
        out.append((path, _show(a), _show(b)))
    return out


def npz_members(p):
    import numpy as np
    with np.load(p, allow_pickle=False) as f:
        return {k: (f[k].dtype.str, tuple(f[k].shape), hashlib.sha256(np.ascontiguousarray(f[k]).tobytes()).hexdigest()) for k in f.files}


def npy_member(p):
    import numpy as np
    a = np.load(p, allow_pickle=False)
    return (a.dtype.str, tuple(a.shape), bool(a.flags.f_contiguous and not a.flags.c_contiguous),
            hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest())


def content_digest(p):
    return hashlib.sha256(json.dumps(sorted(npz_members(p).items())).encode()).hexdigest()


def read_json(p):
    return json.loads(Path(p).read_text())


def argv_map(argv):
    return dict(zip(argv[::2], argv[1::2]))


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

    def canon(self, rel):
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0] == 'stages' and parts[1] in self.dir2name:
            return '/'.join(['stages', self.dir2name[parts[1]]] + parts[2:])
        return rel

    def inventory(self):
        return {self.canon(r): self.run / r for r in self.files}


class Side:
    def __init__(self, run, tokens):
        self.run = Path(run)
        self.tokens = sorted(tokens, key=lambda t: -len(t[0]))
        self.hexmap = {}
        for p in self.run.rglob('*'):
            if p.is_symlink():
                continue
            if p.is_file() and p.suffix == '.npz':
                self.hexmap[sha_file(p)] = 'NPZ:' + content_digest(p)
            elif p.is_file() and p.suffix == '.json':
                self.hexmap[sha_file(p)] = '<JSONFILE:%s>' % re.sub(r'^stages/\d\d_', 'stages/NN_', str(p.relative_to(self.run)))
        for p in self.run.glob('stages/*_route_a/checkpoint/**/*.json'):
            try:
                body = json.loads(p.read_text())
            except ValueError:
                continue
            rel = re.sub(r'^stages/\d\d_', 'stages/NN_', str(p.relative_to(self.run)))
            if isinstance(body, dict):
                if HEX.fullmatch(str(body.get('payload_sha256', ''))):
                    self.hexmap[body['payload_sha256']] = '<RA_PAYLOAD:%s>' % rel
                if HEX.fullmatch(str(body.get('identity_sha256', ''))):
                    self.hexmap[body['identity_sha256']] = '<RA_IDENTITY_SHA>'
        self.fired = {}

    def s(self, v):
        for a, tok in self.tokens:
            if a in v:
                self.fired[tok] = self.fired.get(tok, 0) + v.count(a)
                v = v.replace(a, tok)
        if str(self.run) in v:
            v = v.replace(str(self.run), '<RUN>')
        v = re.sub(r'<RUN>/stages/\d\d_', '<RUN>/stages/NN_', v)
        return HEX.sub(lambda m: self.hexmap.get(m.group(0), m.group(0)), v)

    def norm(self, o, drop=()):
        if hasattr(o, 'tolist') and not isinstance(o, (str, bytes)):
            o = o.tolist()
        if isinstance(o, tuple):
            o = list(o)
        if isinstance(o, dict):
            return {self.s(k): self.norm(x, drop) for k, x in o.items() if k not in MASK_KEYS and k not in drop}
        if isinstance(o, list):
            return [self.norm(x, drop) for x in o]
        if isinstance(o, str):
            return self.s(o)
        return o


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
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
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
    v = argv_map(req.get('argv') or []).get('--column-workers', '1')
    try:
        return int(v)
    except (TypeError, ValueError):
        return -1


def auto_custody(gate, ref, new, sr, sn, new_t, uvt_kinds):
    rep = {'reference_driver': None, 'pairs': [], 'inadmissible': []}
    st_r, st_n = read_json(ref / 'start.json'), read_json(new / 'start.json')
    rdrv, rsha = st_r.get('driver'), st_r.get('driver_sha256')
    ref_t, rd_ok = {}, False
    if isinstance(rdrv, str) and REFERENCE_DRIVERS.get(rdrv) == rsha and Path(rdrv).is_file() and sha_file(rdrv) == rsha:
        ref_t, rd_ok = driver_tables(rdrv), True
    rep['reference_driver'] = {'path': rdrv, 'sha256': rsha, 'declared_and_verified_from_bytes': rd_ok, 'tables': sorted(ref_t)}
    admitted = []
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
            continue
        a, b = read_json(qr), read_json(qn)
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
            ma, mb = argv_map(a.get('argv') or []), argv_map(b.get('argv') or [])
            gr, gn = (ma.get('--solver'), ma.get('--solver-sha256')), (mb.get('--solver'), mb.get('--solver-sha256'))
            if gr != gn:
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
        ok = rd_ok and list(nd) == DRIVER and sha_file(DRIVER[0]) == DRIVER[1]
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


def _sha_or(p):
    return sha_file(p) if Path(p).is_file() else 'MISSING_FILE(%s)' % p


def source_rotation_stage(name):
    """driver L3168 (rfs: fs_rot), L3172/L3276 (le p: le(p-1) rotation; le1: fs_rot)."""
    if name.startswith('rfs_columns'):
        return 'fs_rotation'
    m = re.match(r'^le(\d+)_(columns_\d\d|rotation)$', name)
    if m:
        p = int(m.group(1))
        return 'fs_rotation' if p == 1 else 'le%d_rotation' % (p - 1)
    return None


def expected_tail_blocks(gate, drv, new, sn, rec):
    """Raw expected tail argv per new stage name ('*' for every other stage = []), plus the UV_TAIL_RECORD cross-check."""
    blocks, rc = {}, None
    if gate == 'Z2':
        req = new / 'inputs/uv_tail_route_a_request.json'
        cfg = new / 'inputs/uv_tail_config.json'
        man_dir = sn.get('route_a_tail_manifest')
        man = (man_dir / 'manifest/ROUTE_A_TAIL_MANIFEST.json') if man_dir is not None else None
        ra = sn.get('route_a')
        if ra is not None:
            blocks['route_a'] = ['--uv-tail-config', str(req), '--uv-tail-config-sha256', _sha_or(req),
                                 '--eps-certificate', TEST_ONLY, '--eps-certificate-sha256', TEST_ONLY,
                                 '--lo-certificate', TEST_ONLY, '--lo-certificate-sha256', TEST_ONLY,
                                 '--uv-tail-sidecar-directory', str(ra / 'uv_tail_sidecar')]
        trunc = rec.get('truncation_argv') if isinstance(rec, dict) else None
        rc = {'record_present': isinstance(rec, dict)}
        if isinstance(rec, dict):
            rc.update({
                'enabled_true': rec.get('enabled') is True,
                'config_is_inputs_file_from_bytes': (rec.get('config') or {}).get('path') == str(cfg) and (rec.get('config') or {}).get('sha256') == _sha_or(cfg),
                'request_is_inputs_file_from_bytes': (rec.get('request') or {}).get('path') == str(req) and (rec.get('request') or {}).get('sha256') == _sha_or(req),
                'manifest_is_stage_file_from_bytes': man is not None and (rec.get('manifest') or {}).get('path') == str(man) and (rec.get('manifest') or {}).get('sha256') == _sha_or(man),
                'admissibility_test_only': rec.get('admissibility') == 'test_only',
                'test_only_flag': rec.get('test_only_flag') == ['--uv-tail-admit-test-only'],
                'certificates_test_only': rec.get('certificates') == {'eps_certificate': [TEST_ONLY, TEST_ONLY], 'lo_certificate': [TEST_ONLY, TEST_ONLY]},
                'route_a_argv_equals_driver_block': ra is not None and rec.get('route_a_argv') == blocks['route_a'][:-2],
                'truncation_argv_null_or_json': trunc is None or (isinstance(trunc, str) and _is_json(trunc)),
            })
        for name, d in sn.items():
            if name in ('route_a', 'route_a_tail_manifest') or not (d / 'request.json').is_file():
                continue
            kind = stage_kind(name, read_json(d / 'request.json'))
            if kind not in drv.UVT_TAIL_KINDS:
                continue
            bk = drv.UVT_BINDING_KIND[kind]
            b = ['--uv-tail-config', str(cfg), '--uv-tail-config-sha256', _sha_or(cfg), '--uv-tail-admit-test-only']
            if bk in ('reference', 'body', 'offset'):
                b += ['--route-a-tail-manifest', str(man) if man else 'MISSING_MANIFEST_STAGE',
                      '--route-a-tail-manifest-sha256', _sha_or(man) if man else 'MISSING_MANIFEST_STAGE']
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
            E = hashlib.sha256(off_request_bytes(drv)).hexdigest()
            blocks['route_a'] = ['--uv-tail-config', str(off), '--uv-tail-config-sha256', E, '--eps-certificate', TEST_ONLY,
                                 '--eps-certificate-sha256', TEST_ONLY, '--lo-certificate', TEST_ONLY, '--lo-certificate-sha256', TEST_ONLY,
                                 '--uv-tail-sidecar-directory', str(ra / 'uv_tail_sidecar')]
    return blocks, rc


def _is_json(s):
    try:
        json.loads(s)
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
        a, b = R.norm(read_json(qr)), N.norm(read_json(qn))
        block = N.norm(blocks.get(name, []))
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


def check_manifest_stage(gate, drv, new, sn, R_dummy=None):
    """Z2: the route_a_tail_manifest request is the driver's (L2930-2934, L1821): script = AUX_UVT manifest_writer (from bytes)."""
    d = sn.get('route_a_tail_manifest')
    ra = sn.get('route_a')
    if d is None or not (d / 'request.json').is_file():
        return False, {'reason': 'no route_a_tail_manifest request'}
    q = read_json(d / 'request.json')
    mw = drv.AUX_UVT['manifest_writer']
    det = {'script': q.get('script') == str(mw[0]) and q.get('script_sha256') == mw[1] and file_ok(str(mw[0]), mw[1]),
           'kind_and_name': q.get('kind') == 'route_a_tail_manifest' and q.get('name') == 'route_a_tail_manifest'}
    exp = None
    if ra is not None and (ra / 'request.json').is_file():
        am = argv_map(read_json(ra / 'request.json').get('argv') or [])
        req = new / 'inputs/uv_tail_route_a_request.json'
        exp = ['--seed', am.get('--seed'), '--seed-sha256', am.get('--seed-sha256'), '--attempt-directory', am.get('--outdir'),
               '--checkpoint-directory', am.get('--checkpoint-directory'), '--checkpoint-module', str(drv.AUX['checkpoint_module'][0]),
               '--checkpoint-module-sha256', drv.AUX['checkpoint_module'][1], '--uv-tail-request', str(req),
               '--uv-tail-request-sha256', _sha_or(req), '--outdir', str(d / 'manifest')]
    det['argv'] = exp is not None and q.get('argv') == exp
    if not det['argv']:
        det['argv_found'], det['argv_expected'] = q.get('argv'), exp
    return all(v is True for k, v in det.items() if k in ('script', 'kind_and_name', 'argv')), det


# ---------------------------------------------------------------- tail-off declared records (c2v004 unchanged)
def route_a_facts(run, stages):
    d = stages.get('route_a')
    if d is None or not (d / 'request.json').is_file():
        return None
    req = read_json(d / 'request.json')
    atts = sorted(x.name for x in d.glob('attempt_*') if x.is_dir())
    st = d / 'attempt_000' / 'start.json'
    return {'dir': d, 'request': req, 'argv': argv_map(req.get('argv') or []), 'attempts': atts,
            'start': read_json(st) if st.is_file() else None}


def check_declared_off(drv, new_run, fn, cn_raw):
    raw = off_request_bytes(drv)
    E = hashlib.sha256(raw).hexdigest()
    d1 = new_run / 'inputs' / OFF_REQUEST_NAME
    det = {'expected_request_sha256': E}
    det['D1_request_file'] = d1.is_file() and sha_file(d1) == E and json.loads(d1.read_text()) == drv.ro1_off_request()
    if fn is None:
        det['route_a'] = 'NO_COMPUTED_ROUTE_A'
        return False, det, None, set(), E
    side = fn['dir'] / 'uv_tail_sidecar'
    rec = {'request': {'path': str(d1.resolve()), 'sha256': E}, 'enabled': False, 'sidecar_directory': str(side.resolve())}
    am = fn['argv']
    det['argv_flags'] = (am.get('--uv-tail-config') is not None and str(Path(am['--uv-tail-config']).resolve()) == str(d1.resolve())
                         and am.get('--uv-tail-config-sha256') == E
                         and all(am.get(k) == drv.UVT_TEST_ONLY for k in ('--eps-certificate', '--eps-certificate-sha256', '--lo-certificate', '--lo-certificate-sha256'))
                         and am.get('--uv-tail-sidecar-directory') is not None and str(Path(am['--uv-tail-sidecar-directory']).resolve()) == str(side.resolve()))
    det['attempts'] = fn['attempts']
    det['single_attempt'] = fn['attempts'] == ['attempt_000']
    st = fn['start'] or {}
    det['D2_start_json_record'] = st.get('uv_tail') == rec
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


def stray_uv_tail(run):
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
    run = Path(run)
    for p in sorted(run.rglob('*.json')):
        if '/checkpoint/' in str(p) or p.is_symlink():
            continue
        try:
            walk(json.loads(p.read_text()), str(p.relative_to(run)))
        except ValueError:
            continue
    for p in sorted(run.rglob('*.jsonl')):
        hit, tail = False, b''
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 22), b''):
                if b'"uv_tail' in tail + b:
                    hit = True
                    break
                tail = b[-16:]
        if hit:
            out.append({'at': str(p.relative_to(run)) + ':JSONL_TEXT', 'enabled': None})
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
    exp = {N.s(str(Path(p).resolve())): N.s(s) for p, s in (drv.AUX_UVT['controller'], drv.UVT_LIB['lib'], drv.UVT_LIB['roster'], drv.UVT_LIB['provider'])}
    req = new / 'inputs' / ('uv_tail_route_a_request.json' if gate == 'Z2' else OFF_REQUEST_NAME)
    exp[N.s(str(req.resolve()))] = N.s(_sha_or(req))
    return exp


def static_pin_verifier(N):
    """top-level start.json static_pins: a NEW-only pin is admitted only when the raw path's bytes hash to the raw value."""
    rev = {}

    def ok(key_norm, val_norm):
        raw = rev.get(key_norm)
        return raw is not None and file_ok(raw[0], raw[1])
    return ok, rev


def compare_json_file(rel, p, q, R, N, rules, pin_allow, _unused=None):
    x = R.norm(read_json(p))
    y = N.norm(read_json(q))
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
    x = [R.norm(json.loads(l), drop=extra_mask) for l in p.read_text().splitlines() if l.strip()]
    y = [N.norm(json.loads(l), drop=extra_mask) for l in q.read_text().splitlines() if l.strip()]
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
    DRIVER[:] = list(DRIVERS[a.driver])
    tail_on, ro1_req, declared_off = GATES[a.gate]
    if ro1_req == 'UNARMED' and a.require_ro1_armed:
        raise SystemExit('REFUSED: --require-ro1-armed contradicts gate %s (A52.1: ro1 armed false, fired false)' % a.gate)
    if ro1_req == 'OPTIONAL' and a.require_ro1_armed:
        ro1_req = 'ARMED_BLOCK_ONLY'
    MASK_KEYS.clear(); MASK_KEYS.update(MASK_KEYS_BASE | (TAIL_KEYS if tail_on else set()))
    ref, new = Path(a.reference).resolve(), Path(a.new).resolve()
    tok = json.loads(Path(a.tokens).read_text())['declared']
    if sha_file(DRIVER[0]) != DRIVER[1]:
        raise SystemExit('driver pin')
    new_t = driver_tables(DRIVER[0])
    drv = load_driver()
    checks = {}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
    TR, TN = Tree(ref), Tree(new)
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
    auto, auto_rep = auto_custody(a.gate, ref, new, sr, sn, new_t, tuple(drv.UVT_TAIL_KINDS))
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
    tok_all = tok + auto + led_tokens
    R = Side(ref, [(r, t) for r, n, t in tok_all])
    N = Side(new, [(n, t) for r, n, t in tok_all])
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
                x, y = R.norm(read_json(ka[k]), RECORD_DROP), N.norm(read_json(kb[k]), RECORD_DROP)
                if not seq(x, y):
                    lbad.append({'dir': d, 'record': k, 'differing': diffs(x, y)[:4]})
    put('ATTEMPT_LEDGER', not lbad, {'directories': {d: [len(led_r.get(d) or {}), len(led_n.get(d) or {})] for d in sorted(set(led_r) | set(led_n))},
                                     'tokens': [t[2] for t in led_tokens], 'differing': lbad[:8]})
    # ---------------- INVENTORY (real paths; symlinks fail)
    ref_only = sorted(set(inv_r) - set(inv_n))
    new_only = sorted(set(inv_n) - set(inv_r))
    pats = [(re.compile(p + r'\Z'), why) for p, why in DECLARED_NEW_ONLY[a.gate]]
    adm_new, undeclared = {}, []
    for rel in new_only:
        hit = [why for rx, why in pats if rx.match(rel)]
        (adm_new.setdefault(hit[0], []).append(rel)) if hit else undeclared.append(rel)
    put('INVENTORY', not ref_only and not undeclared and not TR.links and not TN.links,
        {'n_files': [len(TR.files), len(TN.files)], 'reference_only': ref_only[:20], 'n_reference_only': len(ref_only),
         'new_only_undeclared': undeclared[:20], 'n_new_only_undeclared': len(undeclared),
         'new_only_declared': {k: {'n': len(v), 'first': v[:6]} for k, v in adm_new.items()},
         'symlinks': {'reference': TR.links[:10], 'new': TN.links[:10]}})
    # ---------------- NEW_DRIVER_PIN (A67 N1) and SCRIPT_CUSTODY (A59 raw)
    st_n = read_json(new / 'start.json')
    rn_raw = read_json(new / 'result.json')
    rr_raw = read_json(ref / 'result.json')
    put('NEW_DRIVER_PIN', [st_n.get('driver'), st_n.get('driver_sha256')] == DRIVER and rn_raw.get('driver_sha256') == DRIVER[1]
        and sha_file(DRIVER[0]) == DRIVER[1],
        {'selected': a.driver, 'pin': list(DRIVER), 'start_json': [st_n.get('driver'), st_n.get('driver_sha256')],
         'result_json_driver_sha256': rn_raw.get('driver_sha256', '<ABSENT>')})
    sc_bad, sc_rows = [], {}
    for name, d in sn.items():
        if not (d / 'request.json').is_file():
            continue
        q = read_json(d / 'request.json')
        kind, exp = planned_script(a.gate, name, q, drv)
        got = (q.get('script'), q.get('script_sha256'))
        ok = exp is not None and got == (str(exp[0]), exp[1]) and file_ok(str(exp[0]), exp[1])
        sc_rows[name] = {'kind': kind, 'script_sha256': got[1], 'planned_sha256': exp[1] if exp else None, 'ok': ok}
        if not ok:
            sc_bad.append({'stage': name, 'kind': kind, 'got': list(got), 'planned': [str(exp[0]), exp[1]] if exp else None})
    put('SCRIPT_CUSTODY', not sc_bad, {'rule': 'A59: every new stage runs the driver-planned script for gate %s, hashed from bytes' % a.gate,
                                       'stages': sc_rows, 'violations': sc_bad[:12]})
    # ---------------- route A
    fr, fn = route_a_facts(ref, sr), route_a_facts(new, sn)
    cn_raw, declared_rec, expected_stray, E = None, None, set(), None
    ra_r, ra_n = sr.get('route_a'), sn.get('route_a')
    if ra_n is not None and (ra_n / 'checkpoint/IDENTITY.json').is_file():
        cn_raw = cm.decode(cm._read(str(ra_n / 'checkpoint/IDENTITY.json'), 'identity')['identity']['caller']['record'])
    if declared_off:
        ok, det, declared_rec, expected_stray, E = check_declared_off(drv, new, fn, cn_raw)
        put('UV_TAIL_DECLARED', ok, det)
    exp_ra_pins = ra_new_pins(a.gate, drv, N, new)
    if ra_r is not None and ra_n is not None:
        br, bn = ra_r / 'checkpoint/blobs', ra_n / 'checkpoint/blobs'
        fr_b = {p.name: sha_file(p) for p in br.iterdir()} if br.is_dir() else {}
        fn_b = {p.name: sha_file(p) for p in bn.iterdir()} if bn.is_dir() else {}
        compared.update('stages/route_a/checkpoint/blobs/' + k for k in fr_b)
        put('RA_BLOBS', fr_b == fn_b and bool(fr_b), {'n': [len(fr_b), len(fn_b)], 'differing': sorted(set(fr_b) ^ set(fn_b) | {k for k in fr_b if fn_b.get(k) != fr_b[k]})[:10]})
        bad, n = [], 0
        for p in sorted((ra_r / 'checkpoint').glob('iteration_*/*.json')):
            q = ra_n / 'checkpoint' / p.relative_to(ra_r / 'checkpoint')
            n += 1
            compared.add(TR.canon(str(p.relative_to(ref))))
            if not q.is_file():
                bad.append(str(p.relative_to(ra_r)) + ' MISSING')
                continue
            x, y = R.norm(read_json(p), RECORD_DROP), N.norm(read_json(q), RECORD_DROP)
            if not seq(x, y):
                bad.append((str(p.relative_to(ra_r)), diffs(x, y)[:3]))
        nn = len(list((ra_n / 'checkpoint').glob('iteration_*/*.json')))
        put('RA_RECORDS', not bad and n == nn and n > 0, {'n': [n, nn], 'differing': bad[:8]})
        ir = cm._read(str(ra_r / 'checkpoint/IDENTITY.json'), 'identity')['identity']
        compared.add('stages/route_a/checkpoint/IDENTITY.json')
        cr = caller_norm(cm.decode(ir['caller']['record']), tail_on)
        if cn_raw is None:
            raise SystemExit('NEW route-A checkpoint IDENTITY.json missing: %s' % ra_n)
        cn = caller_norm(cn_raw, tail_on, declared_rec)
        x, y = R.norm(cr), N.norm(cn)
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
    blocks, rc = expected_tail_blocks(a.gate, drv, new, sn, (rn_raw.get('uv_tail') if isinstance(rn_raw, dict) else None))
    if a.gate == 'Z2':
        put('UV_TAIL_RECORD', rc is not None and all(v is True for v in rc.values()), rc)
        ok, det = check_manifest_stage(a.gate, drv, new, sn)
        put('MANIFEST_STAGE', ok, det)
    ok, det = check_requests(a.gate, R, N, sr, sn, blocks)
    put('REQUEST', ok, det)
    compared.update('stages/%s/request.json' % k for k in set(sr) & set(sn) if (sr[k] / 'request.json').is_file() and (sn[k] / 'request.json').is_file())
    # ---------------- STAGE_RECORDS (result.json stage_records tied to the run's own requests)
    sr_bad, sr_det = [], {}
    has = ['stage_records' in rr_raw, 'stage_records' in rn_raw]
    if has[0] != has[1]:
        sr_bad.append('stage_records present on one side only')
    elif has[0]:
        per = {}
        for tag, raw, T, S in (('reference', rr_raw, TR, R), ('new', rn_raw, TN, N)):
            recs = raw['stage_records']
            names = [r.get('name') for r in recs]
            with_req = [x for x in T.order if (T.stages[x] / 'request.json').is_file()]
            if names != with_req:
                sr_bad.append({'side': tag, 'why': 'stage_records names != stage directories with a request, in order', 'records': names, 'stages': with_req})
            per[tag] = {}
            for r in recs:
                nm = r.get('name')
                if nm not in T.stages or not (T.stages[nm] / 'request.json').is_file():
                    continue
                q = read_json(T.stages[nm] / 'request.json')
                core = {k: v for k, v in r.items() if k not in STAGE_RECORD_EXTRA}
                if not seq(core, q) or not set(r) - set(core) <= STAGE_RECORD_EXTRA:
                    sr_bad.append({'side': tag, 'stage': nm, 'why': 'record != own request.json', 'differing': diffs(q, core)[:4]})
                per[tag][nm] = S.norm({k: v for k, v in r.items() if k in STAGE_RECORD_EXTRA})
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
        file_rules['stages/route_a/attempt_000/start.json'] = [{'path': ('uv_tail',), 'rule': 'NEW_ONLY', 'value': N.norm(declared_rec),
                                                                 'why': 'D2 declared tail-off record (driver R5)'}]
    sp_ok, sp_rev = static_pin_verifier(N)
    for k, v in (st_n.get('static_pins') or {}).items():
        sp_rev[N.s(k)] = (k, v)
    # ---------------- RESULT
    x, y = R.norm(rr_raw), N.norm(rn_raw)
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
    route_a_files = set()
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
        if suf == '.npz':
            if npz_members(p) != npz_members(q):
                groups[g].append((rel, 'NPZ_CONTENT'))
        elif suf == '.npy':
            if npy_member(p) != npy_member(q):
                groups[g].append((rel, 'NPY_CONTENT'))
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
            ok, det, rep, pn = compare_json_file(rel, p, q, R, N, file_rules.get(rel, []), pin_allow, None)
            if rep:
                applied.append({'file': rel, 'rules': rep})
            if pn:
                pin_notes.append(pn)
            if not ok:
                groups[g].append(det)
        else:
            if p.read_bytes() != q.read_bytes():
                groups[g].append((rel, 'RAW_BYTES'))
    for g, bad in groups.items():
        put(g, not bad, {'compared': counts[g], 'differing': bad[:12], 'n_differing': len(bad)})
    checks['FILES_TOP']['detail']['declared_rules_applied'] = applied
    checks['FILES_TOP']['detail']['declared_new_only_pins'] = pin_notes[:20]
    if not tail_on:
        sr_, sn_ = stray_uv_tail(ref), stray_uv_tail(new)
        new_at = {s['at'] for s in sn_}
        # canonical form of the expected stray locations (real paths, as written by the run)
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
    # ---------------- coverage (a gate check in c2v005)
    unc = sorted(x for x in both if x not in compared and not (x.startswith('stages/') and Path(x).name in LOG_NAMES)
                 and not (x.startswith('stages/route_a/checkpoint/blobs/') or x == 'stages/route_a/checkpoint/IDENTITY.json'))
    # blobs and IDENTITY.json: compared by RA_BLOBS / RA_IDENTITY (added above when route A is present on both sides)
    logs = sorted(x for x in both if x.startswith('stages/') and Path(x).name in LOG_NAMES)
    put('COVERAGE', not unc, {'files_both_sides': len(both), 'logs_skipped': len(logs), 'not_compared_non_log': unc[:20],
                              'new_only_declared_not_compared': sum(len(v) for v in adm_new.values()),
                              'note': 'every both-side file except stage stdout/stderr is content-compared; new-only declared files have no counterpart'})
    rep = {'schema': 'RUN_IDENTITY_COMPARE_C2V005', 'gate': a.gate, 'driver_selected': a.driver, 'driver_pin': list(DRIVER),
           'tail_on': tail_on, 'ro1_requirement': ro1_req, 'declared_tail_off_records': declared_off, 'expected_tail_off_request_sha256': E,
           'require_ro1_armed_flag': bool(a.require_ro1_armed), 'masked_keys': sorted(MASK_KEYS),
           'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
           'auto_tokens_admitted': auto, 'attempt_tokens': led_tokens,
           'reference': str(ref), 'new': str(new), 'tokens': {'path': str(Path(a.tokens).resolve()), 'sha256': sha_file(a.tokens)},
           'tokens_fired': {'reference': R.fired, 'new': N.fired}, 'checks': checks,
           'verdict': 'PASS_BITWISE_EQUAL' if all(c['pass'] for c in checks.values()) else 'FAIL',
           'failing': [k for k, c in checks.items() if not c['pass']]}
    with open(a.out, 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({'verdict': rep['verdict'], 'failing': rep['failing']}))
    return 0 if rep['verdict'] == 'PASS_BITWISE_EQUAL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
