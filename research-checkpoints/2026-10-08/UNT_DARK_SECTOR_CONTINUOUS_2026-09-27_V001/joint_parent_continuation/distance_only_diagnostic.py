"""Exposed-data, distance-only analytic fit; no source-shape or force refit."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import disk_solver as law

ROOT = Path(__file__).resolve().parent


def main():
    out = ROOT/'DISTANCE_ONLY_DIAGNOSTIC.json'
    assert not out.exists()
    # Same angular source, fixed M/L and fixed acceleration scales imply
    # v_D(theta)=sqrt(D/13.8)*v_13.8(theta). All source lengths scale together.
    # This fits already exposed data; it is explicitly not a new prediction.
    names = [(f'galaxy_HI{hi}_H2{h2}_N512_L255_Newton0', 'GALAXY_FIELD_FROZEN.json')
             for hi,h2 in ((1,1),(0,1),(1,0),(0,0))]
    names += [('ML36_CAL_HI1_H21_V001_N512_L255_Newton0', 'STELLAR_CALIBRATION_FROZEN.json')]
    names += [(f'HALOGAS{width}_ML36_RETAINED_V001_N512_L255_Newton0', 'HALOGAS_FIELD_FROZEN.json') for width in (40,120)]
    final_path = ROOT/'HALOGAS_FIELD_RESULTS.json'
    final = json.loads(final_path.read_text())
    completed = final['payload']
    assert final['freeze_sha256']==law.sha(ROOT/'HALOGAS_FIELD_FROZEN.json')
    assert final['payload_sha256']==hashlib.sha256(law.encode(completed)).hexdigest()
    assert completed['status']=='COMPLETE' and len(completed['case_files_sha256'])==8
    for name,digest in completed['case_files_sha256'].items():
        assert law.sha(ROOT/name)==digest
    cases, inputs, checks = [], {final_path.name:law.sha(final_path)}, []
    for name,frozen in names:
        path=ROOT/(name+'.json')
        obj=json.loads(path.read_text())
        p=obj['payload']
        assert obj['freeze_sha256']==law.sha(ROOT/frozen)
        assert obj['payload_sha256']==hashlib.sha256(law.encode(p)).hexdigest()
        assert p['case']==name and all(p['checks'].values())
        rows=p['comparison']
        assert len(rows)==43 and all(r['prediction'] is not None and r['error']>0 for r in rows)
        inputs[path.name]=law.sha(path)
        inputs[frozen]=law.sha(ROOT/frozen)
        fits=[]
        for weighting in ('equal_all43', 'quoted_error_inverse_variance_all43'):
            weights=[1. if weighting=='equal_all43' else 1/r['error']**2 for r in rows]
            pp=math.fsum(w*r['prediction']**2 for w,r in zip(weights,rows))
            po=math.fsum(w*r['prediction']*r['velocity'] for w,r in zip(weights,rows))
            oo=math.fsum(w*r['velocity']**2 for w,r in zip(weights,rows))
            assert pp>0 and po>0
            unconstrained=po/pp
            # The paper's 13.8 +/-1.5 Mpc interval is a declared comparison
            # bound, not a posterior, Gaussian prior or confidence statement.
            bounded=min(math.sqrt(15.3/13.8),max(math.sqrt(12.3/13.8),unconstrained))
            for constraint,scale in (('unconstrained_positive_distance',unconstrained),
                                     ('published_12.3_to_15.3_Mpc_interval',bounded)):
                residual=[scale*r['prediction']-r['velocity'] for r in rows]
                objective=math.fsum(w*e*e for w,e in zip(weights,residual))
                polynomial=pp*scale*scale-2*po*scale+oo
                error=abs(objective-polynomial)
                allowance=1e-11*max(1.,pp*scale*scale+2*abs(po*scale)+oo)
                checks.append({'name':name+'/'+weighting+'/'+constraint,
                               'error':error,'tolerance':allowance,'passed':error<=allowance})
                summaries={}
                for lower in (0.,2.,8.):
                    chosen=[e for r,e in zip(rows,residual) if r['R']>=lower]
                    summaries[f'original_radius_ge_{lower:g}_kpc']={
                        'count':len(chosen),'rms_kms':math.sqrt(math.fsum(e*e for e in chosen)/len(chosen))}
                fits.append({'weighting':weighting,'constraint':constraint,
                    'speed_multiplier':scale,'distance_Mpc':13.8*scale*scale,
                    'weighted_objective':objective,'descriptive_same_angular_row_groups':summaries,
                    'all43_residuals_kms':residual,'last_radius_prediction_kms':scale*rows[-1]['prediction']})
        cases.append({'case':name,'original_distance_Mpc':13.8,'fits':fits})
    result={'status':'COMPLETE' if all(c['passed'] for c in checks) else 'FAILED',
        'role':'In-sample one-amplitude diagnostic, not held-out evidence or source-shape correction',
        'formula':'s=sum(w*v_model*v_obs)/sum(w*v_model^2); D=13.8*s^2 Mpc',
        'scope':'Angular source/tracer coordinates are fixed and every physical length scales with D. Angular surface-density profiles and acceleration scales stay fixed; three-dimensional density transforms as rho_D(x)=rho_0(x/d)/d, d=D/13.8. Quoted errors omit source/geometry covariance; no likelihood or significance claimed.',
        'interval_source':'https://arxiv.org/pdf/1304.4232, Table1 and section5.3; original sources in existing packets',
        'input_sha256':inputs,'script_sha256':law.sha(Path(__file__)),
        'cases':cases,'checks':checks}
    result['payload_sha256']=hashlib.sha256(law.encode(result)).hexdigest()
    law.save_new(out,result)
    print(json.dumps({'status':result['status'],'sources':len(cases),'fits':sum(len(c['fits']) for c in cases)}))


if __name__=='__main__':
    main()
