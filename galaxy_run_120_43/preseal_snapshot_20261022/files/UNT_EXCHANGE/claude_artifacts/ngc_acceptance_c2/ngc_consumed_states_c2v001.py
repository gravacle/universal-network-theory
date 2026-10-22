"""NGC consumed-state enumerator c2v001 (V006 A153; text of record NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md 9916cb6f,
section 6 S9). Root build (Claude2 workflow); nothing here is adopted until root rules and a distinct lane reviews.

It replaces the DDO inventory schema and ENUMERATOR_SHA (lo_state_proof_adapter_c3v003 L66, L77, L362-368) for NGC calls of
driver cx3r008 (577f8c94). Custody and enumeration only: it reads digests, roster digests, stage kinds and kept regions, never
a speed, a sigma, a target, a slots file or an observed velocity, and it computes no LO number.

Sources (driver cx3r008 577f8c94, read from bytes for layout only):
  - <call>/out/result.json and <call>/out/finish.json (L9082-9101: finish.result_sha256 = sha256(result.json));
  - result.uv_tail.stage_records[] (L6657-6671: {stage, kind, finish_sha256, state_digest, ...} or finish 'ABSENT'); each
    entry's finish.json is found through result.stage_records[] (the ctx records: name, kind, executed, argv --outdir) and
    its uv_tail {state_digest, roster_digest, stage_kind, kept, empty} is read (a route_a_tail_manifest entry: the top-level
    state_digest);
  - result.uv_tail.route_a_record.boundary_state_digest_at_return and .sidecar (L8693);
  - result.uv_tail.manifest {path, sha256, state_digest} (L8706) and the ROUTE_A_TAIL_MANIFEST.json it pins
    (state.digest, state.record, state.arrays; acceptance_handoff_c2v004 L270-271, L403 layout);
  - the route-A pre-acceptance iterates: an OPEN INTERFACE. The driver keeps them in the route-A sidecar directory, whose
    format this build does not read. Root supplies a pinned iterate list (schema ITERATES_SCHEMA) written by a producer in
    root's approved list. Without it the inventory is incomplete (ROUTE_A_ITERATE_LIST_UNAVAILABLE), so the call reads
    INCOMPLETE downstream.
Q5 class map (A134 Q5; c3v003 state_classes L315-358, same precedence): ACCEPTED_ROUTE_A (digest = boundary digest =
manifest digest), INHERITED_ROUTE_A, ROUTE_B_STAGE (own_source_state), ROUTE_A_PRE_ACCEPTANCE_ITERATE, else UNAVAILABLE.
NGC has no anchor class.
"""
import hashlib
import json
import os

SCHEMA = 'UNT_NGC_CONSUMED_STATE_INVENTORY_C2V001'
ITERATES_SCHEMA = 'UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001'
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'   # cx3r008 (A136 G3, A141)
GALAXY = 'NGC3198'
UVT_TAIL_KINDS = ('reference', 'body', 'offset', 'columns_v001', 'rotation_v001', 'columns_v003', 'columns_v005',
                  'rotation_v005')                                          # driver L351
UVT_BINDING_KIND = {'reference': 'reference', 'body': 'body', 'offset': 'offset', 'columns_v001': 'fs_columns',
                    'rotation_v001': 'fs_rotation', 'columns_v003': 'rfs_columns', 'columns_v005': 'le_columns',
                    'rotation_v005': 'le_rotation'}                         # driver L352-354
MANIFEST_KIND = 'route_a_tail_manifest'
ACCEPTED = 'ACCEPTED_ROUTE_A'
INHERITED = 'INHERITED_ROUTE_A'
ROUTE_B = 'ROUTE_B_STAGE'
ITERATE = 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
CLASS_UNAVAILABLE = 'UNAVAILABLE'
ITERATE_ROLES = ('current_begin_inferred_from_completion', 'next_built_and_monitor_consumed')
ROUTE_B_ROLES = ('own_source_state',)
STATE_KEYS = ('state_sha256', 'source_sha256', 'stage_kind')
MAX_JSON_BYTES = 256 * 2 ** 20


class Refusal(ValueError):
    """Fail-closed refusal with a stable code."""


def need(ok, code):
    if not ok:
        raise Refusal(code)


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


def _strict_json(raw, label):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(_):
        raise Refusal(label + ': NONFINITE_JSON')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except ValueError as exc:
        if isinstance(exc, Refusal):
            raise
        raise Refusal(label + ': JSON_INVALID')


def _own_path(path, out, label):
    """An existing regular file inside <call>/out (resolved), not NGC3198-named; symlinks resolved before the check."""
    need(isinstance(path, str) and os.path.isabs(path), label + ': PATH_NOT_ABSOLUTE')
    real = os.path.realpath(path)
    need(real == out or real.startswith(out + os.sep), label + ': OUTSIDE_OWN_CALL_OUT')
    need('ngc3198' not in os.path.basename(real).lower(), label + ': NGC3198_NAMED_FILE_REFUSED')
    need(os.path.isfile(real), label + ': FILE_MISSING')
    return real


def _read_own(pin, out, label):
    need(is_pin(pin), label + ': NOT_AN_EXACT_PIN')
    real = _own_path(pin['path'], out, label)
    need(os.path.getsize(real) <= MAX_JSON_BYTES or not real.endswith('.json'), label + ': JSON_TOO_LARGE')
    with open(real, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == pin['sha256'], label + ': SHA_MISMATCH')
    return raw


def _read_pinned_anywhere(pin, label):
    need(is_pin(pin) and os.path.isabs(pin['path']), label + ': NOT_AN_EXACT_PIN')
    real = os.path.realpath(pin['path'])
    need('ngc3198' not in os.path.basename(real).lower(), label + ': NGC3198_NAMED_FILE_REFUSED')
    with open(real, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == pin['sha256'], label + ': SHA_MISMATCH')
    return raw


def _argv_outdir(argv):
    """driver _argv_map (L3601) for one flag: the value after a single '--outdir'."""
    need(isinstance(argv, list) and all(isinstance(x, str) for x in argv), 'STAGE_ARGV_INVALID')
    need(argv.count('--outdir') == 1, 'STAGE_OUTDIR_NOT_UNIQUE')
    i = argv.index('--outdir')
    need(i + 1 < len(argv) and not argv[i + 1].startswith('--'), 'STAGE_OUTDIR_MISSING')
    return argv[i + 1]


def _kept_claim(k):
    if not isinstance(k, dict):
        return None
    return {str(a): b for a, b in k.items()}


def classify(occurrences, accepted, states):
    """Q5 class per unique state, from occurrences only (c3v003 state_classes precedence).
    Returns [{state, class, roles, stages}] in the order of `states`."""
    roles = {}
    for o in occurrences:
        k = digest(o['state'])
        r = roles.setdefault(k, (set(), set()))
        r[0].add(o['role'])
        r[1].add(o['stage'])
    out = []
    for s in states:
        r, stages = roles.get(digest(s), (set(), set()))
        if not r:
            cls = CLASS_UNAVAILABLE
        elif s['state_sha256'] == accepted:
            cls = ACCEPTED
        elif 'inherited_route_a' in r:
            cls = INHERITED
        elif r & set(ROUTE_B_ROLES):
            cls = ROUTE_B
        elif r <= set(ITERATE_ROLES):
            cls = ITERATE
        else:
            cls = CLASS_UNAVAILABLE
        out.append({'state': s, 'class': cls, 'roles': sorted(r), 'stages': sorted(str(x) for x in stages)})
    return out


def _iterates(ref, approved, result_pin, accepted, accepted_kind):
    raw = _read_pinned_anywhere(ref, 'route-A iterate list')
    doc = _strict_json(raw, 'route-A iterate list')
    need(isinstance(doc, dict) and doc.get('schema') == ITERATES_SCHEMA, 'ITERATE_LIST_SCHEMA')
    prod = doc.get('producer')
    need(is_pin(prod) and isinstance(approved, (list, tuple, set, frozenset)) and prod['sha256'] in set(approved),
         'ITERATE_LIST_PRODUCER_NOT_APPROVED (open interface: the route-A sidecar reader)')
    _read_pinned_anywhere(prod, 'iterate list producer')
    need(doc.get('call_result') == result_pin, 'ITERATE_LIST_NOT_THIS_CALL')
    occ = doc.get('occurrences')
    need(isinstance(occ, list) and occ, 'ITERATE_LIST_EMPTY')
    out = []
    for o in occ:
        need(isinstance(o, dict) and set(o) == {'iteration', 'role', 'state_sha256', 'source_sha256'}, 'ITERATE_FIELDS')
        need(type(o['iteration']) is int and o['iteration'] >= 0 and o['role'] in ITERATE_ROLES, 'ITERATE_ROLE_OR_INDEX')
        need(is_sha(o['state_sha256']) and is_sha(o['source_sha256']), 'ITERATE_DIGESTS')
        out.append({'role': o['role'], 'stage': 'route_a:iteration_%d' % o['iteration'], 'iteration': o['iteration'],
                    'state': {'state_sha256': o['state_sha256'], 'source_sha256': o['source_sha256'],
                              'stage_kind': accepted_kind}, 'kept_claim': None})
    current = [o for o in out if o['role'] == 'current_begin_inferred_from_completion']
    need(current and max(current, key=lambda x: x['iteration'])['state']['state_sha256'] == accepted,
         'ITERATE_LAST_CURRENT_IS_NOT_THE_ACCEPTED_STATE (b1 enumerator accepted_lineage precedent)')
    return out


def enumerate_call(call_dir, *, route_a_iterates_ref=None, approved_iterate_producer_sha256=(),
                   driver_sha256=DRIVER_SHA256):
    """The complete consumed-state inventory of one NGC call, or complete=False with blockers (never raises on data)."""
    inv = {'schema': SCHEMA, 'status': 'TESTED', 'complete': False, 'blockers': [], 'states': [], 'classes': [],
           'occurrences': [], 'producer': self_pin(), 'driver_sha256': driver_sha256,
           'science_approval': 'custody and enumeration only; no LO, GQ or row value is read or approved here'}
    try:
        call = os.path.realpath(str(call_dir))
        out = os.path.realpath(os.path.join(call, 'out'))
        need(os.path.isdir(out), 'CALL_OUT_MISSING')
        rp = _own_path(os.path.join(out, 'result.json'), out, 'result.json')
        with open(rp, 'rb') as f:
            rraw = f.read()
        result_pin = {'path': rp, 'sha256': hashlib.sha256(rraw).hexdigest()}
        inv['call_result'] = result_pin
        result = _strict_json(rraw, 'result.json')
        fp = _own_path(os.path.join(out, 'finish.json'), out, 'finish.json')
        with open(fp, 'rb') as f:
            fraw = f.read()
        fin = _strict_json(fraw, 'finish.json')
        inv['call_finish'] = {'path': fp, 'sha256': hashlib.sha256(fraw).hexdigest()}
        need(isinstance(result, dict) and isinstance(fin, dict), 'RESULT_OR_FINISH_NOT_AN_OBJECT')
        need(fin.get('result_sha256') == result_pin['sha256'], 'FINISH_NOT_BOUND_TO_THIS_RESULT (driver L9101)')
        need(result.get('driver_sha256') == driver_sha256, 'CALL_DRIVER_NOT_CX3R008')
        need(result.get('galaxy') == GALAXY, 'CALL_GALAXY_NOT_NGC')
        inv['call_status'] = {'result_status': result.get('status'), 'finish_status': fin.get('status'),
                              'valid': result.get('valid')}
        uv = result.get('uv_tail')
        need(isinstance(uv, dict), 'UV_TAIL_RECORD_MISSING (tail-ON call required)')
        rar = uv.get('route_a_record')
        need(isinstance(rar, dict) and is_sha(rar.get('boundary_state_digest_at_return')),
             'ROUTE_A_BOUNDARY_DIGEST_UNRECORDED (driver L8693)')
        boundary = rar['boundary_state_digest_at_return']
        inv['route_a_sidecar_recorded'] = rar.get('sidecar')
        man = uv.get('manifest')
        need(isinstance(man, dict) and is_sha(man.get('state_digest')), 'MANIFEST_DIGEST_UNRECORDED (driver L8706)')
        mpin = {'path': man.get('path'), 'sha256': man.get('sha256')}
        mdoc = _strict_json(_read_own(mpin, out, 'route-A tail manifest'), 'route-A tail manifest')
        st = mdoc.get('state') if isinstance(mdoc, dict) else None
        need(isinstance(st, dict) and is_sha(st.get('digest')) and isinstance(st.get('record'), dict)
             and is_pin(st.get('arrays')), 'MANIFEST_STATE_MALFORMED')
        need(st['digest'] == man['state_digest'] == boundary, 'ACCEPTED_BOUNDARY_MANIFEST_DIGEST_MISMATCH')
        _own_path(st['arrays']['path'], out, 'manifest arrays')
        accepted = boundary
        rec = st['record']
        need(isinstance(rec.get('stage_kind'), str) and rec['stage_kind'] and is_sha(rec.get('roster_digest')),
             'ACCEPTED_RECORD_STAGE_OR_ROSTER_UNRECORDED')
        acc_state = {'state_sha256': accepted, 'source_sha256': rec['roster_digest'], 'stage_kind': rec['stage_kind']}
        inv.update(manifest=mpin, accepted_state_sha256=accepted, accepted_stage_kind=rec['stage_kind'])
        occ = [{'role': 'boundary_at_return', 'stage': 'route_a:boundary_at_return', 'state': acc_state,
                'kept_claim': _kept_claim(rec.get('kept'))}]
        ctx_records = result.get('stage_records')
        need(isinstance(ctx_records, list), 'RESULT_STAGE_RECORDS_MISSING')
        by_name = {}
        for r in ctx_records:
            if isinstance(r, dict) and r.get('executed') and isinstance(r.get('name'), str):
                need(r['name'] not in by_name, 'STAGE_NAME_NOT_UNIQUE: ' + r['name'])
                by_name[r['name']] = r
        srecs = uv.get('stage_records')
        need(isinstance(srecs, list), 'UV_TAIL_STAGE_RECORDS_MISSING (driver L6657-6671)')
        stage_rows = []
        for e in srecs:
            need(isinstance(e, dict) and isinstance(e.get('stage'), str), 'UV_TAIL_STAGE_RECORD_MALFORMED')
            name, kind = e['stage'], e.get('kind')
            need(e.get('finish') != 'ABSENT', 'STAGE_FINISH_ABSENT: ' + name)
            need(kind in UVT_TAIL_KINDS or kind == MANIFEST_KIND, 'STAGE_KIND_NOT_A_TAIL_KIND: %s %r' % (name, kind))
            ctx = by_name.get(name)
            need(ctx is not None and ctx.get('kind') == kind, 'STAGE_CTX_RECORD_MISSING: ' + name)
            fpath = os.path.join(_argv_outdir(ctx.get('argv')), 'finish.json')
            sfin_raw = _read_own({'path': fpath, 'sha256': e.get('finish_sha256')}, out, name + ' finish')
            sfin = _strict_json(sfin_raw, name + ' finish')
            if kind == MANIFEST_KIND:
                need(sfin.get('state_digest') == accepted == e.get('state_digest'),
                     'MANIFEST_STAGE_DIGEST_NOT_THE_ACCEPTED_STATE: ' + name)
                stage_rows.append({'stage': name, 'kind': kind, 'role': 'manifest_of_accepted'})
                continue
            u = sfin.get('uv_tail')
            need(isinstance(u, dict) and is_sha(u.get('state_digest')) and u['state_digest'] == e.get('state_digest'),
                 'STAGE_TAIL_DIGEST_UNRECORDED_OR_DIFFERS: ' + name)
            need(u.get('empty') is False, 'STAGE_TAIL_STATE_EMPTY_OR_UNRECORDED: ' + name)
            if u['state_digest'] == accepted:
                o = {'role': 'inherited_route_a', 'stage': name, 'state': dict(acc_state),
                     'kept_claim': _kept_claim(u.get('kept'))}
                if u.get('roster_digest') is not None:
                    need(u['roster_digest'] == acc_state['source_sha256'], 'INHERITED_ROSTER_DIFFERS: ' + name)
            else:
                need(is_sha(u.get('roster_digest')), 'STAGE_ROSTER_DIGEST_UNRECORDED: ' + name)
                need(u.get('stage_kind') == UVT_BINDING_KIND[kind], 'STAGE_KIND_DIFFERS_FROM_BINDING: ' + name)
                o = {'role': 'own_source_state', 'stage': name,
                     'state': {'state_sha256': u['state_digest'], 'source_sha256': u['roster_digest'],
                               'stage_kind': u['stage_kind']},
                     'kept_claim': _kept_claim(u.get('kept'))}
            occ.append(o)
            stage_rows.append({'stage': name, 'kind': kind, 'role': o['role']})
        inv['stage_rows'] = stage_rows
        if route_a_iterates_ref is None:
            inv['blockers'].append('ROUTE_A_ITERATE_LIST_UNAVAILABLE (open interface: the route-A sidecar reader)')
        else:
            occ += _iterates(route_a_iterates_ref, approved_iterate_producer_sha256, result_pin, accepted,
                             rec['stage_kind'])
        states, seen = [], set()
        for o in occ:
            k = digest(o['state'])
            if k not in seen:
                seen.add(k)
                states.append(o['state'])
        # one TailState digest is one state: a digest seen under two identities is refused
        by_sha = {}
        for s in states:
            need(by_sha.setdefault(s['state_sha256'], s) == s, 'STATE_DIGEST_UNDER_TWO_IDENTITIES')
        inv['occurrences'] = [dict(o, ordinal=i) for i, o in enumerate(occ)]
        inv['states'] = states
        inv['classes'] = classify(occ, accepted, states)
        inv['complete'] = not inv['blockers']
    except (Refusal, OSError, KeyError, TypeError, AttributeError) as exc:
        inv['blockers'].append('%s: %s' % (type(exc).__name__, exc))
        inv['complete'] = False
    return inv
