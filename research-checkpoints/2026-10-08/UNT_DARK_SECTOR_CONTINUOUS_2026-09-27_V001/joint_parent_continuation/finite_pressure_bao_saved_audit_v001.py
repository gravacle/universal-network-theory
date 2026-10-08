"""Independent saved-array arithmetic only; no producer, quadrature or root import."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files={}; manifests=set(); occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True); p.relative_to(ROOT)
    got=sha(p)
    if digest is not None and got!=digest: raise AssertionError(('hash',str(p)))
    files[str(p.relative_to(ROOT))]=got
    return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,digest in json.loads(p.read_text())['files'].items():
        raw=Path(name)
        candidates=[raw] if raw.is_absolute() else [ROOT/raw,p.parent/raw]
        matches={x.resolve() for x in candidates if x.is_file() and x.resolve().is_relative_to(ROOT)}
        if len(matches)!=1:raise AssertionError(('manifest path',name))
        m=member(matches.pop(),digest);occurrences+=1
        if m.name.endswith('_FROZEN.json'):manifest(m)
def packet(name,freeze,digest=None):
    p=member(HERE/name,digest); obj=json.loads(p.read_text())
    fp=member(HERE/freeze); manifest(fp)
    if obj['freeze_sha256']!=sha(fp):raise AssertionError('freeze link')
    if hashlib.sha256(enc(obj['payload'])).hexdigest()!=obj['payload_sha256']:raise AssertionError('payload')
    return obj['payload']
counts={}; maxima={}; failures=[]
def check(name,a,b,scale=1.,tol=3e-10):
    er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
    m=float(np.max(er));counts[name]=counts.get(name,0)+int(er.size);maxima[name]=max(maxima.get(name,0.),m)
    if not np.all(np.isfinite(er)) or m>tol:failures.append(dict(check=name,error=m,tolerance=tol))
def yes(name,x):check(name,int(bool(x)),1,tol=0)
inv=packet('BBN_SHARED_INVERSE_V001_RESULTS.json','BBN_SHARED_INVERSE_V001_FROZEN.json',
           'e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0')
old=packet('DESI_BAO_SHAPE_V001_RESULTS.json','DESI_BAO_SHAPE_V001_FROZEN.json',
           '1b7f1b02b2988e0109c1afd01f4ca621e36f1cd5729261ebff676853596f3fe7')
points={p['point_id']:p for p in inv['table_points']}
states={(s['point_id'],s['background_id'],s['spectrum_index']):s for s in inv['state_rows']}
constants={(s['background_id'],s['spectrum_index']):s for s in inv['constants']}
bgmap={b['background_id']:b for b in inv['backgrounds']}
rawdata=[]
for line in (HERE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt').read_text().splitlines():
    if line.strip() and not line.lstrip().startswith('#'):
        z,y,label=line.split();rawdata.append((float(z),float(y),label))
cov=np.loadtxt(HERE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt')
y=np.array([x[1] for x in rawdata]);chol=np.linalg.cholesky(cov)
dataorder=[[x[0],x[2]] for x in rawdata]
yes('LyA_order',dataorder[-2:]==[[2.33,'DH_over_rs'],[2.33,'DM_over_rs']])
check('covariance_symmetry',cov,cov.T,tol=2e-12)
check('covariance_factor',chol@chol.T,cov,tol=2e-12)
def fitcheck(shape,fit):
    f=np.array(shape);ci_f=np.linalg.solve(cov,f);ci_y=np.linalg.solve(cov,y)
    curvature=float(f@ci_f);free=float(f@ci_y/curvature);amp=max(0.,free)
    residual=amp*f-y;ci_r=np.linalg.solve(cov,residual)
    check('profile_amplitude',fit['amplitude'],amp,max(1,amp))
    check('profile_unconstrained',fit['unconstrained_amplitude'],free,max(1,abs(free)))
    check('profile_curvature',fit['curvature_half'],curvature,curvature)
    yes('profile_boundary',fit['boundary_active']==(free<0))
    check('prediction',fit['prediction'],amp*f,np.maximum(1,np.abs(amp*f)))
    check('residual',fit['residual'],residual,np.maximum(1,np.abs(residual)))
    check('whitened',fit['whitened_residual'],np.linalg.solve(chol,residual),np.maximum(1,np.abs(fit['whitened_residual'])))
    check('covariance_contributions',fit['covariance_residual_contributions'],residual*ci_r,np.maximum(1,np.abs(residual*ci_r)))
    check('profile_score',fit['score'],float(residual@ci_r),max(1,fit['score']))
    check('profile_derivative',fit['derivative'],2*float(f@ci_r),max(1,curvature*abs(amp)))
records=[];runstats=[];dust_by_bg={};seen=set()
label_mapping=[{k:r[k] for k in ['point_id','background_id','spectrum_index','status']} for r in inv['state_rows']]
for bi in range(5):
    pl=packet(f'FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{bi}.json','FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json')
    yes('subset_status',pl['status']=='COMPLETE_BACKGROUND_SUBSET' and not pl['benchmark_only'] and not pl['failures'])
    yes('subset_id',pl['selected_background_id']==bi and len(pl['records'])==67)
    yes('all_labels',pl['retained_state_label_mapping']==label_mapping)
    yes('metadata',pl['backgrounds']==inv['backgrounds'] and pl['reference_mapping']==inv['reference_mapping'])
    yes('data_order',pl['data']['order']==dataorder)
    check('data_values',pl['data']['values'],y,tol=0);check('covariance_bytes_values',pl['data']['covariance'],cov,tol=0)
    yes('recombination_not_computed',pl['configuration']['actual_recombination_status']=='NOT_COMPUTED')
    dust=pl['dust_controls'][0];yes('dust_id',len(pl['dust_controls'])==1 and dust['background_id']==bi)
    fitcheck(dust['shape'],dust['fit']);dust_by_bg[bi]=dust
    check('old_dust_shape',dust['historical_zero_radiation_shape'],old['references'][bgmap[bi]['representative_reference']]['shape'],np.abs(dust['historical_zero_radiation_shape']))
    runstats.append(dict(background_id=bi,seconds=pl['seconds'],peak_self_rss_bytes=pl['peak_self_rss_bytes'],producer_checks=sum(pl['counts'].values()),producer_maxima=pl['maxima']))
    for row in pl['records']:
        pi=row['point_id'];p=points[pi];bg=bgmap[bi];src=states[(pi,bi,0)]
        yes('row_association',(pi,bi) not in seen and row['background_id']==bi);seen.add((pi,bi))
        yes('row_status',row['status']=='COMPLETE_CONDITIONAL_BACKGROUND')
        yes('roles',row['point_roles']==p['roles'] and row['inherited_local_BBN_rectangle']==p['prediction']['local_numerical_rectangle'])
        check('table_parameters',[row['omega_b'],row['Delta']],[p['omega_b'],p['Delta']],tol=0)
        finite=src['status']=='FINITE_HARD_STATE';yes('finite_label',row['finite_gap']==finite)
        check('r1',row['r1'],2*src['s']**2/(1-src['s']**2) if finite else 0.,max(row['r1'],1e-300))
        check('density_parameters',[row['Omega_b'],row['Omega_exc']],[src['Omega_b'],src['Omega_exc']])
        check('baryon_physical_density',row['Omega_b'],p['omega_b']/(bg['H0_km_s_Mpc']/100)**2)
        check('total_matter',row['Omega_b']+row['Omega_exc'],bg['Omega_m'])
        og=constants[(bi,0)]['Omega_gamma'];orad=og*(1+inv['fnu']*3.044)
        check('ordinary_radiation',row['Omega_ordinary_radiation'],orad,orad)
        check('present_normalization',row['H_present_over_Hcal'],math.sqrt(1+orad))
        for si in range(4):
            ss=states[(pi,bi,si)]
            yes('copy_status',row['spectrum_statuses'][si]==ss['status'])
            check('copy_background',[ss['Omega_b'],ss['Omega_exc']],[row['Omega_b'],row['Omega_exc']])
            if finite:
                check('copy_r1',2*ss['s']**2/(1-ss['s']**2),row['r1'],row['r1'])
                target=(p['Delta']*inv['fnu']*og/(inv['C4']*row['Omega_exc']))**.75
                check('copy_normalized_action',ss['I']/ss['hard_energy']**.75,target,target)
        fitcheck(row['shape'],row['fit'])
        check('dust_score_difference',row['score_minus_same_background_dust'],row['fit']['score']-dust['fit']['score'])
        check('dust_shape_difference',row['fractional_shape_minus_dust'],np.array(row['shape'])/dust['shape']-1)
        unit=299792.458/bg['H0_km_s_Mpc'];Ac=1e7;qq=p['Delta']*inv['fnu']*og
        tail=min(2/(math.sqrt(3)*Ac*(math.sqrt(qq+row['Omega_b']/Ac)+math.sqrt(qq))),2/math.sqrt(3*bg['Omega_m']*Ac))
        req=row['required_drag'];yes('required_endpoint_scope',req['status']=='REQUIRED_ENDPOINT_NOT_RECOMBINATION')
        check('ruler_units',req['ruler_Mpc'],unit/row['fit']['amplitude'],req['ruler_Mpc'])
        check('early_tail',req['unknown_early_tail_Mpc_interval'],[0,unit*tail],max(1,unit*tail))
        lo,hi=req['A_interval'];yes('endpoint_order',lo is not None and hi is not None and 1<=lo<=hi<=Ac)
        yes('epoch_census',[e['A'] for e in row['epochs']]==[1.,11.,101.,501.,1101.,3001.,10001.])
        lastph=lasthard=float('inf')
        for ep in row['epochs']:
            A=ep['A'];ratio=ep['energy_over_present'];w=ep['w'];ci=ep['cI2']
            check('dust_energy_ratio',ep['energy_over_dust'],ratio/A**3,max(1,ratio/A**3))
            check('H_identity',ep['H_over_Hcal']**2,row['Omega_b']*A**3+row['Omega_exc']*ratio+bg['Omega_Lambda']+orad*A**4,ep['H_over_Hcal']**2)
            yes('energy_envelope',A**3*(1-3e-11)<=ratio<=A**4*(1+3e-11))
            yes('material_bounds',0<=w<=1/3+3e-11 and 0<=ci<=1/3+3e-11)
            yes('pressure_sound_bound',ci<=2*w/(1+w)+3e-11)
            ph=ep['photon_horizon_Mpc_interval'];hard=ep['hard_horizon_Mpc_interval']
            yes('horizon_positive_monotone',0<=ph[0]<=ph[1] and ph[0]<=lastph and 0<=hard[0]<=hard[1] and hard[0]<=lasthard)
            lastph,lasthard=ph[0],hard[0]
            check('photon_tail_width',ph[1]-ph[0],unit*tail,max(1,unit*tail))
            check('hard_tail_width',hard[1]-hard[0],unit*tail if finite else 0.,max(1,unit*tail))
            if A==1:
                check('present_energy',ratio,1.)
                check('saved_present_material',[w,ci],[src['w'],src['cI2']] if finite else [0,0],np.maximum([w,ci],1e-300))
            if not finite:check('dust_epoch',[ratio/A**3,w,ci],[1,0,0])
        markers=row['transition_markers'];yes('marker_targets',[m['w'] for m in markers]==[.01,.1,.3])
        if finite:
            yes('marker_order',all(m['A'] is not None for m in markers) and markers[0]['A']<markers[1]['A']<markers[2]['A'])
        else:
            yes('dust_markers',all(m['A'] is None and m['status']=='DUST_LIMIT_NO_TRANSITION' for m in markers))
            check('exact_dust_shape',row['shape'],dust['shape'],np.maximum(np.abs(dust['shape']),1e-300))
        records.append(row)
yes('complete_histories',seen=={(pi,bi) for pi in points for bi in range(5)} and len(records)==335)
def summary(rr):
    if not rr:return dict(count=0)
    def bounds(fn):
        values=[fn(r) for r in rr];return [min(values),max(values)]
    def epoch(r):return next(e for e in r['epochs'] if e['A']==1101.)
    return dict(count=len(rr),finite=sum(r['finite_gap'] for r in rr),local_BBN_rectangle=sum(r['inherited_local_BBN_rectangle'] for r in rr),
        score=bounds(lambda r:r['fit']['score']),score_minus_dust=bounds(lambda r:r['score_minus_same_background_dust']),
        max_abs_fractional_shape_minus_dust=max(max(abs(x) for x in r['fractional_shape_minus_dust']) for r in rr),
        ruler_Mpc=bounds(lambda r:r['required_drag']['ruler_Mpc']),required_A_lower=bounds(lambda r:r['required_drag']['A_interval'][0]),
        required_A_upper=bounds(lambda r:r['required_drag']['A_interval'][1]),tail_Mpc=bounds(lambda r:r['required_drag']['unknown_early_tail_Mpc_interval'][1]),
        A1101_w=bounds(lambda r:epoch(r)['w']),A1101_cI2=bounds(lambda r:epoch(r)['cI2']),
        A1101_energy_over_dust=bounds(lambda r:epoch(r)['energy_over_dust']),A1101_hard_horizon_lower_Mpc=bounds(lambda r:epoch(r)['hard_horizon_Mpc_interval'][0]),
        A1101_photon_horizon_lower_Mpc=bounds(lambda r:epoch(r)['photon_horizon_Mpc_interval'][0]))
groups={'all':summary(records),'all_finite':summary([r for r in records if r['finite_gap']]),
        'all_dust_limits':summary([r for r in records if not r['finite_gap']])}
for label,predicate in [('joint_any',lambda roles:any(x.startswith('joint:') for x in roles)),
                        ('central_only',lambda roles:any(x.startswith('central:') for x in roles))]+[
                        (f'joint_{k}',lambda roles,k=k:any(x.startswith(f'joint:{k}:') for x in roles)) for k in (1,2,3)]:
    for finite in (False,True):
        rr=[r for r in records if predicate(r['point_roles']) and (r['finite_gap'] or not finite)]
        groups[label+('_finite' if finite else '_including_limits')]=summary(rr)
bybg={str(bi):{'joint_finite':summary([r for r in records if r['background_id']==bi and r['finite_gap'] and any(x.startswith('joint:') for x in r['point_roles'])]),
              'dust_score':dust_by_bg[bi]['fit']['score']} for bi in range(5)}
out=dict(status='PASS_SAVED_ARITHMETIC' if not failures else 'FAILED',scope='No producer, quadrature, endpoint inversion, or optimization rerun. Saved distance/horizon integrals and transition roots are not independently recomputed.',
         checks=counts,maxima=maxima,failures=failures,total_checks=sum(counts.values()),files=files,
         unique_files=len(files),recursive_manifests=len(manifests),manifest_member_occurrences=occurrences,
         histories=len(records),represented_labels=len(label_mapping),run_statistics=runstats,summary_groups=groups,by_background=bybg)
print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False))
