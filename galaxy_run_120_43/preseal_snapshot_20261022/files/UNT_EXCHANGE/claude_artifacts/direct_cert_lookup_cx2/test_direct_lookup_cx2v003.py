"""Release candidate v002 bridge tests plus the 48 mapping/integrity checks."""
from pathlib import Path
prefix = Path(__file__).with_name('direct_lookup_cases_prefix_cx2v003.py')
exec(compile(prefix.read_bytes(), str(prefix), 'exec'), globals())

adapter = load(HERE/'direct_preflight_cert_cx2v002.py', 'direct_adapter_candidate')
native_calls = {'policy': 0, 'sensitivity': 0, 'prelaunch': 0, 'base': 0}
native_failures = {'policy': False, 'sensitivity': False}
class InertBaseContext:
    def certificate_policy_gate(self):
        native_calls['policy'] += 1
        _, reasons = A.c1_policy_gate(c1six, gen)
        if native_failures['policy']:
            reasons.append('SYNTHETIC_POLICY_REFUSAL')
        return {'ok': not reasons, 'reasons': reasons}
    def sensitivity_gate(self, spec):
        native_calls['sensitivity'] += 1
        return {'ok': not native_failures['sensitivity'],
                'reasons': ['SYNTHETIC_SENSITIVITY_REFUSAL'] if native_failures['sensitivity'] else []}
    def prelaunch_check(self, spec, recovery=False):
        native_calls['prelaunch'] += 1
        a, b = self.sensitivity_gate(spec), self.certificate_check(spec, 'prelaunch')
        if not a['ok'] or not b['ok']:
            raise ValueError('INERT_BASE_PREFLIGHT_GATE')
        return copy.deepcopy(spec)
def base_build(C, config, guard, admission):
    native_calls['base'] += 1
    ctx = InertBaseContext()
    ctx.cfg = copy.deepcopy(config)
    ctx.numerics = copy.deepcopy(base['numerics'])
    return ctx
def native_read(ref, label):
    raw = Path(ref['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ref['sha256']
    return raw
native_O = types.SimpleNamespace(read_pinned=native_read,
    load_pinned_module=lambda ref, name, label: types.SimpleNamespace(
        derive_custody=lambda spec, driver_sha256: custody))
native_M = types.SimpleNamespace(digest=L.digest, canonical=L.canonical,
    pin_doc=lambda ref, label: json.loads(native_read(ref, label)))
native_C = types.SimpleNamespace(O=native_O, M=native_M, G=G, Error=ValueError,
    DRIVER_SHA=L.DRIVER_SHA, validate_block=A.validate_block, point_identity=L.point_identity)
def guard_load(ref, admission, name):
    assert ref in (adapter.LOOKUP, adapter.BASE_ADAPTER)
    assert rawpin(Path(ref['path'])) == ref
    if ref == adapter.LOOKUP:
        return L
    return types.SimpleNamespace(build=base_build)
sg = types.SimpleNamespace(require=L.need, load=guard_load)
config = {'tail_readiness': json.loads(Path(c1six['path']).read_bytes())['tail_readiness']}
admission = {'direct_certificate_lookup': {'request': request_ref, 'manifest': published['manifest']}}
direct = adapter.build(native_C, config, guard=sg, admission=admission)
final = json.loads(ready['points'][0]['raw'])
cg = direct.certificate_check(final, 'prelaunch')
check('direct_adapter_native_certificate_body_passes', cg['ok'] is True, cg)
check('direct_adapter_native_base_is_called', native_calls['base'] == 1, native_calls)
check('direct_adapter_inherited_sensitivity_is_called', direct.sensitivity_gate(final)['ok'] is True and
      native_calls['sensitivity'] == 1)
check('direct_adapter_inherited_prelaunch_is_called', direct.prelaunch_check(final) == final and
      native_calls['prelaunch'] == 1)
check('direct_adapter_acceptance_not_exposed', direct.certificate_check(final, 'acceptance') ==
      {'ok': False, 'blockers': ['DIRECT_CERT_PREFLIGHT_ONLY']})
unknown = copy.deepcopy(final)
unknown['physical']['common_scale_s'] = 1.999
unknown_result = direct.certificate_check(unknown, 'prelaunch')
check('direct_unknown_point_refused', unknown_result['ok'] is False and
      unknown_result['blockers'] == ['CERTIFICATE_POINT_MISSING_OR_MISMATCHED'])
def throws(name, fn, expected):
    try:
        fn()
    except Exception as exc:
        check(name, expected in str(exc), type(exc).__name__+': '+str(exc))
    else:
        check(name, False, 'ACCEPTED')
wrong = copy.deepcopy(final)
wrong['label'] += ' modified'
throws('direct_label_not_bound_final_refused', lambda: direct.certificate_check(wrong, 'prelaunch'),
       'DIRECT_CERT_SPEC_NOT_EXACT_FINAL')
wrongslot = copy.deepcopy(final)
wrongslot['numerics']['uv_tail']['lo_certificate'] = ready['points'][1]['record']['lo_certificate']
throws('direct_other_point_slot_refused', lambda: direct.certificate_check(wrongslot, 'prelaunch'),
       'DIRECT_CERT_SPEC_NOT_EXACT_FINAL')
throws('direct_bridge_required', lambda: adapter.build(native_C, config, guard=sg, admission={}),
       'DIRECT_CERT_LOOKUP_BINDING_REQUIRED')
bad_config = copy.deepcopy(config)
bad_config['tail_readiness']['approved_certificate_producers'].reverse()
throws('direct_config_C1_policy_binding', lambda: adapter.build(native_C, bad_config, guard=sg, admission=admission),
       'DIRECT_CERT_C1_POLICY_MISMATCH')
native_failures['policy'] = True
refused_policy = direct.certificate_check(final, 'prelaunch')
check('direct_native_policy_not_bypassed', refused_policy['ok'] is False and
      'SYNTHETIC_POLICY_REFUSAL' in refused_policy['blockers'])
native_failures['policy'] = False
native_failures['sensitivity'] = True
throws('direct_native_sensitivity_not_bypassed', lambda: direct.prelaunch_check(final), 'INERT_BASE_PREFLIGHT_GATE')
native_failures['sensitivity'] = False
corrupt_manifest = json.loads(Path(published['manifest']['path']).read_bytes())
corrupt_manifest['points'][0]['spec'] = corrupt_manifest['points'][1]['spec']
corrupt_ref = write('CORRUPT_MANIFEST.json', corrupt_manifest)
bad_admission = {'direct_certificate_lookup': {'request': request_ref, 'manifest': corrupt_ref}}
throws('direct_manifest_wrong_spec_refused', lambda: adapter.build(native_C, config, guard=sg, admission=bad_admission),
       'DIRECT_CERT_FINAL_SPEC_BYTES')

# The native certificate function differs only in name and the two-line genesis
# lookup replaced with a one-line genesis-plus-record lookup.
original_wrapper = source(ART/'calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',
    '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d')
original_class = next(n for n in original_wrapper.body if isinstance(n, ast.ClassDef) and n.name == 'Context')
original_fn = copy.deepcopy(next(n for n in original_class.body if isinstance(n, ast.FunctionDef) and n.name == 'certificate_check'))
original_fn.name = '_certificate_check_snapshot'
original_fn.body = [n for n in original_fn.body if not (isinstance(n, ast.Assign) and
    any(isinstance(t, ast.Name) and t.id in ('registry', 'rec') for t in n.targets))]
adapter_tree = ast.parse(Path(adapter.__file__).read_bytes())
adapter_fn = copy.deepcopy(next(n for n in ast.walk(adapter_tree) if isinstance(n, ast.FunctionDef) and
                                    n.name == '_certificate_check_snapshot'))
adapter_fn.body = [n for n in adapter_fn.body if not (isinstance(n, ast.Assign) and
    any(isinstance(t, ast.Name) and t.id == 'rec' for t in n.targets))]
check('native_certificate_AST_unchanged_except_lookup',
      ast.dump(original_fn, include_attributes=False) == ast.dump(adapter_fn, include_attributes=False))
throws('protected_path_refused_before_open', lambda: L.safe_path(
    '/Users/bgm/Research/NGC3198_DO_NOT_OPEN/velocity.dat'), 'PROTECTED_PATH_REFUSED')
throws('duplicate_JSON_key_refused', lambda: L.decode(b'{"x":1,"x":2}'), 'DUPLICATE_JSON_KEY')
throws('nonfinite_JSON_refused', lambda: L.decode(b'{"x":NaN}'), 'NONFINITE_JSON')
changed = copy.deepcopy(ready)
changed['points'][0]['raw'] += b' '
throws('post_replay_spec_mutation_refused', lambda: L.publish(s, changed, str(ROOT/'ALTERED_AFTER_REPLAY')),
       'FULL_REPLAY_REQUIRED')
changed = copy.deepcopy(ready)
changed['verification']['points'][0]['wrapper_replica']['block']['block_sha256'] = '0'*64
throws('full_verify_tamper_is_replayed_and_refused', lambda: L.replay(SyntheticSnapshot(), changed),
       'FULL_VERIFY_REPLAY_MISMATCH')

# Exercise the actual guard014 source fence and pinned module loader. The base
# context and custody remain the explicit synthetic boundaries described above.
stepguard = load(ART/'s1_successors_c2/step4_guard_c2v014.py', 'actual_guard014_fence')
fence_sources = {p: rawpin(Path(p))['sha256'] for p in list(READS) if Path(p).suffix == '.py'}
fence_cfg = {'sources': fence_sources}
with stepguard.fence(fence_sources):
    loaded_lookup = stepguard.load(adapter.LOOKUP, fence_cfg, 'guard_loaded_lookup')
    loaded_adapter = stepguard.load(rawpin(Path(adapter.__file__)), fence_cfg, 'guard_loaded_adapter')
    check('actual_guard014_loads_lookup_source', loaded_lookup.DIRECT_LOOKUP_API == L.DIRECT_LOOKUP_API)
    check('actual_guard014_loads_adapter_source', loaded_adapter.DIRECT_CONTEXT_API == adapter.DIRECT_CONTEXT_API)
    fenced_direct = loaded_adapter.build(native_C, config, guard=sg, admission=admission)
    check('actual_guard014_fence_admits_synthetic_bridge_preflight',
          fenced_direct.certificate_check(final,'prelaunch')['ok'] is True)
throws('actual_guard014_refuses_unadmitted_lookup_source',
    lambda: stepguard.load(adapter.LOOKUP, {'sources': {}}, 'unadmitted_source'), 'SOURCE_NOT_ALLOWLISTED')

inputs = [rawpin(Path(p)) for p in sorted(READS) if not Path(p).is_relative_to(ROOT)]
result = {'schema': 'DIRECT_LOOKUP_TESTS_CX2V003', 'status': 'TESTED',
    'n': len(RESULTS), 'passed': sum(r['passed'] for r in RESULTS), 'cases': RESULTS,
    'inputs': inputs, 'snapshot_counts': s.counts, 'native_calls': native_calls,
    'scope': 'Synthetic custody and inert direct base-construction/sensitivity/normalizer boundary. '
             'Actual pinned mapper, points-manifest, list verifier, native certificate body and b1 guard.',
    'untested': ['actual W3 selection', 'production pending or final spec bytes', 'physical custody',
                 'full production direct Context construction', 'launch admission'],
    'no_subprocess_network_delete_rename_existing_write': True}
out = write('TEST_REPORT.json', result)
print(json.dumps({'report': out, 'n': result['n'], 'passed': result['passed']}))
raise SystemExit(0 if result['passed'] == result['n'] else 1)
