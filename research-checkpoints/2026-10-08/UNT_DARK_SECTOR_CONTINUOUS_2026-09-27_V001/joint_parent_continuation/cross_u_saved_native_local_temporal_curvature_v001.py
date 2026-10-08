"""Guarded root-only saved local native temporal-curvature inventory; no evolution."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
AUTHOR_DRAFT=False
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001'
PARENT='CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001'
PROTOCOL_SHA='7e5f08b5b34b67188eba1fdb7c741a1d788ffe12db30da46758d646c46e3e904'
PINS={'CROSS_U_NATIVE_RETARDED_RESPONSE_AND_STATIONARY_HISTORY_V001.md': '662a0eb290057bf0d7f5160e64c38edf17257b4073c1b07f4fa15ef1e1c710c7', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md': '048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py': 'e77230a1819e89799e4463d5ca3808b1cab9f6a2c9166b593cbca2b949dec853', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001.md': '3ffc808394102d8b7479d9e1f604ba940e0ac7570181f1c386fb5eddc2c5e729', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RESULT.json': '963de6b73e19820fc424bbb994d7e07fbed4ecea4401b25730fbe38499f1524d', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json': 'b7834e205c379e8f9444e3ac17243744fc2266f92ccd186bcd780a7cebaac926', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_FINE_Q3_CASE.json': '587f3686c9d232fadfb9c7b41ecc88e94246740bbfef52cc3db7e9917d4713bd', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_MANIFEST.json': 'a103ef976e3035fb48c57b878328620cf49f92118f5aeb45a84ee9dc4665ea0c', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz': 'e12f36d7b3c822d41d003ff428fae88ed433436ce3f58c2f6764b046c81aac49', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00165_FINAL.npz.COMMIT.json': 'af8945a902a162bb8a1fd6772021dc4899498ec006ba0965063a498aec34aff0', 'sparc_official_NGC3198_rotmod.dat': '17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953'}
SIGMAS=(.1,1.,10.,100.)
A0=1.0059833281731022e-10;L0=3.085677581491367e19;CP=299792458.;GC=3*math.pi/8;B=A0*L0/CP**2
HUNIT=67.49711988577813;TOL=2e-11;CONTROL_COUNT=8
np=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];RAW={};CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('physical_inertia_registered','full_metric_qualified','global_native_spectrum_qualified','global_stability_qualified','retarded_response_qualified','formation_qualified','physical_exterior_qualified','observational_qualified','joint_model_adopted')}

def now():return datetime.now(timezone.utc).isoformat()

def path(n):
    p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:assert math.isfinite(v);return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,raw):
    p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[name]=sha(p);assert p.read_bytes()==raw
    return CREATED[name]

def json_file(name,v):return publish(name,encode(v))

def seal_created():
    for p in BASE.glob(STEM+'_*'):
        if p.is_file():p.chmod(0o444);CREATED[p.name]=sha(p)

def merge(mapping,pins):
    for n,h in mapping.items():
        assert type(n) is str and type(h) is str and len(h)==64
        assert n not in pins or pins[n]==h,('conflicting byte binding',n)
        pins[n]=h

def authenticate():
    pins=dict(PINS,**{STEM+'.md':PROTOCOL_SHA})
    assert pins and all(len(h)==64 for h in pins.values())
    for n,h in pins.items():assert sha(path(n))==h,('direct seal',n)
    receipt=json.loads(path(PARENT+'_RECEIPT.json').read_text())
    assert receipt['status']=='CLOSED' and receipt['owner']['owner']=='root' and receipt['owner']['pid']==78729
    assert receipt['closed']>receipt['owner']['started'] and receipt['owner']['source_sha256']==pins['cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py']
    assert receipt['result_sha256']==pins[PARENT+'_RESULT.json'] and all(v is False for v in receipt['physical_flags'].values())
    merge(receipt['input_sha256'],pins);merge(receipt['output_sha256'],pins)
    for n,h in pins.items():assert sha(path(n))==h,('full CLOSED input/output seal',n)
    case=json.loads(path(PARENT+'_FINE_Q3_CASE.json').read_text());manifest=json.loads(path(PARENT+'_MANIFEST.json').read_text())
    assert manifest['owner']==receipt['owner']
    assert case['arm']=='FINE_Q3' and case['status']=='CONVERGED' and case['identity']['grid_shape']==[65,173,89]
    assert case['identity']['Hunit']==HUNIT and case['identity']['eps']==1e-5 and case['identity']['quadrature_order']==3
    assert case['identity']['space_refined'] is True and case['identity']['hi_tail'] is False and case['identity']['h2_tail'] is False
    assert case['identity']['source_identity']['source_id']=='EXP24' and case['identity']['source_identity']['eps']==1e-5
    assert case['identity']['stellar_refinement_manifest_sha256']==pins[PARENT+'_MANIFEST.json']
    assert case['identity']['stellar_refinement_source_sha256']==pins['cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py']
    assert all(v is False for v in case['physical_flags'].values()) and case['readout_qualified'] is False
    assert len(case['controls'])==22 and all(c['passed'] for c in case['controls']) and len(case['source_controls_copied'])==20
    assert len(case['historical_native_controls'])==3 and [c['passed'] for c in case['historical_native_controls']]==[False,True,True]
    rec=case['final_checkpoint'];assert rec['file']==PARENT+'_00165_FINAL.npz'
    assert pins[rec['file']]==rec['sha256'] and pins[rec['commit_file']]==rec['commit_sha256']
    assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
    md=rec['metadata'];assert md['owner']==receipt['owner'] and md['arm']=='FINE_Q3' and md['status']=='CONVERGED'
    assert md['kind']=='final_state_and_signed_readouts' and md['identity']==case['identity'] and md['source_identity']==case['identity']['source_identity']
    return pins,case,rec

def load_input(rec,case):
    names=('final_state','current_mask','current_weights','current_xi','final_midplane_psi')
    out={}
    with np.load(path(rec['file']),allow_pickle=False) as z:
        assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
        for n in names:
            a=z[n].copy();RAW['parent_'+n]=a
            assert rec['metadata']['schema'][n]==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
            assert np.all(np.isfinite(a));out[n]=a
    x=out['final_state'];mask=out['current_mask'];w=out['current_weights'];xi=out['current_xi']
    assert x.shape==mask.shape==(65,173,89) and x.dtype==np.dtype('float64') and mask.dtype==np.dtype('bool')
    assert w.shape==xi.shape==(32,) and w.dtype==xi.dtype==np.dtype('float64')
    assert np.all(w>0) and np.all(xi>0) and np.all(xi<1) and np.all(np.diff(xi)>0) and abs(float(w.sum())-1)<=TOL
    assert np.all(x[~mask]==0) and np.array_equal(x[0,:,0],out['final_midplane_psi'])
    r=np.array(case['identity']['r_kpc'],dtype=float);z=np.array(case['identity']['z_kpc'],dtype=float)
    RAW['r_kpc']=r;RAW['z_kpc']=z
    assert r.shape==(173,) and z.shape==(89,) and np.all(np.isfinite(r)) and np.all(np.isfinite(z))
    assert r[0]==z[0]==0 and r[-1]==z[-1]==128 and np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
    radii=[]
    for line in path('sparc_official_NGC3198_rotmod.dat').read_text().splitlines():
        if line.strip() and not line.startswith('#'):radii.append(float(line.split()[0]))
    q=np.array(radii,dtype=float);RAW['official_radii_kpc']=q
    assert q.shape==(43,) and np.all(np.isfinite(q)) and np.all(np.diff(q)>0) and np.all(q>r[0]) and np.all(q<r[-1])
    return out,r,z,q

def checkpoint(tag,arrays,meta):
    for k,a in arrays.items():assert isinstance(a,np.ndarray) and a.dtype.kind in 'biufc',('non-numeric raw dtype',k,str(a.dtype))
    md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for k,a in arrays.items()}))
    text=encode(md).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p)
    rec=dict(file=p.name,sha256=CREATED[p.name],metadata=md)
    cs=json_file(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=cs);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,a in arrays.items():assert np.array_equal(z[k],a,equal_nan=True)
    return rec

def recheck(strict=True):
    assert sha(__file__)==OWNER['source_sha256']
    for n,h in INPUTS.items():assert sha(path(n))==h,('input seal',n)
    for n,h in CREATED.items():assert sha(BASE/n)==h,('own seal',n)
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads(path(STEM+'_OWNER_START.json').read_text())==OWNER
    if strict:
        assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
        assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}
    for rec in RECORDS:
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(path(rec['file']),allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for n,s in rec['metadata']['schema'].items():
                a=z[n];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))

def check(name,a,b):
    a=np.asarray(a);b=np.asarray(b);i=len(CHECKS);CONTEXT.update(control=name,control_ordinal=i)
    RAW[f'control_{i:02d}_{name}_actual']=a.copy();RAW[f'control_{i:02d}_{name}_expected']=b.copy()
    assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    gap=float(np.linalg.norm(a-b));env=max(1e-30,float(np.linalg.norm(a)),float(np.linalg.norm(b)));e=gap/env
    assert all(math.isfinite(v) for v in (gap,env,e))
    row=dict(name=name,error=e,absolute_gap=gap,envelope=env,tolerance=TOL,passed=e<=TOL);CHECKS.append(row);return row

def local_curvature(x,r,q,w,xi):
    CONTEXT.update(stage='Q1_value_interpolation')
    idx=np.searchsorted(r,q,side='right')-1;RAW['sample_cell_index']=idx
    frac=(q-r[idx])/(r[idx+1]-r[idx]);RAW['sample_cell_fraction']=frac
    samples=(1-frac)[None,:]*x[:,idx,0]+frac[None,:]*x[:,idx+1,0];RAW['Q1_sampled_fields']=samples
    independent=np.array([np.interp(q,r,a[:,0]) for a in x]);RAW['independent_value_samples']=independent
    check('continuous_Q1_values',samples,independent)
    u=np.stack((samples[1::2],samples[2::2]),axis=-1)/np.sqrt(w)[:,None,None];RAW['unweighted_u']=u
    phi=B*samples[0];RAW['conditional_Phi']=phi
    lapse=np.exp(phi);RAW['aligned_lapse']=lapse
    zscaled=B*u;RAW['physical_scaled_covectors_L0z']=zscaled
    kscaled=(B*GC)**2*xi**4;RAW['physical_scaled_k_L0sq']=kscaled
    flat=np.sum(u*u,axis=-1)/(GC**2*xi[:,None]**4);RAW['flat_ratio']=flat
    metric=np.exp(2*phi);RAW['conditional_inverse_metric_factor']=metric
    proper=metric[None,:]*np.sum(zscaled*zscaled,axis=-1)/kscaled[:,None];RAW['conditional_proper_ratio']=proper
    canceled=metric[None,:]*flat;check('physical_invariant_unit_cancellation',proper,canceled)
    kappa=np.stack((1+proper,1+3*proper),axis=-1);RAW['local_curvatures']=kappa
    check('parallel_minus_transverse',kappa[...,1]-kappa[...,0],2*proper)
    assert np.all(np.isfinite(lapse)) and np.all(lapse>0) and np.all(np.isfinite(kappa)) and np.all(kappa>=1)
    return dict(Q1_sampled_fields=samples,unweighted_u=u,conditional_Phi=phi,aligned_lapse=lapse,physical_scaled_covectors_L0z=zscaled,physical_scaled_k_L0sq=kscaled,flat_ratio=flat,conditional_proper_ratio=proper,local_curvatures=kappa,sample_cell_index=idx,sample_cell_fraction=frac)

def rate_arm(sigma,curv,xi,hstar):
    CONTEXT.update(stage='local_rates',sigma=sigma)
    omega=sigma*xi*hstar;RAW['bare_proper_omega_rad_per_second']=omega
    proper=omega[:,None,None]*np.sqrt(curv['local_curvatures']);RAW['proper_Omega_rad_per_second']=proper
    inverse=1/proper;RAW['proper_inverse_angular_rate_seconds']=inverse
    period=2*math.pi*inverse;RAW['proper_period_seconds']=period
    coord=curv['aligned_lapse'][None,:,None]*proper;RAW['coordinate_Omega_rad_per_second']=coord
    coordinate_period=period/curv['aligned_lapse'][None,:,None];RAW['coordinate_period_seconds']=coordinate_period
    dimensionless=proper/hstar;RAW['proper_Omega_over_Hstar']=dimensionless
    dimensionless_period=period*hstar;RAW['proper_period_in_Hstar_inverse']=dimensionless_period
    actual=np.stack((proper*period/(2*math.pi),coord*coordinate_period/(2*math.pi),coord/proper),axis=0)
    expected=np.stack((np.ones_like(proper),np.ones_like(proper),np.broadcast_to(curv['aligned_lapse'][None,:,None],proper.shape)),axis=0)
    check('sigma_'+str(sigma)+'_proper_and_coordinate_periods',actual,expected)
    for n,a in list(RAW.items()):assert np.all(np.isfinite(a)),('nonfinite rate operand',n)
    assert np.all(proper>0) and np.all(coord>0)
    return {k:v.copy() for k,v in RAW.items()}

def main():
    global np,OWNER,INPUTS
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
    assert args.root_run and not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64,'Author guard: root review/seal required.'
    assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace; no automatic replay.'
    INPUTS,case,parent=authenticate();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__));arms=[]
    try:
        json_file(STEM+'_OWNER_START.json',OWNER)
        json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_final_file=parent['file'],parent_final_sha256=parent['sha256'],parent_case_file=PARENT+'_FINE_Q3_CASE.json',sigmas=SIGMAS,radii_count=43,modes=32,qualification=FLAGS))
        import numpy as _np
        np=_np
        inputs,r,z,q=load_input(parent,case)
        checkpoint('INPUT',dict(**inputs,r_kpc=r,z_kpc=z,official_radii_kpc=q),dict(kind='authentic_closed_FINE_Q3_input',parent_file=parent['file'],parent_sha256=parent['sha256'],parent_commit_sha256=parent['commit_sha256']))
        RAW.clear();curv=local_curvature(inputs['final_state'],r,q,inputs['current_weights'],inputs['current_xi'])
        hstar=HUNIT*1000/(1000*L0);RAW['Hstar_SI']=np.array(hstar)
        check('Hstar_SI_unit_conversion',np.array(hstar),np.array(HUNIT/L0))
        curvature=checkpoint('LOCAL_CURVATURE',dict(curv,**{k:v for k,v in RAW.items() if k.startswith('control_')},Hstar_SI=np.array(hstar)),dict(kind='conditional_local_q_zero_curvatures',controls=list(CHECKS),component_order=['transverse','parallel'],field_axis_order=['mode','radius','component'],metric='conditional_exp_minus_2Phi_flat',Hunit=HUNIT))
        for sigma in SIGMAS:
            RAW.clear();start=len(CHECKS);arrays=rate_arm(sigma,curv,inputs['current_xi'],hstar)
            rec=checkpoint('SIGMA_'+str(sigma),arrays,dict(kind='declared_local_temporal_benchmark',sigma=sigma,controls=CHECKS[start:],curvature_file=curvature['file'],curvature_sha256=curvature['sha256']))
            arms.append(dict(sigma=sigma,status='LOCAL_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS[start:]) else 'ARITHMETIC_FAILED',checkpoint=rec,proper_rate_min=float(arrays['proper_Omega_rad_per_second'].min()),proper_rate_max=float(arrays['proper_Omega_rad_per_second'].max()),proper_period_min_seconds=float(arrays['proper_period_seconds'].min()),proper_period_max_seconds=float(arrays['proper_period_seconds'].max()),qualification=FLAGS))
        assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==6
        status='LOCAL_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS) else 'ARITHMETIC_FAILED'
        result=dict(owner=OWNER,status=status,controls=CHECKS,expected_control_census=CONTROL_COUNT,checkpoints=RECORDS,arms=arms,parent_reference=dict(case_file=PARENT+'_FINE_Q3_CASE.json',case_sha256=INPUTS[PARENT+'_FINE_Q3_CASE.json'],final_file=parent['file'],final_sha256=parent['sha256']),copied_parent_controls=case['controls'],copied_source_controls=case['source_controls_copied'],copied_historical_native_controls=case['historical_native_controls'],copied_parent_physical_flags=case['physical_flags'],copied_parent_status=case['status'],copied_historical_status=case['historical_status'],unknown_registration={k:None for k in ('actual_full_metric','physical_native_inertia','convective_generator','Cauchy_state','assembly_history','physical_exterior')},qualification=FLAGS)
        recheck();rh=json_file(STEM+'_RESULT.json',result)
        publish(STEM+'_REPORT.md',('# '+STEM+'\n\n'+status+'. Saved local q=0 curvature inventory only: all43 radii,32 modes and4 declared sigma arms.\n\nLocal rates are neither global retarded response nor physical formation/history or stability. No source, spectrum or preparation was selected.\n').encode());recheck()
        rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,qualification=FLAGS)
        json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==rc
        print(json.dumps(dict(status=status,controls=len(CHECKS),pairs=len(RECORDS),result_sha256=rh),sort_keys=True));return 0 if status=='LOCAL_ARITHMETIC_PASS' else 3
    except BaseException:
        failure=traceback.format_exc();raw_failure=None;prior=path(STEM+'_RECEIPT.json');prior_sha=sha(prior) if prior.exists() else None
        try:
            if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_available_local_operands',context=CONTEXT,traceback=failure))
        except BaseException:raw_failure=traceback.format_exc()
        seal_created();recheck(strict=False)
        unpaired=sorted(({p.name for p in BASE.glob(STEM+'_*.npz')}|{p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}) - {r['file'] for r in RECORDS}-{r['commit_file'] for r in RECORDS})
        eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,failed=now(),context=CONTEXT,traceback=failure,raw_preservation_traceback=raw_failure,unqualified_partial_pair_files=unpaired,checkpoints=RECORDS,completed_arms=arms,controls=CHECKS,preserved_outputs=dict(CREATED),existing_receipt_sha256=prior_sha,qualification=FLAGS))
        if prior_sha is None:
            rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,qualification=FLAGS)
            json_file(STEM+'_RECEIPT.json',rc);recheck(strict=False);assert json.loads(prior.read_text())==rc
        else:recheck(strict=False);assert sha(prior)==prior_sha
        raise

if __name__=='__main__':raise SystemExit(main())
