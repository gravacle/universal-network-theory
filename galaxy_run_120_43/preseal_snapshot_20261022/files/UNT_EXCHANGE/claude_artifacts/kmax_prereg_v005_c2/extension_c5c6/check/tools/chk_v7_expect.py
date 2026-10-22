"""Independent recompute of the V7 expectation (prep v009 operator evaluation of the per-call seed my own dry run produced).
usage: chk_v7_expect.py DRY_REPORT_DIR SMOKE_JSON OUT_DIR"""
import hashlib, importlib.util, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
H = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers')
PINS = {'cm': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'),
        'sol': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
        'str': (H / 'recovered_packet_audit/owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
        'base': (H / 'recovered_packet_audit/owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491')}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(t, p, s):
    assert sha(p) == s, p
    sp = importlib.util.spec_from_file_location('v7_' + t, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
dry, smoke, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=False)
t0 = time.time()
rep = json.loads((dry / 'DRYRUN_REPORT.json').read_text()); st = [s for s in rep['stages'] if s['name'] == 'route_a'][0]
a = st['argv']; seed_p = Path(a[a.index('--seed') + 1]); assert sha(seed_p) == a[a.index('--seed-sha256') + 1]
assert a[a.index('--seed-sha256') + 1] == smoke['seed']['sha256'], 'seed differs from smoke seed'
ni = json.loads(seed_p.read_text())['numerical_inputs']
pt = st['module_patches'][0]; lp = st['stage_dict_items']['LOCAL']['prep']
assert pt['sha256'] == lp['sha256'] == 'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc'
m = {k: load(k, *v) for k, v in PINS.items()}; cm, sol = m['cm'], m['sol']
prep = load('p9', Path(pt['path']), pt['sha256'])
for k, v in pt['set'].items(): setattr(prep, k, Path(v['__path__']) if isinstance(v, dict) and '__path__' in v else v)
d = prep.prepare_inputs(**ni); fa = d['fourier_arguments']
fixed = sol._supplied_fixed_source(d['fixed_source_fourier_J'], len(fa['k_physical'])); gas = sol.np.asarray(d['initial_gas_fourier_J'], dtype=complex)
e = smoke['expected_identity_inputs_sha256']
mine = {'fixed_positions_m': cm.digest(d['fixed_positions_m']), 'fixed_integrated_columns_J': cm.digest(d['fixed_integrated_columns_J']),
        'initial_gas_fourier_J': cm.digest(gas), 'fixed_source_fourier_J': cm.digest(fixed), 'gas_columns': cm.digest(d['gas_columns'])}
res = {'identity': {k: mine[k] == e[k] for k in mine}, 'fourier_arguments': {k: cm.digest(v) == e['fourier_arguments'].get(k) for k, v in fa.items()},
       'fa_keys_equal': sorted(fa) == sorted(e['fourier_arguments']), 'ni_max_iterations': ni['max_iterations'], 'ni_nodes': ni['fourier_points_per_axis']}
fac = m['str'].make_fourier_module(base_module=m['base'], log_directory=out / 'nd', start_iteration=0)
cur = fixed + gas; pr = fac.prepare(**dict(fa), source_density_fourier=cur); es = smoke['expected_start_iteration_0000']
res['start'] = {'gas_fourier_J': cm.digest(gas) == es['gas_fourier_J'], 'current_source_fourier_J': cm.digest(cur) == es['current_source_fourier_J'],
                'fixed_source_fourier_J': cm.digest(fixed) == es['fixed_source_fourier_J'], 'prepared_wavevectors': cm.digest(pr['wavevectors']) == es['prepared_wavevectors'],
                'prepared_weighted_responses': cm.digest(pr['weighted_responses']) == es['prepared_weighted_responses'], 'prepared_metric_response_sha256': cm.digest(pr) == es['prepared_metric_response_sha256']}
ok = all(res['identity'].values()) and all(res['fourier_arguments'].values()) and res['fa_keys_equal'] and all(res['start'].values())
res['verdict'] = 'PASS_BITWISE' if ok else 'FAIL'; res['elapsed_s'] = round(time.time() - t0, 1)
(out / 'CHK_V7_EXPECT.json').write_text(json.dumps(res, indent=1, sort_keys=True)); print(json.dumps(res))
