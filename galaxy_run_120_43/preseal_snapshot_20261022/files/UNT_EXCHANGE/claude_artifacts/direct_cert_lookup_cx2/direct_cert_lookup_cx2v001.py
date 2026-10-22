"""0828 direct non-genesis spec preparation. Read-only replay; exclusive outputs.

No authority is created. Root must independently bind the inputs and final specs.
The full list verifier is replayed before publication. Native direct preflight
remains mandatory. No campaign ledger, cache, wave or launch is touched.
"""
import argparse
import builtins
import contextlib
import copy
import hashlib
import importlib.machinery
import io
import json
import math
import os
from pathlib import Path
import stat
import sys
import types

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = Path(__file__).resolve().parent
C1 = {'path': str(ART/'c1_h1_c2/C1_H1_C2V001.json'),
      'sha256': '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}
GENESIS = {'path': str(ART/'s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json'),
           'sha256': '2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319'}
ASSEMBLER = {'path': str(HERE/'cp1_points_assembler_cx2v002.py'),
             'sha256': '1b701591714c11856d525631f946d19a64f76f28041da21c6e9f1a62863b0e88'}
OLD_ASSEMBLER = {'path': str(ART/'h3_campaign_path_c2/cp1_points_assembler_c2v001.py'),
                 'sha256': '951e7203a676afe3cdf566d54970cf5a7d574fbb4cc4c485cd628aca2c0da3af'}
C3V004 = {'path': str(ART/'s4rc1_c3/build_c3v004/registry_assembler_c3v004.py'),
          'sha256': 'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0'}
C3V005 = {'path': str(ART/'s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py'),
          'sha256': '7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310'}
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
R1 = str(ART/'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py')
R1_SHA = '1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'
SLOTS = ('eps_certificate', 'lo_certificate')
REQUEST_SCHEMA = 'DIRECT_CERT_LOOKUP_REQUEST_CX2V001'
MANIFEST_SCHEMA = 'DIRECT_CERT_LOOKUP_MANIFEST_CX2V001'
DIRECT_LOOKUP_API = 'DIRECT_CERT_LOOKUP_CX2V001'

class Refusal(ValueError):
    pass

def need(condition, code):
    if condition is not True:
        raise Refusal(code)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def json_bytes(obj):
    # Exact parent v005 json_bytes, used by core and ledger Mapper.
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')

def decode(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'DUPLICATE_JSON_KEY')
            out[key] = value
        return out
    def constant(value):
        raise Refusal('NONFINITE_JSON')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def is_sha(value):
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)

def exact_pin(ref):
    need(isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and
         isinstance(ref['path'], str) and is_sha(ref['sha256']), 'EXACT_BYTE_PIN_REQUIRED')
    return ref

def lexical(value):
    need(isinstance(value, str) and os.path.isabs(value) and os.path.normpath(value) == value,
         'ABSOLUTE_NORMALIZED_PATH_REQUIRED')
    p = Path(value)
    bad = ('.codex', 'runs', 'runs_ext', 'unt_internal_runs',
           'kmax_a2f10_c5h_run_v001', 'v007_postseal_records')
    need(not any(x.casefold() in bad or 'ngc3198' in x.casefold() for x in p.parts),
         'PROTECTED_PATH_REFUSED')
    need(not any(x.casefold().startswith('uvt_') for x in p.parts) or value == R1,
         'UVT_PATH_REFUSED')
    return p

def safe_path(value):
    """Check each symlink target lexically before probing it."""
    p = lexical(str(value))
    todo, current, links = list(p.parts[1:]), Path('/'), 0
    while todo:
        part = todo.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            current = current.parent
            continue
        candidate = lexical(str(current/part))
        try:
            mode = os.lstat(candidate).st_mode
        except FileNotFoundError:
            current = candidate
            continue
        if stat.S_ISLNK(mode):
            links += 1
            need(links <= 40, 'SYMLINK_LOOP')
            target = os.readlink(candidate)
            path = Path(target) if os.path.isabs(target) else current/target
            lexical(os.path.normpath(str(path)))
            if path.is_absolute():
                current, more = Path('/'), list(path.parts[1:])
            else:
                more = list(path.parts)
            todo = more + todo
        else:
            current = candidate
    return lexical(str(current))

class Snapshot:
    """One physical read per canonical file/inode. All hashes/parse/replay use it."""
    def __init__(self):
        self.cache = {}
        self.inodes = {}
        self.counts = {}
        self.depth = 0

    def raw(self, path, expected=None):
        p = safe_path(str(path))
        name = str(p)
        if name not in self.cache:
            st = p.stat()
            need(stat.S_ISREG(st.st_mode), 'REGULAR_INPUT_REQUIRED')
            need(st.st_size <= 64*1024*1024, 'INPUT_SIZE_LIMIT')
            inode = (st.st_dev, st.st_ino)
            if inode in self.inodes:
                self.cache[name] = self.inodes[inode]
            else:
                fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
                try:
                    opened = os.fstat(fd)
                    need((opened.st_dev, opened.st_ino) == inode, 'INPUT_IDENTITY_CHANGED')
                    chunks, size = [], 0
                    while True:
                        b = os.read(fd, 1024*1024)
                        if not b:
                            break
                        size += len(b)
                        need(size <= 64*1024*1024, 'INPUT_SIZE_LIMIT')
                        chunks.append(b)
                    raw = b''.join(chunks)
                    end = os.fstat(fd)
                    need((opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) ==
                         (end.st_size, end.st_mtime_ns, end.st_ctime_ns) and len(raw) == end.st_size,
                         'INPUT_CHANGED_DURING_READ')
                finally:
                    os.close(fd)
                self.cache[name] = self.inodes[inode] = raw
                self.counts[name] = 1
        raw = self.cache[name]
        if name == R1:
            need(sha(raw) == R1_SHA, 'R1_SOURCE_CHANGED')
        need(expected is None or sha(raw) == expected, 'INPUT_SHA_MISMATCH: '+name)
        return raw

    def read(self, ref):
        exact_pin(ref)
        return self.raw(ref['path'], ref['sha256'])

    def doc(self, ref):
        return decode(self.read(ref))

    def pin(self, path):
        return {'path': str(path), 'sha256': sha(self.raw(path))}

    def module(self, ref, name):
        raw = self.read(ref)
        obj = types.ModuleType(name)
        obj.__file__ = ref['path']
        sys.modules[name] = obj
        exec(compile(raw, ref['path'], 'exec'), obj.__dict__)
        return obj

    @contextlib.contextmanager
    def reads(self):
        """Legacy readers and source loaders share the exact snapshot buffers.

        This is synchronous, process-local replay, not a concurrent service.
        Writes and all process/network operations are outside this context.
        """
        if self.depth:
            self.depth += 1
            try:
                yield
            finally:
                self.depth -= 1
            return
        oldopen, oldio = builtins.open, io.open
        olddata = importlib.machinery.SourceFileLoader.get_data
        research = ('/Users/bgm/Research/', '/Volumes/External1/')
        def selected(path):
            return isinstance(path, (str, bytes, os.PathLike)) and os.fsdecode(path).startswith(research)
        def opening(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
            if not selected(file):
                return oldopen(file, mode, buffering, encoding, errors, newline, closefd, opener)
            need(mode in ('r', 'rt', 'rb') and opener is None, 'REPLAY_READ_ONLY')
            b = self.raw(os.fsdecode(file))
            if 'b' in mode:
                return io.BytesIO(b)
            return io.TextIOWrapper(io.BytesIO(b), encoding=encoding or 'utf-8', errors=errors, newline=newline)
        def source_data(loader, path):
            if selected(path):
                # Never use stale bytecode; B prevents writing a replacement.
                if str(path).endswith('.pyc'):
                    raise FileNotFoundError(path)
                return self.raw(path)
            return olddata(loader, path)
        self.depth = 1
        builtins.open = io.open = opening
        importlib.machinery.SourceFileLoader.get_data = source_data
        try:
            yield
        finally:
            builtins.open, io.open = oldopen, oldio
            importlib.machinery.SourceFileLoader.get_data = olddata
            self.depth = 0

def point_identity(spec):
    # Exact core dc895f8a identity recipe (the slots do not enter the key).
    n = copy.deepcopy(spec['numerics'])
    for key in SLOTS:
        n['uv_tail'].pop(key, None)
    return {'driver_sha256': DRIVER_SHA, 'physical': spec['physical'],
            'coefficients': spec['coefficients'], 'numerics': n}

def theta_key(theta):
    need(isinstance(theta, dict) and bool(theta), 'THETA_REQUIRED')
    need(all(isinstance(k, str) and type(v) in (int, float) and math.isfinite(v)
             for k, v in theta.items()), 'FINITE_THETA_REQUIRED')
    return digest({'schema': 'DDO154_CALIBRATION_THETA_KEY_C2V001',
                   'theta': {str(k): float(v) for k, v in theta.items()}})

def fill(pending, rec):
    need(rec.get('identity') == point_identity(pending), 'CERTIFICATE_IDENTITY_MISMATCH')
    spec = copy.deepcopy(pending)
    for field in SLOTS:
        exact_pin(rec[field])
        spec['numerics']['uv_tail'][field] = copy.deepcopy(rec[field])
    need(point_identity(spec) == point_identity(pending), 'SLOT_FILL_CHANGED_IDENTITY')
    return json_bytes(spec)

def check_mapper_pending(row, spec, raw):
    """Reject labels, theta/physical mapping or serialization a mapper cannot emit.

    Other immutable base-spec fields remain bound to the pending byte pin.
    Equality with a future campaign is conditional on that same pending pin;
    the later importer must independently require the natural mapper's exact SHA.
    """
    key = theta_key(row['theta'])
    th, ph = row['theta'], spec['physical']
    need(spec.get('galaxy') == 'DDO154' and spec.get('admit') == {}, 'FRESH_DDO154_SPEC_REQUIRED')
    for field, name in (('common_scale_s', 'common_scale_s'), ('ell_F_m', 'ell_F_m'),
                        ('distance_Mpc', 'distance_Mpc'), ('Eref_J', 'Eref_base_J'),
                        ('entropy_K_factor', 'entropy_K_factor')):
        need(ph.get(field) == float(th[name]), 'THETA_PHYSICAL_MISMATCH: '+field)
    need(ph.get('gamma') == float(th['gamma_over_Eref'])*float(th['Eref_base_J']), 'THETA_GAMMA_MISMATCH')
    need(spec.get('label') == 'DDO154 cx2v006 theta %s; point %s' % (key[:16], row['key'][:16]),
         'CORE_MAPPER_LABEL_MISMATCH')
    need(row.get('call_key') in (None, key), 'CALL_KEY_MISMATCH')
    need(raw == json_bytes(spec), 'PENDING_SPEC_NOT_MAPPER_SERIALIZATION')
    return key

def validate(s, request_ref):
    """Validate pinned inputs and deterministically fill every point; no writes."""
    req = s.doc(request_ref)
    need(isinstance(req, dict) and set(req) == {'schema', 'records', 'verification', 'c1',
         'genesis_registry', 'approved_producers'}, 'REQUEST_FIELDS')
    need(req['schema'] == REQUEST_SCHEMA, 'REQUEST_SCHEMA')
    need(req['c1'] == C1 and req['genesis_registry'] == GENESIS, 'FROZEN_C1_AND_GENESIS_REQUIRED')
    c1, gen = s.doc(C1), s.doc(GENESIS)
    approved = s.doc(req['approved_producers'])
    if isinstance(approved, dict):
        approved = approved.get('approved_certificate_producers')
    tr = c1['tail_readiness']
    need(approved == tr['approved_certificate_producers'] and isinstance(approved, list)
         and len(approved) == 6, 'FROZEN_SIX_APPROVED_PRODUCERS_REQUIRED')
    need(tr['certificate_registry'] == GENESIS, 'C1_GENESIS_MISMATCH')
    for p in approved:
        s.read(p)
    records, verification = s.doc(req['records']), s.doc(req['verification'])
    need(records.get('schema') == 'CP1_POINTS_LEDGER_RECORDS_C2V001', 'RECORDS_SCHEMA')
    need(records.get('generator') in (ASSEMBLER, OLD_ASSEMBLER), 'RECORDS_GENERATOR')
    expected_assembler = C3V005 if records['generator'] == ASSEMBLER else C3V004
    need(records.get('c3v004_assembler') == expected_assembler, 'RECORDS_ASSEMBLER_BINDING')
    s.read(records['generator'])
    s.read(expected_assembler)
    need(records.get('genesis_registry') == GENESIS, 'RECORDS_GENESIS_MISMATCH')
    need(records.get('approved_certificate_producers') == approved, 'RECORDS_PRODUCERS_MISMATCH')
    need(is_sha(gen.get('eps_source_pins_digest')) and
         records.get('eps_source_pins_digest') == gen['eps_source_pins_digest'], 'GENESIS_EPS_SOURCE_DRIFT')
    need(verification.get('schema') == 'CP1_POINTS_OFFLINE_VERIFY_C2V001'
         and verification.get('generator') == ASSEMBLER, 'VERIFY_SCHEMA_OR_GENERATOR')
    s.read(ASSEMBLER)
    for key, value in (('records', req['records']), ('c1', C1), ('genesis_registry', GENESIS)):
        need(verification.get(key) == value, 'VERIFY_BINDING: '+key)
    need(verification.get('ok') is True and
         verification.get('c1_policy_gate') == {'ok': True, 'blockers': []} and
         verification.get('keys_already_in_genesis') == [] and
         verification.get('record_keys_not_in_the_list') == [], 'VERIFY_NOT_PASS')
    plist = s.doc(records['points_list'])
    need(plist.get('schema') == 'H3_CAMPAIGN_POINTS_LIST_C2V003', 'POINTS_LIST_SCHEMA')
    rows, entries, verified = plist.get('points'), records.get('records'), verification.get('points')
    need(isinstance(rows, list) and 1 <= len(rows) <= 99 and isinstance(entries, list)
         and isinstance(verified, list), 'POINTS_SHAPE')
    count = len(rows)
    need(len(entries) == len(verified) == count and type(records.get('count')) is int
         and records['count'] == count and type(verification.get('n')) is int
         and type(verification.get('n_ok')) is int and verification['n'] == verification['n_ok'] == count,
         'POINT_COUNTS_MISMATCH')
    wave = records.get('wave')
    need(type(wave) is int and wave >= 1 and wave == plist.get('wave'), 'WAVE_MISMATCH')
    keys, nums, labels, output = set(), set(), set(), []
    for row, entry, check in zip(rows, entries, verified):
        key = row.get('key')
        need(is_sha(key) and key not in keys and key not in gen['points'], 'DUPLICATE_OR_GENESIS_KEY')
        num, label = row.get('row'), row.get('label')
        need(type(num) is int and num > 31 and num not in nums and isinstance(label, str)
             and label and label not in labels, 'POINT_ROW_OR_LABEL')
        keys.add(key); nums.add(num); labels.add(label)
        for field in ('key', 'row', 'label', 'theta', 'pending_spec_sha256'):
            need(entry.get(field) == row.get(field), 'RECORD_LIST_MISMATCH: '+field)
        need(entry.get('wave') == wave, 'RECORD_WAVE_MISMATCH')
        for field in ('key', 'row', 'label'):
            need(check.get(field) == row.get(field), 'VERIFY_POINT_MISMATCH: '+field)
        need(check.get('ok') is True and check.get('wrapper_replica', {}).get('ok') is True
             and check['wrapper_replica'].get('blockers') == []
             and check.get('guard_b1', {}).get('ok') is True
             and check['guard_b1'].get('blockers') == []
             and check['guard_b1'].get('phase') == 'prelaunch', 'VERIFY_POINT_REFUSED')
        raw = s.read(row['spec'])
        need(row['pending_spec_sha256'] == row['spec']['sha256'], 'PENDING_PIN_MISMATCH')
        pending = decode(raw)
        ident = point_identity(pending)
        need(digest(ident) == key, 'POINT_IDENTITY_KEY_MISMATCH')
        call_key = check_mapper_pending(row, pending, raw)
        rec = entry.get('record')
        need(isinstance(rec, dict) and set(rec) == {'identity', 'bundle', *SLOTS}
             and rec['identity'] == ident, 'RECORD_IDENTITY_OR_KEYS')
        bundle = s.doc(rec['bundle'])
        slots = {field: rec[field] for field in SLOTS}
        need(bundle.get('schema') == 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'
             and bundle.get('identity') == ident and bundle.get('driver_certificate_bindings') == slots,
             'BUNDLE_IDENTITY_OR_SLOTS')
        for field in SLOTS:
            s.read(rec[field])
        eps = s.doc(rec['eps_certificate'])
        need(digest({'dependencies': eps.get('dependencies'), 'producer': eps.get('producer')})
             == gen['eps_source_pins_digest'], 'POINT_EPS_SOURCE_DRIFT')
        for gate in ('EPS', 'GQ', 'LO_RHO_SLOT'):
            proof = s.doc(bundle['prelaunch'][gate])
            need(proof.get('schema') == 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
                 and proof.get('gate') == gate and proof.get('status') == 'TESTED'
                 and proof.get('verdict') == 'PASS' and proof.get('point_sha256') == key
                 and proof.get('custody_sha256') == digest(bundle.get('custody'))
                 and proof.get('producer') in approved, 'PROOF_SCOPE_OR_PRODUCER: '+gate)
            if gate in ('EPS', 'LO_RHO_SLOT'):
                field = 'eps_certificate' if gate == 'EPS' else 'lo_certificate'
                need(proof.get('driver_certificate') == rec[field], 'PROOF_SLOT_BINDING: '+gate)
            if gate == 'LO_RHO_SLOT':
                need(not ({'covers_all_consumed_states', 'cover_all_consumed_states'} & set(proof)),
                     'RETIRED_LO_ENVELOPE')
        final = fill(pending, rec)
        output.append({'key': key, 'row': num, 'label': label, 'theta': row['theta'],
                       'call_key': call_key, 'pending_spec': row['spec'],
                       'record': rec, 'raw': final, 'sha256': sha(final)})
    return {'request': request_ref, 'inputs': req, 'points_list': records['points_list'],
            'wave': wave, 'points': output, 'verification': verification}

def replay(s, result):
    """Replay the full verifier, including real custody; timestamps alone may differ."""
    with s.reads():
        N = s.module(ASSEMBLER, '_direct_lookup_list_verifier')
        _, rows = N.P.load_points_list(N.C, result['points_list'])
        rep = N.verify_list(result['inputs']['records'], rows, c1_ref=C1, genesis_ref=GENESIS,
                            custody_loader=N.A.real_custody_fn, guard=N.A.real_guard())
    expected = copy.deepcopy(result['verification'])
    actual = copy.deepcopy(rep)
    expected.pop('utc', None)
    actual.pop('utc', None)
    need(actual == expected and rep.get('ok') is True, 'FULL_VERIFY_REPLAY_MISMATCH')
    result['_replayed_request_sha256'] = result['request']['sha256']
    return rep

def publish(s, result, out_dir):
    need(result.get('_replayed_request_sha256') == result['request']['sha256'], 'FULL_REPLAY_REQUIRED_BEFORE_PUBLICATION')
    out = safe_path(out_dir)
    need(out.is_relative_to(HERE) and out != HERE and not os.path.lexists(out)
         and out.parent.is_dir(), 'EXCLUSIVE_OUTPUT_DIRECTORY_REQUIRED')
    # Prepare every byte before the first write. Failed writes preserve the prefix.
    specs, points = [], []
    for point in result['points']:
        path = out/('SPEC_'+point['key']+'.json')
        ref = {'path': str(path), 'sha256': point['sha256']}
        points.append({k: copy.deepcopy(v) for k, v in point.items() if k not in ('raw', 'sha256')} | {'spec': ref})
        specs.append((path, point['raw']))
    manifest = {'schema': MANIFEST_SCHEMA, 'request': result['request'], 'points': points,
                'points_list': result['points_list'], 'wave': result['wave'],
                'generator': s.pin(__file__), 'verification_replayed': True,
                'scope': 'Static certificate/spec preparation; not launch authorization.',
                'production_natural_wave_equality': 'UNTESTED until the campaign naturally rebuilds this pending/final spec.',
                'single_read_physical_counts': dict(s.counts)}
    payload = json_bytes(manifest)
    os.mkdir(out)
    for path, raw in specs + [(out/'MANIFEST.json', payload)]:
        with path.open('xb') as f:
            f.write(raw)
    return {'manifest': {'path': str(out/'MANIFEST.json'), 'sha256': sha(payload)},
            'specs': [p['spec'] for p in points]}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--request', required=True)
    ap.add_argument('--request-sha256', required=True)
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args(argv)
    s = Snapshot()
    result = validate(s, {'path': args.request, 'sha256': args.request_sha256})
    replay(s, result)
    print(json.dumps(publish(s, result, args.out_dir), indent=2))

if __name__ == '__main__':
    try:
        main()
    except (Refusal, ValueError, KeyError, TypeError, OSError) as exc:
        print('REFUSED: '+str(exc), file=sys.stderr)
        raise SystemExit(3)
