"""Bounded serial custody wrapper for exactly two new exploratory cases.

No numerical solver import. Reuse only pinned publication/resource definitions;
never invoke an ancestral main, snapshot, science freeze or case runner.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'spherical_consistent_two_current_supervisor_v001.py'
SOURCE = J/'spherical_consistent_two_current_v001.py'
PROTOCOL = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_PROTOCOL_V001.md'
SCIENCE_FREEZE = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_FROZEN.json'
CONTROL_FREEZE = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_SUPERVISOR_V001_FROZEN.json'
FREEZE_INTENT = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_FREEZE_INTENT.json'
FREEZE_RUN = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_FREEZE_RUN.json'
SERIAL_INTENT = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_SERIAL_INTENT.json'
SERIAL_RESULT = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_SERIAL_RESULT.json'
PUBLISHER = J/'run_scientific_case_v001.py'
MONITOR = J/'spherical_two_current_supervisor_v001.py'
PINS = {
    SOURCE.name: 'a4f0546b1a3082e1eab46adfb9f942353459079830c58188c59a42ad77ff22b0',
    PUBLISHER.name: 'f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8',
    MONITOR.name: '5629874875219900e121a6c907d8b3baad26cf08f7c2e0671223e15f1f31ef3c',
}
CONFIG = dict(wall_seconds=180., sampled_process_group_rss_bytes=536870912,
              sample_seconds=.2, terminate_grace_seconds=3., cases=2,
              serial_wall_seconds=390., maximum_stdout_bytes=16777217,
              maximum_stderr_bytes=1048576, maximum_receipt_bytes=33554432,
              resource_bounds_are_sampled=True)
CASES = [dict(case_index=i, gap=gap, L=8., dx=1/16, cells=128)
         for i, gap in enumerate((128, 8192))]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def enc(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def checked(path, expected=None):
    path.relative_to(ROOT)
    for p in (path, *path.parents):
        if p == ROOT.parent:
            break
        if p.is_symlink():
            raise RuntimeError('Linked input refused')
    raw = path.read_bytes()
    if expected is not None and sha(raw) != expected:
        raise RuntimeError('Changed source '+str(path))
    return raw


def helpers():
    if Path.cwd().resolve() != ROOT or Path(__file__).resolve() != THIS or sys.platform != 'darwin':
        raise RuntimeError('Fixed project/source/Mac required')
    sys.dont_write_bytecode = True
    for path in (PUBLISHER, MONITOR):
        checked(path, PINS[path.name])
    publication = runpy.run_path(str(PUBLISHER), run_name='owned_publication_definitions_only')
    monitor = runpy.run_path(str(MONITOR), run_name='owned_resource_definitions_only')
    # Function globals refer to this exact CONFIG object; update, do not replace.
    monitor['CONFIG'].update({k:CONFIG[k] for k in ('wall_seconds', 'sampled_process_group_rss_bytes',
                                                 'sample_seconds', 'terminate_grace_seconds')})
    return publication['bound'], publication['publish'], monitor['invoke']


def controller_snapshot():
    files = {str((J/name).relative_to(ROOT)):sha(checked(J/name, digest)) for name, digest in PINS.items()}
    files.update({str(p.relative_to(ROOT)):sha(checked(p)) for p in (THIS, PROTOCOL)})
    python = Path(sys.executable).resolve(strict=True)
    return dict(schema='SPHERICAL_CONSISTENT_TWO_CURRENT_CONTROLLER_V001', files=files, config=CONFIG,
                cases=CASES, python=dict(path=str(python), sha256=sha(python.read_bytes()), version=sys.version))


def absent(bound, paths):
    for path in paths:
        bound(path)
        if path.exists() or path.is_symlink():
            raise RuntimeError('No overwrite or automatic retry: '+str(path))


def save(publish, path, payload, freeze_sha=None):
    raw = enc(dict(schema='SPHERICAL_CONSISTENT_TWO_CURRENT_CUSTODY_V001', freeze_sha256=freeze_sha,
                   payload_sha256=sha(enc(payload)), payload=payload))+b'\n'
    if len(raw) > CONFIG['maximum_receipt_bytes']:
        raise RuntimeError('Receipt byte bound')
    publish(raw, path)
    if checked(path) != raw:
        raise RuntimeError('Published receipt differs')
    return sha(raw)


def authenticate_science(raw):
    frozen = json.loads(raw)
    if frozen.get('schema') != 'SPHERICAL_CONSISTENT_TWO_CURRENT_FREEZE_V001' or frozen.get('cases') != CASES:
        raise RuntimeError('New freeze schema/census differs')
    if not isinstance(frozen.get('files'), dict) or len(frozen['files']) > 220:
        raise RuntimeError('Invalid frozen custody census')
    for name, digest in frozen['files'].items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Invalid frozen member')
        checked(ROOT/rel, digest)
    for path in (SOURCE, THIS, PROTOCOL):
        if frozen['files'].get(str(path.relative_to(ROOT))) != sha(checked(path)):
            raise RuntimeError('Missing new source identity')
    enc(frozen)
    return frozen


def invoke_checked(invoke, argv):
    rec, raw = invoke(argv)
    # These limits validate completed capture, not a claim of instantaneous pipe
    # monitoring. The child bounds JSON output; the parent samples group RSS.
    if rec['stdout_bytes'] > CONFIG['maximum_stdout_bytes'] or rec['stderr_bytes'] > CONFIG['maximum_stderr_bytes']:
        rec['stop_reason'] = rec['stop_reason'] or 'CAPTURE_BYTE_BOUND_EXCEEDED'
    return rec, raw


def clean_invocation(rec):
    return (rec['returncode'] in (0, 2) and rec['exception'] is None and rec['stop_reason'] is None
            and not rec['resource_monitor_errors'])


def case_paths(i):
    stem = 'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_CASE_'+format(i, '03d')
    return J/(stem+'_INTENT.json'), J/(stem+'_RUN.json'), J/(stem+'.json')


def main():
    bound, publish, invoke = helpers(); inputs = controller_snapshot(); args = sys.argv[1:]
    if args == ['freeze']:
        absent(bound, (FREEZE_INTENT, FREEZE_RUN, SCIENCE_FREEZE, CONTROL_FREEZE))
        argv = [inputs['python']['path'], '-B', str(SOURCE), 'freeze']
        save(publish, FREEZE_INTENT, dict(status='INTENT_NO_RETRY', controller_inputs=inputs, argv=argv))
        rec, raw = invoke_checked(invoke, argv); error = None
        try:
            if not clean_invocation(rec) or rec['returncode'] != 0:
                raise RuntimeError('New freeze invocation failed')
            authenticate_science(raw)
            if controller_snapshot() != inputs:
                raise RuntimeError('Controller inputs changed during freeze')
        except BaseException:
            error = traceback.format_exc()
        receipt_sha = save(publish, FREEZE_RUN, dict(status='FREEZE_COMPLETE' if error is None else 'FREEZE_FAILED_RETAINED',
            controller_inputs=inputs, invocation=rec, validation_error=error))
        if error is None:
            publish(raw, SCIENCE_FREEZE)
            publish(enc(dict(controller_inputs=inputs, producer_freeze_sha256=sha(raw),
                             freeze_receipt_sha256=receipt_sha))+b'\n', CONTROL_FREEZE)
        print(enc(dict(freeze_complete=error is None, receipt=str(FREEZE_RUN), sha256=receipt_sha)).decode())
        return 0 if error is None else 2
    if args != ['run-all']:
        raise RuntimeError('Use freeze or run-all; no parallel case entry point')
    c_raw = checked(CONTROL_FREEZE); control = json.loads(c_raw); control_sha = sha(c_raw)
    if control['controller_inputs'] != inputs or sha(checked(FREEZE_RUN)) != control['freeze_receipt_sha256']:
        raise RuntimeError('Controller freeze or its capture differs')
    f_raw = checked(SCIENCE_FREEZE); f_sha = sha(f_raw)
    if f_sha != control['producer_freeze_sha256']:
        raise RuntimeError('Science freeze differs')
    authenticate_science(f_raw)
    absent(bound, (SERIAL_INTENT, SERIAL_RESULT, *[p for i in range(2) for p in case_paths(i)]))
    save(publish, SERIAL_INTENT, dict(status='SERIAL_INTENT_NO_RETRY', cases=CASES,
        producer_freeze_sha256=f_sha, controller_inputs=inputs), control_sha)
    started = time.monotonic(); completed = []
    for i in range(2):
        if time.monotonic()-started >= CONFIG['serial_wall_seconds']:
            break
        intent, receipt, output = case_paths(i)
        argv = [inputs['python']['path'], '-B', str(SOURCE), 'run-case', str(i)]
        save(publish, intent, dict(status='INTENT_NO_RETRY', case=CASES[i], argv=argv,
                                  producer_freeze_sha256=f_sha), control_sha)
        rec, raw = invoke_checked(invoke, argv); error = None; science = None; valid = False
        try:
            wrapper = json.loads(raw); science = wrapper['payload']; enc(science)
            if wrapper['freeze_sha256'] != f_sha or wrapper['payload_sha256'] != sha(enc(science)) or science['case'] != CASES[i]:
                raise RuntimeError('Case/payload/freeze binding differs')
            if not isinstance(science['status'], str) or not isinstance(science['failures'], list):
                raise RuntimeError('Case receipt schema differs')
            authenticate_science(f_raw)
            if checked(SCIENCE_FREEZE) != f_raw or checked(CONTROL_FREEZE) != c_raw or controller_snapshot() != inputs:
                raise RuntimeError('Custody changed during case')
            valid = True
        except BaseException:
            error = traceback.format_exc()
        passed = bool(valid and clean_invocation(rec) and rec['returncode'] == 0
                      and science['status'] == 'COMPLETE_EXPLORATORY_NUMERICAL_CASE'
                      and science.get('custody_end_verified') and not science['failures'])
        payload = dict(status='EXPLORATORY_CASE_CHECKS_PASSED' if passed else 'CASE_FAILURE_OR_INCOMPLETE_RETAINED',
            case=CASES[i], invocation=rec, validation_error=error, valid_scientific_output=valid,
            scientific_status=None if science is None else science.get('status'),
            scientific_failures=None if science is None else science.get('failures'),
            raw_output_path=str(output) if valid else None, numerical_checks_passed=passed)
        receipt_sha = save(publish, receipt, payload, control_sha)
        if valid:
            publish(raw, output)  # Valid failed science is preserved, not filtered.
        completed.append(dict(case_index=i, receipt=str(receipt), receipt_sha256=receipt_sha,
                              raw_sha256=sha(raw), passed=passed, valid_scientific_output=valid))
        print(enc(completed[-1]).decode(), flush=True)
    passed = len(completed) == 2 and all(r['passed'] for r in completed)
    save(publish, SERIAL_RESULT, dict(status='TWO_EXPLORATORY_CASES_CHECKED' if passed else 'FAILURES_OR_INCOMPLETE_RETAINED',
        cases=completed, seconds=time.monotonic()-started, all_numerical_checks_passed=passed,
        physical_or_continuum_qualification=False, mandatory_lanes_open=11), control_sha)
    return 0 if passed else 2


if __name__ == '__main__':
    sys.exit(main())
