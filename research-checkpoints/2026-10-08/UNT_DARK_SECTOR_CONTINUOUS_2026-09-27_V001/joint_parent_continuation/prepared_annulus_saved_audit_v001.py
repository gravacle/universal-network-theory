"""Saved-state/row arithmetic only; no ODE solve, model import, or writes."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
STEM = 'PREPARED_ANNULUS_RELEASE_V001'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    fp, rp = HERE/(STEM+'_FROZEN.json'), HERE/(STEM+'_RESULTS.json')
    frozen, result = json.loads(fp.read_text()), json.loads(rp.read_text())
    v = result['payload']
    assert result['status'] == 'COMPLETE'
    assert result['freeze_sha256'] == sha(fp)
    assert result['payload_sha256'] == hashlib.sha256(canon(v)).hexdigest()
    assert len(frozen['files']) == 21
    for name, expected in frozen['files'].items():
        path = (PROJECT/name).resolve(); path.relative_to(PROJECT)
        assert sha(path) == expected, name
    assert frozen['configuration'] == v['configuration']
    transport = json.loads((HERE/(STEM+'_CAPTURE_TRANSPORT.json')).read_text())
    decoded = zlib.decompress(base64.b64decode(transport['data']))
    assert len(decoded) == transport['uncompressed_bytes'] == 1240186
    assert hashlib.sha256(decoded).hexdigest() == transport['uncompressed_sha256'] == sha(rp)
    assert decoded == rp.read_bytes()
    old = json.loads((HERE/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json').read_text())
    assert hashlib.sha256(canon(old['payload'])).hexdigest() == old['payload_sha256'] == frozen['ancestor_payload_sha256']
    assert len(v['checks']) == len({c['name'] for c in v['checks']}) == 173
    assert all(c['passed'] and 0 <= c['residual'] <= c['tolerance'] for c in v['checks'])
    expected = {(s,r,n) for s in (0,1,2) for r in (1/4096,1/8192) for n in (64,128)}
    assert len(v['cases']) == 12
    assert {(c['state_index'],c['inner_radius'],c['cells']) for c in v['cases']} == expected
    maxima, count = {}, 0

    def near(label, actual, expected, tolerance=5e-12):
        nonlocal count
        error = abs(actual-expected)
        assert math.isfinite(error) and error <= tolerance*max(1.,abs(expected)), (label,error,actual,expected)
        maxima[label] = max(maxima.get(label,0.),error)
        count += 1

    def bounded(a, gs):
        q=1+(a/gs)**2
        return a/math.sqrt(q), q**-1.5, -3*a/gs**2*q**-2.5

    states = {}
    for s in v['state_summaries']:
        i=s['index']; original=old['payload']['cases'][i]; obs=original['observations'][0]
        d,w,y,vel=(original['delta'],original['weights'],obs['y'],obs['v'])
        assert (len(d),original['order'],original['dt']) == (s['order'],s['order'],s['preparation_dt'])
        kb=math.fsum(w); b=math.fsum(a*z*x for a,z,x in zip(w,d,y)); vb=math.fsum(a*z*x for a,z,x in zip(w,d,vel))
        kinetic=math.fsum(a*x*x/2 for a,x in zip(w,vel))
        quadratic=math.fsum(a*z*z*x*x/2 for a,z,x in zip(w,d,y))
        quartic=math.fsum(a*x**4/4 for a,x in zip(w,y))
        # Algebraic positive cubic root; this is no trajectory or metric solve.
        ys=[2*z/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*s['gs']/(2*z*z))/3) for z in d]
        du=math.fsum(a*(z*z*x*x/2+3*x**4/4) for a,z,x in zip(w,d,ys))
        e0=kinetic+quadratic+quartic
        for label,value in [('Kb',kb),('B',b),('VB',vb),('kinetic',kinetic),('quadratic',quadratic),('quartic',quartic),('E0',e0),('DeltaU',du),('C',2/kb),('Lambda',2*du/kb)]:
            near('state_'+label,s[label],value)
        hc,hp,hpp=bounded(.0025,s['gs'])
        near('state_complete_energy',kb*.0025**2/2+e0-b*hc,s['old_clamp_energy'])
        near('state_work',s['old_clamp_energy'],s['old_clamp_work'])
        near('weak_rate_coefficient',s['weak_rate_coefficient'],vb*hp/(b*hpp))
        for a,z,x in zip(s['local_curvature_frequencies'],d,y): near('local_curvature_frequency',a,math.sqrt(z*z+3*x*x))
        for gap,key in [('0.0','endpoint_full_band_difference'),('0.001','endpoint_same_band_quadrature_difference')]:
            near('baseline_contrast',s[key],du-v['endpoint_continuum_contrasts'][gap]['192'])
        states[i]=s

    summaries=[]
    for c in v['cases']:
        assert c['status'] == 'COMPLETE'
        s=states[c['state_index']]; l=c['inner_radius']; n=c['cells']; rows=c['rows']
        assert len(rows)==n+1
        near('constant_flux_scaling',c['constant_flux'],l*l*c['constant_scaled_flux'])
        near('K_integrals',c['constant_scaled_flux'],c['A_over_D_integral']/c['inverse_scaled_D_integral'])
        for j,r in enumerate(rows):
            x=1+j/n; u=r['u']; f=1-l*u; lapse=math.exp(.0025*l*(x-2)); a=.0025*math.sqrt(f)
            h,hp,hpp=bounded(a,s['gs'])
            e=s['E0']+s['DeltaU']-s['B']*h+a*s['B']*hp
            denominator=1+s['C']*l*x*s['B']*hpp*.0025/2
            slope=(-u/x+s['C']*l*x*e+2*s['C']*math.sqrt(f)*s['B']*hp)/denominator
            dd=lapse*x*x*s['B']*hpp*math.sqrt(f); aa=lapse*lapse*x*x*s['VB']*hp
            rate=(c['constant_scaled_flux']-aa)/dd
            divergence=2*s['B']*math.sqrt(f)*hp/(l*x)-s['B']*hpp*.0025*slope/2
            rho=s['C']*(e+divergence); curvature=(u+x*slope)/(l*x*x)
            gm=l*l*x*u/2; gmsub=gm-s['Lambda']*(l*x)**3/6
            expected_fields=dict(x=x,r=l*x,f=f,lapse=lapse,acceleration=a,held_source=h,
                u_x=slope,metric_denominator=denominator,scaled_D=dd,scaled_A=aa,eta_r=rate,
                acceleration_dot=math.sqrt(f)*rate,proper_source_rate=hp*math.sqrt(f)*rate/lapse,
                source_fractional_rate=hp*math.sqrt(f)*rate/(lapse*h),
                weak_eta_r=s['weak_rate_coefficient']*(2/x**2-1),
                interaction_quench=-s['B']*(h-s['old_clamp_h']),mode_density=rho,curvature_density=curvature,
                source_aBhprime=a*s['B']*hp,polarization_divergence=divergence,GM_geometric=gm,GM_Lambda_subtracted=gmsub)
            for label,wanted in expected_fields.items(): near('row_'+label,r[label],wanted)
            near('original_constraint',rho,curvature)
            near('release_flux',dd*r['eta_r']+aa,c['constant_scaled_flux'])
            near('weak_difference',r['weak_rate_difference'],r['eta_r']-r['weak_eta_r'])
            assert f>0 and lapse>0 and dd<0 and denominator!=0
        near('inner_mass',rows[0]['GM_Lambda_subtracted'],.0025*l*l)
        near('eta_inner',rows[0]['eta'],0.,2e-11)
        near('eta_outer',rows[-1]['eta'],0.,2e-11)
        near('independent_eta_outer',c['independent_gauss_eta_at_outer'],0.,2e-7)
        for label,column in [('min_f','f'),('min_lapse','lapse')]: near('summary_'+label,c[label],min(r[column] for r in rows))
        near('min_D',c['min_abs_scaled_D'],min(abs(r['scaled_D']) for r in rows))
        near('min_denominator',c['min_abs_metric_denominator'],min(abs(r['metric_denominator']) for r in rows))
        near('annulus_mass',c['annulus_GM_geometric'],rows[-1]['GM_geometric']-rows[0]['GM_geometric'])
        near('annulus_subtracted_mass',c['annulus_GM_Lambda_subtracted'],rows[-1]['GM_Lambda_subtracted']-rows[0]['GM_Lambda_subtracted'])
        assert c['fd_metric_node_indices']==list(range(3,n-2))
        assert c['fd_release_node_indices']==list(range(6,n-5))
        # Reconstruct the saved finite-difference controls from all stored nodes.
        def deriv(a):
            co=(-1,9,-45,0,45,-9,1)
            return [sum(cc*a[i+j] for j,cc in enumerate(co))*n/60 for i in range(len(a)-6)]
        ufd=deriv([r['u'] for r in rows]); eta_fd=[z/l for z in deriv([r['eta'] for r in rows])]
        flux=[r['scaled_D']*z+r['scaled_A'] for r,z in zip(rows[3:-3],eta_fd)]
        for got,wanted in zip(deriv(flux),c['fd_release_residual']): near('fd_release_recombination',got,wanted)
        for z,r,wanted in zip(ufd,rows[3:-3],c['fd_metric_residual']):
            e=s['E0']+s['DeltaU']-s['B']*r['held_source']+r['source_aBhprime']
            hp=bounded(r['acceleration'],s['gs'])[1]
            residual=r['metric_denominator']*z+r['u']/r['x']-s['C']*l*r['x']*e-2*s['C']*math.sqrt(r['f'])*s['B']*hp
            near('fd_metric_recombination',residual,wanted)
        summaries.append(dict(state=c['state_index'],inner_radius=l,cells=n,min_f=c['min_f'],
            inner_source_rate=rows[0]['proper_source_rate'],outer_source_rate=rows[-1]['proper_source_rate'],
            inner_fractional_rate=rows[0]['source_fractional_rate'],outer_fractional_rate=rows[-1]['source_fractional_rate'],
            max_abs_eta=max(abs(r['eta']) for r in rows),eta_outer=rows[-1]['eta'],
            independent_outer=c['independent_gauss_eta_at_outer'],
            weak_max_scaled=c['weak_oracle_max_scaled_difference'],
            max_curvature_frequency=max(s['local_curvature_frequencies'])))
    out=dict(status='PASS_SAVED_DATA_AUDIT',source_sha256=sha(Path(__file__)),
        freeze_sha256=sha(fp),result_sha256=sha(rp),payload_sha256=result['payload_sha256'],
        transport_bytes_verified=len(decoded),authenticated_input_count=21,scientific_cases=12,
        radial_rows=sum(len(c['rows']) for c in v['cases']),original_checks=173,
        independent_arithmetic_checks=count,maxima=maxima,summaries=summaries,
        original_maximum_scaled_gate=max(v['checks'],key=lambda c:c['residual']/c['tolerance']),
        elapsed_seconds=v['elapsed_seconds'],peak_self_rss_bytes=v['peak_rss_bytes'],
        scope='Read-only stored-state and row arithmetic; no ODE, release evolution, or new source preparation.')
    print(json.dumps(out,sort_keys=True,allow_nan=False))


if __name__ == '__main__': main()
