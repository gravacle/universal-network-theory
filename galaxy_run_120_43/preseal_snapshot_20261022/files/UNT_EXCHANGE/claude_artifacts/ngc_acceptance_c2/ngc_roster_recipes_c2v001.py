"""NGC roster recipes c2v001 (V006 A177 "Commissioned: NGC roster recipes (route A, route B)"). Root build (Claude2 workflow);
nothing here is adopted until root rules and Claude3 (after its reset) or Claude4 (after Fri) reviews it.

What a recipe is (S5 tool ngc_s5_rebuild_export_c2v003 3611e993 L273-309): S5 calls
    roster_for_state(*, call_dir, out_dir, result, target, lib, provider)
and receives {'roster', 'build': {config, kept, gamma_eff, c_m_s, eval_radii_m, i1t, stage_kind}, 'provenance'}. The recipe
never builds the state. S5 requires roster.digest() == the recorded roster digest when one is recorded (route B: finish.json
uv_tail.roster_digest), builds the state with the pinned library v002 (2026f2b6) and admits it only on exact TailState digest
equality. Digest equality is the proof; this module is provenance.

Entries
  RECIPE_ROUTE_A                  a route-A iterate state (the manifest writer's rebuild at iteration m)
  RECIPE_ROUTE_B_offset           the offset Delta roster
  RECIPE_ROUTE_B_fs_columns       stars + body gas (offset updated_base_arrays)
  RECIPE_ROUTE_B_fs_rotation      stars + body gas (offset updated_base_arrays)
  RECIPE_ROUTE_B_rfs_columns      stars + the feedback's source-rotation rings
  RECIPE_ROUTE_B_le_columns       stars + the feedback's source-rotation rings
  RECIPE_ROUTE_B_le_rotation      stars + the feedback's source-rotation rings
  roster_for_state                the S5 entry: dispatch on the target origin, with the production toolkit
  recipe_for_state                the same with an explicit toolkit (the synthetic suite passes its own; see TOOLKIT)

Every input is read from the call's own output records (paths resolved inside <call>/out) or from a file pinned by sha in
those records or in the named code. Basis per input (recorded in the returned provenance):
  FORMAL    the named code constructs the input at the cited lines from a record the call writes;
  DECLARED  the route-B binding receives the input from its stage successor (driver V011_B_STAGES), whose bytes are not a
            named path under the A177 commission. The recipe reads it from the cited call record. S5 digest equality decides
            (roster digest before any build, TailState digest after), so a wrong DECLARED reading is refused, never admitted.

Named code (paths + sha256 from bytes):
  driver cx3r008            577f8c94 (identity.seed L8464; manifest stage argv L8697-8700; route-B argv L8710-8736;
                            ctx records L1822-1857; uv_tail stage records L1155-1172 / L6657-6671; result L9081-9084)
  route-A controller        c5bdd055 (from_prepared L219-284; _i1t L366-393; _build L395-406; complete_iteration L470-525)
  NGC manifest writer       b9247b1a (LOCAL prep L43-45; PINS controller L46-49; attempt_tail_record L98-121;
                            sidecar_elements L124-148; rebuild_state L151-159; main L191-249)
  NGC route-B binding       aee7af12 (_grid_K L235-258; _truncation L261-268; _stars L325-346; _manifest L379-405;
                            _manifest_gas_roster L407-427; bind L430-532; bind_offset L534-568; ngc_h2_component L578-593)
  library v002              2026f2b6 (kept_region L138-160; normalize_config L73-130; build L645-796)

THE MONITOR-NEXT STATE (A177 item; reader role next_built_and_monitor_consumed of the accepted iteration a). The controller
builds it at L483-484: g_next = (1-r)*gas_a + r*updated_a; st_next = _build(a+1, _i1t(a+1, g_next)). Recorded: updated_a as
the element roster <sidecar>/elements_{a:04d}.npz (L475-481, L518-519; digests in iteration_{a:04d}.json payload.elements, L499),
the I1-T record payload.next_i1t (L497-498) and the digest payload.next_state_digest (L496). NOT recorded by any named code:
the gas array g_next = gas_{a+1} (the sidecar write list is L363, L518-520, L560-561; g_next lives only in _pending, L522), and
no checkpoint START holds it (iteration folders stop at a, driver L7024-7038). The MW path re-verifies I1-T from the gas array
(MW L217-221, L232), so that state is REFUSED here with ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED (never approximated). The same code
refuses an (n, next) state with n < a whose digest is not iteration n+1's begun state (its g_next is equally unrecorded).
"""
import hashlib
import importlib.util
import io
import json
import math
import os
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'          # cx3r008 (A136 G3, A141)
MANIFEST_WRITER = (ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/'
                         'ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005.py',
                   'b9247b1aef0d9c3c05757bd27d68a9964a22d078ce8189311f11e0e2ad6b4c7c')       # driver V011_PINS L4992
ROUTE_B_BINDING = (ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/'
                         'ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py',
                   'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3')       # driver V011_PINS L4992
LIBRARY_SHA256 = '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'         # S5 LIBRARY; BB PINS['lib'] L42
CHECKPOINT_MODULE_SHA256 = '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'  # driver AUX L253 (manifest argv)
CONTROLLER_SHA256 = 'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc'       # MW PINS L47-48
GALAXY = 'NGC3198'
MANIFEST_KIND = 'route_a_tail_manifest'                                                    # driver L8697
UVT_BINDING_KIND = {'reference': 'reference', 'body': 'body', 'offset': 'offset', 'columns_v001': 'fs_columns',
                    'rotation_v001': 'fs_rotation', 'columns_v003': 'rfs_columns', 'columns_v005': 'le_columns',
                    'rotation_v005': 'le_rotation'}                                       # driver L352-354
INHERITED_KINDS = ('reference', 'body')                                                    # BB L457-470: the manifest state
STAGE_RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_B_STAGE_RECORD_C2V001'                           # BB L36
MANIFEST_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_MANIFEST_C2V001'                                    # MW L40; BB L37
CURRENT = 'current_begin_inferred_from_completion'                                         # reader L69
NEXT = 'next_built_and_monitor_consumed'                                                   # reader L70
BODY_ARRAYS = 'body_arrays.npz'                                                            # driver L3307
BASE_ARRAYS = 'updated_base_arrays.npz'                                                    # driver L3310; BB L21
SOURCE_OFFSET = 'source_offset.npz'                                                        # BB L493
FORMAL = 'FORMAL'
DECLARED = 'DECLARED'

# named refusal codes
C_CALL = 'RECIPE_CALL_NOT_BOUND'
C_TARGET = 'RECIPE_TARGET_INVALID'
C_OWN = 'RECIPE_INPUT_OUTSIDE_CALL'
C_PIN = 'RECIPE_INPUT_PIN'
C_MSTAGE = 'ROUTE_A_MANIFEST_STAGE_RECORD'
C_WRITER = 'ROUTE_A_MANIFEST_WRITER_NOT_RECIPE_BOUND'
C_PATCH = 'ROUTE_A_MODULE_PATCH_UNSUPPORTED'
C_ATTEMPT = 'ROUTE_A_ATTEMPT_RECORD'
C_SIDECAR = 'ROUTE_A_SIDECAR_RECORD'
C_ELEMENT = 'ROUTE_A_SIDECAR_ELEMENT_MISSING'
C_RANGE = 'ROUTE_A_TARGET_ITERATION_OUT_OF_RANGE'
C_ITERATE = 'ROUTE_A_TARGET_NOT_THE_ITERATE_STATE'
C_NEXT_GAS = 'ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED'
C_CKPT = 'ROUTE_A_CHECKPOINT_RECORDS_DISAGREE'
C_GAS = 'ROUTE_A_CHECKPOINT_GAS_UNREADABLE'
C_IDENT = 'ROUTE_A_CONTROLLER_IDENTITY_DIFFERS'
C_I1T = 'ROUTE_A_I1T_REFUSED'
C_I1T_REC = 'ROUTE_A_I1T_NOT_THE_RECORDED_I1T'
C_BSTAGE = 'ROUTE_B_STAGE_RECORD'
C_BKIND = 'ROUTE_B_STAGE_KIND_MISMATCH'
C_INHERIT = 'ROUTE_B_KIND_NOT_REBUILT'
C_BFIN = 'ROUTE_B_FINISH_NOT_THE_RECORDED_FINISH'
C_BSTATE = 'ROUTE_B_TARGET_NOT_THE_STAGE_STATE'
C_BIND = 'ROUTE_B_BINDING_NOT_THE_PINNED_BINDING'
C_CFG = 'ROUTE_B_CONFIG_NOT_THE_RECORDED_CONFIG'
C_KEPT = 'ROUTE_B_KEPT_NOT_THE_RECORDED_KEPT'
C_SEED = 'ROUTE_B_SEED_PIN'
C_PROFILE = 'ROUTE_B_PROFILE_UNRESOLVED'
C_BODY = 'ROUTE_B_BODY_ARRAYS_UNRECORDED'
C_BASE = 'ROUTE_B_BASE_ARRAYS_UNRECORDED'
C_SROT = 'ROUTE_B_SOURCE_ROTATION_UNRECORDED'
C_MANIFEST = 'ROUTE_B_ROUTE_A_MANIFEST'
C_PHYS = 'ROUTE_B_PHYS_UNRECORDED'
C_I1T_B = 'ROUTE_B_I1T_UNRECORDED'


class RecipeRefusal(ValueError):
    def __init__(self, code, detail=''):
        ValueError.__init__(self, '%s: %s' % (code, detail) if detail else code)
        self.code = code
        self.detail = detail


def need(ok, code, detail=''):
    if not ok:
        raise RecipeRefusal(code, detail)


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def _strict_json(raw, label, code):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, code, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(_):
        raise RecipeRefusal(code, label + ': NONFINITE_JSON')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except RecipeRefusal:
        raise
    except ValueError:
        raise RecipeRefusal(code, label + ': JSON_INVALID')


# ------------------------------------------------------------------------------------------------ custody helpers
def _inside(real, root):
    return real == root or real.startswith(root + os.sep)


def _own_path(path, out, label):
    """A path of the call's own outputs: absolute, resolved inside <call>/out, not NGC3198-named."""
    need(isinstance(path, str) and os.path.isabs(path), C_OWN, label + ': PATH_NOT_ABSOLUTE %r' % (path,))
    real = os.path.realpath(path)
    need(_inside(real, out), C_OWN, '%s: %s is outside the call out %s' % (label, real, out))
    need('ngc3198' not in os.path.basename(real).lower(), C_OWN, label + ': NGC3198_NAMED_FILE_REFUSED')
    return real


def _own_bytes(path, out, label, sha=None, code=C_PIN):
    real = _own_path(path, out, label)
    try:
        with open(real, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise RecipeRefusal(code, '%s: UNREADABLE %s' % (label, exc))
    if sha is not None:
        need(_sha_bytes(raw) == sha, code, label + ': SHA_MISMATCH')
    return real, raw


def _pinned_bytes(path, sha, label, code=C_PIN):
    """A file pinned by sha in a call record or in named code (code, a registered source)."""
    need(isinstance(path, str) and os.path.isabs(path) and _is_sha(sha), code, label + ': NOT_AN_EXACT_PIN')
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise RecipeRefusal(code, '%s: UNREADABLE %s' % (label, exc))
    need(_sha_bytes(raw) == sha, code, label + ': SHA_MISMATCH')
    return raw


def _npz(raw, label, code):
    import numpy as np
    try:
        with np.load(io.BytesIO(raw), allow_pickle=False) as z:
            return {k: z[k].copy() for k in z.files}
    except (ValueError, OSError, KeyError) as exc:
        raise RecipeRefusal(code, '%s: NPZ_UNREADABLE %s' % (label, exc))


def load_exact(path, sha, name, code=C_PIN):
    """A module from exact bytes (sha checked before exec); not registered in sys.modules."""
    path = str(path)
    need(os.path.isabs(path) and os.path.realpath(path) == path, code, 'NONCANONICAL_MODULE_PATH: ' + path)
    raw = _pinned_bytes(path, sha, 'module ' + os.path.basename(path), code)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def _argv_value(argv, flag, code, label):
    """The value after a single occurrence of flag (driver _argv_map L3601 for one flag)."""
    need(isinstance(argv, list) and all(isinstance(x, str) for x in argv), code, label + ': ARGV_INVALID')
    need(argv.count(flag) == 1, code, '%s: %s not exactly once' % (label, flag))
    i = argv.index(flag)
    need(i + 1 < len(argv) and not argv[i + 1].startswith('--'), code, '%s: %s has no value' % (label, flag))
    return argv[i + 1]


def _argv_optional(argv, flag, code, label):
    need(isinstance(argv, list) and argv.count(flag) <= 1, code, '%s: %s more than once' % (label, flag))
    return _argv_value(argv, flag, code, label) if flag in argv else None


def _executed_record(result, *, name=None, kind=None, code):
    recs = [r for r in result.get('stage_records') or [] if isinstance(r, dict) and r.get('executed') is True
            and (name is None or r.get('name') == name) and (kind is None or r.get('kind') == kind)]
    need(len(recs) == 1, code, 'stage record (name %r, kind %r) not unique among executed records: %d' % (name, kind, len(recs)))
    r = recs[0]
    need(type(r.get('exit_code')) is int and r['exit_code'] == 0, code, 'stage %r exit code %r' % (r.get('name'), r.get('exit_code')))
    return r


def _request_of(rec, out, code):
    """The stage's request.json (driver L1842-1843), bound by the ctx record's request_sha256; it must be the record's
    request (script, argv, module patches): the stage shim applied exactly these patches (driver L709-753)."""
    _, raw = _own_bytes(rec.get('request_path'), out, 'stage request', rec.get('request_sha256'), code)
    req = _strict_json(raw, 'stage request', code)
    need(isinstance(req, dict), code, 'stage request not an object')
    for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'module_patches'):
        need(req.get(k) == rec.get(k), code, 'stage request %s differs from the ctx record' % k)
    return req


def _decode_value(v):
    """driver _decode_value L698-707, verbatim semantics."""
    from pathlib import Path
    if isinstance(v, dict) and len(v) == 1:
        (key, val), = v.items()
        if key == '__path__':
            return Path(val)
        if key == '__pathdict__':
            return {Path(p): s for p, s in val}
        if key == '__ordered__':
            return {p: s for p, s in val}
    return v


def _apply_prep_patches(prep, prep_path, prep_sha, patches):
    """The stage shim's module patch (driver L731-739): after the module's own code ran, each listed global is replaced
    (it must exist). Only the prep is a patch target of the manifest stage (driver uvt_prep_patches L1020-1028)."""
    need(isinstance(patches, list), C_PATCH, 'module_patches not a list')
    applied = []
    for p in patches:
        need(isinstance(p, dict) and set(p) == {'path', 'sha256', 'set'} and isinstance(p['set'], dict), C_PATCH, 'patch shape')
        need(os.path.realpath(str(p['path'])) == os.path.realpath(str(prep_path)), C_PATCH,
             'patch target %s is not the writer prep %s' % (p['path'], prep_path))
        need(p['sha256'] == prep_sha, C_PATCH, 'patch pin is not the prep sha')
        for name, value in p['set'].items():
            need(hasattr(prep, name), C_PATCH, 'Override target absent: %s' % name)
            setattr(prep, name, _decode_value(value))
            applied.append(name)
    return applied


# ------------------------------------------------------------------------------------------------ toolkit
class ProductionToolkit:
    """The pinned modules of a real call, exactly as the driver's stages load them. The synthetic suite substitutes a
    toolkit that differs only in: the call driver sha, the writer's prep (MW LOCAL['prep']), the checkpoint module sha, the
    roster module handed to the controller and the binding, and the binding's H2 component (its source is NGC3198-named)."""
    kind = 'PRODUCTION'
    driver_sha256 = DRIVER_SHA256
    writer = MANIFEST_WRITER
    binding = ROUTE_B_BINDING
    checkpoint_module_sha256 = CHECKPOINT_MODULE_SHA256

    def prep_pin(self, mw):
        p, s = mw.LOCAL['prep']                                     # MW L43-45 (8681da84)
        return str(p), s

    def controller_libraries(self, ctl_mod):
        return ctl_mod.load_libraries()                             # MW L209; controller L99-125

    def binding_roster(self, bmod):
        return bmod._load('roster')                                 # BB L67-75, PINS L43 (4366e3d6)

    def h2_component(self, bmod):
        return bmod.ngc_h2_component()[0]                           # BB L578-593 (pinned H2 reduction)


TOOLKIT = ProductionToolkit


def _writer(toolkit):
    mw = load_exact(toolkit.writer[0], toolkit.writer[1], 'ngc_recipes_c2v001_manifest_writer', C_WRITER)
    cp, cs = mw.PINS['controller']                                  # MW L46-49
    need(cs == CONTROLLER_SHA256, C_WRITER, 'writer controller pin')
    return mw, (str(cp), cs)


def _binding(toolkit, lib):
    bmod = load_exact(toolkit.binding[0], toolkit.binding[1], 'ngc_recipes_c2v001_route_b_binding', C_BIND)
    need(bmod.PINS['lib'][1] == LIBRARY_SHA256, C_BIND, 'binding library pin is not the S5 library (BB L42)')
    return bmod


# ------------------------------------------------------------------------------------------------ route A
def RECIPE_ROUTE_A(*, call_dir, out_dir, result, target, lib, provider, toolkit=None):
    """A route-A iterate state: the NGC manifest writer's rebuild (MW main L191-232) at iteration m instead of the accepted
    iteration, i.e. the controller's own build path at m (controller _i1t L372-393, _build L395-406):
        roster = roster_route_a(stars, init_rings, elements[:m], r, s_edges, kpc_m, M_s, c_m_s)   (controller L396-397)
        build  = config, kept, gamma_eff, c_m_s, eval_radii, i1t = _i1t(m, gas_m), 'route_a'      (controller L399-401)
    with the static parts from from_prepared on the reviewed prep (with the driver's prep patches) and the seed numerical
    inputs (MW L225-227), the element rosters 0..m-1 from the sidecar (MW L124-148), r from the sidecar identity (MW L155) and
    gas_m from the checkpoint iteration_m/START.json (MW L217-221). Target -> m (reader s5_targets L342-351):
      (n, current)            m = n            (payload[n].state_digest, controller L490/L496)
      (n, next), n < a        m = n + 1        only if payload[n].next_state_digest == payload[n+1].state_digest
      (a, next) or a broken chain              REFUSED: ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED (module docstring)."""
    import numpy as np
    tk = toolkit or TOOLKIT()
    out = os.path.realpath(str(out_dir))
    prov = {'recipe': 'RECIPE_ROUTE_A', 'toolkit': tk.kind, 'inputs': {}}
    inputs = prov['inputs']
    og, st = target['origin'], target['state']
    need(og.get('kind') == 'ROUTE_A_ITERATE' and og.get('role') in (CURRENT, NEXT) and type(og.get('iteration')) is int
         and st.get('stage_kind') == 'route_a', C_TARGET, 'not a route-A iterate target')
    uv = result.get('uv_tail') or {}
    rar = uv.get('route_a_record')
    need(isinstance(rar, dict) and type(rar.get('accepted_iteration')) is int, C_SIDECAR, 'route_a_record (driver L8693)')
    a, n, role = rar['accepted_iteration'], og['iteration'], og['role']
    need(0 <= n <= a, C_RANGE, 'iteration %d outside 0..%d' % (n, a))
    if role == NEXT and n == a:
        raise RecipeRefusal(C_NEXT_GAS, 'the monitor-next state of the accepted iteration %d: gas_%d = (1-r) gas_%d + r '
                                        'updated_%d (controller L483) is not recorded; no checkpoint START holds it '
                                        '(driver L7024-7038)' % (a, a + 1, a, a))
    # ---- the manifest stage (driver L8697-8700) and its writer
    mrec = _executed_record(result, kind=MANIFEST_KIND, code=C_MSTAGE)
    need(mrec.get('script_sha256') == tk.writer[1], C_WRITER, 'manifest stage script %s' % mrec.get('script_sha256'))
    req = _request_of(mrec, out, C_MSTAGE)
    need('stage_dict_items' not in req and 'stage_dict_items' not in mrec, C_PATCH,
         'stage_dict_items (LOCAL prep replacement; driver L8701-8702 sets it only for prep_v008/v009, never NGC)')
    need(req.get('mask') is None and not req.get('stage_globals'), C_PATCH,
         'the manifest stage runs with no mask wrapper and no stage globals (driver L8699, ctx.request L1820-1823)')
    argv = mrec['argv']

    def av(flag):
        return _argv_value(argv, flag, C_MSTAGE, 'manifest argv')
    seed_path, seed_raw = _own_bytes(av('--seed'), out, 'seed', av('--seed-sha256'), C_PIN)
    seed = _strict_json(seed_raw, 'seed', C_PIN)
    ident_seed = (result.get('identity') or {}).get('seed') or {}
    need(ident_seed.get('sha256') == av('--seed-sha256') and os.path.realpath(str(ident_seed.get('path'))) == seed_path,
         C_PIN, 'seed is not identity.seed (driver L8464)')
    att = _own_path(av('--attempt-directory'), out, 'attempt directory')
    cp = _own_path(av('--checkpoint-directory'), out, 'checkpoint directory')
    rrec = _executed_record(result, kind='route_a', code=C_MSTAGE)                         # driver L8607-8618
    rargv = rrec.get('argv')
    need(os.path.realpath(_argv_value(rargv, '--outdir', C_MSTAGE, 'route_a argv')) == att
         and os.path.realpath(_argv_value(rargv, '--checkpoint-directory', C_MSTAGE, 'route_a argv')) == cp, C_MSTAGE,
         'manifest attempt/checkpoint are not the route_a stage outdir/checkpoint (driver L8607, L8698)')
    req_path, raw_req = _own_bytes(av('--uv-tail-request'), out, 'uv-tail request', av('--uv-tail-request-sha256'), C_PIN)
    raw_request = _strict_json(raw_req, 'uv-tail request', C_PIN)
    mdir = _own_path(av('--outdir'), out, 'manifest outdir')
    man_pin = uv.get('manifest') or {}
    need(os.path.realpath(str(man_pin.get('path'))) == os.path.join(mdir, 'ROUTE_A_TAIL_MANIFEST.json'), C_MSTAGE,
         'result manifest is not this stage outdir (driver L8703-8706)')
    cm_path, cm_sha = av('--checkpoint-module'), av('--checkpoint-module-sha256')
    need(cm_sha == tk.checkpoint_module_sha256, C_PIN, 'checkpoint module %s is not the driver pin (AUX L253)' % cm_sha)
    inputs.update(
        seed={'basis': FORMAL, 'cite': 'manifest argv --seed (driver L8698, L8450); MW L198-203, L225', 'pin': {'path': seed_path, 'sha256': av('--seed-sha256')}},
        request={'basis': FORMAL, 'cite': 'manifest argv --uv-tail-request (driver L8698, L5286); MW L208-210', 'pin': {'path': req_path, 'sha256': av('--uv-tail-request-sha256')}},
        module_patches={'basis': FORMAL, 'cite': 'manifest request.json module_patches (driver L8699, L1020-1028, L731-739)', 'value': req['module_patches']},
        checkpoint_module={'basis': FORMAL, 'cite': 'manifest argv --checkpoint-module (driver L8698, AUX L253)', 'pin': {'path': cm_path, 'sha256': cm_sha}})
    # ---- seed provenance pins (MW L201-203)
    pins = seed.get('pins')
    need(isinstance(pins, dict), C_PIN, 'seed pins')
    for p, s in sorted(pins.items()):
        _pinned_bytes(p, s, 'seed pin ' + os.path.basename(p))
    # ---- modules: the writer, its controller (MW PINS), the checkpoint module (manifest argv)
    mw, ctl_pin = _writer(tk)
    ctl_mod = load_exact(ctl_pin[0], ctl_pin[1], 'ngc_recipes_c2v001_route_a_controller', C_WRITER)
    cm = load_exact(os.path.realpath(cm_path), cm_sha, 'ngc_recipes_c2v001_checkpoint', C_PIN)
    libs = tk.controller_libraries(ctl_mod)
    req_norm = ctl_mod.normalize_request(raw_request, libs['lib'])                       # MW L210
    # ---- the attempt (MW L211, L98-121) and the checkpoint identity (MW L213-216)
    try:
        _, rsha, auv = mw.attempt_tail_record(att, req_norm['sha256'])
    except (mw.ManifestRefusal, OSError, KeyError, TypeError, ValueError) as exc:
        raise RecipeRefusal(C_ATTEMPT, '%s: %s' % (type(exc).__name__, exc))
    need(auv.get('accepted_iteration') == a, C_ATTEMPT, 'attempt accepted iteration %r != route_a_record %d' % (auv.get('accepted_iteration'), a))
    try:
        ident = cm._read(str(os.path.join(cp, 'IDENTITY.json')), 'identity')
    except Exception as exc:                                     # the checkpoint module's own refusal types
        raise RecipeRefusal(C_CKPT, 'IDENTITY %s: %s' % (type(exc).__name__, exc))
    need(auv.get('checkpoint_identity_sha256') == ident.get('identity_sha256'), C_CKPT, 'attempt checkpoint identity (MW L215)')
    cust = ((result.get('identity') or {}).get('route_a') or {}).get('custody') or {}
    need(cust.get('identity_sha256') == ident.get('identity_sha256') and cust.get('iteration') == a, C_CKPT,
         'identity.route_a.custody is not this checkpoint identity / accepted iteration (driver L8682, L6900)')
    # ---- the sidecar (MW L222-224; controller L329-363, L470-525)
    sc = auv.get('sidecar')
    need(isinstance(sc, dict) and sc == rar.get('sidecar'), C_SIDECAR, 'attempt sidecar is not route_a_record.sidecar (driver L8693)')
    sdir = _own_path(sc['directory'], out, 'sidecar directory')
    need(os.path.realpath(_argv_value(rargv, '--uv-tail-sidecar-directory', C_SIDECAR, 'route_a argv')) == sdir, C_SIDECAR,
         'sidecar is not the route_a stage --uv-tail-sidecar-directory (driver L8628)')
    files = sc.get('files')
    need(isinstance(files, dict) and 'SIDECAR_IDENTITY.json' in files, C_SIDECAR, 'sidecar files')
    _, sid_raw = _own_bytes(os.path.join(sdir, 'SIDECAR_IDENTITY.json'), out, 'sidecar identity', files['SIDECAR_IDENTITY.json'], C_SIDECAR)
    sid_doc = _strict_json(sid_raw, 'sidecar identity', C_SIDECAR)
    sid = sid_doc.get('identity') if isinstance(sid_doc, dict) else None
    need(isinstance(sid, dict) and sid_doc.get('identity_sha256') == _sha_bytes(_canon(sid).encode()), C_SIDECAR,
         'sidecar identity self-sha (controller L363)')
    # ---- target -> iteration m
    m = n if role == CURRENT else n + 1
    for i in range(m):                                               # the element rosters 0..m-1 must be listed (controller L553-556)
        need('elements_%04d.npz' % i in files, C_ELEMENT, 'elements_%04d.npz is not in the sidecar finish file list' % i)
    try:
        records, elements = mw.sidecar_elements(sdir, m)              # MW L124-148: records 0..m, elements 0..m-1 (digests checked)
    except mw.ManifestRefusal as exc:
        raise RecipeRefusal(C_ELEMENT, str(exc))
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise RecipeRefusal(C_ELEMENT, '%s: %s' % (type(exc).__name__, exc))
    for i in range(m + 1):
        need(records[i].get('relaxation') == sid.get('relaxation'), C_SIDECAR, 'iteration %d relaxation' % i)
    if role == CURRENT:
        need(records[m].get('state_digest') == st['state_sha256'], C_ITERATE,
             'payload[%d].state_digest is not the target (controller L490, L496)' % m)
        recorded_i1t = [records[m].get('i1t')]
    else:
        need(records[n].get('next_state_digest') == st['state_sha256'], C_ITERATE, 'payload[%d].next_state_digest is not the target' % n)
        if records[n + 1].get('state_digest') != st['state_sha256']:
            raise RecipeRefusal(C_NEXT_GAS, 'the monitor-next state of iteration %d is not iteration %d begun state; its gas '
                                            '(1-r) gas_%d + r updated_%d (controller L483) is not recorded' % (n, n + 1, n, n))
        recorded_i1t = [records[n].get('next_i1t'), records[m].get('i1t')]
    inputs.update(
        relaxation={'basis': FORMAL, 'cite': 'SIDECAR_IDENTITY identity.relaxation (controller L335, L363); MW L155', 'value': sid.get('relaxation')},
        elements={'basis': FORMAL, 'cite': 'sidecar elements_0000..%04d.npz, digests in iteration payloads (controller L495-499, L518-519); MW L124-148' % (m - 1),
                  'files': {('elements_%04d.npz' % i): files['elements_%04d.npz' % i] for i in range(m)}},
        iteration={'basis': FORMAL, 'cite': 'reader s5_targets L342-351 origin; payload digests controller L490/L496', 'm': m, 'origin': dict(og)})
    # ---- checkpoint iteration m: START/COMPLETED bound to the identity, gas_m (MW L217-221; driver L7031-7036)
    try:
        start = cm._read(str(os.path.join(cp, 'iteration_%04d' % m, 'START.json')), 'iteration_start')
        done = cm._read(str(os.path.join(cp, 'iteration_%04d' % m, 'COMPLETED.json')), 'iteration_completed')
    except Exception as exc:
        raise RecipeRefusal(C_CKPT, 'iteration %d records %s: %s' % (m, type(exc).__name__, exc))
    need(start.get('iteration') == m and done.get('iteration') == m and start.get('identity_sha256') == ident['identity_sha256']
         and done.get('identity_sha256') == ident['identity_sha256'] and done.get('iteration_start_sha256') == start.get('payload_sha256')
         and type(done.get('converged')) is bool and done['converged'] == (m == a), C_CKPT,
         'iteration %d START/COMPLETED not bound to this identity and iteration (driver L7033-7037)' % m)
    try:
        gas = cm._get(str(cp), start['gas_fourier_J'])
    except Exception as exc:
        raise RecipeRefusal(C_GAS, 'iteration %d gas_fourier_J %s: %s' % (m, type(exc).__name__, exc))
    inputs['gas'] = {'basis': FORMAL, 'cite': 'checkpoint iteration_%04d/START.json gas_fourier_J via the checkpoint module _get (MW L217, L221)' % m,
                     'start_payload_sha256': start.get('payload_sha256'), 'ref': start.get('gas_fourier_J')}
    # ---- the writer's prep with the driver's patches; the controller from_prepared (MW L206-207, L225-231)
    ppath, psha = tk.prep_pin(mw)
    prep = load_exact(os.path.realpath(ppath), psha, 'root_composite_prep', C_PIN)
    applied = _apply_prep_patches(prep, ppath, psha, req['module_patches'])
    ni = seed.get('numerical_inputs')
    need(isinstance(ni, dict), C_PIN, 'seed numerical_inputs')
    try:
        data = prep.prepare_inputs(**ni)
        ctl = ctl_mod.RouteATailController.from_prepared(galaxy=GALAXY, prep_module=prep, prep_arguments=ni, data=data,
                                                         request=raw_request, sidecar_directory=None, libraries=libs)
    except ctl_mod.UVTailRouteAError as exc:
        raise RecipeRefusal(C_IDENT, 'from_prepared: %s' % exc)
    want = dict(ctl.static_identity, relaxation=float(sid['relaxation']), checkpoint_identity_sha256=ident['identity_sha256'])
    if json.loads(_canon(want)) != sid:
        diff = sorted(k for k in set(want) | set(sid) if json.loads(_canon(want.get(k))) != sid.get(k))
        raise RecipeRefusal(C_IDENT, 'rebuilt controller identity differs from SIDECAR_IDENTITY in %s (MW L228-231)' % diff)
    inputs['prep'] = {'basis': FORMAL, 'cite': 'MW LOCAL[prep] L43-45 with the manifest stage patches; from_prepared controller L219-284; MW L225-231',
                      'pin': {'path': ppath, 'sha256': psha}, 'patched_globals': applied, 'controller': {'path': ctl_pin[0], 'sha256': ctl_pin[1]}}
    # ---- I1-T at m and the roster (MW rebuild_state L151-159 = controller _i1t / _build)
    ctl.relaxation = float(sid['relaxation'])
    ctl.elements = list(elements[:m])
    ctl._T_upd = []
    ctl._T_init = None
    try:
        i1t = ctl._i1t(m, gas)
    except ctl_mod.UVTailRouteAError as exc:
        raise RecipeRefusal(C_I1T, 'iteration %d: %s (controller L372-393)' % (m, exc))
    got = _canon(ctl_mod._plain(i1t))
    need(all(isinstance(x, dict) and _canon(x) == got for x in recorded_i1t), C_I1T_REC,
         'the recomputed I1-T at %d is not the recorded payload i1t (controller L497-498)' % m)
    roster = ctl.rs.roster_route_a(ctl.stars, ctl.init_rings, ctl.elements[:m], ctl.relaxation, s_edges_kpc2=ctl.s_edges,
                                   kpc_m=ctl.kpc_m, M_s=ctl.M_s, c_m_s=ctl.c_m_s)
    build = {'config': ctl.config, 'kept': ctl.kept, 'gamma_eff': ctl.gamma_eff, 'c_m_s': ctl.c_m_s,
             'eval_radii_m': np.asarray(ctl.eval_radii, dtype=float), 'i1t': i1t, 'stage_kind': 'route_a'}
    inputs.update(
        roster={'basis': FORMAL, 'cite': 'controller _build L396-397 (roster_route_a)'},
        build={'basis': FORMAL, 'cite': 'controller _build L399-401; kept L190, gamma_eff/c_m_s L191, eval radii L196-197'},
        i1t={'basis': FORMAL, 'cite': 'controller _i1t L372-393 on gas_m; equal to the recorded payload i1t (L497-498)'})
    prov['attempt_result_sha256'] = rsha
    return {'roster': roster, 'build': build, 'provenance': prov}


# ------------------------------------------------------------------------------------------------ route B
def _route_b_context(*, out, result, target, lib, toolkit, want_kind):
    """Common route-B inputs (binding bind/bind_offset): the stage's ctx record and finish.json, config, kept, i1t, seed,
    the binding module and its roster module, gamma_eff and c_m_s."""
    tk = toolkit
    og, st = target['origin'], target['state']
    need(og.get('kind') == 'ROUTE_B_STAGE' and isinstance(og.get('stage'), str), C_TARGET, 'not a route-B stage target')
    rec = _executed_record(result, name=og['stage'], code=C_BSTAGE)
    ckind = rec.get('kind')
    need(ckind in UVT_BINDING_KIND, C_BSTAGE, 'stage %r kind %r is not a tail kind (driver L351)' % (og['stage'], ckind))
    bkind = UVT_BINDING_KIND[ckind]
    need(bkind not in INHERITED_KINDS, C_INHERIT, '%s reuses the accepted manifest state (BB L457-470); S5 never rebuilds it' % bkind)
    need(bkind == want_kind == st.get('stage_kind'), C_BKIND,
         'stage %r binding kind %r, recipe kind %r, target stage_kind %r' % (og['stage'], bkind, want_kind, st.get('stage_kind')))
    argv = rec.get('argv')
    outdir = _own_path(_argv_value(argv, '--outdir', C_BSTAGE, og['stage']), out, og['stage'] + ' outdir')
    srec = [e for e in (result.get('uv_tail') or {}).get('stage_records') or [] if isinstance(e, dict) and e.get('stage') == og['stage']]
    need(len(srec) == 1 and srec[0].get('kind') == ckind, C_BFIN, 'uv_tail stage record (driver L1155-1172)')
    fpath, fraw = _own_bytes(os.path.join(outdir, 'finish.json'), out, og['stage'] + ' finish', srec[0].get('finish_sha256'), C_BFIN)
    fin = _strict_json(fraw, og['stage'] + ' finish', C_BFIN)
    u = fin.get('uv_tail') if isinstance(fin, dict) else None
    need(isinstance(u, dict) and u.get('schema') == STAGE_RECORD_SCHEMA and u.get('enabled') is True, C_BFIN, 'finish uv_tail record (BB L352)')
    need(u.get('stage_kind') == bkind, C_BKIND, 'finish stage_kind %r != binding kind %r (BB L352)' % (u.get('stage_kind'), bkind))
    need(u.get('state_digest') == st['state_sha256'] == srec[0].get('state_digest') and u.get('empty') is False, C_BSTATE,
         'finish state digest is not the target (BB L358)')
    need(st.get('source_sha256') is None or u.get('roster_digest') == st['source_sha256'], C_BSTATE, 'finish roster digest (BB L359)')
    need(u.get('binding_sha256') == tk.binding[1], C_BIND, 'stage binding %s (BB L352)' % u.get('binding_sha256'))
    # config (BB L692-699; recorded L356-357)
    cpath, craw = _own_bytes(_argv_value(argv, '--uv-tail-config', C_BSTAGE, og['stage']), out, 'uv-tail config',
                             _argv_value(argv, '--uv-tail-config-sha256', C_BSTAGE, og['stage']), C_CFG)
    try:
        cfg = lib.normalize_config(json.loads(craw))
    except (ValueError, TypeError) as exc:
        raise RecipeRefusal(C_CFG, 'normalize_config: %s' % exc)
    need(cfg == u.get('config') and cfg['sha256'] == u.get('config_sha256') and _sha_bytes(craw) == u.get('config_file_sha256'),
         C_CFG, 'the stage config is not the recorded config (BB L356-357)')
    # seed (common argv L8736; identity.seed L8464)
    spath = _own_path(_argv_value(argv, '--seed', C_BSTAGE, og['stage']), out, 'seed')
    ident_seed = (result.get('identity') or {}).get('seed') or {}
    need(os.path.realpath(str(ident_seed.get('path'))) == spath, C_SEED, 'stage seed is not identity.seed (driver L8464)')
    _, sraw = _own_bytes(spath, out, 'seed', ident_seed.get('sha256'), C_SEED)
    seed = _strict_json(sraw, 'seed', C_SEED)
    ni = seed.get('numerical_inputs')
    need(isinstance(ni, dict), C_SEED, 'seed numerical_inputs')
    # binding module (its own grid edge, truncation and kept-region code), roster module
    bmod = _binding(tk, lib)
    b = bmod.Binding(types.SimpleNamespace(uv_tail_truncation=_argv_optional(argv, '--uv-tail-truncation', C_BSTAGE, og['stage']),
                                           uv_tail_admit_test_only=('--uv-tail-admit-test-only' in argv)), bkind, cfg, u.get('config_file_sha256'))
    b.lib = lib
    try:
        K_m = b._grid_K(ni, [[0.0, 0.0, 0.0]])        # BB L235-258 (the stage-wave containment check is the stage's own)
        tr = b._truncation() if bkind in bmod.MASK_KINDS else None                     # BB L261-268, L271
        kept = lib.kept_region(bkind, tr, K_m)                                         # BB L272
    except (ValueError, TypeError, KeyError) as exc:
        raise RecipeRefusal(C_KEPT, '%s: %s' % (type(exc).__name__, exc))
    need(kept == u.get('kept'), C_KEPT, 'recomputed kept %s != recorded %s (BB L357)' % (kept, u.get('kept')))
    i1t = u.get('i1t')
    need(isinstance(i1t, dict) and i1t.get('verdict') in ('PASS', 'NOT_APPLICABLE_SYNTHETIC'), C_I1T_B,
         'finish uv_tail.i1t (BB L359: the dict handed to build, L528-531 / L558)')
    rs = tk.binding_roster(bmod)
    b.rs = rs
    # gamma_eff, c_m_s: DECLARED (BB L372 phys from the successor) = the call's accepted route-A state record
    mpin = (result.get('uv_tail') or {}).get('manifest') or {}
    mpath, mraw = _own_bytes(mpin.get('path'), out, 'route-A tail manifest', mpin.get('sha256'), C_MANIFEST)
    man = _strict_json(mraw, 'route-A tail manifest', C_MANIFEST)
    mrec = ((man.get('state') or {}).get('record') or {}) if isinstance(man, dict) else {}
    g, c = mrec.get('gamma_eff'), mrec.get('c_m_s')
    need(type(g) is float and type(c) is float and math.isfinite(g) and math.isfinite(c) and g > 0 and c > 0, C_PHYS,
         'accepted state record gamma_eff / c_m_s (MW L170, L180; lib L685-686)')
    ctx = {'bmod': bmod, 'b': b, 'rs': rs, 'K_m': K_m, 'cfg': cfg, 'kept': kept, 'i1t': i1t, 'ni': ni, 'u': u, 'fin': fin, 'argv': argv,
           'bkind': bkind, 'stage': og['stage'], 'gamma': g, 'c': c, 'man': man, 'man_pin': {'path': mpath, 'sha256': mpin.get('sha256')},
           'kpc': float(ni['kpc_m']), 'M_s': cfg['gas']['M_s']}
    ctx['prov'] = {'recipe': 'RECIPE_ROUTE_B_' + bkind, 'toolkit': tk.kind, 'stage': og['stage'], 'inputs': {
        'finish': {'basis': FORMAL, 'cite': 'stage --outdir finish.json bound by uv_tail.stage_records (driver L1155-1172)', 'pin': {'path': fpath, 'sha256': srec[0].get('finish_sha256')}},
        'config': {'basis': FORMAL, 'cite': 'argv --uv-tail-config (driver L8714); BB L692-699; recorded L356-357', 'pin': {'path': cpath, 'sha256': _sha_bytes(craw)}},
        'kept': {'basis': FORMAL, 'cite': 'lib.kept_region(kind, truncation, K_m) BB L270-272; K_m BB L235-258; truncation argv (driver L8717-8718)', 'value': kept},
        'i1t': {'basis': FORMAL, 'cite': 'finish uv_tail.i1t = the build i1t (BB L528-531 / L558, L359)'},
        'stage_kind': {'basis': FORMAL, 'cite': 'BB L373 stage_kind=self.kind; driver L352-354', 'value': bkind},
        'gamma_eff_c_m_s': {'basis': DECLARED, 'cite': 'BB L372 phys (successor argument); value = the accepted route-A state record (MW L177-181; lib L686), the bits A167 C4b requires of every NGC state', 'pin': {'path': mpath, 'sha256': mpin.get('sha256')}}}}
    return ctx


def _sidecar_profile(result, out, u):
    """DECLARED: the route-B successor's registered profile pin = the route-A prep profile recorded in the sidecar identity
    (controller L235, L216, L363); with an NGC outer gas cut the binding records it (BB L435), and it must be the same pin."""
    sc = ((result.get('uv_tail') or {}).get('route_a_record') or {}).get('sidecar') or {}
    files = sc.get('files') or {}
    need(isinstance(sc.get('directory'), str) and 'SIDECAR_IDENTITY.json' in files, C_PROFILE, 'route-A sidecar identity unrecorded')
    _, raw = _own_bytes(os.path.join(sc['directory'], 'SIDECAR_IDENTITY.json'), out, 'sidecar identity', files['SIDECAR_IDENTITY.json'], C_PROFILE)
    doc = _strict_json(raw, 'sidecar identity', C_PROFILE)
    pin = (((doc.get('identity') or {}).get('provenance') or {}).get('profile')) if isinstance(doc, dict) else None
    need(isinstance(pin, dict) and isinstance(pin.get('path'), str) and _is_sha(pin.get('sha256')), C_PROFILE, 'sidecar identity provenance.profile (controller L235)')
    cut = u.get('ngc_outer_gas_cut_custody')
    basis = DECLARED
    if isinstance(cut, dict) and cut.get('profile_pin') is not None:
        need(cut['profile_pin'] == {'path': pin['path'], 'sha256': pin['sha256']}, C_PROFILE, 'BB L435 profile pin differs from the route-A profile')
        basis = FORMAL
    raw = _pinned_bytes(pin['path'], pin['sha256'], 'registered profile', C_PROFILE)
    return json.loads(raw), {'basis': basis, 'cite': 'BB bind profile argument (successor); route-A sidecar identity provenance.profile (controller L235); BB L435 when an outer cut is set', 'pin': {'path': pin['path'], 'sha256': pin['sha256']}}


def _stars(ctx, toolkit, prof):
    """BB _stars L325-334 (the continuum stars; the GL4 and H2 packet rings there are the I1-T replica only)."""
    ni = ctx['ni']
    units = dict(kpc_m=float(ni['kpc_m']), solar_mass_kg=float(ni['solar_mass_kg']))     # BB L331
    extra = toolkit.h2_component(ctx['bmod'])                                           # BB L332, L578-593
    return ctx['rs'].stars_registered(prof, GALAXY, units=units, extra_components=(extra,))   # BB L334


def _producer_finish(result, out, argv, flag, stage_name, label, code):
    """A producer stage's finish.json reached through this stage's argv directory, bound by the uv_tail stage records."""
    d = _own_path(_argv_value(argv, flag, code, label), out, label)
    srec = [e for e in (result.get('uv_tail') or {}).get('stage_records') or [] if isinstance(e, dict) and e.get('stage') == stage_name]
    sha = srec[0].get('finish_sha256') if len(srec) == 1 else None
    need(_is_sha(sha), code, '%s finish is not a recorded uv_tail stage (%s)' % (label, stage_name))
    p, raw = _own_bytes(os.path.join(d, 'finish.json'), out, label + ' finish', sha, code)
    return d, _strict_json(raw, label + ' finish', code), {'path': p, 'sha256': sha}


def _output_npz(fin, d, out, name, label, code):
    """DECLARED producer output file: finish['outputs'][name] = {path, sha256} when recorded (BB L493 form), else <dir>/name."""
    o = (fin.get('outputs') or {}).get(name) if isinstance(fin, dict) else None
    if isinstance(o, dict) and _is_sha(o.get('sha256')):
        p, raw = _own_bytes(o.get('path'), out, label, o['sha256'], code)
        how = 'producer finish outputs[%s] (BB L493 form)' % name
    else:
        p, raw = _own_bytes(os.path.join(d, name), out, label, None, code)
        how = '<producer dir>/%s (no sha in a named record)' % name
    return _npz(raw, label, code), {'path': p, 'sha256': _sha_bytes(raw), 'how': how}


def _base_arrays(ctx, result, out):
    off_dir, off_fin, off_pin = _producer_finish(result, out, ctx['argv'], '--offset-directory', 'offset', 'offset', C_BASE)
    base, bpin = _output_npz(off_fin, off_dir, out, BASE_ARRAYS, 'offset updated_base_arrays', C_BASE)
    need(all(k in base for k in ('physical_positions_m', 'rho0', 'volume_weights_m3', 'radial_nodes_m')), C_BASE, 'base array keys')
    return base, bpin, off_fin, off_pin


def _own_roster_radii(base):
    """DECLARED eval radii of the own-roster kinds (BB L372 `radii` from the successor): the unique radial nodes of the
    offset updated_base_arrays, the radial-node set every downstream stage reads from that file (driver L629-631)."""
    import numpy as np
    return np.unique(np.asarray(base['radial_nodes_m'], dtype=float))


def _route_b_fs(kind, *, call_dir, out_dir, result, target, lib, provider, toolkit):
    """fs_columns / fs_rotation (BB L476-501): stars (registered profile + H2) + body gas from the offset
    updated_base_arrays: J = -c^2 rho0 vol at physical_positions_m (BB L489-492)."""
    import numpy as np
    tk = toolkit or TOOLKIT()
    out = os.path.realpath(str(out_dir))
    ctx = _route_b_context(out=out, result=result, target=target, lib=lib, toolkit=tk, want_kind=kind)
    prof, ppro = _sidecar_profile(result, out, ctx['u'])
    s_edges = prof['galaxies'][GALAXY]['HI_plus_He']['s_edges_kpc2']                          # BB L481
    stars = _stars(ctx, tk, prof)
    base, bpin, off_fin, _ = _base_arrays(ctx, result, out)
    ref = (off_fin.get('outputs') or {}).get(SOURCE_OFFSET)
    need(isinstance(ref, dict) and (ctx['u'].get('source') or {}).get('new_body') == ref, C_BASE,
         'stage source.new_body is not the offset source_offset.npz pin (BB L493, L501)')
    c = ctx['c']
    pos = np.asarray(base['physical_positions_m'], float).reshape(-1, 3)                      # BB L489
    J = (-c * c * np.asarray(base['rho0']) * np.asarray(base['volume_weights_m3'])).reshape(-1)   # BB L490
    roster = ctx['rs'].roster_body({'physical_positions_m': pos, 'base_integrated_source_J': J}, stars,
                                   s_edges_kpc2=s_edges, kpc_m=ctx['kpc'], M_s=ctx['M_s'], c_m_s=c)   # BB L491-492
    radii = _own_roster_radii(base)
    ctx['prov']['inputs'].update(
        profile=ppro, h2={'basis': FORMAL if tk.kind == 'PRODUCTION' else 'SYNTHETIC', 'cite': 'BB ngc_h2_component L578-593'},
        base_arrays={'basis': DECLARED, 'cite': 'BB L21 / L489-490 base = offset updated_base_arrays (driver L3310); argv --offset-directory (driver L8796)', 'pin': bpin},
        roster={'basis': FORMAL, 'cite': 'BB L489-492 roster_body(stars + body gas)'},
        eval_radii_m={'basis': DECLARED, 'cite': 'BB L372 radii (successor); unique offset updated_base_arrays radial_nodes_m (driver L629-631)'})
    return _done(ctx, roster, radii)


def _route_b_rotation(kind, *, call_dir, out_dir, result, target, lib, provider, toolkit):
    """rfs_columns / le_columns / le_rotation (BB L502-514): stars + the rings of the rotation the feedback transformed:
    arr = {rho0, volume_weights_m3, radial_nodes_m, z} of <--uv-tail-source-rotation-directory>/finish.json arrays_path."""
    tk = toolkit or TOOLKIT()
    out = os.path.realpath(str(out_dir))
    ctx = _route_b_context(out=out, result=result, target=target, lib=lib, toolkit=tk, want_kind=kind)
    prof, ppro = _sidecar_profile(result, out, ctx['u'])
    s_edges = prof['galaxies'][GALAXY]['HI_plus_He']['s_edges_kpc2']
    stars = _stars(ctx, tk, prof)
    d = _own_path(_argv_value(ctx['argv'], '--uv-tail-source-rotation-directory', C_SROT, ctx['stage']), out, 'source rotation')
    src = (ctx['u'].get('source') or {}).get('source_rotation') or {}
    need(os.path.realpath(str(src.get('directory'))) == d, C_SROT, 'finish source.source_rotation.directory (BB L525-526)')
    rp, rraw = _own_bytes(os.path.join(d, 'finish.json'), out, 'source rotation finish', src.get('finish_sha256'), C_SROT)
    rfin = _strict_json(rraw, 'source rotation finish', C_SROT)
    ap, araw = _own_bytes(rfin.get('arrays_path'), out, 'source rotation arrays', rfin.get('arrays_sha256'), C_SROT)   # BB L510-511
    z = _npz(araw, 'source rotation arrays', C_SROT)
    need(all(k in z for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')), C_SROT, 'rotation array keys (BB L513)')
    arr = {kk: z[kk].copy() for kk in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}                       # BB L512-513
    roster = ctx['rs'].roster_rotation(arr, stars, s_edges_kpc2=s_edges, kpc_m=ctx['kpc'], M_s=ctx['M_s'])         # BB L514
    base, bpin, _, _ = _base_arrays(ctx, result, out)
    radii = _own_roster_radii(base)
    ctx['prov']['inputs'].update(
        profile=ppro, h2={'basis': FORMAL if tk.kind == 'PRODUCTION' else 'SYNTHETIC', 'cite': 'BB ngc_h2_component L578-593'},
        source_rotation={'basis': FORMAL, 'cite': 'argv --uv-tail-source-rotation-directory (driver L8719-8720); BB L503-513, L525-526',
                         'finish': {'path': rp, 'sha256': src.get('finish_sha256')}, 'arrays': {'path': ap, 'sha256': rfin.get('arrays_sha256')}},
        roster={'basis': FORMAL, 'cite': 'BB L514 roster_rotation(arr, stars)'},
        eval_radii_m={'basis': DECLARED, 'cite': 'BB L372 radii (successor); unique offset updated_base_arrays radial_nodes_m (driver L629-631)', 'pin': bpin})
    return _done(ctx, roster, radii)


def RECIPE_ROUTE_B_offset(*, call_dir, out_dir, result, target, lib, provider, toolkit=None):
    """offset (BB bind_offset L534-568): roster = _DifferenceRoster(body_r, ra_roster, synthetic or i1t verdict != PASS) with
    body_r = roster_body(body positions / base_integrated_source_J[...,0,0], no stars) (BB L549-552) and ra_roster = the
    route-A gas_IT roster of the call's ROUTE_A_TAIL_MANIFEST (BB L407-427, manifest validated by BB _manifest L379-405);
    eval radii = unique(body radial_nodes_m) (BB L560)."""
    import numpy as np
    tk = toolkit or TOOLKIT()
    out = os.path.realpath(str(out_dir))
    ctx = _route_b_context(out=out, result=result, target=target, lib=lib, toolkit=tk, want_kind='offset')
    b, argv = ctx['b'], ctx['argv']
    mpath = _own_path(_argv_value(argv, '--route-a-tail-manifest', C_MANIFEST, 'offset'), out, 'offset manifest argv')
    msha = _argv_value(argv, '--route-a-tail-manifest-sha256', C_MANIFEST, 'offset')
    need({'path': mpath, 'sha256': msha} == ctx['man_pin'], C_MANIFEST, 'offset manifest argv is not result.uv_tail.manifest (driver L8715-8716)')
    cust = ((result.get('identity') or {}).get('route_a') or {}).get('custody') or {}
    b.args.route_a_tail_manifest, b.args.route_a_tail_manifest_sha256 = mpath, msha
    b.jn = provider.create_provider()
    try:
        K_cube = lib.kept_region('route_a', None, ctx['K_m'])                                        # BB L544
        man, ra_state, mref = b._manifest(cust.get('identity_sha256'), cust.get('iteration'),
                                          {'payload_sha256': cust.get('start_payload_sha256')}, K_cube)   # BB L545, L379-405
        ra_roster, synthetic = b._manifest_gas_roster(man, ctx['ni'])                                  # BB L407-427
    except (ValueError, TypeError, KeyError, OSError) as exc:
        raise RecipeRefusal(C_MANIFEST, '%s: %s (BB L379-427)' % (type(exc).__name__, exc))
    prof, ppro = _sidecar_profile(result, out, ctx['u'])
    s_edges = prof['galaxies'][GALAXY]['HI_plus_He']['s_edges_kpc2']                                  # BB L546-547
    body_dir, body_fin, body_pin = _producer_finish(result, out, argv, '--body-directory', 'body', 'body', C_BODY)
    need(_argv_value(argv, '--body-finish-sha256', C_BODY, 'offset') == body_pin['sha256'], C_BODY, 'offset --body-finish-sha256 (driver L8778)')
    body, bpin = _output_npz(body_fin, body_dir, out, BODY_ARRAYS, 'body arrays', C_BODY)
    need(all(k in body for k in ('physical_positions_m', 'base_integrated_source_J', 'radial_nodes_m')), C_BODY, 'body array keys (BB L549-560)')
    c = ctx['c']
    pos = np.asarray(body['physical_positions_m'], float).reshape(-1, 3)                              # BB L549
    J = np.asarray(body['base_integrated_source_J'])[..., 0, 0].reshape(-1)                           # BB L550
    body_r = ctx['rs'].roster_body({'physical_positions_m': pos, 'base_integrated_source_J': J}, None,
                                   s_edges_kpc2=s_edges, kpc_m=ctx['kpc'], M_s=ctx['M_s'], c_m_s=c)       # BB L551-552
    roster = ctx['bmod']._DifferenceRoster(body_r, ra_roster, synthetic or ctx['i1t']['verdict'] != 'PASS')   # BB L559
    radii = np.unique(np.asarray(body['radial_nodes_m'], float))                                      # BB L560
    ctx['prov']['inputs'].update(
        profile=dict(ppro, use='s_edges only (BB L546-547)'),
        route_a_manifest={'basis': FORMAL, 'cite': 'argv --route-a-tail-manifest (driver L8715-8716); BB _manifest L379-405, _manifest_gas_roster L407-427', 'pin': {'path': mpath, 'sha256': msha}, 'state_digest': ra_state.digest},
        body_arrays={'basis': DECLARED, 'cite': 'BB bind_offset body (successor); body_arrays.npz of --body-directory (driver L8778, L3307)', 'pin': bpin, 'body_finish': body_pin},
        roster={'basis': FORMAL, 'cite': 'BB L549-552, L559 _DifferenceRoster(body_r, ra_roster)'},
        eval_radii_m={'basis': FORMAL, 'cite': 'BB L560 unique(body radial_nodes_m) (body file DECLARED)'})
    return _done(ctx, roster, radii)


def _done(ctx, roster, radii):
    build = {'config': ctx['cfg'], 'kept': ctx['kept'], 'gamma_eff': ctx['gamma'], 'c_m_s': ctx['c'], 'eval_radii_m': radii,
             'i1t': ctx['i1t'], 'stage_kind': ctx['bkind']}
    return {'roster': roster, 'build': build, 'provenance': ctx['prov']}


def RECIPE_ROUTE_B_fs_columns(**kw):
    return _route_b_fs('fs_columns', **dict({'toolkit': None}, **kw))


def RECIPE_ROUTE_B_fs_rotation(**kw):
    return _route_b_fs('fs_rotation', **dict({'toolkit': None}, **kw))


def RECIPE_ROUTE_B_rfs_columns(**kw):
    return _route_b_rotation('rfs_columns', **dict({'toolkit': None}, **kw))


def RECIPE_ROUTE_B_le_columns(**kw):
    return _route_b_rotation('le_columns', **dict({'toolkit': None}, **kw))


def RECIPE_ROUTE_B_le_rotation(**kw):
    return _route_b_rotation('le_rotation', **dict({'toolkit': None}, **kw))


ROUTE_B_RECIPES = {'offset': RECIPE_ROUTE_B_offset, 'fs_columns': RECIPE_ROUTE_B_fs_columns,
                   'fs_rotation': RECIPE_ROUTE_B_fs_rotation, 'rfs_columns': RECIPE_ROUTE_B_rfs_columns,
                   'le_columns': RECIPE_ROUTE_B_le_columns, 'le_rotation': RECIPE_ROUTE_B_le_rotation}


# ------------------------------------------------------------------------------------------------ S5 entry
def recipe_for_state(*, call_dir, out_dir, result, target, lib, provider, toolkit):
    """Dispatch one S5 target to its recipe with an explicit toolkit."""
    need(isinstance(result, dict) and result.get('driver_sha256') == toolkit.driver_sha256 and result.get('galaxy') == GALAXY,
         C_CALL, 'call driver %r / galaxy %r is not the toolkit call' % (result.get('driver_sha256'), result.get('galaxy')))
    need(isinstance(target, dict) and isinstance(target.get('origin'), dict) and isinstance(target.get('state'), dict)
         and _is_sha(target['state'].get('state_sha256')), C_TARGET, 'target shape')
    out = os.path.realpath(str(out_dir))
    need(out == os.path.realpath(os.path.join(os.path.realpath(str(call_dir)), 'out')), C_TARGET, 'out_dir is not <call>/out')
    og = target['origin']
    kw = dict(call_dir=call_dir, out_dir=out, result=result, target=target, lib=lib, provider=provider, toolkit=toolkit)
    if og.get('kind') == 'ROUTE_A_ITERATE':
        return RECIPE_ROUTE_A(**kw)
    if og.get('kind') == 'ROUTE_B_STAGE':
        rec = _executed_record(result, name=og.get('stage'), code=C_BSTAGE)
        bkind = UVT_BINDING_KIND.get(rec.get('kind'))
        need(bkind is not None, C_BSTAGE, 'stage kind %r' % rec.get('kind'))
        need(bkind in ROUTE_B_RECIPES, C_INHERIT, '%s reuses the accepted manifest state (BB L457-470)' % bkind)
        return ROUTE_B_RECIPES[bkind](**kw)
    raise RecipeRefusal(C_TARGET, 'origin kind %r' % og.get('kind'))


def roster_for_state(*, call_dir, out_dir, result, target, lib, provider):
    """The S5 entry (ngc_s5_rebuild_export_c2v003 L277-278): the production toolkit, i.e. the driver's pinned modules."""
    return recipe_for_state(call_dir=call_dir, out_dir=out_dir, result=result, target=target, lib=lib, provider=provider,
                            toolkit=TOOLKIT())
