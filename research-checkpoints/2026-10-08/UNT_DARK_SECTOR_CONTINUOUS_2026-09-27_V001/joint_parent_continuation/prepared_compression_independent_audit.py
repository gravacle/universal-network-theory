"""Independent midpoint/complex-step action curvature, all saved modes."""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'PREPARED_COMPRESSION_INDEPENDENT_REVIEW_DATA.json'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def encode(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def main():
    assert not OUTPUT.exists()
    files={}
    def load(stem):
        rp,fp=ROOT/(stem+'_RESULTS.json'),ROOT/(stem+'_FROZEN.json')
        result,frozen=json.loads(rp.read_text()),json.loads(fp.read_text())
        assert result['freeze_sha256']==sha(fp)
        assert result['payload_sha256']==hashlib.sha256(encode(result['payload'])).hexdigest()
        assert all(result['payload']['checks'].values())
        for name,digest in frozen['files'].items():
            path=fp.parent/name
            assert sha(path)==digest,name
            files[str(path)]=digest
        files[str(rp)]=sha(rp);files[str(fp)]=sha(fp)
        return result['payload']
    current=load('PREPARED_COMPRESSION_V001')
    returned=load('PREPARED_ACTION_RETURN_V001')
    states=load('COMMON_HISTORY_MECHANISM_V001')
    def key(c):return c['gap'],c.get('mode_order',c.get('order')),c['dt'],c['duration']
    old={(key(c),c['g']):c for c in returned['rows']}
    cases={key(c):c for c in states['cases']}
    rows=[]
    for row in current['rows']:
        original=old[(key(row),row['g'])];case=cases[key(row)]
        delta=np.asarray(case['delta']);weights=np.asarray(case['weights'])
        md=original['mode_data'];b=np.asarray(md['zero_source_turning_amplitude'])
        action=np.asarray(md['action']);pressure=np.asarray(md['zero_source_pressure'])
        saved=np.asarray(row['quadratures'][-1]['energy_curvature'])
        answers=[]
        for count in (512,1024):
            theta=(np.arange(count)+.5)*math.pi/(2*count)
            sine=np.sin(theta)**2;cosine=np.cos(theta)**2
            def integral(bb):
                q=delta[:,None]**2+bb[:,None]**2*(1+sine)/2
                # Midpoint interval length cancels directly into these prefactors.
                period=2*math.pi*np.mean(q**-.5,axis=1)
                omega=2*math.pi/period
                ii=bb*bb*np.mean(cosine*np.sqrt(q),axis=1)
                return ii,omega
            ii,omega=integral(b)
            derivatives=[]
            for eps in (1e-20,1e-25):
                ic,wc=integral(b.astype(complex)*(1+1j*eps))
                # e_II=(d omega/db)/(d I/db); complex-step avoids subtraction,
                # and does not reuse the production K-integral curvature formula.
                derivatives.append(wc.imag/ic.imag)
            curvature=derivatives[-1]
            modal=action*curvature/omega
            enthalpy=float(weights@(action*omega))
            bulk=float(weights@(action*action*curvature))
            cad=bulk/enthalpy
            ratio=(b/delta)**2
            lo=ratio*(ratio+1)/((ratio+2)*(3*ratio+2))
            hi=ratio*(ratio+2)/((ratio+1)*(3*ratio+4))
            error={
                'returned_action_relative':float(max(abs(ii/action-1))),
                'period_relative':float(max(abs(2*math.pi/omega/np.asarray(md['zero_source_period'])-1))),
                'curvature_relative':float(max(abs(curvature/saved-1))),
                'complex_step_refinement':float(max(abs(derivatives[0]/derivatives[1]-1))),
                'modal_coefficient_absolute':float(max(abs(modal-np.asarray(row['quadratures'][-1]['modal_c_ad_squared'])))),
                'enthalpy_relative':abs(enthalpy/row['quadratures'][-1]['enthalpy']-1),
                'bulk_relative':abs(bulk/row['quadratures'][-1]['bulk_response']-1),
                'mixture_coefficient_absolute':abs(cad-row['c_ad_squared'])}
            assert max(error.values())<2e-8
            assert np.all(curvature>0)
            assert np.all(modal>=lo-2e-8) and np.all(modal<=hi+2e-8)
            assert np.all(action*action*curvature<=2*pressure+2e-8*np.asarray(md['zero_source_energy']))
            pressure_bound=2*original['return_w']/(1+original['return_w'])
            assert 0<cad<1/3 and cad<=pressure_bound+2e-8
            answers.append({'midpoint_nodes':count,'complex_steps':[1e-20,1e-25],
                'energy_curvature':curvature.tolist(),'modal_coefficient':modal.tolist(),
                'enthalpy':enthalpy,'bulk':bulk,'c_ad_squared':cad,
                'low_pressure_upper_bound':pressure_bound,'errors':error})
        rows.append({'key':list(key(row)),'g':row['g'],'return_w':row['return_w'],'answers':answers})
    assert len(rows)==36
    output={'status':'INDEPENDENT_CHECKS_PASS','role':'Post-result midpoint and complex-step arithmetic, not dynamics or a population fit.',
        'script_sha256':sha(Path(__file__)),'input_sha256':files,'rows':rows,
        'modal_entries':sum(len(x['answers'][-1]['energy_curvature'])for x in rows),
        'max_scaled_residual':max(v for r in rows for q in r['answers']for v in q['errors'].values())}
    with OUTPUT.open('x')as stream:
        json.dump(output,stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in output.items()if k not in ('rows','input_sha256')},indent=2))

if __name__=='__main__':main()
