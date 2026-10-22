"""Independent checker re-run (CHECK_V001): prep v009 vs prep v008 in-memory, and vs the SAVED route-A IDENTITY/START
of a saved prefix.  Operator evaluation only (prepare_inputs + one iteration-0 prepare); no iteration, no stage.
usage: python3 -I -B chk_prep_v009_repro.py RUN_DIR OUT_DIR"""
import hashlib, importlib.util, json, sys, time
from pathlib import Path
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
H = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers')
P9 = (EX / 'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py', 'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc')
CM = (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
SOL = (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644')
STR = (H / 'recovered_packet_audit/owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529')
BASE = (H / 'recovered_packet_audit/owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491')
def sha(p):
    h = hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def load(tag, p, s):
    assert sha(p) == s, ('PIN', p)
    sp = importlib.util.spec_from_file_location('chk_' + tag, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
def patch(m, pt):
    for k, v in pt['set'].items():
        setattr(m, k, Path(v['__path__']) if isinstance(v, dict) and '__path__' in v else v)
run, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=False)
t0 = time.time(); rep = {'run': str(run)}
req = json.loads((run / 'stages/01_route_a/request.json').read_text()); a = req['argv']
seed_p = Path(a[a.index('--seed') + 1]); assert sha(seed_p) == a[a.index('--seed-sha256') + 1]
ni = json.loads(seed_p.read_text())['numerical_inputs']
pt = req['module_patches'][0]; rep['saved_prep_sha256'] = pt['sha256']
cm = load('cm', *CM); sol = load('sol', *SOL)
p_old = load('pold', Path(pt['path']), pt['sha256']); patch(p_old, pt)
p_new = load('p9', *P9); patch(p_new, pt)
d_old = p_old.prepare_inputs(**ni); d_new = p_new.prepare_inputs(**ni)
keys = sorted(set(d_old) | set(d_new))
def _same(x, y):
    try:
        return cm.digest(x) == cm.digest(y)
    except Exception:
        if callable(x) and callable(y):
            cx, cy = getattr(x, '__code__', None), getattr(y, '__code__', None)
            return 'CALLABLE_CODE_EQUAL' if (cx is not None and cy is not None and cx.co_code == cy.co_code and cx.co_consts == cy.co_consts) else 'CALLABLE_CODE_DIFFERS'
        if isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y):
            sub = {kk: _same(x[kk], y[kk]) for kk in x}
            return True if all(v is True or v == 'CALLABLE_CODE_EQUAL' for v in sub.values()) else sub
        return 'UNDIGESTABLE_%s' % type(x).__name__
rep['v008_vs_v009_output_keys'] = {k: _same(d_old[k], d_new[k]) if k in d_old and k in d_new else 'MISSING' for k in keys if k != 'source_pins'}
rep['v008_vs_v009_source_pins_equal'] = d_old.get('source_pins') == d_new.get('source_pins')
del d_old
ident = json.loads((run / 'stages/01_route_a/checkpoint/IDENTITY.json').read_text())['identity']['inputs_sha256']
fa = d_new['fourier_arguments']; waves = fa['k_physical']
fixed = sol._supplied_fixed_source(d_new['fixed_source_fourier_J'], len(waves)); gas = sol.np.asarray(d_new['initial_gas_fourier_J'], dtype=complex)
idc = {'fixed_positions_m': cm.digest(d_new['fixed_positions_m']) == ident['fixed_positions_m'],
       'fixed_integrated_columns_J': cm.digest(d_new['fixed_integrated_columns_J']) == ident['fixed_integrated_columns_J'],
       'initial_gas_fourier_J': cm.digest(gas) == ident['initial_gas_fourier_J'],
       'fixed_source_fourier_J': cm.digest(fixed) == ident['fixed_source_fourier_J'],
       'gas_columns': cm.digest(d_new['gas_columns']) == ident['gas_columns']}
for k in sorted(set(fa) | set(ident['fourier_arguments'])):
    idc['fourier_arguments.' + k] = k in fa and cm.digest(fa[k]) == ident['fourier_arguments'].get(k)
extra = sorted(set(ident) - {'fixed_positions_m', 'fixed_integrated_columns_J', 'initial_gas_fourier_J', 'fixed_source_fourier_J', 'gas_columns', 'fourier_arguments'})
rep['identity'] = {'n': len(idc), 'equal': sum(bool(v) for v in idc.values()), 'differing': [k for k, v in idc.items() if not v], 'saved_keys_not_checked': extra}
stream = load('str', *STR); base = load('base', *BASE)
fac = stream.make_fourier_module(base_module=base, log_directory=out / 'nd', start_iteration=0)
cur = fixed + gas; prep = fac.prepare(**dict(fa), source_density_fourier=cur)
st = json.loads((run / 'stages/01_route_a/checkpoint/iteration_0000/START.json').read_text())
rep['start'] = {'gas': cm.digest(gas) == st['gas_fourier_J']['array_sha256'], 'current': cm.digest(cur) == st['current_source_fourier_J']['array_sha256'],
                'fixed': cm.digest(fixed) == st['fixed_source_fourier_J']['array_sha256'], 'wavevectors': cm.digest(prep['wavevectors']) == st['prepared_wavevectors']['array_sha256'],
                'weighted_responses': cm.digest(prep['weighted_responses']) == st['prepared_weighted_responses']['array_sha256'], 'prepared': cm.digest(prep) == st['prepared_metric_response_sha256']}
nd = run / 'stages/01_route_a/attempt_000/node_diagnostics'
rep['nodes'] = {n: sha(out / 'nd' / n) == sha(nd / n) for n in ('iteration_000000_nodes.jsonl', 'iteration_000000_scaled_nodes.jsonl')}
ok = all(v is True or v == 'CALLABLE_CODE_EQUAL' for v in rep['v008_vs_v009_output_keys'].values()) and rep['v008_vs_v009_source_pins_equal'] in (True,) and not rep['identity']['differing'] and all(rep['start'].values()) and all(rep['nodes'].values())
rep['verdict'] = 'PASS_BITWISE' if ok else 'FAIL'; rep['elapsed_s'] = round(time.time() - t0, 1)
(out / 'CHK_PREP_V009_REPRO.json').write_text(json.dumps(rep, indent=1, sort_keys=True))
print(json.dumps(rep))
