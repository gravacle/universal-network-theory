"""NGC route-A iterate reader c2v003 (V006 A162 item 1; A153 S9). Root build (Claude2 workflow); nothing here is adopted
until root rules and Claude3 reviews c2v003.

A162 item 1, verbatim: "An approved reader of the route-A sidecar, from the driver code, enumerates the pre-acceptance
iterates. The A134 class is ROUTE_A_PRE_ACCEPTANCE_ITERATE."

The sidecar format, read from the driver code (cx3r008 577f8c94) and the code it pins:
  - driver L8628: a computed tail-ON route A runs with '--uv-tail-sidecar-directory <route_a stage dir>/uv_tail_sidecar';
    driver L8693 copies the route-A result's uv_tail keys (outcome, accepted_iteration, ..., boundary_state_digest_at_return,
    sidecar) into result.uv_tail.route_a_record; L8706 records result.uv_tail.manifest.state_digest.
  - the route-A controller the NGC workers and manifest writer pin (route_a_uv_tail_controller_c2v001_r5.py c5bdd055,
    L29-31, L329-363, L470-525, L527-565) writes, append-only and by exclusive create:
      SIDECAR_IDENTITY.json   {identity, identity_sha256 = sha256(canonical(identity))}, identity.schema
                              UNT_UV_TAIL_ROUTE_A_SIDECAR_C2V001 (static identity + relaxation + checkpoint identity);
      iteration_NNNN.json     {payload, diagnostics}; payload {schema, iteration, state_digest (the state begun at
                              iteration n), next_state_digest (built at completion n; the M_T monitor consumes it),
                              i1t, next_i1t, relaxation, elements {file, count, positions_digest, J_digest}, summary};
      elements_NNNN.npz       the updated_n element roster (positions_m, integrated_J), controller _array_digest form;
      finish_NNN.json         {record: the controller result_record without 'sidecar', files: {name: sha256}};
    and the route-A result's uv_tail.sidecar = {directory, finish {path, sha256}, files}.
  - the NGC manifest writer (ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005 b9247b1a L98-148) reads the same files to
    rebuild the accepted state.

Consumed route-A states (the M_T monitor reads both states at every completion, controller L486):
  for each completed iteration n = 0..a (a = the accepted iteration):
    (n, current_begin_inferred_from_completion, payload[n].state_digest)
    (n, next_built_and_monitor_consumed,        payload[n].next_state_digest)
The last current state (iteration a) is the accepted state (boundary at return = manifest digest); every other digest is
a pre-acceptance iterate (enumerator c2v001 classes them ROUTE_A_PRE_ACCEPTANCE_ITERATE). The roles are the enumerator
c2v001's ITERATE_ROLES (L44).

Source digests. The sidecar does not record an iterate's roster digest. The list therefore carries a source digest only
when it is established: the accepted state's from its ROUTE_A_TAIL_MANIFEST record (TailState digest re-checked from the
manifest's own bytes), every other state's from its S5 admission (ngc_s5_rebuild_export_c2v003, by exact sha; the rebuilt
TailState digest equals the recorded digest, and the digest covers the record's roster_digest). An iterate without an
admission refuses (ROUTE_A_ITERATE_SOURCE_UNESTABLISHED): no list is written and the inventory stays incomplete.

Entries:
  enumerate_sidecar(call_dir)            the occurrences, from the call's own bytes (refuses any custody gap)
  s5_targets(enumeration)                the S5 targets (every non-accepted iterate digest)
  write_iterate_list(call_dir, admissions, out_dir)    the UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001 list (producer: this file)
  verify_iterate_list(ref, call_dir)     the handoff's check: the list's occurrences are exactly the sidecar's
"""
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
S5_TOOL = (os.path.join(HERE, 'ngc_s5_rebuild_export_c2v003.py'),
           '3611e9933b57363ffab8dbdbaae67960751e59d3d34b219f1777e8e2f2a54100')
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
CONTROLLER = {'path': ART + '/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/'
                            'route_a_uv_tail_controller_c2v001_r5.py',
              'sha256': 'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc'}   # cited (format source), not loaded
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
GALAXY = 'NGC3198'
ITERATES_SCHEMA = 'UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001'       # enumerator c2v001 L30
ENUMERATION_SCHEMA = 'UNT_NGC_ROUTE_A_SIDECAR_ENUMERATION_C2V003'
SIDECAR_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_SIDECAR_C2V001'           # controller L44
ROUTE_A_RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_RECORD_C2V001'     # controller L45
CONVERGED = 'CONVERGED_FINITE_FIXED_POINT'
CURRENT = 'current_begin_inferred_from_completion'
NEXT = 'next_built_and_monitor_consumed'
COPIED_KEYS = ('outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags',
               'production_admissible', 'boundary_state_digest_at_return', 'config_sha256', 'request_sha256',
               'admissibility', 'E_A_rows_km_s_accepted')        # driver L8693 (without 'sidecar')
SIDECAR_DIR_NAME = 'uv_tail_sidecar'                            # driver L8628
FILE_RE = re.compile(r'(SIDECAR_IDENTITY\.json|iteration_([0-9]{4})\.json|elements_([0-9]{4})\.npz)\Z')
FINISH_RE = re.compile(r'finish_([0-9]{3})\.json\Z')
C_READ = 'ROUTE_A_SIDECAR_CUSTODY'
C_SOURCE = 'ROUTE_A_ITERATE_SOURCE_UNESTABLISHED'
C_LIST = 'ITERATE_LIST_NOT_THE_SIDECAR_ENUMERATION'
BASIS_MANIFEST = 'ACCEPTED_ROUTE_A_TAIL_MANIFEST'
BASIS_S5 = 'S5_ADMISSION'


class Refusal(ValueError):
    def __init__(self, code, detail=''):
        ValueError.__init__(self, '%s: %s' % (code, detail) if detail else code)
        self.code = code
        self.detail = detail


def need(ok, code, detail=''):
    if not ok:
        raise Refusal(code, detail)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and is_sha(x['sha256'])


def self_pin():
    p = os.path.realpath(__file__)
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def strict_json(raw, label, code=C_READ):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, code, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(_):
        raise Refusal(code, label + ': NONFINITE_JSON')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except Refusal:
        raise
    except ValueError:
        raise Refusal(code, label + ': JSON_INVALID')


def load_exact(path, sha, name, code):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.realpath(path) == path, code,
         'NONCANONICAL_MODULE_PATH: ' + str(path))
    with open(path, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == sha, code, 'MODULE_PIN_MISMATCH: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


_MODS = {}


def s5_tool():
    if 'S5' not in _MODS:
        _MODS['S5'] = load_exact(S5_TOOL[0], S5_TOOL[1], 'ngc_iterates_c2v003_s5_tool', C_SOURCE)
    return _MODS['S5']


def library():
    if 'U' not in _MODS:
        _MODS['U'] = load_exact(LIBRARY[0], LIBRARY[1], 'ngc_iterates_c2v003_owned_uv_tail_lapse_v002', C_SOURCE)
    return _MODS['U']


def _inside(path, root):
    real = os.path.realpath(path)
    return real == root or real.startswith(root + os.sep)


def _read_own(path, out, label, sha=None):
    need(isinstance(path, str) and os.path.isabs(path), C_READ, label + ': PATH_NOT_ABSOLUTE')
    real = os.path.realpath(path)
    need(_inside(real, out), C_READ, label + ': OUTSIDE_OWN_CALL_OUT')
    need('ngc3198' not in os.path.basename(real).lower(), C_READ, label + ': NGC3198_NAMED_FILE_REFUSED')
    try:
        with open(real, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise Refusal(C_READ, '%s: UNREADABLE %s' % (label, exc))
    if sha is not None:
        need(hashlib.sha256(raw).hexdigest() == sha, C_READ, label + ': SHA_MISMATCH')
    return raw


def _array_digest(a):
    """The controller's _array_digest (L78-81) and the manifest writer's sidecar_elements digest (L129-134)."""
    import numpy as np
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def _call(call_dir, driver_sha256):
    call = os.path.realpath(str(call_dir))
    out = os.path.realpath(os.path.join(call, 'out'))
    rraw = _read_own(os.path.join(out, 'result.json'), out, 'result.json')
    fraw = _read_own(os.path.join(out, 'finish.json'), out, 'finish.json')
    result, fin = strict_json(rraw, 'result.json'), strict_json(fraw, 'finish.json')
    need(isinstance(result, dict) and isinstance(fin, dict), C_READ, 'RESULT_OR_FINISH_NOT_AN_OBJECT')
    rsha = hashlib.sha256(rraw).hexdigest()
    need(fin.get('result_sha256') == rsha, C_READ, 'FINISH_NOT_BOUND_TO_THIS_RESULT (driver L9101)')
    need(result.get('driver_sha256') == driver_sha256, C_READ, 'CALL_DRIVER_NOT_THE_REGISTERED_DRIVER')
    need(result.get('galaxy') == GALAXY, C_READ, 'CALL_GALAXY')
    return call, out, result, {'path': os.path.join(out, 'result.json'), 'sha256': rsha}


def enumerate_sidecar(call_dir, *, driver_sha256=DRIVER_SHA256):
    """Every consumed route-A state of a computed tail-ON route A, from the call's own sidecar bytes."""
    import numpy as np
    call, out, result, result_pin = _call(call_dir, driver_sha256)
    uv = result.get('uv_tail')
    need(isinstance(uv, dict), C_READ, 'UV_TAIL_RECORD_MISSING (tail-ON call required)')
    rar = uv.get('route_a_record')
    need(isinstance(rar, dict), C_READ, 'ROUTE_A_RECORD_MISSING (driver L8693)')
    need(rar.get('outcome') == CONVERGED, C_READ, 'ROUTE_A_OUTCOME_NOT_CONVERGED %r' % rar.get('outcome'))
    a = rar.get('accepted_iteration')
    need(type(a) is int and a >= 0, C_READ, 'ACCEPTED_ITERATION_UNRECORDED')
    boundary = rar.get('boundary_state_digest_at_return')
    need(is_sha(boundary), C_READ, 'BOUNDARY_STATE_DIGEST_UNRECORDED')
    man = uv.get('manifest')
    need(isinstance(man, dict) and man.get('state_digest') == boundary, C_READ,
         'BOUNDARY_IS_NOT_THE_MANIFEST_STATE (driver L8706)')
    mraw = _read_own(man.get('path'), out, 'route-A tail manifest', man.get('sha256'))
    mdoc = strict_json(mraw, 'route-A tail manifest')
    mst = mdoc.get('state') if isinstance(mdoc, dict) else None
    need(isinstance(mst, dict) and mst.get('digest') == boundary and isinstance(mst.get('record'), dict)
         and isinstance(mst['record'].get('stage_kind'), str), C_READ, 'MANIFEST_STATE_IS_NOT_THE_BOUNDARY_STATE')
    # the route-A stage record that names the sidecar directory (driver L8628)
    recs = [r for r in result.get('stage_records') or [] if isinstance(r, dict) and r.get('kind') == 'route_a']
    need(len(recs) == 1 and recs[0].get('executed') is True, C_READ, 'ROUTE_A_STAGE_RECORD_NOT_UNIQUE_OR_NOT_EXECUTED')
    st = recs[0]
    argv = st.get('argv')
    need(isinstance(argv, list) and all(isinstance(x, str) for x in argv) and argv.count('--uv-tail-sidecar-directory') == 1,
         C_READ, 'ROUTE_A_ARGV_SIDECAR_FLAG')
    i = argv.index('--uv-tail-sidecar-directory')
    need(i + 1 < len(argv), C_READ, 'ROUTE_A_ARGV_SIDECAR_VALUE')
    sdir = os.path.realpath(argv[i + 1])
    stage_dir = st.get('stage_dir')
    need(isinstance(stage_dir, str) and _inside(stage_dir, out), C_READ, 'ROUTE_A_STAGE_DIR_NOT_OWN_CALL')
    need(sdir == os.path.join(os.path.realpath(stage_dir), SIDECAR_DIR_NAME) and _inside(sdir, out), C_READ,
         'SIDECAR_IS_NOT_THE_ROUTE_A_STAGE_SIDECAR (driver L8628)')
    sc = rar.get('sidecar')
    need(isinstance(sc, dict) and set(sc) == {'directory', 'finish', 'files'} and isinstance(sc['directory'], str)
         and os.path.realpath(sc['directory']) == sdir and is_pin(sc['finish']) and isinstance(sc['files'], dict),
         C_READ, 'ROUTE_A_RECORD_SIDECAR (controller L562)')
    fpath = os.path.realpath(sc['finish']['path'])
    m = FINISH_RE.match(os.path.basename(fpath))
    need(m is not None and os.path.dirname(fpath) == sdir, C_READ, 'SIDECAR_FINISH_NAME_OR_DIRECTORY')
    fin = strict_json(_read_own(fpath, out, 'sidecar finish', sc['finish']['sha256']), 'sidecar finish')
    need(isinstance(fin, dict) and set(fin) == {'record', 'files'} and fin['files'] == sc['files'], C_READ,
         'SIDECAR_FINISH_FILES_DIFFER_FROM_THE_RECORD')
    rec = fin['record']
    need(isinstance(rec, dict) and rec.get('schema') == ROUTE_A_RECORD_SCHEMA, C_READ, 'SIDECAR_FINISH_RECORD_SCHEMA')
    for k in COPIED_KEYS:
        need(k in rec and k in rar and canonical(rec[k]) == canonical(rar[k]), C_READ,
             'SIDECAR_FINISH_RECORD_DIFFERS_FROM_ROUTE_A_RECORD: ' + k)
    # the listed files: names, bytes, and the iteration range 0..a without gaps
    its, els = set(), set()
    for name, sha in sc['files'].items():
        fm = FILE_RE.match(name) if isinstance(name, str) else None
        need(fm is not None and is_sha(sha), C_READ, 'SIDECAR_FILE_NAME %r' % (name,))
        _read_own(os.path.join(sdir, name), out, 'sidecar ' + name, sha)
        if fm.group(2) is not None:
            its.add(int(fm.group(2)))
        if fm.group(3) is not None:
            els.add(int(fm.group(3)))
    need('SIDECAR_IDENTITY.json' in sc['files'], C_READ, 'SIDECAR_IDENTITY_NOT_LISTED')
    need(its == set(range(a + 1)) and els == set(range(a + 1)), C_READ,
         'SIDECAR_ITERATIONS_ARE_NOT_EXACTLY_0..%d (iterations %s, elements %s)' % (a, sorted(its), sorted(els)))
    ident_doc = strict_json(_read_own(os.path.join(sdir, 'SIDECAR_IDENTITY.json'), out, 'sidecar identity',
                                      sc['files']['SIDECAR_IDENTITY.json']), 'sidecar identity')
    need(isinstance(ident_doc, dict) and set(ident_doc) == {'identity', 'identity_sha256'}, C_READ, 'SIDECAR_IDENTITY_KEYS')
    ident = ident_doc['identity']
    need(isinstance(ident, dict) and ident_doc['identity_sha256'] == hashlib.sha256(canonical(ident)).hexdigest(), C_READ,
         'SIDECAR_IDENTITY_SHA (controller L363)')
    need(ident.get('schema') == SIDECAR_SCHEMA and ident.get('config_sha256') == rar.get('config_sha256')
         and ident.get('request_sha256') == rar.get('request_sha256')
         and ident.get('checkpoint_identity_sha256') == rec.get('checkpoint_identity_sha256'), C_READ,
         'SIDECAR_IDENTITY_IS_NOT_THIS_ROUTE_A (schema, config, request, checkpoint identity)')
    payloads = []
    for n in range(a + 1):
        name = 'iteration_%04d.json' % n
        doc = strict_json(_read_own(os.path.join(sdir, name), out, 'sidecar ' + name, sc['files'][name]), name)
        p = doc.get('payload') if isinstance(doc, dict) else None
        need(isinstance(p, dict) and p.get('schema') == SIDECAR_SCHEMA and p.get('iteration') == n
             and is_sha(p.get('state_digest')) and is_sha(p.get('next_state_digest'))
             and p.get('relaxation') == ident.get('relaxation'), C_READ, 'ITERATION_PAYLOAD %d' % n)
        s = p.get('summary')
        need(isinstance(s, dict) and s.get('iteration') == n and s.get('state_digest') == p['state_digest']
             and s.get('next_state_digest') == p['next_state_digest'] and type(s.get('converged')) is bool, C_READ,
             'ITERATION_SUMMARY %d' % n)
        e = p.get('elements')
        ename = 'elements_%04d.npz' % n
        need(isinstance(e, dict) and e.get('file') == ename and type(e.get('count')) is int, C_READ, 'ITERATION_ELEMENTS %d' % n)
        raw = _read_own(os.path.join(sdir, ename), out, 'sidecar ' + ename, sc['files'][ename])
        try:
            with np.load(io.BytesIO(raw), allow_pickle=False) as z:
                pos, J = z['positions_m'].copy(), z['integrated_J'].copy()
        except (KeyError, ValueError, OSError) as exc:
            raise Refusal(C_READ, 'ELEMENTS_UNREADABLE %d %s' % (n, exc))
        need(_array_digest(pos) == e.get('positions_digest') and _array_digest(J) == e.get('J_digest')
             and len(J) == e['count'], C_READ, 'ELEMENTS_DIGEST %d (controller L499)' % n)
        payloads.append(p)
    its_rec = rec.get('iterations')
    need(isinstance(its_rec, list) and len(its_rec) == a + 1, C_READ, 'RECORD_ITERATIONS_LENGTH')
    for n, (s, p) in enumerate(zip(its_rec, payloads)):
        need(isinstance(s, dict) and s.get('iteration') == n and s.get('state_digest') == p['state_digest']
             and s.get('next_state_digest') == p['next_state_digest'], C_READ, 'RECORD_ITERATION_%d_DIFFERS_FROM_SIDECAR' % n)
    need(rec.get('accepted_iteration') == a and its_rec[-1].get('converged') is True
         and payloads[a]['summary']['converged'] is True, C_READ, 'ACCEPTED_ITERATION_NOT_THE_LAST_CONVERGED_ITERATION')
    need(payloads[a]['state_digest'] == boundary == rec.get('boundary_state_digest_at_return'), C_READ,
         'ACCEPTED_ITERATION_STATE_IS_NOT_THE_BOUNDARY_STATE')
    occ = []
    for n, p in enumerate(payloads):
        occ.append({'iteration': n, 'role': CURRENT, 'state_sha256': p['state_digest']})
        occ.append({'iteration': n, 'role': NEXT, 'state_sha256': p['next_state_digest']})
    states = []
    for o in occ:
        if o['state_sha256'] not in states:
            states.append(o['state_sha256'])
    return {'schema': ENUMERATION_SCHEMA, 'producer': self_pin(), 'call_result': result_pin, 'driver_sha256': driver_sha256,
            'route_a_stage': {'name': st.get('name'), 'stage_dir': os.path.realpath(stage_dir)},
            'sidecar': {'directory': sdir, 'finish': dict(sc['finish']), 'finish_index': int(m.group(1)),
                        'files_count': len(sc['files']), 'identity_sha256': ident_doc['identity_sha256']},
            'manifest': {'path': man.get('path'), 'sha256': man.get('sha256')},
            'accepted_iteration': a, 'accepted_state_sha256': boundary, 'accepted_stage_kind': mst['record']['stage_kind'],
            'occurrences': occ, 'states': states,
            'chain_next_equals_next_current': [payloads[n]['next_state_digest'] == payloads[n + 1]['state_digest']
                                               for n in range(a)],
            'converged_flags': [p['summary']['converged'] for p in payloads],
            'reloaded_iterations': [n for n, s in enumerate(its_rec) if s.get('reloaded') is True],
            'controller': dict(CONTROLLER),
            'rule': 'A162 item 1: every completed iteration n = 0..a contributes its begun state (current) and its '
                    'monitor-consumed next state (next); the last current state is the accepted state'}


def s5_targets(enum):
    """Every non-accepted digest of the enumeration, first occurrence as origin; the roster digest is not recorded."""
    out, seen = [], set()
    for o in enum['occurrences']:
        d = o['state_sha256']
        if d == enum['accepted_state_sha256'] or d in seen:
            continue
        seen.add(d)
        out.append({'state': {'state_sha256': d, 'source_sha256': None, 'stage_kind': enum['accepted_stage_kind']},
                    'origin': {'kind': 'ROUTE_A_ITERATE', 'iteration': o['iteration'], 'role': o['role']}})
    return out


def _accepted_source(enum, out):
    """The accepted state's roster digest from its manifest record, the TailState digest re-checked from bytes."""
    import numpy as np
    U = library()
    man = strict_json(_read_own(enum['manifest']['path'], out, 'route-A tail manifest', enum['manifest']['sha256']),
                      'route-A tail manifest')
    st = man['state']
    araw = _read_own(st['arrays']['path'], out, 'manifest arrays', st['arrays']['sha256'])
    with np.load(io.BytesIO(araw), allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    try:
        U.TailState.from_arrays(arrays, st['record'], expected_digest=enum['accepted_state_sha256'])
    except U.Refusal as exc:
        raise Refusal(C_SOURCE, 'ACCEPTED_MANIFEST_STATE_DOES_NOT_REPRODUCE %s' % exc)
    rd = st['record'].get('roster_digest')
    need(is_sha(rd), C_SOURCE, 'ACCEPTED_ROSTER_DIGEST_UNRECORDED')
    return rd


def write_iterate_list(call_dir, admissions, out_dir, *, driver_sha256=DRIVER_SHA256):
    """The UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001 list (enumerator c2v001 _iterates), re-enumerated here from bytes; every
    source digest established (accepted: manifest; others: an ADMITTED S5 admission with the exported files re-checked)."""
    need(isinstance(out_dir, str) and os.path.isabs(out_dir) and os.path.realpath(out_dir) == out_dir
         and os.path.isdir(out_dir), C_SOURCE, 'OUT_DIR_INVALID')
    enum = enumerate_sidecar(call_dir, driver_sha256=driver_sha256)
    out = os.path.realpath(os.path.join(os.path.realpath(str(call_dir)), 'out'))
    need(isinstance(admissions, dict), C_SOURCE, 'ADMISSIONS_NOT_A_MAP')
    S5 = s5_tool()
    source, basis = {}, {}
    for d in enum['states']:
        if d == enum['accepted_state_sha256']:
            source[d] = _accepted_source(enum, out)
            basis[d] = {'kind': BASIS_MANIFEST, 'manifest': dict(enum['manifest'])}
            continue
        ref = admissions.get(d)
        need(is_pin(ref), C_SOURCE, 'NO_S5_ADMISSION_FOR_ITERATE %s' % d[:16])
        try:
            adm = S5.verify_admission(ref, call_result=enum['call_result'], state_sha256=d, recheck_digest=True)
        except S5.Refusal as exc:
            raise Refusal(C_SOURCE, 'S5_ADMISSION_REFUSED %s: %s' % (d[:16], exc))
        need(adm['rebuilt']['stage_kind'] == enum['accepted_stage_kind'], C_SOURCE, 'ITERATE_STAGE_KIND_IS_NOT_ROUTE_A')
        source[d] = adm['rebuilt']['roster_digest']
        basis[d] = {'kind': BASIS_S5, 'admission': dict(ref)}
    occ = [dict(o, source_sha256=source[o['state_sha256']]) for o in enum['occurrences']]
    doc = {'schema': ITERATES_SCHEMA, 'producer': self_pin(), 'call_result': enum['call_result'], 'utc': utc(),
           'occurrences': [{k: o[k] for k in ('iteration', 'role', 'state_sha256', 'source_sha256')} for o in occ],
           'source_basis': basis, 'enumeration_digest': digest({k: enum[k] for k in ('occurrences', 'accepted_iteration',
                                                                                     'accepted_state_sha256', 'sidecar')}),
           'accepted_state_sha256': enum['accepted_state_sha256'], 'rule': enum['rule']}
    raw = (json.dumps(doc, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    p = os.path.join(out_dir, 'ROUTE_A_ITERATES_%s.json' % enum['call_result']['sha256'][:24])
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}


def verify_iterate_list(ref, call_dir, *, driver_sha256=DRIVER_SHA256):
    """The handoff's check: the list is this reader's, for this call, and its occurrences are exactly the sidecar's (none
    dropped, added, reordered or relabelled); each source digest has its recorded basis."""
    need(is_pin(ref), C_LIST, 'ITERATE_LIST_NOT_PINNED')
    real = os.path.realpath(ref['path'])
    need('ngc3198' not in os.path.basename(real).lower(), C_LIST, 'NGC3198_NAMED_FILE_REFUSED')
    try:
        with open(real, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise Refusal(C_LIST, 'UNREADABLE %s' % exc)
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], C_LIST, 'BYTE_PIN_MISMATCH')
    doc = strict_json(raw, 'iterate list', C_LIST)
    need(isinstance(doc, dict) and doc.get('schema') == ITERATES_SCHEMA and doc.get('producer') == self_pin(), C_LIST,
         'ITERATE_LIST_IS_NOT_THIS_READER_S')
    enum = enumerate_sidecar(call_dir, driver_sha256=driver_sha256)
    need(doc.get('call_result') == enum['call_result'], C_LIST, 'ITERATE_LIST_NOT_THIS_CALL')
    occ = doc.get('occurrences')
    need(isinstance(occ, list) and [{k: o.get(k) for k in ('iteration', 'role', 'state_sha256')} if isinstance(o, dict)
                                    else None for o in occ] == enum['occurrences'], C_LIST,
         'OCCURRENCES_DIFFER_FROM_THE_SIDECAR (dropped, added, reordered or relabelled iterates)')
    basis = doc.get('source_basis')
    need(isinstance(basis, dict) and set(basis) == set(enum['states']), C_LIST, 'SOURCE_BASIS_STATES')
    S5 = s5_tool()
    out = os.path.realpath(os.path.join(os.path.realpath(str(call_dir)), 'out'))
    for o in occ:
        d, src = o['state_sha256'], o.get('source_sha256')
        b = basis[d]
        if d == enum['accepted_state_sha256']:
            need(b == {'kind': BASIS_MANIFEST, 'manifest': enum['manifest']}, C_LIST, 'ACCEPTED_BASIS')
            man = strict_json(_read_own(enum['manifest']['path'], out, 'manifest', enum['manifest']['sha256']), 'manifest')
            need(src == man['state']['record'].get('roster_digest'), C_LIST, 'ACCEPTED_SOURCE_IS_NOT_THE_MANIFEST_ROSTER')
        else:
            need(isinstance(b, dict) and b.get('kind') == BASIS_S5 and is_pin(b.get('admission')), C_LIST, 'ITERATE_BASIS')
            try:
                adm = S5.verify_admission(b['admission'], call_result=enum['call_result'], state_sha256=d)
            except S5.Refusal as exc:
                raise Refusal(C_LIST, 'S5_ADMISSION_REFUSED %s: %s' % (d[:16], exc))
            need(src == adm['rebuilt']['roster_digest'], C_LIST, 'ITERATE_SOURCE_IS_NOT_THE_ADMITTED_ROSTER')
    return {'list': dict(ref), 'enumeration': {k: enum[k] for k in ('accepted_iteration', 'accepted_state_sha256',
                                                                      'occurrences', 'states', 'sidecar')}}
