"""Source-only V007 R5 cross-lineage review; all numerical records manufactured.
No driver, scientific solve, saved run, target, subprocess or network is used.
Fixture constructors are AST-selected from the author tests; their top-level reads
are never executed. Adversaries and the independent noise oracle are ours.
nice unavailable (sandbox); 0514 waiver
"""
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import random
import resource
import sys
import time
import types
import numpy as np

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT = ROOT / 'review_v007_compare_cx2'
CMP = ROOT / 'v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py'
FIX = ROOT / 'v007_compare_c2/r5/tests_kmax_tail_compare_c2v007_r5.py'
LIB = ROOT / 'tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py'
INPUTS = [CMP, FIX, LIB]
READS = []
def audit(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if '/runs/' in p or '/runs_ext/' in p or 'KMAX_A2F10_C5H_RUN_V001' in p or 'NGC3198' in p or '/.codex/' in p:
            raise RuntimeError('FORBIDDEN_READ_ATTEMPT')
        if '/Research/' in p:
            READS.append(p)
            if p not in {str(x) for x in INPUTS} and not p.startswith(str(OUT) + '/'):
                raise RuntimeError('UNDECLARED_RESEARCH_READ')
sys.addaudithook(audit)

PINS = {}
def load_source(path, name):
    raw = path.read_bytes()
    PINS[str(path)] = hashlib.sha256(raw).hexdigest()
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module
M = load_source(CMP, 'cmp_r5_review')
L = load_source(LIB, 'tail_normalizer_review')
source = FIX.read_bytes()
PINS[str(FIX)] = hashlib.sha256(source).hexdigest()
names = {'sha', 'uv_cfg', 'ro1b', 'numerics_for', 'case_block', 'passes_from', 'receipt_for', 'make_run',
         'identity_run', 'a53_picard_shape', 'shift', 't1_rows', 'base_runs', 'rec', '_sh', 'complete_records',
         'b0_ext_entry', 'mt_record'}
tree = ast.parse(source)
chosen = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name in names]
assert {x.name for x in chosen} == names
ids = ['SYNTH_ROW_%02d' % (i + 1) for i in range(12)]
tau = {x: 1.0 for x in ids}
grids = {'G%d' % i: {'manufactured_grid_index': i} for i in range(2, 7)}
anchor = {'galaxy': 'DDO154', 'physical': {'manufactured': True}, 'coefficients': {'manufactured': True},
          'picard': {'passes': 6, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True}}
c5num = {'picard': copy.deepcopy(anchor['picard']), 'brackets': {'manufactured': True},
         'route_a': {'column_workers': 8, 'max_iterations': 32}, 'truncation': dict(M.EXPECTED_TRUNCATION['C5H']),
         'composite_grid_spec': grids['G5']}
ctx = {'ids': ids, 'tau': tau, 'sigma': dict(tau), 'tau_picard': 0.0125, 'grids': grids, 'anchor': anchor,
       'ra4_block': c5num['brackets'], 'c5h_numerics_reference': c5num, 'route_a_mode': 'parallel8',
       'row_radii_m': [float(i + 1) for i in range(12)], 'c5h_admission': {'admitted': True, 'failed': []},
       'v005_next_steps': {k: 'repair manufactured ' + k for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6')}}
f = {'M': M, 'CTX': ctx, 'IDS': ids, 'TAU': tau, 'RADII': ctx['row_radii_m'], 'copy': copy,
     'hashlib': hashlib, 'json': json, 'V010': 'a' * 64, 'EPS_COV': 128., 'LO_EXT': ((64, 128),),
     'REAL': {'C2R3': {'rows': {x: 10. for x in ids}}}, 'C2': {x: 10. for x in ids},
     'GOOD_D23': {x: 2. * (-1 if i % 2 else 1) for i, x in enumerate(ids)},
     'GOOD_D34': {x: .4 * (-1 if i % 2 else 1) for i, x in enumerate(ids)}}
f.update(WORKER_SERIAL=M.PIN_RO1_CUSTODY['worker'][1], WORKER_PARALLEL=M.PIN_RO1_CUSTODY['worker_parallel'][1],
         BINDING=M.PIN_RO1_CUSTODY['binding'][1], NODES_SERIAL=M.PIN_RO1_NODES_CUSTODY['worker'][1],
         NODES_PARALLEL=M.PIN_RO1_NODES_CUSTODY['worker_parallel'][1])
exec(compile(ast.Module(body=chosen, type_ignores=[]), str(FIX) + ':selected_functions_only', 'exec'), f)
f['UVT_SHA'] = {lab: L.normalize_config(f['uv_cfg'](lab))['sha256'] for lab in M.T_CASES}
ctx['case_block'] = f['case_block']()
CHECKS = []
def check(name, ok, **data):
    CHECKS.append(dict(name=name, passed=bool(ok), **data))

def hist(increments, final=None):
    final = final or {i: 10. for i in ids}
    rows = [dict(final)]
    for inc in reversed(increments):
        rows.insert(0, {i: rows[0][i] - inc[j] for j, i in enumerate(ids)})
    return {'pass_rows': rows, 'adapted': {'rows': final}}

def oracle(run):
    r = run['pass_rows'][-4:]
    ds = [[r[k][i] - r[k-1][i] for i in ids] for k in range(1, len(r))]
    if not ds:
        return None
    norms = [max(abs(v) / tau[i] for i, v in zip(ids, d)) for d in ds]
    ratios = [norms[j] / norms[j-1] if norms[j-1] else (math.inf if norms[j] else 0.) for j in range(1, len(ds))]
    if any(v >= 1 for v in ratios):
        return None
    q = min(.9, max(ratios)) if ratios else .5
    output = {}
    for j, i in enumerate(ids):
        row_bound = 0.
        if len(ds) >= 2 and (ds[-1][j] > 0 and ds[-2][j] > 0 or ds[-1][j] < 0 and ds[-2][j] < 0):
            qrow = min(.9, abs(ds[-1][j] / ds[-2][j]))
            row_bound = abs(ds[-1][j]) * qrow / (1-qrow)
        output[i] = max(tau[i] * norms[-1] * q / (1-q), row_bound)
    return output

rng = random.Random(524)
for n in range(1000):
    increments = [[rng.uniform(-.01, .01) * (10 ** (-k * rng.uniform(0., 1.))) for _ in ids] for k in range(rng.randrange(1, 6))]
    run = hist(increments)
    want = oracle(run)
    got, code, detail = M.picard_noise_detail(run, ids, tau)
    check('noise_oracle_%04d' % n, (got is None) == (want is None) and (want is None or all(math.isclose(got[i], want[i], rel_tol=2e-13, abs_tol=2e-15) for i in ids)), code=code)

for name, seq in [('equal', [.003, .003]), ('growing', [.002, .003]), ('last_equal', [.004, .002, .002]),
                  ('previous_equal', [.004, .004, .002]), ('zero_to_nonzero', [0., .002])]:
    got, code, _ = M.picard_noise_detail(hist([[v] * 12 for v in seq]), ids, tau)
    check('NEW7_' + name, got is None and code == M.E_UNAVAILABLE_NONCONTRACTING)

inc = [[.01] + [.00009]*11, [.0001] + [.000081]*11]
got, code, detail = M.picard_noise_detail(hist(inc, {i: 0. for i in ids}), ids, tau)
check('A54_slow_same_sign_row', code is None and got[ids[1]] > .0007, value=got[ids[1]], enhanced_rows=detail['rows_where_per_row_bound_exceeds_norm_bound'])
for mode in ('missing_rows', 'index_gap'):
    raw = {'passes': [{'pass': k+1, 'rows': [{'id': i, 'speed_km_s': 1.} for i in ids]} for k in range(4)]}
    if mode == 'missing_rows':
        raw['passes'][1].pop('rows')
    else:
        raw['passes'][1]['pass'] = 8
    check('B4_' + mode, M.pass_rows_gap(raw) is not None)

def world():
    R = f['base_runs']()
    IDR = {n: f['identity_run'](n) for n in M.IDENTITY_RUNS}
    return R, IDR

def gate_eval(records, R, IDR, RP=None):
    rs = M.runs_sha_map(R, IDR, RP)
    original = M._read_json
    G = {}
    try:
        for name in M.ALL_GATES:
            rec = records.get(name)
            if rec is None:
                G[name] = M.evaluate_gate(name, None, ctx, rs)
            else:
                raw = json.dumps(rec, sort_keys=True).encode()
                M._read_json = lambda p, rec=rec, raw=raw: (copy.deepcopy(rec), hashlib.sha256(raw).hexdigest())
                G[name] = M.evaluate_gate(name, CMP, ctx, rs)
    finally:
        M._read_json = original
    return M.cross_gate_checks(G, R, RP)

def evaluate(R=None, IDR=None, RP=None, change_records=None, packets_bad=()):
    if R is None:
        R, IDR = world()
    RP = RP or {}
    records = f['complete_records'](R, IDR, RP, b0_c5h=True)
    if change_records:
        change_records(records)
    G = gate_eval(records, R, IDR, RP)
    packet = {k: {'V4': k not in packets_bad, 'V5': True} for k in list(R) + ['%s@RPAIR:%s' % (m, p) for p, rp in RP.items() for m in rp['_runs']]}
    try:
        result = M.evaluate_v007(ctx, R, IDR, G, RP, packet)
    except M.Refused as exc:
        result = {'decision': {'outcome': 'REFUSED_AT_LOAD'}, 'reason': str(exc)}
    return result, G

ev, G = evaluate()
check('baseline_manufactured_ADOPT', ev['decision']['outcome'] == 'ADOPT_TAIL', observed=ev['decision']['outcome'],
      invalid={k: v['failed'] for k, v in ev.get('validity', {}).items() if not v['valid_all']},
      gates={k: v['codes'] for k, v in G.items() if v['status'] != 'PASS'})
assert CHECKS[-1]['passed'], CHECKS[-1]

for lab in M.REGISTERED:
    for attack in ('missing', 'bad_receipt', 'bad_driver', 'flagged', 'noncontracting', 'pass_gap', 'packet'):
        if lab == M.C5H and attack == 'flagged':
            continue
        R, IDR = world()
        r = R[lab]
        packets_bad = ()
        if attack == 'missing':
            R[lab] = {'present': False, 'absent': 'SYNTHETIC_MISSING'}
        elif attack == 'bad_receipt':
            r['receipt']['result']['sha256'] = '0' * 64
        elif attack == 'bad_driver':
            r['result']['driver_sha256'] = '0' * 64
        elif attack == 'flagged':
            r['uvt_record'].update(flags=[M.FLAG_TSU], monitor_status='FLAGGED', M_T_accepted=.3)
        elif attack == 'noncontracting':
            r['pass_rows'] = hist([[.0005]*12, [.0005]*12], r['adapted']['rows'])['pass_rows']
        elif attack == 'pass_gap':
            r['pass_rows_gap'] = 'PASS_WITHOUT_ROWS'
        elif attack == 'packet':
            packets_bad = (lab,)
        ev, _ = evaluate(R, IDR, packets_bad=packets_bad)
        # Noncontracting is only a decidability obligation on selected pairs, plus RB_FP.
        requires = attack != 'noncontracting' or lab in set(sum([list(M.PAIRS[p]) for p in M.DECIDABILITY_PAIRS], [])) | {'C4T-A'}
        check('adoption_barrier_%s_%s' % (lab, attack), not requires or ev['decision']['outcome'] != 'ADOPT_TAIL', observed=ev['decision']['outcome'])

for gate in M.required_gates('parallel8'):
    ev, _ = evaluate(change_records=lambda records, gate=gate: records.__setitem__(gate, None))
    check('missing_gate_' + gate, ev['decision']['outcome'] != 'ADOPT_TAIL', observed=ev['decision']['outcome'])

for pid in M.DECIDABILITY_PAIRS:
    R, IDR = world()
    members = {m: copy.deepcopy(R[m]) for m in M.PAIRS[pid]}
    ev, _ = evaluate(R, IDR, {'%s' % pid: {'branch': 'PICARD', '_runs': members}})
    check('NEW17_' + pid, ev['decision']['outcome'] == 'REFUSED_AT_LOAD', observed=ev['decision']['outcome'])

# Direct member-validity probes preserve actual implementation and synthetic source custody.
R, IDR = world()
base = R['C4T']
key = 'C4T@RPAIR:T1_H'
member = f['make_run'](key, base['adapted']['rows'], numerics=copy.deepcopy(base['result']['normalized_spec']['numerics']))
member['result']['normalized_spec']['numerics']['picard'] = dict(M.RPAIR_PICARD)
f['a53_picard_shape'](member, base)
def member_validity(run):
    return M.case_validity(key, run, ctx, {'V4': True, 'V5': True}, {'status': 'PASS', 'per': {key: 'PASS'}},
                           None, {'base': 'C4T', 'branch': 'PICARD', 'base_run': base}, {})
v = member_validity(member)
check('A53_picard_base_outcome_and_parallel_worker', v['valid_all'], codes=v.get('V3_mismatch'), v6=v.get('V6_codes'))
for attack in ('outcome_sha', 'identity_sha', 'ro1', 'tail_record', 'nonleaf_numerics'):
    r = copy.deepcopy(member)
    if attack == 'outcome_sha': r['route_a_outcome']['result_sha256'] = '1' * 64
    if attack == 'identity_sha': r['adapted']['route_a_identity_sha256'] = '1' * 64
    if attack == 'ro1': r['route_a_outcome']['ro1']['worker_sha256'] = M.PIN_RO1_CUSTODY['worker'][1]
    if attack == 'tail_record': r['uvt_record']['M_T_accepted'] = .06
    if attack == 'nonleaf_numerics': r['result']['normalized_spec']['numerics']['route_a']['max_iterations'] = 33
    v = member_validity(r)
    check('A53_reject_' + attack, not v['valid_all'], codes=v.get('V3_mismatch'), v6=v.get('V6_codes'))

# Blinded labels: no numeric target values or raw attacker-controlled shell names.
for canary in ('x61.2345678', 'x612345678', 'speed_64.0', 'alpha', 'x1e7', 'x.456'):
    R, IDR = world()
    recs = f['complete_records'](R, IDR, b0_c5h=True)
    recs['RB_FP']['shells'] = [canary]
    recs['RB_FP']['dV_static_shells_km_s'] = {canary: [.5]*12}
    g = gate_eval(recs, R, IDR)['RB_FP']
    rendered = json.dumps(M.blinded_gate(g), sort_keys=True)
    check('blinded_shell_' + canary, canary not in rendered, rendered=rendered)

# Raw malformed history: duplicate and unknown ids should not be silently contracted.
RAW_HISTORY_OBSERVATIONS = []
for attack in ('duplicate_early_row', 'unknown_early_row', 'duplicate_last_row'):
    R, IDR = world()
    r = R['C6T']
    raw = {'passes': [{'pass': j+1, 'rows': [{'id': i, 'speed_km_s': row[i]} for i in ids]} for j, row in enumerate(r['pass_rows'])]}
    at = -1 if attack == 'duplicate_last_row' else 0
    if attack.startswith('duplicate'):
        raw['passes'][at]['rows'].insert(0, {'id': ids[0], 'speed_km_s': 999.})
    else:
        raw['passes'][at]['rows'].append({'id': 'UNKNOWN_SYNTHETIC', 'speed_km_s': 999.})
    r['result']['passes'] = raw['passes']
    r['pass_rows'] = M._pass_rows(raw)
    r['pass_rows_gap'] = M.pass_rows_gap(raw)
    ev, _ = evaluate(R, IDR)
    RAW_HISTORY_OBSERVATIONS.append(dict(attack=attack, pass_rows_gap=r['pass_rows_gap'], outcome=ev['decision']['outcome']))

summary = {'schema': 'UNT_CX2_COMPARE_R5_SOURCE_SYNTHETIC_REVIEW_V001',
           'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'date_u_literal': 'Sun Oct 18 12:35:46 UTC 2026 (earlier documentary read; final report records fresh date -u)',
           'priority_note': 'nice unavailable (sandbox); 0514 waiver', 'processes': 1,
           'numpy_threads': {k: os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')},
           'max_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'source_pins': PINS, 'source_stable_end': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() == s for p,s in PINS.items()},
           'manufactured_context': True, 'real_run_reads': False, 'launches': False,
           'limitations': ['No scientific records used', 'Gate reader virtualized in memory; real gate evaluator unchanged',
                           'Run-validity records constructed in memory; not full CLI custody validation', 'Packet V4/V5 supplied as fixture assertions; not replayed'],
           'fixture_functions_reused': sorted(names), 'checks': CHECKS,
           'raw_history_observations': RAW_HISTORY_OBSERVATIONS,
           'counts': {'total': len(CHECKS), 'passed': sum(x['passed'] for x in CHECKS)},
           'research_files_read': sorted(set(READS))}
dest = OUT / 'PROBE_RESULTS_CX2V001.json'
with dest.open('x') as handle:
    json.dump(summary, handle, sort_keys=True, indent=2, allow_nan=False)
    handle.write('\n')
print(json.dumps({'counts': summary['counts'], 'failed': [x for x in CHECKS if not x['passed']],
                  'raw_history_observations': RAW_HISTORY_OBSERVATIONS, 'max_rss_bytes': summary['max_rss_bytes_macos']}))
