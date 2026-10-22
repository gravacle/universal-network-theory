"""Run-output identity comparator for the V007 identity gates, c2v003 (Claude2 tail_scheme_impl_c2/gates_v003).
c2v003 = successor of driver_r4/gates/run_identity_compare_c2v002.py (f7bb7e7f) for driver_r4 CHECK K1 and root V005 addendum
A52 rulings 1-2 (open addendum, cited by name; frozen pin V004 addendum 487d4449).  Gates (--gate, required):
  Z2          tail ON (unchanged c2v002 masking) + RO1 ARMED (built in, A50 item 12 / A52.1): result.route_a_outcome.ro1 armed True,
              fired False, events [], worker = the RO1 c2v002 worker of the route-A column_workers, binding = RO1 c2v002 binding;
              RO1_CUSTODY: worker, binding and facade swaps on the declared custody list (tokens), consistent with the reference.
  Z2_OFF_RO1  NEW (A52.2, K1).  Tail-OFF semantics (nothing masked; STRAY_UV_TAIL listed) EXCEPT the declared enabled:false
              records the RO1 c2v002 worker / driver r4 write on a ro1_workers tail-OFF call, admitted only at these three locations
              and only with exactly the declared content:
                D1 <NEW>/inputs/uv_tail_route_a_request_tail_off_ro1.json: bytes sha256 = the driver's tail-off request
                   (ro1_off_request() serialized as _write_x does), content = ro1_off_request();
                D2 <NEW>/stages/NN_route_a/attempt_000/start.json uv_tail = {request: {path D1, sha256 E}, enabled False,
                   sidecar_directory <NEW>/stages/NN_route_a/uv_tail_sidecar} (that sidecar must not exist);
                D3 checkpoint caller numerical_controls.uv_tail: ABSENT or exactly the D2 record (dropped from RA_IDENTITY only
                   when equal).  The worker sets it (d676ecb2 L98), but the RO1 binding 86af6198 L151 replaces the caller
                   numerical_controls by the prep controls when the controller is None, so a real run is predicted ABSENT
                   (code reading; the report records which state was observed).
              The route-A request argv must carry exactly the declared tail-off flags (D1 path, E, NONE_TEST_ONLY x4, sidecar).
              Any other uv_tail / uv_tail_tap record anywhere (JSON key walk outside checkpoint/, byte scan of every .jsonl) in
              either run FAILS.  RA_PINSET: caller code_pins keys present on one side only must be exactly the declared RO1-off
              additions (controller, module-lane lib/roster/provider, D1) with the driver's shas; nothing reference-only.
              RO1 ARMED + RO1_CUSTODY as Z2.
  Z2_OFF      c2v002 semantics unchanged (plain tail OFF; --require-ro1-armed optional).  Not an A52 identity gate (A52.1: "a plain
              Z2-OFF is not needed"); kept for regression and saved tail-OFF pairs.
  B0P_RERUN   tail-OFF semantics (Z2_OFF) + RO1 UNARMED (A52.1): ro1 a dict with armed False, fired False, events [],
              worker_sha256 None, binding_sha256 None, no inadmissible_record.  --require-ro1-armed is REFUSED with this gate.
  B0PRIME_RERUN (c2v002 name) is REFUSED: renamed B0P_RERUN with the A52.1 requirement.
Other c2v003 changes: --reference / --new are resolved (Path.resolve) before use; the driver r4 (b9ae92d5) is loaded from pinned
bytes (inert on import; no function that touches files is called) for RO1_ROUTE_A, AUX_UVT, UVT_LIB and ro1_off_request.
INERT on import; reads two completed run directories (read-only) and writes ONE report (exclusive create).  numpy only.

  python3 -I -B run_identity_compare_c2v003.py --gate GATE --reference REF_RUN --new NEW_RUN --tokens TOKENS.json --out REPORT.json

c2v002 text follows (method unchanged).
Method: compare_deciding_ii_c2v008 (b122b8e6) extended to every route-B stage (design V002 sec 4.3; R1 L3 exception list).
TOKENS.json = {"declared": [[ref_string, new_string, token], ...]} -- the declared custody list of the gate; each pair is replaced
by its token on its own side before comparing.  Always tokenized as well: the run directory (<RUN>).
Always masked: keys elapsed_seconds, ended_unix_ns, started_unix_ns, utc, pid (uv_tail, uv_tail_tap in the tail-ON gate Z2 only);
npz file digests are replaced by the digest of the referenced array CONTENT; the sha256 of a JSON file of the run is replaced by
<JSONFILE:relative path> (its content is compared on its own).
PASS (PASS_BITWISE_EQUAL) requires every check: RA_BLOBS, RA_RECORDS, RA_ARRAYS, RA_IDENTITY (or RA_PRESENT), STAGES, RESULT, and
the gate's STRAY_UV_TAIL / UV_TAIL_DECLARED / RA_PINSET / RO1 / RO1_CUSTODY.  Anything else differing is listed."""
import argparse
import hashlib
import importlib.util
import json
import re
import types
from pathlib import Path

CKPT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',
        '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
DRIVER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
          'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b')
MASK_KEYS_BASE = {'elapsed_seconds', 'ended_unix_ns', 'started_unix_ns', 'utc', 'pid'}
TAIL_KEYS = {'uv_tail', 'uv_tail_tap'}
MASK_KEYS = set(MASK_KEYS_BASE)  # set by main() from --gate
# gate -> (tail ON, RO1 requirement, declared tail-off RO1 records)
GATES = {'Z2': (True, 'ARMED', False), 'Z2_OFF_RO1': (False, 'ARMED', True), 'Z2_OFF': (False, 'OPTIONAL', False),
         'B0P_RERUN': (False, 'UNARMED', False)}
RETIRED_GATES = {'B0PRIME_RERUN': 'gate B0PRIME_RERUN is renamed B0P_RERUN in c2v003 (root V005 A52 ruling 1: ro1 armed false, fired false)'}
OFF_REQUEST_NAME = 'uv_tail_route_a_request_tail_off_ro1.json'
RECORD_DROP = {'attempt', 'payload_sha256', 'identity_sha256', 'iteration_start_sha256', 'checkpoint_identity_sha256'}
HEX = re.compile(r'[0-9a-f]{64}')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def load_cm():
    if sha_file(CKPT[0]) != CKPT[1]:
        raise SystemExit('checkpoint module pin')
    s = importlib.util.spec_from_file_location('ckpt_cmp_c2v003', CKPT[0])
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def load_driver():
    """The pinned driver r4, executed from the verified bytes (module body: constants and defs only)."""
    raw = Path(DRIVER[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != DRIVER[1]:
        raise SystemExit('driver pin')
    m = types.ModuleType('v010r4_cmp_c2v003')
    m.__file__ = DRIVER[0]
    exec(compile(raw, DRIVER[0], 'exec'), m.__dict__)
    return m


def off_request_bytes(drv):
    """The bytes the driver writes for the tail-off request (ctx.write_input -> _write_x: json.dump indent=1 + newline)."""
    return (json.dumps(drv._jsonable(drv.ro1_off_request()), indent=1, allow_nan=False) + '\n').encode()


def npz_members(p):
    import numpy as np
    with np.load(p, allow_pickle=False) as f:
        return {k: (f[k].dtype.str, tuple(f[k].shape), hashlib.sha256(np.ascontiguousarray(f[k]).tobytes()).hexdigest()) for k in f.files}


def content_digest(p):
    return hashlib.sha256(json.dumps(sorted(npz_members(p).items())).encode()).hexdigest()


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
    """Declared custody rule (design sec 4.3 exception list): pin dictionaries are compared on the keys present on BOTH
    sides; keys present on one side only are listed in the report, never silently ignored (c2v003: and, in the gate
    Z2_OFF_RO1, the caller code_pins one-side sets are checked against the declared set by RA_PINSET)."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in list(set(a) & set(b)):
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
    elif a != b:
        out.append((path, str(a)[:160], str(b)[:160]))
    return out


def stage_dirs(run):
    d = Path(run) / 'stages'
    return {re.sub(r'^\d\d_', '', x.name): x for x in sorted(d.iterdir()) if x.is_dir()} if d.is_dir() else {}


def argv_map(argv):
    return dict(zip(argv[::2], argv[1::2]))


def auto_tokens(ref, new):
    """Declared automatically (stage-script custody): per stage name present in both runs, the script path and sha of its
    request.json (and the route-A --solver/--solver-sha256 argv), and the driver path/sha of start.json."""
    out = []
    sr, sn = stage_dirs(ref), stage_dirs(new)
    for name in sorted(set(sr) & set(sn)):
        qr, qn = sr[name] / 'request.json', sn[name] / 'request.json'
        if not (qr.is_file() and qn.is_file()):
            continue
        a, b = json.loads(qr.read_text()), json.loads(qn.read_text())
        for k in ('script', 'script_sha256'):
            if a[k] != b[k]:
                out.append([a[k], b[k], '<SCRIPT_%s_%s>' % (name.upper(), 'SHA' if k.endswith('sha256') else 'PATH')])
        if name == 'route_a':
            ma, mb = argv_map(a['argv']), argv_map(b['argv'])
            for k in ('--solver', '--solver-sha256'):
                if ma.get(k) and mb.get(k) and ma[k] != mb[k]:
                    out.append([ma[k], mb[k], '<ROUTE_A%s>' % k.upper().replace('-', '_')])
    st_r, st_n = json.loads((ref / 'start.json').read_text()), json.loads((new / 'start.json').read_text())
    for k in ('driver', 'driver_sha256'):
        if st_r.get(k) != st_n.get(k):
            out.append([st_r[k], st_n[k], '<DRIVER_%s>' % k.upper()])
    return out


def caller_norm(c, tail_on, declared_record=None):
    """tail ON: numerical_controls.uv_tail dropped and the ' UV-TAIL' prescription suffix stripped; tail OFF: unchanged, except
    (c2v003, gate Z2_OFF_RO1) numerical_controls.uv_tail is dropped when it EQUALS the declared tail-off record (else it stays and
    is a difference)."""
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
    """Every uv_tail / uv_tail_tap record of a run: JSON key walk of every .json outside checkpoint/ (c2v002), plus (c2v003) a
    byte scan of every .jsonl for the key text (one entry per file, never parsed: progress/node logs can be GB)."""
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
    """(stage dir, request.json, argv map, attempt dirs, attempt start.json) of a run's computed route A, or Nones."""
    d = stage_dirs(run).get('route_a')
    if d is None or not (d / 'request.json').is_file():
        return None
    req = json.loads((d / 'request.json').read_text())
    atts = sorted(x.name for x in d.glob('attempt_*') if x.is_dir())
    st = d / 'attempt_000' / 'start.json'
    return {'dir': d, 'request': req, 'argv': argv_map(req.get('argv') or []), 'attempts': atts,
            'start': json.loads(st.read_text()) if st.is_file() else None}


def ro1_expectations(drv, fn):
    """The RO1 c2v002 worker the driver plans for this route A (serial for column_workers 1, parallel otherwise)."""
    n = int(fn['argv'].get('--column-workers', 1)) if fn else 1
    w = drv.RO1_ROUTE_A['worker' if n == 1 else 'worker_parallel']
    return n, (str(w[0]), w[1])


def check_custody(drv, tok_all, fr, fn, worker):
    """RO1 worker/binding (and the facade the RO1 worker's LOCAL swaps in) on the declared custody list: an entry whose NEW
    side is each path and each sha; the REF side of the binding / facade entries must be the reference attempt's own pin."""
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
    """D1-D3 + argv + sidecar for the gate Z2_OFF_RO1.  Returns (ok, detail, declared_record, expected stray set, E)."""
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


def main(argv=None):
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
        ro1_req = 'ARMED_BLOCK_ONLY'  # c2v002 --require-ro1-armed semantics (armed True, fired False)
    MASK_KEYS.clear(); MASK_KEYS.update(MASK_KEYS_BASE | (TAIL_KEYS if tail_on else set()))
    ref, new = Path(a.reference).resolve(), Path(a.new).resolve()
    tok = json.loads(Path(a.tokens).read_text())['declared']
    auto = auto_tokens(ref, new)
    tok_all = tok + auto
    R = Side(ref, [(r, t) for r, n, t in tok_all])
    N = Side(new, [(n, t) for r, n, t in tok_all])
    cm = load_cm()
    drv = load_driver() if ro1_req == 'ARMED' or declared_off else None
    checks = {}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
    sr, sn = stage_dirs(R.run), stage_dirs(N.run)
    fr, fn = route_a_facts(R.run), route_a_facts(N.run)
    cn_raw, declared_rec, expected_stray, E = None, None, set(), None
    ra_r, ra_n = sr.get('route_a'), sn.get('route_a')
    if ra_n is not None and (ra_n / 'checkpoint/IDENTITY.json').is_file():
        cn_raw = cm.decode(cm._read(str(ra_n / 'checkpoint/IDENTITY.json'), 'identity')['identity']['caller']['record'])
    if declared_off:
        ok, det, declared_rec, expected_stray, E = check_declared_off(drv, N.run, fn, cn_raw)
        put('UV_TAIL_DECLARED', ok, det)
    # ---------------- route A
    if ra_r is not None and ra_n is not None:
        br, bn = ra_r / 'checkpoint/blobs', ra_n / 'checkpoint/blobs'
        fr_b = {p.name: sha_file(p) for p in br.iterdir()} if br.is_dir() else {}
        fn_b = {p.name: sha_file(p) for p in bn.iterdir()} if bn.is_dir() else {}
        put('RA_BLOBS', fr_b == fn_b and fr_b, {'n': [len(fr_b), len(fn_b)], 'differing': sorted(set(fr_b) ^ set(fn_b) | {k for k in fr_b if fn_b.get(k) != fr_b[k]})[:10]})
        bad, n = [], 0
        for p in sorted((ra_r / 'checkpoint').glob('iteration_*/*.json')):
            q = ra_n / 'checkpoint' / p.relative_to(ra_r / 'checkpoint')
            n += 1
            if not q.is_file():
                bad.append(str(p.relative_to(ra_r)) + ' MISSING')
                continue
            x, y = R.norm(json.loads(p.read_text()), RECORD_DROP), N.norm(json.loads(q.read_text()), RECORD_DROP)
            if x != y:
                bad.append((str(p.relative_to(ra_r)), diffs(x, y)[:3]))
        nn = len(list((ra_n / 'checkpoint').glob('iteration_*/*.json')))
        put('RA_RECORDS', not bad and n == nn and n, {'n': [n, nn], 'differing': bad[:8]})
        ar, an = sorted((ra_r / 'attempt_000/arrays').glob('*.npz')), sorted((ra_n / 'attempt_000/arrays').glob('*.npz'))
        badA = [p.name for p, q in zip(ar, an) if p.name != q.name or npz_members(p) != npz_members(q)]
        put('RA_ARRAYS', len(ar) == len(an) and ar and not badA, {'n': [len(ar), len(an)], 'differing': badA[:10]})
        ir = cm._read(str(ra_r / 'checkpoint/IDENTITY.json'), 'identity')['identity']
        cr = caller_norm(cm.decode(ir['caller']['record']), tail_on)
        if cn_raw is None:
            raise SystemExit('NEW route-A checkpoint IDENTITY.json missing: %s' % ra_n)
        cn = caller_norm(cn_raw, tail_on, declared_rec)
        x, y = R.norm(cr), N.norm(cn)
        if declared_off:  # c2v003 RA_PINSET: the one-side caller code_pins are exactly the declared RO1-off additions
            xp, yp = x.get('code_pins') or {}, y.get('code_pins') or {}
            exp = {N.s(str(Path(p).resolve())): N.s(s) for p, s in (drv.AUX_UVT['controller'], drv.UVT_LIB['lib'], drv.UVT_LIB['roster'], drv.UVT_LIB['provider'])}
            exp[N.s(str((N.run / 'inputs' / OFF_REQUEST_NAME).resolve()))] = N.s(E)
            ref_only, new_only = sorted(set(xp) - set(yp)), sorted(set(yp) - set(xp))
            put('RA_PINSET', not ref_only and set(new_only) == set(exp) and all(yp.get(k) == v for k, v in exp.items()),
                {'reference_only': ref_only, 'new_only': new_only, 'expected_new_only': sorted(exp),
                 'value_mismatch': sorted(k for k, v in exp.items() if k in yp and yp[k] != v)})
        notes = []
        align_pins({'caller': x}, {'caller': y}, 'IDENTITY', notes)
        put('RA_IDENTITY', x == y, {'differing': diffs(x, y)[:8], 'declared_pin_set_differences': notes})
    else:
        put('RA_PRESENT', ra_r is None and ra_n is None and not declared_off, {'reference': str(ra_r), 'new': str(ra_n)})
    # ---------------- route B stages
    bad, n_arr, n_json, pin_notes = [], 0, 0, []
    for name, dr in sr.items():
        if name == 'route_a':
            continue
        dn = sn.get(name)
        if dn is None:
            bad.append((name, 'MISSING_IN_NEW'))
            continue
        for p in sorted(dr.rglob('*')):
            if not p.is_file() or p.name in ('stdout.txt', 'stderr.txt', 'request.json'):
                continue
            q = dn / p.relative_to(dr)
            if not q.is_file():
                bad.append((name, str(p.relative_to(dr)), 'MISSING'))
                continue
            if p.suffix == '.npz':
                n_arr += 1
                if npz_members(p) != npz_members(q):
                    bad.append((name, str(p.relative_to(dr)), 'NPZ_CONTENT'))
            elif p.suffix in ('.json', '.jsonl'):
                n_json += 1
                if p.suffix == '.jsonl':
                    x = [R.norm(json.loads(l)) for l in p.read_text().splitlines() if l.strip()]
                    y = [N.norm(json.loads(l)) for l in q.read_text().splitlines() if l.strip()]
                else:
                    x, y = R.norm(json.loads(p.read_text())), N.norm(json.loads(q.read_text()))
                align_pins(x, y, '%s/%s' % (name, p.relative_to(dr)), pin_notes)
                if x != y:
                    bad.append((name, str(p.relative_to(dr)), diffs(x, y)[:3]))
    extra = sorted(set(sn) - set(sr))
    put('STAGES', not bad and set(extra) <= ({'route_a_tail_manifest'} if tail_on else set()), {'arrays_compared': n_arr, 'json_compared': n_json,
                                                                         'differing': bad[:12], 'extra_stages_new': extra,
                                                                         'declared_pin_set_differences': pin_notes[:40], 'n_pin_notes': len(pin_notes)})
    # ---------------- result
    rr, rn = json.loads((R.run / 'result.json').read_text()), json.loads((N.run / 'result.json').read_text())
    keys = ('status', 'valid', 'final_pass', 'speeds_km_s', 'rows')
    pr = [(p.get('pass'), p.get('rows'), p.get('max_abs_change_km_s')) for p in rr.get('passes') or []]
    pn = [(p.get('pass'), p.get('rows'), p.get('max_abs_change_km_s')) for p in rn.get('passes') or []]
    put('RESULT', all(rr.get(k) == rn.get(k) for k in keys) and pr == pn and rr.get('status') == 'COMPLETED',
        {'differing': [k for k in keys if rr.get(k) != rn.get(k)], 'passes_equal': pr == pn, 'status': [rr.get('status'), rn.get('status')]})
    if not tail_on:  # tail-OFF gates: every uv_tail record is listed; only the declared Z2_OFF_RO1 records are admitted
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
    rep = {'schema': 'RUN_IDENTITY_COMPARE_C2V003', 'gate': a.gate, 'tail_on': tail_on, 'ro1_requirement': ro1_req,
           'declared_tail_off_records': declared_off, 'expected_tail_off_request_sha256': E,
           'require_ro1_armed_flag': bool(a.require_ro1_armed),
           'masked_keys': sorted(MASK_KEYS), 'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
           'driver_pin': list(DRIVER) if drv is not None else None, 'auto_tokens': auto,
           'reference': str(R.run), 'new': str(N.run), 'tokens': {'path': str(Path(a.tokens).resolve()), 'sha256': sha_file(a.tokens)},
           'tokens_fired': {'reference': R.fired, 'new': N.fired}, 'checks': checks,
           'verdict': 'PASS_BITWISE_EQUAL' if all(c['pass'] for c in checks.values()) else 'FAIL',
           'failing': [k for k, c in checks.items() if not c['pass']]}
    with open(a.out, 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({'verdict': rep['verdict'], 'failing': rep['failing']}))
    return 0 if rep['verdict'] == 'PASS_BITWISE_EQUAL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
