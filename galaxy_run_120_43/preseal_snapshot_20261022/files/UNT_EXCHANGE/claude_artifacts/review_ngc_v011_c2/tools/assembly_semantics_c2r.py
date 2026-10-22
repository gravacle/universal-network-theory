"""Claude2-review independent result-assembly semantics check: v009 parent vs v010 r4 vs v011 cx3v003.
Own method (not Codex3's compare_ngc_results):
  1. the cmd_run result-assembly block (`if final is None:` inside cmd_run) is extracted by AST from each driver and its
     unparsed source text compared across the three drivers (so any semantic difference must come from callees);
  2. that block is executed against a matrix of synthetic final-pass dicts with each driver's OWN final_rows_check, and
     the science fields of the assembled result (valid, reasons, rows, speeds_km_s, invalid_rows, headline_rule) compared;
  3. every case is pre-labelled INTENDED_DIFF (contains a well-formed QUERY_BEYOND_OUTER_GAS_CUT row) or MUST_EQUAL; the
     verdict is whether the observed difference set equals the intended set, plus a list of semantic widenings found.
usage: assembly_semantics_c2r.py OUT_JSON
"""
import ast
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
DRIVERS = {'v009': (A / 'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py', '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'),
           'v010r4': (A / 'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py', 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'),
           'v011': (A / 'ngc_route_tail_readiness_cx3/v011/galaxy_m0_forward_c2v011_cx3v003.py', 'd120eead0e424d5ae0c2e4854377f2808f258646a7fefdaba5c66f105f5e610b')}
SCI = ('valid', 'reasons', 'rows', 'speeds_km_s', 'invalid_rows', 'headline_rule', 'final_pass', 'picard_bound_met')
OUT = 'QUERY_BEYOND_OUTER_GAS_CUT'; IN = 'QUERY_INSIDE_INNERMOST_NODE'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p, name):
    s = importlib.util.spec_from_file_location(name, str(p)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def block(path):
    run = next(n for n in ast.parse(Path(path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'cmd_run')
    return next(n for n in ast.walk(run) if isinstance(n, ast.If) and ast.unparse(n.test) == 'final is None')


def assemble(mod, blk, final, galaxy='NGC3198'):
    nspec = {'physical': {'entropy_K_member': 'N4_PRIMARY_64_OVER_121'}, 'numerics': {'picard': {'speed_change_bound_km_s': .01}}}
    result = {'valid': False, 'reasons': []}
    env = {'result': result, 'final': final, 'nspec': nspec, 'g': {'n_queries': 43 if galaxy == 'NGC3198' else 12},
           'ctx': SimpleNamespace(passes=[final]), 'final_rows_check': mod.final_rows_check, 'harmonic_diagnostic': mod.harmonic_diagnostic}
    try:
        exec(compile(ast.Module(body=[blk], type_ignores=[]), '<assembly>', 'exec'), env)
    except Exception as e:
        return {'EXCEPTION': '%s: %s' % (type(e).__name__, e)}
    return {k: result.get(k) for k in SCI}


def rows_ngc():
    return [{'id': 'NGC3198-Q%02d' % i, 'speed_km_s': 50. + i, 'valid': True} for i in range(1, 44)]


def inval(r, reason, speed=None):
    r.update(valid=False, speed_km_s=speed, reason=reason)


def cases():
    c = {}
    f0 = {'pass': 4, 'rows': rows_ngc(), 'column_failures': [], 'rotation_positive': True, 'max_abs_change_km_s': .004}
    c['all_valid'] = (copy.deepcopy(f0), False)
    f = copy.deepcopy(f0); [inval(r, IN) for r in f['rows'][:2]]; c['gl4_inner_Q01_Q02'] = (f, False)
    f = copy.deepcopy(f0); [inval(r, OUT) for r in f['rows'][-2:]]; c['outer_cut_Q42_Q43'] = (f, True)
    f = copy.deepcopy(f0); [inval(r, IN) for r in f['rows'][:2]]; [inval(r, OUT) for r in f['rows'][-5:]]; c['inner_plus_outer'] = (f, True)
    # well-formed rows but semantically impossible for a radial cut: an interior row beyond-cut, outer rows valid
    f = copy.deepcopy(f0); inval(f['rows'][19], OUT); c['outer_reason_on_interior_row_Q20_only'] = (f, True)
    f = copy.deepcopy(f0); [inval(r, OUT) for r in f['rows']]; c['all_rows_outer_cut'] = (f, False)
    f = copy.deepcopy(f0); inval(f['rows'][-1], OUT, speed=70.); c['outer_reason_with_finite_speed'] = (f, False)
    f = copy.deepcopy(f0); inval(f['rows'][-1], 'QUERY_FOO'); c['unregistered_reason'] = (f, False)
    f = copy.deepcopy(f0); f['rows'][-1]['reason'] = OUT; c['valid_row_with_outer_reason'] = (f, False)
    f = copy.deepcopy(f0); inval(f['rows'][-1], OUT); f['rows'][-1]['valid'] = None; c['outer_reason_valid_None'] = (f, False)
    f = copy.deepcopy(f0); f['rows'] = f['rows'][:-1]; c['42_rows'] = (f, False)
    f = copy.deepcopy(f0); [inval(r, OUT) for r in f['rows'][-2:]]; f['rows'][0]['id'] = 'DDO154-R01'; c['mixed_ids_outer_cut'] = (f, False)
    f = copy.deepcopy(f0); f['column_failures'] = [{'i': 3}]; [inval(r, OUT) for r in f['rows'][-2:]]; c['outer_cut_with_column_failure'] = (f, True)
    return c


def main():
    out = Path(sys.argv[1]); assert not out.exists()
    mods, blocks = {}, {}
    for k, (p, s) in DRIVERS.items():
        assert sha(p) == s, k
        mods[k] = load(p, 'asm_' + k); blocks[k] = block(p)
    texts = {k: ast.unparse(b) for k, b in blocks.items()}
    block_equal = {'v009_eq_v010r4': texts['v009'] == texts['v010r4'], 'v010r4_eq_v011': texts['v010r4'] == texts['v011']}
    res = []
    for name, (final, intended) in cases().items():
        r = {k: assemble(mods[k], blocks[k], copy.deepcopy(final)) for k in DRIVERS}
        d09_11 = r['v009'] != r['v011']; d10_11 = r['v010r4'] != r['v011']; d09_10 = r['v009'] != r['v010r4']
        res.append({'case': name, 'intended_v011_difference': intended, 'differs_v009_v011': d09_11, 'differs_v010r4_v011': d10_11,
                    'differs_v009_v010r4': d09_10, 'as_intended': d09_11 == intended and not d09_10,
                    'v009_valid': r['v009'].get('valid'), 'v011_valid': r['v011'].get('valid'),
                    'v011_invalid_rows': r['v011'].get('invalid_rows'), 'v011_headline_rule': r['v011'].get('headline_rule'),
                    'v011_reasons': r['v011'].get('reasons'), 'v009_reasons': r['v009'].get('reasons')})
    widen = [x['case'] for x in res if x['case'] in ('outer_reason_on_interior_row_Q20_only',) and x['v011_valid'] is True]
    rec = {'schema': 'ASSEMBLY_SEMANTICS_C2R_V001', 'drivers': {k: {'path': str(p), 'sha256': s} for k, (p, s) in DRIVERS.items()},
           'assembly_block_text_equal': block_equal, 'cases': res,
           'all_as_intended': all(x['as_intended'] for x in res),
           'semantic_widening_accepted_by_v011': widen,
           'tool': {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)}}
    with out.open('x') as f:
        json.dump(rec, f, indent=1, default=str)
    print(json.dumps(block_equal))
    for x in res:
        print('%-40s intended=%-5s d09_11=%-5s d09_10=%-5s ok=%-5s v009=%-5s v011=%-5s inv=%s' % (
            x['case'], x['intended_v011_difference'], x['differs_v009_v011'], x['differs_v009_v010r4'], x['as_intended'],
            x['v009_valid'], x['v011_valid'], x['v011_invalid_rows']))
    print('widening', widen)


if __name__ == '__main__':
    main()
