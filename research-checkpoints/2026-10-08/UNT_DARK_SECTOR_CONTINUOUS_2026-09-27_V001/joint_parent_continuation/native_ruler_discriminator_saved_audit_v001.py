"""Saved algebra and initial-vector contractions only; no propagator."""
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
    file=HERE/'NATIVE_RULER_DISCRIMINATOR_V001_RESULTS.json'
    freeze=HERE/'NATIVE_RULER_DISCRIMINATOR_V001_FROZEN.json'
    d=json.loads(file.read_text());p=d['payload'];f=json.loads(freeze.read_text())
    assert p['status']=='COMPLETE' and not p['failures']
    assert d['freeze_sha256']==sha(freeze)
    assert d['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    for name,expected in f['files'].items():
        path=Path(name) if Path(name).is_absolute() else ROOT/name
        path.resolve().relative_to(ROOT.resolve())
        assert sha(path)==expected,name
    assert sum(p['check_counts'].values())==55766
    old=json.loads((HERE/'RECORD_ADDITION_RESULTS.json').read_text())['payload']
    oldcases={c['name']:c for c in old['cases']}
    names=('native','feedback_off','copying_off');ages=(0.,.25,.5,1.,2.)
    times=(.08,.04,.02,.01);amps=(-.01,.01,-.005,.005)
    assert len(p['ages'])==15 and len(p['sectors'])==90
    assert len(p['delays'])==60 and len(p['pulses'])==240 and len(p['constructed_witness'])==6
    aindex={(r['preparation'],r['age']):r for r in p['ages']}
    dindex={(r['preparation'],r['age'],r['duration']):r for r in p['delays']}
    pindex={(r['preparation'],r['age'],r['duration'],r['amplitude']):r for r in p['pulses']}
    assert set(aindex)=={(n,a) for n in names for a in ages}
    assert set(dindex)=={(n,a,t) for n in names for a in ages for t in times}
    assert set(pindex)=={(n,a,t,z) for n in names for a in ages for t in times for z in amps}
    counts={};maxima={}
    def check(label,a,b=0.,scale=1.,tol=1e-11):
        err=abs(a-b)/scale
        assert math.isfinite(err) and err<=tol,(label,err)
        counts[label]=counts.get(label,0)+1;maxima[label]=max(maxima.get(label,0.),err)
    sector_invariants={};retained=0;null=0
    for name in names:
        oldcase=oldcases[name];par=oldcase['parameters'];lam=par['lambda_R'];h=par['h'];t=par['t_hop']
        psi=[complex(x,y) for x,y in zip(oldcase['formed_vector']['real'],oldcase['formed_vector']['imag'])]
        corr=0j;work=0j
        for j,z in enumerate(psi):
            bc=j&1;bi=(j>>1)&1
            for rb in (2,3):
                br=(j>>rb)&1
                target=j^(1<<rb)^2^1
                corr+=psi[target].conjugate()*(1-2*bc)*(1-2*br)*z
                target_y=j^(1<<rb)
                work+=psi[target_y].conjugate()*(-1j)*(1-2*br)*(1-lam*bi)*z
        check('formed_correlation',aindex[name,0.]['correlation'],corr.real)
        check('formed_correlation_imaginary',corr.imag)
        check('formed_impulse_work',aindex[name,0.]['impulse_work_derivative'],work.real)
        for age,old_age in zip(ages,oldcase['hold']):
            a=aindex[name,age]
            check('native_gamma',a['gamma'],lam*t*h*a['correlation'])
            check('cubic',a['impulse_cubic'],a['gamma']/6)
            check('quartic',a['step_quartic'],a['gamma']/24)
            check('old_held_energy',a['held_energy'],oldcase['held_energy'])
            check('old_carrier_readout',a['carrier_probability'],old_age['carrier_right'])
            sectors=[s for s in p['sectors'] if s['preparation']==name and s['age']==age]
            assert len(sectors)==6 and {(s['R'],s['s']) for s in sectors}=={(R,sg) for R in range(3) for sg in (-1,1)}
            check('sector_weight_sum',math.fsum(s['weight'] for s in sectors),1.)
            Es=[];ns=[];Xs=[];Rs=[]
            for s in sectors:
                w=s['weight'];R=s['R'];sg=s['s'];Rs.append(w*R)
                if s['status']=='NUMERICALLY_NULL_WEIGHT_NOT_DIVIDED':
                    null+=1;assert -1e-11<=w<=1e-24;continue
                retained+=1;assert s['status']=='RETAINED'
                X,Y,Z=s['X'],s['Y'],s['Z'];r=math.sqrt(X*X+Y*Y+Z*Z)
                x=2.25-lam*R-t*sg;gap=math.sqrt(x*x+4*h*h)
                L=(2*h*X+x*Z)/gap;S1=(x*X-2*h*Z)/gap;I=(r-L)/2
                minimum=3+R+x/2-gap*r/2
                check('radius',s['radius'],r)
                check('action',s['action'],I)
                check('capacity',s['capacity'],r)
                check('frequency',s['frequency'],gap)
                check('minimum',s['minimum'],minimum)
                check('affine_energy',s['energy'],minimum+gap*I)
                check('incidence_from_Z',s['incidence'],(1-Z)/2)
                check('source_map',s['incidence'],(1-x*r/gap)/2+x*I/gap+h*S1/gap)
                check('signed_moment',s['signed_source_moment'],h*X)
                if s['phi'] is not None:
                    check('canonical_phase',s['phi'],-math.atan2(Y,S1))
                if 'lower_point_stiffness' in s:
                    Q0=2*h*r/gap;k=4*h*r*r/Q0**3;invM=h*Q0
                    check('stiffness',s['lower_point_stiffness'],k)
                    check('inverse_mass',s['lower_point_inverse_mass'],invM)
                    check('native_frequency_identity',k*invM,gap*gap)
                key=(name,R,sg)
                if key not in sector_invariants:sector_invariants[key]=(w,r,I)
                for current,initial in zip((w,r,I),sector_invariants[key]):check('held_block_invariants',current,initial)
                Es.append(w*s['energy']);ns.append(w*s['incidence']);Xs.append(w*h*X)
            check('weighted_held_energy',math.fsum(Es),a['held_energy'])
            check('weighted_incidence',math.fsum(ns),old_age['link_occupation'])
            check('weighted_record_count',math.fsum(Rs),old_age['record_count'])
            check('weighted_source_moment',math.fsum(Xs),-old_age['energy_terms']['incidence_flip'])
            for tau in times:
                dr=dindex[name,age,tau]
                check('step_remainder_identity',dr['step_minus_quartic'],dr['exact_step_derivative']-a['step_quartic']*tau**4)
                check('impulse_remainder_identity',dr['impulse_minus_cubic'],dr['exact_impulse_derivative']-a['impulse_cubic']*tau**3)
                central=[]
                for amp in (.01,.005):
                    plus=pindex[name,age,tau,amp];minus=pindex[name,age,tau,-amp]
                    central.append((plus['carrier_change']-minus['carrier_change'])/(2*amp))
                for c0,c1 in zip(central,dr['central_derivatives']):check('saved_central',c0,c1)
                rich=(4*central[1]-central[0])/3
                check('saved_Richardson',dr['Richardson_derivative'],rich)
                if name!='native':
                    check('control_step_null',dr['exact_step_derivative'])
                    check('control_impulse_null',dr['exact_impulse_derivative'])
                for amp in amps:
                    pr=pindex[name,age,tau,amp]
                    check('finite_linear_prediction',pr['linear_prediction'],amp*dr['exact_step_derivative'])
                    check('finite_work',pr['held_energy_change'],pr['work_on']+pr['work_off'])
                    if lam==0:check('feedback_finite_null',pr['carrier_change'])
    synindex={(s['preparation_H'],s['constructed_sign']):s for s in p['constructed_witness']}
    for name in names:
        lam=oldcases[name]['parameters']['lambda_R'];t=oldcases[name]['parameters']['t_hop'];h=1.
        for sign in (-1,1):
            s=synindex[name,sign];zeta=sign*.5
            check('witness_correlation',s['correlation'],zeta)
            check('witness_energy',s['held_energy'],4+(2.25-lam)/2)
            check('witness_quartic',s['step_quartic'],lam*t*h*zeta/24)
            check('witness_cubic',s['impulse_cubic'],lam*t*h*zeta/6)
            for value in s['carrier_baselines']:check('witness_baseline',value,.5)
        for left,right in zip(synindex[name,-1]['linear_responses'],synindex[name,1]['linear_responses']):
            assert left[0]==right[0]
            check('witness_opposite_step',left[1],-right[1])
            check('witness_opposite_impulse',left[2],-right[2])
    assert (retained,null)==(70,20)
    actual=[r for r in p['ages'] if r['preparation']=='native']
    return dict(status='ACCEPTED_SAVED_ALGEBRA',script_sha256=sha(Path(__file__)),result_sha256=sha(file),
        freeze_sha256=sha(freeze),payload_sha256=d['payload_sha256'],frozen_members=len(f['files']),
        producer_checks=sum(p['check_counts'].values()),independent_checks=sum(counts.values()),
        maxima=maxima,retained_sectors=retained,null_sectors=null,native_age_rows=actual,
        native_step_range=[min(r['exact_step_derivative'] for r in p['delays'] if r['preparation']=='native'),
                           max(r['exact_step_derivative'] for r in p['delays'] if r['preparation']=='native')],
        native_impulse_range=[min(r['exact_impulse_derivative'] for r in p['delays'] if r['preparation']=='native'),
                              max(r['exact_impulse_derivative'] for r in p['delays'] if r['preparation']=='native')],
        maximum_finite_work_residual=max(abs(r['held_energy_change']-r['work_on']-r['work_off']) for r in p['pulses']),
        source_work_range=[min(r['held_energy_change'] for r in p['pulses']),max(r['held_energy_change'] for r in p['pulses'])],
        producer_seconds=p['seconds'],producer_self_RSS_bytes_on_Darwin=p['peak_self_rss_platform_units'],
        limits=['No propagation, Kubo quadrature or finite pulse rerun.',
            'At age zero the triple correlation and impulse work were independently contracted with the inherited full formed vector.',
            'Later aged correlations and dephased kernel nulls remain authenticated operator/producer evidence; conditional saved blocks do not reconstruct intersector coherence.',
            'The constructed witness is separate from actual native formation; grouping is record-pair/incidence/carrier.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
