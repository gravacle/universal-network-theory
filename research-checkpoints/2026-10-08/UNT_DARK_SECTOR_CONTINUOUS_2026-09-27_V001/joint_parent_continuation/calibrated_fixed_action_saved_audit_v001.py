"""Saved columns and relaxed algebra only; no finite-action orbit or quadrature."""
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    file=HERE/'CALIBRATED_FIXED_ACTION_V001_RESULTS.json'
    freeze=HERE/'CALIBRATED_FIXED_ACTION_V001_FROZEN.json'
    out=json.loads(file.read_text());p=out['payload'];f=json.loads(freeze.read_text())
    assert out['freeze_sha256']==sha(freeze)
    assert out['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    assert p['status']=='COMPLETE' and not p['failures']
    assert sum(p['check_counts'].values())==4254292
    for name,digest in f['files'].items():
        path=Path(name) if Path(name).is_absolute() else ROOT/name
        path.resolve().relative_to(ROOT.resolve())
        assert sha(path)==digest,name
    cal=json.loads((HERE/'ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json').read_text())['payload']
    old=json.loads((HERE/'PREPARED_ACTION_RETURN_V001_RESULTS.json').read_text())['payload']
    history=json.loads((HERE/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json').read_text())['payload']
    cases={(c['gap'],c['order'],c['dt'],c['duration']):c for c in history['cases']}
    def rows(name):
        result=[]
        for r in p[name]:
            assert len(r)==len(p['columns'][name])
            assert all(math.isfinite(x) for x in r)
            result.append(dict(zip(p['columns'][name],r)))
        return result
    branches=rows('branches');origins=rows('origins');pred=rows('predictions');sat=rows('saturation')
    assert len(branches)==len(sat)==648 and len(origins)==36 and len(pred)==1944
    assert {r['branch'] for r in branches}=={r['branch'] for r in sat}==set(range(648))
    assert {r['template'] for r in origins}==set(range(36))
    assert {(r['branch'],r['physical_field_index']) for r in pred}=={(b,i) for b in range(648) for i in range(3)}
    bindex={r['branch']:r for r in branches};oindex={r['template']:r for r in origins}
    count=0;maxima={};spectra=[]
    def check(name,a,b,scale=None,tol=2e-12):
        nonlocal count
        err=abs(a-b)/(max(abs(b),1e-300) if scale is None else scale)
        assert math.isfinite(err) and err<=tol,(name,err)
        maxima[name]=max(maxima.get(name,0.),err);count+=1
    for ti,t in enumerate(old['rows']):
        c=cases[(t['gap'],t['mode_order'],t['dt'],t['duration'])]
        w,d=c['weights'],c['delta'];md=t['mode_data'];i0=math.fsum(w)
        spectra.append((d,w,i0))
        mu=math.fsum(wj*3*(ej+pj)/(dj**4+4*ej) for wj,dj,ej,pj in
                     zip(w,d,md['zero_source_energy'],md['zero_source_pressure']))/i0
        o=oindex[ti]
        check('origin_saved_slope',o['mu0_saved'],mu)
        check('origin_orbit_slope',o['mu0_orbit'],mu,scale=1.)
        check('origin_energy',o['energy'],math.fsum(wj*ej for wj,ej in zip(w,md['zero_source_energy'])))
        check('origin_pressure',o['pressure'],math.fsum(wj*pj for wj,pj in zip(w,md['zero_source_pressure'])))
        frequencies=[2*math.pi/t0 for t0 in md['zero_source_period']]
        check('origin_frequency_min',o['omega_min'],min(frequencies))
        check('origin_frequency_max',o['omega_max'],max(frequencies))
    for b in branches:
        c=cal['rows'][b['branch']]
        assert b['template']==c['template'] and b['reference']==c['reference']
        for key in ('gstar_m_s2','S','gs_m_s2'):
            check('branch_'+key,b[key],c[key])
        check('physical_scale_product',b['gs_m_s2'],b['gstar_m_s2']*b['S'])
    duplicate={};signed=[]
    for r in pred:
        b=bindex[r['branch']];ti=b['template'];d,w,i0=spectra[ti]
        g=p['configuration']['physical_fields_m_s2'][r['physical_field_index']]
        scale,S,gs=b['gstar_m_s2'],b['S'],b['gs_m_s2']
        G=g/scale;z=(g/gs)**2;h=G/math.sqrt(1+z);hp=(1+z)**(-1.5)
        check('dimensionless_field',r['G'],G)
        check('new_bounded_source',r['h'],h)
        check('physical_force_ratio',r['gN_over_g'],r['gN_m_s2']/g)
        check('origin_departure',r['departure_from_mu0'],r['gN_over_g']-oindex[ti]['mu0_saved'],scale=1.)
        lower=g*z*(2+z)/(1+z)**2
        check('universal_lower',r['universal_lower_m_s2'],lower)
        # Independent closed-form relaxed cubic, not a new finite-I orbit solve.
        star=[2*dj/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/(2*dj*dj))/3) for dj in d]
        Brel=math.fsum(wj*dj*yj for wj,dj,yj in zip(w,d,star))
        minimum=-math.fsum(wj*(.5*dj*dj*yj*yj+.75*yj**4) for wj,dj,yj in zip(w,d,star))
        relaxed=scale*(G-hp*Brel/i0)
        check('relaxed_force',r['gN_relaxed_m_s2'],relaxed,scale=g)
        check('relaxed_minimum',r['weighted_minimum'],minimum)
        work=i0*G*G/2+r['weighted_minimum']+r['weighted_excitation']-old['rows'][ti]['return_energy']
        check('ideal_work_difference',r['ideal_work_from_zero_source'],work,
              scale=max(abs(i0*G*G/2),old['rows'][ti]['return_energy']))
        assert lower<=r['gN_m_s2']+2e-12*g
        assert r['gN_relaxed_m_s2']<=r['gN_m_s2']+2e-12*g
        assert r['gN_m_s2']<=g+2e-12*g and r['gN_m_s2']>0
        # Recover the implied aggregate mean to test physical normalization/order.
        implied_B=i0*(G-r['gN_m_s2']/scale)/hp
        assert -2e-10*i0*h<=implied_B<=Brel+2e-10*i0*h
        assert r['weighted_excitation']>0 and 0<r['omega_min']<=r['omega_max']
        diff=r['signed_64_minus_128_gN_over_g'];signed.append(diff)
        assert abs(diff)<=2e-8
        key=(ti,scale,S,g)
        if key in duplicate:
            earlier=duplicate[key]
            for name in ('gN_m_s2','gN_relaxed_m_s2','weighted_minimum','weighted_excitation',
                         'signed_64_minus_128_gN_over_g'):
                check('duplicate_reference_'+name,r[name],earlier[name],scale=max(g,abs(r[name])))
        else:
            duplicate[key]=r
    for r in sat:
        b=bindex[r['branch']];c=cal['rows'][r['branch']];i0=spectra[b['template']][2]
        ratio=r['C3_over_gs4'];relratio=r['relaxed_C3_over_gs4']
        check('dimensioned_C3',r['C3_acceleration4'],b['gs_m_s2']**4*ratio)
        check('saturation_relaxed_derivative',relratio,1/(c['dS_dQ']*i0*b['S']))
        check('saturation_minimum',r['weighted_minimum'],-c['Q'])
        assert 0<ratio<=relratio+2e-12<=1+4e-12
        assert r['weighted_excitation']>0 and 0<r['omega_min']<=r['omega_max']
    check('signed_quadrature_maximum',max(abs(x) for x in signed),p['maximum_errors']['quadrature_D_over_G'])
    summaries=[]
    for fi,g in enumerate(p['configuration']['physical_fields_m_s2']):
        group=[r for r in pred if r['physical_field_index']==fi]
        summaries.append(dict(g_m_s2=g,count=len(group),ranges={key:
            dict(minimum=min(r[key] for r in group),maximum=max(r[key] for r in group))
            for key in ('gN_over_g','gN_m_s2','departure_from_mu0','gN_relaxed_m_s2','universal_lower_m_s2')}))
    return dict(status='ACCEPTED_SAVED_ALGEBRA',script_sha256=sha(Path(__file__)),
        result_sha256=sha(file),freeze_sha256=sha(freeze),payload_sha256=out['payload_sha256'],
        frozen_members=len(f['files']),branch_count=648,origin_count=36,physical_count=1944,saturation_count=648,
        producer_checks=sum(p['check_counts'].values()),independent_arithmetic_checks=count,
        maximum_relative_or_scale_normalized_errors=maxima,physical_summary=summaries,
        saturation_ranges={k:dict(minimum=min(r[k] for r in sat),maximum=max(r[k] for r in sat))
                           for k in ('C3_acceleration4','C3_over_gs4','relaxed_C3_over_gs4')},
        signed_quadrature_differences=dict(negative=sum(x<0 for x in signed),zero=sum(x==0 for x in signed),
            positive=sum(x>0 for x in signed),minimum=min(signed),maximum=max(signed),maximum_absolute=max(map(abs,signed))),
        representative_branch=bindex[108],representative_predictions=[r for r in pred if r['branch']==108],
        representative_saturation=next(r for r in sat if r['branch']==108),
        producer_seconds=p['seconds'],producer_self_RSS_bytes_on_Darwin=p['peak_self_rss_platform_units'],
        orbit_rule_evaluations=p['orbit_rule_evaluations'],
        limitations=['No finite-action radius inversion, angle quadrature or propagation repeated.',
            'Relaxed minima/forces independently evaluated by closed-form cubic algebra.',
            'Active aggregate B and both quadrature orders are not saved separately; their full orbit agreement remains producer evidence.',
            'Physical field probes are not a galaxy solution or observational fit.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
