"""Run the one frozen exact-algebra child under the existing resource monitor.

No source editing, physics imports, implicit retry or scientific parameter change.
This supervisor's own source and the complete child freeze are bound in its
exclusive intent; raw process streams and any child result survive failure.
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
THIS = J/'native_finite_gap_formation_exact_supervisor_v001.py'
CHILD = J/'native_finite_gap_formation_exact_v001.py'
FREEZE = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_FROZEN.json'
CHILD_RESULT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_RESULTS.json'
CHILD_INTENT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_INTENT.json'
INTENT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_RUN_INTENT.json'
RESULT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_RUN.json'
MONITOR = K/'class_candidate_supervisor_v006.py'
PUBLISHER = J/'run_scientific_case_v001.py'
ENV_SOURCE = K/'CLASS_CANDIDATE_COMPILER_ARGV_V006.json'
PYTHON = Path('/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
PINS = {
    CHILD: '76d7dcaa34d57545433112648301ba3b996ac2bdd96d39b4d99635c0d2480d73',
    J/'NATIVE_FINITE_GAP_FORMATION_V001.md': '97b3f79ce25fca071a1b80dbac4667345457f7ea93305d617dcb3cd9a59658eb',
    J/'NATIVE_FINITE_GAP_FORMATION_EXACT_PROTOCOL_V001.md': '9f71a3b154def99bd255bf4297ed3698a16de80a8e4fea5dc042df7ad81ff639',
    MONITOR: 'd88f84a3a8fa3187ff1dd128bc2e18c3606830d54966789a3ab96c619c2f7778',
    PUBLISHER: 'f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8',
    ENV_SOURCE: 'ab8f3dddd2663864e1d5957f3a36341e657d737110f3bc377da566f2b61732bd',
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def enc(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    path = Path(path)
    need(path.resolve() == path and path.is_relative_to(ROOT), 'Noncanonical input')
    return path.read_bytes()

def art(path):
    raw = read(path)
    return dict(path=str(path), bytes=len(raw), sha256=sha(raw))

def main():
    need(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == THIS,
         'Fixed workspace and supervisor source')
    need(sys.argv[1:] == ['run'], 'One explicit run only')
    for path in (INTENT, RESULT, CHILD_INTENT, CHILD_RESULT):
        need(not path.exists() and not path.is_symlink(), 'No retry or overwrite')
    for path, digest in PINS.items():
        need(sha(read(path)) == digest, 'Changed reviewed source '+str(path))
    frozen = json.loads(read(FREEZE))
    files = dict(frozen['files'])
    files.update({str(p): h for p, h in PINS.items()})
    files[str(FREEZE)] = sha(read(FREEZE))
    files[str(THIS)] = sha(read(THIS))
    for path, digest in files.items():
        need(sha(read(path)) == digest, 'Changed frozen input '+path)
    config = frozen['config']
    need(config['external_wall_seconds'] == 10 and
         config['external_sampled_rss_bytes'] == 268435456, 'Changed external limits')
    monitor = runpy.run_path(str(MONITOR), run_name='finite_gap_monitor_only')
    publisher = runpy.run_path(str(PUBLISHER), run_name='finite_gap_publisher_only')
    monitor['CONFIG'].update(smoke_wall_seconds=10., smoke_sampled_rss_bytes=268435456)
    env_source = json.loads(read(ENV_SOURCE))
    argv = [str(PYTHON), '-B', str(CHILD), 'run']
    publisher['publish'](enc(dict(schema='NATIVE_FINITE_GAP_EXACT_RUN_INTENT_V001',
        files=files, argv=argv, child_result=str(CHILD_RESULT),
        wall_seconds=10, sampled_rss_bytes=268435456))+b'\n', INTENT)
    output = dict(status='EXACT_CHILD_OR_MONITOR_FAILED_RETAINED', intent=art(INTENT),
                  physical_qualification=False, Stage3_complete=False)
    try:
        invocation, stdout = monitor['invoke'](argv, env_source)
        output['invocation'] = invocation
        if CHILD_RESULT.is_file() and not CHILD_RESULT.is_symlink():
            output['child_result'] = art(CHILD_RESULT)
        need(invocation['returncode'] == 0 and invocation['exception'] is None and
             invocation['stop_reason'] is None and not invocation['resource_monitor_errors']
             and invocation['stderr_bytes'] == 0, 'Unclean monitored child')
        need(len(stdout) <= 1048576, 'Bounded child stdout')
        child = json.loads(read(CHILD_RESULT))
        need(child['freeze_sha256'] == files[str(FREEZE)] and
             child['payload_sha256'] == sha(enc(child['payload'])), 'Child receipt identity')
        need(child['payload']['intent'] == art(CHILD_INTENT), 'Child intent binding')
        need(child['payload']['status'] ==
             'EXACT_POLYNOMIAL_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION', 'Child failed')
        report = json.loads(stdout)
        need(report == dict(**art(CHILD_RESULT), status=child['payload']['status']),
             'Captured child publication differs')
        for path, digest in files.items():
            need(sha(read(path)) == digest, 'Changed end input '+path)
        output['status'] = 'EXACT_CHILD_AND_MONITOR_COMPLETE'
    except BaseException:
        output['error'] = traceback.format_exc()
    publisher['publish'](enc(dict(schema='NATIVE_FINITE_GAP_EXACT_RUN_RECEIPT_V001',
        payload_sha256=sha(enc(output)), payload=output))+b'\n', RESULT)
    print(enc(dict(**art(RESULT), status=output['status'])).decode())
    return int(output['status'] != 'EXACT_CHILD_AND_MONITOR_COMPLETE')

if __name__ == '__main__':
    sys.exit(main())
