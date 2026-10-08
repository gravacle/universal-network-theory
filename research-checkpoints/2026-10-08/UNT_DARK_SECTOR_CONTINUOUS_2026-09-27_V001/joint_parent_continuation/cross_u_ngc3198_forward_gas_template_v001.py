"""Guarded forward Newtonian registration of the existing measured gas source."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, time, traceback
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001'
AUTHOR_DRAFT=False
PROTOCOL_SHA='64688082ea86791c5cda4884f30caaa048eac0554737c35bcc020ae5f6d76214'
PINS={'GALAXY_SOURCE_PREFLIGHT.md': 'c83b77c5521c2e138caf9ba9dc533186dd4033047272f5e81ccf007295c44b1a', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'OUTER_GAS_INPUT_DECISION.md': 'b45a72c3b2f0067aae71efe25e92f1a3340f99a666ae708d757a3b7ccbe119be', 'RING_ORACLE_FROZEN.json': '2942e7f9a01b68b44cc2c3138ae1e1c1d2fdb977af837bfa1ef77894d6d36ddb', 'RING_ORACLE_PROTOCOL.md': 'c332385e30e01e14705d5e89cf5d54886dc44956a6dd2adcbf0ead9ca4f61c2f', 'RING_ORACLE_RESULT.md': '3eed757fb736e98f1fbeb12d73973ae8e045ccea4f6bdde3ba72584fbae7ac38', 'RING_ORACLE_RESULTS.json': '0d296b8e2025051b407f7cc4af17b203d01e17fd2d509941c99e9d6fecd3441f', 'begeman1989_original.pdf': '7745f7e83d2e31f90f493fa6c35b8e090c344b4dbdf83bc3bb206bde2899420c', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'galaxy_ring_oracle.py': 'a06f393df8246a97e70dea04af059408be5447ba6e6199ad5206aff2271ea250', 'leroy2008_ReadMe.html': 'cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48', 'leroy2008_table4.dat': '938104d0289f93f9fed0843028555e92f63a61889d623ee5b5f132e9d6ea1f44', 'leroy2008_table7.dat': '43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99', 'prepare_galaxy_input.py': '62a6f8d10bd155c201721d7fefe1f85134f30b183d7f6307774a6f5082b98fce', 'sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf': '87fa39590a0cded15e6dc7a51355fa2354eea8a130f477b92e4cee15c4e36a19', 'sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf.SOURCE.json': '0413b81940409e9bba28c4956b1683259084b3b4f227f50868725ce263a850f4', 'sparc_official_massmodels_2026-10-06_v001.mrt': '9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c', 'sparc_official_massmodels_2026-10-06_v001.mrt.SOURCE.json': '2c9b80c5bd6afefab410ce860853811785e4cb3fe24dd54ed0cb71ba5c2a1e20', 'sparc_official_sample_2026-10-06_v001.mrt': '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243', 'sparc_official_sample_2026-10-06_v001.mrt.SOURCE.json': 'bacfd875aa818b3e74712009da6e18b36e4941bebe4e2c576358aa5620512a88', 'reviewed_cross_u_ngc3198_forward_gas_template_v001_235.py': '6e5b552d30e5056644295368bef29feffa1750bccef7e057ea26b43cbee5ef54', 'reviewed_CROSS_U_NGC3198_FORWARD_GAS_TEMPLATE_V001_21.md': '4893409cf2b75bb78e01109d0821a3d05e0837d21b6e989a35f9fb024146faca'}
ORDERS=(48,96)
HEIGHT_TOL=1e-3
FLAGS=dict(source_registration_qualified=False,full_SPARC_model_qualified=False,
           thickness_qualified=False,warp_qualified=False,observational_qualified=False,
           nonlinear_response_qualified=False,full_metric_qualified=False,
           continuum_error_bound_qualified=False,joint_superiority_qualified=False)
CREATED={}; PAIRS=[]; AVAILABLE={}; np=None
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
def closed_legacy():
    freeze=json.loads((BASE/'RING_ORACLE_FROZEN.json').read_text())
    for n,h in freeze['files'].items():assert sha(BASE/n)==h
    old=json.loads((BASE/'RING_ORACLE_RESULTS.json').read_text())
    assert old['freeze_sha256']==sha(BASE/'RING_ORACLE_FROZEN.json')
    assert hashlib.sha256(encode(old['payload']).encode()).hexdigest()==old['payload_sha256']
    assert old['payload']['status']=='COMPLETE' and len(old['payload']['checks'])==397 and not old['payload']['failed_checks']
    assert all(t['passed'] for t in old['payload']['checks']) and len(old['payload']['cases'])==20
    doc=json.loads((BASE/'sparc_official_massmodels_2026-10-06_v001.mrt.SOURCE.json').read_text())
    assert doc['sha256']==sha(BASE/'sparc_official_massmodels_2026-10-06_v001.mrt')
    raw=(BASE/'sparc_official_massmodels_2026-10-06_v001.mrt').read_text()
    assert 'Vgas includes a factor 1.33' in raw
    rows=[]
    for line in raw.splitlines():
        v=line.split()
        if v and v[0]=='NGC3198':
            assert len(v)==10 and float(v[1])==13.8
            rows.append(dict(R_kpc=float(v[2]),Vgas_kms=float(v[5])))
    assert len(rows)==43 and all(math.isfinite(x[k]) for x in rows for k in x)
    assert all(a['R_kpc']<b['R_kpc'] for a,b in zip(rows,rows[1:])) and rows[0]['R_kpc']>0
    return old,rows
def check(checks,raw,name,actual,expected,tol,envelope=None):
    i=len(checks);a=np.asarray(actual,dtype=float);b=np.asarray(expected,dtype=float)
    raw[f'{i:04d}_actual']=a.copy();raw[f'{i:04d}_expected']=b.copy()
    assert a.shape==b.shape
    env=max(1.,float(np.max(abs(b)))) if envelope is None else float(envelope)
    gap=float(np.max(abs(a-b)));error=gap/env if math.isfinite(env) and env>0 else math.inf
    t=dict(name=name,absolute_gap=finite(gap),envelope=finite(env),error=finite(error),tolerance=tol,
           passed=bool(math.isfinite(error) and error<=tol));checks.append(t);return t
def implementation(ring):
    checks=[];raw={};context=dict(kind='prospective_kernel_normalization',physical_flags=FLAGS)
    AVAILABLE.update(context=context,arrays=raw,checks=checks)
    x,w=np.polynomial.legendre.leggauss(256);theta=(x+1)*math.pi/4;weights=w*math.pi/4
    for k in (0.,.2,.7,.99):
        values=ring.elliptic(math.sqrt((1-k)*(1+k)));q=np.sqrt(1-k*k*np.sin(theta)**2)
        for i,ref in enumerate((np.dot(weights,1/q),np.dot(weights,q))):check(checks,raw,f'elliptic_{k}_{i}',values[i],ref,1e-11)
    for R,a,z in ((2.,1.,.4),(1.,2.,.4),(2.,2.,.4),(8.,3.,.5),(3.,8.,.5)):
        values=ring.ring_kernels(R,z,a);direct={}
        for order in (128,256):
            x,w=np.polynomial.legendre.leggauss(order);t=(x+1)*math.pi/2;ww=w*math.pi
            d=np.sqrt(R*R+a*a+z*z-2*R*a*np.cos(t))
            direct[order]=(np.dot(ww,-1/d),np.dot(ww,(R-a*np.cos(t))/d**3))
        for i in (0,1):
            check(checks,raw,f'ring_{R}_{a}_{z}_{i}',values[i],direct[256][i],2e-10)
            check(checks,raw,f'angular_{R}_{a}_{z}_{i}',direct[128][i],direct[256][i],2e-10)
        if (R,a)==(1.,2.):check(checks,raw,'outward_exterior_ring',float(values[1]<0),1.,0.)
    cutoff=1024.;knots=[0.,.25,.5,1.,2.,4.,8.,16.,32.,64.,128.,256.,512.,cutoff]
    omitted=1/math.sqrt(1+cutoff*cutoff)
    for R,z in ((.7,.2),(3.7,.2)):
        out={}
        for order in ORDERS:
            a,w=ring.radial_quadrature(R,z,knots,cutoff,order);shell=a/(2*math.pi*(1+a*a)**1.5)*w
            pk,fk=ring.ring_kernels(R,z,a);out[order]=(np.dot(shell,pk),np.dot(shell,fk),2*math.pi*np.sum(shell))
        for i in (0,1):check(checks,raw,f'kuzmin_order_{R}_{i}',out[48][i],out[96][i],1e-10)
        ep=-1/math.sqrt(R*R+(z+1)**2);eg=R/(R*R+(z+1)**2)**1.5
        check(checks,raw,f'kuzmin_potential_{R}',out[96][0],ep,omitted/(cutoff-R)+1e-10,envelope=1.)
        check(checks,raw,f'kuzmin_force_{R}',out[96][1],eg,omitted/(cutoff-R)**2+1e-10,envelope=1.)
        check(checks,raw,f'kuzmin_mass_{R}',out[96][2],1-omitted,1e-10,envelope=1.)
    assert len(checks)==39
    return checks,raw
def one_case(ring,density,row,hi_tail,h2_tail):
    R=row['R_kpc'];name=f'HI{int(hi_tail)}_H2{int(h2_tail)}_R{R:.2f}'
    checks=[];raw={};out=[];context=dict(case=name,R_kpc=R,hi_tail=hi_tail,h2_tail=h2_tail,physical_flags=FLAGS)
    AVAILABLE.update(context=context,arrays=raw,checks=checks)
    try:
        allprofiles=density.profiles(hi_tail,h2_tail);p={k:allprofiles[k] for k in ('HI_He','H2_He')}
        for k,v in p.items():raw[k+'_r']=v.r.copy();raw[k+'_surface']=v.s.copy()
        knots=ring.source_knots(p);raw['gas_knots']=knots.copy()
        distance=float(np.min(abs(knots-R)));assert distance>1e-10
        z0=min(.2,distance/4);heights=[z0/2**i for i in range(3)];raw['heights_kpc']=np.asarray(heights)
        masses=density.masses(p);cutoff=ring.source_cutoff(p);context.update(knots_distance_kpc=distance,cutoff_kpc=cutoff,masses_Msun=masses)
        for iz,z in enumerate(heights):
            oo={}
            for order in ORDERS:
                context.update(current_height_index=iz,current_order=order)
                f=ring.field(R,z,p,order);oo[str(order)]=f
                for k,v in f['components'].items():
                    raw[f'h{iz}_o{order}_{k}']=np.array([v['potential_kms2'],v['gR_kms2_per_kpc'],v['quadrature_mass_Msun'],v['omitted_mass_Msun']])
            out.append(dict(z_kpc=z,orders=oo))
            for key in ('gR_kms2_per_kpc','potential_kms2'):
                check(checks,raw,f'total_order_{iz}_{key}',oo['48'][key],oo['96'][key],1e-8)
            for k in p:
                a=oo['48']['components'][k];b=oo['96']['components'][k]
                check(checks,raw,f'component_force_order_{iz}_{k}',a['gR_kms2_per_kpc'],b['gR_kms2_per_kpc'],1e-8)
                check(checks,raw,f'component_mass_{iz}_{k}',b['quadrature_mass_Msun']+b['omitted_mass_Msun'],masses[k],1e-9,envelope=masses[k])
        extrap={};slope={};corrected={};tails={}
        for k in ('HI_He','H2_He','TOTAL_GAS'):
            values=[f['orders']['96']['gR_kms2_per_kpc'] if k=='TOTAL_GAS' else f['orders']['96']['components'][k]['gR_kms2_per_kpc'] for f in out]
            raw[k+'_finite_height_force']=np.asarray(values)
            extrap[k]=[2*values[i+1]-values[i] for i in (0,1)]
            check(checks,raw,'height_'+k,extrap[k][0],extrap[k][1],HEIGHT_TOL)
            subset=p if k=='TOTAL_GAS' else {k:p[k]};slope[k]=2*math.pi*ring.G*ring.surface_slope(R,subset)
            corrected[k]=[v-slope[k]*z for v,z in zip(values,heights)]
            omitted=sum(out[-1]['orders']['96']['components'][q]['omitted_mass_Msun'] for q in subset)
            tails[k]=ring.G*omitted/(cutoff-R)**2
            check(checks,raw,'tail_'+k,tails[k],0.,1e-10,envelope=max(1.,abs(extrap[k][1])))
        assert len(checks)==24
        signed_template=row['Vgas_kms']*abs(row['Vgas_kms']);raw['published_signed_vgas_squared']=np.array(signed_template)
        variants=[]
        for helium in (1.36,1.33):
            ratio=helium/1.36;hi=[ratio*v for v in extrap['HI_He']];h2=extrap['H2_He'];total=[a+b for a,b in zip(hi,h2)]
            values=R*hi[1];gap=values-signed_template
            variants.append(dict(helium=helium,linear_ratio=ratio,HI_extrapolated_gR=hi,H2_extrapolated_gR=h2,
                total_gas_extrapolated_gR=total,published_Vgas_kms=row['Vgas_kms'],published_signed_vgas_squared=signed_template,
                HI_signed_vgas_squared=values,signed_template_difference_kms2=gap,
                HI_mass_Msun=ratio*masses['HI_He'],H2_mass_Msun=masses['H2_He']))
        result=dict(context,status='NUMERICAL_CONTROLS_PASS' if all(x['passed'] for x in checks) else 'NUMERICAL_FAILURES_RETAINED',
            heights=out,extrapolated_gR=extrap,slope_dgR_dz=slope,slope_corrected_gR=corrected,tail_force_bounds=tails,
            variants=variants,controls=checks,agreement_gate=None)
    except (ArithmeticError,ValueError,AssertionError) as e:
        result=dict(context,status='NUMERICAL_REFUSAL_RETAINED',exception=type(e).__name__,reason=str(e),traceback=traceback.format_exc(),
                    completed_heights=out,controls=checks,agreement_gate=None)
    cp=checkpoint(name,dict(context,result=result),raw);result['checkpoint']=cp
    return result
def close(status,original,rows,implementation_record,cases):
    authenticate();assert sha(__file__)==SOURCE
    for p in PAIRS:reread(p)
    result=dict(status=status,manifest=MANIFEST,legacy397_controls_copied_exactly=original['payload']['checks'],
        old_qualification_scope='Twenty prior declared total-source interior checkpoints, not new radius qualification',
        published_gas_template=rows,implementation=implementation_record,cases=cases,physical_flags=FLAGS,
        agreement_gate=None,automatic_followup=False)
    rh=publish(STEM+'_RESULT.json',result)
    report=f'{status}: {len(cases)}/172 gas source/radius cases; no agreement or physical success gate.\n'
    p=BASE/(STEM+'_REPORT.txt')
    with p.open('xb') as f:f.write(report.encode());f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);assert p.read_bytes()==report.encode()
    for n,h in CREATED.items():assert sha(BASE/n)==h
    publish(STEM+'_RECEIPT.json',dict(status=status,owner=OWNER,closed=now(),elapsed_seconds=time.monotonic()-T0,
        input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,checkpoint_pairs=len(PAIRS),
        finite_cases=sum(c['status']!='NUMERICAL_REFUSAL_RETAINED' for c in cases),physical_flags=FLAGS))
    for n,h in CREATED.items():assert sha(BASE/n)==h
    authenticate();assert sha(__file__)==SOURCE
def main():
    global np,OWNER,SOURCE,INPUTS,MANIFEST,MANIFEST_SHA,T0
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');args=parser.parse_args()
    assert args.run,'Explicit root-owned --run required';authenticate();assert not list(BASE.glob(STEM+'_*')),'Existing namespace preserved'
    original,rows=closed_legacy();SOURCE=sha(__file__);INPUTS={**PINS,STEM+'.md':PROTOCOL_SHA,Path(__file__).name:SOURCE}
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=SOURCE,started=now());T0=time.monotonic()
    MANIFEST=dict(owner=OWNER,input_sha256=INPUTS,orders=list(ORDERS),height_rule='min(.2,nearest gas-knot distance/4) divided by1/2/4',
        arms=[[a,b] for a in (False,True) for b in (False,True)],radii_kpc=[r['R_kpc'] for r in rows],helium=[1.36,1.33],
        calibration=dict(D_Mpc=13.8,G_kpc_kms2_Msun=original['payload']['G_kpc_kms2_Msun']),
        source='Legacy measured HI/H2 only; no stellar, observed-velocity or inverse-density input',
        normalization='DeltaPhi=4piG Sigma delta(Z); signed gR=partialR Phi; published comparator Vgas abs(Vgas)',
        expected_cases=172,expected_controls=4167,expected_pairs=173,physical_flags=FLAGS)
    cases=[];impl=None
    try:
        MANIFEST_SHA=publish(STEM+'_MANIFEST.json',MANIFEST)
        for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
        import numpy as numpy_module
        np=numpy_module
        import galaxy_ring_oracle as ring
        import galaxy_density as density
        authenticate();assert sha(__file__)==SOURCE
        assert ring.G==original['payload']['G_kpc_kms2_Msun'] and density.DISTANCE_MPC==13.8
        try:ic,ir=implementation(ring)
        except (ArithmeticError,ValueError,AssertionError) as e:
            cc=dict(status='NUMERICAL_REFUSAL_RETAINED',context=AVAILABLE.get('context'),controls=AVAILABLE.get('checks',[]),
                    exception=type(e).__name__,reason=str(e),traceback=traceback.format_exc())
            cp=checkpoint('IMPLEMENTATION_REFUSED',cc,AVAILABLE.get('arrays',{}));impl=dict(cc,checkpoint=cp)
        else:
            cp=checkpoint('IMPLEMENTATION',dict(AVAILABLE['context'],controls=ic),ir);impl=dict(controls=ic,checkpoint=cp)
        for a in (False,True):
            for b in (False,True):
                for row in rows:cases.append(one_case(ring,density,row,a,b))
        assert len(cases)==172
        allchecks=impl['controls']+[t for c in cases for t in c['controls']]
        complete=all(c['status']!='NUMERICAL_REFUSAL_RETAINED' for c in cases)
        implemented=len(impl['controls'])==39 and impl.get('status')!='NUMERICAL_REFUSAL_RETAINED'
        if complete and implemented:assert len(allchecks)==4167
        good=complete and implemented and all(t['passed'] for t in allchecks)
        status='NUMERICAL_CONTROLS_PASS' if good else 'NUMERICAL_FAILURES_RETAINED';close(status,original,rows,impl,cases)
        print(status,flush=True);return 0 if good else 3
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
