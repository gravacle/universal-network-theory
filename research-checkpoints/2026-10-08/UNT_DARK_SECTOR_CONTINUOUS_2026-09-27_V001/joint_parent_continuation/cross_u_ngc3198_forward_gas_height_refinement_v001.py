"""Guarded additive gas-height refinement; completed parent fields are not rerun."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, time, traceback
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_FORWARD_GAS_HEIGHT_REFINEMENT_V001'
PARENT='CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001'
AUTHOR_DRAFT=False
PROTOCOL_SHA='75c14eefdb2018d01be947d09441c2469ac63d6ee4786ade0f0f8c394dc734c1'
ORDERS=(48,96)
HEIGHT_TOL=1e-3
CREATED={};PAIRS=[];AVAILABLE={};np=None
PINS={'cross_u_ngc3198_forward_gas_template_v001.py': '9d01ef2e5e0e8cf33b144ce0143a38b5aba369793df562df9aa933a34877b53a', 'CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001.md': '64688082ea86791c5cda4884f30caaa048eac0554737c35bcc020ae5f6d76214', 'CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001_RESULT.json': 'd79972b39a2fb72c645423904762d0430c9585cb76c56dbb1315bf964c438ae2', 'CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001_RECEIPT.json': 'a876b479756897aa33f4f15dfaca3c3d4d2afb32821afd0320710c44bc7f714d', 'CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001_MANIFEST.json': 'd31daf16bdb77f932db86d11b09ef310d7b107f615ae67246f44c148d0177bf3'}
TARGETS=('HI0_H20_R0.64', 'HI0_H20_R2.57', 'HI0_H20_R2.89', 'HI0_H20_R3.21', 'HI0_H20_R3.54', 'HI0_H20_R6.43', 'HI0_H20_R6.74', 'HI0_H20_R7.06', 'HI0_H21_R0.64', 'HI0_H21_R2.57', 'HI0_H21_R2.89', 'HI0_H21_R3.21', 'HI0_H21_R3.54', 'HI1_H20_R0.64', 'HI1_H20_R2.57', 'HI1_H20_R2.89', 'HI1_H20_R3.21', 'HI1_H20_R3.54', 'HI1_H20_R6.43', 'HI1_H20_R6.74', 'HI1_H20_R7.06', 'HI1_H21_R0.64', 'HI1_H21_R2.57', 'HI1_H21_R2.89', 'HI1_H21_R3.21', 'HI1_H21_R3.54')
FLAGS={'continuum_error_bound_qualified': False, 'full_SPARC_model_qualified': False, 'full_metric_qualified': False, 'joint_superiority_qualified': False, 'nonlinear_response_qualified': False, 'observational_qualified': False, 'source_registration_qualified': False, 'thickness_qualified': False, 'warp_qualified': False}
def now():return datetime.now(timezone.utc).isoformat()

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def canonical(o):
    if isinstance(o,float) and not math.isfinite(o):return dict(nonfinite_float=repr(o))
    if isinstance(o,dict):return {k:canonical(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [canonical(v) for v in o]
    return o

def encode(o):return json.dumps(canonical(o),sort_keys=True,separators=(',',':'),allow_nan=False)

def finite(v):return float(v) if math.isfinite(float(v)) else None

def authenticate():
    assert not AUTHOR_DRAFT and PINS and PROTOCOL_SHA!='PENDING','Guarded unexecuted author draft'
    for n,h in PINS.items():assert sha(BASE/n)==h,('changed input',n)
    assert sha(BASE/(STEM+'.md'))==PROTOCOL_SHA

def publish(name,o):
    raw=(encode(o)+'\n').encode();p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[name]=sha(p);assert p.read_bytes()==raw;return CREATED[name]

def freeze_actual_files():
    for p in sorted(BASE.glob(STEM+'_*')):
        if p.is_file():p.chmod(0o444);CREATED[p.name]=sha(p)
    return dict(CREATED)

def checkpoint(label,meta,arrays):
    meta=dict(meta,owner=OWNER,manifest_sha256=MANIFEST_SHA,source_sha256=SOURCE)
    meta['schema']={n:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for n,a in arrays.items()}
    text=encode(meta);meta=json.loads(text);name=f'{STEM}_{len(PAIRS):03d}_{label}.npz';p=BASE/name
    with p.open('xb') as f:np.savez_compressed(f,__metadata__=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[name]=sha(p)
    cn=name+'.COMMIT.json';ch=publish(cn,dict(status='COMMITTED',file=name,sha256=CREATED[name],metadata=meta))
    rec=dict(file=name,sha256=CREATED[name],commit_file=cn,commit_sha256=ch,metadata=meta);PAIRS.append(rec)
    reread(rec);return rec

def reread(rec):
    assert sha(BASE/rec['file'])==rec['sha256'] and sha(BASE/rec['commit_file'])==rec['commit_sha256']
    c=json.loads((BASE/rec['commit_file']).read_text())
    assert c==dict(status='COMMITTED',file=rec['file'],sha256=rec['sha256'],metadata=rec['metadata'])
    with np.load(BASE/rec['file'],allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'__metadata__'}
        assert json.loads(str(z['__metadata__']))==rec['metadata']
        for n,d in rec['metadata']['schema'].items():
            a=z[n];assert list(a.shape)==d['shape'] and str(a.dtype)==d['dtype'] and bool(np.all(np.isfinite(a)))==d['finite']

def check(checks,raw,name,actual,expected,tol,envelope=None):
    i=len(checks);a=np.asarray(actual,dtype=float);b=np.asarray(expected,dtype=float)
    raw[f'{i:04d}_actual']=a.copy();raw[f'{i:04d}_expected']=b.copy()
    assert a.shape==b.shape
    env=max(1.,float(np.max(abs(b)))) if envelope is None else float(envelope)
    gap=float(np.max(abs(a-b)));error=gap/env if math.isfinite(env) and env>0 else math.inf
    t=dict(name=name,absolute_gap=finite(gap),envelope=finite(env),error=finite(error),tolerance=tol,
           passed=bool(math.isfinite(error) and error<=tol));checks.append(t);return t
def parent():
    receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    assert receipt['status']=='NUMERICAL_FAILURES_RETAINED' and receipt['owner']['owner']=='root' and receipt['owner']['pid']==86353
    assert datetime.fromisoformat(receipt['closed'])>datetime.fromisoformat(receipt['owner']['started'])
    assert len(receipt['input_sha256'])==25 and len(receipt['output_sha256'])==349 and receipt['checkpoint_pairs']==173
    bindings=dict(PINS)
    for mapping in (receipt['input_sha256'],receipt['output_sha256']):
        for n,h in mapping.items():
            assert n not in bindings or bindings[n]==h,('conflicting parent binding',n)
            bindings[n]=h;assert sha(BASE/n)==h,('changed parent file',n)
    data=json.loads((BASE/(PARENT+'_RESULT.json')).read_text())
    assert data['status']==receipt['status'] and data['physical_flags']==FLAGS and not any(FLAGS.values())
    assert data['manifest']==json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    assert data['manifest']['owner']==receipt['owner'] and data['manifest']['input_sha256']==receipt['input_sha256']
    assert receipt['result_sha256']==sha(BASE/(PARENT+'_RESULT.json')) and len(data['cases'])==172
    checks=data['implementation']['controls']+[x for c in data['cases'] for x in c['controls']]
    assert len(checks)==4167 and sum(x['passed'] for x in checks)==4115
    assert all(x['passed'] for x in data['implementation']['controls']) and len(data['implementation']['controls'])==39
    selected=[c for c in data['cases'] if any(not x['passed'] for x in c['controls'])]
    assert tuple(c['case'] for c in selected)==TARGETS and len(selected)==26
    assert all(c['status']=='NUMERICAL_FAILURES_RETAINED' and c['physical_flags']==FLAGS for c in selected)
    assert all(x['name'].startswith('height_') for c in selected for x in c['controls'] if not x['passed'])
    assert len(data['legacy397_controls_copied_exactly'])==397 and all(x['passed'] for x in data['legacy397_controls_copied_exactly'])
    for c in selected:
        assert len(c['heights'])==3 and len(c['controls'])==24 and len(c['variants'])==2
        cp=c['checkpoint'];assert all(receipt['output_sha256'][cp[k]]==cp[h] for k,h in [('file','sha256'),('commit_file','commit_sha256')])
        commit=json.loads((BASE/cp['commit_file']).read_text())
        assert commit==dict(status='COMMITTED',file=cp['file'],sha256=cp['sha256'],metadata=cp['metadata'])
        assert cp['metadata']['owner']==receipt['owner'] and cp['metadata']['manifest_sha256']==sha(BASE/(PARENT+'_MANIFEST.json'))
        assert cp['metadata']['source_sha256']==receipt['owner']['source_sha256'] and cp['metadata']['case']==c['case']
        assert cp['metadata']['result']=={k:v for k,v in c.items() if k!='checkpoint'}
    return data,receipt,selected,bindings
def one_case(ring,density,old):
    raw={};checks=[];context=dict(case=old['case'],R_kpc=old['R_kpc'],hi_tail=old['hi_tail'],h2_tail=old['h2_tail'],
        parent_checkpoint={k:v for k,v in old['checkpoint'].items() if k!='metadata'},physical_flags=FLAGS)
    AVAILABLE.update(context=context,arrays=raw,checks=checks)
    reread(old['checkpoint'])
    with np.load(BASE/old['checkpoint']['file'],allow_pickle=False) as z:
        for n in old['checkpoint']['metadata']['schema']:raw['parent__'+n]=z[n].copy()
    for iz,record in enumerate(old['heights']):
        for order in ORDERS:
            for k in ('HI_He','H2_He'):
                v=record['orders'][str(order)]['components'][k]
                assert np.array_equal(raw[f'parent__h{iz}_o{order}_{k}'],np.asarray([v['potential_kms2'],v['gR_kms2_per_kpc'],v['quadrature_mass_Msun'],v['omitted_mass_Msun']]))
    added=[];heights=[old['heights'][-1]['z_kpc']/2**i for i in (1,2,3)];raw['added_heights_kpc']=np.asarray(heights)
    allprofiles=density.profiles(old['hi_tail'],old['h2_tail']);p={k:allprofiles[k] for k in ('HI_He','H2_He')}
    for k,v in p.items():
        assert np.array_equal(v.r,raw['parent__'+k+'_r']) and np.array_equal(v.s,raw['parent__'+k+'_surface'])
    R=old['R_kpc'];cutoff=old['cutoff_kpc'];masses=old['masses_Msun'];assert ring.source_cutoff(p)==cutoff
    context.update(cutoff_kpc=cutoff,masses_Msun=masses)
    try:
        for j,z in enumerate(heights,start=3):
            oo={}
            for order in ORDERS:
                context.update(current_height_index=j,current_order=order)
                f=ring.field(R,z,p,order);oo[str(order)]=f
                for k,v in f['components'].items():
                    raw[f'h{j}_o{order}_{k}']=np.asarray([v['potential_kms2'],v['gR_kms2_per_kpc'],v['quadrature_mass_Msun'],v['omitted_mass_Msun']])
            added.append(dict(z_kpc=z,orders=oo))
            for key in ('gR_kms2_per_kpc','potential_kms2'):
                check(checks,raw,f'total_order_{j}_{key}',oo['48'][key],oo['96'][key],1e-8)
            for k in p:
                a=oo['48']['components'][k];b=oo['96']['components'][k]
                check(checks,raw,f'component_force_order_{j}_{k}',a['gR_kms2_per_kpc'],b['gR_kms2_per_kpc'],1e-8)
                check(checks,raw,f'component_mass_{j}_{k}',b['quadrature_mass_Msun']+b['omitted_mass_Msun'],masses[k],1e-9,envelope=masses[k])
        whole=old['heights']+added;allheights=[h['z_kpc'] for h in whole]
        raw['six_heights_kpc']=np.asarray(allheights);extrap={};slopes={};corrected={};tails={};lastchecks=[]
        for k in ('HI_He','H2_He','TOTAL_GAS'):
            values=[h['orders']['96']['gR_kms2_per_kpc'] if k=='TOTAL_GAS' else h['orders']['96']['components'][k]['gR_kms2_per_kpc'] for h in whole]
            raw[k+'_six_height_force']=np.asarray(values)
            if not np.array_equal(raw[k+'_six_height_force'][:3],raw['parent__'+k+'_finite_height_force']):raise RuntimeError('Old height operands changed')
            extrap[k]=[2*values[i+1]-values[i] for i in range(5)]
            if extrap[k][:2]!=old['extrapolated_gR'][k]:raise RuntimeError('Old extrapolants changed')
            for i in (1,2,3):
                t=check(checks,raw,f'height_{k}_extrap{i}_to{i+1}',extrap[k][i],extrap[k][i+1],HEIGHT_TOL)
                if i==3:lastchecks.append(t)
            subset=p if k=='TOTAL_GAS' else {k:p[k]}
            slopes[k]=old['slope_dgR_dz'][k]
            corrected[k]=[v-slopes[k]*z for v,z in zip(values,allheights)]
            if corrected[k][:3]!=old['slope_corrected_gR'][k]:raise RuntimeError('Old slope diagnostics changed')
            omitted=sum(whole[-1]['orders']['96']['components'][q]['omitted_mass_Msun'] for q in subset)
            tails[k]=ring.G*omitted/(cutoff-R)**2
            check(checks,raw,'tail_'+k,tails[k],0.,1e-10,envelope=max(1.,abs(extrap[k][-1])))
        if len(checks)!=30:raise RuntimeError('New control census changed')
        template=old['variants'][0]['published_signed_vgas_squared'];variants=[]
        for helium in (1.36,1.33):
            ratio=helium/1.36;hi=[ratio*v for v in extrap['HI_He']];h2=extrap['H2_He'];total=[a+b for a,b in zip(hi,h2)]
            value=R*hi[-1]
            variants.append(dict(helium=helium,linear_ratio=ratio,HI_extrapolated_gR=hi,H2_extrapolated_gR=h2,total_gas_extrapolated_gR=total,
                published_Vgas_kms=old['variants'][0]['published_Vgas_kms'],published_signed_vgas_squared=template,
                HI_signed_vgas_squared=value,signed_template_difference_kms2=value-template,
                HI_mass_Msun=ratio*masses['HI_He'],H2_mass_Msun=masses['H2_He']))
        result=dict(context,status='NEW_NUMERICAL_CONTROLS_PASS' if all(x['passed'] for x in checks) else 'NEW_NUMERICAL_FAILURES_RETAINED',
            old_status_copied_exactly=old['status'],old_controls_copied_exactly=old['controls'],old_variants_copied_exactly=old['variants'],
            old_heights_copied_exactly=old['heights'],added_heights=added,six_heights=whole,extrapolated_gR=extrap,
            slope_dgR_dz_copied_exactly=slopes,slope_corrected_gR=corrected,tail_force_bounds=tails,
            finest_height_arithmetic_pass=all(t['passed'] for t in lastchecks),variants=variants,controls=checks,agreement_gate=None)
    except (ArithmeticError,ValueError,AssertionError) as e:
        result=dict(context,status='NUMERICAL_REFUSAL_RETAINED',exception=type(e).__name__,reason=str(e),traceback=traceback.format_exc(),
            old_status_copied_exactly=old['status'],old_controls_copied_exactly=old['controls'],old_variants_copied_exactly=old['variants'],
            old_heights_copied_exactly=old['heights'],completed_added_heights=added,controls=checks,agreement_gate=None)
    cp=checkpoint(old['case'],dict(context,result=result),raw);result['checkpoint']=cp;return result
def close(status,data,cases):
    authenticate();assert sha(__file__)==SOURCE
    for n,h in PARENT_BINDINGS.items():assert sha(BASE/n)==h
    for p in PAIRS:reread(p)
    result=dict(status=status,manifest=MANIFEST,legacy397_controls_copied_exactly=data['legacy397_controls_copied_exactly'],
        parent39_implementation_controls_copied_exactly=data['implementation']['controls'],
        all172_original_dispositions_copied_exactly=[dict(case=c['case'],status=c['status'],controls=c['controls'],variants=c['variants']) for c in data['cases']],
        original_failed_height_controls_remain_failed=True,cases=cases,physical_flags=FLAGS,agreement_gate=None,automatic_followup=False)
    rh=publish(STEM+'_RESULT.json',result);report=f'{status}: {len(cases)}/26 additive gas-height cases; all original failures retained.\n'
    p=BASE/(STEM+'_REPORT.txt')
    with p.open('xb') as f:f.write(report.encode());f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);assert p.read_bytes()==report.encode()
    for n,h in CREATED.items():assert sha(BASE/n)==h
    publish(STEM+'_RECEIPT.json',dict(status=status,owner=OWNER,closed=now(),elapsed_seconds=time.monotonic()-T0,input_sha256=INPUTS,
        output_sha256=dict(CREATED),result_sha256=rh,checkpoint_pairs=len(PAIRS),physical_flags=FLAGS))
    for n,h in CREATED.items():assert sha(BASE/n)==h
    authenticate();assert sha(__file__)==SOURCE
    for n,h in PARENT_BINDINGS.items():assert sha(BASE/n)==h
def main():
    global np,OWNER,SOURCE,INPUTS,MANIFEST,MANIFEST_SHA,T0,PARENT_BINDINGS
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');args=parser.parse_args()
    assert args.run,'Explicit root-owned --run required';authenticate();assert not list(BASE.glob(STEM+'_*')),'Existing namespace preserved'
    data,receipt,selected,PARENT_BINDINGS=parent();SOURCE=sha(__file__)
    INPUTS={**PARENT_BINDINGS,STEM+'.md':PROTOCOL_SHA,Path(__file__).name:SOURCE}
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=SOURCE,started=now());T0=time.monotonic()
    MANIFEST=dict(owner=OWNER,input_sha256=INPUTS,parent_receipt=PINS[PARENT+'_RECEIPT.json'],targets=list(TARGETS),
        refinement='Append z0/8,z0/16,z0/32 only; old three heights reused without field calls',orders=list(ORDERS),
        expected_new_field_calls=156,expected_new_controls=780,expected_pairs=26,physical_flags=FLAGS)
    cases=[]
    try:
        MANIFEST_SHA=publish(STEM+'_MANIFEST.json',MANIFEST)
        for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
        import numpy as numpy_module
        np=numpy_module
        import galaxy_ring_oracle as ring
        import galaxy_density as density
        for n,h in PARENT_BINDINGS.items():assert sha(BASE/n)==h
        assert ring.G==data['manifest']['calibration']['G_kpc_kms2_Msun'] and density.DISTANCE_MPC==13.8
        for c in selected:cases.append(one_case(ring,density,c))
        assert len(cases)==26
        complete=all(c['status']!='NUMERICAL_REFUSAL_RETAINED' for c in cases)
        checks=[t for c in cases for t in c['controls']]
        if complete:assert len(checks)==780
        good=complete and all(t['passed'] for t in checks)
        status='ADDITIVE_NUMERICAL_CONTROLS_PASS' if good else 'ADDITIVE_NUMERICAL_FAILURES_RETAINED'
        close(status,data,cases);print(status,flush=True);return 0 if good else 3
    except Exception:
        tb=traceback.format_exc();rawcp=None;raw_error=None
        if np is not None and AVAILABLE.get('arrays'):
            try:rawcp=checkpoint('ERROR_RAW',dict(context=AVAILABLE.get('context'),controls=AVAILABLE.get('checks'),traceback=tb),AVAILABLE['arrays'])
            except Exception:raw_error=traceback.format_exc()
        preserved=freeze_actual_files();receipt=BASE/(STEM+'_RECEIPT.json')
        existing=sha(receipt) if receipt.exists() else None;name=STEM+('_POSTRECEIPT_ERROR.json' if existing else '_ERROR.json')
        try:
            publish(name,dict(status='ERROR',owner=OWNER,traceback=tb,raw_checkpoint=rawcp,existing_receipt_sha256=existing,
                raw_checkpoint_publication_error=raw_error,completed_cases=cases,preserved_output_sha256=preserved,physical_flags=FLAGS))
            if not receipt.exists():publish(STEM+'_RECEIPT.json',dict(status='ERROR',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),physical_flags=FLAGS))
        finally:freeze_actual_files()
        for n,h in CREATED.items():assert sha(BASE/n)==h
        raise
if __name__=='__main__':raise SystemExit(main())
