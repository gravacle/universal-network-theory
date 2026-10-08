"""Read-only saved profile/monodromy identities; no ODE or quadrature."""
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    file=HERE/'VECTOR_ORBIT_KERNEL_V001_RESULTS.json'
    freeze=HERE/'VECTOR_ORBIT_KERNEL_V001_FROZEN.json'
    d=json.loads(file.read_text());p=d['payload'];f=json.loads(freeze.read_text())
    assert d['status']=='COMPLETE' and d['freeze_sha256']==sha(freeze)
    assert d['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    for name,h in f['files'].items():
        assert sha(HERE/name)==h,name
    assert len(p['checks'])==277 and all(c['passed'] for c in p['checks'])
    assert all(math.isfinite(c['normalized_error']) and c['normalized_error']<=c['tolerance'] for c in p['checks'])
    assert [c['r'] for c in p['cases']]==[0.,1e-4,.01,1.,100.]
    maxima={};counts={}
    def check(name,a,b=0.,scale=1.,tol=2e-11):
        err=abs(a-b)/scale
        assert math.isfinite(err) and err<=tol,(name,err)
        maxima[name]=max(maxima.get(name,0.),err);counts[name]=counts.get(name,0)+1
    def L(q):
        return math.asin(math.sqrt(q))/math.sqrt(q*(1-q)) if q else 1.
    summaries=[]
    for c in p['cases']:
        u=c['r'];K=1+u;eta=u/(2*K);energy=.5+u/4
        check('eta',c['eta'],eta);check('energy',c['energy'],energy)
        q64,q128=c['quadratures'];assert [q64['order'],q128['order']]==[64,128]
        for key in ('period','chi_parallel','chi_perp'):
            check('angle_order_'+key,q64[key],q128[key],scale=max(1.,abs(q128[key])))
        check('isotropic_trace',c['chi_iso_conditional'],(q128['chi_parallel']+2*q128['chi_perp'])/3)
        check('isotropic_deficit',c['mu_iso'],1-c['chi_iso_conditional'])
        check('scalar_deficit',c['mu_parallel'],1-q128['chi_parallel'])
        low=L(eta)/K;upper=4*K/(2+u)**2
        check('lower_bound',c['pointwise_bounds']['lower'],low)
        check('upper_bound',c['pointwise_bounds']['upper'],upper)
        check('L_tail',c['series_tail_bounds']['L'],eta**65/(1-eta))
        check('Lprime_tail',c['series_tail_bounds']['L_prime'],eta**64*(65-64*eta)/(1-eta)**2)
        assert max(c['series_tail_bounds'].values())<=2e-12
        for y,xi,dy in zip(c['exact_profile_y'],c['exact_xi'],c['exact_dxi_dy']):
            q=eta*(1-y*y);l=L(q);R=l/K
            check('first_order_exact_profile',y*dy-xi,-R)
            lp=(1-(1-2*q)*l)/(2*q*(1-q)) if q else 2/3
            dyy=2*eta*lp/K
            residual=dyy*(2*energy-y*y-u*y**4/2)+dy*(-y-u*y**3)+(1+u*y*y)*xi
            check('second_order_exact_profile',residual,1.)
            assert low-2e-11<=xi<=upper+2e-11
        if u:
            assert 0<q128['chi_parallel']<q128['chi_perp']<1
            assert 0<c['mu_iso']<c['mu_parallel']
            for key,value in (('parallel',(1-q128['chi_parallel'])/u),
                              ('transverse',(1-q128['chi_perp'])/u),
                              ('isotropic',c['mu_iso']/u)):
                check('small_r_coefficient',c['small_r_deficit_coefficients'][key],value)
        else:
            check('harmonic_period',q128['period'],2*math.pi)
            check('harmonic_chi',q128['chi_perp'],1.)
        assert [s['steps_per_half'] for s in c['independent_shooting']]==[1024,2048]
        for s in c['independent_shooting']:
            M=s['monodromy'];det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
            detforce=(1-M[0][0])*(1-M[1][1])-M[0][1]*M[1][0]
            check('monodromy_trace',M[0][0]+M[1][1],-2.,tol=2e-7)
            check('monodromy_det',det,1.,tol=2e-7)
            check('forced_det',detforce,4.,tol=2e-7)
            check('saved_forced_det',s['determinant_I_minus_M'],detforce)
            check('dt',s['dt'],q128['period']/(2*s['steps_per_half']))
            check('mean_half',s['mean_half'],q128['chi_perp'],tol=2e-7)
            check('mean_full',s['mean_full'],q128['chi_perp'],tol=2e-7)
            check('mean_angular',s['full_period_mean_induced_angular_momentum'],scale=max(1.,math.sqrt(K)),tol=2e-7)
            assert s['profile_time_over_T']==[j/8 for j in range(9)]
            y,v,xi,xd=s['profile_y'],s['profile_velocity'],s['profile_xi'],s['profile_xidot']
            assert all(len(a)==9 for a in (y,v,xi,xd))
            for j in range(9):
                check('shoot_profile_energy',v[j]**2/2+y[j]**2/2+u*y[j]**4/4,energy,
                      scale=max(1.,energy),tol=2e-7)
            for j in range(5):
                check('shoot_antiperiodic_y',y[j+4],-y[j],tol=2e-7)
                check('shoot_periodic_xi',xi[j+4],xi[j],tol=2e-7)
                angular=y[j]*xd[j]-v[j]*xi[j]
                angular2=y[j+4]*xd[j+4]-v[j+4]*xi[j+4]
                check('shoot_antiperiodic_angular',angular2,-angular,scale=max(1.,math.sqrt(K)),tol=2e-7)
            check('shoot_initial_xi',xi[0],s['initial_forced_data'][0])
            check('shoot_initial_velocity',xd[0],s['initial_forced_data'][1])
        summaries.append(dict(r=u,chi_parallel=q128['chi_parallel'],chi_perp=q128['chi_perp'],
            chi_iso=c['chi_iso_conditional'],mu_iso=c['mu_iso'],mu_scalar=c['mu_parallel'],
            isotropic_to_scalar_deficit=c['mu_iso']/c['mu_parallel'] if u else None,
            coarse_mean_error=abs(c['independent_shooting'][0]['mean_full']-q128['chi_perp']),
            fine_mean_error=abs(c['independent_shooting'][1]['mean_full']-q128['chi_perp'])))
    return dict(status='ACCEPTED_SAVED_IDENTITY_AUDIT',script_sha256=sha(Path(__file__)),
        result_sha256=sha(file),freeze_sha256=sha(freeze),payload_sha256=d['payload_sha256'],
        frozen_files=len(f['files']),producer_checks=len(p['checks']),case_count=5,shooting_count=10,
        independent_checks=sum(counts.values()),maximum_errors=maxima,summary=summaries,
        producer_max_ODE_check=max(c['normalized_error'] for c in p['checks'] if c['tolerance']==2e-7),
        producer_seconds=p['seconds'],producer_peak_self_RSS_bytes=p['peak_rss_bytes'],
        scope=['Source/protocol full review completed after outcomes were reported, not claimed as an independent pre-run review.',
               'No ODE or quadrature rerun. Saved exact profiles checked with independent arcsine identities.',
               'Only nine shooting witnesses are stored; full-mesh controls remain authenticated producer evidence.',
               'Fixed selected half-periodic response and conditional isotropic second moment, not arbitrary switch-on or permanent isotropy.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
