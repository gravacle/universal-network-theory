"""NGC S5 rebuild-export tool c2v003 (V006 A162 item 2; A153 S5; text of record NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md
9916cb6f section 6 S5). Root build (Claude2 workflow); nothing here is adopted until root rules and Claude3 reviews c2v003.

A162 item 2, verbatim: "Every consumed non-accepted state is rebuilt post-run from its own roster, and admitted only if
its digest equals the recorded `state_digest`. That gives B1 per state. The rebuild time is measured on the first call
(U4)."

What this tool does, per consumed non-accepted state (a route-A pre-acceptance iterate or a route-B stage state):
  1. custody: the call's own out/result.json, bound by out/finish.json result_sha256, driver cx3r008 (577f8c94), galaxy
     NGC3198; the target is not the accepted route-A state (that one comes from the call's ROUTE_A_TAIL_MANIFEST, S5).
  2. its own roster: a ROSTER RECIPE (a module in root's approved list, loaded by exact bytes) returns the roster object
     and the build arguments {config, kept, gamma_eff, c_m_s, eval_radii_m, i1t, stage_kind} from the call's own outputs.
     When the state's roster digest is recorded (a route-B stage finish.json uv_tail.roster_digest; the inventory
     source_sha256), the recipe's roster.digest() must equal it before anything is built (S5_ROSTER_NOT_THE_RECORDED_ROSTER).
  3. rebuild: the pinned library owned_uv_tail_lapse_v002 (2026f2b6; the library the driver pins) build(...) with the pinned
     POSIX libm Jn provider (d6c55b55). The recipe never builds the state itself.
  4. admission: ADMITTED only if the rebuilt TailState digest (library TailState._digest: canonical record plus every array's
     dtype, shape and bytes) equals the recorded state digest (S5_REBUILD_DIGEST_MISMATCH otherwise). Digest equality makes
     the rebuilt record and arrays the recorded state bit for bit, so a recipe cannot make a different state pass; recipe
     approval is provenance, the digest is the proof.
  5. export: arrays (npz) and record (JSON) written by exclusive create and re-loaded with TailState.from_arrays
     (expected_digest) before the admission is written; then, once the state's inventory identity is known, the state input
     the adapter reads (schema UNT_NGC_LO_STATE_INPUT_C2V001, source POST_RUN_REBUILD, producer = this file's pin) carrying
     the admission pin.
  6. timing (U4): recipe, build, export and total wall seconds per state are recorded in the admission.
Every refusal still writes an admission record with admitted false and its code, so nothing is silently dropped.

OPEN INTERFACE (disclosed; UNTESTED): no roster recipe for a real NGC call exists in this build. The route-A recipe must
follow the reviewed manifest-writer path (ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005 b9247b1a: from_prepared, the
sidecar element rosters 0..n-1, the iteration-n gas for I1-T) at iteration n; a route-B recipe must reconstruct the stage's
roster as the route-B binding (aee7af12) builds it. Until root approves a recipe, every non-accepted state of a real call
reads UNAVAILABLE in the adapter (NGC_STATE_INPUT_UNAVAILABLE) and the call reads INCOMPLETE: UNTESTED, not a null.
"""
import datetime
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import sys
import time

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')          # the library cx3r008 pins (L311)
PROVIDER = (ART + '/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py',
            'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')         # library PROVIDER_SHA256 (L44)
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'       # cx3r008 (A136 G3, A141)
GALAXY = 'NGC3198'
ADMISSION_SCHEMA = 'UNT_NGC_S5_REBUILD_ADMISSION_C2V003'
STATE_INPUT_SCHEMA = 'UNT_NGC_LO_STATE_INPUT_C2V001'           # the adapter c2v002 interface (unchanged)
SOURCE = 'POST_RUN_REBUILD'                                    # adapter c2v002 L1018
ORIGIN_KINDS = ('ROUTE_A_ITERATE', 'ROUTE_B_STAGE')
ITERATE_ROLES = ('current_begin_inferred_from_completion', 'next_built_and_monitor_consumed')   # enumerator c2v001 L44
BUILD_KEYS = ('config', 'kept', 'gamma_eff', 'c_m_s', 'eval_radii_m', 'i1t', 'stage_kind')     # library build() keywords
STATE_KEYS = ('state_sha256', 'source_sha256', 'stage_kind')
RULE = ('A162 item 2 (S5): every consumed non-accepted state is rebuilt post-run from its own roster with the pinned library '
        'build, and admitted only if its TailState digest equals the recorded state_digest; the rebuild time is measured '
        '(U4). Digest equality is the admission criterion; recipe approval is provenance.')
SCOPE = ('S5 admission only: the rebuilt TailState equals the recorded state bit for bit; no LO, GQ or row value is '
         'computed or approved here')

C_ADMIT = 'S5_NOT_ADMITTED'
C_TARGET = 'S5_TARGET_INVALID'
C_ACCEPTED = 'S5_TARGET_IS_THE_ACCEPTED_STATE'
C_CALL = 'S5_CALL_CUSTODY'
C_RECIPE = 'S5_RECIPE_NOT_APPROVED'
C_RECIPE_FAIL = 'S5_RECIPE_FAILED'
C_ROSTER = 'S5_ROSTER_NOT_THE_RECORDED_ROSTER'
C_BUILD = 'S5_REBUILD_REFUSED'
C_DIGEST = 'S5_REBUILD_DIGEST_MISMATCH'
C_EXPORT = 'S5_EXPORT_NOT_REPRODUCED'
C_VERIFY = 'S5_EXPORT_NOT_VERIFIED'


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


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def self_pin():
    p = os.path.realpath(__file__)
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def strict_json(raw, label, code):
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


def read_pin(ref, code, label):
    need(is_pin(ref) and os.path.isabs(ref['path']), code, label + ': NOT_AN_EXACT_PIN')
    real = os.path.realpath(ref['path'])
    need('ngc3198' not in os.path.basename(real).lower(), code, label + ': NGC3198_NAMED_FILE_REFUSED')
    try:
        with open(real, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise Refusal(code, '%s: UNREADABLE %s' % (label, exc))
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], code, label + ': BYTE_PIN_MISMATCH')
    return raw


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


_LIBS = {}


def libraries():
    """The pinned library and Jn provider (exact bytes); the provider pin must be the library's own PROVIDER_SHA256."""
    if not _LIBS:
        lib = load_exact(LIBRARY[0], LIBRARY[1], 'ngc_s5_c2v003_owned_uv_tail_lapse_v002', C_BUILD)
        need(lib.PROVIDER_SHA256 == PROVIDER[1], C_BUILD, 'PROVIDER_PIN_DISAGREES_WITH_LIBRARY')
        pv = load_exact(PROVIDER[0], PROVIDER[1], 'ngc_s5_c2v003_jn_provider', C_BUILD)
        _LIBS.update(lib=lib, provider=pv)
    return _LIBS['lib'], _LIBS['provider']


def own_call(call_dir, driver_sha256=DRIVER_SHA256):
    """The call's own result and finish (finish bound to the result bytes), driver and galaxy."""
    call = os.path.realpath(str(call_dir))
    out = os.path.realpath(os.path.join(call, 'out'))
    rp, fp = os.path.join(out, 'result.json'), os.path.join(out, 'finish.json')
    try:
        with open(rp, 'rb') as f:
            rraw = f.read()
        with open(fp, 'rb') as f:
            fraw = f.read()
    except OSError as exc:
        raise Refusal(C_CALL, 'RESULT_OR_FINISH_UNREADABLE %s' % exc)
    result = strict_json(rraw, 'result.json', C_CALL)
    fin = strict_json(fraw, 'finish.json', C_CALL)
    need(isinstance(result, dict) and isinstance(fin, dict), C_CALL, 'RESULT_OR_FINISH_NOT_AN_OBJECT')
    rsha = hashlib.sha256(rraw).hexdigest()
    need(fin.get('result_sha256') == rsha, C_CALL, 'FINISH_NOT_BOUND_TO_THIS_RESULT (driver L9101)')
    need(result.get('driver_sha256') == driver_sha256, C_CALL, 'CALL_DRIVER_NOT_THE_REGISTERED_DRIVER')
    need(result.get('galaxy') == GALAXY, C_CALL, 'CALL_GALAXY')
    uv = result.get('uv_tail')
    man = uv.get('manifest') if isinstance(uv, dict) else None
    need(isinstance(man, dict) and is_sha(man.get('state_digest')), C_CALL, 'ACCEPTED_STATE_DIGEST_UNRECORDED (driver L8706)')
    return {'call': call, 'out': out, 'result': result, 'result_pin': {'path': rp, 'sha256': rsha},
            'accepted_state_sha256': man['state_digest']}


def check_target(target, accepted):
    """target = {'state': {state_sha256, source_sha256 (sha or None: not recorded), stage_kind}, 'origin': {...}}."""
    need(isinstance(target, dict) and set(target) == {'state', 'origin'}, C_TARGET, 'TARGET_KEYS')
    st, og = target['state'], target['origin']
    need(isinstance(st, dict) and set(st) == set(STATE_KEYS) and is_sha(st['state_sha256'])
         and (st['source_sha256'] is None or is_sha(st['source_sha256']))
         and isinstance(st['stage_kind'], str) and st['stage_kind'], C_TARGET, 'TARGET_STATE')
    need(isinstance(og, dict) and og.get('kind') in ORIGIN_KINDS, C_TARGET, 'TARGET_ORIGIN_KIND')
    if og['kind'] == 'ROUTE_A_ITERATE':
        need(set(og) == {'kind', 'iteration', 'role'} and type(og['iteration']) is int and og['iteration'] >= 0
             and og['role'] in ITERATE_ROLES, C_TARGET, 'TARGET_ITERATE_ORIGIN')
    else:
        need(set(og) == {'kind', 'stage'} and isinstance(og['stage'], str) and og['stage'], C_TARGET, 'TARGET_STAGE_ORIGIN')
    need(st['state_sha256'] != accepted, C_ACCEPTED,
         'the accepted route-A state comes from the call ROUTE_A_TAIL_MANIFEST (S5), never from a rebuild')
    return {'state': dict(st), 'origin': dict(og)}


def _out_dir(out_dir):
    need(isinstance(out_dir, str) and os.path.isabs(out_dir) and os.path.realpath(out_dir) == out_dir
         and os.path.isdir(out_dir), C_ADMIT, 'OUT_DIR_INVALID (absolute, canonical, existing)')
    return out_dir


def _write_json(out_dir, name, obj):
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    p = os.path.join(out_dir, name)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}


def _write_npz(out_dir, name, arrays):
    import numpy as np
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    raw = buf.getvalue()
    p = os.path.join(out_dir, name)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}


def _load_arrays(raw):
    import numpy as np
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        return {k: z[k].copy() for k in z.files}


def rebuild_admit(*, call_dir, target, recipe_ref, approved_recipe_sha256, out_dir, driver_sha256=DRIVER_SHA256):
    """S5 for one consumed non-accepted state. Always returns the pin of an admission record (admitted true or false)."""
    out_dir = _out_dir(out_dir)
    t_all = time.monotonic()
    timing = {'recipe': None, 'build': None, 'export': None, 'total': None}
    lib_pin = {'path': LIBRARY[0], 'sha256': LIBRARY[1]}
    prov_pin = {'path': PROVIDER[0], 'sha256': PROVIDER[1]}
    adm = {'schema': ADMISSION_SCHEMA, 'producer': self_pin(), 'utc': utc(), 'rule': RULE, 'scope': SCOPE,
           'driver_sha256': driver_sha256, 'call_result': None, 'target': target, 'recipe': recipe_ref,
           'library': lib_pin, 'provider': prov_pin, 'admitted': False, 'codes': [], 'detail': [],
           'roster': None, 'digest_equal': None, 'rebuilt': None, 'timing_seconds': timing}
    name_key = 'UNKNOWN'
    try:
        if isinstance(target, dict) and isinstance(target.get('state'), dict) and is_sha(target['state'].get('state_sha256')):
            name_key = target['state']['state_sha256'][:24]
        c = own_call(call_dir, driver_sha256)
        adm['call_result'] = c['result_pin']
        tg = check_target(target, c['accepted_state_sha256'])
        adm['target'] = tg
        need(is_pin(recipe_ref) and isinstance(approved_recipe_sha256, (list, tuple, set, frozenset))
             and recipe_ref['sha256'] in set(approved_recipe_sha256), C_RECIPE,
             'ROSTER_RECIPE_NOT_IN_ROOT_APPROVED_LIST (open interface: no real NGC recipe is approved in this build)')
        lib, pv = libraries()
        recipe = load_exact(os.path.realpath(recipe_ref['path']), recipe_ref['sha256'],
                            'ngc_s5_c2v003_recipe_' + recipe_ref['sha256'][:12], C_RECIPE)
        t0 = time.monotonic()
        try:
            got = recipe.roster_for_state(call_dir=c['call'], out_dir=c['out'], result=c['result'], target=tg, lib=lib,
                                          provider=pv)
        except Exception as exc:          # the recipe is external code: a structured refusal, never a crash
            raise Refusal(C_RECIPE_FAIL, '%s: %s' % (type(exc).__name__, exc))
        finally:
            timing['recipe'] = time.monotonic() - t0
        need(isinstance(got, dict) and set(got) >= {'roster', 'build'} and isinstance(got['build'], dict)
             and set(got['build']) == set(BUILD_KEYS), C_RECIPE_FAIL, 'RECIPE_RETURN_SHAPE (roster, build{%s})' % ','.join(BUILD_KEYS))
        roster, b = got['roster'], got['build']
        try:
            rd = roster.digest()
        except Exception as exc:
            raise Refusal(C_RECIPE_FAIL, 'ROSTER_DIGEST_UNAVAILABLE %s: %s' % (type(exc).__name__, exc))
        need(is_sha(rd), C_RECIPE_FAIL, 'ROSTER_DIGEST_NOT_A_SHA')
        recorded = tg['state']['source_sha256']
        adm['roster'] = {'digest': rd, 'recorded_source_sha256': recorded,
                         'equal': None if recorded is None else rd == recorded}
        need(recorded is None or rd == recorded, C_ROSTER,
             'the recipe roster %s is not the recorded roster %s' % (rd[:16], recorded[:16] if recorded else None))
        import numpy as np
        t0 = time.monotonic()
        try:
            st = lib.build(config=b['config'], kept=b['kept'], roster=roster, gamma_eff=float(b['gamma_eff']),
                           c_m_s=float(b['c_m_s']), eval_radii_m=np.asarray(b['eval_radii_m'], dtype=float),
                           jn_provider=pv.create_provider(), i1t=b['i1t'], stage_kind=b['stage_kind'])
        except (ValueError, TypeError, KeyError, OverflowError, MemoryError, ZeroDivisionError, RuntimeError) as exc:
            raise Refusal(C_BUILD, '%s: %s' % (type(exc).__name__, exc))
        finally:
            timing['build'] = time.monotonic() - t0
        adm['digest_equal'] = st.digest == tg['state']['state_sha256']
        need(adm['digest_equal'], C_DIGEST, 'rebuilt %s != recorded %s' % (st.digest[:16], tg['state']['state_sha256'][:16]))
        need(st.record.get('roster_digest') == rd, C_DIGEST, 'REBUILT_RECORD_ROSTER_DIGEST_IS_NOT_THE_RECIPE_ROSTER')
        need(st.record.get('stage_kind') == tg['state']['stage_kind'], C_DIGEST, 'REBUILT_STAGE_KIND_DIFFERS')
        t0 = time.monotonic()
        try:
            rec_pin = _write_json(out_dir, 'S5_TAILSTATE_RECORD_%s.json' % name_key, json.loads(json.dumps(st.record)))
            arr_pin = _write_npz(out_dir, 'S5_TAILSTATE_ARRAYS_%s.npz' % name_key, st.to_arrays())
            back = lib.TailState.from_arrays(_load_arrays(read_pin(arr_pin, C_EXPORT, 'exported arrays')),
                                             strict_json(read_pin(rec_pin, C_EXPORT, 'exported record'), 'record', C_EXPORT),
                                             expected_digest=tg['state']['state_sha256'])
        except lib.Refusal as exc:
            raise Refusal(C_EXPORT, str(exc))
        except OSError as exc:
            raise Refusal(C_EXPORT, 'EXPORT_WRITE %s' % exc)
        finally:
            timing['export'] = time.monotonic() - t0
        adm['rebuilt'] = {'state_digest': back.digest, 'roster_digest': back.record.get('roster_digest'),
                          'stage_kind': back.record.get('stage_kind'), 'empty': bool(back.empty), 'record': rec_pin,
                          'arrays': arr_pin}
        adm['recipe_provenance'] = got.get('provenance')
        adm['admitted'] = True
    except Refusal as exc:
        adm['codes'] = [exc.code]
        adm['detail'].append(str(exc))
    except (OSError, KeyError, TypeError, AttributeError, IndexError) as exc:
        adm['codes'] = [C_ADMIT]
        adm['detail'].append('%s: %s' % (type(exc).__name__, exc))
    timing['total'] = time.monotonic() - t_all
    adm['u4_note'] = 'U4: rebuild wall time per state, measured here; the first real call decides the cost'
    return _write_json(out_dir, 'S5_ADMISSION_%s.json' % name_key, adm)


def verify_admission(ref, *, call_result=None, state_sha256=None, recheck_digest=False):
    """An ADMITTED admission of this tool (by its pin), for this call and state; recheck_digest re-loads the exported
    arrays and record and requires TailState.from_arrays(expected_digest) to hold."""
    a = strict_json(read_pin(ref, C_VERIFY, 'S5 admission'), 'S5 admission', C_VERIFY)
    need(isinstance(a, dict) and a.get('schema') == ADMISSION_SCHEMA, C_VERIFY, 'ADMISSION_SCHEMA')
    need(a.get('producer') == self_pin(), C_VERIFY, 'ADMISSION_PRODUCER_IS_NOT_THIS_S5_TOOL')
    need(a.get('admitted') is True and a.get('codes') == [] and a.get('digest_equal') is True, C_VERIFY,
         'ADMISSION_NOT_ADMITTED: %s' % (a.get('codes'),))
    rb = a.get('rebuilt')
    need(isinstance(rb, dict) and is_pin(rb.get('record')) and is_pin(rb.get('arrays')) and is_sha(rb.get('state_digest'))
         and is_sha(rb.get('roster_digest')), C_VERIFY, 'ADMISSION_REBUILT_FIELDS')
    tg = a.get('target') or {}
    need(isinstance(tg, dict) and isinstance(tg.get('state'), dict)
         and tg['state'].get('state_sha256') == rb['state_digest'], C_VERIFY, 'ADMISSION_TARGET_DIGEST')
    if call_result is not None:
        need(a.get('call_result') == call_result, C_VERIFY, 'ADMISSION_NOT_THIS_CALL')
    if state_sha256 is not None:
        need(rb['state_digest'] == state_sha256, C_VERIFY, 'ADMISSION_NOT_THIS_STATE')
    if recheck_digest:
        lib, _ = libraries()
        try:
            lib.TailState.from_arrays(_load_arrays(read_pin(rb['arrays'], C_VERIFY, 'admitted arrays')),
                                      strict_json(read_pin(rb['record'], C_VERIFY, 'admitted record'), 'record', C_VERIFY),
                                      expected_digest=rb['state_digest'])
        except lib.Refusal as exc:
            raise Refusal(C_VERIFY, 'ADMITTED_FILES_DO_NOT_REPRODUCE_THE_DIGEST %s' % exc)
    return a


def export_state_input(*, admission_ref, state, out_dir):
    """The adapter's state input for an admitted state, once its inventory identity {state_sha256, source_sha256,
    stage_kind} is known: the identity must be the rebuilt state's (digest, roster digest, stage kind)."""
    out_dir = _out_dir(out_dir)
    a = verify_admission(admission_ref)
    rb = a['rebuilt']
    need(isinstance(state, dict) and set(state) == set(STATE_KEYS), C_VERIFY, 'INVENTORY_STATE_KEYS')
    need(state['state_sha256'] == rb['state_digest'] and state['source_sha256'] == rb['roster_digest']
         and state['stage_kind'] == rb['stage_kind'], C_VERIFY,
         'INVENTORY_STATE_IS_NOT_THE_ADMITTED_STATE (digest, roster digest, stage kind)')
    return _write_json(out_dir, 'S5_STATE_INPUT_%s.json' % state['state_sha256'][:24], {
        'schema': STATE_INPUT_SCHEMA, 'state': dict(state), 'call_result': a['call_result'], 'source': SOURCE,
        'producer': self_pin(), 'tail_state': {'record': dict(rb['record']), 'arrays': dict(rb['arrays'])},
        'admission': dict(admission_ref)})


def verify_export(ref, *, call_result, state):
    """A state input of this tool for this call and state, carrying an ADMITTED admission whose exported files are the
    input's tail-state pins. The adapter then re-checks the TailState digest from those bytes (S5)."""
    obj = strict_json(read_pin(ref, C_VERIFY, 'state input'), 'state input', C_VERIFY)
    need(isinstance(obj, dict) and obj.get('schema') == STATE_INPUT_SCHEMA and obj.get('source') == SOURCE, C_VERIFY,
         'STATE_INPUT_SCHEMA_OR_SOURCE')
    need(obj.get('producer') == self_pin(), C_VERIFY, 'STATE_INPUT_PRODUCER_IS_NOT_THIS_S5_TOOL')
    need(obj.get('state') == state and obj.get('call_result') == call_result, C_VERIFY, 'STATE_INPUT_NOT_THIS_CALL_AND_STATE')
    a = verify_admission(obj.get('admission'), call_result=call_result, state_sha256=state['state_sha256'])
    rb = a['rebuilt']
    need(obj.get('tail_state') == {'record': rb['record'], 'arrays': rb['arrays']}, C_VERIFY,
         'STATE_INPUT_FILES_ARE_NOT_THE_ADMITTED_FILES')
    need(state['source_sha256'] == rb['roster_digest'] and state['stage_kind'] == rb['stage_kind'], C_VERIFY,
         'STATE_INPUT_IDENTITY_IS_NOT_THE_ADMITTED_STATE')
    return {'admission': dict(obj['admission']), 'timing_seconds': a.get('timing_seconds')}


def targets_from_inventory(inventory):
    """S5 targets: every inventory state except the accepted one, with its origin (a route-B stage occurrence or a
    route-A iterate occurrence); the recorded roster digest is the inventory source_sha256."""
    need(isinstance(inventory, dict) and inventory.get('complete') is True, C_TARGET, 'COMPLETE_INVENTORY_REQUIRED')
    acc = inventory.get('accepted_state_sha256')
    out = []
    for s in inventory.get('states') or []:
        if s['state_sha256'] == acc:
            continue
        occ = [o for o in inventory.get('occurrences') or [] if o.get('state') == s]
        rb = [o for o in occ if o.get('role') == 'own_source_state']
        it = sorted((o for o in occ if o.get('role') in ITERATE_ROLES), key=lambda o: (o.get('iteration', 0), o['role']))
        if rb:
            origin = {'kind': 'ROUTE_B_STAGE', 'stage': rb[0]['stage']}
        else:
            need(bool(it), C_TARGET, 'STATE_WITHOUT_A_REBUILDABLE_ORIGIN %s' % s['state_sha256'][:16])
            m = re.fullmatch(r'route_a:iteration_([0-9]+)', str(it[0].get('stage')))
            need(m is not None, C_TARGET, 'ITERATE_STAGE_LABEL')
            origin = {'kind': 'ROUTE_A_ITERATE', 'iteration': int(m.group(1)), 'role': it[0]['role']}
        out.append({'state': dict(s), 'origin': origin})
    return out
