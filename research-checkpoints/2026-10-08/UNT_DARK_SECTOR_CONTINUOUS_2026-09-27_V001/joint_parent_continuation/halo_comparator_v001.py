"""Same-source saved-field halo comparisons. Stdout only; no field solve."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import re
import resource
import time
import numpy as np
import halo_profile_fitter_v001 as fit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.resolve()
STEMS=['galaxy_HI1_H21','galaxy_HI0_H21','galaxy_HI1_H20','galaxy_HI0_H20',
       'ML36_CAL_HI1_H21_V001','HALOGAS40_ML36_RETAINED_V001',
       'HALOGAS120_ML36_RETAINED_V001','DDO154_THINGS_NA40_ML36_H2OMIT_V001',
       'DDO154_THINGS_RO40_ML36_H2OMIT_V001']
FREEZES=['GALAXY_FIELD_FROZEN.json','STELLAR_CALIBRATION_FROZEN.json',
         'HALOGAS_FIELD_FROZEN.json','external_ddo154_v001/FIELD_V002_FROZEN.json',
         'external_ddo154_v001/SCORING_FROZEN.json']
RECEIPTS={'STELLAR_CALIBRATION_RESULTS.json':FREEZES[1],
          'HALOGAS_FIELD_RESULTS.json':FREEZES[2],
          'external_ddo154_v001/FIELD_V002_RESULTS.json':FREEZES[3],
          'external_ddo154_v001/ROTATION_COMPARISON.json':FREEZES[4]}
CONFIG=dict(stems=STEMS,models=['NFW','ISO'],masks=[0.,2.],
            weightings=['equal','quoted_error'],grids=[257,513],
            score_relative_tolerance=1e-6,identity_tolerance=1e-8,
            synthetic_mass_tolerance=2e-11,synthetic_derivative_tolerance=2e-8,
            synthetic_parameter_tolerance=1e-4,synthetic_sse_tolerance=1e-8,
            helper=fit.CONFIG)


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload(path,freeze=None):
    data=json.loads(path.read_text())
    if data['payload_sha256']!=hashlib.sha256(encoded(data['payload'])).hexdigest():
        raise RuntimeError('Canonical payload differs: '+str(path))
    if freeze is not None and data['freeze_sha256']!=sha(freeze):
        raise RuntimeError('Freeze link differs: '+str(path))
    p=data['payload']
    if p.get('status','COMPLETE')!='COMPLETE':
        raise RuntimeError('Parent not complete: '+str(path))
    if 'checks' in p and isinstance(p['checks'],dict) and not all(p['checks'].values()):
        raise RuntimeError('Parent numerical checks failed: '+str(path))
    return p


def inputs():
    files={}
    def remember(path,expected=None):
        path=path.resolve()
        if not path.is_relative_to(ROOT):
            raise RuntimeError('Input outside project root')
        digest=sha(path)
        if expected is not None and digest!=expected:
            raise RuntimeError('Input identity differs: '+str(path))
        files[str(path.relative_to(ROOT))]=digest
    proposal=HERE/'HALO_COMPARATOR_PROPOSAL_V001.md'
    prose=proposal.read_text()
    expected_pairs={m[0]:(m[1],m[2]) for m in re.findall(
        r'^\| `([^`]+)` \| `([a-f0-9]{64})` \| `([a-f0-9]{64})` \|$',prose,re.M)}
    if set(expected_pairs)!=set(STEMS):
        raise RuntimeError('Prospective input census differs')
    expected_receipts=dict(re.findall(r'^\| `([^`]+)` \| `([a-f0-9]{64})` \|$',prose,re.M))
    for name in FREEZES:
        freeze=HERE/name
        remember(freeze,expected_receipts[name])
        for rel,digest in json.loads(freeze.read_text())['files'].items():
            remember(freeze.parent/rel,digest)
    receipts={}
    for name,freeze in RECEIPTS.items():
        remember(HERE/name,expected_receipts[name])
        receipts[name]=payload(HERE/name,HERE/freeze)
        for rel,digest in receipts[name].get('case_files_sha256',{}).items():
            remember((HERE/name).parent/rel,digest)
    review=HERE/'GALAXY_FIELD_RESULTS_REVIEW_DATA.json'
    remember(review)
    previous=json.loads(review.read_text())['all_case_sha256']
    for stem in STEMS:
        base=HERE/('external_ddo154_v001' if stem.startswith('DDO154') else '')
        fi=FREEZES[3] if stem.startswith('DDO154') else FREEZES[2] if stem.startswith('HALOGAS') else FREEZES[1] if stem.startswith('ML36') else FREEZES[0]
        for newton in (0,1):
            name=stem+'_N512_L255_Newton'+str(newton)+'.json'
            remember(base/name,expected_pairs[stem][newton])
            if stem.startswith('galaxy') and sha(base/name)!=previous[name]:
                raise RuntimeError('Original reviewed case differs')
            p=payload(base/name,HERE/fi)
            if p['newtonian']!=bool(newton) or p['N']!=512 or p['extent']!=255:
                raise RuntimeError('Wrong fine-field case')
    for path in (proposal,Path(__file__).resolve(),HERE/'halo_profile_fitter_v001.py',
                 HERE/'HALO_COMPARATOR_EXECUTION_V001.md'):
        remember(path)
    return dict(config=CONFIG,files=files)


def frozen():
    path=HERE/'HALO_COMPARATOR_V001_FROZEN.json'
    snapshot=inputs()
    if json.loads(path.read_text())!=snapshot:
        raise RuntimeError('Prospective comparator freeze differs')
    return path


def recorder():
    checks=[]
    def check(name,a,b=0.,tol=CONFIG['identity_tolerance']):
        error=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        checks.append(dict(name=name,error=error,tolerance=tol,passed=bool(math.isfinite(error) and error<=tol)))
    return checks,check


def emit(p,freeze,started,**extra):
    result=dict(status='COMPLETE' if all(x['passed'] for x in p['checks']) else 'FAILED',
                payload=p,payload_sha256=hashlib.sha256(encoded(p)).hexdigest(),
                freeze_sha256=sha(freeze),seconds=time.perf_counter()-started,
                peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,**extra)
    print(json.dumps(result,allow_nan=False))
    return int(result['status']!='COMPLETE')


def tests():
    started=time.perf_counter(); freeze=frozen(); checks,check=recorder()
    nodes,weights=np.polynomial.legendre.leggauss(128)
    z=(nodes+1)/2; weights=weights/2
    for model in CONFIG['models']:
        for x in (1e-6,.05,.125,1.,10.):
            value,slope=fit._log_kernel_and_slope(model,np.array([math.log(x)]))
            # Integrating the positive spherical mass density, not subtracting
            # the closed-form speed kernels against one another.
            y=x*z
            integrand=y/(1+y)**2 if model=='NFW' else y*y/(1+y*y)
            oracle=float(weights @ integrand)
            actual=math.exp(float(value[0]))
            check(model+'_mass_'+str(x),actual/oracle,1.,CONFIG['synthetic_mass_tolerance'])
            eps=1e-5
            upper=fit._log_kernel_and_slope(model,np.array([math.log(x)+eps]))[0][0]
            lower=fit._log_kernel_and_slope(model,np.array([math.log(x)-eps]))[0][0]
            check(model+'_slope_'+str(x),(upper-lower)/(2*eps),slope[0],CONFIG['synthetic_derivative_tolerance'])
        r=np.geomspace(.1,30.,23); pivot=float(np.median(r))
        for t in (-20.,0.,20.):
            check(model+'_pivot_'+str(t),fit.shape(model,pivot,t,pivot),1.)
        check(model+'_small_scale',fit.shape(model,r,-math.inf,pivot),pivot/r if model=='NFW' else np.ones_like(r))
        check(model+'_large_scale',fit.shape(model,r,math.inf,pivot),r/pivot if model=='NFW' else (r/pivot)**2)
        b=200.+15*r; a=2500.; ell=.4; w=1+np.arange(len(r))/len(r)
        y=np.sqrt(b+a*fit.shape(model,r,ell,pivot))
        fixed=fit.optimize_amplitude(fit.shape(model,r,ell,pivot),b,y,w)
        check(model+'_amplitude_exact',fixed['amplitude']/a,1.,1e-11)
        solved=fit.profile_fit(model,r,b,y,w,129,pivot=pivot)['selected']
        check(model+'_synthetic_sse',solved['sse'],0.,CONFIG['synthetic_sse_tolerance'])
        check(model+'_synthetic_amplitude',solved['amplitude']/a,1.,CONFIG['synthetic_parameter_tolerance'])
        check(model+'_synthetic_scale',solved['logscale'],ell,CONFIG['synthetic_parameter_tolerance'])
        zero=fit.optimize_amplitude(fit.shape(model,r,0.,pivot),b,.9*np.sqrt(b),w)
        check(model+'_zero_boundary',zero['amplitude'],0.,0.)
        check(model+'_zero_gradient',min(0.,zero['amplitude_gradient']),0.,0.)
    return emit(dict(checks=checks,scope='Synthetic and numerical controls only; no observational fit'),freeze,started)


def arrays(index):
    stem=STEMS[index]
    if index<7:
        a=payload(HERE/(stem+'_N512_L255_Newton0.json'))
        b=payload(HERE/(stem+'_N512_L255_Newton1.json'))
        if a['component_masses_Msun']!=b['component_masses_Msun']:
            raise RuntimeError('Baryonic mass census differs')
        ar,br=a['comparison'],b['comparison']
        if [(x['R'],x['velocity'],x['error']) for x in ar]!=[(x['R'],x['velocity'],x['error']) for x in br]:
            raise RuntimeError('Unmatched observed rows')
        rows=[dict(radius=x['R'],observed=x['velocity'],error=x['error'],
                   baryon_v2=y['velocity_squared'],network=x['prediction']) for x,y in zip(ar,br)]
    else:
        key='NA' if index==7 else 'RO'
        p=payload(HERE/'external_ddo154_v001/ROTATION_COMPARISON.json')
        rows=[dict(radius=x['R_kpc'],observed=x['observed_velocity_kms'],error=x['quoted_error_kms'],
                   baryon_v2=x['newtonian']['velocity_squared_kms2'],network=x['candidate']['prediction_kms'])
              for x in p['models'][key]['comparison']]
    expected=43 if index<7 else 12
    if len(rows)!=expected or sum(x['radius']>=2 for x in rows)!=(37 if index<7 else 9):
        raise RuntimeError('Raw row census differs')
    if any(not all(math.isfinite(v) for v in x.values()) or min(x.values())<=0 for x in rows):
        raise RuntimeError('Invalid original row; no clipping authorized')
    return rows,{key:np.array([x[key] for x in rows]) for key in rows[0]}


def summary(prediction,a):
    result={}
    for cut in (0.,2.,8.):
        selected=a['radius']>=cut
        residual=np.asarray(prediction)[selected]-a['observed'][selected]
        result[str(cut)]=dict(count=int(selected.sum()),rms=float(np.sqrt(np.mean(residual**2))) if len(residual) else None,
            mean=float(np.mean(residual)) if len(residual) else None,
            velocity_sse=float(residual @ residual),quoted_error_sse=float(np.sum((residual/a['error'][selected])**2)))
    return result


def compact_profile(p):
    p=dict(p); grid=p.pop('grid_profiles')
    p['grid_digest']=hashlib.sha256(encoded(grid)).hexdigest()
    p['grid_census']=len(grid)
    p['grid_sse_min']=min(x['sse'] for x in grid)
    p['grid_sse_max']=max(x['sse'] for x in grid)
    removed={'prediction','residual','halo_v2','halo_velocity','shape'}
    p['candidates']=[{k:v for k,v in x.items() if k not in removed} for x in p['candidates']]
    p['selected']={k:v for k,v in p['selected'].items() if k not in removed}
    return p


def run(index):
    started=time.perf_counter(); freeze=frozen(); checks,check=recorder()
    testpath=HERE/'HALO_COMPARATOR_V001_TESTS.json'
    test=json.loads(testpath.read_text())
    if test['status']!='COMPLETE' or test['freeze_sha256']!=sha(freeze) or not all(x['passed'] for x in test['payload']['checks']):
        raise RuntimeError('Synthetic qualification missing')
    if hashlib.sha256(encoded(test['payload'])).hexdigest()!=test['payload_sha256']:
        raise RuntimeError('Synthetic payload mismatch')
    original,a=arrays(index); pivot=float(np.median(a['radius'])); results=[]
    for model in CONFIG['models']:
        for cut in CONFIG['masks']:
            mask=a['radius']>=cut
            for weighting in CONFIG['weightings']:
                weights=np.ones(len(original)) if weighting=='equal' else 1/a['error']**2
                profiles=[fit.profile_fit(model,a['radius'][mask],a['baryon_v2'][mask],a['observed'][mask],weights[mask],n,pivot=pivot) for n in CONFIG['grids']]
                small,large=profiles; best=large['selected']; score=best['sse']
                check('grid_'+model+'_'+str(cut)+'_'+weighting,small['selected']['sse'],score,CONFIG['score_relative_tolerance']*max(1,abs(score)))
                if best['amplitude_boundary']:
                    check('boundary_gradient',min(0.,best['amplitude_gradient']))
                else:
                    check('root_gradient',best['amplitude_gradient'])
                check('zero_halo_admissible',max(0.,score-large['newtonian_sse']),tol=1e-8*max(1,score))
                ell=best['logscale']
                if ell is None:
                    ell=-math.inf if best['kind']=='zero_scale_limit' else math.inf
                halo=best['amplitude']*fit.shape(model,a['radius'],ell,pivot)
                pred=np.sqrt(a['baryon_v2']+halo)
                residual=pred-a['observed']
                check('full_curve_matches_fit',pred[mask],best['prediction'])
                check('score_reconstruction',np.dot(weights[mask],residual[mask]**2),score,tol=1e-8*max(1,score))
                results.append(dict(model=model,fit_radius_min=cut,weighting=weighting,
                    fitted_row_indices=np.flatnonzero(mask).tolist(),halo_parameter_count=2,
                    halo_v2=halo.tolist(),halo_velocity=np.sqrt(halo).tolist(),prediction=pred.tolist(),
                    residual=residual.tolist(),summaries=summary(pred,a),
                    coarse_profile=compact_profile(small),fine_profile=compact_profile(large)))
    check('fit_census',len(results),8.,0.)
    p=dict(source_index=index,source=STEMS[index],galaxy='NGC3198' if index<7 else 'DDO154',
           pivot=pivot,original_rows=original,network_summary=summary(a['network'],a),
           newtonian_summary=summary(np.sqrt(a['baryon_v2']),a),fits=results,checks=checks,
           scope='Exposed-data fixed-source descriptive comparison; no likelihood or joint-stage completion')
    return emit(p,freeze,started,synthetic_result_sha256=sha(testpath))


if __name__=='__main__':
    if sys.argv[1:]==['freeze']:
        print(json.dumps(inputs(),indent=2,allow_nan=False))
    elif sys.argv[1:]==['tests']:
        raise SystemExit(tests())
    elif len(sys.argv)==2 and sys.argv[1].isdigit() and 0<=int(sys.argv[1])<len(STEMS):
        raise SystemExit(run(int(sys.argv[1])))
    else:
        raise SystemExit('Use freeze, tests, or source index0..8')
