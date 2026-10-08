"""Read-only saved-state sums and controls; no orbit inversion or quadrature."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    file=HERE/'HOMOGENEOUS_DILUTION_V001_RESULTS.json'
    freeze=HERE/'HOMOGENEOUS_DILUTION_V001_FROZEN.json'
    wrapper=json.loads(file.read_text()); p=wrapper['payload']
    f=json.loads(freeze.read_text())
    assert wrapper['status']=='COMPLETE' and not p['failures']
    assert wrapper['freeze_sha256']==sha(freeze)
    assert wrapper['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    for name,digest in f['files'].items():
        path=Path(name) if Path(name).is_absolute() else ROOT/name
        path.resolve().relative_to(ROOT.resolve())
        assert sha(path)==digest,name
    assert sum(p['check_counts'].values())==568119
    old=json.loads((HERE/'PREPARED_ACTION_RETURN_V001_RESULTS.json').read_text())['payload']
    history=json.loads((HERE/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json').read_text())['payload']
    pulse=json.loads((HERE/'HIGH_GAP_PULSE_V001_RESULTS.json').read_text())['payload']
    cases={(c['gap'],c['order'],c['dt'],c['duration']):c for c in history['cases']}
    templates=[]
    for ti,r in enumerate(old['rows']):
        c=cases[(r['gap'],r['mode_order'],r['dt'],r['duration'])]; m=r['mode_data']
        templates.append(dict(family='original_soft',index=ti,
            identity={k:r[k] for k in ('gap','mode_order','dt','duration','g')},
            delta=c['delta'],weights=c['weights'],I=m['action'],e=m['zero_source_energy'],
            p=m['zero_source_pressure'],omega=[2*math.pi/t for t in m['zero_source_period']],
            Kb=c['Kb'],DeltaU=None))
    for ti,r in enumerate(pulse['cases']):
        m=r['fine_end_state'];s=r['finite_spectrum']
        templates.append(dict(family='soft_plus_hard_pulse',index=ti,
            identity={k:r[k] for k in ('gap','amplitude','cycles')},
            delta=m['delta'],weights=m['weights'],I=m['action'],e=m['energy'],
            p=m['pressure'],omega=m['frequency'],Kb=s['Kb'],DeltaU=s['DeltaU']))
    assert len(templates)==42
    count=0;maxima={}

    def check(label,a,b,scale=None,tolerance=2e-12):
        nonlocal count
        err=abs(a-b)/(max(abs(b),1e-300) if scale is None else scale)
        assert math.isfinite(err) and err<=tolerance,(label,err)
        maxima[label]=max(maxima.get(label,0.),err);count+=1

    factors=(1.,2.,4.,11.,101.,1101.)
    index={(r['template_index'],r['inverse_scale_factor']):r for r in p['rows']}
    assert len(p['rows'])==len(index)==252
    assert set(index)=={(i,a) for i in range(42) for a in factors}
    assert sum(len(r['modal_frequency']) for r in p['rows'])==27684
    for ti,t in enumerate(templates):
        E1=math.fsum(w*e for w,e in zip(t['weights'],t['e']))
        P1=math.fsum(w*p0 for w,p0 in zip(t['weights'],t['p']))
        prior_w=-1.
        for A in factors:
            r=index[(ti,A)];freq=r['modal_frequency'];E,P=r['E'],r['P']
            assert r['family']==t['family'] and r['input_index']==t['index']
            assert r['identity']==t['identity'] and r['unchanged_DeltaU']==t['DeltaU']
            assert len(freq)==len(t['delta'])
            assert all(math.isfinite(o) and o>0 for o in freq)
            assert E>0 and -2e-12*E<=P<=E/3+2e-12*E
            assert E>=E1*A**3*(1-2e-12) and E<=E1*A**4*(1+2e-12)
            check('contact',r['Kb'],math.fsum(t['weights']))
            W=math.fsum(w*(i*A**3)*o for w,i,o in zip(t['weights'],t['I'],freq))
            check('independent_action_enthalpy',E+P,W)
            check('w',r['P_over_E'],P/E)
            check('dust_ratio',r['E_over_present_dust'],E/(E1*A**3))
            check('minimum_frequency',r['minimum_frequency'],min(freq))
            check('maximum_frequency',r['maximum_frequency'],max(freq))
            cc=r['clock_coefficients']
            check('clock_H',cc['H_over_omega'],1/min(freq))
            check('clock_period',cc['fractional_action_change_per_period'],6*math.pi/min(freq))
            assert 0<=cc['frequency_adiabaticity']<=cc['H_over_omega']*(1+2e-12)
            c=r['common_compression_coefficient']
            assert -2e-12<=c<=1/3+2e-12
            assert c<=2*P/(E+P)+2e-12
            assert r['P_over_E']>=prior_w-2e-12
            prior_w=r['P_over_E']
            for name in ('quadrature_max_relative_energy','quadrature_max_energy_scaled_pressure',
                         'quadrature_max_relative_frequency'):
                assert math.isfinite(r[name]) and 0<=r[name]<=2e-8
            if A==1:
                check('saved_E',E,E1)
                check('saved_P',P,P1,scale=E1)
                for o,o1 in zip(freq,t['omega']):
                    check('saved_frequency',o,o1)
    original={(r['identity']['gap'],r['identity']['duration'],r['identity']['g'],
               r['identity']['mode_order'],r['identity']['dt'],r['inverse_scale_factor']):r
              for r in p['rows'] if r['family']=='original_soft'}
    assert len(p['resolution_comparisons'])==144
    for c in p['resolution_comparisons']:
        left,right=((64,.01),(128,.01)) if c['label']=='old_spectral_order' else ((128,.01),(128,.005))
        key=(c['gap'],c['duration'],c['g'])
        x=original[(*key,*left,c['inverse_scale_factor'])]
        y=original[(*key,*right,c['inverse_scale_factor'])]
        for field,value in c['signed_right_minus_left'].items():
            check('resolution_'+field,value,y[field]-x[field],scale=max(abs(y[field]),1e-300))
        check('resolution_relative_energy',c['energy_relative_to_right'],(y['E']-x['E'])/y['E'],scale=1.)
    summaries=[]
    for family in ('original_soft','soft_plus_hard_pulse'):
        for A in factors:
            group=[r for r in p['rows'] if r['family']==family and r['inverse_scale_factor']==A]
            summaries.append(dict(family=family,inverse_scale_factor=A,count=len(group),
                ranges={k:dict(minimum=min(r[k] for r in group),maximum=max(r[k] for r in group))
                        for k in ('P_over_E','E_over_present_dust','common_compression_coefficient',
                                  'minimum_frequency','maximum_frequency')}))
    representative=[{k:v for k,v in index[(ti,A)].items() if k!='modal_frequency'}
                    for ti in (6,41) for A in factors]
    return dict(status='ACCEPTED_SAVED_ARITHMETIC',script_sha256=sha(Path(__file__)),
        result_sha256=sha(file),freeze_sha256=sha(freeze),payload_sha256=wrapper['payload_sha256'],
        frozen_members=len(f['files']),rows=252,modal_frequencies=27684,
        producer_checks=sum(p['check_counts'].values()),independent_arithmetic_checks=count,
        maximum_relative_errors=maxima,summary=summaries,representative=representative,
        producer_seconds=p['seconds'],producer_peak_self_RSS_bytes=p['peak_rss_bytes'],
        limits=['No new orbit roots, quadrature or propagation.',
                'Saved frequencies and inherited actions independently reconstruct aggregate E+P; individual new modal energies/pressures are not saved.',
                'Curvature and the third clock maximum are analytically preflighted producer evidence, not re-evaluated here.',
                'A is a conditional inverse scale factor, not independently identified observed redshift; physical H and inertia clock remain unspecified.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
