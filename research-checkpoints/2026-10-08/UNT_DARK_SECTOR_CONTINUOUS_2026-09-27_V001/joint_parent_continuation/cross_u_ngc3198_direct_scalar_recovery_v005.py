"""Guarded per-case direct-scalar recovery; unchanged physical S_cross Hessian."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, importlib, json, math, os, time, traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_DIRECT_SCALAR_RECOVERY_V005'
PARENT='CROSS_U_NGC3198_MINRES_RECOVERY_V003'
ACTIVE_PARENT='CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004'
DIRECT='CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001'
AUTHOR_DRAFT=False
PINS={'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json': '720cbaf0902285d35dc3a50d59f81d266431c7d91b4985eb19ab822b0b14413b', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': '337e7b82f5270fc2e3cd4823cb95c92600acde45dc6adbc66a98c7ebb1bef400', 'cross_u_ngc3198_partial_recovery_v002.py': '6f52dddd8ec0fbf844f9174c92e80d3700b51dcc8432709cd1d88c81811b1925', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002.md': 'c236db1e798d4df086460e880d3515612dea127335eb85c4defde842e4589400', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_MANIFEST.json': 'a1756ed9cec5bff2273088008ca6410c9c9a6f769f0fb92c6750c2601a89f687', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RESULT.json': 'dcc18c6714c7f4d427a452eb11ba86b91496bf305925a4a2b22a0c3d87779963', 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': 'c72830fb31defeae5443beed55eec910b08c2bf520a45f14853c9cdfe59950a1', 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_MANIFEST.json': 'b83b93c6c64e5a9f356e849e0688a5690073f4d07c756ee67fd1390c8671471c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5', 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RESULT.json': 'd20f71731fe822a5af9e7d78408a346b5414752d9378a2a062a1e4ae5f16b871', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': '1f1f1aa4c06cf74f54875aefed42dc347932debc4a321211a96a5b3623f7331a', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004.md': '74e026fb4bfb331820fa18758bae815b7abb27ac442a2b126a43f0ae8d6418c3', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900', 'cross_u_ngc3198_coupled_fgmres_recovery_v004.py': '692d94ea692391886c77f0bb02968d2b52458cdd455b915c4b96c5c6faf206bd', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_MANIFEST.json': 'e902dd60d19012009a8a4400acb4fa0be9594abf5d9dead4d58b1a20e2e1717f', 'cross_u_direct_scalar_proxy_controls_v001.py': '0d58dcff5ae26ba16bf6f4272144fb7a0ce4f14474ac2edfa50115f911fc7621', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001.md': '480b5f201e67fcd8ccb973e48d0e43e8e95c5a856446ccef1867809b53121ce6', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RESULT.json': 'e52f243794bf9c81e17316faabfc87615215a4a9df86945756c7eda1d2f7b43f', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': '19944cbae13660a48ac10d3ad4f97d9a5df1a8b06b1bb6a0b5d4f8ebe9b376e5', 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_MANIFEST.json': '50246a7010a0b37c9671f7b3b0e6e350debfb628dd1e58fd411a8da55a0895b3', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_CASE.json': 'a19e508881b1274ef77cd4b13a50090040c7ce4de02146614dc4373f52680514', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz': 'ccf1115dd1d10411f4581172ab0dd029cb9678be1dd44f423bfa0ae876ce8735', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz.commit.json': '60925dd4c9a77832445fefc867e8aaed1af169f351c8f1c6bf26ea4e0b2e46c2', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_STEP_000.npz': '04dd693e6a92d91f131bb628d4ab6692e192901100625015cdb38f5981bd64cd', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_STEP_000.npz.commit.json': '8a4e5fb206dbd68df4b2f6607053714702ce697a8d6fd6e60c5c4715028acb26', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_CASE.json': '54a6e0bd94b6ab4a2a1842dfc83d723d7ac429541a363ed63e63c02e9e93a199', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz': 'a2ca7a3f0c46ca08408d60706066c9ab031872a5d1ba04d624a404d8f142365d', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz.commit.json': '6f9d2e5c33025ada5ba75ea4c2908d6199c177b38e6de4b042e7605eee01bc22', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_STEP_000.npz': 'ad9c2d9f043ec71415d2c2493eb5900bc1957b78a0d656beb9af3f574b959a30', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_STEP_000.npz.commit.json': 'c4abb50c4c6ec6b27f2372d4af2fdf3660113f87bec10190e398de17c65122a6', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_CASE.json': '8ac35ca7cb4ce8b4b8f9a2fbb7b00d6d4104e1aa59c74fb4c235ab00e388642d', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz': '8b36ba0aa6321ef658c8f1e6acc04c5b24063096033c178443d3a11fddf7f112', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz.commit.json': '8f1e0ddfd579dd37594a23eccdc7928c847f38edfaadbe89aaf39cb7b691f7fc', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_STEP_000.npz': '74355f43a0bd64dfcb42b8bbc0b1c48f6af81a943d71d2031d6f559dabf339ab', 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_STEP_000.npz.commit.json': '2841f645f11bcefdca79b2d9b2018923af619ff67f24e01f152e458bef6f6c38'}
STATE_BINDINGS={'E1em05_HI0_H20': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_CASE.json', 'case_sha256': 'a19e508881b1274ef77cd4b13a50090040c7ce4de02146614dc4373f52680514', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz', 'sha256': 'ccf1115dd1d10411f4581172ab0dd029cb9678be1dd44f423bfa0ae876ce8735', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H20_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '60925dd4c9a77832445fefc867e8aaed1af169f351c8f1c6bf26ea4e0b2e46c2'}, 'E1em05_HI0_H21': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_CASE.json', 'case_sha256': '54a6e0bd94b6ab4a2a1842dfc83d723d7ac429541a363ed63e63c02e9e93a199', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz', 'sha256': 'a2ca7a3f0c46ca08408d60706066c9ab031872a5d1ba04d624a404d8f142365d', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI0_H21_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '6f9d2e5c33025ada5ba75ea4c2908d6199c177b38e6de4b042e7605eee01bc22'}, 'E1em05_HI1_H20': {'case_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_CASE.json', 'case_sha256': '8ac35ca7cb4ce8b4b8f9a2fbb7b00d6d4104e1aa59c74fb4c235ab00e388642d', 'file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz', 'sha256': '8b36ba0aa6321ef658c8f1e6acc04c5b24063096033c178443d3a11fddf7f112', 'commit_file': 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004_E1em05_HI1_H20_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '8f1e0ddfd579dd37594a23eccdc7928c847f38edfaadbe89aaf39cb7b691f7fc'}}
CORE_INPUT_PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
PROTOCOL_SHA='9e71f5c5925ba7cbf7964768850e8e55ffb0f7850f417ba087967c83ddb38142'
np=core=native=direct=None
RECEIPTS={}
OWNER=None
CONTEXT={}


def now():return datetime.now(timezone.utc).isoformat()

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def finite(v):return float(v) if math.isfinite(v) else None

def native_tree(v):
    if v is None or type(v) in (str,bool,int):return
    if type(v) is float:assert math.isfinite(v);return
    if type(v) is list:
        for x in v:native_tree(x)
        return
    assert type(v) is dict and all(type(k) is str for k in v)
    for x in v.values():native_tree(x)

def encode(v):
    native_tree(v)
    return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,v):
    raw=encode(v);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw
    return sha(p)

def norm(a):return float(np.linalg.norm(a))

def dot(a,b):return float(np.sum(a*b))


def inputs():
    out=dict(PINS);out[STEM+'.md']=PROTOCOL_SHA
    return out

def auth():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64 and len(STATE_BINDINGS)==3,'Unexecuted author draft'
    for n,h in inputs().items():assert len(h)==64 and sha(BASE/n)==h,('changed input',n)
    if core is not None:core.authenticate();assert core.PINS==CORE_INPUT_PINS

def closed_receipt(name):
    assert name in PINS and sha(BASE/name)==PINS[name]
    r=json.loads((BASE/name).read_text());native_tree(r)
    if name==DIRECT+'_RECEIPT.json':
        owner=r['owner'];assert type(owner['pid']) is int and owner['pid']>0 and datetime.fromisoformat(r['finished_utc'])>datetime.fromisoformat(owner['started_utc'])
        assert r['status']=='CLOSED' and r['qualification'] and all(v is False for v in r['qualification'].values())
        for n,h in r['pins'].items():assert sha(BASE/n)==h,('direct input changed',n)
        assert owner['source_sha256']==PINS['cross_u_direct_scalar_proxy_controls_v001.py']
    else:
        assert r['owner']=='root' and type(r['pid']) is int and r['pid']>0
        assert datetime.fromisoformat(r['started'])<datetime.fromisoformat(r['closed'])
    assert r['output_sha256']
    for n,h in r['output_sha256'].items():assert sha(BASE/n)==h,('closed output changed',n)
    RECEIPTS[name]=(PINS[name],r);return r

def selected_prefix():
    m=json.loads((BASE/(ACTIVE_PARENT+'_MANIFEST.json')).read_text());native_tree(m)
    assert m['owner']=='root' and m['pid']==51488 and m['source_sha256']==PINS['cross_u_ngc3198_coupled_fgmres_recovery_v004.py']
    assert m['no_automatic_resume'] is True and m['physics_changes']==[]
    for n,h in m['input_sha256'].items():assert sha(BASE/n)==h,('parent manifest input',n)
    ancestor=json.loads((BASE/(PARENT+'_RESULT.json')).read_text())
    assert m['parent_cases_preserved']==ancestor['cases'] and m['parent_controls_preserved']==ancestor['controls']
    cases=[]
    for name,d in STATE_BINDINGS.items():
        case=json.loads((BASE/d['case_file']).read_text());native_tree(case)
        assert case['identity']['case']==name and case['status']=='LINEAR_FAILED' and case['readout_qualified'] is False
        assert all(v is False for v in case['physical_flags'].values()) and len(case['rows'])==43
        assert case['identity']['fgmres_manifest_sha256']==PINS[ACTIVE_PARENT+'_MANIFEST.json']
        assert case['identity']['fgmres_source_sha256']==PINS['cross_u_ngc3198_coupled_fgmres_recovery_v004.py']
        assert case['parent_case']==next(c for c in ancestor['cases'] if c['identity']['case']==name)
        assert len(case['history'])==1 and case['history'][0]['outer']==0 and case['history'][0]['linear']['ok'] is False
        assert case['history'][0]['linear']['iterations']==240 and len(case['own_checkpoints'])==2
        for rec in case['own_checkpoints']:
            assert PINS[rec['file']]==rec['sha256']==sha(BASE/rec['file'])
            assert PINS[rec['commit_file']]==rec['commit_sha256']==sha(BASE/rec['commit_file'])
            cp=json.loads((BASE/rec['commit_file']).read_text());assert cp['file']==rec['file'] and cp['sha256']==rec['sha256'] and cp['identity']==case['identity']
            assert cp['history_length']==rec['history_length'] and cp['partial_schema']==rec['partial_schema']
        last=case['own_checkpoints'][-1]
        assert all(last[k]==d[k] for k in ('file','sha256','commit_file','commit_sha256'))
        assert last['history_length']==len(case['history']) and last['partial_schema']==dict(shape=[65,87,45],dtype='float64',finite=True,mask_zero=True,unaccepted=True)
        cases.append(case)
    return m,cases

def recover_selected(case):
    name=case['identity']['case'];d=STATE_BINDINGS[name]
    assert json.loads((BASE/d['case_file']).read_text())==case
    cp=json.loads((BASE/d['commit_file']).read_text())
    with np.load(BASE/d['file'],allow_pickle=False) as n:
        assert set(n.files)=={'state','history','identity','schema','unaccepted_linear_partial'}
        x=n['state'].copy();partial=n['unaccepted_linear_partial'].copy();history=json.loads(str(n['history']));identity=json.loads(str(n['identity']));schema=json.loads(str(n['schema']))
    assert identity==case['identity']==cp['identity'] and history==case['history']
    assert schema==dict(history_length=len(history),partial_schema=cp['partial_schema'])
    assert x.shape==partial.shape==(65,87,45) and np.issubdtype(x.dtype,np.floating) and np.issubdtype(partial.dtype,np.floating)
    assert np.all(np.isfinite(x)) and np.all(np.isfinite(partial))
    mask=np.ones(x.shape,bool);mask[:,-1,:]=False;mask[:,:,-1]=False;mask[1::2,0,:]=False;mask[2::2,:,0]=False
    assert np.all(x[~mask]==0) and np.all(partial[~mask]==0)
    parent=case['identity']['parent_state']
    with np.load(BASE/parent['file'],allow_pickle=False) as n:assert np.array_equal(x,n['state'])
    return x,partial,history,d


def pcg(A,b,diagonal,tolerance=.01,cap=100):
    """Positive blocks only; finite incomplete output is a preconditioner partial."""
    x=np.zeros_like(b);bn=norm(b);it=0;reason='iteration_allowance';checks=[]
    def action(v):
        if not np.all(np.isfinite(v)):return np.full_like(v,np.nan)
        try:return A(v)
        except (AssertionError,ValueError,FloatingPointError):return np.full_like(v,np.nan)
    def close(why):
        error=None
        if math.isfinite(bn) and bn>0 and np.all(np.isfinite(x)):
            ax=action(x)
            if np.all(np.isfinite(ax)):error=finite(norm(b-ax)/bn)
        return x,dict(ok=error is not None and error<=tolerance,error=error,iterations=it,
                      reason=why,true_checks=checks,finite_partial=bool(np.all(np.isfinite(x))))
    if bn==0 and np.all(b==0):return x,dict(ok=True,error=0.,iterations=0,reason='zero_rhs',true_checks=[],finite_partial=True)
    if not math.isfinite(bn) or bn<=0 or not np.all(np.isfinite(b)):
        return close('nonfinite_or_underflow_rhs')
    if not np.all(np.isfinite(diagonal)) or not np.all(diagonal>0):return close('positive_diagonal_failed')
    r=b.copy();z=r/diagonal;p=z.copy();rz=dot(r,z)
    for it in range(1,cap+1):
        if not math.isfinite(rz) or rz<=0:return close('positive_residual_breakdown')
        ap=action(p)
        if not np.all(np.isfinite(ap)):return close('nonfinite_positive_action')
        den=dot(p,ap)
        if not math.isfinite(den) or den<=0:return close('positive_block_breakdown')
        alpha=rz/den
        if not math.isfinite(alpha):return close('nonfinite_alpha')
        x+=alpha*p;r-=alpha*ap
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(r)):return close('nonfinite_inner_state')
        if norm(r)/bn<=tolerance or it%25==0:
            ax=action(x)
            if not np.all(np.isfinite(ax)):return close('nonfinite_true_action')
            r=b-ax;error=finite(norm(r)/bn);checks.append(dict(iteration=it,error=error))
            if error is not None and error<=tolerance:return close('true_residual')
            z=r/diagonal;p=z.copy();rz=dot(r,z);continue
        z=r/diagonal;new=dot(r,z)
        if not math.isfinite(new) or new<=0:return close('positive_update_breakdown')
        beta=new/rz
        if not math.isfinite(beta):return close('nonfinite_beta')
        p=z+beta*p;rz=new
    return close(reason)

def triangular(h,g,k):
    y=np.zeros(k)
    for i in range(k-1,-1,-1):
        if not math.isfinite(h[i,i]) or h[i,i]==0:return None
        y[i]=(g[i]-dot(h[i,i+1:k],y[i+1:k]))/h[i,i]
    return y if np.all(np.isfinite(y)) else None

def fgmres(A,b,M,seed,tolerance,restart=24,cap=240):
    """Right flexible preconditioning; original-denominator true residual only."""
    x=seed.copy();bn=norm(b);it=0;checks=[];prec=[]
    def action(v):
        if not np.all(np.isfinite(v)):return np.full_like(v,np.nan)
        try:return A(v)
        except (AssertionError,ValueError,FloatingPointError):return np.full_like(v,np.nan)
    def check(label):
        error=None
        if math.isfinite(bn) and bn>0 and np.all(np.isfinite(x)):
            ax=action(x)
            if np.all(np.isfinite(ax)):error=finite(norm(b-ax)/bn)
        checks.append(dict(iteration=it,error=error,reason=label));return error
    def close(label):
        error=check(label)
        return x,dict(ok=error is not None and error<=tolerance,error=error,iterations=it,
                      reason=label,true_checks=checks,preconditioner_calls=prec)
    if bn==0 and np.all(b==0):return np.zeros_like(b),dict(ok=True,error=0.,iterations=0,reason='zero_rhs',true_checks=[],preconditioner_calls=[])
    if not math.isfinite(bn) or bn<=0 or not np.all(np.isfinite(b)) or not np.all(np.isfinite(x)):
        return close('nonfinite_or_underflow_initial_state')
    initial=check('initial_true_residual')
    if initial is not None and initial<=tolerance:return close('authenticated_seed_true_residual')
    while it<cap:
        ax=action(x)
        if not np.all(np.isfinite(ax)):return close('nonfinite_restart_action')
        r=b-ax;beta=norm(r)
        if not math.isfinite(beta) or beta<=0:return close('restart_norm_breakdown')
        base=x.copy();v=[r/beta];z=[];h=np.zeros((restart+1,restart));g=np.zeros(restart+1)
        cs=np.zeros(restart);sn=np.zeros(restart);g[0]=beta
        for j in range(min(restart,cap-it)):
            try:zz,info=M(v[j])
            except (AssertionError,ValueError,FloatingPointError):return close('preconditioner_refusal')
            prec.append(dict(iteration=it+1,details=info))
            if not np.all(np.isfinite(zz)):return close('nonfinite_preconditioner_partial')
            z.append(zz);w=action(zz)
            if not np.all(np.isfinite(w)):return close('nonfinite_arnoldi_action')
            # Two modified Gram-Schmidt passes; no normal equations or dense field solve.
            for _ in range(2):
                for k in range(j+1):
                    a=dot(v[k],w);h[k,j]+=a;w-=a*v[k]
            sub=norm(w);h[j+1,j]=sub
            if not math.isfinite(sub) or not np.all(np.isfinite(h[:j+2,j])):
                return close('nonfinite_arnoldi_coefficient')
            if sub>0:v.append(w/sub)
            for k in range(j):
                aa=h[k,j];bb=h[k+1,j]
                h[k,j]=cs[k]*aa+sn[k]*bb;h[k+1,j]=-sn[k]*aa+cs[k]*bb
            gamma=math.hypot(h[j,j],h[j+1,j]);it+=1
            if not math.isfinite(gamma) or gamma==0:return close('rank_or_givens_breakdown')
            cs[j]=h[j,j]/gamma;sn[j]=h[j+1,j]/gamma;h[j,j]=gamma;h[j+1,j]=0
            g[j+1]=-sn[j]*g[j];g[j]=cs[j]*g[j]
            estimate=abs(g[j+1])/bn
            need=(it%25==0 or estimate<=tolerance or sub==0 or j==restart-1 or it==cap)
            if need:
                y=triangular(h,g,j+1)
                if y is None:return close('small_triangular_refusal')
                candidate=base.copy()
                with np.errstate(over='ignore',invalid='ignore'):
                    for k in range(j+1):candidate+=y[k]*z[k]
                if not np.all(np.isfinite(candidate)):return close('nonfinite_candidate_retained_previous_partial')
                x=candidate
                error=check('estimate_or_periodic_true_residual')
                if error is not None and error<=tolerance:return close('true_residual')
            if sub==0:return close('terminal_arnoldi_true_residual_failed')
        # x was updated at the cycle end; each restart recomputes the actual residual.
    return close('iteration_allowance')

class BlockPreconditioner:
    def __init__(self,model,x,root):
        self.model=model;self.root=root;self.forms=native.NativeForms(x,model.r,model.z)
        self.mask=model.mask[0];self.w=self.forms.w;self.sw=np.sqrt(self.w)
        assert np.array_equal(self.forms.mask,model.mask[[1,2]])
        self.shape=self.forms.shape;nr,nz=len(model.r),len(model.z)
        self.a=np.zeros((32,nr,nz));self.c=np.zeros_like(self.a);self.b=np.zeros_like(self.a)
        self.kdiag=np.zeros((2,nr,nz));self.pdiag=np.zeros((nr,nz));self.kpsi=np.zeros_like(self.pdiag)
        self.pressure=[]
        for rr,vol,shapes,vv,alpha,nn,t in self.forms.quad:
            val,_,_=core.interpolate(x[0],shapes)
            coefficient=-native.pressure_coefficient(val,model.ep,self.fixed(model))
            assert np.all(np.isfinite(coefficient)) and np.all(coefficient>0)
            self.pressure.append(coefficient)
            for n,dr,dz,i,j in shapes:
                sl=(slice(None),slice(i,nr-1+i),slice(j,nz-1+j));ss=(slice(i,nr-1+i),slice(j,nz-1+j))
                self.a[sl]+=vol*n*(t+2*alpha*vv[:,0]**2)
                self.c[sl]+=vol*n*(t+2*alpha*vv[:,1]**2)
                self.b[sl]+=vol*n*(2*alpha*vv[:,0]*vv[:,1])
                self.kdiag[(0,)+ss]+=vol*(dr*dr+dz*dz+n*n/rr**2)
                self.kdiag[(1,)+ss]+=vol*(dr*dr+dz*dz)
                self.kpsi[ss]+=vol*(dr*dr+dz*dz);self.pdiag[ss]+=vol*coefficient*n*n
        self.a+=4*core.ELL**2*self.kdiag[0];self.c+=4*core.ELL**2*self.kdiag[1]
        # Restrict the principal node block to free components BEFORE inversion.
        both=self.forms.mask[0]&self.forms.mask[1];onlya=self.forms.mask[0]&~self.forms.mask[1]
        onlyc=self.forms.mask[1]&~self.forms.mask[0];self.ia=np.zeros_like(self.a);self.ic=np.zeros_like(self.c);self.ib=np.zeros_like(self.b)
        assert np.all(np.isfinite(self.a)) and np.all(np.isfinite(self.b)) and np.all(np.isfinite(self.c))
        scale=np.maximum(self.a[:,both],self.c[:,both]);aa=self.a[:,both]/scale;cc=self.c[:,both]/scale;bb=self.b[:,both]/scale
        det=aa*cc-bb*bb;assert np.all(scale>0) and np.all(det>0)
        self.ia[:,both]=cc/(scale*det);self.ic[:,both]=aa/(scale*det);self.ib[:,both]=-bb/(scale*det)
        self.ia[:,onlya]=1/self.a[:,onlya];self.ic[:,onlyc]=1/self.c[:,onlyc]
        assert all(np.all(np.isfinite(t)) for t in (self.ia,self.ic,self.ib))
        self.weight=float(np.sum(self.w));self.remainder=abs(1-self.weight)
        self.diagonal=self.kpsi+self.pdiag;self.diagonal[~self.mask]=1
        assert np.all(self.diagonal>0) and np.all(np.isfinite(self.diagonal))
    @staticmethod
    def fixed(model):return model.fgmres_fixed
    def split(self,v):return np.stack([v[1::2],v[2::2]],axis=1)
    def join(self,p,v):
        out=np.zeros(self.model.shape);out[0]=p;out[1::2]=v[:,0];out[2::2]=v[:,1]
        out[~self.model.mask]=0;return out
    def B(self,p):
        out=np.zeros(self.shape)
        for rr,vol,shapes,*_ in self.forms.quad:
            _,gr,gz=core.interpolate(p,shapes);value=self.sw[:,None,None,None]*np.stack([gr,gz])[None]
            core.add(out,value,np.zeros_like(value),np.zeros_like(value),vol,shapes)
        out[:,~self.forms.mask]=0;return out
    def BT(self,v):
        out=np.zeros_like(self.pdiag)
        for rr,vol,shapes,*_ in self.forms.quad:
            val,_,_=core.interpolate(v,shapes);gr=np.sum(self.sw[:,None,None]*val[:,0],axis=0);gz=np.sum(self.sw[:,None,None]*val[:,1],axis=0)
            core.add(out,np.zeros_like(gr),gr,gz,vol,shapes)
        out[~self.mask]=0;return out
    def K(self,p):
        out=np.zeros_like(p)
        for rr,vol,shapes,*_ in self.forms.quad:
            _,gr,gz=core.interpolate(p,shapes);core.add(out,np.zeros_like(gr),gr,gz,vol,shapes)
        out[~self.mask]=0;return out
    def mass(self,p):
        out=np.zeros_like(p)
        for (rr,vol,shapes,*_),coefficient in zip(self.forms.quad,self.pressure):
            val,_,_=core.interpolate(p,shapes);core.add(out,coefficient*val,np.zeros_like(val),np.zeros_like(val),vol,shapes)
        out[~self.mask]=0;return out
    def upper_inverse(self,v):
        out=np.zeros_like(v);out[:,0]=self.ia*v[:,0]+self.ib*v[:,1];out[:,1]=self.ib*v[:,0]+self.ic*v[:,1]
        out[:,~self.forms.mask]=0;return out
    def upper(self,v):
        out=np.zeros_like(v);out[:,0]=self.a*v[:,0]+self.b*v[:,1];out[:,1]=self.b*v[:,0]+self.c*v[:,1]
        out[:,~self.forms.mask]=0;return out
    def P(self,p):return (self.weight+self.remainder)*self.K(p)-self.BT(self.upper_inverse(self.B(p)))+self.mass(p)
    def block_action(self,v):
        vv=self.split(v);p=v[0]
        return self.join(self.K(p)-self.mass(p)-self.BT(vv),self.forms.apply(vv,core.ELL)-self.B(p))
    def physical(self,rhs):
        t,i1=pcg(lambda y:self.forms.apply(y,core.ELL),self.split(rhs),self.forms.diage)
        if not np.all(np.isfinite(t)):return np.full_like(rhs,np.nan),dict(first_native=i1)
        p,ip=pcg(self.P,rhs[0]+self.BT(t),self.diagonal)
        if not np.all(np.isfinite(p)):return np.full_like(rhs,np.nan),dict(first_native=i1,scalar=ip)
        v,i2=pcg(lambda y:self.forms.apply(y,core.ELL),self.B(p),self.forms.diage)
        out=self.join(p,t+v)
        return out,dict(first_native=i1,scalar=ip,second_native=i2,
                        incomplete_finite_partials_used=not(i1['ok'] and ip['ok'] and i2['ok']))
    def __call__(self,rhs):
        value,info=self.physical(self.root*rhs);return self.root*value,info

def implementation_controls():
    rows=[]
    specs=[('variable_SPD',[[4.,1.],[1.,3.]],[1.,2.],[.3,-.2],[1/11,7/11]),
           ('indefinite',[[2.,3.],[3.,-1.]],[1.,2.],[0.,0.],[7/11,-1/11]),
           ('compatible_singular',[[1.,1.],[1.,1.]],[2.,2.],[.2,.3],None),
           ('incompatible_singular',[[1.,0.],[0.,0.]],[1.,1.],[0.,0.],None)]
    for name,aa,bb,ss,exact in specs:
        a=np.array(aa);b=np.array(bb);seed=np.array(ss);counter=[0]
        def M(v):
            counter[0]+=1;d=np.array([1.+counter[0]%3,2.+counter[0]%2])
            return v/d,dict(variable_positive_diagonal=d.tolist())
        x,info=fgmres(lambda v:a@v,b,M,seed,1e-12,restart=4,cap=20)
        if exact is not None:err=finite(float(np.max(abs(x-np.array(exact)))));passed=info['ok'] and err is not None and err<=2e-11
        elif name=='compatible_singular':err=finite(abs(float(np.sum(x))-2));passed=info['ok'] and err is not None and err<=2e-11
        else:err=info['error'];passed=not info['ok'] and err is not None and err>=.7
        row=dict(name=name,linear=info,solution_error=err,passed=passed)
        raw=encode(row);path=BASE/f'{STEM}_CONTROL_{name}.npz'
        with path.open('xb') as f:np.savez_compressed(f,state=x,seed=seed,rhs=b,matrix=a,metadata=raw.decode());f.flush();os.fsync(f.fileno())
        path.chmod(0o444);row.update(file=path.name,sha256=sha(path));publish(path.name+'.commit.json',row)
        with np.load(path,allow_pickle=False) as n:
            assert set(n.files)=={'state','seed','rhs','matrix','metadata'}
            for key,value in (('state',x),('seed',seed),('rhs',b),('matrix',a)):assert np.array_equal(n[key],value,equal_nan=True)
            assert str(n['metadata'])==raw.decode()
        rows.append(row)
    return rows

def field_controls(block,H):
    ir=np.arange(block.model.shape[-2])[:,None];iz=np.arange(block.model.shape[-1])[None,:]
    p=np.sin(.17*(ir+1))*np.cos(.11*(iz+1));p[~block.mask]=0
    jj=np.arange(32)[:,None,None];v=np.empty(block.shape)
    v[:,0]=np.sin(.07*(jj+1)+.13*ir+.05*iz);v[:,1]=np.cos(.09*(jj+1)+.03*ir+.11*iz)
    v[:,~block.forms.mask]=0;dx=block.join(p,v)/block.root;other=block.join(.3*p,-.2*v)/block.root
    h=H(dx);hh=block.block_action(dx);b=block.B(p);bt=block.BT(v);u=block.upper_inverse(b)
    du=block.upper(v);dv=block.forms.apply(v,core.ELL);pp=block.P(p)
    kd=dot(p,block.K(p));md=dot(p,block.mass(p));pe=dot(p,pp)
    direct=(block.weight+block.remainder)*kd-2*dot(b,u)+dot(u,block.upper(u))+md
    gap=dot(v,du-dv);env=max(1e-30,abs(dot(v,du)),abs(dot(v,dv)))
    vals=[('whole_original_block_action',norm(h-hh)/max(1e-30,norm(h),norm(hh))),
          ('B_BT_exact_adjoint',abs(dot(b,v)-dot(p,bt))/max(1e-30,norm(b)*norm(v),norm(p)*norm(bt))),
          ('whole_original_symmetry',abs(dot(other,h)-dot(dx,H(other)))/max(1e-30,norm(other)*norm(h),norm(dx)*norm(H(other)))),
          ('positive_proxy_direct_energy',abs(pe-direct)/max(1e-30,(block.weight+block.remainder)*kd+md+2*abs(dot(b,u))+abs(dot(u,block.upper(u))))),
          ('upper_native_bound',max(0.,-gap)/env),('positive_scalar_proxy',max(0.,-pe)/max(1e-30,abs(pe),kd+md))]
    return [dict(name=n,error=finite(e),tolerance=2e-11,
                 signed_energy=finite(pe) if n=='positive_scalar_proxy' else None,
                 passed=math.isfinite(e) and e<=2e-11 and (pe>0 if n=='positive_scalar_proxy' else True)) for n,e in vals]

def save_state(name,step,x,history,identity,partial=None):
    suffix=f'STEP_{step:03d}' if partial is None else f'LINEAR_FAILED_{step:03d}'
    path=BASE/f'{STEM}_{name}_{suffix}.npz';ht=encode(history).decode();ident=encode(identity).decode()
    assert np.all(np.isfinite(x))
    mask=np.ones(x.shape,bool);mask[:,-1,:]=False;mask[:,:,-1]=False;mask[1::2,0,:]=False;mask[2::2,:,0]=False
    assert np.all(x[~mask]==0)
    partial_schema=None
    if partial is not None:
        assert partial.shape==x.shape and np.issubdtype(partial.dtype,np.floating)
        partial_schema=dict(shape=list(partial.shape),dtype=str(partial.dtype),finite=bool(np.all(np.isfinite(partial))),
                            mask_zero=bool(np.all(partial[~mask]==0)),unaccepted=True)
    sm=encode(dict(history_length=len(history),partial_schema=partial_schema)).decode()
    with path.open('xb') as f:
        fields=dict(state=x,history=ht,identity=ident,schema=sm)
        if partial is not None:fields['unaccepted_linear_partial']=partial
        np.savez_compressed(f,**fields);f.flush();os.fsync(f.fileno())
    path.chmod(0o444);commit=dict(file=path.name,sha256=sha(path),identity=identity,history_length=len(history),partial_schema=partial_schema)
    ch=publish(path.name+'.commit.json',commit)
    with np.load(path,allow_pickle=False) as n:
        assert np.array_equal(n['state'],x) and str(n['history'])==ht and str(n['identity'])==ident and str(n['schema'])==sm
        if partial is not None:assert np.array_equal(n['unaccepted_linear_partial'],partial,equal_nan=True)
    assert json.loads((BASE/(path.name+'.commit.json')).read_text())==commit
    return dict(file=path.name,sha256=commit['sha256'],commit_file=path.name+'.commit.json',commit_sha256=ch,
                history_length=len(history),partial_schema=partial_schema)


class DirectScalarPreconditioner(BlockPreconditioner):
    def prepare_scalar(self,x):
        self.scalar_arrays={};self.scalar_info=dict(status='ASSEMBLY_PENDING');self.scalar_controls=[];self.scalar_factor=None;self.scalar_failure_records=[]
        proxy=direct.Proxy(self.model,x,self.fixed(self.model))
        band,free=direct.assembly(proxy,self.scalar_arrays);self.scalar_free=free
        ir,iz=np.indices(self.mask.shape)
        for tag,p in [('smooth',np.sin(.17*(ir+1))*np.cos(.11*(iz+1))),('alternating',(-1.)**(ir+iz)*np.sin(.07*(ir+iz+1)))]:
            p[~self.mask]=0;original=self.P(p);assembled=direct.band_action(band,p.ravel()[free])
            env=(self.weight+self.remainder)*norm(self.K(p))+norm(self.BT(self.upper_inverse(self.B(p))))+norm(self.mass(p))
            er=norm(assembled-original.ravel()[free])/env if math.isfinite(env) and env>0 else math.inf
            self.scalar_controls.append(dict(name='original_proxy_band_'+tag,error=finite(er),tolerance=2e-11,passed=math.isfinite(er) and er<=2e-11))
            self.scalar_arrays['original_action_'+tag]=original;self.scalar_arrays['band_action_'+tag]=assembled
        self.scalar_factor,self.scalar_info=direct.factor_band(band,self.scalar_arrays)
        keep=('raw_band','free_full_indices','scalar_mask','scaled_band','factor','congruence_scale','original_action_smooth','original_action_alternating','band_action_smooth','band_action_alternating')
        self.scalar_arrays={k:v for k,v in self.scalar_arrays.items() if k in keep}
    def physical(self,rhs):
        if self.scalar_factor is None or not all(c['passed'] for c in self.scalar_controls):raise ValueError('Scalar factor/control refusal')
        t,i1=pcg(lambda y:self.forms.apply(y,core.ELL),self.split(rhs),self.forms.diage)
        if not np.all(np.isfinite(t)):return np.full_like(rhs,np.nan),dict(first_native=i1)
        sr=rhs[0]+self.BT(t);arrays={'scalar_rhs':sr.ravel()[self.scalar_free].copy()};f,scale=self.scalar_factor
        try:error,history=direct.refined_solve(self,f,scale,self.scalar_free,arrays['scalar_rhs'],arrays,'scalar')
        except (AssertionError,ValueError,FloatingPointError) as exc:
            history=[dict(reason='scalar_refinement_exception',exception=type(exc).__name__,detail=str(exc))]
            self.scalar_failure_records.append(save_scalar_failure(self,arrays,history,dict(ok=False,error=None,reason='scalar_refinement_exception')));raise
        ip=dict(ok=math.isfinite(error) and error<=1e-10,error=finite(error),iterations=max(0,len(history)-1),reason='original_proxy_true_residual',true_checks=history,finite_partial=bool(np.all(np.isfinite(arrays['scalar_solution']))),factor_reused=True)
        if not ip['ok']:
            self.scalar_failure_records.append(save_scalar_failure(self,arrays,history,ip))
            return np.full_like(rhs,np.nan),dict(first_native=i1,scalar=ip)
        p=np.zeros_like(sr);p.ravel()[self.scalar_free]=arrays['scalar_solution']
        v,i2=pcg(lambda y:self.forms.apply(y,core.ELL),self.B(p),self.forms.diage)
        return self.join(p,t+v),dict(first_native=i1,scalar=ip,second_native=i2,incomplete_finite_partials_used=not(i1['ok'] and i2['ok']))

def save_scalar_factor(name,outer,identity,block):
    arrays=block.scalar_arrays;schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}
    metadata=dict(owner=OWNER,identity=identity,outer=outer,physical_state_checkpoint=block.physical_state_checkpoint,factor=block.scalar_info,controls=block.scalar_controls,schema=schema)
    text=encode(metadata).decode();metadata=json.loads(text);path=BASE/f'{STEM}_{name}_SCALAR_FACTOR_{outer:03d}.npz'
    with path.open('xb') as f:np.savez_compressed(f,scalar_factor_metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    path.chmod(0o444);record=dict(kind='scalar_proxy_factor',file=path.name,sha256=sha(path),metadata=metadata)
    ch=publish(path.name+'.commit.json',record)
    with np.load(path,allow_pickle=False) as n:
        assert str(n['scalar_factor_metadata'])==text and set(n.files)==set(arrays)|{'scalar_factor_metadata'}
        for k,v in arrays.items():assert np.array_equal(n[k],v,equal_nan=True)
    return dict(record,commit_file=path.name+'.commit.json',commit_sha256=ch)

def save_scalar_failure(block,arrays,history,info):
    assert info['ok'] is False
    fields={k:v for k,v in arrays.items() if k in ('scalar_rhs','scalar_solution','scalar_original_action')}
    fields.update(free_full_indices=block.scalar_free,scalar_mask=block.mask)
    schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in fields.items()}
    metadata=dict(owner=OWNER,identity=block.case_identity,outer=block.newton_outer,physical_state_checkpoint=block.physical_state_checkpoint,unaccepted=True,history=history,scalar=info,
                  coordinates='physical scalar components in factor free_full_indices order',factor_checkpoint=block.scalar_factor_record,
                  original_proxy_source_sha256=PINS['cross_u_ngc3198_coupled_fgmres_recovery_v004.py'],
                  factor_helper_source_sha256=PINS['cross_u_direct_scalar_proxy_controls_v001.py'],schema=schema)
    text=encode(metadata).decode();metadata=json.loads(text)
    path=BASE/f'{STEM}_{block.case_name}_SCALAR_FAILED_{block.newton_outer:03d}_{len(block.scalar_failure_records):03d}.npz'
    with path.open('xb') as f:np.savez_compressed(f,scalar_failure_metadata=text,**fields);f.flush();os.fsync(f.fileno())
    path.chmod(0o444);record=dict(kind='scalar_proxy_failure',file=path.name,sha256=sha(path),metadata=metadata)
    ch=publish(path.name+'.commit.json',record)
    with np.load(path,allow_pickle=False) as n:
        assert str(n['scalar_failure_metadata'])==text and set(n.files)==set(fields)|{'scalar_failure_metadata'}
        for k,v in fields.items():assert np.array_equal(n[k],v,equal_nan=True)
    return dict(record,commit_file=path.name+'.commit.json',commit_sha256=ch)


def solve(model,name,identity,x,partial):
    started=time.monotonic();history=[];diagnostics=[];factor_records=[];scalar_failures=[];checkpoints=[save_state(name,0,x,history,identity)]
    _,pre0,_=model.residual(np.zeros(model.shape));scale=norm(model.rhs/np.sqrt(pre0))
    assert math.isfinite(scale) and scale>0;status='NEWTON_ALLOWANCE'
    for outer in range(40):
        r,pre,H=model.residual(x);root=np.sqrt(pre);b=-r/root;error=norm(b)/scale
        if error<=1e-8:status='CONVERGED';break
        target=min(.5,max(1e-6,.5*math.sqrt(error)))
        try:
            block=DirectScalarPreconditioner(model,x,root)
            block.case_name=name;block.newton_outer=outer;block.case_identity=identity;block.physical_state_checkpoint=checkpoints[-1]
            CONTEXT.update(case=name,outer=outer,stage='scalar_proxy_preparation')
            try:block.prepare_scalar(x)
            except (AssertionError,ValueError,FloatingPointError) as exc:
                block.scalar_info=dict(status='ASSEMBLY_OR_FACTOR_REFUSAL',reason=type(exc).__name__,detail=str(exc),helper_context=dict(direct.CONTEXT));raise
            finally:
                if hasattr(block,'scalar_arrays'):
                    block.scalar_factor_record=save_scalar_factor(name,outer,identity,block);factor_records.append(block.scalar_factor_record)
            assert block.scalar_factor is not None and all(c['passed'] for c in block.scalar_controls),'Scalar factor/control refused'
            if outer==0:diagnostics=field_controls(block,H)
            diagnostics+=block.scalar_controls
        except (AssertionError,ValueError,FloatingPointError) as exc:
            diagnostics=[dict(name='block_construction_or_control_refusal',passed=False,reason=type(exc).__name__)];status='BLOCK_IMPLEMENTATION_CONTROL_FAILED';break
        if not all(t['passed'] for t in diagnostics):status='BLOCK_IMPLEMENTATION_CONTROL_FAILED';break
        def A(v):
            with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
                physical=v/root
                if not np.all(np.isfinite(physical)):return np.full_like(v,np.nan)
                return H(physical)/root
        valid=outer==0 and partial is not None and partial.shape==b.shape and np.all(np.isfinite(partial)) and np.all(partial[~model.mask]==0)
        seed=partial.copy() if valid else np.zeros_like(b)
        delta,linear=fgmres(A,b,block,seed,target)
        scalar_failures.extend(block.scalar_failure_records)
        row=dict(outer=outer,error=error,inexact_target=target,linear=linear,
                 parent_whitened_partial_used=bool(valid),parent_partial_rejected=bool(outer==0 and partial is not None and not valid))
        if not linear['ok']:
            row['raw_partial_nonfinite']=not bool(np.all(np.isfinite(delta)))
            if row['raw_partial_nonfinite']:row['raw_partial_disposition']='nonfinite_unaccepted_array_preserved'
            history.append(row)
            checkpoints.append(save_state(name,outer,x,history,identity,delta))
            status='LINEAR_FAILED';break
        delta=delta/root;accepted=False;guard=merit=0
        for back in range(32):
            step=2.**(-back);candidate=x+step*delta
            try:cr,_=model.residual(candidate,False);candidate_error=norm(cr/root)/scale
            except (ValueError,AssertionError,FloatingPointError):guard+=1;continue
            if math.isfinite(candidate_error) and candidate_error<=(1-1e-4*step)*error:
                x=candidate;accepted=True;row.update(step=step,candidate_error=candidate_error);break
            merit+=1
        row.update(accepted=accepted,domain_or_finite_rejections=guard,merit_rejections=merit);history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        checkpoints.append(save_state(name,outer+1,x,history,identity))
        print('COUPLED_FGMRES',name,'NEWTON',outer+1,'ERROR',candidate_error,'STEP',step,flush=True)
    r,pre,_=model.residual(x);error=norm(r/np.sqrt(pre))/scale
    if error<=1e-8:status='CONVERGED'
    force=np.gradient(x[0,:,0],model.r,edge_order=2);rows=[]
    for obs in core.observation_rows():
        g=float(np.interp(obs['R'],model.r,force));v2=obs['R']*core.A0_V*g;v=math.sqrt(v2) if v2>=0 else None
        rows.append(dict(obs,radial_force_a0=g,velocity_squared=v2,model_velocity=v,residual=None if v is None else v-obs['velocity']))
    return dict(identity=identity,status=status,numerical_residual=error,history=history,own_checkpoints=checkpoints,scalar_factor_checkpoints=factor_records,scalar_failure_checkpoints=scalar_failures,block_controls=diagnostics,rows=rows,
                elapsed_seconds=time.monotonic()-started,readout_qualified=False,
                physical_flags=dict(refinement_qualified=False,full_metric_qualified=False,FLRW_junction_qualified=False,
                                    formation_qualified=False,stability_qualified=False,joint_superiority_qualified=False))

def final_recheck(source):
    auth();selected_prefix();assert sha(__file__)==source
    for name,(h,receipt) in RECEIPTS.items():
        assert sha(BASE/name)==h
        for n,k in receipt['output_sha256'].items():assert sha(BASE/n)==k
    for p in BASE.glob(STEM+'_*.npz'):
        cp=p.with_name(p.name+'.commit.json');commit=json.loads(cp.read_text());native_tree(commit)
        assert commit.get('sha256')==sha(p) and commit.get('file')==p.name
        with np.load(p,allow_pickle=False) as n:
            if 'state' in n:assert np.all(np.isfinite(n['state']))
            if 'scalar_failure_metadata' in n:
                metadata=json.loads(str(n['scalar_failure_metadata']));native_tree(metadata)
                assert commit['kind']=='scalar_proxy_failure' and commit['metadata']==metadata
                assert set(n.files)==set(metadata['schema'])|{'scalar_failure_metadata'}
                for key,s in metadata['schema'].items():
                    a=n[key];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
                case=json.loads((BASE/f"{STEM}_{metadata['identity']['case']}_CASE.json").read_text());assert case['identity']==metadata['identity']
                records=[r for r in case['scalar_failure_checkpoints'] if r['file']==p.name];assert len(records)==1
                assert dict(commit,commit_file=cp.name,commit_sha256=sha(cp))==records[0]
                factor=metadata['factor_checkpoint'];assert factor in case['scalar_factor_checkpoints']
                assert sha(BASE/factor['file'])==factor['sha256'] and sha(BASE/factor['commit_file'])==factor['commit_sha256']
                state=metadata['physical_state_checkpoint'];assert state in case['own_checkpoints']
                assert sha(BASE/state['file'])==state['sha256'] and sha(BASE/state['commit_file'])==state['commit_sha256'] and metadata['unaccepted'] is True
            elif 'scalar_factor_metadata' in n:
                metadata=json.loads(str(n['scalar_factor_metadata']));native_tree(metadata)
                assert commit['kind']=='scalar_proxy_factor' and commit['metadata']==metadata
                assert set(n.files)==set(metadata['schema'])|{'scalar_factor_metadata'}
                for key,s in metadata['schema'].items():
                    a=n[key];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
                case=json.loads((BASE/f"{STEM}_{metadata['identity']['case']}_CASE.json").read_text())
                assert case['identity']==metadata['identity']
                state=metadata['physical_state_checkpoint'];assert state in case['own_checkpoints']
                assert sha(BASE/state['file'])==state['sha256'] and sha(BASE/state['commit_file'])==state['commit_sha256']
                records=[r for r in case['scalar_factor_checkpoints'] if r['file']==p.name];assert len(records)==1
                assert dict(commit,commit_file=cp.name,commit_sha256=sha(cp))==records[0]
            elif 'identity' in n:
                identity=json.loads(str(n['identity']));history=json.loads(str(n['history']))
                schema=json.loads(str(n['schema']));native_tree(identity);native_tree(history);native_tree(schema)
                assert commit['identity']==identity and commit['history_length']==len(history)==schema['history_length']
                assert commit['partial_schema']==schema['partial_schema']
                case=json.loads((BASE/f"{STEM}_{identity['case']}_CASE.json").read_text());native_tree(case)
                assert case['identity']==identity and case['history'][:len(history)]==history
                records=[r for r in case['own_checkpoints'] if r['file']==p.name];assert len(records)==1
                record=records[0];assert record['sha256']==sha(p) and record['commit_sha256']==sha(cp)
                assert record['history_length']==len(history) and record['partial_schema']==schema['partial_schema']
                state=n['state'];mask=np.ones(state.shape,bool);mask[:,-1,:]=False;mask[:,:,-1]=False;mask[1::2,0,:]=False;mask[2::2,:,0]=False
                assert np.all(state[~mask]==0)
                if 'unaccepted_linear_partial' in n:
                    a=n['unaccepted_linear_partial'];s=schema['partial_schema']
                    assert a.shape==state.shape and np.issubdtype(a.dtype,np.floating)
                    assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))),mask_zero=bool(np.all(a[~mask]==0)),unaccepted=True)
                    assert history[-1]['raw_partial_nonfinite']==(not s['finite'])
                else:assert schema['partial_schema'] is None
            else:
                assert set(n.files)=={'state','seed','rhs','matrix','metadata'}
                for key in ('state','seed','rhs','matrix'):assert np.issubdtype(n[key].dtype,np.floating) and np.all(np.isfinite(n[key]))
                assert n['state'].shape==n['seed'].shape==n['rhs'].shape and n['matrix'].shape==(n['state'].size,n['state'].size)
                row=json.loads(str(n['metadata']));native_tree(row)
                assert dict(row,file=p.name,sha256=sha(p))==commit

def close(source,manifest,result):
    final_recheck(source);result['manifest']=manifest;rh=publish(STEM+'_RESULT.json',result)
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    publish(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),source_sha256=source,started=manifest['started'],
                                    closed=now(),result_sha256=rh,output_sha256=outputs))
    print('COUPLED_FGMRES_BATCH_CLOSED',result['status'],flush=True)


def main():
    global np,core,native,direct,OWNER
    auth();source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing outputs preserved'
    for name in (PARENT+'_RECEIPT.json','CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json','CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json','CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json',DIRECT+'_RECEIPT.json'):closed_receipt(name)
    control_result=json.loads((BASE/(DIRECT+'_RESULT.json')).read_text())
    assert control_result['status']=='CONTROL_PASS' and control_result['planned_predicates']==control_result['completed_predicates']==51
    assert len(control_result['implementation_controls'])==3 and len(control_result['cases'])==4
    assert all(c['passed'] for c in control_result['implementation_controls']) and all(c['status']=='CONTROL_PASS' and len(c['controls'])==12 and all(t['passed'] for t in c['controls']) for c in control_result['cases'])
    assert all(v is False for v in control_result['qualification'].values())
    active_manifest,cases=selected_prefix()
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001');native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
    direct=importlib.import_module('cross_u_direct_scalar_proxy_controls_v001');direct.np=np;direct.core=core;direct.native=native;direct.auth();auth()
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=source,started=now())
    manifest=dict(owner='root',pid=OWNER['pid'],started=OWNER['started'],source_sha256=source,input_sha256=inputs(),physics_changes=[],no_automatic_resume=True,
                  parent_batch_closed=False,completed_parent_cases_only=[c['identity']['case'] for c in cases],parent_prefix_manifest=active_manifest,parent_terminal_cases_preserved=cases,
                  parent_cases_preserved=parent['cases'],parent_controls_preserved=parent['controls'],direct_controls_preserved=control_result,
                  numerical_change='Replace only scalar positive-proxy PCG by sealed stable band factor, once per Newton; original P corrections',
                  limits=dict(restart=24,outer_linear=240,inner_native=100,inner_native_true_tolerance=.01,scalar_true_tolerance=1e-10,scalar_corrections=3,newton=40,final_residual=1e-8))
    mh=publish(STEM+'_MANIFEST.json',manifest);controls=implementation_controls();results=[]
    if not all(t['passed'] for t in controls):
        close(source,manifest,dict(status='IMPLEMENTATION_CONTROL_FAILED',controls=controls,cases=[],original_cases=parent['cases'],completed_parent_cases=cases,joint_superiority_qualified=False));return 3
    for case in cases:
        old=case['identity'];name=old['case'];x,partial,parent_history,seals=recover_selected(case)
        model=core.Model(np.array(old['r_kpc']),np.array(old['z_kpc']),32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
        model.fgmres_fixed=fixed;assert x.shape==model.shape and np.all(x[~model.mask]==0)
        identity=dict(old,direct_scalar_manifest_sha256=mh,direct_scalar_source_sha256=source,direct_scalar_parent_state=seals)
        result=solve(model,name,identity,x,partial)
        result.update(parent_case=case,parent_checkpoint_history=parent_history,ancestral_history=case.get('ancestral_history',[]),ancestral_checkpoint_history=case.get('ancestral_checkpoint_history',[]))
        auth();selected_prefix();assert sha(__file__)==source;publish(f'{STEM}_{name}_CASE.json',result);results.append(result)
    close(source,manifest,dict(status='RECOVERY_OUTCOMES_RETAINED',controls=controls,cases=results,original_cases=parent['cases'],completed_parent_cases=cases,joint_superiority_qualified=False))
    return 0 if all(c['status']=='CONVERGED' for c in results) else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    try:code=main()
    except Exception:
        if OWNER is not None:
            publish(STEM+'_ERROR.json',dict(status='EXECUTION_ERROR_PRESERVED',owner=OWNER,failed=now(),context=CONTEXT,traceback=traceback.format_exc(),preserved_outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}))
        raise
    raise SystemExit(code)
