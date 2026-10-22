"""Execute only the pinned consumer LO metadata gate, never its CLI or engine."""
import ast
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

OUT = Path(__file__).parent
CONSUMER = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py')
CONSUMER_SHA = 'b00dd854e79b36718fc67d9e82311e567a3e1ce08fbc1ed93cab5e60d9e6af01'
RECORD = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/gates/LO_CERT_V003_MS128.json')
RECORD_SHA = '9fdb897ae3b80dd6a3d2cf9ff273619dbf5fa419405cc8dacd1fa77ee2539268'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    return {'path': str(p), 'sha256': sha(p)}

def write(name, value):
    with (OUT/name).open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')

assert sha(CONSUMER) == CONSUMER_SHA
assert sha(RECORD) == RECORD_SHA
source = CONSUMER.read_text()
tree = ast.parse(source)
functions = {'FieldMissing', '_num', '_hex64', 'need', 'registered_P',
             'production_kbig', 'coverage_edge_2P', '_shells', '_union_covers',
             '_g_lo', 'g_LO'}
constants = {'KINDS', 'PIN_R3', 'PRODUCTION_GAS_M_S_A57', 'LO_RANGES_R1',
             'LO_RANGES', 'LO_COVERAGE_LOWER', 'COVERAGE_FACTOR_OF_2P',
             'R1_DDO_COVERAGE_EDGE'}
selected = []
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in functions:
        selected.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in node.targets):
        selected.append(node)
snapshot = [{'line_start': n.lineno, 'line_end': n.end_lineno,
             'source': ast.get_source_segment(source, n)} for n in selected]
write('LO_CONSUMER_FRAGMENT_SNAPSHOT_V001.json', {
    'consumer': pin(CONSUMER), 'utc': datetime.now(timezone.utc).isoformat(),
    'date_u': 'Sun Oct 18 15:03:51 UTC 2026', 'fragments': snapshot,
    'scope': 'Only LO metadata gate definitions and dependencies. No main, module import, scientific state open, or comparison engine.'})
# CTRL is only used to construct unused pathname strings in PIN_R3; all actual
# scientific-result hashes and all gate logic are the original source bytes.
namespace = {'math': math, 'CTRL': 'NOT_OPENED_PATH_PREFIX'}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(CONSUMER), 'exec'), namespace)
context = {'case_block': {'cases': {'C4T': {'normalized_spec_equal': {
    '/numerics': {'uv_tail': {'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128}}}}}}}}
record = json.loads(RECORD.read_text())

def run(rec):
    read = []
    try:
        defects = namespace['g_LO'](rec, context, None, read)
        return {'defects': defects, 'read': read, 'exception': None}
    except namespace['FieldMissing'] as exc:
        return {'defects': None, 'read': read, 'exception': exc.code}

tests = []
actual = run(record)
tests.append({'name': 'actual_original_record_missing_required_field_refuses',
              'passed': actual['exception'] == 'FIELD_MISSING:LO:source_gas_M_s', 'result': actual})
fixed = dict(record, source_gas_M_s=128)
answer = run(fixed)
tests.append({'name': 'synthetic_metadata_only128_diagnostic_gate_accepts',
              'passed': answer['defects'] == [] and answer['exception'] is None, 'result': answer})
answer = run(dict(record, source_gas_M_s=64))
tests.append({'name': 'synthetic_wrong64_refuses',
              'passed': 'DEFECT:LO_SOURCE_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S' in (answer['defects'] or []), 'result': answer})
answer = run(dict(record, source_gas_M_s=True))
tests.append({'name': 'synthetic_bool_refuses',
              'passed': answer['exception'] == 'FIELD_TYPE_int:LO:source_gas_M_s', 'result': answer})
short = copy.deepcopy(fixed)
short['shells'][-1]['range_inverse_kpc'][1] = 362
answer = run(short)
tests.append({'name': 'synthetic362_endpoint_refuses_full_geometric_reach',
              'passed': 'DEFECT:LO_COVERAGE_BELOW_SQRT2_TIMES_2P_A54' in (answer['defects'] or []), 'result': answer})
write('LO_CONSUMER_GATE_REVIEW_V001.json', {
    'date_u': 'Sun Oct 18 15:03:51 UTC 2026', 'utc': datetime.now(timezone.utc).isoformat(),
    'source': pin(__file__), 'consumer': pin(CONSUMER), 'record': pin(RECORD),
    'fragment_snapshot': pin(OUT/'LO_CONSUMER_FRAGMENT_SNAPSHOT_V001.json'),
    'tests': tests, 'passed': sum(t['passed'] for t in tests), 'total': len(tests),
    'actual_original_record_admission': 'FAIL_REQUIRED_FIELD',
    'qualification': 'Synthetic in-memory field additions are diagnostic only; they do not amend or adopt the original record, create a production certificate, or test the full comparison engine.',
    'scientific_launches': 0, 'real_targets_opened': False})
assert all(t['passed'] for t in tests)
print(json.dumps(pin(OUT/'LO_CONSUMER_GATE_REVIEW_V001.json')))
