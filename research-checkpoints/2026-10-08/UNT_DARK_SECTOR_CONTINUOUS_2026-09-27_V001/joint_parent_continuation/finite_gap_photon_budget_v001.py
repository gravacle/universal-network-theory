"""Same-state photon reference using saved finite-gap actions; stdout only."""
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import zlib

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE/'FINITE_GAP_PHOTON_BUDGET_V001_FROZEN.json'
CONFIG = dict(beta=.005, A=1101, tolerance=2e-11, expected_rows=360,
              approximation_epsilons=[.01,.001])

def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inputs():
    files, seen = {}, set()
    def add(p, expected=None):
        p=p.resolve(strict=True);p.relative_to(ROOT)
        h=sha(p)
        if expected is not None and h != expected:
            raise RuntimeError('Changed input: '+str(p))
        files[str(p.relative_to(ROOT))]=h
        return p
    def manifest(p):
        p=add(p)
        if p in seen:return
        seen.add(p)
        for name,h in json.loads(p.read_text())['files'].items():
            q=Path(name)
            candidates={v.resolve() for v in ([q] if q.is_absolute() else [ROOT/q,p.parent/q]) if v.is_file()}
            if len(candidates)!=1:raise RuntimeError('Ambiguous manifest member')
            q=add(candidates.pop(),h)
            if q.name.endswith('_FROZEN.json'):manifest(q)
    t=json.loads(add(HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json','11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4').read_text())
    raw=zlib.decompress(base64.b64decode(t['data'],validate=True))
    if hashlib.sha256(raw).hexdigest()!=t['raw_sha256'] or len(raw)!=t['raw_bytes']:
        raise RuntimeError('Old transport differs')
    old=json.loads(raw);p=old['payload'];f=HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json'
    manifest(f)
    if old['freeze_sha256']!=sha(f) or old['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():
        raise RuntimeError('Old wrapper differs')
    if p['status']!='COMPLETE' or p['failures'] or len(p['rows'])!=360:
        raise RuntimeError('Old qualification differs')
    global_path=add(HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json','11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628')
    calibration=json.loads(global_path.read_text())['payload']
    photons=json.loads(add(HERE/'RADIATION_PHOTON_REFERENCE_V001_RESULTS.json','45d4353256d15b87bf57df3f67a6b581a8f6d347fc42f8eb022f3c43713e7b41').read_text())
    if photons['status']!='COMPLETE':raise RuntimeError('Photon receipt incomplete')
    for name in ['SAME_ACTION_RADIATION_ASYMPTOTE_V001.md','RADIATION_PHOTON_REFERENCE_V001.md','RADIATION_PHOTON_REFERENCE_RESULT_REVIEW_V001.md','FINITE_GAP_PHOTON_BUDGET_PROTOCOL_V001.md',Path(__file__).name]:
        add(HERE/name)
    return p,calibration,photons,dict(configuration=CONFIG,files=files)

def run(old,calibration,photons):
    started=time.perf_counter();failures=[];counts={};maxima={};rows=[]
    def check(name,a,b,scale=None):
        den=max(abs(a),abs(b),1e-300) if scale is None else max(abs(scale),1e-300)
        err=abs(a-b)/den;counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),err)
        if not math.isfinite(err) or err>CONFIG['tolerance']:
            failures.append(dict(check=name,row=len(rows),error=err))
    C=((3*math.sqrt(math.pi)/2)*math.gamma(.75)/math.gamma(.25))**(4/3)
    beta_fn=math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)
    check('quartic_coefficient',C,(math.pi/beta_fn)**(4/3))
    refs={r['reference']:r for r in photons['references']}
    c=photons['constants'];u=8*math.pi**5*(c['k_B_J_K']*c['T_K'])**4/(15*c['h_P_J_s']**3*c['c_m_s']**3)
    check('photon_energy',u,photons['photon_energy_J_m3'])
    for n,ref in enumerate(calibration['references']):
        pr=refs[n]
        if pr['inherited_reference']!=ref:raise RuntimeError('Photon/calibration reference identity differs')
        omega=8*math.pi*c['G_SI']*u/(3*ref['H0_s_inverse']**2*c['c_m_s']**2)
        check('photon_omega',omega,pr['Omega_gamma'])
    A=CONFIG['A'];beta=CONFIG['beta']
    for index,r in enumerate(old['rows']):
        ref=calibration['references'][r['reference']];og=refs[r['reference']]['Omega_gamma']
        e0=C*r['I']**(4/3);Q=beta*e0;D=beta*r['R']**2*math.sqrt(e0)
        factor=ref['Omega_exc']/(r['E']*og)
        asympt=factor*Q;finite=factor*r['early_E']/A**4;upper=factor*D/A**2
        check('saved_action_at_A',r['early_I'],r['I']*A**3)
        check('saved_energy_ratio',r['early_E']/(r['E']*A**3),r['early_dust_ratio'])
        check('saved_pressure_ratio',beta*r['early_p']/r['early_E'],r['early_w'])
        check('quartic_lower_bound',min(finite-asympt,0.),0.,max(finite,asympt))
        check('quartic_upper_bound',max(finite-asympt-upper,0.),0.,max(finite,asympt+upper))
        check('present_quartic_floor',max(Q-r['E'],0.),0.,r['E'])
        rows.append(dict(source_row_index=index,spectrum_index=r['spectrum_index'],reference=r['reference'],R=r['R'],
            I=r['I'],E_present=r['E'],Omega_exc=ref['Omega_exc'],Omega_gamma=og,Q=Q,D=D,Q_over_E=Q/r['E'],
            asymptote_over_photons=asympt,at_A1101_over_photons=finite,upper_difference_bound_A1101=upper,
            w_at_A1101=r['early_w'],A_sufficient_for_fractional_quartic_error={str(e):math.sqrt(D/(e*Q)) for e in CONFIG['approximation_epsilons']}))
    expected={(s,r,R) for s in range(4) for r in range(18) for R in [32,128,512,2048,8192]}
    check('census',len(rows),CONFIG['expected_rows'])
    check('labels',int({(r['spectrum_index'],r['reference'],r['R']) for r in rows}==expected),1)
    summaries=[]
    for R in [32,128,512,2048,8192]:
        subset=[r for r in rows if r['R']==R]
        summaries.append(dict(R=R,rows=len(subset),ranges={key:[min(r[key] for r in subset),max(r[key] for r in subset)] for key in ['asymptote_over_photons','at_A1101_over_photons','upper_difference_bound_A1101','Q_over_E','w_at_A1101']}))
    return dict(status='FAILED_CONTROLS' if failures else 'COMPLETE',configuration=CONFIG,C=C,
        counts=counts,maxima=maxima,failures=failures,rows=rows,summaries=summaries,
        seconds=time.perf_counter()-started,peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        scope='Same-state conditional density coefficient relative to ordinary photons; not a CMB, BBN, neutrino, thermal-origin or observational acceptance test.')

def main():
    old,calibration,photons,snapshot=inputs()
    if sys.argv[1:]==['freeze']:
        print(encode(snapshot).decode());return 0
    if sys.argv[1:]!=['run']:raise RuntimeError('Use freeze or run')
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Prospective freeze differs')
    p=run(old,calibration,photons)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
    return 0 if not p['failures'] else 2

if __name__=='__main__':sys.exit(main())
