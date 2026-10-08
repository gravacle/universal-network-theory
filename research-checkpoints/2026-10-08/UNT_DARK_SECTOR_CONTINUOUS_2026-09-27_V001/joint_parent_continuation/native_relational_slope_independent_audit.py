"""Saved-state derivative audit in the energy basis; no new impulse or age."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
OUTPUT=ROOT/'NATIVE_RELATIONAL_SLOPE_INDEPENDENT_REVIEW_DATA.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def main():
    assert not OUTPUT.exists()
    files={}
    def load(resultname,freezename):
        rp,fp=ROOT/resultname,ROOT/freezename
        r,f=json.loads(rp.read_text()),json.loads(fp.read_text())
        assert r['status']=='COMPLETE' and all(c['passed']for c in r['payload']['checks'])
        assert r['freeze_sha256']==sha(fp)
        assert r['payload_sha256']==hashlib.sha256(encoded(r['payload'])).hexdigest()
        for name,digest in f['files'].items():
            p=WORKSPACE/name
            assert sha(p)==digest,name
            files[str(p)]=digest
        files[str(rp)]=sha(rp);files[str(fp)]=sha(fp)
        return r
    result=load('native_relational_slope_v001_results.json','native_relational_slope_v001_frozen.json')
    old=load('RECORD_ADDITION_RESULTS.json','RECORD_ADDITION_FROZEN.json')
    clock=load('native_phase_clock_v001_results.json','native_phase_clock_v001_frozen.json')
    checks=[];rows=[]
    def check(label,a,b):
        err=float(np.max(abs(np.asarray(a)-np.asarray(b))))
        assert err<=1e-11,(label,err)
        checks.append({'name':label,'residual':err})
    def cx(x):return complex(x['real'],x['imag'])
    id2=np.eye(2);eye=np.eye(16)
    def embed(mat,pos):
        a=np.ones((1,1),complex)
        for i in range(4):a=np.kron(a,mat if i==pos else id2)
        return a
    n2=np.diag([0.,1.]);x2=np.array([[0.,1.],[1.,0.]])
    a2=np.array([[0.,0.],[1.,0.]])
    n=embed(n2,2);x=embed(x2,2);xc=embed(x2,3)
    rcount=embed(n2,0)+embed(n2,1);a=embed(a2,0)+embed(a2,1)
    assert [c['name']for c in result['payload']['cases']]==['native','feedback_off','copying_off']
    for case,original,cl in zip(result['payload']['cases'],old['payload']['cases'],clock['payload']['cases']):
        assert case['name']==original['name']==cl['name']
        lam=case['parameters']['lambda_R'];name=case['name']
        h=3*eye+rcount-x+(2.25*eye-lam*rcount-.5*xc)@n
        e,v=np.linalg.eigh(h);freq=e[:,None]-e[None,:]
        ne=v.conj().T@n@v;ae=v.conj().T@a@v;xe=v.conj().T@x@v
        xae=v.conj().T@x@a@v
        psi=np.asarray(original['formed_vector']['real'])+1j*np.asarray(original['formed_vector']['imag'])
        psi_e=v.conj().T@psi
        assert [z['age']for z in case['rows']]==[0,.25,.5,1,2]
        for row,prior,clockrow in zip(case['rows'],original['hold'],cl['ages']):
            age=row['age'];state=psi_e*np.exp(-1j*e*age)
            def ex(op):return np.vdot(state,op@state)
            def kernel_derivative(op,order):
                od=(1j*freq)**order*op
                return 1j*ex(od@ne-ne@od)
            aa=ex(ae);ad=ex(1j*freq*ae);xa=ex(xae)
            drift=ex(1j*freq*ne)
            first=kernel_derivative(ne,1);second=kernel_derivative(ne,2)
            a0=kernel_derivative(ae,0);a1=kernel_derivative(ae,1);a2d=kernel_derivative(ae,2)
            check(name+':A0_kernel',a0,0.);check(name+':A1_kernel',a1,0.)
            for field,value in [('incidence',ex(ne)),('X',ex(xe)),('incidence_drift',drift),
                                ('laboratory_initial_slope',first),('incidence_second_delay_derivative',second)]:
                check(name+':'+field,value,row[field])
            check(name+':XA',xa,cx(row['XA']))
            check(name+':A_second',a2d,cx(row['A_second_delay_derivative']))
            check(name+':saved_flip',first,-prior['energy_terms']['incidence_flip'])
            check(name+':saved_clock_A',aa,cx(clockrow['A']))
            item={'name':name,'age':age,'laboratory_slope':float(first.real)}
            if name=='copying_off':
                for field in ('phase_rate','equal_phase_initial_slope','XA_over_A','phase_shift_tau2_per_impulse',
                              'readout_time_shift_tau2_per_impulse','incidence_timing_correction_tau2_per_impulse'):
                    assert row[field]is None
                check(name+':blank',aa,0.)
                item['equal_phase_slope']=None
            else:
                nu=float((ad/aa).imag)
                phase_shift=float((a2d/aa).imag/2)
                time_shift=-phase_shift/nu
                correction=float(drift.real*time_shift)
                for field,value in [('phase_rate',nu),('equal_phase_initial_slope',first.real/nu),
                    ('phase_shift_tau2_per_impulse',phase_shift),('readout_time_shift_tau2_per_impulse',time_shift),
                    ('incidence_timing_correction_tau2_per_impulse',correction)]:
                    check(name+':'+field,value,row[field])
                check(name+':XA_over_A',xa/aa,cx(row['XA_over_A']))
                item.update(equal_phase_slope=float(first.real/nu),phase_shift=phase_shift,
                            incidence_timing_correction=correction)
            rows.append(item)
        for key,summary in [('laboratory_initial_slope',case['laboratory_summary']),
                            ('equal_phase_initial_slope',case['phase_summary'])]:
            values=[z[key]for z in case['rows']if z[key]is not None]
            assert summary['defined_rows']==len(values)
            if values:
                check(name+':summary_min',min(values),summary['minimum'])
                check(name+':summary_max',max(values),summary['maximum'])
                check(name+':summary_spread',max(values)-min(values),summary['spread'])
                assert summary['all_positive']==(min(values)>1e-11)
                assert summary['constant_compatible']==(max(values)-min(values)<=2e-11)
    assert len(rows)==15
    output={'status':'INDEPENDENT_CHECKS_PASS','role':'Saved-state energy-basis derivative audit; no new pulse or preparation.',
            'script_sha256':sha(Path(__file__)),'input_sha256':files,'rows':rows,'checks':checks,
            'max_absolute_residual':max(c['residual']for c in checks)}
    with OUTPUT.open('x')as stream:
        json.dump(output,stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')
    print(json.dumps({'status':output['status'],'checks':len(checks),'rows':len(rows),
                      'max_absolute_residual':output['max_absolute_residual']},indent=2))

if __name__=='__main__':main()
