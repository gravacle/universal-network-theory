"""Algebraic saved-witness audit; no angle quadrature, root-action solve or propagation."""
import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent.parent
read=lambda name:json.loads((HERE/name).read_text())
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
encode=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
name='FIXED_ACTION_FINITE_FIELD_V001_RESULTS.json'; frozen_name=name.replace('RESULTS','FROZEN')
result=read(name); payload=result['payload']; frozen=read(frozen_name)
checks=0; maxima={}


def require(value,label):
    global checks
    checks+=1
    if not value: raise AssertionError(label)


def near(label,a,b,scale=1.,tol=2e-8):
    error=abs(a-b)/max(abs(scale),1e-300)
    maxima[label]=max(maxima.get(label,0.),error)
    require(math.isfinite(error) and error<=tol,(label,error))


@lru_cache(None)
def star(d,h):
    lo,hi=0.,h/d
    for _ in range(100):
        mid=(lo+hi)/2
        if mid**3+d*d*mid>d*h: hi=mid
        else: lo=mid
    return (lo+hi)/2


for relative,digest in frozen['files'].items():
    path=(ROOT/relative).resolve(strict=True)
    require(path.is_relative_to(ROOT) and sha(path)==digest,'input identity')
require(result['freeze_sha256']==sha(HERE/frozen_name),'freeze')
require(result['payload_sha256']==hashlib.sha256(encode(payload)).hexdigest(),'payload')
require(result['status']=='COMPLETE' and not payload['failures'],'qualification')
require(sum(payload['check_counts'].values())==641600,'original checks')
require(payload['config']==frozen['config'],'config')
for key,value in payload['maximum_errors'].items():
    tol=2e-12 if key.startswith('synthetic_signed') or key in ('zero_action_cubic','zero_mean_parity','control_negative_radicand') else 2e-8
    require(math.isfinite(value) and 0<=value<=tol,'control maximum '+key)
old=read('PREPARED_ACTION_RETURN_V001_RESULTS.json')['payload']['rows']
states=read('COMMON_HISTORY_MECHANISM_V001_RESULTS.json')['payload']['cases']
phase=read('COMMON_HISTORY_PHASE_MEAN_V003_RESULTS.json')['payload']['rows']
state_index={(x['gap'],x['order'],x['dt'],x['duration']):x for x in states}
phase_index={(x['gap'],x['mode_order'],x['dt'],x['duration'],x['g']):x for x in phase}
rows=payload['rows']; fields=[0.,1e-5,.0025,.01,.04,1.,100.]; gs=payload['gs']
require(len(rows)==252 and {(x['template'],x['G']) for x in rows}==set(itertools.product(range(36),fields)),'complete 252 census')
row_index={(r['template'],r['G']):r for r in rows}; witnesses=0; bounds=[]
for row in rows:
    previous=old[row['template']]; md=previous['mode_data']; G=row['G']; h=G/math.sqrt(1+(G/gs)**2); hp=(1+(G/gs)**2)**-1.5
    key=(previous['gap'],previous['mode_order'],previous['dt'],previous['duration']); source=state_index[key]
    delta,weights=source['delta'],source['weights']; kb=source['Kb']
    for key2,oldkey in [('gap','gap'),('mode_order','mode_order'),('dt','dt'),('duration','duration'),('preparation_G','g')]:
        require(row[key2]==previous[oldkey],'unchanged row identity')
    near('source h',row['h'],h,tol=2e-12); near('source derivative',row['hprime'],hp,tol=2e-12)
    near('intrinsic sum',row['intrinsic_energy'],row['weighted_energy_minimum']+row['weighted_excitation'])
    near('ideal work ledger',row['ideal_adiabatic_energy_difference'],kb*G*G/2+row['intrinsic_energy']-previous['return_energy'])
    minimum=math.fsum(w*(-.5*d*d*(s:=star(d,h))**2-.75*s**4) for w,d in zip(weights,delta))
    near('weighted minimum',row['weighted_energy_minimum'],minimum,max(abs(minimum),previous['return_energy']))
    relaxed=G-hp*math.fsum(w*d*star(d,h) for w,d in zip(weights,delta))/kb
    if G:
        near('force ratio',row['D_over_G'],row['D']/G,tol=2e-12)
        near('origin departure',row['finite_G_departure_from_origin_slope'],row['D']/G-row['mu_linear_origin'],tol=2e-12)
        require(relaxed-2e-12*G<=row['D']<=G+2e-12*G,'post-proof force ordering')
        bounds.append(dict(template=row['template'],G=G,D=row['D'],D_relaxed=relaxed))
    else:
        require(row['D']==0 and row['D_over_G'] is None,'exact origin')
    require([v['mode'] for v in row['modal_witnesses']]==[0,len(delta)//2,len(delta)-1],'witness census')
    for z in row['modal_witnesses']:
        witnesses+=1; j=z['mode']; d=delta[j]; c=(z['a']+z['b'])/2; r=(z['b']-z['a'])/2; s=star(d,h)
        require(z['delta']==d and z['target_I']==md['action'][j],'original witness input')
        near('witness action target',z['solved_I'],z['target_I'],z['target_I'])
        near('witness center cubic',c**3+(d*d+r*r)*c,d*h,max(abs(d*h),1e-20))
        shift=-c*r*r/(d*d+c*c+c*s+s*s); xp=r+shift; xm=shift-r; stiff=d*d+3*s*s
        excess=lambda x:x*x*(stiff/2+s*x+x*x/4)
        near('witness minimum',z['energy_minimum'],-.5*d*d*s*s-.75*s**4,max(abs(z['energy_minimum']),z['excitation']))
        near('witness excitation',z['excitation'],excess(xp),z['excitation'])
        near('witness equal endpoints',excess(xp),excess(xm),z['excitation'])
        require(z['omega']>0 and r>0,'positive frequency and width')
        if G:
            require(-2e-12<=z['mean_y']<=c+2e-12 and c<=s+2e-12,'post-proof witness ordering')
        else:
            require(z['mean_y']==0,'zero witness mean')
            near('old origin witness frequency',z['omega'],2*math.pi/md['zero_source_period'][j],z['omega'])
            near('old origin witness energy',z['excitation'],md['zero_source_energy'][j],z['excitation'])
        if G==previous['g']:
            anchor=phase_index[(*key,G)]['mode_data']
            near('old held witness mean',z['mean_y'],anchor['mean_y'][j],max(abs(z['a']),abs(z['b'])))
            near('old held witness frequency',z['omega'],2*math.pi/anchor['periods'][j],z['omega'])
            near('old held witness energy',z['excitation'],anchor['mode_excitation'][j],z['excitation'])
require(witnesses==756,'756 witnesses')
for origin in payload['origin_comparisons']:
    previous=old[origin['template']]; source=state_index[(previous['gap'],previous['mode_order'],previous['dt'],previous['duration'])]; md=previous['mode_data']
    mu=math.fsum(w*3*(e+p)/(d**4+4*e) for w,d,e,p in zip(source['weights'],source['delta'],md['zero_source_energy'],md['zero_source_pressure']))/source['Kb']
    for a,b in [('computed_E','return_energy'),('computed_P','return_pressure')]: near('old origin aggregate '+a,origin[a],previous[b],previous['return_energy'])
    near('old origin slope',origin['stored_mu_linear'],mu,tol=2e-12); near('new origin slope',origin['computed_mu_linear'],mu,tol=2e-12)
for anchor in payload['held_anchor_comparisons']:
    previous=old[anchor['template']]; key=(previous['gap'],previous['mode_order'],previous['dt'],previous['duration'],previous['g']); old_phase=phase_index[key]
    near('old held aggregate D',anchor['D'],old_phase['phase_mean_D'],anchor['G'])
    near('old held aggregate energy',anchor['intrinsic_energy'],previous['held_intrinsic_energy'],max(abs(previous['held_intrinsic_energy']),1e-20))
require(len(payload['origin_comparisons'])==36 and len(payload['held_anchor_comparisons'])==36,'origin/anchor census')
for comparison in payload['resolution_comparisons']:
    G=comparison['G']; a=row_index[(comparison['left_template'],G)]; b=row_index[(comparison['right_template'],G)]
    require(comparison['signed_D_difference']==b['D']-a['D'],'resolution delta')
    require(comparison['D_difference_over_G']==((b['D']-a['D'])/G if G else 0),'scaled resolution delta')
require(len(payload['resolution_comparisons'])==168,'168 comparisons')
print(json.dumps(dict(status='PASS',audit_checks=checks,original_checks=641600,frozen_inputs=len(frozen['files']),
    script_sha256=sha(Path(__file__)),result_sha256=sha(HERE/name),freeze_sha256=sha(HERE/frozen_name),
    payload_sha256=result['payload_sha256'],witnesses=witnesses,maxima=maxima,
    max_resolution_D_over_G=max(abs(c['D_difference_over_G']) for c in payload['resolution_comparisons']),
    template6=[dict(G=r['G'],D_over_G=r['D_over_G'],mu_origin=r['mu_linear_origin']) for r in rows if r['template']==6],
    all_positive_field_rows_ordered=len(bounds),seconds=result['seconds'],peak_self_rss_bytes=result['peak_self_rss_bytes'],
    audit_limit='Full new modal means are not saved; all aggregate mean forces are not independently reconstructed.'),indent=2))
