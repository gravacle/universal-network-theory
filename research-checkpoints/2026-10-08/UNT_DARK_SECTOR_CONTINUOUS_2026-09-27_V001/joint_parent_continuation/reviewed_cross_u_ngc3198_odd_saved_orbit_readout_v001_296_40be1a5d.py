"""Guarded root-only orbit readout of four future CLOSED band corrections."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,mmap,os,re,struct,traceback,zipfile
AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_ODD_SAVED_ORBIT_READOUT_V001'
PARENT='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
ORIGINAL='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
PROTOCOL_SHA='b80b07674a36ca75d37c39462734c0bda59749db53639c4acd3e3026cfa3dd6d'
PINS={'cross_u_ngc3198_conditional_odd_sector_v001.py': '508c379f4bd287435b406567f772fb14efdb7142ca17b18ef0d3e4e74736b394', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001.md': '030a618dc6ac06f9faa6748e3559afe074e17be4ad6feba94ae7348a935a9f2e', 'CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md': 'b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5', 'sparc_official_NGC3198_rotmod.dat': '17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953'}
PARENT_OWNER_PID=None
PARENT_TERMINAL_PINS={PARENT+'_RECEIPT.json':None,PARENT+'_RESULT.json':None,
 'cross_u_ngc3198_odd_banded_correction_v001.py':None,PARENT+'.md':None,
 **{PARENT+'_SIGMA_'+str(s)+'_CASE.json':None for s in (.1,1.,10.,100.)}}
SIGMAS=(.1,1.,10.,100.);TRUE_TOL=1e-10;ARITH_TOL=2e-11
A0=1.0059833281731022e-10;KPC=3.085677581491367e19;LIGHT=299792458.;B=A0*KPC/LIGHT**2
np=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];RAW={};CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('physical_temporal_spectrum_qualified','physical_exterior_qualified',
 'full_even_metric_qualified','full_stationary_state_qualified','stability_qualified',
 'source_feedback_qualified','formation_qualified','orbital_force_qualified',
 'observational_qualified','joint_model_adopted')}

def now():return datetime.now(timezone.utc).isoformat()


def path(n):
    p=Path(n);return p if p.is_absolute() else BASE/p


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def finite(x):return float(x) if math.isfinite(float(x)) else None


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
        if p.is_file():p.chmod(0o555 if p.suffix=='.exe' else 0o444);CREATED[p.name]=sha(p)


def selected_json(filename,wanted):
    """Scoped mmap field selection: never DOM-parse inherited huge JSON objects."""
    wanted=set(wanted);out={};token=re.compile(rb'[{}\[\]"]');quoted=re.compile(rb'"(?:[^"\\]|\\.)*"');ws=re.compile(rb'\s*');end=re.compile(rb'[,}\]]')
    with path(filename).open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as data:
        def space(p):return ws.match(data,p).end()
        def skip(p):
            p=space(p);ch=data[p:p+1]
            if ch==b'"':return quoted.match(data,p).end()
            if ch not in (b'{',b'['):return end.search(data,p).start()
            depth=1;q=p+1
            while depth:
                m=token.search(data,q);assert m is not None
                q=m.end();t=m.group()
                if t==b'"':q=quoted.match(data,m.start()).end()
                elif t in (b'{',b'['):depth+=1
                else:depth-=1
            return q
        def visit(p,key):
            p=space(p)
            if key in wanted:
                q=skip(p);out[key]=json.loads(data[p:q]);return q
            if not any(k[:len(key)]==key for k in wanted):return skip(p)
            assert data[p:p+1]==b'{';p=space(p+1)
            while data[p:p+1]!=b'}':
                m=quoted.match(data,p);assert m is not None
                k=json.loads(m.group());p=space(m.end());assert data[p:p+1]==b':'
                p=space(visit(p+1,key+(k,)))
                if data[p:p+1]==b',':p=space(p+1)
                else:assert data[p:p+1]==b'}'
            return p+1
        visit(0,());assert set(out)==wanted,('Missing selected custody field',filename,wanted-set(out))
    return out


def checkpoint(tag,arrays,meta):
    md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,
        schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
    text=encode(md).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p)
    rec=dict(file=p.name,sha256=CREATED[p.name],metadata=md)
    ch=json_file(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,v in arrays.items():assert np.array_equal(z[k],v,equal_nan=True)
    return rec

def orbit_rows(r,psi,odd):
    obs=[]
    for line in (BASE/'sparc_official_NGC3198_rotmod.dat').read_text().splitlines():
        if line.strip() and not line.startswith('#'):obs.append([float(v) for v in line.split()[:3]])
    beta=odd[0,:,0];gs=np.diff(psi)/np.diff(r);bs=np.diff(beta)/np.diff(r);rows=[];raw=[]
    for R,V,E in obs:
        hits=np.flatnonzero(r==R)
        inds=[int(hits[0])-1,int(hits[0])] if len(hits) else [int(np.searchsorted(r,R)-1)]*2
        ph=B*float(np.interp(R,r,psi));bet=float(np.interp(R,r,beta));sides=[]
        for i in inds:
            assert 0<=i<len(gs);D=B*gs[i];A=1/R-D;Bs=R*math.exp(-2*ph)*bs[i];disc=Bs*Bs+4*A*D
            plus=minus=None
            if disc>=0 and A!=0:
                root=math.sqrt(disc);plus=(-Bs+root)/(2*A);minus=(-Bs-root)/(2*A)
                if D>0 and root+Bs>0:plus=2*D/(root+Bs)
            timelike=plus is not None and math.isfinite(plus) and 0<=plus<1
            omega=None if not timelike else LIGHT/KPC*(math.exp(2*ph)*plus/R-bet)
            lead2=R*D/(1-R*D) if 1-R*D!=0 else None
            sides.append(dict(cell=i,radial_Phi_derivative=finite(D),radial_beta_star_derivative=finite(bs[i]),discriminant=finite(disc),prograde_v_over_c=finite(plus) if plus is not None else None,retrograde_v_over_c=finite(minus) if minus is not None else None,constructed_metric_timelike=bool(timelike),Omega_rad_per_second=finite(omega) if omega is not None else None,velocity_kms=None if not timelike else plus*LIGHT/1000,leading_v2_over_c2=finite(lead2) if lead2 is not None else None))
            raw.append([R,ph,bet,A,Bs,D,disc,0. if plus is None else plus,0. if minus is None else minus,float(plus is not None),float(timelike)])
        rows.append(dict(R_kpc=R,Vobs_kms=V,error_kms=E,exact_mesh_node=bool(len(hits)),left=sides[0],right=sides[1],orbital_force_qualified=False))
    assert len(rows)==43
    return rows,np.array(raw)


def inputs_and_parent():
    assert type(PARENT_OWNER_PID) is int and PARENT_OWNER_PID>0 and all(type(h) is str and len(h)==64 for h in PARENT_TERMINAL_PINS.values()),'Future parent is not admitted.'
    pins=dict(PINS,**PARENT_TERMINAL_PINS,**{STEM+'.md':PROTOCOL_SHA})
    for n,h in pins.items():assert sha(path(n))==h,('direct seal',n)
    rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
    assert rc['status']=='CLOSED' and rc['owner']['owner']=='root' and rc['owner']['pid']==PARENT_OWNER_PID and rc['closed']>rc['owner']['started']
    assert rc['owner']['source_sha256']==pins['cross_u_ngc3198_odd_banded_correction_v001.py'] and rc['result_sha256']==pins[PARENT+'_RESULT.json']
    for n,h in dict(rc['input_sha256'],**rc['output_sha256']).items():assert n not in pins or pins[n]==h;pins[n]=h
    for n,h in pins.items():assert sha(path(n))==h,('complete parent seal',n)
    assert path(PARENT+'_RESULT.json').stat().st_size<=16*1024*1024,'Compact parent allocation cap exceeded; no giant RESULT DOM.'
    result=json.loads(path(PARENT+'_RESULT.json').read_text())
    assert result['owner']==rc['owner'] and result['qualification']==rc['qualification']==FLAGS
    assert [c['sigma'] for c in result['cases']]==list(SIGMAS) and len(result['controls'])==22 and all(c['passed'] for c in result['controls'])
    assert len(result['copied_parent_controls'])==21 and len(result['copied_parent_cases'])==4
    records=result['checkpoints'];assert len(records)==11
    for rec in records:
        assert pins[rec['file']]==rec['sha256'] and pins[rec['commit_file']]==rec['commit_sha256']
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        assert rec['metadata']['owner']==rc['owner']
    for c in result['cases']:
        assert json.loads(path(PARENT+'_SIGMA_'+str(c['sigma'])+'_CASE.json').read_text())==c and c['qualification']==FLAGS
        assert c['final_checkpoint'] in records and c['assembly_checkpoint'] in records
        md=c['final_checkpoint']['metadata'];assert md['sigma']==c['sigma'] and md['status']==c['status'] and md['INFO']==c['INFO'] and md['original_residual']==c['original_residual']
    return pins,result

def load_arrays(rec,names):
    with zipfile.ZipFile(path(rec['file'])) as zz,zz.open('metadata.npy') as f:
        magic=f.read(8);assert magic[:6]==b'\x93NUMPY' and magic[6:]==b'\x01\x00'
        h=ast.literal_eval(f.read(struct.unpack('<H',f.read(2))[0]).decode())
        assert h['shape']==() and not h['fortran_order'] and h['descr'].startswith('<U')
    out={}
    with np.load(path(rec['file']),allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
        for n in names:
            v=z[n].copy();RAW['loaded_'+n]=v
            assert rec['metadata']['schema'][n]==dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) and np.all(np.isfinite(v))
            out[n]=v
    return out

def original_input():
    file=ORIGINAL+'_00000_INPUT.npz';commit=file+'.COMMIT.json'
    fields={('file',),('sha256',),('metadata','owner'),('metadata','kind'),('metadata','schema')}
    v=selected_json(commit,fields)
    assert v[('file',)]==file and v[('sha256',)]==INPUTS[file] and v[('metadata','owner')]['pid']==86078
    assert v[('metadata','kind')]=='unchanged_authentic_even_state'
    return dict(file=file,sha256=INPUTS[file],commit_file=commit,commit_sha256=INPUTS[commit],metadata=dict(kind=v[('metadata','kind')],owner=v[('metadata','owner')],schema=v[('metadata','schema')]))

def recheck():
    assert sha(__file__)==OWNER['source_sha256']
    for n,h in INPUTS.items():assert sha(path(n))==h,('input seal',n)
    for n,h in CREATED.items():assert sha(BASE/n)==h,('own seal',n)
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads(path(STEM+'_OWNER_START.json').read_text())==OWNER
    for rec in RECORDS:
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(path(rec['file']),allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for n,s in rec['metadata']['schema'].items():
                a=z[n];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))

def check(name,a,b,tol=ARITH_TOL):
    a=np.asarray(a);b=np.asarray(b);i=len(CHECKS);CONTEXT.update(control=name,control_ordinal=i)
    RAW[f'control_{i:03d}_{name}_actual']=a.copy();RAW[f'control_{i:03d}_{name}_expected']=b.copy();assert a.shape==b.shape
    gap=float(np.linalg.norm(a-b));env=max(1e-30,float(np.linalg.norm(a)),float(np.linalg.norm(b)));e=gap/env
    row=dict(name=name,error=finite(e),absolute_gap=finite(gap),envelope=finite(env),tolerance=tol,passed=math.isfinite(e) and e<=tol);CHECKS.append(row);return row

def score(rows,side):
    residuals=[];bad=[]
    for i,row in enumerate(rows):
        s=row[side];v=s['velocity_kms']
        if not s['constructed_metric_timelike'] or v is None or not math.isfinite(v):bad.append(i);residuals.append(None)
        else:
            assert row['error_kms']>0;residuals.append((v-row['Vobs_kms'])/row['error_kms'])
    return dict(chi_square=None if bad else sum(x*x for x in residuals),rows=43,invalid_indices=bad,
        reason='At least one absent/nontimelike prediction; no score imputation.' if bad else 'Descriptive only; no fitted nuisance or observational gate.',signed_standardized_residuals=residuals)

def comparison(rows,baseline):
    output=[];raw=[]
    for i,(a,b) in enumerate(zip(rows,baseline)):
        assert a['R_kpc']==b['R_kpc'] and a['Vobs_kms']==b['Vobs_kms'] and a['error_kms']==b['error_kms']
        sides={}
        for j,side in enumerate(('left','right')):
            x,y=a[side],b[side];v=x['velocity_kms'];v0=y['velocity_kms'];valid=x['constructed_metric_timelike'] and y['constructed_metric_timelike'] and v is not None and v0 is not None
            delta=v-v0 if valid else None;minus=x['retrograde_v_over_c']
            sides[side]=dict(delta_v_kms=delta,baseline_velocity_kms=v0,baseline_timelike=y['constructed_metric_timelike'],
                retrograde_timelike=minus is not None and math.isfinite(minus) and abs(minus)<1,constructed=x)
            raw.append([a['R_kpc'],j,0. if delta is None else delta,float(delta is not None),0. if v0 is None else v0,float(v0 is not None),0. if v is None else v,float(v is not None),x['radial_beta_star_derivative']])
        output.append(dict(R_kpc=a['R_kpc'],Vobs_kms=a['Vobs_kms'],error_kms=a['error_kms'],exact_mesh_node=a['exact_mesh_node'],**sides))
    return output,np.array(raw)

def arm(case,r,z,psi,baseline,baseline_raw):
    RAW.clear();CONTEXT.clear();CONTEXT.update(sigma=case['sigma'],stage='parent_numerical_admission')
    reference=dict(case_file=PARENT+'_SIGMA_'+str(case['sigma'])+'_CASE.json',case_sha256=INPUTS[PARENT+'_SIGMA_'+str(case['sigma'])+'_CASE.json'],parent_final=case['final_checkpoint'],parent_status=case['status'],INFO=case['INFO'],original_residual=case['original_residual'])
    admitted=case['status']=='LINEAR_PASS' and case['INFO']==0 and case['original_residual'] is not None and case['original_residual']<=TRUE_TOL
    if not admitted:
        cp=checkpoint('REFUSAL',{},dict(kind='unqualified_failed_linear_parent_no_orbit_prediction',sigma=case['sigma'],reference=reference,rows=[],scores=None))
        row=dict(sigma=case['sigma'],status='PARENT_LINEAR_REFUSED',reference=reference,final_checkpoint=cp,rows=[],scores=None,qualification=FLAGS)
    else:
        values=load_arrays(case['final_checkpoint'],('physical_beta_chi','unknown_coordinates','original_rhs','original_H_action','original_residual'))
        odd=values['physical_beta_chi'];RAW['current_beta_chi']=odd.copy();assert odd.shape==(2,87,45)
        rows,raw=orbit_rows(r,psi,odd);RAW['current_orbit_operands']=raw.copy();start=len(CHECKS)
        check('sigma_'+str(case['sigma'])+'_held_geometry',raw[:,[0,1,3,5]],baseline_raw[:,[0,1,3,5]],tol=0.)
        expected=[]
        for row in rows:
            for side in ('left','right'):
                s=row[side];expected.append(row['R_kpc']*math.exp(-2*B*float(np.interp(row['R_kpc'],r,psi)))*s['radial_beta_star_derivative'])
        check('sigma_'+str(case['sigma'])+'_beta_prime_force',raw[:,4],np.array(expected))
        comp,delta=comparison(rows,baseline);RAW['current_delta_readout']=delta.copy()
        scores={side:score(rows,side) for side in ('left','right')}
        cp=checkpoint('FINAL',dict(resolved_beta_chi=odd,original_unknown_coordinates=values['unknown_coordinates'],original_rhs=values['original_rhs'],original_H_action=values['original_H_action'],original_residual=values['original_residual'],constructed_orbit_operands=raw,delta_readout=delta,**{k:v for k,v in RAW.items() if k.startswith('control_')}),
            dict(kind='conditional_constructed_metric_derivative_readout',sigma=case['sigma'],reference=reference,rows=comp,scores=scores,controls=CHECKS[start:],feedback_solved=False))
        row=dict(sigma=case['sigma'],status='SAVED_ORBIT_READOUT' if all(c['passed'] for c in CHECKS[start:]) else 'ARITHMETIC_FAILED',reference=reference,final_checkpoint=cp,rows=comp,scores=scores,qualification=FLAGS)
    json_file(STEM+'_SIGMA_'+str(case['sigma'])+'_CASE.json',row);return row

def main():
    global np,OWNER,INPUTS
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
    assert args.root_run and not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64,'Guarded future source is unlaunchable.'
    assert not list(BASE.glob(STEM+'_*')),'Unused namespace; no automatic replay.'
    INPUTS,parent=inputs_and_parent();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__));cases=[]
    try:
        json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_owner=parent['owner'],sigmas=SIGMAS,qualification=FLAGS,readout_only=True))
        import numpy as _np
        np=_np
        original=original_input();old=load_arrays(original,('r_kpc','z_kpc','final_midplane_psi'));r=old['r_kpc'];z=old['z_kpc'];psi=old['final_midplane_psi']
        rec=[x for x in parent['checkpoints'] if x['metadata']['kind']=='unchanged_closed_geometry_and_parent_dispositions'];assert len(rec)==1
        held=load_arrays(rec[0],('r_kpc','z_kpc','held_Phi'));assert np.array_equal(r,held['r_kpc']) and np.array_equal(z,held['z_kpc'])
        assert r.shape==(87,) and z.shape==(45,) and psi.shape==(87,);check('unchanged_held_Phi',held['held_Phi'],B*psi,tol=0.)
        checkpoint('INPUT',dict(r_kpc=r,z_kpc=z,midplane_psi=psi,held_Phi=held['held_Phi']),dict(kind='unchanged_held_even_readout_input',original_input=original,parent_input=rec[0],controls=list(CHECKS)))
        RAW.clear();zeros=np.zeros((2,87,45));baseline,base_raw=orbit_rows(r,psi,zeros);RAW['baseline_orbit_operands']=base_raw
        actual=[];expected=[]
        for row in baseline:
            for side in ('left','right'):
                s=row[side]
                if s['constructed_metric_timelike'] and s['leading_v2_over_c2'] is not None:
                    actual.append(s['prograde_v_over_c']**2);expected.append(s['leading_v2_over_c2'])
        check('zero_shift_conformal_orbit_identity',np.array(actual),np.array(expected))
        checkpoint('BASELINE',dict(orbit_operands=base_raw,**{k:v for k,v in RAW.items() if k.startswith('control_')}),dict(kind='zero_shift_conformal_baseline',rows=baseline,scores={s:score(baseline,s) for s in ('left','right')},controls=list(CHECKS)))
        for c in parent['cases']:cases.append(arm(c,r,z,psi,baseline,base_raw))
        passed=sum(c['status']!='PARENT_LINEAR_REFUSED' for c in cases);assert len(CHECKS)==2+2*passed and len(RECORDS)==6
        status='SAVED_READOUT_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS) else 'ARITHMETIC_FAILED'
        result=dict(owner=OWNER,status=status,cases=cases,controls=CHECKS,expected_control_census=2+2*passed,linear_admitted_arms=passed,
            parent_result_file=PARENT+'_RESULT.json',parent_result_sha256=INPUTS[PARENT+'_RESULT.json'],copied_parent_controls=parent['controls'],copied_original_odd_controls=parent['copied_parent_controls'],copied_original_failed_cases=parent['copied_parent_cases'],checkpoints=RECORDS,qualification=FLAGS)
        recheck();rh=json_file(STEM+'_RESULT.json',result)
        publish(STEM+'_REPORT.md',('# '+STEM+'\n\n'+status+'. Derivative/orbit readout only; all four arms retained.\n\n'+''.join(f'- sigma={c["sigma"]}: {c["status"]}\n' for c in cases)+'\nNo full metric/source feedback, physical exterior, stability or observational qualification.\n').encode());recheck()
        rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,qualification=FLAGS)
        json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==rc
        print(json.dumps(dict(status=status,admitted_arms=passed,controls=len(CHECKS),result_sha256=rh),sort_keys=True));return 0 if status=='SAVED_READOUT_ARITHMETIC_PASS' else 3
    except BaseException:
        failure=traceback.format_exc();prior=path(STEM+'_RECEIPT.json');prior_sha=sha(prior) if prior.exists() else None
        if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_available_force_operands',context=CONTEXT,traceback=failure))
        seal_created();recheck();eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,failed=now(),context=CONTEXT,traceback=failure,checkpoints=RECORDS,controls=CHECKS,preserved_outputs=dict(CREATED),existing_receipt_sha256=prior_sha,qualification=FLAGS))
        if prior_sha is None:
            rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,qualification=FLAGS)
            json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(prior.read_text())==rc
        else:recheck();assert sha(prior)==prior_sha
        raise
if __name__=='__main__':raise SystemExit(main())
