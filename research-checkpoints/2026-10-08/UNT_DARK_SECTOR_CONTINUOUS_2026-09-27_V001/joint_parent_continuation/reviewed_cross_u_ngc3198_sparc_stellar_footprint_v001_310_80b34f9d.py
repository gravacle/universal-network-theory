"""Root-only same S_cross stellar-sheet sensitivity; no scientific author evaluation."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os, time, traceback, zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V001'
PARENT='CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006'
AUTHOR_DRAFT=True
PROTOCOL_SHA='3420c85ba0a91cea4fde2ee15e920b06d5e710831142a0f0843d262b46c6f649'
PINS={'cross_u_ngc3198_native_elimination_recovery_v006.py': '3d707e5d078980202cca884b18175673cfcfa649e7a01e7e0805cd6c6f7c8170', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006.md': 'acaca99c1c9c6fef56b50f1daf1b24c7d154f41f8fe53482797aa7f76e354e32', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': '581605c923df95b6008ccf0fabe7ce1fc7ce7533e5d7cd2b2b51e36d90899b3f', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RESULT.json': 'd470f406ec2279c9631f8e3e3c46a9e0d862f2a1691e1af6851b80aa871f3ff8', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_MANIFEST.json': '08252627c9809538690cac22f51fdf2a83606c016e7f731c87f1dfa2c979533b', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_E1em05_HI0_H20_CASE.json': 'a15aac98b954c86af73b85be7c8498ecec3b70da60553837353c4bfd21cab599', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz': 'ce35318b55b6f6afc7f225154aec7deb1587887a912b38962a751d9db97fa6fc', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz.COMMIT.json': 'e14fc7e7268207cb6abb3de025c2a79abf2112bda88da8d10e4e92ddeb6a6ede', 'sparc_official_massmodels_2026-10-06_v001.mrt': '9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c', 'sparc_official_massmodels_2026-10-06_v001.mrt.SOURCE.json': '2c9b80c5bd6afefab410ce860853811785e4cb3fe24dd54ed0cb71ba5c2a1e20', 'sparc_official_sample_2026-10-06_v001.mrt': '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243', 'sparc_official_sample_2026-10-06_v001.mrt.SOURCE.json': 'bacfd875aa818b3e74712009da6e18b36e4941bebe4e2c576358aa5620512a88', 'sparc_official_NGC3198_rotmod.dat': '17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953', 'sparc_official_NGC3198.dens': '4dbe84c28033a501c1599998daa534ae4d73957597c342fba21fd7a3def71d21', 'sparc_official_NGC3198.sfb': 'ae071272156d47f6292fa405adf3a9b2042f8678581af108b2d5d1e9e102ddbc', 'sparc_official_Rotmod_LTG_2026-10-06_v001.zip': '0a80cc90714828cc28b7dd57923576714d209f2490328c087c4a4ad607faf588', 'sparc_official_Rotmod_LTG_2026-10-06_v001.zip.SOURCE.json': 'd15290003f4bfc6687ebd871bc8b42a3b60563c3177a1071a4a50d3e31497075', 'sparc_official_BulgeDiskDec_LTG_2026-10-06_v001.zip': '0733de0d357cbd45c673fd4321a3b339e160abf68530684c09d28e413855fb6d', 'sparc_official_BulgeDiskDec_LTG_2026-10-06_v001.zip.SOURCE.json': 'e097262eb3693a83376d8ae48b88fa197efd05fa81cfed0228727f5a5c074cec', 'sparc_official_sfb_LTG_2026-10-06_v001.zip': '2ca5c5e16517d2096dde47247f2b78837e33fed2e323ea77b0412cf6de66eb27', 'sparc_official_sfb_LTG_2026-10-06_v001.zip.SOURCE.json': '274993d0ab0cd1805ba6fea2d7327bd7ba9a8aab9849116e6ac6bc396b6e440c', 'sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf': '87fa39590a0cded15e6dc7a51355fa2354eea8a130f477b92e4cee15c4e36a19', 'sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf.SOURCE.json': '0413b81940409e9bba28c4956b1683259084b3b4f227f50868725ce263a850f4', 'CROSS_U_NGC3198_FIXED_SOURCE_SHAPE_AUDIT_V001.md': '3a0af05a2246470a753a166794f3766c80cb9e41a1c81ee399f968de7e9eafc1'}
ML=.5; RD=3.14; SOURCE_TOL=2e-11
INHERITED_CONFIG={'newton_cap': 40, 'backtracks': 32, 'final_original_residual': 1e-08, 'native_equilibrium_cap': 40, 'native_equilibrium_tolerance': 1e-10, 'native_trials_cap': 4096, 'native_D_cap': 600, 'native_D_true_tolerance': 1e-10, 'reduced_restart': 24, 'reduced_cap': 240, 'scalar_original_P_tolerance': 1e-10, 'scalar_corrections': 3, 'arithmetic_tolerance': 2e-11, 'energy_gradient_tolerance': 1e-07}
PRIMARY='EXP24'; ARMS=('EXP24','EXP28','ROUND43')
ANCHORS={'EXP24':(24.03,.28),'EXP28':(28.16,.08)}
PHYSICAL={k:False for k in ('source_registration_qualified','full_SPARC_model_qualified','refinement_qualified','full_metric_qualified','FLRW_junction_qualified','formation_qualified','stability_qualified','observational_qualified','joint_superiority_qualified')}
np=core=native=direct=engine=None
OWNER=None; INPUTS={}; CREATED={}; RECORDS=[]; CONTEXT={}; RAW={}; BRANCH={}; CHECKS=[]

RECEIPT_EXPECTATIONS={'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 62181}, 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 50386}, 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 47083}, 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': {'status': 'NUMERICAL_PASS', 'owner_kind': 'str', 'pid': 39330}, 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json': {'status': 'PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': {'status': 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': {'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': {'status': 'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': {'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': {'status': 'NEW_BBN_ACOUSTIC_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 42904}, 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 49006}, 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 42114}, 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 56449}}

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finite(x):return float(x) if math.isfinite(float(x)) else None

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:assert math.isfinite(v);return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,v):
    raw=encode(v);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw;CREATED[name]=sha(p);return CREATED[name]

def receipt_maps(name):
    r=json.loads((BASE/name).read_text());expect=RECEIPT_EXPECTATIONS[Path(name).name]
    assert r.get('status')==expect['status'] and type(r.get('owner')).__name__==expect['owner_kind']
    owner=r.get('owner')
    if isinstance(owner,str):assert owner=='root' and r['pid']==expect['pid'] and r['pid']>0 and r['closed']>r['started']
    elif isinstance(owner,dict):
        assert owner.get('owner','root')=='root' and owner['pid']==expect['pid'] and owner['pid']>0
        assert r.get('closed',r.get('finished_utc'))>owner.get('started',owner.get('started_utc'))
    else:assert expect['owner_kind']=='NoneType' and 'owner' not in r  # Owned historical status/manifest schemas retained literally.
    ins=dict(r.get('input_sha256',r.get('pins',{})));outs=r['output_sha256'];assert outs
    for key,h in outs.items():assert sha(BASE/key)==h
    # Old receipts use absolute output paths; compare the literal immutable manifest.
    basename=Path(name).name[:-len('_RECEIPT.json')]+'_MANIFEST.json';found=[key for key in outs if Path(key).name==basename]
    if found:
        assert len(found)==1;key=found[0];m=json.loads((BASE/key).read_text())
        if 'manifest' in r:assert r['manifest']==m
        if 'manifest_sha256' in r:assert r['manifest_sha256']==outs[key]
        for key,h in dict(m.get('input_sha256',{}),**m.get('inherited_input_sha256',{})).items():
            assert key not in ins or ins[key]==h;ins[key]=h
    return dict(ins,**outs)

def resolve_inputs():
    merged=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[PARENT+'_RECEIPT.json'];done=set()
    while todo:
        n=todo.pop();assert sha(BASE/n)==merged[n]
        if n in done:continue
        done.add(n)
        for key,h in receipt_maps(n).items():
            assert len(h)==64 and (key not in merged or merged[key]==h),(key,'conflicting seal')
            merged[key]=h
            if key.endswith('_RECEIPT.json') and key not in done:todo.append(key)
    for n,h in merged.items():assert sha(BASE/n)==h,('input changed',n)
    return merged

def parent_binding():
    r=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());c=json.loads((BASE/(PARENT+'_E1em05_HI0_H20_CASE.json')).read_text())
    assert r['owner']['pid']==62181 and c['status']=='CONVERGED' and c['numerical_residual']<=1e-8
    assert c['identity']['case']=='E1em05_HI0_H20' and c['identity']['eps']==1e-5 and c['identity']['hi_tail'] is False and c['identity']['h2_tail'] is False
    assert c['identity']['grid_shape']==[65,87,45] and c['readout_qualified'] is False and all(v is False for v in c['physical_flags'].values())
    assert len(c['own_checkpoints'])==149
    for rec in c['own_checkpoints']:
        assert r['output_sha256'][rec['file']]==rec['sha256']==INPUTS[rec['file']]
        assert r['output_sha256'][rec['commit_file']]==rec['commit_sha256']==INPUTS[rec['commit_file']]
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
    b=c['own_checkpoints'][-1];assert b['file']==PARENT+'_00148_FINAL.npz' and b['metadata']['kind']=='final_state' and b['metadata']['status']=='CONVERGED'
    assert b['metadata']['identity']==c['identity'] and b['metadata']['history']==c['history']
    assert b['metadata']['schema']=={k:dict(dtype='float64',finite=True,shape=[65,87,45]) for k in ('state','residual','pre')}
    return c,b

def authenticate():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    for n,h in INPUTS.items():assert sha(BASE/n)==h,('changed input',n)
    assert sha(__file__)==OWNER['source_sha256'] if OWNER else True

def checkpoint(tag,arrays,meta):
    data=canonical(dict(meta,owner=OWNER,source_identity=BRANCH,parent_final=FINAL_BINDING,
      schema={k:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for k,a in arrays.items()}))
    text=encode(data).decode();data=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);rec=dict(file=p.name,sha256=CREATED[p.name],metadata=data)
    ch=publish(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,a in arrays.items():assert np.array_equal(z[k],a,equal_nan=True)
    return rec

def recheck():
    authenticate();assert resolve_inputs()==INPUTS;parent_binding()
    for n,h in CREATED.items():assert sha(BASE/n)==h
    for rec in RECORDS:
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(BASE/rec['file'],allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                a=z[k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
        if 'physical_state_checkpoint' in rec['metadata'] and rec['metadata']['physical_state_checkpoint'] is not None:assert rec['metadata']['physical_state_checkpoint'] in RECORDS
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())==OWNER

def check(name,actual,expected,tol=SOURCE_TOL):
    ordinal=len(CHECKS);CONTEXT.update(control=name,control_ordinal=ordinal)
    a=np.asarray(actual);b=np.asarray(expected);RAW[f'control_{ordinal:03d}_{name}_actual']=a.copy();RAW[f'control_{ordinal:03d}_{name}_expected']=b.copy()
    assert a.shape==b.shape
    gap=float(np.max(abs(a-b))) if a.size else 0.;env=max(1.,float(np.max(abs(a))) if a.size else 0.,float(np.max(abs(b))) if b.size else 0.)
    er=gap/env;row=dict(name=name,ordinal=ordinal,error=finite(er),absolute_gap=finite(gap),envelope=finite(env),tolerance=tol,passed=math.isfinite(er) and er<=tol)
    CHECKS.append(row);return row

def published_data():
    lines=(BASE/'sparc_official_NGC3198_rotmod.dat').read_text().splitlines()
    rows=np.array([[float(x) for x in s.split()] for s in lines if s.strip() and not s.startswith('#')],float)
    assert rows.shape==(43,8) and np.all(np.isfinite(rows)) and np.all(np.diff(rows[:,0])>0) and np.all(rows[:,6:]>=0)
    RAW['official_rotmod']=rows.copy()
    mrt=np.array([[float(x) for x in s.split()[2:]] for s in (BASE/'sparc_official_massmodels_2026-10-06_v001.mrt').read_text().splitlines() if s.split() and s.split()[0]=='NGC3198'],float)
    RAW['official_mrt']=mrt.copy();check('official_MRT_rotmod',rows,mrt,0.)
    sample=[s for s in (BASE/'sparc_official_sample_2026-10-06_v001.mrt').read_text().splitlines() if s.split() and s.split()[0]=='NGC3198'];assert len(sample)==1
    check('owned_Rdisk',np.array(float(sample[0].split()[11])),np.array(RD),0.)
    with zipfile.ZipFile(BASE/'sparc_official_Rotmod_LTG_2026-10-06_v001.zip') as z:assert z.read('NGC3198_rotmod.dat')==(BASE/'sparc_official_NGC3198_rotmod.dat').read_bytes()
    return rows,rows[:,[0,6]].copy(),sample[0]

def footprint(photometry,label):
    # Only radius and SBdisk enter this constructor, never Vobs or velocity components.
    assert photometry.shape==(43,2)
    if label=='ROUND43':data=photometry.copy();tail=None
    else:
        ar,sb=ANCHORS[label];loc=np.flatnonzero(photometry[:,0]==ar);assert len(loc)==1 and photometry[loc[0],1]==sb
        data=photometry[:loc[0]+1].copy();tail=RD
    return core.density.Profile(data[:,0],ML*data[:,1],tail),data

def source_comparison(r,photometry,old_profiles):
    result={};factor=2*math.pi*1e6*core.density.G_KPC_KMS2_MSUN/core.A0_V
    oldload=core.surface_load(r,old_profiles,16);RAW['old_total_load']=oldload.copy()
    oldstar=core.surface_load(r,{'stars':old_profiles['stars']},16);RAW['old_stellar_load']=oldstar.copy()
    queries=np.unique(np.r_[0.,.16,r,photometry[:,0],old_profiles['stars'].r])
    gas=np.stack([old_profiles[k].sigma(queries) for k in ('HI_He','H2_He')]);RAW['query_radii']=queries.copy();RAW['old_gas_sigma']=gas.copy()
    for label in ARMS:
        CONTEXT.update(stage='source_comparison',source_arm=label);star,table=footprint(photometry,label);profiles=dict(old_profiles,stars=star)
        original=star.sigma(table[:,0]);check(label+'_published_prefix',original,ML*table[:,1],0.)
        check(label+'_constant_core',star.sigma(np.array([0.,.16,.32])),np.full(3,ML*photometry[0,1]),0.)
        load=core.surface_load(r,profiles,16);RAW[label+'_load16']=load.copy()
        fine=core.surface_load(r,profiles,32);RAW[label+'_load32']=fine.copy();check(label+'_surface_quadrature',load,fine)
        mass=np.array([float(p.integral(0.,r[-1])) for p in profiles.values()]);RAW[label+'_component_Rsigma_integrals']=mass.copy()
        check(label+'_exact_annular_mass',np.array(float(np.sum(load))),np.array(factor*float(np.sum(mass))))
        newgas=np.stack([profiles[k].sigma(queries) for k in ('HI_He','H2_He')]);check(label+'_unchanged_gas',newgas,gas,0.)
        sl=core.surface_load(r,{'stars':star},16);RAW[label+'_stellar_load']=sl.copy();check(label+'_load_decomposition',load-oldload,sl-oldstar)
        sig=np.stack([profiles[k].sigma(queries) for k in profiles]);RAW[label+'_component_sigma']=sig.copy()
        delta=load-oldload;RAW[label+'_load_delta']=delta.copy();psigma=star.sigma(photometry[:,0]);RAW[label+'_published_SB_delta']=psigma-ML*photometry[:,1]
        assert np.all(np.isfinite(load)) and np.all(load>=0) and np.all(np.isfinite(sig)) and np.all(sig>=0) and np.sum(load)>0
        result[label]=dict(anchor=None if label=='ROUND43' else ANCHORS[label],Rd=star.tail,central_constant=ML*photometry[0,1],M_to_L=ML,total_mass_Msun=float(2*math.pi*1e6*np.sum(mass)),stellar_mass_Msun=float(2*math.pi*1e6*mass[1]),component_names=list(profiles),source_quadrature_order=16)
    assert len(CHECKS)==20
    cp=checkpoint('SOURCE_FOOTPRINTS',dict(RAW),dict(kind='three_predeclared_source_footprints',controls=list(CHECKS),summaries=result,nonlinear_arm=PRIMARY))
    assert all(c['passed'] for c in CHECKS),'Source arithmetic controls refused; full tensors retained'
    return result,cp

def readouts(model,x,observations):
    psi=x[0,:,0].copy();slopes=np.diff(psi)/np.diff(model.r);oldgrad=np.gradient(psi,model.r,edge_order=2)
    RAW['final_midplane_psi']=psi;RAW['final_cell_slopes']=slopes;RAW['final_legacy_nodal_gradient']=oldgrad
    assert np.all(np.isfinite(slopes)) and np.all(np.isfinite(oldgrad))
    signed=[];rows=[]
    for R,V,E,*unused in observations:
        R=float(R);V=float(V);E=float(E);matches=np.flatnonzero(model.r==R)
        if len(matches):
            k=int(matches[0]);assert 0<k<len(model.r)-1;left=float(slopes[k-1]);right=float(slopes[k]);cell=None;node=k
        else:
            k=int(np.searchsorted(model.r,R,side='right')-1);assert 0<=k<len(slopes);left=right=float(slopes[k]);cell=k;node=None
        old=float(np.interp(R,model.r,oldgrad));v2s=[R*core.A0_V*g for g in (left,right,old)]
        signed.append([R,V,E,left,right,old,*v2s]);RAW['final_observed_signed_forces']=np.array(signed)
        assert all(math.isfinite(t) for t in v2s)
        vs=[math.sqrt(v) if v>=0 else None for v in v2s]
        rows.append(dict(R_kpc=R,observed_velocity_kms=V,observed_error_kms=E,cell_index=cell,exact_node_index=node,Q1_left_force_a0=left,Q1_right_force_a0=right,legacy_force_a0=old,Q1_left_v2=v2s[0],Q1_right_v2=v2s[1],legacy_v2=v2s[2],Q1_left_velocity=vs[0],Q1_right_velocity=vs[1],legacy_velocity=vs[2],Q1_left_residual=None if vs[0] is None else vs[0]-V,Q1_right_residual=None if vs[1] is None else vs[1]-V,legacy_residual=None if vs[2] is None else vs[2]-V,negative_force_left=left<0,negative_force_right=right<0,negative_force_legacy=old<0))
    assert len(rows)==43
    return rows

def solve(run,x):
    model=run.model;history=[];status='NATIVE_IMPLEMENTATION_FAILED'
    run.current_state_checkpoint=checkpoint('INPUT',dict(state=x),dict(kind='original_parent_state',identity=run.identity,parent_binding=BINDING))
    controls=native_controls(model,x)
    if not all(c['passed'] for c in controls):return x,status,history,controls
    x,eq=run.equilibrate(x,'initial_fixed_potential')
    if not eq['ok']:return x,'NATIVE_EQUILIBRIUM_FAILED',history,controls
    initial_eq=eq;status='NEWTON_ALLOWANCE'
    run.current_state_checkpoint=checkpoint('EQUILIBRATED_INITIAL',dict(state=x),dict(kind='outer_base',identity=run.identity,native_equilibrium=eq))
    for outer in range(CONFIG['newton_cap']):
        CONTEXT.update(outer=outer,stage='reduced_Newton');r,pre,H=model.residual(x);root=np.sqrt(pre);error=norm(r/root)/run.scale
        if not math.isfinite(error):
            checkpoint('ORIGINAL_NORM_FAILED',dict(state=x,residual=r,pre=pre),dict(kind='original_full_norm_refusal',identity=run.identity,unaccepted=True,reason='Nonfinite original normalized residual; raw arrays retained'));status='ORIGINAL_NORM_FAILED';break
        if error<=CONFIG['final_original_residual']:status='CONVERGED';break
        target=min(.5,max(1e-6,.5*math.sqrt(error)));block=None
        try:
            block=ScalarInverse(model,x,root);block.case_identity=run.identity;block.physical_state_checkpoint=run.current_state_checkpoint;block.prepare(x)
        except (ValueError,AssertionError,FloatingPointError):
            checkpoint('SCALAR_FACTOR_FAILED',getattr(block,'arrays',{}),dict(kind='scalar_factor_refusal',identity=run.identity,physical_state_checkpoint=run.current_state_checkpoint,outer=outer,unaccepted=True,controls=getattr(block,'controls',[]),factor=getattr(block,'factor_info',None),context=dict(CONTEXT),traceback=traceback.format_exc()));status='SCALAR_FACTOR_FAILED';break
        block.factor_record=checkpoint('SCALAR_FACTOR',block.arrays,dict(kind='scalar_proxy_factor',identity=run.identity,physical_state_checkpoint=run.current_state_checkpoint,outer=outer,controls=block.controls,factor=block.factor_info))
        controls+=block.controls
        if outer==0:controls+=field_controls(block,H)
        if not all(c['passed'] for c in controls):status='BLOCK_IMPLEMENTATION_FAILED';break
        forms=block.forms;rv=split(r);saved=dict(state=x,original_residual=r,whitening_pre=pre,whitening_root=root)
        try:
            t,first=run.Dsolve(forms,rv,['Schur_rhs',outer]);bred=-r[0]-block.BT(t);saved['native_rhs_response']=t;saved['reduced_physical_rhs']=bred;bn=bred/root[0]
            calls=[]
            def A(v):
                p=v/root[0];response,info=run.Dsolve(forms,block.B(p),['Schur_action',outer,len(calls)]);calls.append(info)
                return (block.K(p)-block.mass(p)-block.BT(response))/root[0]
            def M(v):
                p,info=block.scalar(root[0]*v);return root[0]*p,info
            dpwhite,lin=fgmres(A,bn,M,np.zeros_like(bn),target,restart=CONFIG['reduced_restart'],cap=CONFIG['reduced_cap']);saved['reduced_whitened_partial']=dpwhite
            dp=dpwhite/root[0];dv,last=run.Dsolve(forms,block.B(dp)-rv,['full_reconstruction',outer]);delta=join(model,dp,dv);saved['full_physical_direction']=delta
            hd=H(delta);saved['original_full_H_action']=hd;b=-r/root;cert=norm((hd+r)/root)/norm(b)
            row=dict(outer=outer,error=error,inexact_target=target,reduced_linear=lin,native_rhs_linear=first,native_action_linears=calls,native_reconstruction_linear=last,original_full_H_error=finite(cert),full_linear_pass=math.isfinite(cert) and cert<=target and lin['ok'])
            checkpoint('REDUCED_LINEAR',saved,dict(kind='reduced_linear_certificate',identity=run.identity,outer=outer,row=row,unaccepted=not row['full_linear_pass']))
        except (ValueError,AssertionError,FloatingPointError):
            checkpoint('REDUCED_LINEAR_FAILED',saved,dict(kind='reduced_linear_refusal',identity=run.identity,outer=outer,unaccepted=True,context=dict(CONTEXT),traceback=traceback.format_exc()));status='LINEAR_FAILED';break
        if not row['full_linear_pass']:history.append(row);status='LINEAR_FAILED';break
        accepted=False;row['trials']=[]
        for back in range(CONFIG['backtracks']):
            step=2.**(-back);candidate=x+step*delta;trialraw=dict(base_state=x,candidate=candidate,direction=delta,outer_whitening_root=root)
            try:
                model.clock(candidate[0]);candidate,eq=run.equilibrate(candidate,['outer_trial',outer,back]);trialraw['candidate_equilibrated']=candidate
                if not eq['ok']:trial=dict(backtrack=back,step=step,accepted=False,reason='native_equilibrium_refusal',native_equilibrium=eq)
                else:
                    cr,cp=model.residual(candidate,False);trialraw['candidate_residual']=cr;trialraw['candidate_pre']=cp;ce=norm(cr/root)/run.scale;accepted=math.isfinite(ce) and ce<=(1-1e-4*step)*error
                    trial=dict(backtrack=back,step=step,accepted=accepted,original_full_error=finite(ce),original_full_error_reason=None if math.isfinite(ce) else 'Nonfinite original full trial norm; raw residual retained',native_equilibrium=eq)
            except (ValueError,AssertionError,FloatingPointError) as exc:accepted=False;trial=dict(backtrack=back,step=step,accepted=False,reason=type(exc).__name__)
            checkpoint('OUTER_TRIAL',trialraw,dict(kind='outer_trial',identity=run.identity,outer=outer,trial=trial,unaccepted=not accepted));row['trials'].append(trial)
            if accepted:x=candidate;row.update(step=step,candidate_error=ce);break
        row['accepted']=accepted;history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        run.current_state_checkpoint=checkpoint('OUTER_ACCEPTED',dict(state=x),dict(kind='outer_accepted',identity=run.identity,outer=outer+1,history=history))
        print('NATIVE_ELIMINATION','NEWTON',outer+1,'ERROR',ce,'STEP',step,flush=True)
    return x,status,history,controls

def main():
    global np,core,native,direct,engine,OWNER,INPUTS,FINAL_BINDING,BINDING,BRANCH
    global native_controls,field_controls,split,join,norm,Run,ScalarInverse,fgmres,CONFIG
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    assert not [p for p in BASE.glob(STEM+'_*')],'Existing runtime namespace preserved'
    INPUTS=resolve_inputs();parent,FINAL_BINDING=parent_binding();BINDING=FINAL_BINDING;source=sha(__file__)
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=source,started=now());tick=time.monotonic()
    try:
        publish(STEM+'_OWNER_START.json',OWNER)
        fixed=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text())['manifest']['fixed']
        BRANCH=dict(source_id=PRIMARY,eps=1e-5,grid_shape=[65,87,45],native_modes=32,hi_tail=False,h2_tail=False,M_to_L=ML,Rd_kpc=RD,anchor=ANCHORS[PRIMARY],inherited_fixed=fixed,source_assumptions=['constant central0to.32','piecewise linear SB','EXP24 thereafter','same thin sheet'],law_changes=[])
        publish(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_final=FINAL_BINDING,parent_case_file=PARENT+'_E1em05_HI0_H20_CASE.json',source_identity=BRANCH,source_arms=ARMS,nonlinear_arms=[PRIMARY],physical_flags=PHYSICAL,no_automatic_resume=True,numerical_configuration=INHERITED_CONFIG))
        authenticate()
        np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001')
        native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
        direct=importlib.import_module('cross_u_direct_scalar_proxy_controls_v001');direct.np=np;direct.core=core;direct.native=native
        engine=importlib.import_module('cross_u_ngc3198_native_elimination_recovery_v006');engine.np=np;engine.core=core;engine.native=native;engine.direct=direct;engine.checkpoint=checkpoint;engine.CONTEXT=CONTEXT;engine.BINDING=FINAL_BINDING
        for name in ('native_controls','field_controls','split','join','norm','Run','ScalarInverse','fgmres','CONFIG'):globals()[name]=getattr(engine,name)
        assert CONFIG==INHERITED_CONFIG;authenticate();core.authenticate()
        with np.load(BASE/FINAL_BINDING['file'],allow_pickle=False) as z:
            assert set(z.files)=={'state','residual','pre','metadata'} and json.loads(str(z['metadata']))==FINAL_BINDING['metadata']
            x=z['state'].copy();pr=z['residual'].copy();pp=z['pre'].copy()
        RAW.update(parent_state=x.copy(),parent_original_residual=pr,parent_original_pre=pp)
        old=parent['identity'];r=np.array(old['r_kpc']);z=np.array(old['z_kpc']);RAW['r_kpc']=r.copy();RAW['z_kpc']=z.copy()
        assert x.shape==(65,87,45) and r.shape==(87,) and z.shape==(45,) and r[0]==z[0]==0 and r[-1]==z[-1]==128 and np.all(np.isfinite(x))
        observations,photometry,sample=published_data();RAW['photometry_only']=photometry.copy()
        oldprofiles=core.density.profiles(False,False);summaries,source_cp=source_comparison(r,photometry,oldprofiles)
        star,_=footprint(photometry,PRIMARY);profiles=dict(oldprofiles,stars=star)
        model=core.Model(r,z,32,1e-5,fixed,profiles);model.fgmres_fixed=fixed
        assert np.all(x[~model.mask]==0) and all(model.source_checks[k] is True for k in ('positive_weights',))
        assert model.source_checks['surface_quadrature_relative']<=SOURCE_TOL and model.source_checks['exact_annular_mass_relative']<=SOURCE_TOL and model.source_checks['weight_sum_error']<=SOURCE_TOL
        delta_rhs=model.rhs.copy();oldload=RAW['old_total_load'];delta_rhs[0,:,0]-=oldload;delta_rhs[~model.mask]=0
        checkpoint('SOURCE_CHANGED_INPUT',dict(state=x,residual_parent=pr,pre_parent=pp,new_rhs=model.rhs,source_rhs_delta=delta_rhs,r_kpc=r,z_kpc=z,mask=model.mask),dict(kind='authentic_warm_start_new_stellar_source',source_checkpoint=source_cp,source_checks=model.source_checks))
        RAW.clear();identity=dict(old,case='E1em05_SPARC_EXP24_HI0_H20',source_identity=BRANCH,source_sensitivity_sha256=source,source_sensitivity_manifest_sha256=CREATED[STEM+'_MANIFEST.json'],source_parent_final=FINAL_BINDING)
        _,pre0,_=model.residual(np.zeros(model.shape));scale=norm(model.rhs/np.sqrt(pre0));assert math.isfinite(scale) and scale>0
        run=Run(model,identity,scale);x,status,history,controls=solve(run,x)
        rr,pre,_=model.residual(x);error=norm(rr/np.sqrt(pre))/scale
        if error<=1e-8 and all(c['passed'] for c in controls) and status in ('CONVERGED','NEWTON_ALLOWANCE'):status='CONVERGED'
        RAW.update(final_state=x,final_residual=rr,final_pre=pre,final_rhs=model.rhs)
        rows=readouts(model,x,observations)
        final=checkpoint('FINAL',dict(RAW),dict(kind='final_state_and_signed_readouts',identity=identity,status=status,history=history,rows=rows,error=finite(error),error_reason=None if math.isfinite(error) else 'Nonfinite original norm retained'))
        case=dict(identity=identity,status=status,numerical_residual=finite(error),history=history,controls=controls,source_controls=list(CHECKS),source_summaries=summaries,source_checkpoint=source_cp,final_checkpoint=final,rows=rows,native_trials=run.native_trials,native_D_failure_checkpoints=run.D_failures,own_checkpoints=list(RECORDS),parent_qualification=parent['physical_flags'],readout_qualified=False,physical_flags=PHYSICAL)
        publish(STEM+'_EXP24_CASE.json',case);recheck()
        result=dict(status=status,owner=OWNER,input_sha256=INPUTS,source_identity=BRANCH,source_controls=list(CHECKS),cases=[case],parent_original_outcomes=dict(status=parent['status'],numerical_residual=parent['numerical_residual'],readout_qualified=parent['readout_qualified'],physical_flags=parent['physical_flags']),qualification=PHYSICAL,elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result)
        raw=('# Same-law fixed SPARC stellar-footprint sensitivity\n\n'+status+'; one EXP24 coarse branch, two source-only endpoint comparisons; all43 signed readouts retained; no source/metric/observational adoption.\n').encode();report=BASE/(STEM+'_REPORT.md')
        with report.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        report.chmod(0o444);assert report.read_bytes()==raw;CREATED[report.name]=sha(report);recheck()
        receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,physical_flags=PHYSICAL)
        publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())==receipt
        return 0 if status=='CONVERGED' else 3
    except Exception:
        if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_available_arrays',unaccepted=True,context=dict(CONTEXT)))
        if STEM+'_RECEIPT.json' not in CREATED:
            eh=publish(STEM+'_ERROR.json',dict(status='ERROR_PRESERVED',owner=OWNER,failed=now(),context=dict(CONTEXT),traceback=traceback.format_exc(),preserved_outputs=dict(CREATED),physical_flags=PHYSICAL))
            recheck();receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,physical_flags=PHYSICAL)
            publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())==receipt
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args();assert args.root_owned
    raise SystemExit(main())
