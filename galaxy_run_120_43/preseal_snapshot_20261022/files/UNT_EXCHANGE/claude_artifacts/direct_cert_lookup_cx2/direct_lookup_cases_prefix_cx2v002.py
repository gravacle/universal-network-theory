"""Independent equality/refusal layer over new inert fixtures, all in process."""
from pathlib import Path
_prefix = Path(__file__).with_name('direct_lookup_fixture_cx2v002.py')
exec(compile(_prefix.read_bytes(), str(_prefix), 'exec'), globals())

L = load(HERE/'direct_cert_lookup_cx2v002.py', 'lookup_candidate')
# Test-only anchors: exactly the earlier synthetic C1/genesis fixtures. The CLI
# exposes no anchor override; frozen production constants are separately checked.
production_c1, production_genesis = L.C1, L.GENESIS
L.C1, L.GENESIS = c1six, gen
verify_ref = write('FULL_VERIFY.json', rep)
approved_ref = write('APPROVED.json', {'approved_certificate_producers': six})
request = {'schema': L.REQUEST_SCHEMA, 'records': records, 'verification': verify_ref,
           'c1': c1six, 'genesis_registry': gen, 'approved_producers': approved_ref}
request_ref = write('REQUEST.json', request)

class SyntheticSnapshot(L.Snapshot):
    def module(self, ref, name):
        obj = super().module(ref, name)
        if ref == L.ASSEMBLER:
            obj.A.real_custody_fn = lambda pin: lambda spec: custody
        return obj

s = SyntheticSnapshot()
ready = L.validate(s, request_ref)
check('lookup_validates_all_three_points', len(ready['points']) == 3)
replayed = L.replay(s, ready)
check('full_verifier_replay_matches_except_utc', replayed['ok'] is True)
check('single_physical_read_through_legacy_verifier',
      bool(s.counts) and set(s.counts.values()) == {1}, {'n_physical_files': len(s.counts)})
need_path = HERE/'direct_cert_lookup_cx2v002.py'
check('frozen_C1_constant_correct', production_c1['sha256'] ==
      '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1')
check('frozen_genesis_constant_correct', production_genesis['sha256'] ==
      '2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319')

# Execute the actual parent, core and ledger Mapper classes extracted from their
# byte-pinned sources. The entire class bodies are preserved. The synthetic ctx
# supplies base/es and an in-memory record lookup; no production Context runs.
import math
def source(path, expected):
    raw = Path(path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected
    return ast.parse(raw)
def selected(tree, names):
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    return ast.Module(body=nodes, type_ignores=[])
parent = source(ART/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
                'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d')
ns = {'copy': copy, 'math': math, 'json': json, 'hashlib': hashlib, 'OrchestratorError': ValueError,
      'SCHEMA_THETA_KEY': 'DDO154_CALIBRATION_THETA_KEY_C2V001',
      'FIXED_TEMPLATE_CHECKS': (('Eref_J', 'Eref_base_J'), ('entropy_K_factor', 'entropy_K_factor')),
      'DECLARED_CHANGED_PATHS': ('label', 'physical.common_scale_s', 'physical.gamma',
                                'physical.ell_F_m', 'physical.distance_Mpc',
                                'numerics.uv_tail.eps_certificate', 'numerics.uv_tail.lo_certificate')}
exec(compile(selected(parent, ['canonical', 'sha256_bytes', 'json_bytes', 'theta_key', 'diff_paths', 'Mapper']),
             'pinned parent mapper', 'exec'), ns)
o = types.SimpleNamespace(**{k: ns[k] for k in ('Mapper', 'canonical', 'sha256_bytes', 'json_bytes', 'diff_paths')})
o.read_pinned = lambda ref, label: s.read(ref)
core = source(ART/'calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py',
              'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')
cs = {'O': o, 'copy': copy, 'json': json, 'hashlib': hashlib, 'DRIVER_SHA': L.DRIVER_SHA,
      'Error': ValueError, 'pin_doc': lambda ref, label: s.doc(ref)}
exec(compile(selected(core, ['canonical', 'digest', 'point_identity', 'Mapper']), 'pinned core mapper', 'exec'), cs)
ledger = source(ART/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py',
                '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229')
ls = {'OldMapper': cs['Mapper'], 'O': o, 'copy': copy, 'Error': ValueError}
exec(compile(selected(ledger, ['Mapper']), 'pinned ledger mapper', 'exec'), ls)
theta0 = points[0]['theta']
base = json.loads(Path(points[0]['spec']['path']).read_bytes())
ctx = types.SimpleNamespace(base=base, base_sha256=L.digest(base), inclination_deg=66.0,
    es={'names': list(theta0), 'trial_values': theta0, 'fixed_names': [],
        'lower': {k: -100.0 for k in theta0}, 'upper': {k: 100.0 for k in theta0}},
    cfg={'tail_readiness': {'certificate_registry': gen,
                           'certificate_ledger': {'schema': 'synthetic', 'path': str(ROOT/'UNOPENED_LEDGER')}}},
    genesis_points=lambda: {}, certificate_record=lambda ident: None)
mapper = ls['Mapper'](ctx)
ctx.mapper = mapper
for i, row in enumerate(points):
    built = mapper.build(row['theta'])
    check('actual_parent_core_mapper_pending_bytes_%d'%i,
          built['raw'] == Path(row['spec']['path']).read_bytes())
ctx.certificate_record = lambda ident: next(
    (r['record'] for r in rec['records'] if r['record']['identity'] == ident), None)
for i, point in enumerate(ready['points']):
    built = mapper.build(point['theta'])
    check('actual_ledger_mapper_final_bytes_%d'%i, built['raw'] == point['raw'] and
          built['sha256'] == point['sha256'])

# Actual points_manifest function, with an inert natural-wave/probe boundary.
# It writes three pending specs using the production mapper, then those bytes
# feed the same two-slot function. The probe is explicitly synthetic.
entry = source(ART/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py',
               'cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d')
ctx.certificate_record = lambda ident: None
ctx.config_sha256 = 'a'*64
ctx.cache_id = 'b'*64
ctx.ledger_head = lambda: {'synthetic': True}
misses = [{'theta': p['theta'], 'key': L.theta_key(p['theta'])} for p in points]
class InertOrchestrator:
    def __init__(self, ctx):
        self.cache = None
        self.probe = types.SimpleNamespace(run=lambda cache, label: {'complete': False, 'misses': misses})
    def prepare(self, create=False):
        assert create is False
    def _dedup(self, misses):
        return misses
    def wave_dirs(self):
        return [1, 2]
o.utc = lambda: 'SYNTHETIC_NO_CLOCK'
em = types.SimpleNamespace(O=o, Context=lambda config: ctx, Orchestrator=InertOrchestrator, Error=ValueError)
en = {'os': os, 'Path': Path, 'json': json, 'hashlib': hashlib, 'ART': str(ART),
      'MAX_POINTS_PER_WAVE': 99, 'POINTS_LIST_SCHEMA': N.P.LIST_SCHEMA,
      '__file__': str(ART/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py'),
      'WRAPPER': ART/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py',
      'WRAPPER_SHA': '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'}
exec(compile(selected(entry, ['lexical_artifacts_dir', 'sha_bytes', 'points_manifest']),
             'pinned points manifest', 'exec'), en)
manifest_result = en['points_manifest'](em, {}, str(ROOT/'NATURAL_W3_SYNTHETIC'))
check('actual_points_manifest_success', manifest_result.get('status') != 'REFUSED', manifest_result)
emitted = json.loads((ROOT/'NATURAL_W3_SYNTHETIC/POINTS_LIST.json').read_bytes())
for i, row in enumerate(emitted['points']):
    pending = Path(row['spec']['path']).read_bytes()
    result = L.fill(json.loads(pending), ready['points'][i]['record'])
    check('actual_manifest_then_fill_matches_direct_%d'%i,
          pending == Path(points[i]['spec']['path']).read_bytes() and result == ready['points'][i]['raw'])

mutation_index = 0
def refuse(name, req, expected):
    global mutation_index
    mutation_index += 1
    p = write('M%02d_REQUEST.json'%mutation_index, req)
    try:
        L.validate(SyntheticSnapshot(), p)
    except Exception as exc:
        check(name, expected in str(exc), type(exc).__name__+': '+str(exc))
    else:
        check(name, False, 'ACCEPTED')
def paired(name, mutate, expected):
    rr = copy.deepcopy(rec)
    mutate(rr)
    rrpin = write(name+'_RECORDS.json', rr)
    vv = copy.deepcopy(rep)
    vv['records'] = rrpin
    vvpin = write(name+'_VERIFY.json', vv)
    q = dict(request, records=rrpin, verification=vvpin)
    refuse(name, q, expected)
refuse('wrong_C1', dict(request, c1=dict(c1six, sha256='0'*64)), 'FROZEN_C1')
refuse('wrong_genesis', dict(request, genesis_registry=other_gen), 'FROZEN_C1')
refuse('unknown_request_field', dict(request, allow_pending=True), 'REQUEST_FIELDS')
refuse('wrong_verification_sha', dict(request, verification=dict(verify_ref, sha256='0'*64)), 'INPUT_SHA_MISMATCH')
refuse('wrong_approved_list', dict(request, approved_producers=write('BAD_APPROVED.json', six[:3])), 'FROZEN_SIX')
paired('records_generator', lambda r: r.update(generator=OLD_ASSEMBLER if False else dict(L.ASSEMBLER, sha256='0'*64)),
       'RECORDS_GENERATOR')
paired('records_assembler', lambda r: r.update(c3v004_assembler=L.C3V004), 'RECORDS_ASSEMBLER_BINDING')
paired('eps_source_drift', lambda r: r.update(eps_source_pins_digest='0'*64), 'GENESIS_EPS_SOURCE_DRIFT')
paired('wrong_record_theta', lambda r: r['records'][0]['theta'].update(common_scale_s=9.0), 'RECORD_LIST_MISMATCH')
paired('wrong_record_pending_sha', lambda r: r['records'][0].update(pending_spec_sha256='0'*64), 'RECORD_LIST_MISMATCH')
paired('wrong_record_count', lambda r: r.update(count=2), 'POINT_COUNTS_MISMATCH')
paired('wrong_record_wave', lambda r: r['records'][0].update(wave=4), 'RECORD_WAVE_MISMATCH')
paired('wrong_record_slot', lambda r: r['records'][0]['record'].update(
    lo_certificate=r['records'][1]['record']['lo_certificate']), 'BUNDLE_IDENTITY_OR_SLOTS')
for field, value, expected in (
        ('ok', 1, 'VERIFY_NOT_PASS'),
        ('n_ok', True, 'POINT_COUNTS_MISMATCH'),
        ('records', dict(records, sha256='0'*64), 'VERIFY_BINDING'),
        ('generator', L.OLD_ASSEMBLER, 'VERIFY_SCHEMA_OR_GENERATOR')):
    v = copy.deepcopy(rep); v[field] = value
    refuse('bad_verify_'+field, dict(request, verification=write('BAD_VERIFY_'+field+'.json', v)), expected)

# Pin-preserving cache is used by both hash and replay. A repeated read cannot
# use a second buffer. An alias to the same inode is not needed for this task.
pre_counts = dict(s.counts)
assert s.read(request_ref) == Path(request_ref['path']).read_bytes()
check('snapshot_repeated_read_does_not_reopen', pre_counts == s.counts)
try:
    s.read(dict(request_ref, sha256='0'*64))
except L.Refusal:
    check('cached_bytes_still_validate_each_pin', True)
else:
    check('cached_bytes_still_validate_each_pin', False)
unreplayed = L.validate(SyntheticSnapshot(), request_ref)
try:
    L.publish(s, unreplayed, str(ROOT/'UNREPLAYED_OUTPUT'))
except L.Refusal as exc:
    check('unreplayed_output_refused', 'FULL_REPLAY_REQUIRED' in str(exc))
else:
    check('unreplayed_output_refused', False)
published = L.publish(s, ready, str(ROOT/'PUBLISHED'))
check('exclusive_publish_exact_bytes', all(
    Path(p['path']).read_bytes() == point['raw'] and rawpin(Path(p['path'])) == p
    for p, point in zip(published['specs'], ready['points'])))
try:
    L.publish(s, ready, str(ROOT/'PUBLISHED'))
except L.Refusal as exc:
    check('existing_output_refused', 'EXCLUSIVE_OUTPUT' in str(exc))
else:
    check('existing_output_refused', False)

