"""SOURCE ONLY, root executes. Complete read-only input/runtime hash custody.
No worker scientific import, no subprocess or global process inspection.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
PYTHON = '/Applications/Xcode.app/Contents/Developer/usr/bin/python3'
PYTHON_SHA = '6b24be8ba00c4abc8b3e7e2620bd710e2cf7a4312d00c147f8f05fbb6f3d297a'
BOOT = ROOT/'ROOT_RESOURCE_BOOTSTRAP_V001.py'
BOOT_SHA = 'd8effd48d577d33ef311adb834afd04d93dc6fc725f2285affc00574577a4b24'
SUP = ROOT/'ROOT_BACKEND_WARNING_SUPERVISOR_V001.py'
SUP_SHA = '846263fa48955c36bffa263d86e050f14b80444d8713b5c1f2ad525c3789cadb'
OLD_SPEC = ROOT/'P49_SPECTRAL_NATIVE_SPEC_V002.json'
OLD_SPEC_SHA = 'f35fe4c7345653603b51a5c63d541a1336b46bfe7b486d67f9b3247c1a058473'
OLD_INVENTORY = ROOT/'P49_SPECTRAL_NATIVE_OUTPUT_V001/RUNTIME_INVENTORY.json'
OLD_INVENTORY_SHA = '15c58a7a33919ad74be318a7ec40a7aa450528d9b740b0ea61df123224e3aead'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def exact(a, b, name):
    need(type(a) is type(b), 'typed '+name)
    if isinstance(b, dict):
        need(a.keys() == b.keys(), 'whole keys '+name)
        for k in b:
            exact(a[k], b[k], name+'/'+k)
    elif isinstance(b, list):
        need(len(a) == len(b), 'whole array '+name)
        for i in range(len(b)):
            exact(a[i], b[i], name+'/'+str(i))
    else:
        need(a == b, 'exact '+name)


def decode(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'duplicate JSON field')
            out[k] = v
        return out
    def bad(v):
        raise ValueError('nonfinite JSON '+v)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


class Inputs:
    def __init__(self, guard):
        self.guard, self.pins, self.aliases = guard, {}, set()

    def read(self, path, sha=None, cap=2*2**30, retain=True, alias=False):
        p = Path(path)
        need(p.is_absolute() and (alias or p.resolve() == p) and (alias or not p.is_symlink())
             and p.is_file() and p.stat().st_size <= cap, 'plain bounded input '+str(p))
        h, count, blocks = hashlib.sha256(), 0, []
        with p.open('rb') as stream:
            while True:
                data = stream.read(1 << 20)
                if not data:
                    break
                count += len(data)
                need(count <= cap, 'bounded actual input')
                h.update(data)
                if retain:
                    blocks.append(data)
                self.guard()
        actual = {'path': str(p), 'sha256': h.hexdigest(), 'bytes': count}
        need(sha is None or actual['sha256'] == sha, 'complete opening hash '+str(p))
        if str(p) in self.pins:
            exact(actual, self.pins[str(p)], 'unchanged repeat input')
        self.pins[str(p)] = actual
        if alias:
            self.aliases.add(str(p))
        return b''.join(blocks) if retain else actual

    def pin(self, pin, retain=True, cap=2*2**30):
        need(set(pin) in ({'path', 'sha256'}, {'path', 'sha256', 'bytes'}), 'literal pin fields')
        result = self.read(pin['path'], pin['sha256'], cap, retain)
        if 'bytes' in pin:
            need(self.pins[pin['path']]['bytes'] == pin['bytes'], 'literal complete bytecount')
        return result

    def close(self):
        for p, pin in list(self.pins.items()):
            self.read(p, pin['sha256'], max(pin['bytes'], 1), False, p in self.aliases)


def usage(value, ceiling):
    need(set(value) == {'rss_peak_bytes', 'user_seconds', 'system_seconds'}, 'complete usage fields')
    need(type(value['rss_peak_bytes']) is int and 0 < value['rss_peak_bytes'] <= ceiling, 'owned RSS envelope')
    for k in ('user_seconds', 'system_seconds'):
        need(type(value[k]) in (int, float) and math.isfinite(value[k]) and value[k] >= 0, 'finite owned CPU usage')


def runtime(I, spec_pin, jobdir, archive, config_pin, worker, worker_sha, pid, payload_bytes):
    """Whole new diagnostic runtime files, exact spec/source/dependency closure.
    Root's earlier C153 whole original namespaces remain a separate obligation.
    """
    old_spec = decode(I.read(OLD_SPEC, OLD_SPEC_SHA, 2*2**20))
    old = decode(I.read(OLD_INVENTORY, OLD_INVENTORY_SHA, 65536))
    spec = decode(I.pin(spec_pin, cap=2*2**20))
    need(Path(spec_pin['path']).parent == ROOT and spec['role'] == 'P49_BACKEND_WARNING_DIAGNOSTIC_V001'
         and spec['bootstrap'] == str(BOOT) and spec['bootstrap_sha256'] == BOOT_SHA
         and spec['interpreter_sha256'] == PYTHON_SHA and spec['pool_lock'] == str(ROOT/'ROOT_POOL.lock'), 'frozen original warning runtime role')
    exact(spec['dependency_files'], old_spec['dependency_files'], 'all499 native dependencies')
    need(len(spec['dependency_files']) == 499 and len(spec['jobs']) == 1, 'whole dependency and one-job census')
    I.read(PYTHON, PYTHON_SHA, 64*2**20, False, True)
    I.read(BOOT, BOOT_SHA, 65536)
    I.read(SUP, SUP_SHA, 65536)
    for pin in spec['dependency_files']:
        I.pin(pin, False)
    gate = decode(I.pin(spec['source_gate'], cap=2*2**20))
    need(Path(spec['source_gate']['path']).parent == ROOT and gate['acceptor'] == '/root'
         and str(gate['status']).startswith('PASS') and gate['role'] == spec['role'], 'root original role source release')
    matches = [r for r in gate['allowed_runners'] if r['path'] == str(worker)
               and r['sha256'] == worker_sha and r['role'] == 'diagnostic']
    need(len(matches) == 1 and matches[0]['source_author'] != matches[0]['reviewer_id'], 'distinct actual worker source gate')
    jobdir = Path(jobdir)
    need(jobdir.is_absolute() and jobdir.resolve() == jobdir and not jobdir.is_symlink()
         and ROOT in jobdir.parents and jobdir.is_dir(), 'literal original producer runtime directory')
    j = spec['jobs'][0]
    exact(j, {'id': jobdir.name, 'native_role': 'diagnostic', 'runner': str(worker), 'runner_sha256': worker_sha,
              'args': ['--config', config_pin['path'], '--config-sha256', config_pin['sha256'], '--output', str(archive)],
              'output_path': str(archive), 'memory_bytes': 8*2**30, 'wall_seconds': 300, 'output_bytes_cap': 128*2**20,
              'dependency_roots': ['/Users/bgm/Library/Python/3.9/lib/python/site-packages']}, 'literal complete diagnostic job')
    names = {'JOB.json', 'CHILD_START.json', 'CHILD_FINISH.json', 'SUPERVISOR_RESULT.json', 'stdout.log', 'stderr.log'}
    need({p.name for p in jobdir.iterdir()} == names, 'complete original six runtime files')
    raw = {name: I.read(jobdir/name, cap=16*2**20) for name in names}
    values = {k: decode(v) for k, v in raw.items() if k.endswith('.json')}
    exact(values['JOB.json'], dict(j, telemetry_dir=str(jobdir)), 'JOB')
    start, end, result = (values[k] for k in ('CHILD_START.json', 'CHILD_FINISH.json', 'SUPERVISOR_RESULT.json'))
    need(set(start) == {'pid', 'python', 'scope', 'rss_peak_bytes', 'user_seconds', 'system_seconds'}
         and start['pid'] == pid and start['python'] == PYTHON and start['scope'] == 'OWNED_PROCESS_ONLY', 'actual child PID and interpreter')
    usage({k: start[k] for k in ('rss_peak_bytes', 'user_seconds', 'system_seconds')}, 8*2**30)
    need(set(end) == {'exit_code', 'rss_peak_bytes', 'user_seconds', 'system_seconds'} and end['exit_code'] == 0, 'actual child success')
    usage({k: end[k] for k in ('rss_peak_bytes', 'user_seconds', 'system_seconds')}, 8*2**30)
    need(type(result['wall_seconds']) in (int, float) and 0 <= result['wall_seconds'] <= 300, 'whole elapsed cap')
    exact(result, {'id': jobdir.name, 'pid': pid, 'status': 'EXITED', 'exit_code': 0,
                  'wall_seconds': result['wall_seconds'], 'child_usage': end, 'memory_breach': False,
                  'output_breach': False, 'final_output_bytes': payload_bytes+sum(len(v) for k, v in raw.items() if k != 'SUPERVISOR_RESULT.json'),
                  'complete_success': True}, 'original supervisor actual result')
    need(payload_bytes+sum(map(len, raw.values())) <= 128*2**20, 'whole final scientific and owned runtime bytes')
    parent = jobdir.parent
    need({p.name for p in parent.iterdir()} == {'START.json', 'FINISH.json', 'SPEC_SNAPSHOT.json', jobdir.name}, 'entire original supervisor wave census')
    parentraw = {k: I.read(parent/k, cap=2*2**20) for k in ('START.json', 'FINISH.json', 'SPEC_SNAPSHOT.json')}
    exact(decode(parentraw['SPEC_SNAPSHOT.json']), spec, 'full original spec snapshot')
    ps, pf = decode(parentraw['START.json']), decode(parentraw['FINISH.json'])
    need(type(ps['utc']) is str and type(pf['utc']) is str, 'original UTC telemetry')
    exact(ps, {'utc': ps['utc'], 'spec_sha256': spec_pin['sha256'], 'supervisor_sha256': SUP_SHA,
               'python': PYTHON, 'python_version': old['python_version'],
               'memory_policy': 'sampled owned-process peak; overshoot reported, not hard RSS quota',
               'host_process_inventory': 'NOT_AVAILABLE; no host-global load claim'}, 'original parent START')
    aggregate = pf['children_aggregate']
    need(set(aggregate) == {'peak_rss_bytes', 'user_seconds', 'system_seconds'}
         and type(aggregate['peak_rss_bytes']) is int and aggregate['peak_rss_bytes'] >= end['rss_peak_bytes'], 'whole children usage')
    usage({'rss_peak_bytes': aggregate['peak_rss_bytes'], 'user_seconds': aggregate['user_seconds'],
           'system_seconds': aggregate['system_seconds']}, 8*2**30)
    exact(pf, {'utc': pf['utc'], 'jobs': [result], 'children_aggregate': aggregate,
               'aggregate_scope': 'whole supervisor lifetime, not individual parallel job attribution',
               'scientific_acceptance': False}, 'original parent FINISH')
    return old, end, raw['stderr.log'], {'producer_runtime': str(jobdir), 'producer_spec': spec_pin,
            'pid': pid, 'complete_new_producer_runtime_census': True, 'dependency_files': 499,
            'original_C153_namespace_closure_checked_here': False}


def inventory_checks(first, final, original, pid, child_end):
    need(set(final) == {'inventory', 'survey'}, 'complete closing inventory/survey')
    last = final['inventory']
    for value in (first, last):
        need(set(value) == set(original) and value['pid'] == pid, 'whole owned inventory keys/PID')
        for k in ('python_literal', 'python_canonical', 'python_version', 'uname', 'numpy_version',
                  'numpy_module_path', 'numpy_build_config', 'thread_environment', 'scope'):
            exact(value[k], original[k], 'same qualified environment/'+k)
        need(value['numpy_version'] == '2.0.2' and all(v == '1' for v in value['thread_environment'].values()), 'fixed NumPy/thread requests')
        images = value['own_loaded_images']
        need(type(images) is list and 0 < len(images) <= 4096
             and all(type(p) is str and p.startswith('/') for p in images), 'entire recorded own image census syntax')
        need(any('Accelerate' in p for p in images), 'recorded original backend loaded')
        usage(value['own_usage'], child_end['rss_peak_bytes'])
    survey = final['survey']
    need(set(survey) == {'samples', 'sample_seconds_requested', 'owned_peak_thread_count_sampled', 'thread_scope',
                        'initial_usage', 'final_usage', 'elapsed_seconds', 'hard_RSS_storage_core_quota_claim',
                        'external_parent_timeout_and_RSS_storage_monitor_required'}, 'entire finished own survey')
    need(type(survey['samples']) is int and survey['samples'] >= 2
         and type(survey['owned_peak_thread_count_sampled']) is int and survey['owned_peak_thread_count_sampled'] >= 1,
         'actual owned telemetry sample census')
    exact(survey['sample_seconds_requested'], 0.05, 'sampling request')
    exact(survey['thread_scope'], 'ALL_OWN_THREADS_INCLUDING_MONITORS_NOT_NUMBER_OF_ACTIVE_BLAS_CORES', 'owned thread scope')
    need(survey['hard_RSS_storage_core_quota_claim'] is False
         and survey['external_parent_timeout_and_RSS_storage_monitor_required'] is True
         and 0 <= survey['elapsed_seconds'] <= 300, 'actual scope and bounded survey interval')
    for field in ('initial_usage', 'final_usage'):
        usage(survey[field], child_end['rss_peak_bytes'])
    for key in ('rss_peak_bytes', 'user_seconds', 'system_seconds'):
        sequence = [survey['initial_usage'][key], first['own_usage'][key], last['own_usage'][key],
                    survey['final_usage'][key], child_end[key]]
        need(sequence == sorted(sequence), 'monotone complete own usage chain')
