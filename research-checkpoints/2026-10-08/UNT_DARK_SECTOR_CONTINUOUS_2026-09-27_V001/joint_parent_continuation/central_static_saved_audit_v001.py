"""Read-only saved arithmetic: no producer import, orbit quadrature or evolution."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(row):
    return tuple(row[k] for k in ('gap', 'mode_order', 'dt', 'duration', 'g'))


def main():
    files = {}
    def read(name):
        path = HERE/name
        files[name] = sha(path)
        return json.loads(path.read_text())
    freeze = read('CENTRAL_STATIC_RESPONSE_V001_FROZEN.json')
    wrapper = read('CENTRAL_STATIC_RESPONSE_V001_RESULTS.json')
    p = wrapper['payload']
    assert wrapper['status'] == 'COMPLETE' and not p['failures']
    assert wrapper['freeze_sha256'] == files['CENTRAL_STATIC_RESPONSE_V001_FROZEN.json']
    assert wrapper['payload_sha256'] == hashlib.sha256(encode(p)).hexdigest()
    assert p['configuration'] == freeze['configuration']
    for name, digest in freeze['files'].items():
        assert sha(ROOT/name) == digest, name
    def inherited(name):
        w = read(name)
        assert w['payload_sha256'] == hashlib.sha256(encode(w['payload'])).hexdigest()
        fr = HERE/name.replace('_RESULTS.json', '_FROZEN.json')
        assert w['freeze_sha256'] == sha(fr)
        return w['payload']
    old = inherited('PREPARED_ACTION_RETURN_V001_RESULTS.json')
    common = inherited('COMMON_HISTORY_MECHANISM_V001_RESULTS.json')
    pulse = inherited('HIGH_GAP_PULSE_V001_RESULTS.json')
    susceptibility = inherited('PREPARED_SUSCEPTIBILITY_V001_RESULTS.json')['rows']
    compression = inherited('PREPARED_COMPRESSION_V001_RESULTS.json')['rows']
    dilution = [r for r in inherited('HOMOGENEOUS_DILUTION_V001_RESULTS.json')['rows'] if r['inverse_scale_factor'] == 1]
    assert len(p['rows']) == len(dilution) == 42
    assert p['original_baseline'] == old['baseline'] == freeze['original_baseline']
    assert sum(p['check_counts'].values()) == 114773 and not p['output_target_exceeded']
    case_index = {(r['gap'],r['order'],r['dt'],r['duration']):r for r in common['cases']}
    counts, maxima, absolute = {}, {}, {}
    def close(kind, actual, expected, scale=None, tol=3e-11):
        if isinstance(actual,list):
            assert len(actual) == len(expected)
            ss = scale if isinstance(scale,list) else [scale]*len(actual)
            for a,b,s in zip(actual,expected,ss):close(kind,a,b,s,tol)
            return
        denom = max(abs(expected) if scale is None else abs(scale),1e-300)
        error = abs(actual-expected)
        ratio = error/denom
        assert math.isfinite(ratio) and ratio <= tol,(kind,actual,expected,ratio)
        counts[kind] = counts.get(kind,0)+1
        maxima[kind] = max(maxima.get(kind,0),ratio)
        absolute[kind] = max(absolute.get(kind,0),error)
    rows = []
    modal_count = 0
    for i,row in enumerate(p['rows']):
        assert row['template_index'] == i and dilution[i]['template_index'] == i
        if i < 36:
            original = old['rows'][i]
            assert identity(row['identity']) == identity(original) == identity(susceptibility[i]) == identity(compression[i])
            source = case_index[(original['gap'],original['mode_order'],original['dt'],original['duration'])]
            md = original['mode_data']
            delta,weights = source['delta'],source['weights']
            actions,energy,pressure = md['action'],md['zero_source_energy'],md['zero_source_pressure']
            omega = [2*math.pi/t for t in md['zero_source_period']]
            old_q,old_mu = susceptibility[i]['modal_q'],susceptibility[i]['mu_linear']
            old_eII = next(x for x in compression[i]['quadratures'] if x['order'] == 128)['energy_curvature']
            du = None
            expected_family,expected_index = 'original_soft',i
            close('inherited_eII',row['modal_eII'],old_eII)
        else:
            source = pulse['cases'][i-36]
            assert row['identity'] == {k:source[k] for k in ('gap','amplitude','cycles')}
            md = source['fine_end_state']
            delta,weights,actions,energy,pressure,omega = [md[k] for k in ('delta','weights','action','energy','pressure','frequency')]
            old_q,old_mu = md['contact_defect'],source['orbit_averaged']['mu_linear']
            du = source['finite_spectrum']['DeltaU']
            expected_family,expected_index = 'soft_plus_hard_pulse',i-36
        assert row['family'] == expected_family and row['input_index'] == expected_index
        assert all(row[k] == dilution[i][k] for k in ('family','input_index','identity','Kb'))
        assert dilution[i]['unchanged_DeltaU'] == du
        count = len(delta)
        assert count == row['modal_count'] and all(len(v)==count for v in (weights,actions,energy,pressure,omega,row['modal_eII'],row['modal_contact_defect'],row['modal_J_static']))
        modal_count += count
        assert all(v>0 and math.isfinite(v) for v in actions+energy+omega+row['modal_eII'])
        qdef = [3*(e+pr)/(d**4+4*e) for d,e,pr in zip(delta,energy,pressure)]
        jvals = [w*w/c+3*act*w for w,c,act in zip(omega,row['modal_eII'],actions)]
        close('modal_deficit',row['modal_contact_defect'],qdef)
        close('inherited_deficit',row['modal_contact_defect'],old_q)
        close('modal_J',row['modal_J_static'],jvals)
        assert all(0<q<1 for q in row['modal_contact_defect'])
        for d,e,q in zip(delta,energy,row['modal_contact_defect']):
            b2 = 4*e/(d*d+math.sqrt(d**4+4*e))
            assert b2/(d*d+b2)-3e-11 <= q <= b2*(2*d*d+b2)/(d*d+b2)**2+3e-11
        kb = math.fsum(weights)
        E = math.fsum(w*e for w,e in zip(weights,energy))
        Pi = math.fsum(w*pr for w,pr in zip(weights,pressure))
        K = math.fsum(w*q for w,q in zip(weights,row['modal_contact_defect']))
        J = math.fsum(w*j for w,j in zip(weights,row['modal_J_static']))
        for key,value in [('Kb',kb),('E',E),('Pi',Pi),('Kcal',K),('J_static',J),('static_wavenumber_squared',J/K),('mu_linear',K/kb),('Pi_over_E',Pi/E),('excitation_active_source',E+3*Pi)]:
            close('aggregate_'+key,row[key],value)
        close('inherited_mu',row['mu_linear'],old_mu)
        close('dilution_E',row['E'],dilution[i]['E'])
        close('dilution_P',row['Pi'],dilution[i]['P'],E)
        assert E>0 and 0<Pi<E/3 and 0<K<kb
        masks = {'all':list(range(count))}
        if i >= 36:
            masks.update(soft=[j for j,d in enumerate(delta) if d<=1],hard=[j for j,d in enumerate(delta) if d>1])
            assert len(masks['hard'])==1
        assert set(row['components'])==set(masks)
        for name,indices in masks.items():
            vals = dict(weight=math.fsum(weights[j] for j in indices),E=math.fsum(weights[j]*energy[j] for j in indices),Pi=math.fsum(weights[j]*pressure[j] for j in indices),Kcal=math.fsum(weights[j]*row['modal_contact_defect'][j] for j in indices),J_static=math.fsum(weights[j]*row['modal_J_static'][j] for j in indices))
            for key,value in vals.items():close('component_'+key,row['components'][name][key],value)
        assert [v['rule'] for v in row['quadrature_controls']]==['GL64','Simpson1024']
        for control in row['quadrature_controls']:
            for key in ('E','Pi','Kcal','J_static'):
                close('saved_quadrature_aggregate_'+key,control[key],row[key],E if key=='Pi' else row[key],2e-8)
            assert all(v['normalized']<=2e-8 for v in control['errors'].values())
        if du is None:
            assert row['center'] is None and row['center_unavailable_reason'] is not None
        else:
            center = row['center']; assert center['DeltaU']==du and center['ordinary_matter']=='absent'
            S=E+3*Pi-2*du; a1=S/(3*K);s2=-a1+(Pi-du)/kb
            rho=E+du+3*(kb-K)*a1
            for key,value in [('active_center_source',S),('a1',a1),('s2',s2),('rho_center_over_C',rho)]:
                close('center_'+key,center[key],value)
            close('center_constraint',rho,-3*kb*s2)
        summary = {k:row[k] for k in ('template_index','family','identity','E','Pi','Kb','Kcal','J_static','mu_linear','static_wavenumber_squared','center')}
        if i>=36:
            summary['soft_fraction']={key:row['components']['soft'][key]/row['components']['all'][key] for key in ('E','Kcal','J_static')}
            R=row['identity']['gap'];EH=row['components']['hard']['E'];beta=row['components']['hard']['weight']
            summary['harmonic_asymptotic_diagnostics']=dict(J_hard_over_4betaR4_div3=row['components']['hard']['J_static']/(4*beta*R**4/3),K_hard_over_3EH_divR4=row['components']['hard']['Kcal']/(3*EH/R**4))
        rows.append(summary)
    sensitivity = p['sensitivity_comparisons']
    assert len(sensitivity)==24
    expected={(gap,dur,g,label) for gap in (.001,.002) for dur in (8,16) for g in (.0025,.01,.04) for label in ('saved_spectral_order','saved_preparation_step')}
    assert {(r['gap'],r['duration'],r['g'],r['label']) for r in sensitivity}==expected
    sensmax={}
    for comparison in sensitivity:
        a,b=[p['rows'][comparison[k]] for k in ('left_template','right_template')]
        for row in (a,b):
            assert all(row['identity'][k]==comparison[k] for k in ('gap','duration','g'))
        assert [(r['identity']['mode_order'],r['identity']['dt']) for r in (a,b)] == ([(64,.01),(128,.01)] if comparison['label']=='saved_spectral_order' else [(128,.01),(128,.005)])
        for key,value in comparison['signed_right_minus_left'].items():
            close('signed_sensitivity',value,b[key]-a[key],max(abs(a[key]),abs(b[key])))
            sensmax[key]=max(sensmax.get(key,0.),abs(value)/max(abs(a[key]),abs(b[key])))
    files[Path(__file__).name]=sha(Path(__file__))
    payload=dict(status='COMPLETE_SAVED_ARITHMETIC_AUDIT',files=files,
        original_payload_sha256=wrapper['payload_sha256'],frozen_member_count=len(freeze['files']),
        census=dict(states=42,original_null_centers=36,owned_pulse_centers=6,modes=modal_count,sensitivity_comparisons=24),
        counts=counts,total_arithmetic_comparisons=sum(counts.values()),maximum_normalized_errors=maxima,maximum_absolute_errors=absolute,
        ranges={family:{key:[min(r[key] for r in rows if r['family']==family),max(r[key] for r in rows if r['family']==family)] for key in ('E','Pi','Kcal','J_static','mu_linear','static_wavenumber_squared')} for family in ('original_soft','soft_plus_hard_pulse')},
        pulse_rows=rows[36:],representative_original=rows[6],sensitivity_maximum_relative_difference=sensmax,
        original_controls=dict(total=sum(p['check_counts'].values()),maximum_normalized_error=max(p['maximum_normalized_errors'].values()),seconds=p['seconds'],peak_self_rss_bytes=p['peak_rss_bytes']),
        scope='Saved algebra/custody only; no new orbit quadrature, producer import, dynamics or radial integration. New eII is compared with independently saved compression for original36 only; pulse eII remains the prospective producer quadrature evidence. J is recombined with original saved frequencies/actions and new eII, with retained inherited numerical uncertainty. No empirical radius or dynamical-stability inference.')
    print(encode(dict(payload=payload,payload_sha256=hashlib.sha256(encode(payload)).hexdigest())).decode())


if __name__=='__main__':main()
