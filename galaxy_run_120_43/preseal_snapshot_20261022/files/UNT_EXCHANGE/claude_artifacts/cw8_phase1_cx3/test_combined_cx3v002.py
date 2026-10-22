"""Synthetic saved-state chain: actual cw8 custody -> registry -> builder -> replay -> G26.

No forward, numerical engine, comparator, monitor, sampler or subprocess is run.
Source-pin/System substitutions are explicit fixture seams. The registry is
rederived by the actual P112 verifier, not the inherited registry fixture seam.
"""
import _strptime
import ast
import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
DATE = subprocess.check_output(['/bin/date', '-u'], text=True).strip()
OLD = Path('/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/c2v004_dryrun_final')
EXTRA = {str(OLD/'DRYRUN_CALIBRATION_RECORD.json'),
         str(OLD/'DRYRUN_SYNTHETIC_REGION_NOT_DDO154.json'),
         str(ART/'s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V004.json')}
READS = []
GENERATED = set()
SOURCE_PINS = []


def audit(event, args):
    if event.startswith('socket.') or event in (
            'os.rename', 'os.remove', 'os.rmdir', 'os.system', 'os.fork',
            'os.posix_spawn', 'os.kill', 'os.killpg', 'os.symlink'):
        raise AssertionError('COMBINED_FENCE: ' + event)
    if event == 'subprocess.Popen' and args[1] != ['/bin/date', '-u']:
        raise AssertionError('NO_PROCESS: ' + repr(args[1]))
    if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    p = Path(os.path.realpath(os.fsdecode(args[0])))
    flags = args[2]
    writing = isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR))
    within = p.is_relative_to(WORK)
    if writing:
        if not within or os.path.lexists(p) or not flags & os.O_EXCL:
            raise AssertionError('EXCLUSIVE_NEW_FILE: ' + str(p))
        GENERATED.add(str(p))
        if 'G' in globals():
            G.env.allowed.add(str(p))
    else:
        allowed_source = p.is_relative_to(ART) and p.suffix == '.py' and '/runs_ext/' not in str(p)
        runtime = p.is_relative_to(Path(sys.base_prefix))
        if not (within or allowed_source or runtime or str(p) in EXTRA):
            raise AssertionError('READ_FENCE: ' + str(p))
        if not p.is_dir():
            READS.append(str(p))


sys.addaudithook(audit)


def raw(path):
    data = path.read_bytes()
    SOURCE_PINS.append({'path': str(path), 'sha256': hashlib.sha256(data).hexdigest()})
    return data


def definitions(path, before, name, work):
    source = raw(path).decode().split(before)[0]
    assert source != path.read_text(), 'definition delimiter missing'
    module = types.ModuleType(name)
    module.__file__ = str(path)
    oldargs = sys.argv
    oldhook = sys.addaudithook
    sys.argv = [str(path), str(work)]
    # Keep the already-installed outer audit; nested fixtures' older fences
    # reject the other fixture's synthetic files. No actual fence is removed.
    sys.addaudithook = lambda hook: None
    try:
        exec(compile(source, str(path)+':definitions', 'exec'), module.__dict__)
    finally:
        sys.argv = oldargs
        sys.addaudithook = oldhook
    return module


P = definitions(HERE/'test_selector_cx3v002.py',
                '\ncase("missing_license_automatic_serial"', 'p112_fixture', WORK/'p112')
P.READS = READS
G = definitions(HERE/'test_g26_cx3v002.py',
                '\ncalls = [b.call', 'g26_fixture_setup', WORK/'g26')
G.fixture.READS = READS
G.env.allowed.update(GENERATED)
G.env.allowed.add(str(P.TOOL))
M, b, rb, t = P.M, G.b, G.rb, G.t
custody_path = HERE/'test_custody_cx3v002.py'
custody_source = raw(custody_path).decode()
for node in ast.parse(custody_source).body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            'saved_monitor', 'save_full', 'save_twin', 'consumer_factory'):
        exec(compile(ast.get_source_segment(custody_source, node),
                     str(custody_path)+':'+node.name, 'exec'), P.__dict__)

# Keep the mock kit's invented theta distinct from this replay PLAN. Its
# canonical seed-key constant is substituted only in synthetic Context modules.
M.SEED_KEY = M.theta_key({'Eref_base_J':2.5,'ell_F_m':6.0,'gamma_over_Eref':0.125,
                         'common_scale_s':1.5,'entropy_K_factor':3.0})
f = P.make_context()
ctx0 = f.ctx
root = f.root/'combined_plan'
root.mkdir()


def put(name, doc, binary=False):
    p = root/name
    p.parent.mkdir(parents=True, exist_ok=True)
    return P.put(p, doc, raw=binary)


plan_pin = b.plan_outputs[t.PRIMARY]
members = M.read_pin(plan_pin)['members']
assert len(members) >= 3
export = put('export.json', {'schema': 'UNT_STEP5_ADMITTED_POINT_EXPORT_CX3V001',
    'target_free': True, 'admitted_points': [
        {'log_index': m['log_index'], 'theta_natural': m['theta_engine']} for m in members]})


def fd(th, role, **extra):
    return dict(theta_natural=th, theta_hex={k: v.hex() for k, v in th.items()},
                key=M.theta_key(th), role=role, **extra)


fdmembers = [fd(m['theta_engine'], m['role'], log_index=m['log_index']) for m in members]
fs = [fd(m['theta_engine'], 'F%d'%k) for k, m in enumerate(members[:3])]
fdplan = put('fdplan.json', {'schema': 'PHASE1_FDPLAN_C2V001', 'members': fdmembers, 'F': fs})
lines = ['## A999: SYNTHETIC COMBINED P112 TEST',
         'TOOL_PIN P112_LAUNCHER_CX3CW8V002 %s %s'%(P.TOOL_SHA, P.TOOL),
         'WATCH_PIN MEMORY_WATCH %s %s'%(f.watch['sha256'], f.watch['path'])]
for name in ('S0_SEED_SERIAL', M.TWIN):
    sp = ctx0.get_vpin('SPEC_PIN', name)
    lines.append('SPEC_PIN %s %s %s'%(name, sp['sha256'], sp['path']))
lines.append('CW8_LICENSE_PIN path=%s sha256=%s'%(f.license['path'], f.license['sha256']))


def fill(name, th, member=None):
    key = M.theta_key(th)
    eps = put(name+'/EPS.json', {'point': {'key': key}})
    gq = put(name+'/GQ.json', {'point': {'key': key}})
    hand = {'schema': 'UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001' if member is not None
            else 'UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001',
            'mode': 'SYNTHETIC_DRY_ONLY', 'driver_branch': 'cx3r008',
            'certificate_pins': {'eps_certificate': eps, 'lo_certificate': f.overrides['lo']},
            'policy_pin': f.overrides['policy']}
    if member is not None:
        hand.update(log_index=member['log_index'], source_export_pin=export)
    else:
        hand.update(point_key=key, source_pin=fdplan)
    hp = put(name+'/HANDOFF.json', hand)
    spec = {'fixture_mode': 'COMPLETED', 'label': 'step5 A_K32_A2_HEADLINE theta_key='+key,
            'physical': {'Eref_J': th['Eref_base_J'], 'ell_F_m': th['ell_F_m'],
                'gamma': th['gamma_over_Eref']*th['Eref_base_J'], 'common_scale_s': th['common_scale_s'],
                'entropy_K_factor': th['entropy_K_factor'], 'distance_Mpc': 13.8, 'inclination_deg': 72.0},
            'numerics': {'route_a': {'column_workers': 1},
                         'uv_tail': {'eps_certificate': eps, 'lo_certificate': f.overrides['lo']}}}
    sp = put(name+'/fill/'+M.SERIAL_FILE, spec)
    spec8 = copy.deepcopy(spec); spec8['numerics']['route_a']['column_workers'] = 8
    sp8 = put(name+'/fill/'+M.TWIN_FILE, spec8)
    put(name+'/fill/'+M.FILL_FILE, {'schema': 'UNT_STEP5_FILLED_SPECS_C2V001',
        'launch_authorized': False, 'handoff_pin': hp, 'theta_key': key, 'pending_certificates': []})
    if member is not None:
        lines.extend(['HANDOFF_PIN %s %s %s'%(name, hp['sha256'], hp['path']),
                      'SPEC_PIN %s %s %s'%(name, sp['sha256'], sp['path']),
                      'SPEC_PIN %s_FULL_CW8 %s %s'%(name, sp8['sha256'], sp8['path'])])
    return {'handoff': hp, 'fill_dir': str(root/name/'fill'), 'eps': eps, 'gq': gq}


mc = [dict(fill('P1_M%04d'%m['log_index'], m['theta_engine'], m),
           log_index=m['log_index'], role=m['role'], order=i, member_id=m['member_id'])
      for i, m in enumerate(members)]
fc = [dict(fill('P1_F%d'%k, v['theta_natural']), label='F%d'%k) for k, v in enumerate(fs)]
vpin = put('V006.md', ('\n'.join(lines)+'\n').encode(), True)
buildpin = put('PLAN_BUILD.json', {'status': 'BUILT', 'stage': 'PLAN', 'phase': 'PHASE_1',
                                 'synthetic': True, 'plan_output_primary': plan_pin})
cfg = dict(f.config_doc, v006=vpin['path'], members=mc, f_points=fc, plan_output_primary=plan_pin,
           plan_build_record=buildpin, selection=b.sel, fdplan=fdplan, spec_of_record=b.spec_pin)
cp = put('CONFIG.json', cfg)
f.overrides['spec_of_record'] = b.spec_pin
f.config_doc, f.config = cfg, cp
f.ctx = f.context(cp)
ctx = f.ctx
assert len([c for c in ctx.calls() if c['origin']=='P112']) == len(members)
MEMBERS_BY_KEY = {m['member_id']: m for m in members}
SYNTHETIC_RESULTS = {}


def saved_monitor(ctx, call, outdir, caps, *, start='2026-10-22T00:00:12Z', end='2026-10-22T00:00:14Z'):
    Path(outdir).mkdir()
    if call['name'] == M.TWIN:
        result = {'synthetic': True, 'status': 'COMPLETED', 'valid': False}
    else:
        theta = MEMBERS_BY_KEY[call['key']]['theta_ngc']
        result = b.valid_result(theta, b.contract(theta, None), {}, float(len(SYNTHETIC_RESULTS)))
        result.update(driver_sha256=ctx.pins['driver']['sha256'], call_spec_sha256=call['spec']['sha256'])
    rp = P.put(Path(outdir)/'result.json', result)
    SYNTHETIC_RESULTS[call['name']] = rp
    pins = {key: ctx.pins[key] for key in ('driver', 'monitor')}
    pins['spec'] = call['spec']
    launch = {'schema': M.MONITOR_SCHEMA+'_LAUNCH', 'utc': start, 'child_pid': 900004,
              'pins': pins, 'caps': caps, 'outdir': outdir, 'retries_allowed': 0,
              'command': M.driver_command(pins, call['spec'], outdir)}
    lp = P.put(Path(outdir+'.receipt.json.launch.json'), launch)
    receipt = {'schema': M.MONITOR_SCHEMA, 'utc_start': start, 'utc_end': end, 'child_pid': 900004,
               'pins': pins, 'caps': caps, 'status': 'FINISHED', 'driver_status': 'COMPLETED',
               'exit_code': 0, 'result': rp}
    receipt['receipt_sha256'] = M.sha(M.canonical(receipt))
    mp = P.put(Path(outdir+'.receipt.json'), receipt)
    return launch, lp, receipt, mp


P.saved_monitor = saved_monitor
calls = [c for c in ctx.calls() if c['origin']=='P112']
saved = []
for call in calls[:-3]:
    saved.append(P.save_full(ctx, call, legacy_entry=True))
names = sorted(c['name'] for c in calls[-3:])
choice = M.select_workers(ctx, P.forecast(f, calls=names))
assert choice['column_workers'] == 8
for name in names:
    saved.append(P.save_full(ctx, ctx.call(name)))
twin = P.save_twin(ctx)
saved.append(twin)
P.put(Path(cfg['p112_launch_root'])/'outside_set_stop/S0_SEED_SERIAL_A1_CX2V001.json',
      {'schema': 'S0_OUTSIDE_SET_STOP_RECORD_C2V001', 'name': 'S0_SEED_SERIAL',
       'plan_output_primary': plan_pin, 'fdplan': fdplan, 'date_u': DATE, 'synthetic': True})
assembly = M.assemble_registry(ctx)
assert M.assemble_registry(ctx, verify=True)['status'] == 'VERIFIED'
rb.verify_launch_registry = rb._legacy_verify_launch_registry_a253
base_factory = P.consumer_factory(f)
def combined_context_factory(module, config_pin):
    module.SEED_KEY = M.SEED_KEY
    return base_factory(module, config_pin)
rb._registry_context_factory = combined_context_factory
descriptors, others = [], []
for item in saved:
    receipt = M.read_pin(item['receipt'])
    attempt = {'run_dir': receipt['run_dir'], 'receipt': item['receipt']}
    if item['name'] == M.TWIN:
        others.append({'label': M.TWIN, 'attempts': [attempt]})
    else:
        call = ctx.call(item['name'])
        descriptors.append({'alternative': call['alternative'], 'kind': call['kind'],
                            'key': call['key'], 'attempts': [attempt],
                            'result': SYNTHETIC_RESULTS[item['name']], 'cut_record': None})
extra = G.w.p1_extra(calls=descriptors, other_phase_calls=others, launch_registry=assembly['registry'])
d = G.env.dir('cases', 'combined_cw8')
promoted = b.input(d, 'PHASE_1', 'FULL', extra)
doc = t.jload(promoted['path'])
doc['registry_verification'] = {'launcher': ctx.own_pin, 'config': ctx.config_pin,
                                'assembly_record': assembly['assembly_record']}
twin_record = M.read_pin(twin['record'])
lp = twin_record['launch_json']
doc['m15']['launch_receipts'] = [{k: lp[k] for k in ('path', 'sha256')}]
ip = G.fixture.jwrite(WORK/'COMBINED_BUILDER_INPUT.json', doc)
out = G.env.fresh('combined_cw8')
before = len(READS)
b.build(ip, out)
counts = collections.Counter(READS[before:])
assert counts and max(counts.values()) == 1, {p:n for p,n in counts.items() if n>1}
plan = t.jload(os.path.join(out, 'REPLAY_PLAN.json'))
assert plan['registry_verification']['mode'] == 'P112_READ_ONLY_VERIFY'
assert plan['registry_verification']['verdict'] == 'BYTE_EQUAL'
plan_pin = t.pin(os.path.join(out, 'REPLAY_PLAN.json'))
p1, _, _ = t.drive(G.env, b, out, 'PASS_ONE')
pk, _, _ = t.drive(G.env, b, out, 'PASS_K')
p1pin = G.fixture.jwrite(WORK/'pass_one.json', p1)
pkpin = G.fixture.jwrite(WORK/'pass_k.json', pk)
comparison, _, successor = t.step7(G.env, out, plan_pin, p1pin, pkpin)
assert comparison['status'] == 'NO_NEW_DISCREPANCY' and successor is None
pass_input = G.fixture.jwrite(WORK/'pass_input.json', {
    'schema': 'PASS_INPUT_C2V003', 'pass_label': 'PASS_K', 'freeze_module': b.fm_pin,
    'build_record': t.pin(os.path.join(out, 'BUILD_RECORD.json')), 'replay_plan': plan_pin,
    'roster_pins': t.pin(os.path.join(out, 'ROSTER_PINS.json')), 'selection': b.sel,
    'spec': b.spec_pin, 'null_direction_rule': t.NULL_RULE})
input_doc = {'schema': G.g.INPUT_SCHEMA, 'pass_input': pass_input,
    'ledger_head': t.pin(os.path.join(t.ledger_dir(out), 'STEP7_0001.json')), 'slots': b.slots,
    'notes': G.fixture.jwrite(WORK/'notes.json', G.notes),
    'parameter_region': G.fixture.jwrite(WORK/'parameter_region.json', {
        'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS', 'scope': 'synthetic'}),
    'observation_rule': G.fixture.jwrite(WORK/'observation_rule.json', {
        'kind': 'SYNTHETIC_SAVED_RECTANGLES', 'scope': 'not observational data'}),
    'code_files': [], 'input_files': [{'path': str(G.CALIBRATION), 'sha256': G.CALIBRATION_SHA},
                                    {'path': str(G.REGION), 'sha256': G.REGION_SHA}]}
gp = G.fixture.jwrite(WORK/'g26_input.json', input_doc)
G.g.SPEC_SHA256, G.g.SLOTS_SHA256, G.g.QUERY_ROLE = b.spec_pin['sha256'], b.slots['sha256'], 'SYNTHETIC_FIXTURE'
before = len(READS)
frozen = G.g.freeze(rb, gp, str(WORK/'freeze'))
counts = collections.Counter(READS[before:])
assert counts and max(counts.values()) == 1, {p:n for p,n in counts.items() if n>1}
assert frozen['allow_incomplete'] is True and frozen['freeze_status'] == 'FREEZE_INCOMPLETE'
assert frozen['pass_k_byte_equal'] and frozen['dn2_coordinates_equal']
ep = G.fixture.jwrite(WORK/'EVIDENCE.json', {
    'date_u': DATE, 'status': 'TESTED', 'scope': __doc__, 'test': {
        'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    'source_pins': SOURCE_PINS, 'choice': choice, 'assembly': assembly,
    'saved': saved, 'builder_input': ip, 'replay_plan': plan_pin,
    'step7': comparison, 'freeze': frozen, 'legacy_serial_calls': len(members)-3,
    'cw8_full_calls': 3, 'identity_twin_calls': 1, 'registry_verifier_seam': False,
    'other_seams': ['inert source pins, SyntheticSystem and synthetic seed theta-key constant', 'saved completed metadata and synthetic dry verdict',
                    'synthetic freeze spec/slots/node constants and query role'],
    'untested': ['actual science launch', 'actual identity record', 'production timing', 'root adoption']})
print(json.dumps({'status': 'PASS', 'evidence': ep, 'cw8_full': 3, 'legacy_serial': len(members)-3}))
