"""Read-only saved-array FIRAS audit; no producer, optimizer or history run."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import hashlib
import io
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
RESULT='FIRAS_SOURCE_SCREEN_V001.json'
FROZEN='FIRAS_SOURCE_SCREEN_V001_FROZEN.json'
PINS={RESULT:'51ff63572314134612877be2a89f157fab6b1841861b80f6a6d81dd5e67471e9',
      FROZEN:'40612c7202e74d400efb1be0cd28b022d037ad1d4dcd4d4d23afeb97958f10eb'}
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def read(p):
    p=Path(p);p.relative_to(ROOT)
    if p.resolve()!=p or p.is_symlink():raise RuntimeError('Noncanonical input')
    return p.read_bytes()

def main():
    if Path.cwd().resolve()!=ROOT:raise RuntimeError('Wrong workspace')
    failures=[];count=0;maxima={}
    def ck(name,ok):
        nonlocal count
        count+=1
        if not ok:failures.append(name)
    def close(name,x,y,atol=2e-12,rtol=2e-9):
        x,y=np.asarray(x,float),np.asarray(y,float)
        er=float(np.max(np.abs(x-y)/(atol+rtol*np.maximum(np.abs(x),np.abs(y)))))
        maxima[name]=er;ck(name,math.isfinite(er) and er<=1)
    for name,digest in PINS.items():ck('raw '+name,sha(read(J/name))==digest)
    f=json.loads(read(J/FROZEN));w=json.loads(read(J/RESULT));p=w['payload']
    ck('freeze reference',w['freeze_sha256']==PINS[FROZEN])
    ck('payload hash',sha(canonical(p))==w['payload_sha256'])
    ck('input digest',sha(canonical(f['inputs']))==f['inputs_sha256'])
    for v in f['inputs']:
        b=read(v['path']);ck('frozen '+v['path'],sha(b)==v['sha256'] and len(b)==v['bytes'])
    ck('config',p['config']==f['config'])
    ck('complete',p['status']=='COMPLETE' and p['failed_checks']==[])
    ck('original checks',len(p['checks'])==p['check_count']==508 and all(x['passed'] and x['error']<=x['tolerance'] for x in p['checks']))
    rawtable=np.loadtxt(io.BytesIO(read(J/'firas_inputs_v001/firas_monopole_spec_v1.txt')))
    d=np.array(p['raw_table']);ck('raw table',np.array_equal(rawtable,d) and d.shape==(43,5))
    metadata=json.loads(read(J/'firas_inputs_v001/FIRAS_COVARIANCE_SOURCE_V001.json'))
    ck('metadata',metadata==p['primary_metadata'] and p['Q']==metadata['Q'])
    q=np.array(p['Q']);C=d[:,3,None]*d[None,:,3]*q[np.abs(np.arange(43)[:,None]-np.arange(43))]
    close('covariance',C,p['covariance_kJy2_sr2'],atol=2e-12,rtol=2e-12)
    W=np.linalg.inv(C) # Independent covariance inverse, not producer Cholesky/fit.
    close('inverse identity',C@W,np.eye(43),atol=2e-12,rtol=2e-12)
    y=d[:,2];cfg=p['config'];nu=d[:,0]*100*cfg['c_SI']
    pref=2*cfg['h_SI']*nu**3/(cfg['c_SI']**2*1000*cfg['Jy_SI'])
    def planck(T):
        x=cfg['h_SI']*nu/(cfg['kB_SI']*T)
        B=pref/np.expm1(x)
        # Independent derivative from B*x/(T*(1-exp(-x))).
        return x,B,B*x/(T*(-np.expm1(-x)))
    def nuisance(T,fg):
        _,_,temp=planck(T);_,bd,db=planck(9.)
        factor=1000/np.max(nu**2*bd)
        cols=[temp,d[:,4] if fg=='published_pole_template' else factor*nu**2*bd]
        if fg=='dust9_amplitude_temperature_tangent':cols.append(factor*nu**2*db)
        return np.column_stack(cols)
    def saved_fit_check(label,A,beta,cov,model,resid,chi):
        beta,cov,model,resid=map(np.asarray,(beta,cov,model,resid))
        close(label+' model',A@beta,model)
        close(label+' residual',y-model,resid)
        close(label+' chi',resid@W@resid,chi)
        norms=np.sqrt(np.diag(A.T@W@A));Z=A/norms
        close(label+' normal equations',Z.T@W@resid,np.zeros(A.shape[1]),atol=2e-9,rtol=0)
        cov_scaled=cov*norms[:,None]*norms[None,:]
        close(label+' covariance inverse',(Z.T@W@Z)@cov_scaled,np.eye(A.shape[1]),atol=2e-9,rtol=2e-9)
    ck('baseline census',len(p['baselines'])==6)
    ck('source census',len(p['source_rows'])==90)
    baselines={}
    for i,b in enumerate(p['baselines']):
        key=(b['T_K'],b['foreground']);ck('unique baseline'+str(i),key not in baselines);baselines[key]=b
        A=nuisance(*key)
        ck('baseline nominal DOF'+str(i),b['nominal_design_degrees_of_freedom']==43-A.shape[1])
        saved_fit_check('baseline'+str(i),A,b['nuisance_coefficients'],b['covariance'],b['model_kJy_sr'],b['residual_kJy_sr'],b['chi2'])
    summaries=[];seen=set();degenerate=0
    for i,r in enumerate(p['source_rows']):
        key=(r['T_K'],r['foreground'],r['family'],r['r']);ck('unique source'+str(i),key not in seen);seen.add(key)
        T,fg,family,ratio=key;A=nuisance(T,fg);x,B,dB=planck(T);G=T*dB
        if family=='mu':s=-G/x
        elif family=='y':s=G*(x/np.tanh(x/2)-4)
        elif family=='inverse_Planck_tangent':s=G
        else:
            Br=planck(ratio*T)[1];s=Br-B if family=='grey_exchange' else Br
        close('template'+str(i),s,r['template_kJy_sr'])
        sw=np.array(r['template_kJy_sr']);gram=A.T@W@A
        perp=sw-A@np.linalg.solve(gram,A.T@W@sw)
        total=float(sw@W@sw);perpnorm=float(perp@W@perp)
        relative=math.sqrt(max(0.,perpnorm/total)) if total else 0.
        close('template perpendicular'+str(i),relative,r['residualized_template_relative_norm'],atol=2e-12)
        expectednull=family=='inverse_Planck_tangent' or (family=='grey_exchange' and ratio==1)
        ck('exact degenerate scope'+str(i),(r['amplitude'] is None)==expectednull)
        b=baselines[(T,fg)];close('nullchi'+str(i),r['chi2_null'],b['chi2'])
        if expectednull:
            degenerate+=1
            ck('null values'+str(i),r['sigma'] is None and r['nominal_nonnegative_profile_band'] is None and relative<=2e-12)
            summaries.append({'T':T,'foreground':fg,'family':family,'r':ratio,'identifiable':False})
            continue
        full=np.column_stack([A,sw]);beta=r['nuisance_coefficients']+[r['amplitude']]
        saved_fit_check('row'+str(i),full,beta,r['coefficient_covariance'],r['model_kJy_sr'],r['residual_kJy_sr'],r['chi2'])
        hat,sig=r['amplitude'],r['sigma'];close('sigma'+str(i),sig*sig,r['coefficient_covariance'][-1][-1],atol=1e-30)
        close('profile curvature'+str(i),1/(sig*sig),perpnorm)
        close('improvement'+str(i),r['delta_chi2_from_null'],b['chi2']-r['chi2'])
        close('profile improvement'+str(i),r['delta_chi2_from_null'],(hat/sig)**2)
        rootdelta=math.sqrt(cfg['nominal_profile_delta_chi2'])
        close('signed band'+str(i),r['nominal_signed_band'],[hat-rootdelta*sig,hat+rootdelta*sig],atol=1e-20)
        ck('source nominal DOF'+str(i),r['nominal_design_degrees_of_freedom']==43-full.shape[1])
        summary={'T':T,'foreground':fg,'family':family,'r':ratio,'identifiable':True,'amplitude':hat,'sigma':sig,'signal_to_sigma':hat/sig,'chi2':r['chi2'],'delta_chi2':r['delta_chi2_from_null']}
        if ratio is not None:
            rad=math.hypot(max(-hat,0),rootdelta*sig);band=[max(0,hat-rad),max(0,hat+rad)]
            close('nonnegative band'+str(i),r['nominal_nonnegative_profile_band'],band,atol=1e-20)
            close('nonnegative optimum'+str(i),r['nonnegative_optimum'],max(0,hat),atol=1e-20)
            # Test profile at the positive upper endpoint against constrained min.
            close('upper profile delta'+str(i),((band[1]-hat)/sig)**2-(max(-hat,0)/sig)**2,cfg['nominal_profile_delta_chi2'])
            ef=ratio**4-(1 if family=='grey_exchange' else 0);nf=ratio**3-(1 if family=='grey_exchange' else 0)
            close('energy'+str(i),r['signed_energy_change_relative_initial_at_upper'],band[1]*ef,atol=1e-20)
            close('number'+str(i),r['signed_number_change_relative_initial_at_upper'],band[1]*nf,atol=1e-20)
            close('channel fractional'+str(i),r['max_fractional_channel_change_at_upper'],np.max(np.abs(band[1]*sw/B)))
            mix=[band[0],min(1.,band[1])] if family=='grey_exchange' and band[0]<=1 else None
            if mix is None:ck('mixture intersection'+str(i),r['grey_fixed_bath_mixture_fraction_band'] is None)
            else:close('mixture intersection'+str(i),r['grey_fixed_bath_mixture_fraction_band'],mix,atol=1e-20)
            dt=r['nuisance_coefficients'][0]
            correction=planck(T+dt)[1]-B-dt*dB
            close('temperature nonlinear'+str(i),r['temperature_second_order_whitened_norm'],math.sqrt(correction@W@correction),atol=2e-10)
            summary.update(upper=band[1],lower=band[0],energy_at_upper=band[1]*ef,number_at_upper=band[1]*nf)
        summaries.append(summary)
    ck('twelve nulls',degenerate==12)
    ck('all six groups',set(baselines)=={(T,fg) for T in cfg['temperatures_K'] for fg in cfg['foregrounds']})
    ck('constructed col2 not fit',p['column2_used_in_likelihood'] is False)
    groups=[]
    for fam in ('grey_exchange','pure_emission'):
        for r in cfg['ratios']:
            rows=[x for x in summaries if x['family']==fam and x['r']==r and x['identifiable']]
            groups.append({'family':fam,'r':r,'rows':len(rows),'upper_range':None if not rows else [min(x['upper'] for x in rows),max(x['upper'] for x in rows)],'energy_at_upper_range':None if not rows else [min(x['energy_at_upper'] for x in rows),max(x['energy_at_upper'] for x in rows)]})
    o={'schema':'FIRAS_SOURCE_SAVED_AUDIT_V001','status':'PASS' if not failures else 'FAIL','source_sha256':sha(read(Path(__file__).resolve())),
       'input_hashes':PINS,'payload_sha256':w['payload_sha256'],'frozen_members':len(f['inputs']),
       'checks':count,'failures':failures,'maximum_tolerance_fraction':max(maxima.values()),'residual_checks':maxima,
       'baselines':[{'T':r['T_K'],'foreground':r['foreground'],'chi2':r['chi2']} for r in p['baselines']],
       'source_rows':summaries,'six_choice_strength_ranges':groups,
       'max_abs_signal_to_sigma':max(abs(x['signal_to_sigma']) for x in summaries if x['identifiable']),
       'scope':'Saved covariance inverse/model/residual/interval audit, no optimizer or ancestral producer. Conditional residual-space GLS, not full FIRAS systematics or cosmological history.'}
    print(json.dumps(o,sort_keys=True,indent=2,allow_nan=False))
    return 0 if not failures else 1

if __name__=='__main__':raise SystemExit(main())
