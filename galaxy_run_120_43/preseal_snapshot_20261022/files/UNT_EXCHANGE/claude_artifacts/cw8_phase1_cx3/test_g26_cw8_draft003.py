"""G26 synthetic saved-state integration. No forward or subprocess runs.

Reuses c2v007's synthetic receipt/registry fixture adapter. Its registry verifier
is an explicit test seam; the real ledger, pass driver, geometry adapter and
v003g freeze writer are exercised. A previously saved synthetic calibration
record supplies exploration; no calibration engine is executed.
"""
import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import types
import traceback

HERE = Path(__file__).resolve().parent
ART = HERE.parent
WORK = Path(sys.argv[1]).resolve()
INHERITED = ART / 'runbook_v002_c2v007_cx2/test_inherited_a253_v002.py'
INHERITED_SHA = '20ccdc70f79e246e8db456b3b41592f8ec00553ce604affb9c41570679bd6378'
FREEZE = ART / 'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py'
FREEZE_SHA = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
METADATA = ART / 's0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V004.json'
METADATA_SHA = '54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce'
OLD = Path('/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/c2v004_dryrun_final')
CALIBRATION = OLD / 'DRYRUN_CALIBRATION_RECORD.json'
CALIBRATION_SHA = '22ac6146991a83ee20927769618b88c57ab74d81b92fe4155815c7661fda6fe6'
REGION = OLD / 'DRYRUN_SYNTHETIC_REGION_NOT_DDO154.json'
REGION_SHA = '7bafa31f623632593853673d53cc36fb3208e95c173b75f58d26d57110a05ec8'
G26 = HERE / 'g26_freeze_cx3cw8_draft003.py'
ALLOWED = {str(CALIBRATION), str(REGION), str(G26)}
PINS = []


def raw_pin(path, expected=None):
    raw = Path(path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert expected is None or expected == sha, str(path)
    PINS.append({'path': str(path), 'sha256': sha})
    return raw


def module(raw, path, name):
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    return mod


g = module(raw_pin(G26), G26, 'g26_synthetic')
fm = module(raw_pin(FREEZE, FREEZE_SHA), FREEZE, 'v003g_selection_only')
metadata = json.loads(raw_pin(METADATA, METADATA_SHA))
values = {r['kwarg']: r for r in metadata['write_freeze_manifest_inputs']}
spec = copy.deepcopy(values['spec']['value']['spec_of_record'])
notes = copy.deepcopy(values['notes']['value'])
record = json.loads(raw_pin(CALIBRATION, CALIBRATION_SHA))
raw_pin(REGION, REGION_SHA)
# Only select representatives from the saved record; the sole read is the
# pinned synthetic region. No run, forward callback or engine is called.
old_read = fm._read_regular
def selection_read(path, nonempty):
    assert os.path.realpath(path) == str(REGION), path
    return old_read(path, nonempty)
fm._read_regular = selection_read
selection = fm.select_representative_points(exploration=record['run'], interior_count=5, spec=spec)
assert selection.get('ok'), selection.get('reasons')

EXTRA_CASES = raw_pin(ART / 'g26_freeze_script_cx2/g26_cases_draft001.py').decode()
source = raw_pin(INHERITED, INHERITED_SHA).decode()
source = source.replace("BUILDER = HERE / 'roster_builder_c2v007_a253_v001.py'","BUILDER = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8_draft003.py')")
source = source.replace("BUILDER_SHA = '799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b'","BUILDER_SHA = 'bd81967c0aaacf9cf161897e2fc07f9bc8552dbad1c333744abb8b1397cfe857'")
# Keep fixture definitions and world setup, without invoking the old case loop.
source = source.split("\nif len(sys.argv) > 2:\n")[0]
source = source.replace("source = source.replace(\n    \"sorted(produced)",
                        "source = source.replace(\n    \"sorted(produced)", 1)
source = source.replace("parent_tree = ast.parse(source)",
    """source = source.replace(
        "'query_block': {'rows':", "'ngc3198_slots': [{k:c[k] for k in ('name','transform','lower','upper','trial_value','units','reference_value')} for c in COORDS if c['scope']=='ngc3198_nuisance'], 'query_block': {'rows':", 1)
parent_tree = ast.parse(source)""")
source = source.replace("sys.addaudithook(audit)", """
old_audit = audit
def audit(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.path.realpath(os.fsdecode(args[0]))
        flags = args[2]
        if path in EXTRA_ALLOWED and isinstance(flags, int) and not flags & (os.O_WRONLY | os.O_RDWR):
            READS.append(path)
            return
    return old_audit(event,args)
sys.addaudithook(audit)
""")
source = source.replace("world = t.World(env)", """
env.allowed.update(EXTRA_ALLOWED)
t.COORDS = CUSTOM_SPEC['coordinates']
t.SEL = {k:v for k,v in CUSTOM_SELECTION.items() if k!='points'}
t.US = [p['u'] for p in CUSTOM_SELECTION['points']]
t.LOGS = [p['log_index'] for p in CUSTOM_SELECTION['points']]
t.ROLES = [p['role'] for p in CUSTOM_SELECTION['points']]
t.PROJ = [p['identified_projection'] for p in CUSTOM_SELECTION['points']]
world = t.World(env)
""")
fixture = types.ModuleType('g26_fixture')
# Preserve inherited __file__ for its source dependency paths, not the wrapper.
fixture.__file__ = str(INHERITED)
fixture.__dict__.update(EXTRA_ALLOWED=ALLOWED, CUSTOM_SPEC=spec, CUSTOM_SELECTION=selection)
exec(compile(source, str(INHERITED), 'exec'), fixture.__dict__)
env, w, t = fixture.env, fixture.world, fixture.t
rb = env.rb
b = w.b1
b.activate()

calls = [b.call(env.dir('g26_calls'), t.PRIMARY, 'MEMBER', m, theta,
                [('FINISHED', '2026-10-23T%02d:00:00Z' % (i + 1))],
                cut_kpc=None, seed=float(i))
         for i, (m, theta) in enumerate(b.thetas.items())]
out = w.build_p1('g26_full', calls=calls)
plan_pin = t.pin(os.path.join(out, 'REPLAY_PLAN.json'))
p1, _, _ = t.drive(env, b, out, 'PASS_ONE')
pk, _, _ = t.drive(env, b, out, 'PASS_K')
p1pin = fixture.jwrite(WORK / 'pass_one.json', p1)
pkpin = fixture.jwrite(WORK / 'pass_k.json', pk)
comparison, _, successor = t.step7(env, out, plan_pin, p1pin, pkpin)
assert comparison['status'] == 'NO_NEW_DISCREPANCY' and successor is None
head_pin = t.pin(os.path.join(t.ledger_dir(out), 'STEP7_0001.json'))
pass_input = fixture.jwrite(WORK / 'pass_input.json', {
    'schema': 'PASS_INPUT_C2V003', 'pass_label': 'PASS_K', 'freeze_module': b.fm_pin,
    'build_record': t.pin(os.path.join(out, 'BUILD_RECORD.json')), 'replay_plan': plan_pin,
    'roster_pins': t.pin(os.path.join(out, 'ROSTER_PINS.json')), 'selection': b.sel,
    'spec': b.spec_pin, 'null_direction_rule': t.NULL_RULE})
notes_pin = fixture.jwrite(WORK / 'notes.json', notes)
parameter_pin = fixture.jwrite(WORK / 'parameter_region.json', {
    'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS',
    'scope': 'synthetic saved-state replay'})
observation_pin = fixture.jwrite(WORK / 'observation_rule.json', {
    'kind': 'SYNTHETIC_SAVED_RECTANGLES', 'scope': 'not an observational data record'})
input_doc = {
    'schema': g.INPUT_SCHEMA, 'pass_input': pass_input, 'ledger_head': head_pin,
    'slots': b.slots, 'notes': notes_pin, 'parameter_region': parameter_pin,
    'observation_rule': observation_pin, 'code_files': [],
    'input_files': [{'path': str(CALIBRATION), 'sha256': CALIBRATION_SHA},
                    {'path': str(REGION), 'sha256': REGION_SHA}],
}
input_pin = fixture.jwrite(WORK / 'g26_input.json', input_doc)
# Explicit test-only constant seams. The deliverable has no override CLI.
g.SPEC_SHA256 = b.spec_pin['sha256']
g.SLOTS_SHA256 = b.slots['sha256']
g.QUERY_ROLE = 'SYNTHETIC_FIXTURE'
results = []


def case(name, fn, code=None):
    try:
        value = fn()
        verdict = 'PASS' if code is None else 'FAIL'
        detail = None if code is None else 'NO_REFUSAL'
    except rb.Refused as exc:
        verdict = 'PASS' if exc.code == code else 'FAIL'
        detail = exc.code
    except Exception as exc:
        verdict = 'FAIL'
        detail = traceback.format_exc()[-1800:]
    results.append({'id': name, 'expected': code or 'PASS', 'verdict': verdict, 'detail': detail})
    print(json.dumps(results[-1], sort_keys=True), flush=True)


def happy():
    before = len(fixture.READS)
    result = g.freeze(rb, input_pin, str(WORK / 'freeze_happy'))
    counts = collections.Counter(fixture.READS[before:])
    assert counts and max(counts.values()) == 1, {k:n for k,n in counts.items() if n != 1}
    assert result['allow_incomplete'] is True
    assert result['freeze_status'] == 'FREEZE_INCOMPLETE'
    assert result['pass_k_byte_equal'] and result['dn2_coordinates_equal']
    return result


case('G001_saved_replay_full_writer_single_read', happy)
exec(compile(EXTRA_CASES, str(ART / 'g26_freeze_script_cx2/g26_cases_draft001.py'), 'exec'), globals())
fixture.jwrite(WORK / 'TEST_RECORD.json', {
    'scope': __doc__, 'sources_from_bytes': PINS, 'cases': results,
    'n_cases': len(results), 'n_pass': sum(r['verdict']=='PASS' for r in results),
    'no_forward_or_subprocess_calls': True,
    'synthetic_seams': ['registry verifier from inherited harness',
                       'slots/spec hashes and synthetic query role', 'synthetic v003g slots/node constants'],
})
raise SystemExit(0 if all(r['verdict']=='PASS' for r in results) else 1)
