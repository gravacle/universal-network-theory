"""Unexecuted bounded right-FGMRES recovery; unchanged S_cross Q1 disk action."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os, time

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004'
PARENT='CROSS_U_NGC3198_MINRES_RECOVERY_V003'
AUTHOR_DRAFT=False
PINS={'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1',
 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76',
 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json': '720cbaf0902285d35dc3a50d59f81d266431c7d91b4985eb19ab822b0b14413b',
 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': '337e7b82f5270fc2e3cd4823cb95c92600acde45dc6adbc66a98c7ebb1bef400',
 'cross_u_ngc3198_partial_recovery_v002.py': '6f52dddd8ec0fbf844f9174c92e80d3700b51dcc8432709cd1d88c81811b1925',
 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002.md': 'c236db1e798d4df086460e880d3515612dea127335eb85c4defde842e4589400',
 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_MANIFEST.json': 'a1756ed9cec5bff2273088008ca6410c9c9a6f769f0fb92c6750c2601a89f687',
 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RESULT.json': 'dcc18c6714c7f4d427a452eb11ba86b91496bf305925a4a2b22a0c3d87779963',
 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': 'c72830fb31defeae5443beed55eec910b08c2bf520a45f14853c9cdfe59950a1',
 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_MANIFEST.json': 'b83b93c6c64e5a9f356e849e0688a5690073f4d07c756ee67fd1390c8671471c',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5',
 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RESULT.json': 'd20f71731fe822a5af9e7d78408a346b5414752d9378a2a062a1e4ae5f16b871',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': '1f1f1aa4c06cf74f54875aefed42dc347932debc4a321211a96a5b3623f7331a',
 'CROSS_U_NGC3198_COUPLED_FGMRES_RECOVERY_V004.md': '74e026fb4bfb331820fa18758bae815b7abb27ac442a2b126a43f0ae8d6418c3'}
STATE_BINDINGS={'E1em05_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_CASE.json',
                    'case_sha256': 'aacab61f915a1bc4347377da1d5b5b7bdcd515ad519cd5b1661ce8c61c71d299',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz',
                    'sha256': '2dd4897d541dc74543bc7185894a0879d5a4ff99c090bf4bf4a369eb29cdef15',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': '5fe0d9fe062eecbcb65997965569ab58e4f56e6a742ec4df84728691bd571b2f'},
 'E1em05_HI0_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_CASE.json',
                    'case_sha256': '6bcdc0ee7e02a3367473dd99185bfd9d1fe5e8f51683d329b4509e77d90fcd75',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz',
                    'sha256': '1b5edc61af9007d840a77f614fe10a17e2fc4c4caf802313ccc84ab7ec6e5e6d',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': 'f708e09a4f08b8305e3917a453e41b7dcd78ed85de7a3d9d5071119c95ad533b'},
 'E1em05_HI1_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H20_CASE.json',
                    'case_sha256': '7125418f4c3e9aa2d6dbf066eb2d85a8d9713a448ab56a2da168a9447c00655c',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H20_LINEAR_FAILED_001.npz',
                    'sha256': '3835a9e0833bc5bd1c82e2b4f0a637612db61b1dabf27fb63a4e101cedba45b2',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H20_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': '69687b54f605ec9b317adf857b9069d1901cfc50d723e0b1334a8717de07129f'},
 'E1em05_HI1_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H21_CASE.json',
                    'case_sha256': '9c177123ef6ae60734f2dd1e19833410509ced083d6fea737344d61581b97cfc',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H21_STEP_040.npz',
                    'sha256': '6300d8a187c4d3837e885ed37bb00997c413c98a8010cfd53dab6bbbbf36d0f2',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI1_H21_STEP_040.npz.commit.json',
                    'commit_sha256': '68ee4a239055c42f84bc0605b8f5defd0cbfa871c1475ee333b0822fe53c55c9'},
 'E1em04_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_CASE.json',
                    'case_sha256': 'e9313e8356bb58177a6b891a028d0293b1feb0a81997f32e997623a5ad0ff7be',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz',
                    'sha256': 'c0b9f237e81f8d8d4d62fb2fa5901aae16711bfc31c0cc70979f687d01ff2aa4',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz.commit.json',
                    'commit_sha256': '14e42f5dea351040f26cd0b14d237a56e1e21a167d4c8e80453fc222bceec5b4'},
 'E1em04_HI0_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H21_CASE.json',
                    'case_sha256': 'd4e8640a4774494ea7d4cbb15ba2027db12c9063812ff7ba9b2862099aebb2f3',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H21_LINEAR_FAILED_000.npz',
                    'sha256': 'ee69462aeaa47ab18ec7a5043ace540df0b28f1f183b9bdd591c2fd9f044e272',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H21_LINEAR_FAILED_000.npz.commit.json',
                    'commit_sha256': '89d0f7ac5210226dee721dccb8a5b1b8d31852b07916d6c7ac23326263891866'},
 'E1em04_HI1_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H20_CASE.json',
                    'case_sha256': 'f53a33ded6da155028414c856ea792e4552ab95dab148174e39415e586eb02fc',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H20_LINEAR_FAILED_001.npz',
                    'sha256': 'f1150c9b583230661721cd73b32e2f2b2b29e8cc1564a10da6a9cddbd6372099',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H20_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': 'f47db0b528e8233e9b739f9372300411f3c35342f2e74efb0e2c5ff816e4f5bc'},
 'E1em04_HI1_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H21_CASE.json',
                    'case_sha256': '3c5aa7073bae8afc892f8dc128f985fe157302966040675ad6aa6e116baa3169',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H21_LINEAR_FAILED_001.npz',
                    'sha256': '9f708762421a0df52c8676f925a119f0531ea852be17d57ea7b3328356fc756f',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI1_H21_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': '2d3bc30053d3f5bdf7ebf41a15e5782a86dab84c3a4a9883f59431e328623e94'},
 'E1em03_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_CASE.json',
                    'case_sha256': '51c138f74b213b6fa455329c578d071eb99eeacd590efd81977ee8f1c715ffc8',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz',
                    'sha256': 'fe0b587bb8a979e260d991216451fb61adc19d3afba37ec6f100f17c0afab24d',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': '15da0758f2cebf87c684d225703c7327a3b9495751fd0445462b239f38aa215a'},
 'E1em03_HI0_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H21_CASE.json',
                    'case_sha256': '750a2e459180a1aba82793ae7696597ab9a15814e1b0fea2890cd3b1c6d3b628',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H21_LINEAR_FAILED_001.npz',
                    'sha256': '177c6d3ac0a0762ba81522a57827ad9706061c505e5c1899a0072c696e9db612',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H21_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': 'c3a1401fd0b301118f7e85dc889ecefe9f35565de77476ee86d7c847ab6b8b69'},
 'E1em03_HI1_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H20_CASE.json',
                    'case_sha256': 'a329f21517bbbc6abd9f8532662c6dc9606e0daf2b6f7a1db2de658acbcb9982',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H20_LINEAR_FAILED_001.npz',
                    'sha256': '21f122e60708a180339eb41506ca42c9a77d1b80f8f24cc8764fc15cdb44b06e',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H20_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': 'b503f8204e9aa4dc2c944d3d10e221ec0e08645b126aa1f4b0f151d3177edb05'},
 'E1em03_HI1_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H21_CASE.json',
                    'case_sha256': '9b9be2c6ee955dbc2a310e9e55e9c12ea7da38f337e2bac4ccbf746756340603',
                    'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H21_LINEAR_FAILED_001.npz',
                    'sha256': '1d9528f57682ecb21e71cf5e1426eb3faf0798d018b782aeb166fce078e3efe9',
                    'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI1_H21_LINEAR_FAILED_001.npz.commit.json',
                    'commit_sha256': 'da3ad6dac5efd5236ff3c6b1defd3955cd0e82bbbe40f16169571f7312d44cd3'}}
CORE_INPUT_PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
np=core=native=None
RECEIPTS={}

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
def inputs():
    pins=dict(CORE_INPUT_PINS)
    for n,h in PINS.items():
        if n in pins:assert pins[n]==h
        pins[n]=h
    for d in STATE_BINDINGS.values():
        for n,h in ((d['case_file'],d['case_sha256']),(d['file'],d['sha256']),
                    (d['commit_file'],d['commit_sha256'])):
            if n in pins:assert pins[n]==h
            pins[n]=h
    return pins
def auth():
    assert not AUTHOR_DRAFT and PINS and len(STATE_BINDINGS)==12,'Unexecuted author draft'
    for n,h in inputs().items():assert len(h)==64 and sha(BASE/n)==h,('changed input',n)
    if core is not None:core.authenticate();assert core.PINS==CORE_INPUT_PINS
def closed_receipt(name):
    h=PINS[name];assert sha(BASE/name)==h
    if name in RECEIPTS:assert RECEIPTS[name][0]==h;return RECEIPTS[name][1]
    r=json.loads((BASE/name).read_text());native_tree(r)
    assert r['owner']=='root' and type(r['pid']) is int and r['pid']>0
    assert datetime.fromisoformat(r['started'])<datetime.fromisoformat(r['closed'])
    assert r['output_sha256']
    for n,k in r['output_sha256'].items():assert sha(BASE/n)==k,('changed closed output',n)
    RECEIPTS[name]=(h,r);return r
def norm(a):return float(np.linalg.norm(a))
def dot(a,b):return float(np.sum(a*b))

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

def recover(case,receipt):
    d=STATE_BINDINGS[case['identity']['case']]
    assert json.loads((BASE/d['case_file']).read_text())==case
    for key,hkey in (('file','sha256'),('commit_file','commit_sha256')):
        assert receipt['output_sha256'][d[key]]==d[hkey]==sha(BASE/d[key])
    commit=json.loads((BASE/d['commit_file']).read_text());assert commit['file']==d['file'] and commit['sha256']==d['sha256']
    with np.load(BASE/d['file'],allow_pickle=False) as n:
        assert {'state','history','identity'}<=set(n.files)
        x=n['state'].copy();history=json.loads(str(n['history']));identity=json.loads(str(n['identity']))
        partial=n['unaccepted_linear_partial'].copy() if 'unaccepted_linear_partial' in n else None
    native_tree(history);native_tree(identity)
    assert identity==commit['identity']==case['identity'] and history==case['history'] and np.all(np.isfinite(x))
    if partial is not None:assert partial.shape==x.shape and np.issubdtype(partial.dtype,np.floating)
    return x,partial,history,d

def solve(model,name,identity,x,partial):
    started=time.monotonic();history=[];diagnostics=[];checkpoints=[save_state(name,0,x,history,identity)]
    _,pre0,_=model.residual(np.zeros(model.shape));scale=norm(model.rhs/np.sqrt(pre0))
    assert math.isfinite(scale) and scale>0;status='NEWTON_ALLOWANCE'
    for outer in range(40):
        r,pre,H=model.residual(x);root=np.sqrt(pre);b=-r/root;error=norm(b)/scale
        if error<=1e-8:status='CONVERGED';break
        target=min(.5,max(1e-6,.5*math.sqrt(error)))
        try:
            block=BlockPreconditioner(model,x,root)
            if outer==0:diagnostics=field_controls(block,H)
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
    return dict(identity=identity,status=status,numerical_residual=error,history=history,own_checkpoints=checkpoints,block_controls=diagnostics,rows=rows,
                elapsed_seconds=time.monotonic()-started,readout_qualified=False,
                physical_flags=dict(refinement_qualified=False,full_metric_qualified=False,FLRW_junction_qualified=False,
                                    formation_qualified=False,stability_qualified=False,joint_superiority_qualified=False))

def final_recheck(source):
    auth();assert sha(__file__)==source
    for name,(h,receipt) in RECEIPTS.items():
        assert sha(BASE/name)==h
        for n,k in receipt['output_sha256'].items():assert sha(BASE/n)==k
    for p in BASE.glob(STEM+'_*.npz'):
        cp=p.with_name(p.name+'.commit.json');commit=json.loads(cp.read_text());native_tree(commit)
        assert commit.get('sha256')==sha(p) and commit.get('file')==p.name
        with np.load(p,allow_pickle=False) as n:
            assert np.all(np.isfinite(n['state']))
            if 'identity' in n:
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
    global np,core,native
    auth();source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing outputs preserved'
    receipt=closed_receipt(PARENT+'_RECEIPT.json')
    assert receipt['source_sha256']==PINS['cross_u_ngc3198_minres_recovery_v003.py']
    for name in ('CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json','CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json'):
        closed_receipt(name)
    closed_receipt('CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json')
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());native_tree(parent)
    assert receipt['result_sha256']==sha(BASE/(PARENT+'_RESULT.json')) and len(parent['cases'])==16
    names=[c['identity']['case'] for c in parent['cases']];assert len(set(names))==16
    assert set(STATE_BINDINGS)=={c['identity']['case'] for c in parent['cases'] if c['identity']['eps']!=1e-6}
    original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001')
    native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core;auth()
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,input_sha256=inputs(),
                  physics_changes=[],no_automatic_resume=True,parent_cases_preserved=parent['cases'],parent_controls_preserved=parent['controls'],
                  numerical_change='Frozen-whitening right flexible GMRES and bounded coupled positive block preconditioner',
                  limits=dict(restart=24,outer_linear=240,inner_native=100,inner_scalar=100,inner_true_tolerance=.01,newton=40,final_residual=1e-8))
    mh=publish(STEM+'_MANIFEST.json',manifest);control=implementation_controls();results=[]
    if not all(t['passed'] for t in control):
        close(source,manifest,dict(status='IMPLEMENTATION_CONTROL_FAILED',controls=control,cases=[],original_cases=parent['cases'],joint_superiority_qualified=False));return 3
    for case in parent['cases']:
        old=case['identity'];name=old['case']
        if old['eps']==1e-6:
            result=case  # Exact original four ineligible case objects; no relabeling.
        else:
            x,partial,parent_history,seals=recover(case,receipt)
            model=core.Model(np.array(old['r_kpc']),np.array(old['z_kpc']),32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
            model.fgmres_fixed=fixed;assert x.shape==model.shape and np.all(x[~model.mask]==0)
            identity=dict(old,fgmres_manifest_sha256=mh,fgmres_source_sha256=source,parent_state=seals)
            result=solve(model,name,identity,x,partial)
            result.update(parent_case=case,parent_checkpoint_history=parent_history,
                          ancestral_history=case.get('ancestral_history',[]),ancestral_checkpoint_history=case.get('ancestral_checkpoint_history',[]))
        auth();assert sha(__file__)==source;publish(f'{STEM}_{name}_CASE.json',result);results.append(result)
    close(source,manifest,dict(status='RECOVERY_OUTCOMES_RETAINED',controls=control,cases=results,original_cases=parent['cases'],joint_superiority_qualified=False))
    return 0 if all(c['status']=='CONVERGED' or c['identity']['eps']==1e-6 for c in results) else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())
