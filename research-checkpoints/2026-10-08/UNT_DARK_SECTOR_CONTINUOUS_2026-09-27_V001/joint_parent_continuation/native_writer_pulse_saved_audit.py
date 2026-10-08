"""Read-only post-execution arithmetic; never imports/evolves native matrices."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
encode=lambda o:json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
freeze=ROOT/'native_writer_pulse_frozen.json'
spec=json.loads(freeze.read_text())
for name,h in spec['files'].items(): assert sha(WORKSPACE/name)==h,name
path=ROOT/'native_writer_pulse_results.json'; result=json.loads(path.read_text());p=result['payload']
assert result['status']=='COMPLETE' and result['freeze_sha256']==sha(freeze)
assert result['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
assert len(p['checks'])==1631 and all(c['passed'] and math.isfinite(c['residual']) and c['residual']<=c['tolerance'] for c in p['checks'])
old=json.loads((ROOT/'RECORD_ADDITION_RESULTS.json').read_text())['payload']
maxima={'arithmetic_absolute':0.,'switch_work_error':0.,'central_derivative_error':0.,'Richardson_derivative_error':0.,'blank_R_linear':0.}
rows=[];pulsecount=0;min_signal=math.inf;kranges={};workranges={}
def close(a,b,tol=1e-12):
    e=abs(a-b);maxima['arithmetic_absolute']=max(maxima['arithmetic_absolute'],e)
    assert e<=tol*max(1.,abs(a),abs(b)),(a,b)
for case,prior in zip(p['cases'],old['cases']):
    name=case['name'];assert name==prior['name']
    assert case['parameters']==prior['parameters']
    assert [a['age'] for a in case['ages']]==[0.,.25,.5,1.,2.]
    kvalues=[];wvalues=[]
    for age,priorage in zip(case['ages'],prior['hold']):
        close(age['record_count'],priorage['record_count'])
        slope=4*(1-priorage['record_count']-case['parameters']['lambda_R']*priorage['link_occupation']-priorage['energy_terms']['record_incidence_feedback'])
        close(age['copy_kernel_initial_slope'],slope)
        close(age['response_series_coefficients']['K'][0],0.)
        close(age['response_series_coefficients']['K'][1],-slope/2)
        close(age['response_series_coefficients']['R'][0],age['initial_Ysum'])
        pulses={(x['duration'],x['epsilon']):x for x in age['pulses']}
        assert set(pulses)=={(t,e) for t in [.08,.04,.02,.01] for e in [-.01,.01,-.005,.005]}
        pulsecount+=len(pulses)
        for (t,e),pulse in pulses.items():
            close(pulse['work_on'],e*age['initial_K'])
            close(pulse['net_work'],pulse['work_on']+pulse['work_off'])
            maxima['switch_work_error']=max(maxima['switch_work_error'],abs(pulse['held_energy_change']-pulse['net_work']))
            assert abs(pulse['held_energy_change']-pulse['net_work'])<=1e-11
            wvalues.append(pulse['net_work'])
        assert {(x['duration'],x['observable']) for x in age['responses']}=={(t,o) for t in [.08,.04,.02,.01] for o in ['K','R']}
        for response in age['responses']:
            t,key=response['duration'],response['observable'];exact=response['exact_linear_response'];central=[]
            for entry in response['central']:
                e=entry['amplitude'];raw=(pulses[(t,e)]['change'][key]-pulses[(t,-e)]['change'][key])/2
                value=raw/e;central.append(value)
                close(entry['derivative'],value);close(entry['error'],value-exact)
                bound=2*(4*t)**3*e**2/6
                close(entry['analytic_error_bound'],bound);close(entry['derivative_roundoff_allowance'],1e-12/e)
                assert abs(value-exact)<=bound+1e-12/e
                maxima['central_derivative_error']=max(maxima['central_derivative_error'],abs(value-exact))
            rich=(4*central[1]-central[0])/3
            close(response['amplitude_Richardson'],rich);close(response['amplitude_Richardson_error'],rich-exact)
            rb=2*(4*t)**5*.01**4/288+(4*1e-12/.005+1e-12/.01)/3
            assert abs(rich-exact)<=rb
            maxima['Richardson_derivative_error']=max(maxima['Richardson_derivative_error'],abs(rich-exact))
            power=2 if key=='K' else 1
            close(response['leading_coefficient'],age['response_series_coefficients'][key][power-1])
            close(response['normalized_linear_response'],exact/t**power)
            close(response['normalized_leading_error'],exact/t**power-response['leading_coefficient'])
            assert abs(response['normalized_leading_error'])<=response['normalized_remainder_bound']+1e-11/t**power
            if name=='copying_off' and key=='R': maxima['blank_R_linear']=max(maxima['blank_R_linear'],abs(exact))
            if key=='K':
                kvalues.append(exact)
                if t==.01:
                    positive=pulses[(t,.005)]['change']['K'];signal=abs(positive)/1e-12
                    min_signal=min(min_signal,signal)
                    assert positive*response['leading_coefficient']>0 and signal>10
        short={r['observable']:r for r in age['responses'] if r['duration']==.01}
        rows.append({'preparation':name,'age':age['age'],'record_count':age['record_count'],'copy_kernel_initial_slope':slope,
                     'K_linear_at_tau_001':short['K']['exact_linear_response'],'R_linear_at_tau_001':short['R']['exact_linear_response'],
                     'positive_short_K_change':pulses[(.01,.005)]['change']['K'],
                     'positive_short_R_change':pulses[(.01,.005)]['change']['R'],
                     'positive_short_work':pulses[(.01,.005)]['net_work']})
    kranges[name]=[min(kvalues),max(kvalues)];workranges[name]=[min(wvalues),max(wvalues)]
assert pulsecount==240 and len(rows)==15
categories={}
for key in ['U_taylor','tangent_taylor','Kubo8','Kubo16','Kubo_orders','pulse_energy','full_switch_work','hold_taylor','state_norm','double_commutator']:
    chosen=[c['residual'] for c in p['checks'] if c['name'].endswith(':'+key)]
    categories[key]={'count':len(chosen),'maximum_absolute_residual':max(chosen)}
out={'status':'PASS','mode':'saved-data scalar audit only; no propagation','source_sha256':sha(Path(__file__)),
     'result_sha256':sha(path),'freeze_sha256':sha(freeze),'freeze_file_count':len(spec['files']),
     'checks':len(p['checks']),'pulse_count':pulsecount,'age_count':len(rows),'seconds_reported':result['seconds'],
     'peak_self_rss_bytes_reported':result['peak_self_rss_bytes'],'audit_maxima':maxima,
     'positive_short_K_min_raw_allowance_multiple':min_signal,'saved_check_categories':categories,
     'K_linear_response_ranges':kranges,'pulse_work_ranges':workranges,'rows':rows}
print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))
