"""New necessary same-clock patch-span test; saved fields only, no fit."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

HERE=Path(__file__).resolve().parent
STEM='SPHERICAL_GRADIENT_BOUNDED_CLOCK_PATCH_SPAN_V001'
PROTOCOL_SHA='58bd219806f72fff2d805e82966443e05f8ea2ff4ea3aabdd27d2693267261d7'
PINS={'SPHERICAL_GRADIENT_FORWARD_V001_RESULT.json':'657fa06ac5fe875a6ccef405b8061c42eb63f4715ed7878ee16f6836e10682f7',
'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V001.md':'8359678351bc69f6e58abc6e0355e9b1f7d450138645c8939b944b0769c16e08',
'SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md':'a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57',
'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json':'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f'}
A0,C,EPS,CAP=1.0059833281731022e-10,299792458.,1e-6,150.
STARTS=(5.,10.,20.,50.)
OUT=HERE/(STEM+'_RESULT.json')
REPORT=HERE/(STEM+'_REPORT.md')
ERROR=HERE/(STEM+'_ERROR.json')
CONTROLS=[]
CUSTODY={}


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check(name,value,tol):
    value=float(value)
    CONTROLS.append(dict(name=name,error=value,tolerance=tol,passed=bool(math.isfinite(value) and value<=tol)))


def strict(ok,name):
    if not ok:raise AssertionError(name)


def seals():
    for name,h in CUSTODY.items():strict(sha(HERE/name)==h,'Changed seal '+name)


def analytic(r,g,start):
    # Exact primitive of g affine in log(r), split at every saved radial knot.
    knots=np.r_[start,r[(r>start)&(r<CAP)],CAP]
    vals=np.interp(np.log(knots),np.log(r),g)
    rr,zz=knots[:-1],np.log(knots[1:]/knots[:-1])
    slope=np.diff(vals)/zz
    moment=zz+(zz-1)*np.expm1(zz)
    return float(np.sum(rr*(vals[:-1]*np.expm1(zz)+slope*moment)))


def quadrature(r,g,start,order,manufactured=None):
    knots=np.r_[start,r[(r>start)&(r<CAP)],CAP]
    xx=np.log(knots)
    mid,half=(xx[1:]+xx[:-1])/2,np.diff(xx)/2
    nodes,weights=np.polynomial.legendre.leggauss(order)
    u=mid[:,None]+half[:,None]*nodes
    rr=np.exp(u)
    vals=np.interp(u,np.log(r),g) if manufactured is None else manufactured(rr)
    return float(np.sum(half[:,None]*weights*rr*vals))


def save(p,obj,markdown=False):
    with p.open('x') as f:
        f.write(obj if markdown else json.dumps(obj,indent=2,allow_nan=False)+'\n')
    p.chmod(0o444)


def main():
    started=time.monotonic()
    for name,h in PINS.items():strict(sha(HERE/name)==h,'Direct pin '+name);CUSTODY[name]=h
    strict(sha(HERE/(STEM+'.md'))==PROTOCOL_SHA,'Protocol seal')
    CUSTODY[STEM+'.md']=PROTOCOL_SHA
    CUSTODY[Path(__file__).name]=sha(Path(__file__))
    prior=json.loads((HERE/'SPHERICAL_GRADIENT_FORWARD_V001_RESULT.json').read_text())
    cal=json.loads((HERE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    strict(prior['all_numerical_controls_pass'] and len(prior['cases'])==12,'Twelve qualified parent cases')
    strict(cal['fixed']['eps']==EPS and cal['all_controls_passed'],'Inherited fixed bounded eps')
    band=math.log1p(EPS)/2
    rows=[]
    for old in prior['cases']:
        name=old['filename'];strict(sha(HERE/name)==old['sha256'],'Actual parent case '+name)
        CUSTODY[name]=old['sha256'];case=json.loads((HERE/name).read_text())
        strict(case['qualified_newton'] and case['status']=='converged','Qualified actual case')
        r=np.array(case['r']);w=np.array(case['spectral_weights']);source=np.array(case['source_over_r'])
        u,local_u=np.array(case['mode_u']),np.array(case['local_u'])
        strict(u.shape==local_u.shape==(len(w),len(r)) and source.shape==r.shape,'Field dimensions')
        strict(r[0]<min(STARTS) and r[-1]>CAP and np.all(np.diff(r)>0),'Patch inside saved support')
        strict(np.isfinite(u).all() and np.isfinite(local_u).all() and np.all(w>0),'Finite positive field census')
        full,local=r*(source+w@u),r*(source+w@local_u)
        delta=r*(w@(u-local_u));baryon=r*source
        tag=str(old['mass_Msun'])+'_'+str(old['index'])
        check('positive_total_'+tag,max(0.,-float(np.min(full)),-float(np.min(local))),0.)
        check('matched_delta_'+tag,np.max(abs(full-local-delta)/np.maximum(full,local)),1e-12)
        for i,x in enumerate(case['readouts']['r']):
            value=float(np.interp(math.log(x),np.log(r),full));expected=case['readouts']['g_full_over_a0'][i]
            check('saved_readout_'+tag+'_'+str(x),abs(value/expected-1),1e-11)
        scale=A0*case['rM_metres']/C**2
        for start in STARTS:
            values={}
            for label,field in [('full',full),('local',local),('delta',delta),('baryon',baryon)]:
                exact=analytic(r,field,start);lo=quadrature(r,field,start,8);hi=quadrature(r,field,start,16)
                strict(exact!=0 and hi!=0,'Nonzero primitive '+label)
                check('exact16_'+tag+'_'+str(start)+'_'+label,abs(exact/hi-1),1e-10)
                check('quadrature8_16_'+tag+'_'+str(start)+'_'+label,abs(lo/hi-1),1e-10)
                values[label]=dict(dimensionless_integral=exact,gauss8_integral=lo,gauss16_integral=hi,delta_lnN=scale*exact)
            span=values['full']['delta_lnN']
            rows.append(dict(mass_Msun=old['mass_Msun'],case_index=old['index'],start_over_rM=start,end_over_rM=CAP,
                             a0_rM_over_c2=scale,values=values,permissive_clock_band=band,
                             full_span_over_band=span/band,necessary_patch_band_condition=bool(span<band),
                             full_span_minus_band=span-band,
                             weak_order_scale_squared=span*span))
            if old['index']==2:
                for label,fn,expected in [('1r',lambda x:1/x,math.log(CAP/start)),
                                          ('1r2',lambda x:1/x**2,1/start-1/CAP),
                                          ('constant',lambda x:np.ones_like(x),CAP-start)]:
                    got=quadrature(r,None,start,16,fn)
                    check('manufactured_'+label+'_'+tag+'_'+str(start),abs(got/expected-1),1e-11)
    comparisons=[]
    for mass in sorted(set(z['mass_Msun'] for z in rows)):
        for start in STARTS:
            selected={z['case_index']:z for z in rows if z['mass_Msun']==mass and z['start_over_rM']==start}
            for name,a,b in [('mesh',0,1),('spectrum',1,2),('boundary',2,3)]:
                differences={label:abs(selected[a]['values'][label]['delta_lnN']/selected[b]['values'][label]['delta_lnN']-1) for label in ('full','local','baryon')}
                check('span_refinement_'+name+'_'+str(mass)+'_'+str(start),max(differences.values()),1e-3)
                comparisons.append(dict(mass_Msun=mass,start_over_rM=start,comparison=name,span_relative_changes=differences,
                                        physical_dispositions_agree=selected[a]['necessary_patch_band_condition']==selected[b]['necessary_patch_band_condition']))
    strict(len(rows)==48 and len(comparisons)==36,'Full physical and refinement census')
    seals()
    result=dict(scope='Necessary aligned stationary same-T bounded-clock admission of inherited leading-weak gradient patches; no joined field solve or observed fit.',
                custody=CUSTODY,inputs=dict(a0_m_s2=A0,c_p_m_s=C,eps=EPS,starts_over_rM=STARTS,cap_over_rM=CAP),
                rows=rows,comparisons=comparisons,controls=CONTROLS,all_numerical_controls_passed=all(z['passed'] for z in CONTROLS),
                physical_admitted_patch_count=sum(z['necessary_patch_band_condition'] for z in rows),
                physical_rejected_patch_count=sum(not z['necessary_patch_band_condition'] for z in rows),
                elapsed_seconds=time.monotonic()-started)
    text=['# Saved gradient patches and bounded same-clock admission V001','',result['scope'],'',
          'Numerical controls: '+('PASS' if result['all_numerical_controls_passed'] else 'FAIL')+' ('+str(len(CONTROLS))+').',
          'The physical condition below is independent of numerical qualification. A necessary pass does not establish a joint state.','',
          '| Mass Msun | Inner r/rM | Outer r/rM | Full Delta ln N | Span / clock band | Necessary aligned patch condition |',
          '|---:|---:|---:|---:|---:|---|']
    for z in rows:
        if z['case_index']==3:text.append(f'| {z["mass_Msun"]:.0e} | {z["start_over_rM"]:g} | {CAP:g} | {z["values"]["full"]["delta_lnN"]:.12g} | {z["full_span_over_band"]:.9g} | '+('satisfied' if z['necessary_patch_band_condition'] else 'VIOLATED')+' |')
    text+=['',f'All48 physical dispositions retained: {result["physical_admitted_patch_count"]} necessary patch passes; {result["physical_rejected_patch_count"]} violations.',
           'All full/local/baryonic/direct-difference primitives, two quadrature values and36 prior-arm comparisons are saved.',
           'No frequency, eps, additive offset or matched cosmic state was selected. Each is only a finite leading-weak prepared patch; tilted/time-dependent/full joined solutions and observed galaxies remain separate.']
    save(OUT,result);save(REPORT,'\n'.join(text)+'\n',True);seals()
    print(json.dumps(dict(numerical_all_pass=result['all_numerical_controls_passed'],controls=len(CONTROLS),rows=len(rows),physical_violations=result['physical_rejected_patch_count'],seconds=result['elapsed_seconds'],result_sha256=sha(OUT)),indent=2))
    return 0 if result['all_numerical_controls_passed'] else 3


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true')
    if not parser.parse_args().execute:parser.error('--execute required')
    for p in (OUT,REPORT,ERROR):strict(not p.exists(),'Preserve existing evidence '+p.name)
    try:raise SystemExit(main())
    except Exception as exc:
        save(ERROR,dict(status='INCOMPLETE_ERROR',error=repr(exc),source_sha256=sha(Path(__file__)),custody=CUSTODY,controls=CONTROLS))
        raise
