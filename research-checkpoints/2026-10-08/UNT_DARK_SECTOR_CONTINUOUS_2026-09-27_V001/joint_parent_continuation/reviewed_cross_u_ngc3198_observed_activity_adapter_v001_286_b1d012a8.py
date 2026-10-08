#!/usr/bin/env python3
"""Guarded surface-observation adapter; no physical source, field or velocity producer."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, bisect, hashlib, json, math, os, sys, traceback

AUTHOR_DRAFT = True
J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE = 'cross_u_ngc3198_observed_activity_adapter_v001.py'
STEM = 'CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = '5e346fa7a66495bc458b7b4e842dce23cbaedcf8615ca10d370ccb597cf0bd6b'
PINS = {'leroy2008_ReadMe.html': 'cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48', 'leroy2008_table4.dat': '938104d0289f93f9fed0843028555e92f63a61889d623ee5b5f132e9d6ea1f44', 'leroy2008_table7.dat': '43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99', 'NGC3198_ACTIVE_SOURCE_OBSERVATION_AUDIT_V001.json': '76675a2ffa36acd3c58e73d5f268a5ce2b6e63cf72d37bd9b1489ee7da593063', 'NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001_RESULT.json': 'fb3a3eb1639547392d54a02fb1d64fbfd61880ea15d46c4ee96b4427ad2ff76f', 'NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001_RECEIPT.json': '894d49062a17567631bc96989df965695abf3197a8d8afd972a0ed93735d1d26', 'sparc_official_NGC3198_rotmod.dat': '17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953', 'sparc_official_sample_2026-10-06_v001.mrt': '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_FINE_Q3_CASE.json': '587f3686c9d232fadfb9c7b41ecc88e94246740bbfef52cc3db7e9917d4713bd', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz': 'e12f36d7b3c822d41d003ff428fae88ed433436ce3f58c2f6764b046c81aac49', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz.COMMIT.json': 'af8945a902a162bb8a1fd6772021dc4899498ec006ba0965063a498aec34aff0', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_MANIFEST.json': 'a103ef976e3035fb48c57b878328620cf49f92118f5aeb45a84ee9dc4665ea0c', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json': 'b7834e205c379e8f9444e3ac17243744fc2266f92ccd186bcd780a7cebaac926', 'cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py': 'e77230a1819e89799e4463d5ca3808b1cab9f6a2c9166b593cbca2b949dec853', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001.md': '3ffc808394102d8b7479d9e1f604ba940e0ac7570181f1c386fb5eddc2c5e729', 'CROSS_U_ACTIVE_RECORD_FORMATION_CURRENT_AND_ENERGY_SOURCE_V001.md': '3e4ac570af650d9182adfea576a0c0982c1fef52715132f14e49f999ae66ca28', 'CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md': 'b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59', 'CROSS_U_EPS5_LINEAR_EXTERIOR_PHASE_NATIVE_AND_METRIC_MATCHING_V001.md': 'a7fc7786b42fa46ca5ec268eaba5ee2e581f3ebcdb48bffb83e8cfc6a5ef54d4'}
PINS['reviewed_cross_u_ngc3198_observed_activity_adapter_v001_281_09ecc771.py'] = '09ecc771e680cb9e06ee133f1938e1046b2ffef5ddbe4ca579b0032dbe8bd9fd'
FIELD_SPECS = {
    'R_kpc': (9, 13, 1.0), 'R_over_r25': (14, 18, 1.0),
    'stellar_surface_Msun_pc2': (41, 48, 1.0),
    'stellar_surface_rms_Msun_pc2': (49, 54, 1.0),
    'SFR_surface_Msun_yr_kpc2': (55, 62, 1e-4),
    'SFR_surface_rms_Msun_yr_kpc2': (63, 68, 1e-4),
    'FUV_component_Msun_yr_kpc2': (69, 75, 1e-4),
    'IR24_component_Msun_yr_kpc2': (76, 82, 1e-4),
}
PROFILE_FIELDS = tuple(k for k in FIELD_SPECS if k not in ('R_kpc', 'R_over_r25'))
SHARED_FIELDS = ('R_kpc', 'R_over_r25', 'stellar_surface_Msun_pc2',
                 'SFR_surface_Msun_yr_kpc2', 'SFR_surface_rms_Msun_yr_kpc2',
                 'FUV_component_Msun_yr_kpc2', 'IR24_component_Msun_yr_kpc2')
CONTROL_COUNT = 176
EPS = sys.float_info.epsilon
CREATED, RECORDS, CHECKS, PROGRESS = {}, {}, [], {}
FLAGS = {k: False for k in ('native_writer_source_registered', 'radiation_energy_source_registered',
    'source_history_registered', 'three_dimensional_source_registered', 'Hilbert_stress_qualified',
    'full_metric_qualified', 'velocity_prediction_qualified', 'observational_success_qualified')}

class PhysicalSourceUnavailable(RuntimeError):
    pass

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def encode(obj):
    return json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n'

def publish(suffix, obj):
    p = J / (STEM + '_' + suffix + '.json')
    data = encode(obj).encode()
    with p.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    if p.read_bytes() != data:
        raise RuntimeError('Publication exact-byte reread: ' + p.name)
    p.chmod(0o444)
    CREATED[p.name] = sha(p)
    RECORDS[p.name] = json.loads(data)
    return {'file': p.name, 'sha256': CREATED[p.name]}

def actual_outputs():
    out = {}
    for p in sorted(J.glob(STEM + '_*.json')):
        if not p.is_file():
            raise RuntimeError('Unexpected own output surface: ' + p.name)
        p.chmod(0o444); out[p.name] = sha(p)
    return out

def verify():
    for name, expected in {**PINS, PROTOCOL: PROTOCOL_SHA}.items():
        if sha(J / name) != expected:
            raise RuntimeError('Input byte mismatch: ' + name)

def read(name):
    return json.loads((J / name).read_text())

def control(name, passed, actual, expected):
    c = dict(ordinal=len(CHECKS), name=name, passed=bool(passed), actual=actual, expected=expected)
    CHECKS.append(c)
    if not passed:
        raise ArithmeticError('Data/implementation control refused: ' + name)

def near(actual, expected):
    return abs(actual - expected) <= 32 * EPS * max(abs(actual), abs(expected), 1e-30)

def catalogue(audit):
    rows = []
    PROGRESS['catalogue_partial'] = rows
    for raw in (J / 'leroy2008_table7.dat').read_text().splitlines():
        if raw[:8] != 'NGC 3198':
            continue
        row = {'raw_row': raw}
        rows.append(row)
        row.update({k: float(raw[a:b]) * unit for k, (a, b, unit) in FIELD_SPECS.items()})
        row['catalog_stellar_upper_limit'] = row['stellar_surface_rms_Msun_pc2'] == 1.0
        row['component_minus_total_SFR_Msun_yr_kpc2'] = (row['FUV_component_Msun_yr_kpc2']
            + row['IR24_component_Msun_yr_kpc2'] - row['SFR_surface_Msun_yr_kpc2'])
    control('exact_catalogue_23', len(rows) == len(audit['rows']) == 23, len(rows), 23)
    rr = [x['R_kpc'] for x in rows]
    control('strictly_increasing_catalogue_radii', all(a < b for a, b in zip(rr, rr[1:])), rr, 'strict increase')
    control('literal_supported_range', [rr[0], rr[-1]] == [0.3, 15.1], [rr[0], rr[-1]], [0.3, 15.1])
    control('finite_positive_catalogue', all(math.isfinite(x[k]) and x[k] >= 0 for x in rows for k in FIELD_SPECS)
        and all(x['SFR_surface_Msun_yr_kpc2'] > 0 and x['stellar_surface_Msun_pc2'] > 0 for x in rows),
        'all original fields finite/nonnegative; SFR and stellar Sigma positive', True)
    for i, (new, old) in enumerate(zip(rows, audit['rows'])):
        if new['raw_row'] != old['raw_row']:
            raise RuntimeError('Catalog string/audit binding')
        new['original_activity_audit_row'] = old
        for k in SHARED_FIELDS:
            control('catalogue_%02d_%s' % (i, k), near(new[k], old[k]), new[k], old[k])
    return rows

def interpolate(rows, radius, fields=PROFILE_FIELDS):
    rr = [x['R_kpc'] for x in rows]
    out = dict(R_kpc=radius, supported=rr[0] <= radius <= rr[-1], exact_catalogue_knot=False,
               values={k: None for k in fields}, left_slopes={k: None for k in fields},
               right_slopes={k: None for k in fields}, operands=None)
    if not math.isfinite(radius):
        raise ValueError('Nonfinite query radius')
    if not out['supported']:
        out['unsupported_reason'] = 'outside measured radial support; no extrapolation or zero fill'
        return out
    knot = bisect.bisect_left(rr, radius)
    if knot < len(rr) and rr[knot] == radius:
        out['exact_catalogue_knot'] = True
        out['values'] = {k: rows[knot][k] for k in fields}
        out['operands'] = {'knot_index': knot, 'original_row': rows[knot]}
        for label, a, b in [('left_slopes', knot - 1, knot), ('right_slopes', knot, knot + 1)]:
            if a >= 0 and b < len(rr):
                out[label] = {k: (rows[b][k] - rows[a][k]) / (rr[b] - rr[a]) for k in fields}
                out['operands'][label] = {'indices': [a, b], 'radii_kpc': [rr[a], rr[b]],
                    'values': [{k: rows[a][k] for k in fields}, {k: rows[b][k] for k in fields}]}
        return out
    b = bisect.bisect_right(rr, radius); a = b - 1
    dr = rr[b] - rr[a]; t = (radius - rr[a]) / dr
    out['values'] = {k: (1 - t) * rows[a][k] + t * rows[b][k] for k in fields}
    slope = {k: (rows[b][k] - rows[a][k]) / dr for k in fields}
    out['left_slopes'], out['right_slopes'] = dict(slope), dict(slope)
    out['operands'] = {'indices': [a, b], 'radii_kpc': [rr[a], rr[b]], 'dr_kpc': dr, 'fraction': t,
        'values': [{k: rows[a][k] for k in fields}, {k: rows[b][k] for k in fields}]}
    return out

def physical_source_gate():
    raise PhysicalSourceUnavailable('Missing registered writer/photon operator, material/coframe/clock/unit map, '
        'joint state/reservoir, full Hilbert/current contacts and retarded history. This surface adapter produces no velocities.')

def manufactured_controls():
    affine = [{'R_kpc': 0., 'value': 1.}, {'R_kpc': 2., 'value': 5.}]
    q = interpolate(affine, 1., ('value',))
    control('manufactured_affine', q['values']['value'] == 3. and q['left_slopes']['value'] == 2., q, 'value3 slope2')
    constant = [{'R_kpc': 0., 'value': 3.}, {'R_kpc': 2., 'value': 3.}]
    q = interpolate(constant, 1., ('value',))
    control('manufactured_constant', q['values']['value'] == 3. and q['right_slopes']['value'] == 0., q, 'value3 slope0')
    kink = [{'R_kpc': 0., 'value': 0.}, {'R_kpc': 1., 'value': 1.}, {'R_kpc': 2., 'value': 3.}]
    q = interpolate(kink, 1., ('value',))
    control('manufactured_two_sided_knot', q['left_slopes']['value'] == 1. and q['right_slopes']['value'] == 2., q, 'left1 right2')
    outside = [interpolate(kink, x, ('value',)) for x in (-1., 3.)]
    control('manufactured_unsupported', all(not x['supported'] and x['values']['value'] is None
        and x['left_slopes']['value'] is None and x['right_slopes']['value'] is None for x in outside), outside, 'all unknown')
    refused = False
    try:
        physical_source_gate()
    except PhysicalSourceUnavailable:
        refused = True
    control('physical_source_gate_refuses', refused, refused, True)

def parent_binding():
    case = read('CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_FINE_Q3_CASE.json')
    receipt = read('CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json')
    manifest = read('CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_MANIFEST.json')
    commit = read('CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz.COMMIT.json')
    if receipt['status'] != 'CLOSED' or receipt['owner']['pid'] != 78729 or case['status'] != 'CONVERGED':
        raise RuntimeError('Actual parent closure/identity')
    if manifest['input_sha256'] != receipt['input_sha256'] or manifest['owner'] != receipt['owner']:
        raise RuntimeError('Parent complete map/owner binding')
    for name in ('CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_FINE_Q3_CASE.json',
        'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz',
        'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz.COMMIT.json',
        'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_MANIFEST.json'):
        if receipt['output_sha256'][name] != PINS[name]:
            raise RuntimeError('Accessed parent output map binding: ' + name)
    final = case['final_checkpoint']
    if final['file'] != commit['file'] or final['sha256'] != commit['sha256'] or commit['metadata']['identity'] != case['identity']:
        raise RuntimeError('Exact selected parent final pair')
    if commit['metadata']['rows'] != case['rows'] or commit['metadata']['status'] != 'CONVERGED':
        raise RuntimeError('Exact parent readout/terminal metadata')
    identity = case['identity']
    if identity['eps'] != 1e-5 or identity['quadrature_order'] != 3 or identity['grid_shape'] != [65, 173, 89]:
        raise RuntimeError('Same actual EPS5/FINE_Q3 geometry')
    audit = read('NGC3198_ACTIVE_SOURCE_OBSERVATION_AUDIT_V001.json')
    demand = read('NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001_RESULT.json')
    drc = read('NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001_RECEIPT.json')
    if drc['status'] != 'CLOSED' or drc['result_sha256'] != PINS['NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001_RESULT.json']:
        raise RuntimeError('Frozen sign-demand closure')
    if demand['parent_final'] != {k: final[k] for k in ('file', 'sha256', 'commit_file', 'commit_sha256')}:
        raise RuntimeError('Sign demand same field binding')
    if demand['original_activity_rows'] != audit['rows'] or [x['original_row'] for x in demand['rows']] != case['rows']:
        raise RuntimeError('Activity/readout exact disposition binding')
    if audit['adopted_in_galaxy_solver'] is not False or demand['physical_source_or_history_selected'] is not False:
        raise RuntimeError('No physical source adoption')
    return case, receipt, manifest, audit, demand

def closing_checks():
    if sha(J / SOURCE) != RECORDS[STEM + '_OWNER_START.json']['source_sha256']:
        raise RuntimeError('Executing source changed after owner admission')
    if actual_outputs() != CREATED:
        raise RuntimeError('Actual own-output file census/hash')
    for name, obj in RECORDS.items():
        if read(name) != obj:
            raise RuntimeError('Own JSON schema/payload reread: ' + name)
    verify()

def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--root-execute', action='store_true'); args = ap.parse_args()
    if AUTHOR_DRAFT or not args.root_execute:
        raise RuntimeError('Held author draft or missing root execution flag')
    if sys.platform != 'darwin' or Path(__file__).resolve() != J / SOURCE:
        raise RuntimeError('Actual root Mac/source context')
    if any(p.name != PROTOCOL for p in J.glob(STEM + '*')):
        raise FileExistsError('Preserved output namespace already exists')
    verify()
    owner = dict(owner='root', pid=os.getpid(), started=datetime.now(timezone.utc).isoformat(), source_sha256=sha(J / SOURCE))
    if sha(J / SOURCE) != owner['source_sha256']:
        raise RuntimeError('Source changed before owned launch')
    case = None
    try:
        publish('OWNER_START', owner)
        case, parent, manifest, audit, demand = parent_binding()
        binding = dict(selected_final={k: case['final_checkpoint'][k] for k in ('file', 'sha256', 'commit_file', 'commit_sha256')}, parent_receipt_sha256=PINS['CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json'],
            parent_map_counts={'inputs': len(parent['input_sha256']), 'outputs': len(parent['output_sha256'])})
        publish('MANIFEST', dict(owner=owner, inputs={**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: owner['source_sha256']},
            binding=binding, control_count=CONTROL_COUNT, physical_flags=FLAGS, no_automatic_resume=True,
            operation='surface data interpolation only; no producer import, field decode or physical source'))
        rows = catalogue(audit)
        catalog_ref = publish('CATALOGUE', dict(owner=owner, rows=rows, original_activity_audit=audit,
            raw_properties_rows=[x for x in (J / 'leroy2008_table4.dat').read_text().splitlines() if x[:8] == 'NGC 3198'],
            raw_SPARC_sample_rows=[x for x in (J / 'sparc_official_sample_2026-10-06_v001.mrt').read_text().splitlines() if 'NGC3198' in x], physical_flags=FLAGS))
        rr, zz = case['identity']['r_kpc'], case['identity']['z_kpc']
        groups = {}
        for group, radii in [('grid', rr), ('observed', [x['R_kpc'] for x in case['rows']]), ('knots', [x['R_kpc'] for x in rows])]:
            groups[group] = []; PROGRESS[group + '_partial'] = groups[group]
            for radius in radii:
                groups[group].append(interpolate(rows, radius))
        control('catalogue_knots_exact_values', all(s['values'] == {k: r[k] for k in PROFILE_FIELDS} for s, r in zip(groups['knots'], rows)), True, True)
        control('grid_dimensions_axes', len(rr) == 173 and len(zz) == 89 and rr[0] == zz[0] == 0 and rr[-1] == zz[-1] == 128
            and all(a < b for axis in (rr, zz) for a, b in zip(axis, axis[1:])), [len(rr), len(zz)], [173, 89])
        control('query_group_census', [len(groups[k]) for k in ('grid', 'observed', 'knots')] == [173, 43, 23],
            [len(groups[k]) for k in ('grid', 'observed', 'knots')], [173, 43, 23])
        official = [float(x.split()[0]) for x in (J / 'sparc_official_NGC3198_rotmod.dat').read_text().splitlines() if x.strip() and not x.lstrip().startswith('#')]
        control('official_43_radii', official == [x['R_kpc'] for x in case['rows']], official, [x['R_kpc'] for x in case['rows']])
        control('copied_covered_sign_demands', demand['covered_counts'] == dict(requires_positive=10, requires_negative=6, not_common_sign=12), demand['covered_counts'], [10, 6, 12])
        central = [x for x in demand['rows'] if 0.64 <= x['R_kpc'] <= 1.61]
        control('preserved_central_negative_demands', bool(central) and all(x['common_quoted_error_sign'] == 'requires_negative' for x in central),
            [{'R_kpc': x['R_kpc'], 'sign': x['common_quoted_error_sign']} for x in central], 'every central demand remains negative')
        manufactured_controls()
        if len(CHECKS) != CONTROL_COUNT:
            raise RuntimeError('Exact declared control census')
        grid_ref = publish('GRID', dict(owner=owner, radial_samples=groups['grid'], original_r_kpc=rr, original_z_kpc=zz,
            dimensional_scope='surface function of R only; no vertical field or height assigned', physical_flags=FLAGS))
        observed_ref = publish('OBSERVED', dict(owner=owner, radial_samples=groups['observed'], knot_samples=groups['knots'],
            original_signed_demand=demand, original_rows=case['rows'], physical_flags=FLAGS))
        result = dict(status='OBSERVED_INPUT_ADAPTER_CLOSED', owner=owner, inputs={**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: owner['source_sha256']},
            payloads=[catalog_ref, grid_ref, observed_ref], binding=binding, controls=CHECKS, counts={'catalogue': 23, 'grid_radial': 173, 'observed': 43, 'knot': 23, 'controls': len(CHECKS)},
            units={'SFR': 'Msun yr^-1 kpc^-2', 'SFR_radial_slope': 'Msun yr^-1 kpc^-3', 'stellar': 'Msun pc^-2', 'stellar_radial_slope': 'Msun pc^-2 kpc^-1'},
            missing_registration=dict(record_rate=None, writer_coupling=None, physical_height=None, bolometric_flux=None, radiation_stress=None,
                joint_state=None, proper_clock=None, history=None, Hilbert_source=None, velocity=None),
            historical_native_controls=case['historical_native_controls'], inherited_physical_flags=case['physical_flags'],
            inherited_source_identity=case['identity']['source_identity'], physical_flags=FLAGS)
        result_ref = publish('RESULT', result); closing_checks()
        publish('RECEIPT', dict(status='CLOSED', owner=owner, closed=datetime.now(timezone.utc).isoformat(),
            input_sha256=result['inputs'], output_sha256=dict(CREATED), result_sha256=result_ref['sha256'], physical_flags=FLAGS))
        closing_checks()
        print(encode(dict(status=result['status'], controls=len(CHECKS), result_sha256=result_ref['sha256'])).strip())
    except BaseException as exc:
        prior = J / (STEM + '_RECEIPT.json')
        prior_receipt = {'file': prior.name, 'sha256': sha(prior)} if prior.exists() else None
        actual = actual_outputs()
        error_ref = publish('ERROR', dict(status='CLOSED_ERROR', owner=owner, exception=repr(exc), traceback=traceback.format_exc(),
            preserved_output_sha256=actual, prior_receipt=prior_receipt, available_raw=PROGRESS, controls=CHECKS, physical_flags=FLAGS))
        if prior_receipt is None:
            publish('RECEIPT', dict(status='CLOSED_ERROR', owner=owner, closed=datetime.now(timezone.utc).isoformat(),
                input_sha256={**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: owner['source_sha256']}, output_sha256=actual_outputs(), error_sha256=error_ref['sha256'], physical_flags=FLAGS))
        actual_outputs()
        raise

if __name__ == '__main__':
    main()
