"""verify_newdefects_2: are the C-1.1 stop inputs of a v003g-format score independent of the target rows?

Synthetic data only. The v003g module is NOT imported: the five pure helpers are extracted with ast
from the module bytes (sha256 checked first) and exec'd in a fresh namespace. An audit hook then
refuses every open except the module path (read) and this folder's output file (write), and refuses
any path with a forbidden name class. No subprocess, no network.

Question 1: do the fields the C-1.1 stops read (row key sets, ids and order, reference-member row
status, envelope label) differ between two synthetic target sets? If not, a stop that passes on a
v003g-format synthetic score also passes on the real one, and no post-target stop can fire.
Question 2: does the E3 value (C-5.3) differ between those target sets while every stop input is
identical? If yes, the post-target NOT_READ of C-1.1 L132 is available exactly when the outcome is known.
"""
import ast, hashlib, json, math, sys

MODULE = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
          'prediction_freeze_c2v003g_cx3v001.py')
MODULE_SHA = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
OUT = sys.argv[1]
FORBIDDEN = ('rotmod', 'vobs', 'massmodels', 'sparc', 'runs_ext', 'kmax_a2f10_c5h_run_v001', 'uvt_')
EVENTS = []

def hook(event, args):
    if event == 'open':
        p = str(args[0]); low = p.lower(); mode = str(args[1]) if len(args) > 1 else 'r'
        if any(t in low for t in FORBIDDEN):
            EVENTS.append(('FORBIDDEN', p)); raise PermissionError('fence: forbidden name class')
        if p == MODULE and ('w' not in mode and 'a' not in mode and '+' not in mode):
            return
        if p == OUT and ('w' in mode or 'x' in mode):
            return
        EVENTS.append(('REFUSED', p, mode)); raise PermissionError('fence: path not allowlisted')
    if event in ('subprocess.Popen', 'os.system', 'socket.connect', 'os.exec', 'os.posix_spawn'):
        EVENTS.append(('REFUSED', event)); raise PermissionError('fence: ' + event)

sys.addaudithook(hook)

with open(MODULE, 'rb') as fh:
    raw = fh.read()
sha = hashlib.sha256(raw).hexdigest()
assert sha == MODULE_SHA, sha
tree = ast.parse(raw.decode('utf-8'))
WANT = ['_median', '_ladder_row', '_score_members', '_band_rows', '_pointwise_envelope']
ns = {'math': math, 'ENVELOPE_LABEL': 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'}
found = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in WANT:
        node.decorator_list = []
        found[node.name] = ast.get_source_segment(raw.decode('utf-8'), node)
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<v003g:%s>' % node.name, 'exec'), ns)
assert set(found) == set(WANT), sorted(found)

N = 43
ids = ['SYN-Q%02d' % (j + 1) for j in range(N)]          # synthetic ids; zone by index only
OUTER = list(range(35, 43))                               # positions 36..43, the registered OUTER set by position
INVALID_POS = {0: 'QUERY_INSIDE_INNERMOST_NODE', 1: 'QUERY_INSIDE_INNERMOST_NODE'}

def member(log_index, offset):
    sp, rv, rg = [], [], []
    for j in range(N):
        if j in INVALID_POS:
            sp.append(None); rv.append(False); rg.append({'reason': INVALID_POS[j]})
        else:
            sp.append(1000.0 + 10.0 * j + offset); rv.append(True); rg.append(None)
    return {'member_id': 'SYN-M%d' % log_index, 'log_index': log_index, 'role': 'representative',
            'evaluated': True, 'member_valid': True, 'speeds_km_s': sp, 'row_valid': rv, 'row_registration': rg}

members = [member(0, -3.0), member(1, 0.0), member(2, +3.0)]
REF = 'SYN-M1'
env_rows = ns['_pointwise_envelope'](members, ids)

def targets(kind):
    out = []
    for j in range(N):
        p = 1000.0 + 10.0 * j                              # the reference member's synthetic prediction
        if kind == 'T1_all_hit':
            out.append((p, 2.0))
        elif kind == 'T2_outer_deficit':                  # model 10 sigma below on every OUTER row
            out.append((p + 20.0 if j in OUTER else p, 2.0))
        elif kind == 'T3_nonfinite_ratio':                # one row with a ratio that overflows
            out.append((p - 1.0, 5e-324) if j == 40 else (p + 20.0 if j in OUTER else p, 2.0))
    return out

def stop_inputs(score_members, band):
    ref = next(m for m in score_members if m['member_id'] == REF)
    return {
        'member_row_key_sets': [sorted({tuple(sorted(r.keys())) for r in m['rows']}) for m in score_members],
        'ref_ids_in_order': [r['id'] for r in ref['rows']] == ids,
        'ref_row_status': [r['status'] for r in ref['rows']],
        'envelope_row_key_sets': sorted({tuple(sorted(r.keys())) for r in band}),
        'envelope_label': sorted({r['label'] for r in band}),
        'ref_any_unevaluated_or_refused': any(r['status'] == 'UNEVALUATED_OR_REFUSED' for r in ref['rows']),
    }

def e3(score_members):
    ref = next(m for m in score_members if m['member_id'] == REF)
    rows = [ref['rows'][j] for j in OUTER if ref['rows'][j]['score_status'] != 'INVALID_AS_MISS']
    nv = len(rows); m = sum(r['score_status'] == 'MISS' for r in rows)
    if nv == 0:
        return {'value': 'NOT_TESTABLE', 'N_v': 0, 'M': 0}
    fail = m >= nv / 2.0
    return {'value': 'TESTED-NEGATIVE' if fail else 'NOT_NEGATIVE_AT_OUTER', 'N_v': nv, 'M': m}

results = {}
for kind in ('T1_all_hit', 'T2_outer_deficit', 'T3_nonfinite_ratio'):
    bound = targets(kind)
    sm = ns['_score_members'](members, ids, bound)
    band, n_ov, n_inv = ns['_band_rows'](env_rows, 'band_low_km_s', 'band_high_km_s', ids, bound)
    si = stop_inputs(sm, band)
    ref = next(m for m in sm if m['member_id'] == REF)
    results[kind] = {
        'stop_inputs_sha256': hashlib.sha256(json.dumps(si, sort_keys=True).encode()).hexdigest(),
        'stop_inputs': si,
        'row_key_set_union': sorted({k for m in sm for r in m['rows'] for k in r.keys()}),
        'outcome': {'e3': e3(sm), 'ref_within_error_count': ref['within_error_count'],
                    'ref_outer_sigma_ratio': [ref['rows'][j]['sigma_ratio'] for j in OUTER],
                    'ref_row_notes_nonempty': {ref['rows'][j]['id']: ref['rows'][j]['row_notes']
                                               for j in range(N) if ref['rows'][j]['row_notes']},
                    'n_band_overlap': n_ov},
    }

shas = {k: v['stop_inputs_sha256'] for k, v in results.items()}
summary = {
    'module_sha256': sha, 'helpers_extracted': WANT,
    'synthetic': 'ids SYN-Q01..SYN-Q43; predictions 1000+10j km/s; sigma 2 km/s (T3: one row 5e-324); implausible by design',
    'stop_inputs_identical_across_targets': len(set(shas.values())) == 1,
    'row_key_set_identical_across_targets': len({tuple(v['row_key_set_union']) for v in results.values()}) == 1,
    'e3_values': {k: v['outcome']['e3']['value'] for k, v in results.items()},
    'e3_differs_while_stop_inputs_identical': len({v['outcome']['e3']['value'] for v in results.values()}) > 1 and len(set(shas.values())) == 1,
    'fence_events': EVENTS,
    'results': results,
}
with open(OUT, 'w') as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
print(json.dumps({k: summary[k] for k in ('stop_inputs_identical_across_targets', 'row_key_set_identical_across_targets',
                                           'e3_values', 'e3_differs_while_stop_inputs_identical', 'fence_events')}, indent=1))
