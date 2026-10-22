"""Q2 acceptance input side, part 1 (A134; S4RC1 rulings 56774ba7 Q2): replay-plan / descriptor / I1-T packet writer.

Root runs this after a tail-ON call's FINISHED receipt, before any value of the call is used.
- It is outside every pin. consumed_states_cx2v010 (e48cca3c) re-verifies everything written here from bytes
  (plan coverage L76-94, lineage L96-115, descriptors L184-198, own-call archive location L181-182), and
  reconstruction_cx2v003 / current_source_evidence_cx2v004 rebuild every state and recompute every I1-T.
  A defect here can only make the inventory UNAVAILABLE.
- It computes no physics number. It maps each real discovered occurrence (v005 discovery order) to the call's
  own saved records, following the r5 code that wrote them (citations at each resolver).
- Writes are exclusive-create: <call_dir>/ACCEPTANCE_INPUTS_C2V002_A<nnn>/ (the first free attempt number) and
  <call_dir>/TAIL_REPLAY_PLAN.json. If any occurrence cannot be resolved, it writes WRITER_REPORT.json with typed gaps
  and NO plan (fail closed); a later attempt writes a fresh input set in the next attempt directory.
- v002 (A115(a); the acceptance pass is repeatable): once <call_dir>/TAIL_REPLAY_PLAN.json exists, the writer writes
  nothing. It reuses that plan and its input set only after checking them from bytes (reuse_existing below): the plan
  is bound to this call's own result and spec bytes, covers exactly the real occurrences, and was recorded by a
  WRITTEN writer report in the same input directory whose every file still matches its sha; the derived G1/G2 inputs
  that report recorded pass the same checks again. Otherwise it reads UNAVAILABLE.

Two inputs are not archived by the pinned r5 code as own-call files (FORMAL, from code):
- G1 ROUTE_A_INITIAL_RINGS: the razor-thin initial rings (R, z, m) are built in memory from the prep result
  (controller L220-285 from_prepared; prep v007 L202-211); only their digest is archived
  (SIDECAR_IDENTITY.json identity.init_rings_digest, controller L208-215). Every route-A source selector needs them
  (reconstruction L207-224; evidence L51-55, L64-65), so every call needs them (boundary, inherited, offset, iterates).
- G2 ROUTE_A_FINAL_NEXT_GAS: the gas packet of the state built after the converged iteration,
  g_N = (1-r) gas_{N-1} + r updated_{N-1} (controller L483), exists only in memory; the solver returns first.
Root may supply both as byte refs (initial_rings_ref: npz R,z,m; final_next_gas_ref: npy [n,10,1]). The writer
checks them against own-call bytes (G1: the archived digest; G2: bitwise re-derivation from the checkpoint blobs).
Where they live is not the writer's decision: v010 L181-182 refuses any I1-T source file outside <call_dir>/out.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
PLAN_SCHEMA = 'DDO154_TAIL_REPLAY_PLAN_CX2V001'            # v010 L77-80
DESCRIPTOR_SCHEMA = 'DDO154_STATE_REPLAY_DESCRIPTOR_CX2V001'  # reconstruction L361
PACKET_SCHEMA = 'DDO154_I1T_REPLAY_CX2V001'                # evidence L132
CONTEXT_SCHEMA = 'DDO154_SAVED_SOURCE_CONTEXT_CX2V001'     # reconstruction L102
RECIPE_SCHEMA = 'DDO154_STATE_REPLAY_RECIPE_C2V001'        # extra key; reconstruction L315-332 reads the others
REPORT_SCHEMA = 'DDO154_REPLAY_INPUTS_WRITER_REPORT_C2V001'
INPUTS_DIR = 'ACCEPTANCE_INPUTS_C2V002_A%03d'              # one directory per writing attempt (v002)
INPUTS_PREFIX = 'ACCEPTANCE_INPUTS_'                        # input sets written by v001 or v002
MAX_ATTEMPTS = 999
PLAN_NAME = 'TAIL_REPLAY_PLAN.json'                         # v010 L146
# Registered DDO154 profile (driver L435; certs_common_r5 PINS['profile']); the per-call geometry profile replaces it
# when the driver wrote one (driver L1626-1649, result['geometry']['files']['profile']).
REGISTERED_PROFILE = {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                              'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json',
                      'sha256': 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'}
GAUSS_FIELD = ['seed', 'numerical_inputs', 'source_gauss_order']   # route-A worker start.json (worker L117-119)
ROLES = ('current_begin_inferred_from_completion', 'next_built_and_monitor_consumed', 'boundary_at_return',
         'inherited_route_a', 'signed_body_minus_route_a', 'own_source_state')     # v010 L28-35
COMPONENT_ROLES = ('body_gas_component', 'route_a_gas_component')                  # v010 L36
FS_KINDS = ('fs_columns', 'fs_rotation')                       # binding L440: stars + offset updated base
ROTATION_SOURCE_KINDS = ('rfs_columns', 'le_columns', 'le_rotation')   # binding L466-488: stars + rotation rings
COLUMN_KINDS = ('fs_columns', 'rfs_columns', 'le_columns')     # radii = base radial nodes at controls indices
ROTATION_STAGE_KINDS = ('fs_rotation', 'le_rotation')          # radii = own joined radial nodes (rotation stages)


class Gap(Exception):
    def __init__(self, code, where=''):
        self.code, self.where = code, str(where)
        super().__init__(code + ((': ' + self.where) if self.where else ''))


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def file_ref(path):
    p = Path(path).resolve(strict=True)
    return {'path': str(p), 'sha256': sha_bytes(p.read_bytes())}


def read_json(path, sha256=None, where=''):
    try:
        p = Path(path).resolve(strict=True)
        raw = p.read_bytes()
    except OSError as exc:
        raise Gap('OWN_CALL_RECORD_MISSING', '%s %s (%s)' % (where, path, type(exc).__name__))
    got = sha_bytes(raw)
    if sha256 is not None and got != sha256:
        raise Gap('OWN_CALL_RECORD_PIN_MISMATCH', '%s %s' % (where, path))
    return {'path': str(p), 'sha256': got}, json.loads(raw)


def argv_value(argv, flag, where):
    if not isinstance(argv, list) or argv.count(flag) != 1 or argv.index(flag) + 1 >= len(argv):
        raise Gap('STAGE_ARGUMENT_MISSING_OR_AMBIGUOUS', '%s %s' % (where, flag))
    return str(argv[argv.index(flag) + 1])


def array_digest(a):
    """Controller L78-81 (_array_digest)."""
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def real_occurrences(discovery):
    """Plan coverage set: v010 split_occurrences L54-74 keeps real role occurrences in discovery order and drops the
    signed-component placeholders. v010 re-derives and checks this itself (L87-88)."""
    real = []
    for o in discovery['occurrences']:
        if o.get('role') in COMPONENT_ROLES:
            continue
        if o.get('role') not in ROLES:
            raise Gap('UNSUPPORTED_OCCURRENCE_ROLE', o.get('role'))
        real.append(o)
    return real


class CallRecords:
    """The call's own records, read once (paths and shas from the call's own bytes)."""

    def __init__(self, call_dir, spec, result):
        self.call = Path(call_dir).resolve(strict=True)
        self.out = self.call / 'out'
        self.result_ref, raw_result = read_json(self.out / 'result.json', where='result')
        if canonical(raw_result) != canonical(result):
            raise Gap('SUPPLIED_RESULT_DIFFERS_FROM_BYTES')
        self.spec_ref, raw_spec = read_json(self.out / 'inputs' / 'call_spec.json', result.get('call_spec_sha256'), 'call_spec')
        if canonical(raw_spec) != canonical(spec):
            raise Gap('SUPPLIED_SPEC_DIFFERS_FROM_BYTES')
        if result.get('driver_sha256') != DRIVER_SHA:
            raise Gap('DRIVER_NOT_R5')
        self.result = result
        self.stages = {s['name']: s for s in result['stage_records']}
        uv = result['uv_tail']
        self.accepted_ref = {'path': uv['manifest']['path'], 'sha256': uv['manifest']['sha256']}
        _, self.manifest = read_json(self.accepted_ref['path'], self.accepted_ref['sha256'], 'accepted manifest')
        self.state_record = self.manifest['state']['record']
        self.accepted_digest = self.manifest['state']['digest']
        self.config_ref = {'path': uv['config']['path'], 'sha256': uv['config']['sha256']}
        outcome = result['route_a_outcome']
        self.attempt_ref, attempt = read_json(outcome['result_path'], outcome['result_sha256'], 'route-A attempt result')
        auv = attempt['result']['uv_tail']
        self.sidecar_dir = Path(auv['sidecar']['directory'])
        self.sidecar_files = auv['sidecar']['files']
        self.accepted_iteration = auv['accepted_iteration']
        if type(self.accepted_iteration) is not int or self.accepted_iteration < 0:
            raise Gap('ROUTE_A_ACCEPTED_ITERATION_MISSING')
        self.flags = list(auv.get('flags') or [])
        self.attempt_start_ref, self.attempt_start = read_json(Path(self.attempt_ref['path']).parent / 'start.json',
                                                               where='route-A attempt start')
        _, ident = read_json(self.sidecar_dir / 'SIDECAR_IDENTITY.json', self.sidecar_files.get('SIDECAR_IDENTITY.json'),
                             'sidecar identity')
        self.relaxation = ident['identity']['relaxation']
        self.init_rings_digest = ident['identity']['init_rings_digest']
        ra = self.stages['route_a']
        self.checkpoint = Path(argv_value(ra['argv'], '--checkpoint-directory', 'route_a'))
        self.payloads = {}
        self.starts = {}

    # ---------------------------------------------------------------- route A (sidecar L505-520; checkpoint L535-578)
    def payload(self, i):
        if i not in self.payloads:
            name = 'iteration_%04d.json' % i
            if name not in self.sidecar_files:
                raise Gap('ROUTE_A_SIDECAR_ITERATION_MISSING', name)
            _, doc = read_json(self.sidecar_dir / name, self.sidecar_files[name], 'sidecar ' + name)
            self.payloads[i] = doc['payload']
        return self.payloads[i]

    def element_ref(self, m):
        name = 'elements_%04d.npz' % m
        if name not in self.sidecar_files:
            raise Gap('ROUTE_A_ELEMENT_ARCHIVE_MISSING', name)
        return {'path': str((self.sidecar_dir / name).resolve(strict=True)), 'sha256': self.sidecar_files[name]}

    def start(self, n):
        if n not in self.starts:
            p = self.checkpoint / ('iteration_%04d' % n) / 'START.json'
            if not p.is_file():
                raise Gap('ROUTE_A_CHECKPOINT_START_MISSING', n)
            self.starts[n] = read_json(p, where='checkpoint START %d' % n)[1]
        return self.starts[n]

    def blob_ref(self, entry, where):
        """checkpoint L223-234: blobs/<file_sha256>.npy, a plain NPY array (selector key null, evidence L69-75)."""
        if not isinstance(entry, dict) or entry.get('blob') != 'blobs/%s.npy' % entry.get('file_sha256'):
            raise Gap('CHECKPOINT_BLOB_REFERENCE_INVALID', where)
        return {'path': str((self.checkpoint / entry['blob']).resolve(strict=True)), 'sha256': entry['file_sha256']}

    def completed_iterations(self):
        return self.accepted_iteration + 1     # iterations 0..N-1, N-1 converged and accepted (controller L527-531)

    # ---------------------------------------------------------------- route B (driver L1171-1180; stage scripts)
    def stage(self, name):
        if name not in self.stages:
            raise Gap('STAGE_RECORD_MISSING', name)
        s = self.stages[name]
        outdir = Path(argv_value(s['argv'], '--outdir', name))
        fin_ref, fin = read_json(outdir / 'finish.json', where=name + ' finish')
        return s, outdir, fin_ref, fin

    def finish_of_dir(self, d, where):
        return read_json(Path(d) / 'finish.json', where=where)


def write_x(path, raw):
    with open(path, 'xb') as f:
        f.write(raw)
    return file_ref(path)


class Writer:
    def __init__(self, recs, inputs_dir):
        self.r = recs
        self.dir = inputs_dir
        self.files = []
        self.cache = {}

    def json(self, name, obj):
        ref = write_x(self.dir / name, canonical(obj) + b'\n')
        self.files.append(ref)
        return ref

    def radii(self, name, values):
        p = self.dir / name
        with open(p, 'xb') as f:
            np.savez(f, eval_radii_m=np.asarray(values, dtype=float))
        ref = file_ref(p)
        self.files.append(ref)
        return ref

    # ------------------------------------------------------------ context (reconstruction L96-133)
    def context(self):
        if 'context' not in self.cache:
            r = self.r
            geo = (r.result.get('geometry') or {}).get('files') or {}
            prof = geo.get('profile')
            profile = {'path': str(prof[0]), 'sha256': prof[1]} if prof else dict(REGISTERED_PROFILE)
            ni = r.attempt_start['seed']['numerical_inputs']
            self.cache['context'] = self.json('CONTEXT.json', {
                'schema': CONTEXT_SCHEMA, 'galaxy': 'DDO154', 'driver_sha256': DRIVER_SHA, 'profile': profile,
                'kpc_m': ni['kpc_m'], 'solar_mass_kg': ni['solar_mass_kg'], 'c_m_s': r.state_record['c_m_s'],
                'config': r.config_ref, 'replay_scope': 'PRODUCTION_P128_MS128'})
        return self.cache['context']

    # ------------------------------------------------------------ route A pieces
    def route_a_source(self, n, rings_ref):
        if rings_ref is None:
            raise Gap('ROUTE_A_INITIAL_RINGS_NOT_ARCHIVED_IN_OWN_CALL',
                      'G1: controller L220-285 keeps the initial rings in memory; only identity.init_rings_digest is archived')
        return {'kind': 'route_a', 'initial_rings': rings_ref, 'elements': [self.r.element_ref(m) for m in range(n)],
                'relaxation': self.r.relaxation, 'iteration': n}

    def route_a_radii(self):
        if 'ra_radii' not in self.cache:
            arr = self.r.manifest['state']['arrays']
            with np.load(Path(arr['path']).resolve(strict=True), allow_pickle=False) as f:
                radii = np.array(f['ring_radii_m'], copy=True)       # lib L728: ring_radii_m = unique(eval radii)
            self.cache['ra_radii'] = self.radii('EVAL_RADII_ROUTE_A.npz', radii)
        return self.cache['ra_radii']

    def stars(self, n):
        st = self.r.start(n)
        return {'packet': {'ref': self.r.blob_ref(st['fixed_source_fourier_J'], 'fixed START %d' % n), 'key': None},
                'gauss_order': {'ref': self.r.attempt_start_ref, 'field_path': list(GAUSS_FIELD)}}

    def route_a_gas(self, n, final_ref):
        N = self.r.completed_iterations()
        if n < N:
            return {'ref': self.r.blob_ref(self.r.start(n)['gas_fourier_J'], 'gas START %d' % n), 'key': None}
        if n == N:
            if final_ref is None:
                raise Gap('ROUTE_A_FINAL_NEXT_GAS_PACKET_NOT_ARCHIVED',
                          'G2: g_N = (1-r) gas_{N-1} + r updated_{N-1} (controller L483) is never written')
            return {'ref': final_ref, 'key': None}
        raise Gap('ROUTE_A_ITERATION_BEYOND_HISTORY', n)

    def route_a_packet(self, n, desc_ref, rings_ref, final_ref):
        base = min(n, self.r.completed_iterations() - 1)
        return {'schema': PACKET_SCHEMA, 'reconstruction': desc_ref, 'source': self.route_a_source(n, rings_ref),
                'waves': {'ref': self.r.blob_ref(self.r.start(base)['prepared_wavevectors'], 'waves START %d' % base), 'key': None},
                'gas_packet': self.route_a_gas(n, final_ref), 'stars': self.stars(base)}

    # ------------------------------------------------------------ one occurrence
    def occurrence(self, o, rings_ref, final_ref):
        r, k = self.r, o['ordinal']
        role = o['role']
        acc = r.accepted_iteration
        if role in ('current_begin_inferred_from_completion', 'next_built_and_monitor_consumed'):
            n = o['iteration']
            nxt = role == 'next_built_and_monitor_consumed'
            pay = r.payload(n - 1 if nxt else n)
            recipe = self.json('RECIPE_%04d.json' % k, {
                'schema': RECIPE_SCHEMA, 'config_sha256': r.state_record['config_sha256'], 'stage_kind': 'route_a',
                'kept': r.state_record['kept'], 'gamma_eff': r.state_record['gamma_eff'],
                'i1t': pay['next_i1t' if nxt else 'i1t'], 'eval_radii': self.route_a_radii()})
            desc = {'schema': DESCRIPTOR_SCHEMA, 'context': self.context(), 'operation': 'rebuild',
                    'source': self.route_a_source(n, rings_ref), 'recipe': recipe, 'state_assertion': o['evidence'],
                    'state_field_path': ['payload', 'next_state_digest' if nxt else 'state_digest']}
            dref = self.json('DESCRIPTOR_%04d.json' % k, desc)
            return dref, self.json('PACKET_%04d.json' % k, self.route_a_packet(n, dref, rings_ref, final_ref))
        if role in ('boundary_at_return', 'inherited_route_a'):
            dref = self.json('DESCRIPTOR_%04d.json' % k, {'schema': DESCRIPTOR_SCHEMA, 'context': self.context(),
                                                          'operation': 'accepted_manifest', 'manifest': r.accepted_ref})
            return dref, self.json('PACKET_%04d.json' % k, self.route_a_packet(acc, dref, rings_ref, final_ref))
        # route-B stage states: finish uv_tail record = binding _base_record L317-329
        s, outdir, fin_ref, fin = r.stage(o['stage'])
        u = fin.get('uv_tail') or {}
        kind = u.get('stage_kind')
        if fin_ref['sha256'] != o['evidence']['sha256']:
            raise Gap('STAGE_FINISH_DIFFERS_FROM_DISCOVERY', o['stage'])
        if role == 'signed_body_minus_route_a':
            if kind != 'offset':
                raise Gap('SIGNED_OCCURRENCE_NOT_OFFSET', o['stage'])
            # offset stage L213-227, L255-267: body arrays from the body finish; packets in its own outputs
            _, bfin = r.finish_of_dir(argv_value(s['argv'], '--body-directory', o['stage']), 'body finish')
            body = {'path': str(Path(bfin['array_file']).resolve(strict=True)), 'sha256': bfin['array_sha256']}
            with np.load(body['path'], allow_pickle=False) as f:
                radii = np.unique(np.asarray(f['radial_nodes_m'], float))     # binding L522
            source = {'kind': 'offset', 'body': body, 'manifest': r.accepted_ref}
            outs = fin['outputs']
            packet_extra = {'waves': {'ref': outs['unit_response.npz'], 'key': 'wavevectors'},
                            'gas_packet': {'ref': outs['source_offset.npz'], 'key': 'new_body_fourier_J'},
                            'route_a_packet': self.route_a_gas(acc, final_ref)}
        elif kind in FS_KINDS or kind in ROTATION_SOURCE_KINDS:
            _, ofin = r.finish_of_dir(argv_value(s['argv'], '--offset-directory', o['stage']), 'offset finish')
            outs = ofin['outputs']
            if kind in COLUMN_KINDS:
                _, controls = read_json(argv_value(s['argv'], '--controls', o['stage']),
                                        argv_value(s['argv'], '--controls-sha256', o['stage']), 'controls')
                with np.load(Path(outs['updated_base_arrays.npz']['path']).resolve(strict=True), allow_pickle=False) as f:
                    nodes = np.asarray(f['radial_nodes_m'])
                radii = [float(nodes[i]) for i in controls['radial_indices']]     # stage scripts: radii=[base nodes[i] for i in ids]
            else:
                ref = {'path': fin['arrays_path'], 'sha256': fin['arrays_sha256']}
                with np.load(Path(ref['path']).resolve(strict=True), allow_pickle=False) as f:
                    radii = np.asarray(f['radial_nodes_m'], float)            # rotation stages: radii=R (joined nodes)
            if kind in FS_KINDS:
                source = {'kind': 'fs', 'arrays': outs['updated_base_arrays.npz']}          # binding L440-452
                packet_extra = {'waves': {'ref': outs['offset_prepared.npz'], 'key': 'wavevectors'},
                                'gas_packet': {'ref': outs['source_offset.npz'], 'key': 'new_body_fourier_J'}}
            else:
                rdir = argv_value(s['argv'], '--uv-tail-source-rotation-directory', o['stage'])
                _, rfin = r.finish_of_dir(rdir, 'source rotation finish')                     # binding L466-474
                source = {'kind': 'rotation', 'arrays': {'path': str(Path(rfin['arrays_path']).resolve(strict=True)),
                                                         'sha256': rfin['arrays_sha256']}}
                _, ffin = r.finish_of_dir(argv_value(s['argv'], '--feedback-directory', o['stage']), 'feedback finish')
                fo = ffin['outputs']                                                           # binding L480-485
                packet_extra = {'waves': {'ref': fo['refreshed_prepared.npz'], 'key': 'wavevectors'},
                                'gas_packet': {'ref': fo['gas_source_feedback.npz'], 'key': 'new_gas_fourier_J'}}
            packet_extra['stars'] = self.stars(acc)
        else:
            raise Gap('UNSUPPORTED_STAGE_KIND', '%s %s' % (o['stage'], kind))
        recipe = self.json('RECIPE_%04d.json' % k, {
            'schema': RECIPE_SCHEMA, 'config_sha256': u['config_sha256'], 'stage_kind': kind, 'kept': u['kept'],
            'gamma_eff': r.state_record['gamma_eff'], 'i1t': u['i1t'],
            'eval_radii': self.radii('EVAL_RADII_%04d.npz' % k, radii)})
        dref = self.json('DESCRIPTOR_%04d.json' % k, {
            'schema': DESCRIPTOR_SCHEMA, 'context': self.context(), 'operation': 'rebuild', 'source': source,
            'recipe': recipe, 'state_assertion': o['evidence'], 'state_field_path': ['uv_tail', 'state_digest']})
        packet = {'schema': PACKET_SCHEMA, 'reconstruction': dref, 'source': source}
        if kind == 'offset':
            packet['route_a_source'] = self.route_a_source(acc, rings_ref)
        packet.update(packet_extra)
        return dref, self.json('PACKET_%04d.json' % k, packet)


def check_initial_rings(recs, ref):
    """G1 check: the supplied rings must reproduce the own-call archived digest (controller L208-215)."""
    if ref is None:
        return
    p = Path(ref['path']).resolve(strict=True)
    if sha_bytes(p.read_bytes()) != ref['sha256']:
        raise Gap('INITIAL_RINGS_PIN_MISMATCH')
    with np.load(p, allow_pickle=False) as f:
        if set(f.files) != {'R', 'z', 'm'}:
            raise Gap('INITIAL_RINGS_FIELDS')
        stack = np.stack([np.asarray(f[k], dtype=float) for k in ('R', 'z', 'm')])
    if array_digest(stack) != recs.init_rings_digest:
        raise Gap('INITIAL_RINGS_DIGEST_MISMATCH')


def derive_final_next_gas(recs):
    """G2 re-derivation from own-call checkpoint blobs: (1-r) START_{N-1}.gas + r COMPLETED_{N-1}.updated
    (controller L483, the solver L215 expression). Returns the array; the writer never decides where it is stored."""
    n = recs.completed_iterations() - 1
    st = recs.start(n)
    done_path = recs.checkpoint / ('iteration_%04d' % n) / 'COMPLETED.json'
    _, done = read_json(done_path, where='checkpoint COMPLETED %d' % n)
    gas = np.load(recs.blob_ref(st['gas_fourier_J'], 'gas')['path'], allow_pickle=False)
    upd = np.load(recs.blob_ref(done['updated_gas_fourier_J'], 'updated')['path'], allow_pickle=False)
    r = recs.relaxation
    return (1 - r) * gas + r * upd


def check_final_next_gas(recs, ref):
    if ref is None:
        return
    p = Path(ref['path']).resolve(strict=True)
    if sha_bytes(p.read_bytes()) != ref['sha256']:
        raise Gap('FINAL_NEXT_GAS_PIN_MISMATCH')
    got = np.load(p, allow_pickle=False)
    want = derive_final_next_gas(recs)
    if got.dtype != want.dtype or got.shape != want.shape or not np.array_equal(got, want):
        raise Gap('FINAL_NEXT_GAS_MISMATCH')


def new_inputs_dir(call):
    """The first free attempt directory, created exclusively (never reused, never overwritten)."""
    for n in range(1, MAX_ATTEMPTS + 1):
        try:
            (call / (INPUTS_DIR % n)).mkdir(exist_ok=False)
            return call / (INPUTS_DIR % n)
        except FileExistsError:
            continue
    raise Gap('INPUT_ATTEMPTS_EXHAUSTED')


def reuse_existing(call, spec, result, discovery, initial_rings_ref, final_next_gas_ref):
    """The plan already exists (v010 reads it at one fixed path, and nothing is ever deleted): check it and its input
    set from bytes and return its refs. Writes nothing."""
    plan_ref, plan = read_json(call / PLAN_NAME, where='existing plan')
    if canonical(plan) + b'\n' != Path(plan_ref['path']).read_bytes() or not isinstance(plan, dict) \
            or set(plan) != {'schema', 'driver_sha256', 'call_result', 'call_spec', 'replays'} \
            or plan['schema'] != PLAN_SCHEMA or plan['driver_sha256'] != DRIVER_SHA:
        raise Gap('EXISTING_PLAN_FORM')
    recs = CallRecords(call, spec, result)
    if plan['call_result'] != recs.result_ref or plan['call_spec'] != recs.spec_ref:
        raise Gap('EXISTING_PLAN_NOT_THIS_CALL_BYTES')
    entries = plan['replays']
    if not isinstance(entries, list) or [e.get('ordinal') for e in entries] != [o['ordinal'] for o in real_occurrences(discovery)]:
        raise Gap('EXISTING_PLAN_OCCURRENCE_COVERAGE')
    dirs = {Path(e[k]['path']).parent for e in entries for k in ('reconstruction', 'packet')}
    if len(dirs) != 1:
        raise Gap('EXISTING_PLAN_INPUT_SET_NOT_ONE_DIRECTORY')
    inputs = dirs.pop()
    if inputs.parent != call or not inputs.name.startswith(INPUTS_PREFIX):
        raise Gap('EXISTING_PLAN_INPUT_SET_LOCATION')
    report_ref, report = read_json(inputs / 'WRITER_REPORT.json', where='existing writer report')
    if report.get('schema') != REPORT_SCHEMA or report.get('status') != 'WRITTEN' or report.get('plan') != plan_ref \
            or report.get('gaps') != [] or report.get('entries') != len(entries):
        raise Gap('EXISTING_PLAN_NOT_RECORDED_BY_A_WRITTEN_REPORT')
    files = report.get('files')
    if not isinstance(files, list) or not files:
        raise Gap('EXISTING_INPUT_SET_EMPTY')
    for f in files:
        if not isinstance(f, dict) or set(f) != {'path', 'sha256'} or Path(f['path']).parent != inputs:
            raise Gap('EXISTING_INPUT_SET_FILE_OUTSIDE_SET')
        if sha_bytes(Path(f['path']).read_bytes()) != f['sha256']:
            raise Gap('EXISTING_INPUT_FILE_CHANGED', f['path'])
    if any(e[k] not in files for e in entries for k in ('reconstruction', 'packet')):
        raise Gap('EXISTING_PLAN_REFERS_OUTSIDE_RECORDED_SET')
    for supplied, key in ((initial_rings_ref, 'initial_rings'), (final_next_gas_ref, 'final_next_gas')):
        if supplied is not None and supplied != report.get(key):
            raise Gap('EXISTING_PLAN_DERIVED_INPUTS_DIFFER', key)
    check_initial_rings(recs, report.get('initial_rings'))
    check_final_next_gas(recs, report.get('final_next_gas'))
    return {'status': 'REUSED', 'plan': plan_ref, 'report': report_ref, 'gaps': [], 'input_set': str(inputs)}


def write_replay_inputs(*, call_dir, spec, result, discovery, initial_rings_ref=None, final_next_gas_ref=None):
    """Return {status, plan, report, gaps}. status WRITTEN only when every real occurrence resolved; REUSED when an
    existing plan and input set passed reuse_existing; UNAVAILABLE otherwise."""
    call = Path(call_dir).resolve(strict=True)
    if (call / PLAN_NAME).exists():
        try:
            return reuse_existing(call, spec, result, discovery, initial_rings_ref, final_next_gas_ref)
        except Gap as g:
            return {'status': 'UNAVAILABLE', 'plan': None, 'report': None,
                    'gaps': [{'ordinal': None, 'code': g.code, 'detail': g.where}]}
        except (KeyError, TypeError, ValueError, OSError) as exc:
            return {'status': 'UNAVAILABLE', 'plan': None, 'report': None,
                    'gaps': [{'ordinal': None, 'code': 'EXISTING_PLAN_UNREADABLE', 'detail': '%s: %s' % (type(exc).__name__, exc)}]}
    inputs = new_inputs_dir(call)                 # one immutable input set per writing attempt
    gaps, entries, wr = [], [], None
    try:
        recs = CallRecords(call, spec, result)
        check_initial_rings(recs, initial_rings_ref)
        check_final_next_gas(recs, final_next_gas_ref)
        wr = Writer(recs, inputs)
        for o in real_occurrences(discovery):
            try:
                dref, pref = wr.occurrence(o, initial_rings_ref, final_next_gas_ref)
                entries.append({'ordinal': o['ordinal'], 'reconstruction': dref, 'packet': pref})
            except Gap as g:
                gaps.append({'ordinal': o['ordinal'], 'role': o['role'], 'stage': o['stage'], 'code': g.code, 'detail': g.where})
            except (KeyError, TypeError, ValueError, OSError) as exc:
                gaps.append({'ordinal': o['ordinal'], 'role': o['role'], 'stage': o['stage'],
                             'code': 'OCCURRENCE_RECORD_UNREADABLE', 'detail': '%s: %s' % (type(exc).__name__, exc)})
    except Gap as g:
        gaps.append({'ordinal': None, 'code': g.code, 'detail': g.where})
    except (KeyError, TypeError, ValueError, OSError) as exc:
        gaps.append({'ordinal': None, 'code': 'CALL_RECORD_UNREADABLE', 'detail': '%s: %s' % (type(exc).__name__, exc)})
    plan_ref = None
    if not gaps:
        plan = {'schema': PLAN_SCHEMA, 'driver_sha256': DRIVER_SHA, 'call_result': recs.result_ref,
                'call_spec': recs.spec_ref, 'replays': entries}
        plan_ref = write_x(call / PLAN_NAME, canonical(plan) + b'\n')
    report = {'schema': REPORT_SCHEMA, 'status': 'WRITTEN' if plan_ref else 'UNAVAILABLE', 'plan': plan_ref,
              'gaps': gaps, 'entries': len(entries), 'files': [] if wr is None else wr.files,
              'initial_rings': initial_rings_ref, 'final_next_gas': final_next_gas_ref,
              'writer': file_ref(__file__),
              'scope': 'Input mapping only. v010 re-verifies from bytes; no physics number computed here.'}
    rep = write_x(inputs / 'WRITER_REPORT.json', canonical(report) + b'\n')
    return {'status': report['status'], 'plan': plan_ref, 'report': rep, 'gaps': gaps}
