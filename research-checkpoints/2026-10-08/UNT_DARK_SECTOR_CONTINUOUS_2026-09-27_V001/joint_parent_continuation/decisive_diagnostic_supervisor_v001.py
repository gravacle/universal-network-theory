"""Root-only one-child capture wrapper for two independently frozen diagnostics.

Exactly one named lane per invocation; no queue, retries, scientific imports,
compilation or changed scientific criteria. An intent precedes child launch.
"""
import hashlib
import json
from pathlib import Path
import runpy
import sys
import traceback

sys.dont_write_bytecode = True
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
K = J/'class_candidate_v001'
THIS = J/'decisive_diagnostic_supervisor_v001.py'
MONITOR = K/'class_candidate_supervisor_v006.py'
PUBLISHER = J/'run_scientific_case_v001.py'
ENV_SOURCE = K/'CLASS_CANDIDATE_COMPILER_ARGV_V006.json'
PYTHON = Path('/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
PINS = {
    MONITOR: 'd88f84a3a8fa3187ff1dd128bc2e18c3606830d54966789a3ab96c619c2f7778',
    PUBLISHER: 'f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8',
    ENV_SOURCE: 'ab8f3dddd2663864e1d5957f3a36341e657d737110f3bc377da566f2b61732bd',
}
LANES = {
    'native': dict(directory=J, stem='NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001',
        source='native_finite_fragment_source_exact_v001.py',
        source_sha='e701bcfec5328caa2a32e30b1dcc1e17c86c6e7e5e047a55aa64942292b575e9',
        protocol='NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_PROTOCOL_V001.md',
        protocol_sha='e3932a026d963527150b68d6e439d8e5e922ddc8f3ef95e83f385d2b9a25c17f',
        argument='run', wall=45,
        expected='EXACT_SOURCE_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION'),
    'thermal': dict(directory=K, stem='CLASS_THERMAL_SAVED_TRANSITION_AUDIT_V001',
        source='class_thermal_saved_transition_audit_v001.py',
        source_sha='25f0381e2c5e5833dd40f12458831c0fceddbb0de8a3fa1e24259686f128358e',
        protocol='CLASS_THERMAL_SAVED_TRANSITION_AUDIT_PROTOCOL_V001.md',
        protocol_sha='8850f8ea9ea34a10d85521d9010227377eda9d5268101c06fb3f4bf6e057044a',
        argument='--run', wall=15,
        expected='SAVED_ALL_EXISTING_TRANSITIONS_AUDIT_COMPLETE_NOT_QUALIFIED'),
}

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def enc(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    p = Path(path)
    need(p.resolve() == p and p.is_relative_to(ROOT), 'Canonical project input')
    need(p.stat().st_size <= 33554432, 'Bounded file input')
    return p.read_bytes()

def art(path):
    b = read(path)
    return dict(path=str(path), bytes=len(b), sha256=sha(b))

def main():
    need(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == THIS, 'Fixed source/workspace')
    need(len(sys.argv) == 2 and sys.argv[1] in LANES, 'Exactly one explicit lane')
    lane = sys.argv[1]; spec = LANES[lane]; directory = spec['directory']; stem = spec['stem']
    child = directory/spec['source']; protocol = directory/spec['protocol']
    freeze = directory/(stem+'_FROZEN.json'); child_result = directory/(stem+'_RESULTS.json')
    child_intent = directory/(stem+'_INTENT.json'); intent = directory/(stem+'_RUN_INTENT.json')
    result = directory/(stem+'_RUN.json')
    for p in (intent, result, child_intent, child_result):
        need(not p.exists() and not p.is_symlink(), 'No retry or overwrite')
    pins = dict(PINS); pins.update({child: spec['source_sha'], protocol: spec['protocol_sha']})
    for p, h in pins.items():
        need(sha(read(p)) == h, 'Changed reviewed source '+str(p))
    frozen = json.loads(read(freeze))
    files = dict(frozen['files']) if lane == 'native' else {p: a['sha256'] for p, a in frozen['sources'].items()}
    files.update({str(p): h for p, h in pins.items()})
    files[str(freeze)] = sha(read(freeze)); files[str(THIS)] = sha(read(THIS))
    for p, h in files.items():
        need(sha(read(p)) == h, 'Changed frozen input '+p)
    if lane == 'native':
        need(frozen['config']['external_wall_seconds'] == spec['wall'] and
             frozen['config']['external_sampled_rss_bytes'] == 268435456, 'Unchanged native caps')
    else:
        need(frozen['limits']['wall_seconds'] == spec['wall'] and
             frozen['limits']['self_rss_bytes'] == 268435456, 'Unchanged audit caps')
    monitor = runpy.run_path(str(MONITOR), run_name='diagnostic_monitor_only')
    publisher = runpy.run_path(str(PUBLISHER), run_name='diagnostic_publisher_only')
    monitor['CONFIG'].update(smoke_wall_seconds=float(spec['wall']), smoke_sampled_rss_bytes=268435456)
    argv = [str(PYTHON), '-B', str(child), spec['argument']]
    publisher['publish'](enc(dict(schema='DECISIVE_DIAGNOSTIC_RUN_INTENT_V001', lane=lane,
        files=files, argv=argv, child_result=str(child_result), expected_status=spec['expected'],
        wall_seconds=spec['wall'], sampled_rss_bytes=268435456,
        monitor_caveat='0.25 second samples, 5 second termination grace; not an unsampled-memory guarantee'))+b'\n', intent)
    output = dict(status='DIAGNOSTIC_CHILD_OR_MONITOR_FAILED_RETAINED', lane=lane, intent=art(intent),
                  physical_qualification=False, thermal_qualified=False, propagation_allowed=False, Stage3_complete=False)
    try:
        invocation, stdout = monitor['invoke'](argv, json.loads(read(ENV_SOURCE)))
        output['invocation'] = invocation
        if child_result.is_file() and not child_result.is_symlink():
            output['child_result'] = art(child_result)
        need(invocation['returncode'] == 0 and invocation['exception'] is None and
             invocation['stop_reason'] is None and not invocation['resource_monitor_errors'] and
             invocation['stderr_bytes'] == 0, 'Unclean monitored child')
        need(len(stdout) <= 1048576, 'Bounded child stdout')
        w = json.loads(read(child_result)); p = w['payload']
        need(w['freeze_sha256'] == files[str(freeze)] and w['payload_sha256'] == sha(enc(p)), 'Child custody')
        need(p['intent'] == art(child_intent) and p['status'] == spec['expected'], 'Child status/intent')
        need(json.loads(stdout) == dict(**art(child_result), status=p['status']), 'Raw child publication')
        for name, h in files.items():
            need(sha(read(name)) == h, 'Changed end input '+name)
        output['status'] = 'DIAGNOSTIC_CHILD_AND_MONITOR_COMPLETE'
    except BaseException:
        output['error'] = traceback.format_exc()
    publisher['publish'](enc(dict(schema='DECISIVE_DIAGNOSTIC_RUN_RECEIPT_V001',
        payload_sha256=sha(enc(output)), payload=output))+b'\n', result)
    print(enc(dict(**art(result), status=output['status'])).decode())
    return int(output['status'] != 'DIAGNOSTIC_CHILD_AND_MONITOR_COMPLETE')

if __name__ == '__main__':
    sys.exit(main())
