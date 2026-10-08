"""Inert equation-level attribution control; unchanged material, stdout only.

Only root runs this producer. Lambda=0 is NOT a second consistent action.
The frozen Newton algorithm is reused by temporary in-memory dispatch;
neither original source file nor its configuration is changed.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import sys
sys.dont_write_bytecode = True
import base64
import hashlib
import json
from pathlib import Path
import resource
import time
import zlib
import numpy as np
import clamped_common_phase_patch_v001 as original

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE/'CLAMPED_HARD_REACTION_ATTRIBUTION_V001_FROZEN.json'
PHYSICAL_EVALUATE = original.evaluate
CONFIG = dict(original_case_indices=[0, 2, 4, 6], hard_reaction_multiplier=0.,
    seed_policy='Original two fixed guesses; saved physical solution is never a seed.',
    algorithm_configuration=original.CONFIG,
    comparison_gate='None; failed iterates retained and labeled separately.',
    scope='Equation-level hard-source-removal counterfactual, not a consistent action.')


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    selected, globalp, local, ancestor = original.inputs()
    if json.loads(original.FREEZE.read_text()) != ancestor:
        raise RuntimeError('Original prospective freeze differs')
    files = dict(ancestor['files'])

    def add(path):
        path = path.resolve(strict=True)
        path.relative_to(ROOT)
        files[str(path.relative_to(ROOT))] = sha(path)
        return path

    add(original.FREEZE)
    saved = {}
    receipts = {}
    labels = [(R, L, n) for R in original.CONFIG['R']
              for L in original.CONFIG['L'] for n in original.CONFIG['N']]
    for index in CONFIG['original_case_indices']:
        path = add(HERE/f'CLAMPED_COMMON_PHASE_PATCH_V001_CASE_{index:03d}.json')
        transport = json.loads(path.read_text())
        if transport.get('encoding') != 'zlib_base64_canonical_json':
            raise RuntimeError('Invalid physical result encoding')
        decoder = zlib.decompressobj()
        raw = decoder.decompress(base64.b64decode(transport['data'], validate=True))+decoder.flush()
        if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
            raise RuntimeError('Invalid physical compression stream')
        if len(raw) != transport['raw_bytes'] or hashlib.sha256(raw).hexdigest() != transport['raw_sha256']:
            raise RuntimeError('Physical raw result changed')
        wrapper = json.loads(raw)
        payload = wrapper['payload']
        if (wrapper['freeze_sha256'] != sha(original.FREEZE)
                or wrapper['payload_sha256'] != hashlib.sha256(encode(payload)).hexdigest()):
            raise RuntimeError('Physical result wrapper changed')
        if (payload['case_index'] != index
                or (payload['R'], payload['L'], payload['n']) != labels[index]
                or payload['configuration'] != original.CONFIG):
            raise RuntimeError('Physical case/configuration differs')
        if [o['seed_multiplier'] for o in payload['outcomes']] != [1., 2.]:
            raise RuntimeError('Physical retained seed census differs')
        saved[index] = payload
        receipts[index] = dict(path=str(path.relative_to(ROOT)),
            transport_sha256=sha(path), raw_sha256=transport['raw_sha256'],
            payload_sha256=wrapper['payload_sha256'])
    for name in [Path(__file__).name, 'CLAMPED_HARD_REACTION_ATTRIBUTION_PROTOCOL_V001.md',
                 'CLAMPED_HARD_REACTION_COUNTERFACTUAL_V001.md']:
        add(HERE/name)
    snapshot = dict(configuration=CONFIG, files=files,
                    original_freeze_sha256=sha(original.FREEZE))
    return selected, globalp, local, saved, receipts, snapshot


def evaluate(u, geo, mat, eps, order=128, jacobian=False, newtonian=False):
    """Keep exact original flux/material, remove only the hard volume source."""
    if newtonian:
        return PHYSICAL_EVALUATE(u, geo, mat, eps, order, jacobian, True)
    out = PHYSICAL_EVALUATE(u, geo, mat, eps, order, False, False)
    cell, face = out['cell'], out['face']
    out['physical_residual'] = out['residual'].copy()
    out['physical_volume_source'] = out['volume_source']
    out['physical_flux_balance'] = out['flux_balance']
    removed = eps/mat.Kb*cell['deltaT_hard']
    soft_source = eps/mat.Kb*cell['deltaT_soft']
    # Assemble afresh, rather than cancel two large reaction contributions.
    out['residual'] = geo.divergence(out['flux'])-soft_source
    out['norm'] = float(np.sum(np.abs(geo.volume*out['residual'])))/out['sheet_flux']
    out['removed_hard_source'] = removed
    out['removed_hard_volume_source'] = float(np.dot(geo.volume, removed))
    out['volume_source'] = float(np.dot(geo.volume, soft_source))
    out['flux_balance'] = out['outer_flux']-out['sheet_flux']-out['volume_source']
    if not jacobian:
        return out

    # Same frozen flux Jacobian, built without subtracting the cold J term.
    fr, fz, fg = out['fr'], out['fz'], out['fg']
    er = np.divide(fr, fg, out=np.zeros_like(fr), where=fg>0)
    ez = np.divide(fz, fg, out=np.zeros_like(fz), where=fg>0)
    en = np.where(geo.axis == 0, er, ez)
    normal_map = np.where((geo.axis == 0)[:, None], geo.XR, geo.XZ)
    df = (face['KT']/mat.Kb)[:, None]*normal_map
    df += ((face['KL']-face['KT'])*en/mat.Kb)[:, None]*(er[:, None]*geo.XR+ez[:, None]*geo.XZ)
    df -= (eps*face['F_Phi']*en/mat.Kb)[:, None]*geo.P
    J = np.zeros((geo.size, geo.size))
    term = geo.face_area[:, None]*df
    np.add.at(J, geo.left, term)
    np.add.at(J, geo.right[geo.internal], -term[geo.internal])
    J /= geo.volume[:, None]
    cg = out['cg']
    er = np.divide(out['cr'], cg, out=np.zeros_like(cg), where=cg>0)
    ez = np.divide(out['cz'], cg, out=np.zeros_like(cg), where=cg>0)
    soft = mat._soft(cell['h'])
    Fsoft = cell['h_prime']*cell['h']*soft['B_over_h']
    J -= (2*eps*Fsoft/mat.Kb)[:, None]*(er[:, None]*geo.GR+ez[:, None]*geo.GZ)
    out['jacobian'] = J
    out['Fsoft'] = Fsoft
    return out


def comparison(a, b, weights):
    """Second minus first; descriptive, not an acceptance criterion."""
    a, b, weights = np.asarray(a), np.asarray(b), np.asarray(weights)
    if a.shape != b.shape or a.shape != weights.shape or not np.all(np.isfinite(a+b)):
        raise RuntimeError('Invalid same-grid comparison')
    total = float(np.sum(weights))
    rms = lambda value: float(np.sqrt(np.sum(weights*value*value)/total))
    first, second, difference = rms(a), rms(b), rms(b-a)
    scale = (first+second)/2
    return dict(weighted_RMS_difference=difference,
        symmetric_relative_RMS=difference/scale if scale else 0.,
        max_absolute_difference=float(np.max(np.abs(b-a))),
        signed_difference_range=[float(np.min(b-a)), float(np.max(b-a))],
        first_RMS=first, second_RMS=second)


def run_case(index, selected, globalp, local, saved, receipts):
    start = time.perf_counter()
    old_index = CONFIG['original_case_indices'][index]
    physical = saved[old_index]
    # Sole-worker scoped dispatch: reuse original Newton, line search,
    # seed/case controls and result construction without changing their files.
    if original.evaluate is not PHYSICAL_EVALUATE:
        raise RuntimeError('Unexpected evaluator dispatch')
    original.evaluate = evaluate
    try:
        result = original.run_case(old_index, selected, globalp, local)
    finally:
        original.evaluate = PHYSICAL_EVALUATE

    result['attribution_configuration'] = CONFIG
    result['attribution_case_index'] = index
    result['physical_result_custody'] = receipts[old_index]
    result['physical_case_control_failures'] = physical['failures']
    result['scope'] = ('Hard volume-source removal only; full phase/flux and all recorded energy remain. '
        'Lambda=0 is an action-inconsistent diagnostic, not a viable alternative model or fitted galaxy.')
    geo = original.Geometry(result['n'], result['L'])
    mat = original.material.Material(selected[result['R']], globalp['spectra'][1]['spectrum'],
                                     beta=.005, chunk_size=256)
    eps = result['epsilon_scale']
    weights = geo.volume.reshape(geo.n, geo.n)
    pairs = []

    def check(name, error, tolerance):
        passed = bool(np.isfinite(error) and error <= tolerance)
        result['checks'][name] = dict(error=float(error), tolerance=tolerance, passed=passed)
        if not passed:
            result['failures'].append(name)

    for outcome in result['outcomes']:
        seed = outcome['seed_multiplier']
        old = next(o for o in physical['outcomes'] if o['seed_multiplier'] == seed)
        pair = dict(seed=seed, physical_solver_status=old['status'],
            counterfactual_solver_status=outcome['status'],
            physical_jacobian_qualified=old.get('jacobian_qualified', False),
            counterfactual_jacobian_qualified=outcome.get('jacobian_qualified', False))
        u = np.asarray(outcome['u']).ravel()
        metrics = {'u': comparison(old['u'], outcome['u'], weights)}
        for name in ['radial', 'vertical']:
            if 'gradients' in old and 'gradients' in outcome:
                metrics[name+'_G'] = comparison(old['gradients'][name], outcome['gradients'][name], weights)
                metrics[name+'_m_s2'] = comparison(
                    mat.gstar*np.asarray(old['gradients'][name]),
                    mat.gstar*np.asarray(outcome['gradients'][name]), weights)
        for name in ['I', 'I_over_Ib', 'deltaT_hard', 'deltaT_soft', 'deltaT', 'hard_E', 'hard_Pi']:
            if 'material' in old and 'material' in outcome:
                metrics[name] = comparison(old['material'][name], outcome['material'][name], weights)
        pair['metrics_physical_to_counterfactual'] = metrics
        if 'material' in outcome:
            state = evaluate(u, geo, mat, eps, jacobian=True)
            full = PHYSICAL_EVALUATE(u, geo, mat, eps, jacobian=True)
            removed = state['removed_hard_source']
            scale = max(state['sheet_flux'], abs(state['volume_source']),
                        abs(state['physical_volume_source']), 1e-300)
            difference = state['residual']-full['residual']-removed
            check(f'seed{seed}_exact_removed_source_identity',
                float(np.sum(np.abs(geo.volume*difference)))/scale,
                original.CONFIG['arithmetic_tolerance'])
            check(f'seed{seed}_exact_removed_flux_identity',
                abs(full['flux_balance']-state['flux_balance']+state['removed_hard_volume_source'])/scale,
                original.CONFIG['arithmetic_tolerance'])
            cg = state['cg']
            er = np.divide(state['cr'], cg, out=np.zeros_like(cg), where=cg>0)
            ez = np.divide(state['cz'], cg, out=np.zeros_like(cg), where=cg>0)
            cell = state['cell']
            hard_dTg = 2*(cell['F']-state['Fsoft'])-cell['F_Phi']
            corrected = full['jacobian'].copy()
            corrected[np.diag_indices(geo.size)] -= eps*eps*cell['J']/mat.Kb
            corrected += (eps*hard_dTg/mat.Kb)[:, None]*(er[:, None]*geo.GR+ez[:, None]*geo.GZ)
            check(f'seed{seed}_independent_removed_jacobian_identity',
                float(np.linalg.norm(corrected-state['jacobian']))/max(1.,float(np.linalg.norm(state['jacobian']))),
                original.CONFIG['arithmetic_tolerance'])
            outcome['recorded_but_removed_hard_volume_source'] = outcome.pop('volume_source_hard')
            outcome['volume_source_hard_applied'] = 0.
            outcome['full_model_volume_source_on_counterfactual'] = full['volume_source']
            outcome['full_model_flux_balance_on_counterfactual'] = full['flux_balance']
            outcome['full_model_residual_norm_on_counterfactual'] = full['norm']
            outcome['full_model_residual_on_counterfactual'] = full['residual'].reshape(geo.n,geo.n).tolist()
            outcome['removed_hard_source_density'] = removed.reshape(geo.n,geo.n).tolist()
            outcome['full_model_source_defect_interpretation'] = (
                'R_physical=R_counterfactual−removed_hard_source. '
                'At a converged counterfactual this is the deliberately omitted source, not a failed counterfactual numerical gate.')
        pairs.append(pair)
    for pair in pairs:
        pair['equilibrium_comparison_qualified'] = bool(
            pair['physical_solver_status'] == 'CONVERGED'
            and pair['counterfactual_solver_status'] == 'CONVERGED'
            and pair['physical_jacobian_qualified'] and pair['counterfactual_jacobian_qualified']
            and not physical['failures'] and not result['failures'])
    result['paired_comparisons'] = pairs
    if result['status'] != 'FAILED_PREREQUISITES':
        result['status'] = 'FAILED_NUMERICAL_CONTROLS' if result['failures'] else 'COMPLETE_RETAINED_OUTCOMES'
    result['seconds_including_attribution_checks'] = time.perf_counter()-start
    result['peak_self_rss_bytes'] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                      *(1 if sys.platform == 'darwin' else 1024))
    return result


def main():
    selected, globalp, local, saved, receipts, snapshot = inputs()
    if sys.argv[1:] == ['freeze']:
        print(encode(snapshot).decode())
        return 0
    if len(sys.argv) != 3 or sys.argv[1] != 'run-case':
        raise RuntimeError('Use freeze or run-case 0..3')
    index = int(sys.argv[2])
    if index not in range(4):
        raise RuntimeError('Unknown attribution case')
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective attribution freeze differs')
    payload = run_case(index, selected, globalp, local, saved, receipts)
    raw = encode(dict(freeze_sha256=sha(FREEZE),
        payload_sha256=hashlib.sha256(encode(payload)).hexdigest(), payload=payload))
    print(encode(dict(encoding='zlib_base64_canonical_json', raw_bytes=len(raw),
        raw_sha256=hashlib.sha256(raw).hexdigest(), data=base64.b64encode(zlib.compress(raw,9)).decode(),
        summary=dict(case=index,original_case=payload['case_index'],status=payload['status'],
            outcomes=[o['status'] for o in payload['outcomes']],failures=payload['failures'],
            seconds=payload['seconds_including_attribution_checks']))).decode())
    return 0 if not payload['failures'] else 2


if __name__ == '__main__':
    sys.exit(main())
