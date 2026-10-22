"""INERT generator of P-88 k_max-matrix call specs and campaign files (Claude2 lane, dispatch 0470, c2v001).

Writes driver call specs (schema UNT_GALAXY_M0_FORWARD_CALL_C2V001, INTERFACE_C2_0466_V001 s3)
for the registered cases of KMAX_MATRIX_PREREG_V001.json, plus campaign files for
campaign_c2v001.py.  It launches nothing.  Every hash is computed from bytes.

  wave1  --outdir NEW   : full-prefix cases C4, C3, R, C2 (route A computed), one campaign file.
  wave2  --grid G2|G3|G4 --cube-out CUBE_CALL_OUT --outdir NEW
                         : sphere/cylinder cases of that grid admitting the cube call's route-A
                           checkpoint, reference and body (identity self-hash recomputed,
                           iteration-4 completion and finish files verified from bytes).
  templates --outdir NEW : one template per case (wave-2 admit fields marked PENDING; not launchable).

Common options:
  --prereg P            registered matrix (sha recorded in every spec label)
  --driver D --driver-sha256 H --monitor M --monitor-sha256 H   (bytes must match)
  --base-spec S         optional production base call spec: its physical and brackets blocks
                        are copied verbatim (its coefficients must be the A2 grid)
  --column-workers N    default 2
usage: python3 -I -B make_kmax_specs_c2v001.py wave1 --prereg P --driver D --driver-sha256 H \
           --monitor M --monitor-sha256 H --outdir NEW [--base-spec S]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = 'UNT_GALAXY_M0_FORWARD_CALL_C2V001'
A2 = {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
      'sha256': '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'}
DEFAULT_PHYSICAL = {'Eref_J': 1.4642919592009638e+58, 'ell_F_m': 9.905025036587288e+19, 'gamma': 2.9410488940677744e+41,
                    'common_scale_s': 1.0, 'entropy_K_factor': 0.5289256198347108, 'distance_Mpc': 4.04, 'inclination_deg': 66.0}
REPRO_RULE_SPEC = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/specs/CALL_REPRO_RULE_FULL_C2V001.json',
                   'c92344bff03cf10a5eed18c612e36be5f6c2a742eb03d9a111e90ae3c8c732b6')
PICARD = {'passes': 4, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True}
PREP_V008 = ('ddo_actual_initial_source_preparation_v008.py', 'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62')
GIB = 1024 ** 3
# per-call caps by grid (model-L projections in GRID_CHECK_V001.json x ~1.3-2 margin)
CAPS = {'G2': {'wall_cap_s': 14400.0, 'rss_cap_bytes': 3 * GIB, 'output_cap_bytes': 12 * GIB},
        'G3': {'wall_cap_s': 21600.0, 'rss_cap_bytes': 3 * GIB, 'output_cap_bytes': 20 * GIB},
        'G4': {'wall_cap_s': 32400.0, 'rss_cap_bytes': 4 * GIB, 'output_cap_bytes': 28 * GIB},
        'GR': {'wall_cap_s': 28800.0, 'rss_cap_bytes': 4 * GIB, 'output_cap_bytes': 26 * GIB}}
WAVE1_ORDER = ['C4', 'C3', 'R', 'C2']   # critical path first


class Refusal(Exception):
    pass


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def canonical_ckpt(obj):
    """coupled_gas_checkpoint_c2v003._canonical, reproduced exactly (lines 168-170)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def spec_bytes(obj):
    return (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()


def write_x(path, raw):
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def verify(path, sha, label):
    if sha256_file(path) != sha:
        raise Refusal('%s pin mismatch: %s' % (label, path))


def load_prereg(path):
    raw = Path(path).read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def common_blocks(base_spec_path):
    if base_spec_path:
        b = json.loads(Path(base_spec_path).read_text())
        if b.get('coefficients', {}).get('sha256') != A2['sha256']:
            raise Refusal('base spec coefficients are not the A2 grid 2e3a36d8...; the k-matrix must use the binding A2 point')
        phys = b['physical']
        brackets = b['numerics']['brackets']
        src = {'base_spec': str(Path(base_spec_path).resolve()), 'base_spec_sha256': sha256_file(base_spec_path)}
    else:
        verify(REPRO_RULE_SPEC[0], REPRO_RULE_SPEC[1], 'repro rule spec')
        r = json.loads(Path(REPRO_RULE_SPEC[0]).read_text())
        phys = dict(DEFAULT_PHYSICAL)
        brackets = r['numerics']['brackets']
        src = {'brackets_from': REPRO_RULE_SPEC[0], 'brackets_from_sha256': REPRO_RULE_SPEC[1], 'physical': 'seed V002 defaults'}
    if brackets.get('mode') != 'rule':
        raise Refusal('column_workers>1 and the matrix need brackets.mode rule')
    return phys, brackets, src


def driver_preflight(driver_path):
    """Static check of precondition P1: the driver must route route-A prep to v008 (<=96 nodes)."""
    text = Path(driver_path).read_text()
    return {'driver_mentions_prep_v008': PREP_V008[0] in text and PREP_V008[1] in text,
            'P1_note': 'G3 (84), GR (92) and G4 (96 nodes/axis) exceed prep v007 budget 80; they need route-A prep v008 (bb05f974..., review aa12d69f...). '
                       'If the driver still pins v007 these calls end FAILED_AT_STAGE in route A ("Composite node budget/order mismatch").'}


def case_spec(pre, pre_sha, case, phys, brackets, workers, admit, label_extra=''):
    g = pre['grids'][case['grid']]
    tr = {'shape': case['shape']}
    if case['shape'] != 'cube':
        tr['kmax_inverse_kpc'] = float(case['kmax_inverse_kpc'])
    return {'schema': SCHEMA, 'galaxy': 'DDO154',
            'label': 'P-88 kmax matrix case %s (grid %s, %s%s); prereg %s%s' % (
                case['id'], case['grid'], case['shape'], '' if case['shape'] == 'cube' else ' K=%g' % case['kmax_inverse_kpc'], pre_sha[:16], label_extra),
            'physical': dict(phys), 'coefficients': dict(A2),
            'numerics': {'composite_grid_spec': g['composite_grid_spec'], 'truncation': tr, 'picard': dict(PICARD),
                         'brackets': brackets, 'column_workers': workers},
            'admit': admit, 'reference_compare': False}


def admission_from_cube_out(cube_out):
    """Derive admit.{route_a, reference, body} from a cube call's outdir; every value from bytes."""
    out = Path(cube_out)
    st = out / 'stages'
    if not st.is_dir():
        raise Refusal('no stages/ under %s' % out)

    def one(suffix):
        c = [d for d in sorted(st.iterdir()) if d.is_dir() and d.name.endswith('_' + suffix)]
        if len(c) != 1:
            raise Refusal('expected exactly one *_%s stage dir, found %d' % (suffix, len(c)))
        return c[0]
    ra, rf, bd = one('route_a'), one('reference'), one('body')
    att, cp = ra / 'attempt_000', ra / 'checkpoint'
    fin = json.loads((att / 'finish.json').read_text())
    rsha = sha256_file(att / 'result.json')
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT' or fin.get('result_sha256') != rsha:
        raise Refusal('route-A attempt not RETURNED_ACTUAL_RESULT or result hash mismatch')
    ident = json.loads((cp / 'IDENTITY.json').read_text())
    isha = hashlib.sha256(canonical_ckpt(ident['identity'])).hexdigest()
    if ident.get('identity_sha256') != isha:
        raise Refusal('checkpoint IDENTITY self-hash does not recompute')
    if not (cp / 'iteration_0004' / 'COMPLETED.json').is_file():
        raise Refusal('route A has no iteration_0004/COMPLETED.json (route-B stages require iteration 4)')
    ref, body = rf / 'reference', bd / 'body'
    for p in (ref / 'start.json', ref / 'finish.json', body / 'finish.json'):
        if not p.is_file():
            raise Refusal('prefix incomplete: missing %s' % p)
    spec = json.loads((out / 'inputs' / 'call_spec.json').read_text())
    return ({'route_a': {'attempt_directory': str(att), 'checkpoint_directory': str(cp), 'identity_sha256': isha, 'result_sha256': rsha},
             'reference': {'directory': str(ref), 'start_sha256': sha256_file(ref / 'start.json'), 'finish_sha256': sha256_file(ref / 'finish.json')},
             'body': {'directory': str(body), 'finish_sha256': sha256_file(body / 'finish.json')}}, spec)


def campaign(calls, grid_ids, driver, dsha, monitor, msha, max_concurrent):
    cap = {k: max(CAPS[g][k] for g in grid_ids) for k in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')}
    cap['poll_s'] = 2.0
    return {'calls': calls, 'max_concurrent': max_concurrent, 'per_call': cap, 'campaign_wall_cap_s': 172800.0,
            'driver': {'path': str(driver), 'sha256': dsha}, 'monitor': {'path': str(monitor), 'sha256': msha}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=('wave1', 'wave2', 'templates'))
    ap.add_argument('--prereg', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--driver')
    ap.add_argument('--driver-sha256')
    ap.add_argument('--monitor')
    ap.add_argument('--monitor-sha256')
    ap.add_argument('--base-spec')
    ap.add_argument('--grid', choices=('G2', 'G3', 'G4'))
    ap.add_argument('--cube-out')
    ap.add_argument('--column-workers', type=int, default=2)
    a = ap.parse_args(argv)
    pre, pre_sha = load_prereg(a.prereg)
    out = Path(a.outdir).resolve()
    if out.exists():
        raise Refusal('outdir exists: %s' % out)
    phys, brackets, src = common_blocks(a.base_spec)
    verify(A2['path'], A2['sha256'], 'A2 coefficients')
    cases = {c['id']: c for c in pre['cases']}
    if a.cmd != 'templates':
        for k in ('driver', 'driver_sha256', 'monitor', 'monitor_sha256'):
            if not getattr(a, k):
                raise Refusal('--' + k.replace('_', '-') + ' required')
        verify(a.driver, a.driver_sha256, 'driver')
        verify(a.monitor, a.monitor_sha256, 'monitor')
    out.mkdir(parents=True)
    manifest = {'schema': 'UNT_KMAX_SPECS_MANIFEST_C2_0470_V001', 'cmd': a.cmd, 'prereg': str(Path(a.prereg).resolve()), 'prereg_sha256': pre_sha,
                'common_source': src, 'specs': {}, 'generator_sha256': sha256_file(__file__)}
    if a.cmd == 'templates':
        for cid, c in cases.items():
            admit = {}
            if c['prefix'].startswith('admit:'):
                cube = c['prefix'].split(':')[1]
                admit = {'route_a': {'attempt_directory': 'PENDING(<%s out>/stages/01_route_a/attempt_000)' % cube,
                                     'checkpoint_directory': 'PENDING(<%s out>/stages/01_route_a/checkpoint)' % cube,
                                     'identity_sha256': 'PENDING(recomputed canonical self-hash of IDENTITY.json)',
                                     'result_sha256': 'PENDING(sha256 of attempt_000/result.json)'},
                         'reference': {'directory': 'PENDING(<%s out>/stages/02_reference/reference)' % cube,
                                       'start_sha256': 'PENDING', 'finish_sha256': 'PENDING'},
                         'body': {'directory': 'PENDING(<%s out>/stages/03_body/body)' % cube, 'finish_sha256': 'PENDING'}}
            s = case_spec(pre, pre_sha, c, phys, brackets, a.column_workers, admit, ' TEMPLATE')
            p = out / ('CALL_KMAX_%s_C2V001.TEMPLATE.json' % cid)
            manifest['specs'][cid] = {'path': str(p), 'sha256': write_x(p, spec_bytes(s)), 'launchable': not admit}
    elif a.cmd == 'wave1':
        manifest['preflight'] = driver_preflight(a.driver)
        calls = []
        for cid in WAVE1_ORDER:
            s = case_spec(pre, pre_sha, cases[cid], phys, brackets, a.column_workers, {})
            p = out / ('CALL_KMAX_%s_C2V001.json' % cid)
            h = write_x(p, spec_bytes(s))
            manifest['specs'][cid] = {'path': str(p), 'sha256': h}
            calls.append({'spec_path': str(p), 'spec_sha256': h})
        camp = campaign(calls, [cases[c]['grid'] for c in WAVE1_ORDER], a.driver, a.driver_sha256, a.monitor, a.monitor_sha256,
                        max_concurrent=min(4, 12 // a.column_workers))
        cp = out / 'CAMPAIGN_KMAX_WAVE1_C2V001.json'
        manifest['campaign'] = {'path': str(cp), 'sha256': write_x(cp, spec_bytes(camp)), 'call_index_to_case': WAVE1_ORDER}
    else:
        if not a.grid or not a.cube_out:
            raise Refusal('wave2 needs --grid and --cube-out')
        cube_id = {'G2': 'C2', 'G3': 'C3', 'G4': 'C4'}[a.grid]
        admit, cube_spec = admission_from_cube_out(a.cube_out)
        expect = case_spec(pre, pre_sha, cases[cube_id], phys, brackets, a.column_workers, {})
        for k in ('physical', 'coefficients'):
            if cube_spec[k] != expect[k]:
                raise Refusal('cube call %s block differs from this generation (%s)' % (k, k))
        if cube_spec['numerics']['composite_grid_spec'] != expect['numerics']['composite_grid_spec'] or cube_spec['numerics']['truncation'] != {'shape': 'cube'}:
            raise Refusal('cube call grid/truncation is not registered case %s' % cube_id)
        if cube_spec['numerics']['brackets'] != brackets or cube_spec['numerics']['picard'] != PICARD:
            raise Refusal('cube call brackets/picard differ from the common block')
        calls, ids = [], []
        for cid, c in cases.items():
            if c['prefix'] == 'admit:' + cube_id:
                s = case_spec(pre, pre_sha, c, phys, brackets, a.column_workers, admit)
                p = out / ('CALL_KMAX_%s_C2V001.json' % cid)
                h = write_x(p, spec_bytes(s))
                manifest['specs'][cid] = {'path': str(p), 'sha256': h}
                calls.append({'spec_path': str(p), 'spec_sha256': h})
                ids.append(cid)
        manifest['admitted_from'] = {'cube_case': cube_id, 'cube_out': str(Path(a.cube_out).resolve()), 'admit': admit}
        camp = campaign(calls, [a.grid], a.driver, a.driver_sha256, a.monitor, a.monitor_sha256, max_concurrent=len(calls))
        cp = out / ('CAMPAIGN_KMAX_WAVE2_%s_C2V001.json' % a.grid)
        manifest['campaign'] = {'path': str(cp), 'sha256': write_x(cp, spec_bytes(camp)), 'call_index_to_case': ids}
    mp = out / 'SPECS_MANIFEST.json'
    write_x(mp, spec_bytes(manifest))
    print(json.dumps({k: v for k, v in manifest.items() if k in ('cmd', 'specs', 'campaign', 'preflight')}, indent=1))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Refusal as exc:
        print('REFUSED: %s' % exc, file=sys.stderr)
        sys.exit(2)
