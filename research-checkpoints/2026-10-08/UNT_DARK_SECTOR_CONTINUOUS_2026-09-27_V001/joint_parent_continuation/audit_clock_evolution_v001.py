"""Read-only saved-case arithmetic audit; never imports/evolves the producer."""
import hashlib
import json
import math
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec = 60
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
counts, maxima, failures, files = Counter(), {}, [], {}


def enc(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(p):
    p = p.resolve(strict=True)
    p.relative_to(ROOT)
    value = hashlib.sha256(p.read_bytes()).hexdigest()
    files[str(p.relative_to(ROOT))] = value
    return value


def d(x):
    return Decimal.from_float(x) if isinstance(x, float) else Decimal(x)


def check(name, condition):
    counts[name] += 1
    if not condition:
        failures.append(dict(check=name))


def near(name, a, b, scale=None):
    a, b = d(a), d(b)
    denominator = max(abs(a), abs(b), Decimal('1e-300')) if scale is None else max(d(scale), Decimal('1e-300'))
    error = float(abs(a-b)/denominator)
    maxima[name] = max(maxima.get(name, 0.), error)
    counts[name] += 1
    if not math.isfinite(error) or error > 2e-12:
        failures.append(dict(check=name, error=error))


def wrapper(name):
    p = HERE/name
    x = json.loads(p.read_text())
    sha(p)
    check('payload_identity', x['payload_sha256'] == hashlib.sha256(enc(x['payload'])).hexdigest())
    return x, x['payload']


freeze_path = HERE/'COSMOLOGICAL_CLOCK_EVOLUTION_V001_FROZEN.json'
freeze = json.loads(freeze_path.read_text())
frozen_sha = sha(freeze_path)
check('frozen_member_census', len(freeze['files']) == 51)
for name, expected in freeze['files'].items():
    check('frozen_member_identity', sha(ROOT/name) == expected)
cw, collected = wrapper('COSMOLOGICAL_CLOCK_EVOLUTION_V001_COLLECTED.json')
check('collected_expected_payload', cw['payload_sha256'] == '52125bd2588818c241c1b6f36056032d5a2ec912ab1c14c281f0ac398a9bc7e7')
for name, expected in collected['files'].items():
    check('collector_input_identity', sha(HERE/name) == expected)
check('collector_status', collected['status'] == 'COMPLETE_SAVED_CASE_CENSUS')
check('case_mapping', [c['case'] for c in freeze['cases']] == list(range(12)))
check('configuration_census', {(c['gap'], c['order'], c['eta']) for c in freeze['cases']} ==
    {(g, n, e) for g in (.001,.002) for n in (64,128) for e in (.001,.1,1.)})
cfg, ref = freeze['configuration'], freeze['reference']
beta, om, oe, ol, h0 = (d(cfg['beta']), d(ref['Omega_b'])+d(ref['Omega_exc']),
    d(ref['Omega_exc']), d(ref['Omega_Lambda']), d(ref['H0_s_inverse']))
near('flat_background', om+ol, 1)
near('H0_SI_conversion', h0, d(ref['inherited_reference_input']['H0_km_s_Mpc'])/d(3.085677581491367e19))
_, history = wrapper('COMMON_HISTORY_MECHANISM_V001_RESULTS.json')
producer_counts, producer_maxima, rows = Counter(), {}, []
expected_counts = dict(clock_flux_identity=64, compensated_density_reconstruction=64,
    dopri_embedded_weight_sum=1, dopri_fifth_order_moment=5, dopri_row_sums=7,
    exact_initial_state=1, exact_matter_power_DOPRI=1, exact_matter_power_RK4=1,
    exact_oscillator_DOPRI=1, exact_oscillator_RK4=1, full_state_milestone_census=1,
    hard_normal_current=64, independent_RK4=1, independent_coordinate_rhs=5,
    slow_reference_RK4=1, slow_reference_repeat=1, tighter_DOPRI=1)
slow = collected['slow_reference']
sample_times = [v['a'] for v in slow]
check('output_grid', len(sample_times) == 64 and all(b>a for a,b in zip(sample_times,sample_times[1:])))
fields = ('u','u_log_a','clock_source_Q','acceleration_over_H0',
    'unitary_lapse_times_k_over_H0','H0_clock_pi_times_k_over_H0',
    'hard_density_contrast_per_k_over_H0','polarization_contrast_per_k_over_H0')
summaries = []
for expected in freeze['cases']:
    index = expected['case']
    w, payload = wrapper(f'COSMOLOGICAL_CLOCK_EVOLUTION_V001_CASE_{index:02d}.json')
    check('case_freeze', w['freeze_sha256'] == frozen_sha)
    check('case_metadata', payload['selected_case'] == index and payload['reference'] == ref and payload['configuration'] == cfg)
    check('case_qualified', payload['status'] == 'COMPLETE' and payload['checks']['failures'] == [])
    check('row_census', len(payload['rows']) == 1)
    row = payload['rows'][0]
    check('case_exact_map', all(row[k] == v for k,v in expected.items()))
    check('same_slow_reference', payload['slow_reference']['rows'] == slow)
    check('sample_census', [v['a'] for v in row['sample_rows']] == sample_times)
    check('numerical_gate_census', payload['checks']['counts'] == expected_counts)
    producer_counts.update(payload['checks']['counts'])
    for key, value in payload['checks']['maximum_errors'].items():
        tolerance = (cfg['independent_tolerance'] if key in ('independent_RK4','slow_reference_RK4') else
            cfg['repeat_tolerance'] if key in ('tighter_DOPRI','slow_reference_repeat',
              'exact_matter_power_DOPRI','exact_matter_power_RK4','exact_oscillator_DOPRI','exact_oscillator_RK4') else
            cfg['arithmetic_tolerance'])
        check('saved_gate_threshold', math.isfinite(value) and value <= tolerance)
        producer_maxima[key] = max(producer_maxima.get(key,0.),value)
    n = row['order']
    delta, weights = list(map(d,row['delta'])),list(map(d,row['weights']))
    source_copies = [c for c in history['cases'] if c['gap']==row['gap'] and c['order']==n]
    check('source_spectrum', bool(source_copies) and all(c['delta']==row['delta'] and c['weights']==row['weights'] for c in source_copies))
    kb = sum(weights)+beta
    near('Kb_sum', row['Kb'], kb)
    near('eta_to_seconds', row['tau_star_seconds'], d(row['eta'])/h0)
    near('coupled_frequency_bound', row['coupled_frequency_bound_over_H0'],
         (max(q*q for q in delta)+sum(p*q*q for p,q in zip(weights,delta))/beta).sqrt()/d(row['eta']))
    check('initial_shape', len(row['initial_state'])==2+2*n and all(len(z)==2 for z in row['initial_state']))
    for i, values in enumerate(row['initial_state']):
        for col,value in enumerate(values):
            check('initial_basis_value', value == float(i==col))
    for method, diagnostic in row['comparisons'].items():
        errors = diagnostic['per_coordinate_and_basis_maximum_errors']
        check('method_coordinate_census', len(errors)==2+2*n and all(len(v)==2 for v in errors))
        check('method_maximum', max(v for r in errors for v in r)==diagnostic['maximum_scaled_error'])
        for v in (v for r in errors for v in r):
            check('finite_nonnegative_method_error', math.isfinite(v) and v>=0)
    for value in row['sample_rows']:
        a = d(value['a']); h=(om/a**3+ol).sqrt()
        near('sample_Hubble',value['H_over_H0'],h)
        near('minimum_soft_rate',value['soft_frequency_over_H_range'][0],min(delta)/(d(row['eta'])*h))
        near('maximum_soft_rate',value['soft_frequency_over_H_range'][1],max(delta)/(d(row['eta'])*h))
        for col in range(2):
            u,un,q = (d(value[k][col]) for k in ('u','u_log_a','clock_source_Q'))
            near('sample_acceleration',value['acceleration_over_H0'][col],h*(u+un))
            near('sample_lapse',value['unitary_lapse_times_k_over_H0'][col],a*h*(u+un))
            near('sample_clock_shift',value['H0_clock_pi_times_k_over_H0'][col],-a*u)
            den=2*a*a*q/(3*kb*oe)
            near('sample_density',value['hard_density_contrast_per_k_over_H0'][col],den)
            near('sample_polarization',value['polarization_contrast_per_k_over_H0'][col],-den)
    check('full_state_census', [v['a'] for v in row['full_states']]==cfg['full_state_scale_factors'])
    for item in row['full_states']:
        a=d(item['a']);h=(om/a**3+ol).sqrt();state=item['state']
        check('full_state_shape',len(state)==2+2*n and all(len(v)==2 for v in state))
        value=min(row['sample_rows'],key=lambda v:abs(v['a']-item['a']))
        near('full_state_epoch',value['a'],a)
        for vector in state:
            for x in vector: check('full_state_finite',math.isfinite(x))
        for col in range(2):
            u,un=d(state[0][col]),d(state[1][col])
            near('full_state_tilt',value['u'][col],u)
            near('full_state_tangent',value['u_log_a'][col],un)
            pieces=[p*d(state[2+j][col]) for j,p in enumerate(weights)]+[beta*h*(u+un)]
            near('full_state_charge',value['clock_source_Q'][col],sum(pieces),max(Decimal(1),sum(map(abs,pieces))))
    summary=collected['cases'][index]
    peaks=[];epochs=[]
    for col in range(2):
        maximum=max(row['sample_rows'],key=lambda v:abs(v['u'][col]))
        peak=abs(maximum['u'][col]);peaks.append(peak);epochs.append(maximum['a'])
        check('sampled_peak',peak==row['sampled_maximum_absolute_tilt_transfer'][col]==summary['sampled_maximum_absolute_tilt_transfer'][col])
        check('peak_epoch',maximum['a']==summary['a_at_sampled_peak'][col])
        near('amplitude_normalization',row['initial_amplitude_for_sampled_tilt_below_display_threshold'][col],d(cfg['linear_tilt_display_threshold'])/d(peak))
    check('present_summary',summary['at_present']==next(v for v in row['sample_rows'] if v['a']==1.))
    check('final_summary',summary['at_final']==row['sample_rows'][-1])
    check('method_summary',summary['numerical_comparisons']=={k:v['maximum_scaled_error'] for k,v in row['comparisons'].items()})
    timing=collected['timing'][index]
    check('timing_summary',timing==dict(case=index,seconds=payload['seconds'],peak_self_rss_bytes=payload['peak_self_rss_bytes']))
    summaries.append(dict(case=index,gap=row['gap'],order=n,eta=row['eta'],peaks=peaks,peak_epochs=epochs,
        tau_star_Julian_years=float(d(row['tau_star_seconds'])/Decimal(31557600))))
    rows.append(row)
check('aggregate_check_census',dict(producer_counts)==collected['producer_check_counts'] and sum(producer_counts.values())==2640==collected['producer_check_total'])
check('aggregate_gate_maxima',producer_maxima==collected['producer_check_maximum_errors'])
check('all_six_contrasts',len(collected['quadrature_contrasts'])==6 and
    {(c['gap'],c['eta']) for c in collected['quadrature_contrasts']}=={(g,e) for g in (.001,.002) for e in (.001,.1,1.)})
contrast_summary=[]
for item in collected['quadrature_contrasts']:
    pair=[next(r for r in rows if r['gap']==item['gap'] and r['eta']==item['eta'] and r['order']==n) for n in (64,128)]
    check('all_contrast_channels',set(item['channels'])==set(fields))
    peaks={}
    for field in fields:
        values=[[v[field] for v in r['sample_rows']] for r in pair]
        diff=item['channels'][field]['fine_minus_coarse']
        check('contrast_epoch_census',len(diff)==64 and all(len(v)==2 for v in diff))
        scale=[max(Decimal(1),*(abs(d(v[col])) for vv in values for v in vv)) for col in range(2)]
        exact=[[d(b[col])-d(a[col]) for col in range(2)] for a,b in zip(*values)]
        for got,want in zip(diff,exact):
            for a,b in zip(got,want):near('signed_contrast',a,b)
        for col in range(2):
            near('normalized_contrast',item['channels'][field]['peak_normalized_difference'][col],max(abs(v[col]) for v in exact)/scale[col])
        peaks[field]=item['channels'][field]['peak_normalized_difference']
    contrast_summary.append(dict(gap=item['gap'],eta=item['eta'],all_channel_peak_normalized_differences=peaks))

# Independent arithmetic of the conserved-charge fast-limit initial matching.
mw,matching=wrapper('FAST_CLOCK_MATCHING_ARITHMETIC_V001.json')
for name,expected in matching['input_sha256'].items():check('matching_input',sha(HERE/name)==expected)
check('matching_script_identity',sha(HERE/'fast_clock_matching_arithmetic_v001.py')==matching['script_sha256'])
check('matching_reference',matching['reference']==ref and matching['slow_reference_rows']==slow)
check('matching_census',len(matching['rows'])==4)
for m in matching['rows']:
    row=next(r for r in rows if r['gap']==m['cutoff'] and r['order']==m['order'])
    kb=sum(map(d,row['weights']))+beta;f=beta/kb
    near('matching_fraction',m['f'],f)
    check('matching_sample_census',len(m['matched_slow_rows'])==64)
    for old,new in zip(slow,m['matched_slow_rows']):
        check('matching_epoch',old['a']==new['a'])
        for line in range(2):
            near('matched_slow_first_column',new['state'][line][0],d(old['state'][line][0])+(f-1)*d(old['state'][line][1]))
            near('matched_slow_second_column',new['state'][line][1],f*d(old['state'][line][1]))
    for col in range(2):
        peak=max(m['matched_slow_rows'],key=lambda v:abs(v['state'][0][col]))
        check('matching_peak_epoch',peak['a']==m['sampled_peak'][col]['a'])
        check('matching_peak_value',abs(peak['state'][0][col])==m['sampled_peak'][col]['absolute_tilt'])
    check('matching_endpoint',m['matched_slow_rows'][-1]==m['endpoint'])
for c in matching['clock_controls_years']:
    near('matching_clock_years',c['tau_star_Julian_years'],d(c['eta'])/h0/Decimal(31557600))

sha(HERE/'FAST_CLOCK_INITIAL_LAYER_V001.md')
output=dict(status='ACCEPTED_SAVED_ARITHMETIC' if not failures else 'AUDIT_FAILED',
    files=files,arithmetic_precision_decimal_digits=60,arithmetic_tolerance=2e-12,
    audit_check_total=sum(counts.values()),audit_check_counts=dict(counts),maximum_errors=maxima,failures=failures,
    producer_gate_count=sum(producer_counts.values()),producer_gate_maxima=producer_maxima,
    case_summary=summaries,quadrature_contrasts=contrast_summary,
    total_producer_seconds=math.fsum(t['seconds'] for t in collected['timing']),
    maximum_producer_self_rss_bytes=max(t['peak_self_rss_bytes'] for t in collected['timing']),
    scope='Saved-data audit by original implementation author with separately coded decimal arithmetic; peer preflight remains separate. No numerical producer import, ODE, eigenproblem or propagation. Secondary trajectories were not saved: their error summaries are authenticated and threshold-checked, not regenerated. Peaks are over 64 saved epochs, not continuous-time maxima. Eta values are illustrative cosmological clocks; no microscopic-clock exclusion.')
output['audit_source_sha256']=sha(Path(__file__))
print(enc(output).decode())
