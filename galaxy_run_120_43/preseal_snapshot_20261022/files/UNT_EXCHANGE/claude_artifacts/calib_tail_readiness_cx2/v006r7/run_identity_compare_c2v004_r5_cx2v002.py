# Explicit 0540 r5 custody successor. Original c2v004 preserved; r4 descriptions below are inherited.
"""Run-output identity comparator for the V007 identity gates, c2v004 (Claude2 tail_scheme_impl_c2/gates_v004).
c2v004 = successor of gates_v003/run_identity_compare_c2v003.py (8f14f466) for root V005 addendum A57 ruling 3 (Codex3
FROM_CODEX3/0591, review_certs_gates_cx3/identity_specs_v002): the five comparator holes are closed.  Gates, masking, the RO1
checks and the declared tail-off records are c2v003's unchanged.  Changes (each is a new or stricter check; nothing is relaxed):
  H1 INVENTORY (extra files fail).  Every file of both run trees (stage numbers normalized: stages/NN_<name> -> stages/<name>) is
     inventoried.  A reference-only file FAILS.  A new-only file FAILS unless it matches the gate's declared additions, each cited
     to the pinned driver/tail code (DECLARED_NEW_ONLY below): Z2 (tail ON) the tail inputs, the route-A uv_tail sidecar and the
     route_a_tail_manifest stage; Z2_OFF_RO1 the tail-off request D1.  The checkpoint attempt ledger
     (checkpoint/attempts/<token>.{start,end}.json; token = time-pid-random, checkpoint module c2v003 L17/L511/L594) is paired by
     sorted token order and its records are content-compared (ATTEMPT_LEDGER).
  H2 .npy compared.  In the stage comparison every file is compared: .npz / .npy by content (dtype, shape, Fortran order, raw
     array bytes), .json / .jsonl normalized (strict, H5), request.json by REQUEST (H3); stdout.txt / stderr.txt are the only
     skipped names (logs; listed in the report's coverage); any other suffix by raw bytes.
  H3 REQUEST (request argv compared).  Every stage request.json present on both sides (route A and the route-B stages) is
     compared normalized and strict.  The new argv must equal the reference argv after removing exactly the gate's declared
     tail flags (DECLARED_ARGV; driver r4 L1103-1107, L2845-2850, L2955-2961), which must be absent from the reference and carry
     declared-shape values.
  H4 AUTO_CUSTODY (automatic script-custody tokens restricted to the declared driver map).  A stage whose request script
     differs between the runs is admitted only when (reference script, sha) is the REFERENCE run's driver table entry for that
     stage kind and (new script, sha) is the pinned driver r4 table entry the gate plans (DRIVER MAP below); the same for the
     route-A --solver pair and the start.json driver pair.  The reference driver must be one of REFERENCE_DRIVERS (path + sha
     from bytes); its tables are read by a restricted AST evaluator (constants, Path, '/', dict/tuple literals; nothing is
     executed).  Script files are hashed from bytes.  Only admitted pairs become tokens; any other pair FAILS and stays visible.
  H5 STRICT JSON.  JSON values are equal only with the same type (bool, int, float, str, None, list, dict are distinct) and,
     for floats, the same IEEE-754 bit pattern (so +0.0 != -0.0; 1 != 1.0; True != 1).  Applied to RA_RECORDS, RA_IDENTITY,
     ATTEMPT_LEDGER, STAGES, REQUEST and RESULT.
The report carries `coverage`: the file classes no check compares by content (top-level start/finish/progress, inputs/*, the
route-A attempt files other than arrays/*.npz and start.json, checkpoint.lock, stage logs), so PASS_BITWISE_EQUAL is read as
"every compared check", never "every byte of the tree" (Codex3 0591).
INERT on import; reads two completed run directories and the pinned code (read-only) and writes ONE report (exclusive create).

  python3 -I -B run_identity_compare_c2v004.py --gate GATE --reference REF_RUN --new NEW_RUN --tokens TOKENS.json --out REPORT.json

c2v003 text (gates and semantics unchanged):
  Z2          tail ON (unchanged c2v002 masking) + RO1 ARMED + RO1_CUSTODY.
  Z2_OFF_RO1  tail-OFF semantics except the declared enabled:false records D1-D3; RA_PINSET; RO1 ARMED + RO1_CUSTODY.
  Z2_OFF      c2v002 semantics (plain tail OFF; --require-ro1-armed optional).
  B0P_RERUN   tail-OFF semantics + RO1 UNARMED.  B0PRIME_RERUN is REFUSED (renamed).
TOKENS.json = {"declared": [[ref_string, new_string, token], ...]}; always tokenized: the run directory (<RUN>).  Masked keys:
elapsed_seconds, ended_unix_ns, started_unix_ns, utc, pid (and uv_tail, uv_tail_tap in Z2 only).  npz digests -> array-content
digest; a run JSON file's sha256 -> <JSONFILE:relative path>."""
import argparse
import ast
import hashlib
import importlib.util
import json
import re
import struct
import types
from pathlib import Path

CKPT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',
        '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
DRIVER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
          'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
# H4: drivers whose runs are identity-gate references (A52.1 / gates_v003 commands) plus r4 itself; path -> sha (from bytes).
REFERENCE_DRIVERS = {
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py':
        'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py':
        '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb',
    '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py':
        '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6',
    DRIVER[0]: DRIVER[1],
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
# H1: declared new-only files per gate (relative to the run, stage numbers normalized), with their source.
DECLARED_NEW_ONLY = {
    'Z2': [
        (r'inputs/uv_tail_config\.json', 'driver r4 L1091 ctx.write_input(uv_tail_config.json)'),
        (r'inputs/uv_tail_route_a_request\.json', 'driver r4 L1092 ctx.write_input(uv_tail_route_a_request.json)'),
        (r'stages/route_a/uv_tail_sidecar/(SIDECAR_IDENTITY\.json|iteration_\d{4}\.json|elements_\d{4}\.npz|finish_\d{3,4}\.json)',
         'driver r4 L2845 --uv-tail-sidecar-directory; controller 51d32e7b L29/L363/L495/L506'),
        (r'stages/route_a_tail_manifest/(request\.json|stdout\.txt|stderr\.txt)', 'driver r4 L2935-2941 (stage route_a_tail_manifest)'),
        (r'stages/route_a_tail_manifest/manifest/(ROUTE_A_TAIL_MANIFEST\.json|finish\.json|route_a_tail_state\.npz|route_a_gas_it_roster\.npz)',
         'manifest writer 5e716092 L169/L176/L187/L249'),
    ],
    'Z2_OFF_RO1': [(r'inputs/' + re.escape(OFF_REQUEST_NAME), 'driver r4 L2847 ctx.write_input (D1)')],
    'Z2_OFF': [],
    'B0P_RERUN': [],
}
# H3: declared tail argv flags (name -> takes a value) per gate and stage class.
UVT_ROUTE_B_FLAGS = {'--uv-tail-config': True, '--uv-tail-config-sha256': True, '--uv-tail-admit-test-only': False,
                     '--route-a-tail-manifest': True, '--route-a-tail-manifest-sha256': True, '--uv-tail-truncation': True,
                     '--uv-tail-source-rotation-directory': True}  # driver r4 L2955-2961 (uvt_argv), L1107
UVT_ROUTE_A_FLAGS = {'--uv-tail-config': True, '--uv-tail-config-sha256': True, '--eps-certificate': True, '--eps-certificate-sha256': True,
                     '--lo-certificate': True, '--lo-certificate-sha256': True, '--uv-tail-sidecar-directory': True}  # L1103-1105, L2845, L2848-2850
DECLARED_ARGV = {'Z2': {'route_a': UVT_ROUTE_A_FLAGS, '*': UVT_ROUTE_B_FLAGS}, 'Z2_OFF_RO1': {'route_a': UVT_ROUTE_A_FLAGS},
                 'Z2_OFF': {}, 'B0P_RERUN': {}}
TABLE_NAMES = ('SCRIPTS', 'AUX', 'PARALLEL_ROUTE_A', 'RO1_ROUTE_A', 'SCRIPTS_UVT', 'AUX_UVT')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def load_cm():
    # 0540 N4: execute the exact bytes whose SHA256 was verified.
    raw = Path(CKPT[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CKPT[1]:
        raise SystemExit('checkpoint module pin')
    m = types.ModuleType('ckpt_cmp_c2v004_r5')
    m.__file__ = CKPT[0]
    exec(compile(raw, CKPT[0], 'exec'), m.__dict__)
    return m


def load_driver():
    """The pinned driver r4, executed from the verified bytes (module body: constants and defs only), as c2v003."""
    raw = Path(DRIVER[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != DRIVER[1]:
        raise SystemExit('driver pin')
    m = types.ModuleType('v010r4_cmp_c2v004')
    m.__file__ = DRIVER[0]
    exec(compile(raw, DRIVER[0], 'exec'), m.__dict__)
    return m


# ---------------------------------------------------------------- H4: restricted AST evaluation of a driver's tables
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
    """Top-level simple assignments evaluated in order by _ev (failures skipped); returns {table: {kind: (path str, sha)}}."""
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


# ---------------------------------------------------------------- H5: strict JSON equality
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


def off_request_bytes(drv):
    return (json.dumps(drv._jsonable(drv.ro1_off_request()), indent=1, allow_nan=False) + '\n').encode()


def npz_members(p):
    import numpy as np
    with np.load(p, allow_pickle=False) as f:
        return {k: (f[k].dtype.str, tuple(f[k].shape), hashlib.sha256(np.ascontiguousarray(f[k]).tobytes()).hexdigest()) for k in f.files}


def npy_member(p):
    """H2: content of a .npy (dtype, shape, Fortran order, raw bytes); allow_pickle False."""
    import numpy as np
    a = np.load(p, allow_pickle=False)
    return (a.dtype.str, tuple(a.shape), bool(a.flags.f_contiguous and not a.flags.c_contiguous),
            hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest())


def content_digest(p):
    return hashlib.sha256(json.dumps(sorted(npz_members(p).items())).encode()).hexdigest()


def rel_norm(run, p):
    return re.sub(r'^stages/\d\d_', 'stages/', str(Path(p).relative_to(run)))


class Side:
    def __init__(self, run, tokens):
        self.run = Path(run)
        self.tokens = sorted(tokens, key=lambda t: -len(t[0]))
        self.hexmap = {}
        for p in self.run.rglob('*'):
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


PIN_DICTS = ('code_pins', 'input_pins', 'dependency_pins', 'source_pins', 'static_pins', 'pins', 'module_pins')


def align_pins(a, b, path, notes):
    """c2v003 declared custody rule: pin dictionaries compared on keys present on BOTH sides; one-side keys listed."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) & set(b)):
            if k in PIN_DICTS and isinstance(a[k], dict) and isinstance(b[k], dict):
                only = sorted(set(a[k]) ^ set(b[k]))
                if only:
                    notes.append({'at': path + '/' + k, 'one_side_only': only[:12], 'n': len(only)})
                common = set(a[k]) & set(b[k])
                a[k] = {x: a[k][x] for x in common}
                b[k] = {x: b[k][x] for x in common}
            else:
                align_pins(a[k], b[k], path + '/' + k, notes)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            align_pins(x, y, '%s[%d]' % (path, i), notes)


def stage_dirs(run):
    d = Path(run) / 'stages'
    return {re.sub(r'^\d\d_', '', x.name): x for x in sorted(d.iterdir()) if x.is_dir()} if d.is_dir() else {}


def argv_map(argv):
    return dict(zip(argv[::2], argv[1::2]))


def read_json(p):
    return json.loads(Path(p).read_text())


# ---------------------------------------------------------------- H4 driver map
def expected_scripts(gate, kind, workers, ref_t, new_t, uvt_kinds):
    """(reference (path, sha) or None, new (path, sha) or None) for a stage kind under this gate (driver r4 L2832-2865, L1821)."""
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


def auto_custody(gate, ref, new, new_t, uvt_kinds):
    """H4: candidate pairs exactly as c2v003 auto_tokens derived them, each classified against the declared driver map.
    Returns (admitted token triples, report)."""
    rep = {'reference_driver': None, 'pairs': [], 'inadmissible': []}
    st_r, st_n = read_json(ref / 'start.json'), read_json(new / 'start.json')
    rdrv, rsha = st_r.get('driver'), st_r.get('driver_sha256')
    ref_t, rd_ok = {}, False
    if isinstance(rdrv, str) and REFERENCE_DRIVERS.get(rdrv) == rsha and Path(rdrv).is_file() and sha_file(rdrv) == rsha:
        ref_t, rd_ok = driver_tables(rdrv), True
    rep['reference_driver'] = {'path': rdrv, 'sha256': rsha, 'declared_and_verified_from_bytes': rd_ok,
                               'tables': sorted(ref_t)}
    admitted = []

    def file_ok(path, sha):
        return Path(path).is_file() and sha_file(path) == sha

    sr, sn = stage_dirs(ref), stage_dirs(new)
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
            continue
        a, b = read_json(qr), read_json(qn)
        if a.get('script') == b.get('script') and a.get('script_sha256') == b.get('script_sha256'):
            pass
        else:
            ka, kb = a.get('kind'), b.get('kind')
            kind = ka if ka == kb and ka is not None else (name if ka is None and kb is None and name in ('route_a', 'reference', 'body', 'offset') else None)
            workers = int(argv_map(b.get('argv') or []).get('--column-workers', 1)) if name == 'route_a' else 1
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
                workers = int(mb.get('--column-workers', 1))
                exp_r, exp_n = expected_solver(gate, workers, ref_t, new_t) if rd_ok else (None, None)
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
        ok = rd_ok and nd == DRIVER and sha_file(DRIVER[0]) == DRIVER[1]
        row = {'what': 'driver', 'reference': [rdrv, rsha], 'new': list(nd), 'expected_new': list(DRIVER), 'admitted': ok}
        rep['pairs'].append(row)
        if ok:
            admitted += [[rdrv, nd[0], '<DRIVER_DRIVER>'], [rsha, nd[1], '<DRIVER_DRIVER_SHA256>']]
        else:
            rep['inadmissible'].append(row)
    return admitted, rep


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
        if '/checkpoint/' in str(p):
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


def route_a_facts(run):
    d = stage_dirs(run).get('route_a')
    if d is None or not (d / 'request.json').is_file():
        return None
    req = read_json(d / 'request.json')
    atts = sorted(x.name for x in d.glob('attempt_*') if x.is_dir())
    st = d / 'attempt_000' / 'start.json'
    return {'dir': d, 'request': req, 'argv': argv_map(req.get('argv') or []), 'attempts': atts,
            'start': read_json(st) if st.is_file() else None}


def ro1_expectations(drv, fn):
    n = int(fn['argv'].get('--column-workers', 1)) if fn else 1
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
    ref_pins = (fr or {}).get('start', {}) or {}
    ref_pins = ref_pins.get('input_pins') or {}
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


# ---------------------------------------------------------------- H1 inventory
def inventory(run):
    run = Path(run)
    return {rel_norm(run, p): p for p in run.rglob('*') if p.is_file() or p.is_symlink()}


def check_inventory(gate, R, N):
    ir, inn = inventory(R.run), inventory(N.run)
    led_r, led_n = {}, {}
    for inv, led in ((ir, led_r), (inn, led_n)):
        for rel in list(inv):
            m = ATTEMPT_RE.match(rel)
            if m:
                led.setdefault(m.group(1), {}).setdefault(m.group(2), {})[m.group(3)] = inv.pop(rel)
    ref_only = sorted(set(ir) - set(inn))
    new_only = sorted(set(inn) - set(ir))
    pats = [(re.compile(p + r'\Z'), why) for p, why in DECLARED_NEW_ONLY[gate]]
    admitted, undeclared = {}, []
    for rel in new_only:
        hit = [why for rx, why in pats if rx.match(rel)]
        if hit:
            admitted.setdefault(hit[0], []).append(rel)
        else:
            undeclared.append(rel)
    # attempt ledger: paired by sorted token order per directory, same record kinds, content strict after masking
    lbad = []
    for d in sorted(set(led_r) | set(led_n)):
        tr, tn = sorted((led_r.get(d) or {}).items()), sorted((led_n.get(d) or {}).items())
        if len(tr) != len(tn):
            lbad.append({'dir': d, 'tokens': [len(tr), len(tn)]})
            continue
        for (ta, ka), (tb, kb) in zip(tr, tn):
            if set(ka) != set(kb):
                lbad.append({'dir': d, 'kinds': [sorted(ka), sorted(kb)]})
                continue
            for k in sorted(ka):
                x, y = R.norm(read_json(ka[k]), RECORD_DROP), N.norm(read_json(kb[k]), RECORD_DROP)
                if not seq(x, y):
                    lbad.append({'dir': d, 'record': k, 'differing': diffs(x, y)[:4]})
    inv_ok = not ref_only and not undeclared
    led_ok = not lbad
    det = {'n_files': [len(ir), len(inn)], 'reference_only': ref_only[:20], 'n_reference_only': len(ref_only),
           'new_only_undeclared': undeclared[:20], 'n_new_only_undeclared': len(undeclared),
           'new_only_declared': {k: {'n': len(v), 'first': v[:6]} for k, v in admitted.items()}}
    ldet = {'directories': {d: [len(led_r.get(d) or {}), len(led_n.get(d) or {})] for d in sorted(set(led_r) | set(led_n))},
            'differing': lbad[:8]}
    return (inv_ok, det), (led_ok, ldet), ir, inn


# ---------------------------------------------------------------- H3 request comparison
def split_declared_argv(argv, flags):
    """Remove declared flags (and their value when the flag takes one) from argv; returns (rest, removed {flag: value or None})."""
    rest, removed, i = [], {}, 0
    while i < len(argv):
        t = argv[i]
        if t in flags:
            if flags[t]:
                removed[t] = argv[i + 1] if i + 1 < len(argv) else '<MISSING_VALUE>'
                i += 2
            else:
                removed[t] = None
                i += 1
            continue
        rest.append(t)
        i += 1
    return rest, removed


def declared_value_ok(flag, v, tail_on):
    """Shape of a declared tail flag value (normalized): paths inside the run, shas the run's own JSON files, the test-only
    certificate sentinel, the JSON truncation, or no value."""
    if flag == '--uv-tail-admit-test-only':
        return v is None
    if flag == '--uv-tail-truncation':
        try:
            json.loads(v)
            return True
        except (TypeError, ValueError):
            return False
    if flag in ('--eps-certificate', '--eps-certificate-sha256', '--lo-certificate', '--lo-certificate-sha256'):
        return v == 'NONE_TEST_ONLY'
    if flag.endswith('-sha256'):
        return isinstance(v, str) and v.startswith('<JSONFILE:') and v.endswith('>')
    return isinstance(v, str) and v.startswith('<RUN>/')


def check_requests(gate, R, N, sr, sn, tail_on):
    bad, n, removed_all = [], 0, {}
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
            if qr.is_file() != qn.is_file():
                bad.append((name, 'request.json present on one side only'))
            continue
        n += 1
        a, b = R.norm(read_json(qr)), N.norm(read_json(qn))
        flags = DECLARED_ARGV[gate].get(name, DECLARED_ARGV[gate].get('*', {})) if name != 'route_a' else DECLARED_ARGV[gate].get('route_a', {})
        ra, rem_r = split_declared_argv(a.get('argv') or [], flags)
        rb, rem_n = split_declared_argv(b.get('argv') or [], flags)
        if rem_r:
            bad.append((name, 'declared tail flags on the reference side', sorted(rem_r)))
        badv = {f: v for f, v in rem_n.items() if not declared_value_ok(f, v, tail_on)}
        if badv:
            bad.append((name, 'declared tail flag value of undeclared shape', badv))
        if rem_n:
            removed_all[name] = rem_n
        a2, b2 = dict(a, argv=ra), dict(b, argv=rb)
        if not seq(a2, b2):
            bad.append((name, diffs(a2, b2)[:4]))
    return not bad, {'requests_compared': n, 'differing': bad[:12], 'declared_tail_flags_removed': removed_all}


# ---------------------------------------------------------------- main
def main(argv=None, *, _return_report=False):
    ap = argparse.ArgumentParser()
    for k in ('reference', 'new', 'tokens', 'out'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--gate', required=True)
    ap.add_argument('--require-ro1-armed', action='store_true')
    a = ap.parse_args(argv)
    if a.gate in RETIRED_GATES:
        raise SystemExit('REFUSED: ' + RETIRED_GATES[a.gate])
    if a.gate not in GATES:
        raise SystemExit('REFUSED: unknown gate %r (one of %s)' % (a.gate, sorted(GATES)))
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
    auto, auto_rep = auto_custody(a.gate, ref, new, new_t, tuple(drv.UVT_TAIL_KINDS))
    tok_all = tok + auto
    R = Side(ref, [(r, t) for r, n, t in tok_all])
    N = Side(new, [(n, t) for r, n, t in tok_all])
    cm = load_cm()
    checks = {}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
    put('AUTO_CUSTODY', not auto_rep['inadmissible'], auto_rep)
    sr, sn = stage_dirs(R.run), stage_dirs(N.run)
    fr, fn = route_a_facts(R.run), route_a_facts(N.run)
    cn_raw, declared_rec, expected_stray, E = None, None, set(), None
    ra_r, ra_n = sr.get('route_a'), sn.get('route_a')
    if ra_n is not None and (ra_n / 'checkpoint/IDENTITY.json').is_file():
        cn_raw = cm.decode(cm._read(str(ra_n / 'checkpoint/IDENTITY.json'), 'identity')['identity']['caller']['record'])
    if declared_off:
        ok, det, declared_rec, expected_stray, E = check_declared_off(drv, N.run, fn, cn_raw)
        put('UV_TAIL_DECLARED', ok, det)
    (inv_ok, inv_det), (led_ok, led_det), inv_r, inv_n = check_inventory(a.gate, R, N)
    put('INVENTORY', inv_ok, inv_det)
    put('ATTEMPT_LEDGER', led_ok, led_det)
    compared = set()
    # ---------------- route A (c2v003, strict)
    if ra_r is not None and ra_n is not None:
        br, bn = ra_r / 'checkpoint/blobs', ra_n / 'checkpoint/blobs'
        fr_b = {p.name: sha_file(p) for p in br.iterdir()} if br.is_dir() else {}
        fn_b = {p.name: sha_file(p) for p in bn.iterdir()} if bn.is_dir() else {}
        compared.update('stages/route_a/checkpoint/blobs/' + k for k in fr_b)
        put('RA_BLOBS', fr_b == fn_b and fr_b, {'n': [len(fr_b), len(fn_b)], 'differing': sorted(set(fr_b) ^ set(fn_b) | {k for k in fr_b if fn_b.get(k) != fr_b[k]})[:10]})
        bad, n = [], 0
        for p in sorted((ra_r / 'checkpoint').glob('iteration_*/*.json')):
            q = ra_n / 'checkpoint' / p.relative_to(ra_r / 'checkpoint')
            n += 1
            compared.add(rel_norm(R.run, p))
            if not q.is_file():
                bad.append(str(p.relative_to(ra_r)) + ' MISSING')
                continue
            x, y = R.norm(read_json(p), RECORD_DROP), N.norm(read_json(q), RECORD_DROP)
            if not seq(x, y):
                bad.append((str(p.relative_to(ra_r)), diffs(x, y)[:3]))
        nn = len(list((ra_n / 'checkpoint').glob('iteration_*/*.json')))
        put('RA_RECORDS', not bad and n == nn and n, {'n': [n, nn], 'differing': bad[:8]})
        ar, an = sorted((ra_r / 'attempt_000/arrays').glob('*.npz')), sorted((ra_n / 'attempt_000/arrays').glob('*.npz'))
        compared.update(rel_norm(R.run, p) for p in ar)
        badA = [p.name for p, q in zip(ar, an) if p.name != q.name or npz_members(p) != npz_members(q)]
        put('RA_ARRAYS', len(ar) == len(an) and ar and not badA, {'n': [len(ar), len(an)], 'differing': badA[:10]})
        ir = cm._read(str(ra_r / 'checkpoint/IDENTITY.json'), 'identity')['identity']
        compared.add('stages/route_a/checkpoint/IDENTITY.json')
        cr = caller_norm(cm.decode(ir['caller']['record']), tail_on)
        if cn_raw is None:
            raise SystemExit('NEW route-A checkpoint IDENTITY.json missing: %s' % ra_n)
        cn = caller_norm(cn_raw, tail_on, declared_rec)
        x, y = R.norm(cr), N.norm(cn)
        if declared_off:
            xp, yp = x.get('code_pins') or {}, y.get('code_pins') or {}
            exp = {N.s(str(Path(p).resolve())): N.s(s) for p, s in (drv.AUX_UVT['controller'], drv.UVT_LIB['lib'], drv.UVT_LIB['roster'], drv.UVT_LIB['provider'])}
            exp[N.s(str((N.run / 'inputs' / OFF_REQUEST_NAME).resolve()))] = N.s(E)
            ref_only, new_only = sorted(set(xp) - set(yp)), sorted(set(yp) - set(xp))
            put('RA_PINSET', not ref_only and set(new_only) == set(exp) and all(yp.get(k) == v for k, v in exp.items()),
                {'reference_only': ref_only, 'new_only': new_only, 'expected_new_only': sorted(exp),
                 'value_mismatch': sorted(k for k, v in exp.items() if k in yp and yp[k] != v)})
        notes = []
        align_pins({'caller': x}, {'caller': y}, 'IDENTITY', notes)
        notes.sort(key=lambda d: d['at'])
        put('RA_IDENTITY', seq(x, y), {'differing': diffs(x, y)[:8], 'declared_pin_set_differences': notes})
    else:
        put('RA_PRESENT', ra_r is None and ra_n is None and not declared_off, {'reference': str(ra_r), 'new': str(ra_n)})
    # ---------------- requests (H3)
    ok, det = check_requests(a.gate, R, N, sr, sn, tail_on)
    put('REQUEST', ok, det)
    compared.update('stages/%s/request.json' % k for k in set(sr) & set(sn))
    # ---------------- route B stages (H2, H5)
    bad, n_arr, n_npy, n_json, n_raw, pin_notes, skipped = [], 0, 0, 0, 0, [], 0
    for name, dr in sr.items():
        if name == 'route_a':
            continue
        dn = sn.get(name)
        if dn is None:
            bad.append((name, 'MISSING_IN_NEW'))
            continue
        for p in sorted(dr.rglob('*')):
            if not p.is_file() or p.name == 'request.json':
                continue
            if p.name in LOG_NAMES:
                skipped += 1
                continue
            q = dn / p.relative_to(dr)
            if not q.is_file():
                bad.append((name, str(p.relative_to(dr)), 'MISSING'))
                continue
            compared.add(rel_norm(R.run, p))
            if p.suffix == '.npz':
                n_arr += 1
                if npz_members(p) != npz_members(q):
                    bad.append((name, str(p.relative_to(dr)), 'NPZ_CONTENT'))
            elif p.suffix == '.npy':
                n_npy += 1
                if npy_member(p) != npy_member(q):
                    bad.append((name, str(p.relative_to(dr)), 'NPY_CONTENT'))
            elif p.suffix in ('.json', '.jsonl'):
                n_json += 1
                if p.suffix == '.jsonl':
                    x = [R.norm(json.loads(l)) for l in p.read_text().splitlines() if l.strip()]
                    y = [N.norm(json.loads(l)) for l in q.read_text().splitlines() if l.strip()]
                else:
                    x, y = R.norm(read_json(p)), N.norm(read_json(q))
                align_pins(x, y, '%s/%s' % (name, p.relative_to(dr)), pin_notes)
                if not seq(x, y):
                    bad.append((name, str(p.relative_to(dr)), diffs(x, y)[:3]))
            else:
                n_raw += 1
                if p.read_bytes() != q.read_bytes():
                    bad.append((name, str(p.relative_to(dr)), 'RAW_BYTES'))
    extra = sorted(set(sn) - set(sr))
    put('STAGES', not bad and set(extra) <= ({'route_a_tail_manifest'} if tail_on else set()),
        {'arrays_compared': n_arr, 'npy_compared': n_npy, 'json_compared': n_json, 'raw_compared': n_raw, 'logs_skipped': skipped,
         'differing': bad[:12], 'extra_stages_new': extra,
         'declared_pin_set_differences': pin_notes[:40], 'n_pin_notes': len(pin_notes)})
    # ---------------- result (strict)
    rr, rn = read_json(R.run / 'result.json'), read_json(N.run / 'result.json')
    compared.add('result.json')
    keys = ('status', 'valid', 'final_pass', 'speeds_km_s', 'rows')
    pr = [[p.get('pass'), p.get('rows'), p.get('max_abs_change_km_s')] for p in rr.get('passes') or []]
    pn = [[p.get('pass'), p.get('rows'), p.get('max_abs_change_km_s')] for p in rn.get('passes') or []]
    put('RESULT', all(seq(rr.get(k), rn.get(k)) for k in keys) and seq(pr, pn) and rr.get('status') == 'COMPLETED',
        {'differing': [k for k in keys if not seq(rr.get(k), rn.get(k))], 'passes_equal': seq(pr, pn), 'status': [rr.get('status'), rn.get('status')],
         'passes_differing': diffs(pr, pn)[:4]})
    if not tail_on:
        sr_, sn_ = stray_uv_tail(R.run), stray_uv_tail(N.run)
        new_at = {s['at'] for s in sn_}
        admitted = sorted(new_at & expected_stray)
        undeclared = [s for s in sn_ if s['at'] not in expected_stray]
        put('STRAY_UV_TAIL', not sr_ and not undeclared and new_at >= expected_stray,
            {'reference': sr_[:12], 'new_undeclared': undeclared[:12], 'new_admitted_declared': admitted,
             'declared_missing': sorted(expected_stray - new_at)})
    if ro1_req == 'ARMED':
        n_workers, worker = ro1_expectations(drv, fn)
        ok, det = check_ro1_armed(ro1_block(rn), worker[1], drv.RO1_ROUTE_A['binding'][1])
        det['route_a_column_workers'] = n_workers
        put('RO1', ok, det)
        ok, det = check_custody(drv, tok_all, fr, fn, worker)
        put('RO1_CUSTODY', ok, det)
    elif ro1_req == 'ARMED_BLOCK_ONLY':
        ro1 = ro1_block(rn)
        put('RO1', isinstance(ro1, dict) and ro1.get('armed') is True and ro1.get('fired') is False, {'new_ro1': ro1})
    elif ro1_req == 'UNARMED':
        ok, det = check_ro1_unarmed(ro1_block(rn))
        put('RO1', ok, det)
    # ---------------- coverage (what no check compares by content)
    both = set(inv_r) & set(inv_n)
    unc = sorted(x for x in both if x not in compared)
    cls = {}
    for x in unc:
        k = re.sub(r'\d+', '#', x)
        cls[k] = cls.get(k, 0) + 1
    coverage = {'files_both_sides': len(both), 'content_compared': len(both) - len(unc), 'not_content_compared': len(unc),
                'not_content_compared_classes': cls,
                'note': 'not content-compared files still pass INVENTORY (present on both sides); PASS_BITWISE_EQUAL covers the checks only'}
    rep = {'schema': 'RUN_IDENTITY_COMPARE_C2V004', 'gate': a.gate, 'tail_on': tail_on, 'ro1_requirement': ro1_req,
           'declared_tail_off_records': declared_off, 'expected_tail_off_request_sha256': E,
           'require_ro1_armed_flag': bool(a.require_ro1_armed),
           'masked_keys': sorted(MASK_KEYS), 'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
           'driver_pin': list(DRIVER), 'auto_tokens_admitted': auto,
           'reference': str(R.run), 'new': str(N.run), 'tokens': {'path': str(Path(a.tokens).resolve()), 'sha256': sha_file(a.tokens)},
           'tokens_fired': {'reference': R.fired, 'new': N.fired}, 'checks': checks, 'coverage': coverage,
           'verdict': 'PASS_BITWISE_EQUAL' if all(c['pass'] for c in checks.values()) else 'FAIL',
           'failing': [k for k, c in checks.items() if not c['pass']]}
    rep['r5_adapter'] = {'schema': 'C2V004_R5_CUSTODY_ADAPTER_CX2V002', 'base_comparator': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004/run_identity_compare_c2v004.py', 'sha256': 'e3d153b6dd5bf07ffd74ca8eeb75087d7a1bfd5cab67039c5514fa8744f7abcf'}, 'change': 'DRIVER r4 to r5; comparison checks and masks unchanged; optional read-only report return; hashed-byte checkpoint loader'}
    if _return_report:
        return rep
    with open(a.out, 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({'verdict': rep['verdict'], 'failing': rep['failing']}))
    return 0 if rep['verdict'] == 'PASS_BITWISE_EQUAL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
