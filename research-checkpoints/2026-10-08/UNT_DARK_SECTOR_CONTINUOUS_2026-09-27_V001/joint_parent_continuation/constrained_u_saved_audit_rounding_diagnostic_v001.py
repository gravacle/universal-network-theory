"""Root-owned SAVED-only rounding diagnostic; no producer or equation imports."""
from pathlib import Path
import argparse, hashlib, json, math, sys

BASE=Path(__file__).resolve().parent
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
STEM='CONSTRAINED_U_SAVED_AUDIT_ROUNDING_DIAGNOSTIC_V001'
PINS={
 PARENT+'_RESULT.json':'0fbbf7a2dc89231da78f31b76e3325bb62e502adfb34ff916c03e81bb5c653f3',
 'constrained_u_clock_gradient_flrw_saved_audit_v001.py':'ea9f88e8b5b971c41bc9888b2b726966359c26b0e169d49f3495c87c3740cd1a',
 PARENT+'_SAVED_AUDIT_V001_ERROR.json':'4707e7e220687bbeb4fcfadebb9886a3e3195d476c39431b1a13d5d0201fb6e9',
}
KB,CBAR,EPS=.02,.99,sys.float_info.epsilon

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    for n,h in PINS.items():
        if sha(BASE/n)!=h:raise ValueError('Changed saved input '+n)
    raw=json.loads((BASE/(PARENT+'_RESULT.json')).read_text())
    fixed=raw['manifest']['fixed'];bad=[];largest=None;count=0
    for trial in raw['trials']:
        ns=trial['ns'];weights=trial['weights']
        for snap in trial['snapshots']:
            row=snap['background'];a,S=row['a'],row['s'];ep=fixed['eps']
            norm=1/ep-math.log1p(1/ep);qb=math.sqrt(1+ep*S/(1+S));charge=fixed['d0']/a**3
            b=1.5*fixed['OB']/fixed['rG']/a**3;r=1.5*fixed['OR']/fixed['rG']/a**4
            rho=1.5*fixed['OA']/fixed['rG']*(1+qb*charge-(math.log1p(S)-S/(1+S))/norm)
            h=math.sqrt(2*(b+r+rho)/3);c=ep*S/(2+(4+3*ep)*S+2*(1+ep)*S*S)
            Q=fixed['Q0_over_Hstar']*qb
            for ci,(k,omega) in enumerate(raw['manifest']['cases']):
                q=k*299792.458/fixed['Hunit']/a;L=Q*q;Ld=-h*(1+3*c)*L
                for seed,state in enumerate(snap['state'][ci]):
                    count+=1;V,pi,d,P=state[7],state[5],state[6],state[8]
                    z=state[9:9+ns];zd=state[9+ns:]
                    Z=math.fsum(w*x for w,x in zip(weights,z));Zd=math.fsum(w*x for w,x in zip(weights,zd))
                    Zabs=math.fsum(abs(w*x) for w,x in zip(weights,z));Zdabs=math.fsum(abs(w*x) for w,x in zip(weights,zd))
                    n=(P-CBAR*Z)/(.5*KB*q);v=V-pi;Gamma=d+3*h*V;vd=n+c*Gamma
                    jt=[Zd,-Ld*v,-L*vd];floor=L*1e-8*1e-10*max(h,Q,100.)
                    den=max(math.fsum(abs(t) for t in jt),floor);fresh=abs(math.fsum(jt))/den
                    stored=snap['first_jet_error'][ci][seed];stored_jt=snap['first_jet_terms'][ci][seed]
                    stored_floor=snap['first_jet_floor'][ci][0];stored_den=max(math.fsum(abs(t) for t in stored_jt),stored_floor)
                    oldscale=(Zdabs+math.fsum(abs(t) for t in jt))/den
                    Nenv=(abs(P)+CBAR*Zabs)/(.5*KB*abs(q));Genv=abs(d)+3*abs(h*V)
                    Venv=abs(V)+abs(pi);VDenv=Nenv+abs(c)*Genv
                    Jenv=Zdabs+abs(Ld)*Venv+abs(L)*VDenv
                    mind=min(den,stored_den);ratio_scale=(1+max(fresh,stored))*Jenv/mind+max(fresh,stored)*max(floor,stored_floor)/mind
                    err=abs(stored-fresh);base=2e-18+2e-11*abs(fresh)
                    record=dict(arm=trial['label'],step=snap['n'],case=ci,seed=seed,
                        stored=stored,fresh=fresh,error=err,old_bound=base+4096*EPS*oldscale,
                        corrected_bound=base+4096*EPS*ratio_scale,
                        stored_terms=stored_jt,fresh_terms=jt,stored_denominator=stored_den,
                        fresh_denominator=den,stored_floor=stored_floor,fresh_floor=floor,
                        h_saved=row['h'],h_fresh=h,V=V,pi=pi,d=d,P=P,Z=Z,Zd=Zd,n=n,
                        Gamma=Gamma,vd=vd,L=L,Ld=Ld,Nenv=Nenv,Genv=Genv,Venv=Venv,
                        VDenv=VDenv,Jenv=Jenv,ratio_scale=ratio_scale)
                    if largest is None or err/max(record['old_bound'],1e-300)>largest['error']/max(largest['old_bound'],1e-300):largest=record
                    if err>record['old_bound']:bad.append(record)
    if count!=3120:raise ValueError('Complete snapshot/channel census')
    result=dict(status='SAVED_ROUNDING_DIAGNOSTIC',rows=count,old_bound_failures=len(bad),
        first=bad[0] if bad else None,largest=largest,all_corrected_bounds_pass=all(r['error']<=r['corrected_bound'] for r in bad),
        source_sha256=sha(Path(__file__)),inputs=PINS,
        scope='Saved operands only. This diagnoses the audit comparison and changes no parent scientific gate, trajectory or status.')
    for n,h in PINS.items():
        if sha(BASE/n)!=h:raise ValueError('Changed saved input '+n)
    path=BASE/(STEM+'_RESULT.json')
    with path.open('x') as f:json.dump(result,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
    path.chmod(0o444)
    print(json.dumps(dict(rows=count,old_bound_failures=len(bad),all_corrected_bounds_pass=result['all_corrected_bounds_pass'],result_sha256=sha(path))))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:ap.error('Root-owned --execute required')
    if (BASE/(STEM+'_RESULT.json')).exists():raise SystemExit('Existing diagnostic preserved')
    main()
