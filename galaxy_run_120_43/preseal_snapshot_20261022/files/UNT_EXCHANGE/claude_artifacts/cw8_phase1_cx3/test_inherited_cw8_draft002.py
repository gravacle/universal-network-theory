"""Port the 160 predecessor cases to synthetic c2v007 fixtures.

The old suite's production TSR/compare/N1/node reads are replaced with invented
fixtures. The old flag-only tests exercise _check_tsr_flag; new G7 tests exercise
the support-aware command separately. Registry production is a fixture seam in
these inherited roster tests; dedicated P112 tests exercise the real verifier.
Receipts, monitoring evidence, custody copies, cutoff and M15 records are real
synthetic files and pass through the c2v007 validators.
"""

import ast
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
BUILDER = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8_draft002.py')
BUILDER_SHA = 'ee28c30d6d2308d6b2a9ed2f7dbc79f4e7d16975ce6e1dabdf94b77b92802799'
DEADLINES={'PHASE_1':'2026-11-06T05:59:00Z','PHASE_2':'2026-12-01T05:59:00Z'}
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
raw = PARENT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == PARENT_SHA
source = raw.decode().replace('env.rb.tsr_check(', 'env.rb._check_tsr_flag(')
t = types.ModuleType('inherited_cases')
t.__file__ = str(HERE / 'synthetic_inherited_source.py')

# Explicit expectation changes required by c2v007 contracts, before execution.
source = source.replace(
    "geometry = e['kind'] == 'NGC3198_NUISANCE'",
    "geometry = e['kind'] == 'NGC3198_NUISANCE'\n            if geometry:\n                continue")
source = source.replace("len(fctx) == 9", "len(fctx) == 5")
source = source.replace("'2026-10-31T15:00:00Z'", "'2026-10-31T01:30:00Z'")
source = source.replace("rec[k]['sha256'].startswith(s)",
                        "rec[k]['sha256'] == pin(rec[k]['path'])['sha256']")
source = source.replace("['BUILD_RECORD.json', 'GATE_STATUS_LIST.json', 'GATE_STATUS_REPORT.json',",
                        "['BUILD_RECORD.json', 'GATE_CUTOFF_V006_COPY.md', 'GATE_STATUS_LIST.json', 'GATE_STATUS_REPORT.json',")

source = source.replace(
    "sorted(produced) == ['gate_status_list', 'tsr_flag_record']",
    "sorted(produced) == ['gate_status_list', 'tsr_flag_record', 'tsr_support_record']")

# Explicit A244–A246 expectation changes; all inherited case IDs are retained.
for old_code in ('RULE_C_INCOMPLETE', 'RULE_C_EVIDENCE_MISSING', 'RULE_C_NOT_SOLO', 'RULE_C_RERUN_CAPS'):
    source = source.replace("'" + old_code + "'", "'CALL_NOT_TERMINAL'")
parent_tree = ast.parse(source)
def replace_case(name, body):
    global source
    node = next(n for n in parent_tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    source = source.replace(ast.get_source_segment(source_original, node), body)
source_original = source
replace_case('_c04', """def _c04(env, w):
    out = w.p1_with_m001('c04', [
        ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T11:00:00Z', dict(ev(raised=True), wall_cap_s=43200))])
    _, plan, _ = w.outputs(out)
    primary = next(a for a in plan['alternatives'] if a['name'] == PRIMARY)
    assert primary['members'][1]['own_disposition'] == 'EVALUATED_FAILED'
""")
source = source.replace(
    "@case('C04_rerun_wall_cap_not_doubled_refused', 'MUST_FAIL', 'CALL_NOT_TERMINAL')",
    "@case('C04_rerun_wall_cap_not_doubled_refused', 'MUST_PASS')")
source = source.replace("'UNEVALUATED_CAP'", "'UNEVALUATED_SCHEDULE_CEILING'")
source = source.replace(
    "    assert rc['counted_attempts'] == [0, 1] and rc['rerun_wall_cap_s'] == 86400 and rc['rerun_rss_cap_bytes'] == RAM",
    "    assert rc is None")
source = source.replace(
    "    assert pa['members'][1]['rule_c']['rerun_output_cap_bytes'] == 136 * 2 ** 30",
    "    assert pa['members'][1]['rule_c'] is None")
source = source.replace("def _b20(env, w):", "def _b20(env, w):\n    env.close_at_ceiling = True")
source = source.replace("def _c08(env, w):", "def _c08(env, w):\n    env.close_at_ceiling = True")

# A249: a terminal failure with no result SHA cannot authenticate a model
# pair. Preserve the old scenario, now expecting its held state.
source=source.replace(
    "@case('B21_failed_terminal_with_rule_c_evidence_is_a_failure_record_MEMBER_INVALID', 'MUST_PASS')",
    "@case('B21_failed_terminal_with_rule_c_evidence_is_a_failure_record_MEMBER_INVALID', 'MUST_FAIL', 'HELD_FOR_CAUSE')")
# Current emitted metadata states A248/A249, replacing the old wall-doubling text.
source=source.replace(
    "assert 'no other NGC process running' in plan['rules']['c'] and 'wall cap' in plan['rules']['c']",
    "assert 'both solo' in plan['rules']['c'] and 'Wall caps are not doubled' in plan['rules']['c'] and 'CAP and nonphysics outcomes never count' in plan['rules']['c']")
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
    if event in ('os.rename', 'os.remove', 'os.rmdir'):
        raise AssertionError('IMMUTABILITY_FENCE: ' + event)
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        flags = args[2]
        if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR) and os.path.lexists(args[0]):
            raise AssertionError('IMMUTABILITY_FENCE: existing-file write')
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
        self.owners_by_sha = {}
        self.by_entry = {}
        self.m15_cache = {}
        self.copy_cache = {}
        self.custody_root = Path(self.dir('custody'))
        self.close_at_ceiling = False
        self.by_cause = {}
        pd = Path(self.dir('model_policy'))
        self.model_driver = jwrite(pd / 'driver.json', {'synthetic_driver': True})
        self.model_audit = jwrite(pd / 'audit.json', {'synthetic_audit': True})
        self.deadline_registration = {phase: jwrite(pd / (phase + '_deadline.json'), {
            'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': phase,
            'deadline_utc': DEADLINES[phase], 'date_u': '2026-10-01T00:00:00Z'})
            for phase in ('PHASE_1', 'PHASE_2')}
        self.cause_producer = jwrite(pd / 'cause_producer.json', {'synthetic_producer': True})

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

    def promote(self, receipt_pin, run_dir, call, result, ordinal, terminal_attempt=True):
        legacy = t.jload(receipt_pin['path'])
        if legacy.get('schema') == 'STEP5_ATTEMPT_RECEIPT_C2V001':
            return receipt_pin
        # Receipt aliases retain the original call; they are never rebound by
        # copying a record to a different call's input.
        owner = self.owners.get(receipt_pin['path']) or self.owners_by_sha.get(receipt_pin['sha256'])
        if owner:
            call, native_run, native_result, native_ordinal = owner
            if run_dir != native_run or call != owner[0]:
                result = native_result
            run_dir, ordinal = native_run, native_ordinal
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
            'utc': fmt(end - 2 * 10**9), 'child_pid': 900004, 'pins': {'spec': spec, 'driver': self.model_driver}, 'caps': caps})
        record = jwrite(d / 'launch_record.json', {
            'name': name, 'attempt': ordinal + 1, 'outdir': str(rd), 'receipt': str(rd) + '.receipt.json',
            'outcome': 'LAUNCH', 'launch_json': launch, 'solo_mode': legacy.get('other_ngc_processes_max') == 0,
            'host_ram_bytes': legacy.get('host_ram_bytes', t.RAM)})
        status_map = {
            'FINISHED': ('FINISHED', 'COMPLETED'),
            'FAILED_SOLVER': ('CHILD_FAILED', 'ROUTE_A_NO_FIXED_POINT'),
            'WALL_CAP': ('STOPPED_WALL_CAP', None),
            'RSS_CAP': ('STOPPED_RSS_CAP', None),
            'OUTPUT_CAP_STOP': ('STOPPED_OUTPUT_CAP', None),
            'INFRA_SPAWN': ('CHILD_FAILED', 'BLOCKED'),
            'PLANNED_KILL': ('STOPPED_SIGNAL', None),
        }
        monitor_status, driver = status_map.get(legacy.get('receipt_status'), ('UNKNOWN', None))
        if driver == 'ROUTE_A_NO_FIXED_POINT' and result is None and not terminal_attempt:
            result = jwrite(d / 'synthetic_first_failed_result.json', {'synthetic_failed_attempt': True})
        stop_pin = None
        if name == self.rb.TWIN and monitor_status.startswith('STOPPED_'):
            stop_pin = jwrite(d / 'twin_stop.json', {
                'schema': 'UNT_S0_TWIN_KILL_RECORD_C2V003A',
                'reason': 'ITERATION_0001_COMPLETED_AND_SIDECAR', 'outdir': str(rd),
                'launch_json': launch, 'pgid': 900004, 'result': 'KILLED_TERM',
                'date_u': fmt(end)})
        monitor = {
            'schema': self.rb.MONITOR_SCHEMA, 'utc_start': fmt(end - 2 * 10**9), 'utc_end': fmt(end),
            'child_pid': 900004, 'pins': {'spec': spec, 'driver': self.model_driver}, 'caps': caps,
            'status': monitor_status, 'driver_status': driver, 'exit_code': 0 if driver == 'COMPLETED' else 1, 'result': result,
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
                'registry_entry': entry, 'solo_sample': sample, 'stop_record': stop_pin,
                'result': result, 'status_map_sha256': self.rb.STATUS_MAP_SHA,
            }}
        pin = jwrite(sidecar, doc)
        cause = None
        if driver == 'ROUTE_A_NO_FIXED_POINT':
            cause = jwrite(d / 'cause.json', {
                'status': driver, 'failing_stage': 'ROUTE_A',
                'failure_code': 'ROUTE_A_NO_FIXED_POINT', 'exception_class': 'ValueError',
                'raise_site': 'SITE_SET:["synthetic.py:100"]',
                'bound_shas': {'receipt': monitor_pin['sha256'], 'spec': spec_sha,
                    'driver': self.model_driver['sha256'], 'finish': 'd'*64,
                    'result': None if result is None else result['sha256']},
                'model_outcome': result is not None,
                'model_outcome_reason': 'SYNTHETIC_MODEL' if result is not None else 'UNAUTHENTICATED'})
        self.by_cause[str(sidecar)] = cause
        self.promoted[key] = pin
        return pin


t.Env = Env
old_call, old_input, old_activate = t.Base.call, t.Base.input, t.Base.activate


def call(self, *args, **kwargs):
    result = old_call(self, *args, **kwargs)
    identity = {k: result[k] for k in ('alternative', 'kind', 'key')}
    for i, a in enumerate(result['attempts']):
        owner = (
            identity, a['run_dir'], result['result'] if i == len(result['attempts']) - 1 else None, i)
        self.env.owners[a['receipt']['path']] = owner
        self.env.owners_by_sha.setdefault(a['receipt']['sha256'], owner)
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
    policy_attempts, policy_closures = {}, []
    for c in calls + others:
        identity = ({k: c[k] for k in ('alternative', 'kind', 'key')} if 'label' not in c else
                    {'alternative': None, 'kind': 'OTHER', 'key': c['label']})
        if not isinstance(c.get('attempts'), list):
            continue
        for i, a in enumerate(c['attempts']):
            a['receipt'] = self.env.promote(
                a['receipt'], a['run_dir'], identity,
                c.get('result') if i == len(c['attempts']) - 1 else None, i, i == len(c['attempts']) - 1)
            receipt = t.jload(a['receipt']['path'])
            policy_attempts[a['receipt']['path']] = {
                'receipt': a['receipt'], 'cause': self.env.by_cause.get(a['receipt']['path']), 'root_stop': None}
            entry = receipt['pins']['registry_entry']
            if entry not in entries:
                entries.append(entry)
            if i == len(c['attempts']) - 1:
                terminal_pins.append(a['receipt'])
                times.append(self.env.rb.parse_utc_ns(receipt['time_utc'], 'fixture'))
                copy_sources += [a['receipt'], receipt['pins']['monitor_receipt']]
                if receipt['pins']['result'] is not None:
                    copy_sources.append(receipt['pins']['result'])
        if self.env.close_at_ceiling and c['attempts'] and receipt['status_class'] in ('CAP', 'OUTPUT_CAP'):
            closure = {
                'schema': self.env.rb.CEILING_SCHEMA, 'phase': phase,
                'date_u': DEADLINES[phase], 'deadline_utc': DEADLINES[phase],
                'deadline_registration': self.env.deadline_registration[phase],
                'call': dict(identity, theta_sha256=receipt['theta_sha256'], spec_sha256=receipt['spec_sha256']),
                'last_receipt': a['receipt']}
            pd = Path(self.env.dir('ceiling_records'))
            cp = pd / (self.env.rb.sha256_hex(self.env.rb.canonical_bytes(closure)) + '.json')
            if not cp.exists():
                jwrite(cp, closure)
            policy_closures.append(t.pin(str(cp)))
            times.append(self.env.rb.parse_utc_ns(closure['date_u'], 'synthetic ceiling'))
        for k in ('result', 'cut_record'):
            if c.get(k) is not None:
                copy_sources.append(c[k])
    policy = {
        'schema': self.env.rb.INTERRUPTION_POLICY_SCHEMA, 'phase': phase,
        'cause_producer': self.env.cause_producer, 'deadline_utc': DEADLINES[phase],
        'deadline_registration': self.env.deadline_registration[phase],
        'attempts': [policy_attempts[k] for k in sorted(policy_attempts)], 'closures': policy_closures}
    pd = Path(self.env.dir('interruption_policies'))
    pp = pd / (self.env.rb.sha256_hex(self.env.rb.canonical_bytes(policy)) + '.json')
    if not pp.exists():
        jwrite(pp, policy)
    extra['interruption_policy'] = t.pin(str(pp))
    if isinstance(extra.get('gate_cutoff'), dict):
        old_cut = extra['gate_cutoff']['v006_copy']
        cut_raw = Path(old_cut['path']).read_bytes()
        cut_raw += ('\\n## A899 2026-10-01T00:00:00Z synthetic cause producer\\n' +
                    self.env.cause_producer['sha256'] + '\\n').encode()
        cut_path = Path(self.env.dir('cause_cutoff')) / (t.sha(cut_raw) + '.md')
        if not cut_path.exists():
            t.wbytes(str(cut_path), cut_raw)
        extra['gate_cutoff']['v006_copy'] = t.pin(str(cut_path))

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

def k12_no_move(env, w):
    x = t.Discrepancy(env, w, 'k12')
    target = t.ledger_dir(x.out)
    previous = env.rb._ledger_files
    def missing(path, build_sha, plan_sha):
        if path == target:
            raise env.rb.Refused('STEP7_LEDGER_MISSING', 'synthetic absent-path view')
        return previous(path, build_sha, plan_sha)
    env.rb._ledger_files = missing
    try:
        t.step7(env, x.out, x.plan_pin, x.p.p1_pin, x.pk_agree)
    finally:
        env.rb._ledger_files = previous


def k16_no_move(env, w):
    a, b = w.build_p1('k16a'), w.build_p1('k16b')
    target = os.path.join(t.ledger_dir(a), 'LEDGER_GENESIS.json')
    foreign_path = os.path.join(t.ledger_dir(b), 'LEDGER_GENESIS.json')
    foreign = Path(foreign_path).read_bytes()
    previous = env.rb._read_regular
    def swapped(path, where, ident_out=None):
        if os.path.realpath(path) == target:
            if ident_out is not None:
                st = os.stat(foreign_path)
                ident_out.append((st.st_dev, st.st_ino))
            return foreign, target
        return previous(path, where, ident_out)
    env.rb._read_regular = swapped
    try:
        t.drive(env, w.b1, a, 'PASS_ONE')
    finally:
        env.rb._read_regular = previous


patched_cases = []
for cid, expect, code, fn in t.CASES:
    if cid.startswith('K12_'):
        fn = k12_no_move
    elif cid.startswith('K16_'):
        fn = k16_no_move
    elif cid.startswith('B09_'):
        # Both calls claim one run directory; one sidecar has one registered
        # call. c2v007 refuses this before reaching the borrowed cut check.
        def bound_sidecar(env, w):
            try:
                t._b09(env, w)
            except AssertionError as exc:
                assert 'observed RECEIPT_CALL_NOT_REGISTERED' in str(exc), str(exc)
                raise env.rb.Refused('RECEIPT_CALL_NOT_REGISTERED')
        fn, code = bound_sidecar, 'RECEIPT_CALL_NOT_REGISTERED'
    patched_cases.append((cid, expect, code, fn))
t.CASES = patched_cases
env = Env(str(WORK))

world = t.World(env)
# Old OTHER fixtures are now saved producer receipts before identity/hard-link
# tests refer to them, rather than intermediate legacy dictionaries.
for other in world.other:
    for i, attempt in enumerate(other['attempts']):
        attempt['receipt'] = env.promote(
            attempt['receipt'], attempt['run_dir'],
            {'alternative': None, 'kind': 'OTHER', 'key': other['label']}, None, i)
old_own_other = t.own_other
def own_other_saved(run_dir, label, time, extra=None):
    other = old_own_other(run_dir, label, time, extra)
    attempt = other['attempts'][0]
    attempt['receipt'] = env.promote(
        attempt['receipt'], attempt['run_dir'],
        {'alternative': None, 'kind': 'OTHER', 'key': label}, None, 0)
    return other
t.own_other = own_other_saved
old_frozen_checks = t.frozen_checks
def frozen_checks_registered_vn1(base, mem, pins):
    geometry = base.env.rb.registered_geometry(base.spec, base.fm)
    answers = base.env.rb.geometry_exemptions([
        (e['entry_id'], e['theta_ngc'], e['skipped_zero_displacement'], e['kind'])
        for e in mem['sensitivity']['evaluations']], geometry)
    plan = {'registered_geometry': geometry, 'geometry_not_exposed': answers}
    with base.env.rb.geometry_runtime(base.fm, plan):
        return old_frozen_checks(base, mem, pins)
t.frozen_checks = frozen_checks_registered_vn1

EXPECTATION_CHANGES = {
    'O1c_': 'RECEIPT_NOT_AT_REGISTERED_SIDECAR',
    'R2a_': 'RECEIPT_NOT_AT_REGISTERED_SIDECAR',
    'R2c_': 'RECEIPT_NOT_AT_REGISTERED_SIDECAR',
    'R2d_': 'RECEIPT_CALL_NOT_REGISTERED',
    'H04_': 'RECEIPT_NOT_AT_REGISTERED_SIDECAR',
    'H10_': 'RESULT_NOT_MONITOR_PIN',
    'J01_': 'RECEIPT_CALL_NOT_REGISTERED',
    'J03_': 'CUT_RECORD_NOT_REGISTERED_SCHEMA',
}
adapted = []
for cid, expect, code, fn in t.CASES:
    replacement = next((v for k, v in EXPECTATION_CHANGES.items() if cid.startswith(k)), None)
    if replacement:
        old_code = code
        def earlier_boundary(e, w, fn=fn, old_code=old_code, replacement=replacement):
            try:
                return fn(e, w)
            except AssertionError as exc:
                # The predecessor's helper rephrases the actual refusal as an
                # assertion. Accept only the explicit documented earlier code.
                assert ('expected ' + old_code + ', observed ' + replacement + ' (') in str(exc), str(exc)
                raise e.rb.Refused(replacement, 'earlier c2v007 producer boundary')
        fn, code = earlier_boundary, replacement
    adapted.append((cid, expect, code, fn))
t.CASES = adapted
"""New command and full-builder checks, using the inherited synthetic world."""

G7_FIXTURE = None


def g7_fixture(env, w):
    global G7_FIXTURE
    if G7_FIXTURE is not None:
        return G7_FIXTURE
    d = Path(env.dir('new_g7'))
    out = w.build_p1('new_g7_full')
    plan_pin = t.pin(os.path.join(out, 'REPLAY_PLAN.json'))
    build_pin = t.pin(os.path.join(out, 'BUILD_RECORD.json'))
    plan = t.jload(plan_pin['path'])
    one, _, _ = t.drive(env, w.b1, out, 'PASS_ONE')
    last, _, _ = t.drive(env, w.b1, out, 'PASS_K')
    p1 = jwrite(d / 'one.json', one)
    pk = jwrite(d / 'last.json', last)
    clear, _, _ = env.rb.step7_run(build_pin, plan_pin, p1, pk)
    assert clear['status'] == 'NO_NEW_DISCREPANCY'
    primary = next(a for a in plan['alternatives'] if a['name'] == plan['primary'])
    fdplan = jwrite(d / 'fdplan.json', {
        'schema': 'PHASE1_FDPLAN_C2V001',
        'members': [{'log_index': m['log_index'], 'role': m['role'], 'order': m['order'],
                     'key': t.sha(env.rb.canonical_bytes([m['log_index'], m['role'], m['order']]))}
                    for m in primary['members']],
    })
    policy = jwrite(d / 'policy.json', {'slots': w.b1.slots})
    flag = t.pin(t.TSR_RECORD_PATH)
    flag_doc = t.jload(flag['path'])
    doc = {
        'schema': env.rb.TSR_SUPPORT_INPUT_SCHEMA, 'build_record': build_pin,
        'replay_plan': plan_pin, 'pass_record': pk, 'fdplan': fdplan,
        'extractor_policy': policy, 'compare': flag_doc['ntest_compare_pin'],
    }
    before = READS.count(w.b1.slots['path'])
    projected = env.rb.tsr_support(doc)
    assert READS.count(w.b1.slots['path']) == before
    support_pin = jwrite(d / 'support.json', projected)
    manifest = jwrite(d / 'manifest.json', {'pins': {'input_files': [
        flag, support_pin, flag_doc['ntest_compare_pin'], flag_doc['n1_record_pin'],
        flag_doc['gl_node_record_pin'],
    ]}})
    G7_FIXTURE = dict(d=d, input=doc, projected=projected, support=support_pin,
                      flag=flag, manifest=manifest)
    return G7_FIXTURE


def g7_command(env, w):
    f = g7_fixture(env, w)
    inp = jwrite(f['d'] / 'support_input.json', f['input'])
    output = f['d'] / 'support_from_command.json'
    with contextlib.redirect_stdout(io.StringIO()):
        code = env.rb.main(['tsr-support', '--input', inp['path'], '--input-sha256', inp['sha256'],
                            '--out', str(output)])
    assert code == 0
    assert output.read_bytes() == Path(f['support']['path']).read_bytes()


def g7_check_command(env, w):
    f = g7_fixture(env, w)
    doc = {'schema': 'TSR_CHECK_INPUT_C2V007', 'flag_record': f['flag'], 'freeze_manifest': f['manifest'],
           'support': {'record': f['support'], 'projection_input': f['input']}}
    inp = jwrite(f['d'] / 'check_input.json', doc)
    output = f['d'] / 'check.json'
    with contextlib.redirect_stdout(io.StringIO()):
        code = env.rb.main(['tsr-check', '--input', inp['path'], '--input-sha256', inp['sha256'],
                            '--out', str(output)])
    assert code == 0
    assert t.jload(str(output))['verdict'] == 'PASS'


def g7_bad_support(env, w):
    f = g7_fixture(env, w)
    changed = copy.deepcopy(f['projected'])
    changed['slots_pin']['path'] += '.different-spelling'
    bad = jwrite(f['d'] / 'bad_support.json', changed)
    env.rb.tsr_check(f['flag'], f['manifest'],
                    support={'record': bad, 'projection_input': f['input']})


def g7_wrong_head(env, w):
    f = g7_fixture(env, w)
    unregistered = t.jload(f['input']['pass_record']['path'])
    unregistered['synthetic_unregistered_marker'] = True
    wrong_pass = jwrite(f['d'] / 'wrong_head_pass.json', unregistered)
    doc = dict(f['input'], pass_record=wrong_pass)
    env.rb.tsr_support(doc)


def g7_uncleared(env, w):
    f = g7_fixture(env, w)
    out = w.build_p1('new_g7_uncleared')
    doc = dict(f['input'], build_record=t.pin(os.path.join(out, 'BUILD_RECORD.json')),
               replay_plan=t.pin(os.path.join(out, 'REPLAY_PLAN.json')))
    env.rb.tsr_support(doc)


def m15_missing_launch(env, w):
    d = env.dir('new_m15_missing_launch')
    input_pin = w.b1.input(d, 'PHASE_1', 'FULL', w.p1_extra())
    doc = t.jload(input_pin['path'])
    expected = list(doc['m15']['launch_receipts'])
    assert len(expected) == 2
    doc['m15']['launch_receipts'] = expected[:1]
    modified = jwrite(Path(d) / 'missing_launch_input.json', doc)
    previous = env.rb.verify_launch_registry
    def complete_sources(given):
        proof = previous(given)
        proof['m15_launch_receipts'] = expected
        return proof
    env.rb.verify_launch_registry = complete_sources
    try:
        w.b1.build(modified, env.fresh('m15_missing'))
    finally:
        env.rb.verify_launch_registry = previous


def missing_custody(env, w):
    d = env.dir('new_custody_missing')
    p = w.b1.input(d, 'PHASE_1', 'FULL', w.p1_extra())
    doc = t.jload(p['path'])
    doc['custody']['copies'] = doc['custody']['copies'][1:]
    modified = jwrite(Path(d) / 'missing_copy.json', doc)
    w.b1.build(modified, env.fresh('custody_missing'))


def single_read_full_build(env, w):
    d = env.dir('new_single_read_build')
    p = w.b1.input(d, 'PHASE_1', 'FULL', w.p1_extra())
    before = len(READS)
    w.b1.build(p, env.fresh('single_read'))
    counts = collections.Counter(READS[before:])
    assert counts and max(counts.values()) == 1, {p: n for p, n in counts.items() if n != 1}


def frozen_geometry_case(env, w, bad=False):
    fm = w.b1.fm
    geometry = env.rb.registered_geometry(w.b1.spec, fm)
    theta = dict(w.b1.thetas['M000'])
    key = next(iter(geometry))
    theta[key] += 0.01
    digest = env.rb.theta_sha256(theta)
    plan = {'registered_geometry': geometry, 'geometry_not_exposed': {digest: ['SYN']}}
    e = {'kind': env.rb.SENS_NGC_KIND, 'theta_ngc': theta, 'evaluated': True,
         'forward_valid_flag': False, 'exception': None,
         'row_valid': [False], 'speeds_km_s': [1.0 if bad else None],
         'row_registration': [None], 'delta_from_reference_km_s': [None],
         'reasons': ['forward_ngc reason: GEOMETRY_NOT_EXPOSED', 'forward_ngc valid flag is not True']}
    previous = fm._root_frozen_rows
    try:
        with env.rb.geometry_runtime(fm, plan):
            fm._root_frozen_rows(e, ['SYN-Q'], {})
    finally:
        assert fm._root_frozen_rows is previous


new_cases = [
    ('N001_G7_support_command_and_no_slots_open', 'MUST_PASS', None, g7_command),
    ('N002_G7_check_command', 'MUST_PASS', None, g7_check_command),
    ('N003_G7_wrong_support_pin_spelling', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH', g7_bad_support),
    ('N004_G7_wrong_head_pass', 'MUST_FAIL', 'TSR_SUPPORT_NOT_HEAD_PASS', g7_wrong_head),
    ('N005_G7_before_step7_clear', 'MUST_FAIL', 'TSR_SUPPORT_STEP7_NOT_CLEARED', g7_uncleared),
    ('N006_G15_missing_seed_or_twin_launch', 'MUST_FAIL', 'M15_LAUNCH_SET_NOT_COMPLETE', m15_missing_launch),
    ('N007_G16_missing_custody_copy', 'MUST_FAIL', 'CUSTODY_SOURCE_SET', missing_custody),
    ('N008_A226_FULL_build_audit_single_read', 'MUST_PASS', None, single_read_full_build),
    ('N009_VN1_frozen_no_context_answer', 'MUST_PASS', None, frozen_geometry_case),
    ('N010_VN1_frozen_finite_row_refused', 'MUST_FAIL', 'VN1_FROZEN_ANSWER_NOT_EXACT',
     lambda e, w: frozen_geometry_case(e, w, True)),
]
t.CASES += new_cases

def zero_attempt_full(env,w,variant='member'):
    directory=Path(env.dir('new_zero_full_'+variant))
    p=w.b1.input(str(directory),'PHASE_1','FULL',w.p1_extra())
    doc=t.jload(p['path'])
    is_other=variant=='other'
    target=doc['other_phase_calls'][0] if is_other else doc['calls'][1]
    old_receipt=t.jload(target['attempts'][-1]['receipt']['path'])
    old_pin=target['attempts'][-1]['receipt']
    remove={old_pin['path'],old_receipt['pins']['monitor_receipt']['path']}
    if old_receipt['pins']['result'] is not None:
        remove.add(old_receipt['pins']['result']['path'])
    target['attempts']=[]
    if not is_other and variant!='has_result':
        target['result']=None;target['cut_record']=None
    doc['custody']['copies']=[x for x in doc['custody']['copies'] if x['source']['path'] not in remove]
    policy=t.jload(doc['interruption_policy']['path'])
    policy['attempts']=[x for x in policy['attempts'] if x['receipt']!=old_pin]
    binding={k:old_receipt['call'][k] for k in ('alternative','kind','key')}
    binding.update({k:old_receipt[k] for k in ('theta_sha256','spec_sha256')})
    cp=jwrite(directory/'closure.json',{
        'schema':env.rb.CEILING_SCHEMA,'phase':'PHASE_1','date_u':DEADLINES['PHASE_1'],
        'deadline_utc':DEADLINES['PHASE_1'],'deadline_registration':policy['deadline_registration'],
        'call':binding,'last_receipt':None})
    policy['closures']=[cp]
    doc['interruption_policy']=jwrite(directory/'policy_successor.json',policy)
    cutoff=t.jload(doc['gate_cutoff']['record']['path'])
    cutoff.update(T=DEADLINES['PHASE_1'],date_u=DEADLINES['PHASE_1'])
    cutoff['terminal_attempt_receipts']=[x for x in cutoff['terminal_attempt_receipts'] if x!=old_pin]
    doc['gate_cutoff']['record']=jwrite(directory/'cutoff_successor.json',cutoff)
    input_pin=jwrite(directory/'input_successor.json',doc)
    previous=env.rb.verify_launch_registry
    def snapshot_seam(given):
        proof=previous(given)
        if variant!='missing_snapshot':
            proof['mode']='P112_SAVED_PHASE1_SNAPSHOT'
            # The actual capture/verify path and PLAN reconstruction have a
            # separate suite. This seam isolates FULL-build handling of zero
            # eligible closed attempts.
            proof['call_states']=[{'call':binding,'attempts':[]}]
        return proof
    env.rb.verify_launch_registry=snapshot_seam
    before=len(READS)
    out=env.fresh('zero_full_'+variant)
    try:w.b1.build(input_pin,out)
    finally:env.rb.verify_launch_registry=previous
    assert not remove.intersection(READS[before:]),remove.intersection(READS[before:])
    _,plan,_=w.outputs(out)
    assert env.rb.parse_utc_ns(plan['step4']['start_utc'],'T')==env.rb.parse_utc_ns(DEADLINES['PHASE_1'],'ceiling')
    assert plan['allow_incomplete'] is True
    if not is_other:
        primary=next(a for a in plan['alternatives'] if a['name']==plan['primary'])
        member=primary['members'][1]
        assert member['own_disposition']=='UNEVALUATED_SCHEDULE_CEILING'
        assert member['n_attempts']==0
    assert old_pin not in t.jload(doc['gate_cutoff']['record']['path'])['terminal_attempt_receipts']

t.CASES += [
    ('N011_A253_FULL_zero_member','MUST_PASS',None,zero_attempt_full),
    ('N012_A253_FULL_zero_other','MUST_PASS',None,lambda e,w:zero_attempt_full(e,w,'other')),
    ('N013_A253_FULL_zero_requires_snapshot','MUST_FAIL','CALL_ATTEMPTS_REQUIRED',lambda e,w:zero_attempt_full(e,w,'missing_snapshot')),
    ('N014_A253_FULL_ceiling_result_refused','MUST_FAIL','SCHEDULE_CEILING_HAS_RESULT_OR_CUT',lambda e,w:zero_attempt_full(e,w,'has_result')),
]

if len(sys.argv) > 2:
    t.CASES = [row for row in t.CASES if row[0].startswith(sys.argv[2])]

results = []
for cid, expect, code, fn in t.CASES:
    verdict, observed, detail = 'FAIL', 'NO_REFUSAL', None
    try:
        env.close_at_ceiling = False
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
