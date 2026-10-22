"""Claude3 0586: validate PRODUCER_REGISTRY_C3V001 with compare r11's OWN loader (producer_registry_from_obj, files hashed from
bytes) and evaluate_gate on every real pre-seal record, in a context with the REAL case block built from the ten FILLED CX1V004
specs' DRY_R5_MS128_V004 normalized numerics (route-A mode parallel8, drivers [r5]). Compare r10 runs unmodified through Claude3's
guarded loader (registered C5H redirected to a stand-in). Anything that does not PASS is REPORTED, not patched.
usage: PY -I -B this REGISTRY_JSON OUT_JSON"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_c3/r11_review/c3'); import r11_loader_c3 as L
R = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/'
M, T = L.load(R + 'kmax_tail_compare_c2v007_r11.py', 'a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a',
              R + 'tests_kmax_tail_compare_c2v007_r11.py', '3cbafa98c07e098d9f569fa5003174ec827f01eb0f19e3fce653786f1611be42', 'cmp7r11')
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'; PKT = A + 'v007_launch_packet_cx1/'
sha = lambda b: hashlib.sha256(b).hexdigest()
reg_raw = Path(sys.argv[1]).read_bytes(); reg_obj = json.loads(reg_raw)
out = {'registry': {'path': sys.argv[1], 'sha256': sha(reg_raw)}, 'compare': 'r11 a5d10cb1'}
try:
    REG = M.producer_registry_from_obj(reg_obj, sha=sha(reg_raw), path=sys.argv[1]); out['registry_load'] = 'LOADED (r11 producer_registry_from_obj, verify_bytes)'
except SystemExit as exc:
    out['registry_load'] = 'REFUSED %s %s' % (getattr(exc, 'refusal_code', ''), str(exc)[:300]); json.dump(out, open(sys.argv[2], 'x'), indent=1); print(out); sys.exit(0)
dry = json.loads(Path(PKT + 'DRY_R5_MS128_V004.json').read_bytes())
assert dry['driver']['sha256'] == M.PIN_DRIVER_V010_R5[1]
nums = {}
for c in dry['checks']:
    b = Path(c['report']['path']).read_bytes(); assert sha(b) == c['report']['sha256'] and c['passed'] and c['executed_stages'] == 0
    nums[c['case']] = json.loads(b)['normalized_spec']['numerics']
LIB = M.load_uvt_lib()
cb = {'schema': M.CASE_BLOCK_SCHEMA, 'route_a_mode': 'parallel8', 'cases': {}}
for lab in M.REGISTERED:
    e = {'grid': M.EXPECTED_GRID[lab], 'truncation': M.EXPECTED_TRUNCATION[lab], 'normalized_spec_equal': {}}
    if lab == M.C5H:
        e.update(tail=False, ro1_required=False, call_spec_sha256=M.PIN_C5H_SPEC[1], drivers_allowed=[M.DRIVER_V009_EXT])
    else:
        n = nums[lab]; e.update(tail=True, ro1_required=True, uv_tail_config_sha256=LIB.normalize_config(n['uv_tail'])['sha256'],
                              drivers_allowed=[M.PIN_DRIVER_V010_R5[1]], normalized_spec_equal={'/numerics': n})
    cb['cases'][lab] = e
why = M.validate_case_block(cb, route_a_mode='parallel8'); out['case_block_refusals'] = why
ctx = M.build_context('parallel8', cb, REG)
def ev(g, p):
    try:
        r = M.evaluate_gate(g, str(p), ctx, {})
        return {'status': r.get('status'), 'codes': r.get('codes', [])[:6]}
    except SystemExit as exc:
        return {'status': 'REFUSED', 'codes': [getattr(exc, 'refusal_code', str(exc)[:120])]}
    except Exception as exc:
        return {'status': 'EXCEPTION', 'codes': ['%s: %s' % (type(exc).__name__, str(exc)[:160])]}
recs = {g: v[0] if isinstance(v, list) and v else None for g, v in reg_obj['gate_records'].items()}
cands = {'EPS': A + 'tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json', 'LO': A + 'tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json',
         'GQ': A + 'producer_registry_c3/out/GQ_CERT_V006.json', 'LO_NGC': A + 'tail_scheme_impl_c2/certificates_v002/gates/LO_NGC_CERT_V002.json', 'DOUBLING': A + 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json'}
out['preseal_records'] = {g: dict(path=p, sha256=sha(Path(p).read_bytes()), **ev(g, p)) for g, p in cands.items()}
# reported (not registered) candidates, to show why they cannot be registered as they stand
rep = {'GQ V005 (fbceefe6, the superseded record of record)': ('GQ', A + 'tail_scheme_impl_c2/certificates_v003/gates/GQ_CERT_V005_MS128.json'),
       'B3 (GATE_B3_C4_V002.md, 465cb3c3)': ('B3', A + 'gate_b3_c4/GATE_B3_C4_V002.md'),
       'SR_K (SR_K_CONTRACT_SYNTHETIC_V001, synthetic)': ('SR_K', PKT + 'SR_K_CONTRACT_SYNTHETIC_V001.json')}
out['unregistered_candidates'] = {k: dict(path=p, sha256=sha(Path(p).read_bytes()), **ev(g, p)) for k, (g, p) in rep.items()}
out['all_registered_preseal_pass'] = all(v['status'] == 'PASS' for v in out['preseal_records'].values())
out['guard_refused'] = L.GUARD['refused']
json.dump(out, open(sys.argv[2], 'x'), indent=1)
print('registry:', out['registry_load']); print('case block refusals:', why)
for g, v in out['preseal_records'].items(): print('  ', g, v['status'], v['codes'])
for g, v in out['unregistered_candidates'].items(): print('  [cand]', g, v['status'], v['codes'][:3])
print('ALL REGISTERED PRE-SEAL PASS:', out['all_registered_preseal_pass'], '| guard refused', L.GUARD['refused'])
