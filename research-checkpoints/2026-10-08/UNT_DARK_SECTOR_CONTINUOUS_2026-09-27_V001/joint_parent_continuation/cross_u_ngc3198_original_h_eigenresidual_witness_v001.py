"""Guarded six-direction original signed-H witness; no spectral or stability solve."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os, time, traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_ORIGINAL_H_EIGENRESIDUAL_WITNESS_V001'
ACTIVE='CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004'
DIRECT='CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001'
AUTHOR_DRAFT=False
PINS={'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json': '720cbaf0902285d35dc3a50d59f81d266431c7d91b4985eb19ab822b0b14413b', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': '337e7b82f5270fc2e3cd4823cb95c92600acde45dc6adbc66a98c7ebb1bef400', 'cross_u_ngc3198_partial_recovery_v002.py': '6f52dddd8ec0fbf844f9174c92e80d3700b51dcc8432709cd1d88c81811b1925', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002.md': 'c236db1e798d4df086460e880d3515612dea127335eb85c4defde842e4589400', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_MANIFEST.json': 'a1756ed9cec5bff2273088008ca6410c9c9a6f769f0fb92c6750c2601a89f687', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RESULT.json': 'dcc18c6714c7f4d427a452eb11ba86b91496bf305925a4a2b22a0c3d87779963', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': 'c72830fb31defeae5443beed55eec910b08c2bf520a45f14853c9cdfe59950a1', 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_MANIFEST.json': 'b83b93c6c64e5a9f356e849e0688a5690073f4d07c756ee67fd1390c8671471c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5', 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RESULT.json': 'd20f71731fe822a5af9e7d78408a346b5414752d9378a2a062a1e4ae5f16b871', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': '1f1f1aa4c06cf74f54875aefed42dc347932debc4a321211a96a5b3623f7331a', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004.md': '74e026fb4bfb331820fa18758bae815b7abb27ac442a2b126a43f0ae8d6418c3', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900', 'cross_u_ngc3198_coupled_fgmres_recovery_v004.py': '692d94ea692391886c77f0bb02968d2b52458cdd455b915c4b96c5c6faf206bd', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_MANIFEST.json': 'e902dd60d19012009a8a4400acb4fa0be9594abf5d9dead4d58b1a20e2e1717f', 'cross_u_direct_scalar_proxy_controls_v001.py': '0d58dcff5ae26ba16bf6f4272144fb7a0ce4f14474ac2edfa50115f911fc7621', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001.md': '480b5f201e67fcd8ccb973e48d0e43e8e95c5a856446ccef1867809b53121ce6', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RESULT.json': 'e52f243794bf9c81e17316faabfc87615215a4a9df86945756c7eda1d2f7b43f', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': '19944cbae13660a48ac10d3ad4f97d9a5df1a8b06b1bb6a0b5d4f8ebe9b376e5', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_MANIFEST.json': '50246a7010a0b37c9671f7b3b0e6e350debfb628dd1e58fd411a8da55a0895b3', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_CASE.json': 'a19e508881b1274ef77cd4b13a50090040c7ce4de02146614dc4373f52680514', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz': 'ccf1115dd1d10411f4581172ab0dd029cb9678be1dd44f423bfa0ae876ce8735', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz.commit.json': '60925dd4c9a77832445fefc867e8aaed1af169f351c8f1c6bf26ea4e0b2e46c2', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_STEP_000.npz': '04dd693e6a92d91f131bb628d4ab6692e192901100625015cdb38f5981bd64cd', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_STEP_000.npz.commit.json': '8a4e5fb206dbd68df4b2f6607053714702ce697a8d6fd6e60c5c4715028acb26', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_CASE.json': '54a6e0bd94b6ab4a2a1842dfc83d723d7ac429541a363ed63e63c02e9e93a199', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz': 'a2ca7a3f0c46ca08408d60706066c9ab031872a5d1ba04d624a404d8f142365d', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz.commit.json': '6f9d2e5c33025ada5ba75ea4c2908d6199c177b38e6de4b042e7605eee01bc22', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_STEP_000.npz': 'ad9c2d9f043ec71415d2c2493eb5900bc1957b78a0d656beb9af3f574b959a30', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_STEP_000.npz.commit.json': 'c4abb50c4c6ec6b27f2372d4af2fdf3660113f87bec10190e398de17c65122a6', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_CASE.json': '8ac35ca7cb4ce8b4b8f9a2fbb7b00d6d4104e1aa59c74fb4c235ab00e388642d', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz': '8b36ba0aa6321ef658c8f1e6acc04c5b24063096033c178443d3a11fddf7f112', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz.commit.json': '8f1e0ddfd579dd37594a23eccdc7928c847f38edfaadbe89aaf39cb7b691f7fc', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_STEP_000.npz': '74355f43a0bd64dfcb42b8bbc0b1c48f6af81a943d71d2031d6f559dabf339ab', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_STEP_000.npz.commit.json': '2841f645f11bcefdca79b2d9b2018923af619ff67f24e01f152e458bef6f6c38'}
BINDINGS={'E1em05_HI0_H20': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_CASE.json', 'case_sha256': 'a19e508881b1274ef77cd4b13a50090040c7ce4de02146614dc4373f52680514', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz', 'sha256': 'ccf1115dd1d10411f4581172ab0dd029cb9678be1dd44f423bfa0ae876ce8735', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '60925dd4c9a77832445fefc867e8aaed1af169f351c8f1c6bf26ea4e0b2e46c2'}, 'E1em05_HI0_H21': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_CASE.json', 'case_sha256': '54a6e0bd94b6ab4a2a1842dfc83d723d7ac429541a363ed63e63c02e9e93a199', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz', 'sha256': 'a2ca7a3f0c46ca08408d60706066c9ab031872a5d1ba04d624a404d8f142365d', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '6f9d2e5c33025ada5ba75ea4c2908d6199c177b38e6de4b042e7605eee01bc22'}, 'E1em05_HI1_H20': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_CASE.json', 'case_sha256': '8ac35ca7cb4ce8b4b8f9a2fbb7b00d6d4104e1aa59c74fb4c235ab00e388642d', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz', 'sha256': '8b36ba0aa6321ef658c8f1e6acc04c5b24063096033c178443d3a11fddf7f112', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '8f1e0ddfd579dd37594a23eccdc7928c847f38edfaadbe89aaf39cb7b691f7fc'}}
PROTOCOL_SHA='75662ae9bca144e9fb9319acbef249a3d84a2950c4abe8e48db7cf2c5506a2bf'
TOL=2e-11
PHYSICAL=dict(rigorous_floating_enclosure=False,physical_near_null_qualified=False,physical_stability_qualified=False,force_qualified=False,refinement_qualified=False,joint_superiority_qualified=False)
OWNER=None
CREATED={}
CONTEXT={}
np=core=native=direct=None

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def finite(v):return float(v) if math.isfinite(float(v)) else None
def norm(v):return float(np.linalg.norm(v))
def dot(a,b):return float(np.sum(a*b))
def write(name,raw):
    p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw;CREATED[name]=sha(p);return CREATED[name]
def publish(name,v):return write(name,enc(v))
def recheck():
    for n,h in CREATED.items():assert sha(BASE/n)==h,('changed own output',n)
    if OWNER is not None:assert sha(__file__)==OWNER['source_sha256']
def auth():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64 and len(BINDINGS)==3
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():assert sha(BASE/n)==h,('input_changed',n)
def closed_maps():
    for stem in ('CROSS_U_NGC3198_NONLINEAR_DISK_V001','CROSS_U_NGC3198_PARTIAL_RECOVERY_V002','CROSS_U_NGC3198_MINRES_RECOVERY_V003','CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001',DIRECT):
        r=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
        if stem==DIRECT:
            assert r['status']=='CLOSED' and r['owner']['pid']>0 and r['finished_utc']>r['owner']['started_utc']
            for n,h in r['pins'].items():assert sha(BASE/n)==h
        else:assert r['owner']=='root' and r['pid']>0 and r['closed']>r['started']
        for n,h in r['output_sha256'].items():assert sha(BASE/n)==h
    m=json.loads((BASE/(ACTIVE+'_MANIFEST.json')).read_text());assert m['owner']=='root' and m['pid']==51488
    assert m['source_sha256']==PINS['cross_u_ngc3198_coupled_fgmres_recovery_v004.py'] and m['no_automatic_resume'] is True
    for n,h in m['input_sha256'].items():assert sha(BASE/n)==h
    return m

def checkpoint(name,arrays,metadata):
    schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}
    metadata=dict(metadata,owner=OWNER,schema=schema);text=enc(metadata).decode();metadata=json.loads(text);path=BASE/f'{STEM}_{name}.npz'
    with path.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    path.chmod(0o444);CREATED[path.name]=sha(path);record=dict(file=path.name,sha256=CREATED[path.name],metadata=metadata)
    ch=publish(path.name+'.COMMIT.json',record)
    with np.load(path,allow_pickle=False) as n:
        assert str(n['metadata'])==text and set(n.files)==set(arrays)|{'metadata'}
        for k,v in arrays.items():assert np.array_equal(n[k],v,equal_nan=True)
    return dict(record,commit_sha256=ch)

def case_witness(name,binding,fixed):
    case=json.loads((BASE/binding['case_file']).read_text());commit=json.loads((BASE/binding['commit_file']).read_text())
    assert case['status']=='LINEAR_FAILED' and case['identity']['case']==name and case['readout_qualified'] is False and len(case['rows'])==43
    assert all(v is False for v in case['physical_flags'].values()) and len(case['history'])==1 and case['history'][0]['linear']['iterations']==240
    assert case['own_checkpoints'][-1]['file']==binding['file'] and commit['file']==binding['file'] and commit['sha256']==binding['sha256'] and commit['identity']==case['identity']
    arrays={};rows=[];checks=[];normalized=[];actions=[]
    try:
        CONTEXT.update(case=name,stage='load_selected_state')
        with np.load(BASE/binding['file'],allow_pickle=False) as n:
            assert set(n.files)=={'state','identity','history','schema','unaccepted_linear_partial'}
            state=n['state'].copy();arrays['state']=state
            partial=n['unaccepted_linear_partial'].copy();arrays['saved_failed_whitened_partial']=partial
            assert json.loads(str(n['identity']))==case['identity'] and json.loads(str(n['history']))==case['history']
            assert json.loads(str(n['schema']))==dict(history_length=1,partial_schema=commit['partial_schema'])
        CONTEXT.update(case=name,stage='original_model_and_residual')
        old=case['identity'];model=core.Model(np.array(old['r_kpc']),np.array(old['z_kpc']),32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
        arrays['mask']=model.mask
        assert state.shape==partial.shape==model.shape and np.all(np.isfinite(state)) and np.all(np.isfinite(partial))
        assert np.all(state[~model.mask]==0) and np.all(partial[~model.mask]==0)
        residual,pre,H=model.residual(state);arrays['physical_rhs']=-residual;arrays['whitening_pre']=pre
        root=np.sqrt(pre);arrays['whitening_root']=root
        assert np.all(np.isfinite(residual)) and np.all(np.isfinite(pre)) and np.all(pre>0) and np.all(np.isfinite(root))
        rhs=-residual/root;arrays['whitened_rhs']=rhs;assert np.all(rhs[~model.mask]==0)
        proxy=direct.Proxy(model,state,fixed)
        for label,raw in (('saved_failed_partial',partial),('whitened_physical_rhs',rhs)):
            CONTEXT.update(case=name,witness=label,stage='original_H_action');rawnorm=norm(raw);assert math.isfinite(rawnorm) and rawnorm>0,'Direction zero/nonfinite/norm-underflow refusal'
            v=raw/rawnorm;arrays[label+'_normalized']=v
            physical=v/root;arrays[label+'_physical_direction']=physical;assert np.all(np.isfinite(physical)) and np.all(v[~model.mask]==0)
            hv=H(physical);arrays[label+'_physical_H_action']=hv
            av=hv/root;arrays[label+'_A_action']=av
            assert np.all(np.isfinite(hv)) and np.all(np.isfinite(av)) and np.all(hv[~model.mask]==0)
            p=physical[0];vv=np.stack([physical[1::2],physical[2::2]],axis=1)
            kp=proxy.K(p);arrays[label+'_K_action']=kp
            mp=proxy.mass(p);arrays[label+'_pressure_action']=mp
            bt=proxy.BT(vv);arrays[label+'_BT_action']=bt
            dv=proxy.forms.apply(vv,core.ELL);arrays[label+'_native_D_action']=dv
            bp=proxy.B(p);arrays[label+'_B_action']=bp
            independent=np.zeros_like(physical);independent[0]=kp-mp-bt;independent[1::2]=(dv-bp)[:,0];independent[2::2]=(dv-bp)[:,1]
            arrays[label+'_independent_physical_block']=independent
            env=norm(kp)+norm(mp)+norm(bt)+norm(dv)+norm(bp);error=norm(hv-independent)/max(env,1e-30)
            checks.append(dict(name='physical_block_'+label,error=finite(error),envelope=finite(env),tolerance=TOL,passed=math.isfinite(env) and math.isfinite(error) and error<=TOL))
            vn=norm(v);mu=dot(v,av)/dot(v,v);ev=av-mu*v;arrays[label+'_eigenresidual']=ev;eta=norm(ev)/vn;actionnorm=norm(av)/vn
            assert all(math.isfinite(z) for z in (mu,eta,actionnorm))
            relative=finite(eta/abs(mu)) if mu!=0 else None
            rows.append(dict(witness=label,raw_norm=rawnorm,normalized_norm=vn,Rayleigh_mu=mu,eigenresidual_eta=eta,action_norm=actionnorm,computed_mu_minus_eta=mu-eta,computed_mu_plus_eta=mu+eta,
                             eta_over_abs_mu=relative,relative_reason=None if relative is not None else 'Zero Rayleigh or nonfinite relative ratio; undefined',spectral_or_stability_qualified=False))
            normalized.append(v);actions.append(av)
        left=dot(normalized[0],actions[1]);right=dot(actions[0],normalized[1]);env=float(np.sum(abs(normalized[0]*actions[1]))+np.sum(abs(actions[0]*normalized[1])))
        e=abs(left-right)/max(env,1e-30);checks.append(dict(name='original_A_symmetry',signed_difference=left-right,error=finite(e),envelope=finite(env),tolerance=TOL,passed=math.isfinite(env) and math.isfinite(e) and e<=TOL))
        status='ARITHMETIC_PASS' if all(c['passed'] for c in checks) else 'ARITHMETIC_FAILURE'
        record=checkpoint(name,arrays,dict(status=status,parent_binding=binding,parent_case=case,rows=rows,controls=checks,qualification=PHYSICAL))
        return dict(case=name,status=status,rows=rows,controls=checks,checkpoint=record,parent_case=case,qualification=PHYSICAL)
    except Exception:
        checkpoint(name+'_FAILED',arrays,dict(status='EXECUTION_REFUSAL',parent_binding=binding,parent_case=case,rows=rows,controls=checks,context=dict(CONTEXT),traceback=traceback.format_exc(),qualification=PHYSICAL));raise

def main():
    global np,core,native,direct,OWNER
    auth();assert not [p for p in BASE.glob(STEM+'_*') if p.is_file()],'Existing runtime preserved'
    source=sha(__file__);parent_manifest=closed_maps()
    original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    OWNER=dict(pid=os.getpid(),source_sha256=source,started=now());start=time.monotonic()
    np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001');native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
    direct=importlib.import_module('cross_u_direct_scalar_proxy_controls_v001');direct.np=np;direct.core=core;direct.native=native;core.authenticate();direct.auth();auth()
    manifest=dict(owner=OWNER,input_sha256=dict(PINS,**{STEM+'.md':PROTOCOL_SHA}),parent_batch_closed=False,parent_manifest=parent_manifest,fixed=fixed,bindings=BINDINGS,
                  physics_changes=[],planned_original_H_actions=6,planned_arithmetic_controls=9,qualification=PHYSICAL)
    publish(STEM+'_MANIFEST.json',manifest);cases=[]
    for name,binding in BINDINGS.items():cases.append(case_witness(name,binding,fixed));auth();closed_maps()
    assert len(cases)==3 and sum(len(c['rows']) for c in cases)==6 and sum(len(c['controls']) for c in cases)==9
    for c in cases:
        rec=c['checkpoint'];assert sha(BASE/rec['file'])==rec['sha256'] and sha(BASE/(rec['file']+'.COMMIT.json'))==rec['commit_sha256']
        assert dict(json.loads((BASE/(rec['file']+'.COMMIT.json')).read_text()),commit_sha256=rec['commit_sha256'])==rec
        with np.load(BASE/rec['file'],allow_pickle=False) as n:
            assert json.loads(str(n['metadata']))==rec['metadata'] and set(n.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                v=n[k];assert s==dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v))))
    auth();closed_maps();recheck();assert sha(__file__)==source
    passed=all(c['status']=='ARITHMETIC_PASS' for c in cases);result=dict(status='ARITHMETIC_PASS' if passed else 'ARITHMETIC_FAILURE',manifest=manifest,cases=cases,qualification=PHYSICAL)
    rh=publish(STEM+'_RESULT.json',result)
    write(STEM+'_REPORT.md',('# Original signed-H eigenresidual witness\n\n'+result['status']+'; six fixed directions, nine arithmetic controls. Computed Rayleigh/eigenresidual enclosures are not rigorous floating intervals or a physical stability/zero-mode certificate.\n').encode())
    assert json.loads((BASE/(STEM+'_RESULT.json')).read_text())==result;auth();closed_maps();recheck()
    publish(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=OWNER,closed=now(),elapsed_seconds=time.monotonic()-start,input_sha256=manifest['input_sha256'],output_sha256=dict(CREATED),result_sha256=rh,qualification=PHYSICAL));auth();closed_maps();recheck()
    print(result['status'],flush=True);return 0 if passed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    try:code=main()
    except Exception:
        if OWNER is not None:publish(STEM+'_ERROR.json',dict(status='EXECUTION_ERROR_PRESERVED',owner=OWNER,failed=now(),context=CONTEXT,traceback=traceback.format_exc(),preserved_outputs=dict(CREATED),qualification=PHYSICAL))
        raise
    raise SystemExit(code)
