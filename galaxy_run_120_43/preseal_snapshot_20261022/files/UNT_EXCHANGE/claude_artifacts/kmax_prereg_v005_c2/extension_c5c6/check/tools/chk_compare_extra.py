"""Checker's own synthetic probes of kmax_compare_ext_c2v006.evaluate_ext (no file writes except OUT json)."""
import copy, importlib.util, json, sys
from pathlib import Path
HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/prereg_v006')
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
CX = load(HERE / 'kmax_compare_ext_c2v006.py', 'cx')
pre = json.loads((HERE / 'KMAX_MATRIX_PREREG_V006.json').read_text()); bi = pre['binding_inputs']
pre5 = json.loads(Path(bi['prereg_v005']['path']).read_text())
C5M = CX.load_pinned(bi['v005_compare']['path'], bi['v005_compare']['sha256'], 'c5m')
r3 = json.loads(Path(bi['r3_recovery']['path']).read_text())['brackets']
cases = {c['id']: c for c in pre['cases']}
real = {cid: C5M.adapt_result(cases[cid]['bound']['result']['path']) for cid in ('C4', 'C3', 'C2', 'R')}
ids = pre5['row_ids']; tau = dict(zip(ids, pre5['tau_km_s'])); v9 = bi['drivers']['v009']['sha256']
def synth(cid, base, mult, route_a=None):
    a = copy.deepcopy(real['C4']); gid = cases[cid]['grid']
    a['rows'] = {i: base[i] + mult * tau[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(ids)}
    a['driver_sha256'] = v9; a['grid_spec'] = pre['grids'][gid]['composite_grid_spec']
    ns = a['normalized_spec']; ns['numerics']['composite_grid_spec'] = a['grid_spec']
    ns['numerics']['route_a'] = route_a or {'column_workers': 8, 'max_iterations': 16}; ns['admit'] = {}
    return a
def run(d45, d56, c5ra=None, c4=None):
    ad = dict(real)
    if c4 is not None: ad['C4'] = c4
    c5 = synth('C5', real['C4']['rows'], d45, c5ra); c6 = synth('C6', c5['rows'], d56)
    ad['C5'], ad['C6'] = c5, c6
    return CX.evaluate_ext(pre, pre5, C5M, ad, {c: {'V4': True, 'V5': True} for c in ad}, r3, {'admissible': True}, {c: {'V7': True} for c in ('C5', 'C6')})
out = {}
e = run(0.8, 0.3, c5ra={'column_workers': 8, 'max_iterations': 32})
out['P1_MAXIT32_per_V1iii_next_step'] = {'outcome': e['decision']['outcome'], 'C5_failed': e['gates']['C5']['failed'], 'V3': e['gates']['C5']['V3_mismatch']}
e = run(1.5, 0.9)
out['P2_d45_1p5_d56_0p9'] = {'outcome': e['decision']['outcome'], 'subtype': e['decision'].get('subtype')}
c3_as_c4 = copy.deepcopy(real['C3'])
e = run(0.8, 0.3, c4=c3_as_c4)
out['P3_C3_result_in_C4_slot'] = {'outcome': e['decision']['outcome'], 'C4_failed': e['gates']['C4']['failed'], 'V3': e['gates']['C4'].get('V3_mismatch')}
e = run(5.0, 1.0)
out['P4_d45_5_d56_1_exact'] = {'outcome': e['decision']['outcome'], 'subtype': e['decision'].get('subtype')}
e = run(4.94, 1.96)
out['P5_geometric_q0p3965_projection'] = {'outcome': e['decision']['outcome'], 'subtype': e['decision'].get('subtype')}
Path(sys.argv[1]).write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))
