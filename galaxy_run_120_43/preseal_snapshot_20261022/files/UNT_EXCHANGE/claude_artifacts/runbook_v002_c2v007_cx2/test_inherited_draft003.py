"""Port the 160 predecessor cases to synthetic c2v007 fixtures.

The old suite's production TSR/compare/N1/node reads are replaced with invented
fixtures. The old flag-only tests exercise _check_tsr_flag; new G7 tests exercise
the support-aware command separately. Registry production is a fixture seam in
these inherited roster tests; dedicated P112 tests exercise the real verifier.
Receipts, monitoring evidence, custody copies, cutoff and M15 records are real
synthetic files and pass through the c2v007 validators.
"""

import _strptime
import inspect
import numbers
import collections
import contextlib
import copy
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import traceback
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
PARENT = ART / 'runbook_v002_c2/test_runbook_v002_c2v006.py'
PARENT_SHA = '88d79035bab8f78131a44d4f03cd209b85ca9245799d3e489441deee5d31268e'
BUILDER = HERE / 'roster_builder_c2v007_draft003.py'
BUILDER_SHA = '585dd5c41e267447e7c92e70137f797abf5894c11ad534ae6d93eddd27a4e2e1'
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
raw = PARENT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == PARENT_SHA
source = raw.decode().replace('env.rb.tsr_check(', 'env.rb._check_tsr_flag(')
t = types.ModuleType('inherited_cases')
t.__file__ = str(HERE / 'synthetic_inherited_source.py')
exec(compile(source, str(PARENT), 'exec'), t.__dict__)
t.BUILDER_PATH = str(BUILDER)
assert hashlib.sha256(BUILDER.read_bytes()).hexdigest() == BUILDER_SHA
rb0 = t.load_module(str(BUILDER), 'fixture_constants', BUILDER_SHA)
t.RECEIPT_KEYS = dict(rb0.EXACT_RECEIPT_KEYS)
t.CLASSES = dict(rb0.STATUS_CLASSES)
FIXTURE_LOG = []


def jwrite(path, doc):
    return t.wbytes(str(path), rb0.dump_bytes(doc))


def setup_tsr():
    d = WORK / 'synthetic_tsr'
    d.mkdir()
    exp = dict(rb0.PRODUCTION_TSR)
    radii = [0.5 + k * 0.7 for k in range(30)]
    radii[14:17] = [exp['lower_kpc'], 10.4, exp['upper_kpc']]
    ring = {'ordinal': 15, 'classification': 'TRUNCATION_SHAPE', 'R_kpc': radii[15]}
    compare = jwrite(d / 'compare.json', {
        'failing_TRUNCATION_SHAPE_rings': [ring], 'failing_non_TRUNCATION_SHAPE_rings': []})
    n1 = jwrite(d / 'n1.json', {'ring_radii_kpc': radii})
    node = jwrite(d / 'node.json', {'orders': {'4': {'radii_kpc': radii}}})
    rule = 'Synthetic flags: r(k-1) < R_q < r(k+1), open interval.'
    flags = [{'query_id': q, 'TRUNCATION_SHAPE_RESIDUAL': q in exp['flagged_ids']} for q in exp['all_ids']]
    v1 = jwrite(d / 'flag_v001.json', {
        'schema': rb0.TSR_FLAG_SCHEMA, 'rule_id': rb0.TSR_RULE_ID, 'rule': rule,
        'failing_ring': ring, 'flags': flags, 'pins': {
            'ntest_compare': compare, 'n1_record': n1, 'gl_node_record': node,
            'support_record': {'status': 'PENDING'},
        }})
    v2doc = {'target_free': True, 'rule': rule, 'failing_ring_ordinal': 15,
             'ntest_compare_pin': compare, 'n1_record_pin': n1, 'gl_node_record_pin': node, 'flags': flags}
    v2 = jwrite(d / 'flag_v002.json', v2doc)
    v3 = jwrite(d / 'flag_v003.json', dict(v2doc, schema=rb0.A_TSR_NAME))
    for name, pin in [('TSR_V001', v1), ('TSR_V002', v2), ('TSR_RECORD', v3)]:
        setattr(t, name + '_PATH', pin['path'])
        setattr(t, name + '_SHA', pin['sha256'])
    t.TSR_FILES = {p['path'] for p in (compare, n1, node)}
    exp.update(flag_record_sha256=v3['sha256'], v001_flag_record_sha256=v1['sha256'],
               compare_sha256=compare['sha256'], n1_sha256=n1['sha256'], node_sha256=node['sha256'])
    return exp


EXPECTED_TSR = setup_tsr()
READS = []


def audit(event, args):
    if event == 'subprocess.Popen':
        raise AssertionError('NO_CHILD_PROCESSES_IN_INHERITED_SUITE')
    if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    path = os.path.realpath(os.fsdecode(args[0]))
    if path not in {str(BUILDER), t.V003G_PATH, str(Path(__file__).resolve())} and \
            not path.startswith(str(WORK) + os.sep):
        raise AssertionError('READ_FENCE: ' + path)
    flags = args[2]
    if not isinstance(flags, int) or not flags & (os.O_WRONLY | os.O_RDWR):
        READS.append(path)


sys.addaudithook(audit)
OriginalEnv = t.Env


class Env(OriginalEnv):
    def __init__(self, work):
        super().__init__(work)
        self.allowed |= {str(BUILDER), t.V003G_PATH}
        self.rb.PRODUCTION_TSR = dict(EXPECTED_TSR)
        self.rb.verify_launch_registry = self.synthetic_registry
        self.promoted = {}
        self.owners = {}
        self.by_entry = {}
        self.m15_cache = {}
        self.copy_cache = {}
        self.custody_root = Path(self.dir('custody'))

    def synthetic_registry(self, doc):
        # Producer seam only. The real P112 verify path is tested separately.
        registry, norm = self.rb._launch_registry(doc['launch_registry'], doc['phase'])
        sources = doc['registry_verification']['entries']
        return {
            'mode': 'SYNTHETIC_PRODUCER_FIXTURE',
            'registry': norm, 'sources': sources, 'nonattempts': [],
            's0_member_mappings': [],
            'm15_launch_receipts': [] if doc.get('m15') is None else doc['m15']['launch_receipts'],
        }

    def launch_m15(self, m15):
        if m15 is None:
            return None
        key = t.sha(self.rb.canonical_bytes(m15))
        if key in self.m15_cache:
            return self.m15_cache[key]
        d = Path(self.dir('m15_promoted', key))
        old = t.jload(m15['pre_launch_record']['path'])
        logged = Path(m15['logged_v006_copy']['path']).read_bytes()
        doc = {k: None for k in self.rb.M15_KIT_KEYS}
        doc.update(schema=old.get('schema'), date_u=old.get('date_u'),
                   date_u_epoch_s=self.rb.parse_utc_ns(old.get('date_u'), 'synthetic old M15') // 10**9,
                   v006={'sha256': old.get('v006_sha256'), 'bytes': len(logged)},
                   gate_documents_pinned_in_v006=[
                       {'sha256_from_bytes': h} for h in old.get('gate_document_sha256s', [])])
        launches = []
        for i, pin in enumerate(m15['launch_receipts']):
            launch = t.jload(pin['path'])
            launches.append(jwrite(d / ('launch%d.json' % i),
                                   {'utc': launch.get('receipt_written_utc')}))
        out = {'pre_launch_record': jwrite(d / 'record.json', doc),
               'logged_v006_copy': m15['logged_v006_copy'], 'launch_receipts': launches}
        self.m15_cache[key] = out
        return out

    def promote(self, receipt_pin, run_dir, call, result, ordinal):
        legacy = t.jload(receipt_pin['path'])
        if legacy.get('schema') == 'STEP5_ATTEMPT_RECEIPT_C2V001':
            return receipt_pin
        # Receipt aliases retain the original call; they are never rebound by
        # copying a record to a different call's input.
        owner = self.owners.get(receipt_pin['path'])
        if owner:
            call, native_run, native_result, native_ordinal = owner
            run_dir, result, ordinal = native_run, native_result, native_ordinal
        key = (receipt_pin['path'], receipt_pin['sha256'], json.dumps(call, sort_keys=True), result and result['path'])
        if key in self.promoted:
            return self.promoted[key]
        rd = Path(run_dir)
        sidecar = Path(str(rd) + '.attempt_receipt.json')
        if sidecar.exists():
            # Deliberately malformed repeat input remains bound to the first
            # immutable producer record, so the builder rejects the alias.
            return t.pin(str(sidecar))
        d = Path(self.dir('producer_records', t.sha(repr(key).encode())))
        name = self.rb.TWIN if call['kind'] == 'OTHER' and call['key'] == 'IDENTITY_TWIN_CW8' else (
            'SYN_' + t.sha(self.rb.canonical_bytes(call))[:16].upper())
        call = dict(call, name=name)
        spec_sha = legacy.get('spec_sha256')
        spec = {'path': str(d / 'registered_spec.bin'), 'sha256': spec_sha}
        if isinstance(spec_sha, str):
            # The predecessor's spec_of hashes these synthetic bytes.
            payload = ('SYN-OTHER-SPEC|' + call['key'] if call['kind'] == 'OTHER' else
                       'SYN-SPEC|%s|%s' % (call['alternative'], legacy.get('theta_sha256'))).encode()
            if t.sha(payload) == spec_sha:
                t.wbytes(spec['path'], payload)
        point = legacy.get('theta_sha256')
        entry = jwrite(d / 'entry.json', {
            'schema': 'UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001', **call, 'spec': spec,
            'theta_sha256': point, 'point_key': point})
        self.by_entry[sidecar.as_posix()] = entry
        end = self.rb.parse_utc_ns(legacy.get('receipt_written_utc'), 'legacy fixture time')
        fmt = self.rb.format_utc_ns
        caps = {k: legacy.get(k, default) for k, default in (
            ('rss_cap_bytes', t.RAM), ('wall_cap_s', 43200), ('output_cap_bytes', 96 * 2**30))}
        launch = jwrite(Path(str(rd) + '.receipt.json.launch.json'), {
            'utc': fmt(end - 2 * 10**9), 'child_pid': 900004, 'pins': {'spec': spec}, 'caps': caps})
        record = jwrite(d / 'launch_record.json', {
            'name': name, 'attempt': ordinal + 1, 'outdir': str(rd), 'receipt': str(rd) + '.receipt.json',
            'outcome': 'LAUNCH', 'launch_json': launch, 'solo_mode': legacy.get('other_ngc_processes_max') == 0,
            'host_ram_bytes': legacy.get('host_ram_bytes', t.RAM)})
        status_map = {
            'FINISHED': ('FINISHED', 'COMPLETED'),
            'FAILED_SOLVER': ('CHILD_FAILED', 'FAILED'),
            'WALL_CAP': ('STOPPED_WALL_CAP', None),
            'RSS_CAP': ('STOPPED_RSS_CAP', None),
            'OUTPUT_CAP_STOP': ('STOPPED_OUTPUT_CAP', None),
            'INFRA_SPAWN': ('CHILD_FAILED', 'BLOCKED'),
            'PLANNED_KILL': ('STOPPED_SIGNAL', None),
        }
        monitor_status, driver = status_map.get(legacy.get('receipt_status'), ('UNKNOWN', None))
        monitor = {
            'schema': self.rb.MONITOR_SCHEMA, 'utc_start': fmt(end - 2 * 10**9), 'utc_end': fmt(end),
            'child_pid': 900004, 'pins': {'spec': spec}, 'caps': caps,
            'status': monitor_status, 'driver_status': driver, 'exit_code': 0, 'result': result,
        }
        monitor['receipt_sha256'] = self.rb.sha256_hex(self.rb.canonical_bytes(monitor))
        monitor_pin = jwrite(Path(str(rd) + '.receipt.json'), monitor)
        count = legacy.get('other_ngc_processes_max')
        sample = None
        if count is not None:
            sample = jwrite(Path(str(rd) + '.solo.json'), {
                'schema': 'STEP5_SOLO_SAMPLE_CX2V001', 'name': name, 'attempt': ordinal + 1,
                'outdir': str(rd), 'declared_list_sha256': self.rb.DECLARED_LIST_SHA,
                'monitor_receipt': monitor_pin, 'complete': True, 'poll_s': 1, 'largest_gap_s': 1,
                'first_utc': fmt(end - 3 * 10**9), 'last_utc': fmt(end + 10**9),
                'n_samples': 5, 'max_other_ngc_processes': count})
        raw_status = ('TWIN_PLANNED_STOP' if name == self.rb.TWIN and monitor_status.startswith('STOPPED_') else
                      monitor_status + '|' + (driver or 'NONE'))
        doc = {
            'schema': 'STEP5_ATTEMPT_RECEIPT_C2V001', 'raw_status': raw_status,
            'status_class': self.rb.STATUS_CLASSES.get(raw_status), 'time_utc': fmt(end),
            'launch_utc': fmt(end - 2 * 10**9), 'spec_sha256': spec_sha, 'theta_sha256': point,
            'point_key': point, **caps, 'host_ram_bytes': legacy.get('host_ram_bytes', t.RAM),
            'other_ngc_processes_max': count, 'call': call, 'attempt': ordinal + 1, 'run_dir': str(rd),
            'solo_mode': count == 0, 'pins': {
                'monitor_receipt': monitor_pin, 'launch_json': launch, 'launch_record': record,
                'registry_entry': entry, 'solo_sample': sample, 'stop_record': None,
                'result': result, 'status_map_sha256': self.rb.STATUS_MAP_SHA,
            }}
        pin = jwrite(sidecar, doc)
        self.promoted[key] = pin
        return pin


t.Env = Env
old_call, old_input, old_activate = t.Base.call, t.Base.input, t.Base.activate


def call(self, *args, **kwargs):
    result = old_call(self, *args, **kwargs)
    identity = {k: result[k] for k in ('alternative', 'kind', 'key')}
    for i, a in enumerate(result['attempts']):
        self.env.owners[a['receipt']['path']] = (
            identity, a['run_dir'], result['result'] if i == len(result['attempts']) - 1 else None, i)
    return result


def activate(self):
    old_activate(self)
    self.env.rb.share_freeze_snapshot(self.fm)


def promoted_input(self, directory, phase, stage, extra):
    extra = copy.deepcopy(extra)
    extra['spec_of_record'] = self.spec_pin
    if stage == 'PLAN':
        return old_input(self, directory, phase, stage, extra)
    calls = extra.get('calls') if isinstance(extra.get('calls'), list) else []
    others = extra.get('other_phase_calls') if isinstance(extra.get('other_phase_calls'), list) else []
    entries, copy_sources, terminal_pins, times = [], [], [], []
    for c in calls + others:
        identity = ({k: c[k] for k in ('alternative', 'kind', 'key')} if 'label' not in c else
                    {'alternative': None, 'kind': 'OTHER', 'key': c['label']})
        if not isinstance(c.get('attempts'), list):
            continue
        for i, a in enumerate(c['attempts']):
            a['receipt'] = self.env.promote(
                a['receipt'], a['run_dir'], identity,
                c.get('result') if i == len(c['attempts']) - 1 else None, i)
            receipt = t.jload(a['receipt']['path'])
            entry = receipt['pins']['registry_entry']
            if entry not in entries:
                entries.append(entry)
            if i == len(c['attempts']) - 1:
                terminal_pins.append(a['receipt'])
                times.append(self.env.rb.parse_utc_ns(receipt['time_utc'], 'fixture'))
                copy_sources += [a['receipt'], receipt['pins']['monitor_receipt']]
                if receipt['pins']['result'] is not None:
                    copy_sources.append(receipt['pins']['result'])
        for k in ('result', 'cut_record'):
            if c.get(k) is not None:
                copy_sources.append(c[k])
    extra['registry_verification'] = {'entries': entries}
    if 'm15' in extra:
        extra['m15'] = self.env.launch_m15(extra['m15'])
    copies = []
    seen = set()
    for p in copy_sources:
        key = (p['path'], p['sha256'])
        if key in seen:
            continue
        seen.add(key)
        if not Path(p['path']).is_file():
            continue
        raw = Path(p['path']).read_bytes()
        destination = self.env.custody_root / (t.sha(raw) + '.bin')
        if not destination.exists():
            t.wbytes(str(destination), raw)
        copies.append({'source': p, 'copy': {'path': str(destination), 'sha256': t.sha(raw)}})
    extra['custody'] = {'root': str(self.env.custody_root), 'run_volumes': ['/'], 'copies': copies}
    if phase == 'PHASE_1' and stage == 'FULL' and isinstance(extra.get('gate_cutoff'), dict) and times:
        cp = extra['gate_cutoff']['v006_copy']
        raw = Path(cp['path']).read_bytes()
        rec = {'schema': 'STEP4_CUTOFF_RECORD_C2V001',
               'date_u': self.env.rb.format_utc_ns(max(times) + 10**9),
               'copy': {**cp, 'bytes': len(raw)}, 'terminal_attempt_receipts': terminal_pins, 'supersedes': None}
        key = t.sha(self.env.rb.canonical_bytes(rec))
        p = Path(self.env.dir('cutoff_records')) / (key + '.json')
        if not p.exists():
            jwrite(p, rec)
        extra['gate_cutoff']['record'] = t.pin(str(p))
    return old_input(self, directory, phase, stage, extra)


t.Base.call, t.Base.input, t.Base.activate = call, promoted_input, activate


def run_cli(args):
    stdout, stderr = io.StringIO(), io.StringIO()
    previous = env.rb.tsr_check
    env.rb.tsr_check = env.rb._check_tsr_flag
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = env.rb._parent_main(args)
    finally:
        env.rb.tsr_check = previous
    return types.SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


t.run_cli = run_cli
env = Env(str(WORK))
world = t.World(env)
results = []
for cid, expect, code, fn in t.CASES:
    verdict, observed, detail = 'FAIL', 'NO_REFUSAL', None
    try:
        fn(env, world)
        if expect == 'MUST_PASS':
            verdict = 'PASS'
    except (env.rb.Refused, env.rb.Stop) as exc:
        observed = exc.code
        if expect == 'MUST_FAIL' and exc.code == code:
            verdict = 'PASS'
        else:
            detail = str(exc)[:800]
    except Exception as exc:
        observed = type(exc).__name__
        detail = repr(exc)[:1500]
    results.append({'id': cid, 'expect': expect, 'expected_code': code, 'observed': observed,
                    'verdict': verdict, 'detail': detail})
    if verdict == 'FAIL':
        print(json.dumps(results[-1], sort_keys=True))
record = {
    'scope': __doc__, 'parent_test_sha256': PARENT_SHA, 'builder_sha256': BUILDER_SHA,
    'n_cases': len(results), 'n_pass': sum(r['verdict'] == 'PASS' for r in results), 'cases': results,
}
jwrite(WORK / 'TEST_RECORD.json', record)
print('%d/%d PASS' % (record['n_pass'], record['n_cases']))
raise SystemExit(0 if record['n_pass'] == record['n_cases'] else 1)
