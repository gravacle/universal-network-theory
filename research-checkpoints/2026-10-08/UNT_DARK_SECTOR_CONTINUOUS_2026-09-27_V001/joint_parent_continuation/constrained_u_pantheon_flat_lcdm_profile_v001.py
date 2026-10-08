"""Guarded same-1590-measurement flat-LCDM profile; root execution only."""
import argparse
import ast
import base64
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import time
import traceback
import urllib.parse
import zlib

AUTHOR_DRAFT = False
J = Path(__file__).resolve().parent
HERE = J
STEM = 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001'
PARENT = 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001'
OLD = 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002'
HELPER_SOURCE = 'constrained_u_clock_gradient_bbn_pantheon_profile_v002.py'
PINS = {'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001.md': '9125291f442dfd3aebb63199de2c707e3f86ec3d02c236f87d606772f9a879ec', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'constrained_u_clock_gradient_bbn_pantheon_profile_v002.py': '976fc4c2b91a5b84e54723ba2d7bdf0508fd5275e6d35dfd615523869744b917', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RESULT.json': '8ccfba9bbded7faf0c2c3eb6250fb49f7d7f2951dbd71fc305f42cb81a3cd67b', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': '4ea9d4615ee248ffd0143cf862348bbc3648d080ac5e6d8cde3ba1dabdca2e3b', 'PANTHEON_INPUT_SELECTION_V001.md': 'be486e54eed8acc14f345aa8382cdc8aec8e6f448f9691d876bc5cd6adf71fa2', 'fetch_pantheon_reference_v001.py': '03d001317e99dedbdc43838abfd9eab46e62e339e021e3a2cea518e1f3b1a5f3', 'pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json': 'c2408ce5f9914c349d926a89e8124adc8828b7f885075aa8a08e0d5a9e4357bb', 'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json': '58317db1be2c6591309a206f6ac6b54d564218f596f639457389eaaa5945a573', 'pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json': '1be77d822136ac140b6e1bb7b260133c6d91fcd901e34cd002ef40d089b14497', 'pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json': '1d1aaeef696bcc99c711b05bb5c6226936485d927b063acda6c561e726fe5eaf', 'pantheon_inputs_v001/COVARIANCE_V001.part000.b64': '96e41bebcfe6217606c01656011d6e75d43076932706547fc27093071aa38898', 'pantheon_inputs_v001/COVARIANCE_V001.part001.b64': '341b243ea87a15275b570fa34c58d8296df7d78b5c9dd91e3db2c2775a0bd81e', 'pantheon_inputs_v001/COVARIANCE_V001.part002.b64': '8c73a43d20fe428423e4e84bbbe649d3037fcf8f53d00524dddd4955431b9236', 'pantheon_inputs_v001/COVARIANCE_V001.part003.b64': 'ab6f98037a4c3fe64c8448622efe42525e0d7abd6afd733e3a349dcfdb8850d9', 'pantheon_inputs_v001/COVARIANCE_V001.part004.b64': '63aadd0d4eac0e47138f9eec9602d75c63c3e425e34b4e830257367fdfab1e21', 'pantheon_inputs_v001/COVARIANCE_V001.part005.b64': '1342a15074048c948e3b7684024e1c8ae9153874b227be564f2dc42632e7119b', 'pantheon_inputs_v001/COVARIANCE_V001.part006.b64': '4ac5e9000ca304e96cc6745624997f6b8cb5ecc03f49c0a6c41ff656d0a9146f', 'pantheon_inputs_v001/COVARIANCE_V001.part007.b64': 'd224830e719c84927724ac3f938200d8f90112b4ab0d22dd8cadb753129692d9', 'pantheon_inputs_v001/COVARIANCE_V001.part008.b64': '938771ea6c8b4f6fb27bafdb7c17cfdc6099c6ee3e3617588aa52b63822e17b6', 'pantheon_inputs_v001/COVARIANCE_V001.part009.b64': '8392b21df6c52f72f95ea6eac31afb9d594c33ab5e7bd737b2f7167422474eb0', 'pantheon_inputs_v001/COVARIANCE_V001.part010.b64': 'dd0f98d0864dd0a6b3d824c883d5c988024b77e832ae44de09ee7fffafb93d88', 'pantheon_inputs_v001/COVARIANCE_V001.part011.b64': '18625dd0a97c0e326cd29d3340f1262777f55d89761631538072ec6fd3dd82db', 'pantheon_inputs_v001/COVARIANCE_V001.part012.b64': 'a0ce31a52f8b0f3357b8462534973785c082b0a17820826ee292f6d52e75fe4a', 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001.md': 'b0bfe3ddd7fafaec34f0d424b359f285abce69463a9a82ddcc7822b4aa884e17'}
HELPER_SHA = {'decode_receipt': 'eeef7b943bb5c00d887f3265c271edf2784b884a3eb656d60c2f7ff69e45dada', 'load_data': '869dd2ad368e6e97b3817326fa30bb1a5c3224f1b190a8c23a99c9024b66ba57', 'forward': '10e1416b0621828cd660bc725b7f272bd2b530bb086d8a2f9e5d4e83deb3f667', 'backward': '84b5a3cbb60dd96969f3ffa57f4db51018ce1d3b3d9a6ee421ed6c5d41025a11', 'profile_batch': '0f5dcc5f2c28beb582c3be79e6b5f4dca7c23c75ddb93dc10586f4d3316229ed'}
COMMIT = 'c447f0fea703fcd0fff57de5000947b5ca81286b'
REMOTE_PATHS = {
    'vector': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat',
    'covariance': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov',
    'readme': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/README',
    'likelihood': 'Pantheon+_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon+_only_cosmosis_likelihood.py'}
RECEIPTS = {k: 'pantheon_inputs_v001/PANTHEON_' + k.upper() + '_V001_TRANSPORT.json'
            for k in REMOTE_PATHS}
CONFIG = dict(expected_total_rows=1701, redshift_cut_exclusive=.01,
    source_size_ceiling=64*1024*1024, covariance_tolerance=2e-12,
    arithmetic_tolerance=2e-11, solve_tolerance=2e-10, distance_tolerance=2e-10,
    offset_refinement_tolerance=2e-9, score_refinement_tolerance=2e-6,
    optimizer_Omega_tolerance=2e-7, optimizer_offset_tolerance=2e-7,
    golden_width=1e-10, golden_iterations=80, evaluation_cap_per_arm=4096,
    model_batch=16, grids=[257, 513], orders=[16, 32],
    profiled_parameters=['Omega_m', 'common magnitude offset'],
    observational_success_gate=None)
CP = J / 'constrained_u_pantheon_flat_lcdm_profile_v001_checkpoints'
PHYSICAL = dict(native_origin_qualified=False, joint_likelihood_qualified=False,
    model_superiority_qualified=False, unused_validation_qualified=False,
    new_native_parameter_adopted=False, H0_measured=False,
    analytic_global_optimum_proved=False)
SEALS, CREATED, CONTEXT = {}, {}, {}
np = None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canonical(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def utc():
    return datetime.now(timezone.utc).isoformat()


def exclusive(p, raw):
    p = Path(p)
    with p.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    p.chmod(0o444)
    h = sha(p)
    CREATED[p.relative_to(J).as_posix()] = h
    return h


def merge(mp):
    for n, h in mp.items():
        p = Path(n)
        p = p if p.is_absolute() else J/p
        p = p.resolve(strict=True)
        p.relative_to(J)
        rel = p.relative_to(J).as_posix()
        assert isinstance(h, str) and len(h) == 64 and sha(p) == h, ('byte_seal', rel)
        assert rel not in SEALS or SEALS[rel] == h, ('conflicting_seal', rel)
        SEALS[rel] = h


def recheck():
    for n, h in {**SEALS, **CREATED}.items():
        assert sha(J/n) == h, ('changed_input_or_output', n)


def authenticate():
    merge(PINS)
    merge({Path(__file__).name: sha(__file__)})
    r = json.loads((J/(PARENT+'_RECEIPT.json')).read_text())
    p = json.loads((J/(PARENT+'_RESULT.json')).read_text())
    m = json.loads((J/(PARENT+'_MANIFEST.json')).read_text())
    assert r['status'] == p['status'] == 'NUMERICAL_PASS'
    assert r['owner'] == m['owner'] == 'root' and type(r['pid']) is int and r['pid'] > 0
    assert r['pid'] == m['pid'] and r['started'] == m['started'] and r['closed'] > r['started']
    assert p['manifest'] == m and r['manifest_sha256'] == sha(J/(PARENT+'_MANIFEST.json'))
    assert r['result_sha256'] == PINS[PARENT+'_RESULT.json']
    assert r['source_sha256'] == m['source_sha256'] == PINS['constrained_u_shared_eps_ngc_pantheon_v001.py']
    merge(m['input_sha256'])
    merge(r['output_sha256'])
    assert len(p['controls']) == 31 and all(c['passed'] is True for c in p['controls'])
    assert len(p['prior_numerical_gates_copied']) == 52
    assert all(c['passed'] is True for c in p['prior_numerical_gates_copied'])
    assert p['physical_flags'] and all(v is False for v in p['physical_flags'].values())
    assert [row['eps'] for row in p['rows']] == [1e-6, 1e-5, 1e-4, 1e-3]
    old = json.loads((J/(OLD+'_RESULT.json')).read_text())
    old_r = json.loads((J/(OLD+'_RECEIPT.json')).read_text())
    assert old_r['result_sha256'] == PINS[OLD+'_RESULT.json']
    assert old['status'] == old_r['status'] == 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS'
    assert old['manifest'] == old_r['manifest']
    assert old['manifest']['source_sha256'] == PINS[HELPER_SOURCE]
    assert old['all_numerical_gates_passed'] and len(old['numerical_gates']) == 52
    assert old['numerical_gates'] == p['prior_numerical_gates_copied']
    assert old['manifest']['fixed'] == m['fixed_parent']
    assert p['reference_copied_exactly'] == old['rows'][1]
    assert p['rows'][0]['pantheon']['profile_rows'] == old['rows'][0]['profile_rows']
    for row in p['rows']:
        n = PARENT+'_EPS_'+format(row['eps'], '.0e').replace('-', 'm')+'_CP.json'
        assert json.loads((J/n).read_text()) == row
    source = (J/HELPER_SOURCE).read_text()
    own = Path(__file__).read_text()
    for name, h in HELPER_SHA.items():
        nodes = [next(n for n in ast.parse(s).body if isinstance(n, ast.FunctionDef) and n.name == name)
                 for s in (source, own)]
        parts = [ast.get_source_segment(s, n) for s, n in zip((source, own), nodes)]
        assert parts[0] == parts[1] and hashlib.sha256(parts[1].encode()).hexdigest() == h
    raw, metadata = {}, {}
    for k, rel in RECEIPTS.items():
        raw[k], metadata[k], parts = decode_receipt(J/rel, k)
        for part in parts:
            merge({part.relative_to(J).as_posix(): sha(part)})
    return p, old, raw, metadata


class Checks:
    def __init__(self):
        self.records = []

    def check(self, name, a, b=0., scale=1., tol=None, context=None):
        tol = CONFIG['arithmetic_tolerance'] if tol is None else tol
        er = np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale), 1e-300)
        finite = bool(np.all(np.isfinite(er)))
        mx = float(np.max(er)) if finite else None
        self.records.append(dict(name=name, error=mx, tolerance=tol, scalar_count=int(er.size),
                                 passed=finite and mx <= tol, context=context))

    def yes(self, name, value, context=None):
        self.check(name, int(bool(value)), 1., context=context)


def decode_receipt(path,key):
    packet=json.loads(path.read_text())
    for k,v in {"kind":"public_source_verbatim_zlib_base64","encoding":"zlib_base64",
                "repository":"PantheonPlusSH0ES/DataRelease","commit":COMMIT,
                "path":REMOTE_PATHS[key],"key":key}.items():
        if packet.get(k)!=v:raise RuntimeError("Receipt metadata differs: "+key+"/"+k)
    expected_url="https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/"+COMMIT+"/"+urllib.parse.quote(REMOTE_PATHS[key],safe="/")
    if packet["url"]!=expected_url:raise RuntimeError("Receipt URL differs")
    if packet["transport_sha256"]!=sha(HERE/"fetch_pantheon_reference_v001.py"):
        raise RuntimeError("Fetcher provenance differs")
    size=packet["bytes"]
    if not isinstance(size,int) or not 0<size<=CONFIG["source_size_ceiling"]:
        raise RuntimeError("Unexpected raw source size")
    parts=[]
    if "data_parts" in packet:
        if "data" in packet:raise RuntimeError("Ambiguous source transport")
        joined=[]
        for part in packet["data_parts"]:
            p=(path.parent/part["file"]).resolve(strict=True);p.relative_to(path.parent)
            rawpart=p.read_bytes()
            if len(rawpart)!=part["characters"]+1 or not rawpart.endswith(b"\n"):
                raise RuntimeError("Transport part size/final LF differs")
            # validate=True below rejects any further whitespace, including LF.
            joined.append(rawpart[:-1]);parts.append(p)
        compressed=base64.b64decode(b"".join(joined),validate=True)
    else:compressed=base64.b64decode(packet["data"],validate=True)
    dec=zlib.decompressobj();raw=dec.decompress(compressed,size+1)
    if len(raw)!=size or not dec.eof or dec.unused_data or dec.unconsumed_tail:
        raise RuntimeError("Raw source size/stream failed")
    if hashlib.sha256(raw).hexdigest()!=packet["sha256"]:raise RuntimeError("Raw source hash differs")
    raw.decode("utf-8")
    return raw,{k:packet[k] for k in ["repository","commit","path","url","key","bytes","sha256","transport_sha256"]},parts

def load_data(raw,ck):
    table=np.genfromtxt(io.StringIO(raw["vector"].decode()),names=True,dtype=None,
                        encoding="utf-8",autostrip=True)
    columns=table.dtype.names
    for key in ["CID","IDSURVEY","zHD","zHEL","m_b_corr"]:
        if key not in columns:raise RuntimeError("Missing Pantheon column: "+key)
    if len(table)!=CONFIG["expected_total_rows"]:raise RuntimeError("Total vector row census differs")
    stream=raw["covariance"].decode();head,body=stream.split("\n",1)
    n=int(head.strip());values=np.fromstring(body,sep=" ")
    if n!=len(table) or len(values)!=n*n:raise RuntimeError("Covariance layout differs")
    full=values.reshape(n,n)
    mask=np.asarray(table["zHD"]>CONFIG["redshift_cut_exclusive"])
    ix=np.flatnonzero(mask);cov=full[np.ix_(ix,ix)].copy()
    zh=np.asarray(table["zHD"][mask],float);zhel=np.asarray(table["zHEL"][mask],float)
    y=np.asarray(table["m_b_corr"][mask],float)
    ck.yes("data_finite",np.all(np.isfinite(full)) and np.all(np.isfinite(y)) and
           np.all(np.isfinite(zh)) and np.all(np.isfinite(zhel)))
    ck.yes("positive_distance_domain",len(ix)>1 and np.all(zh>.01) and np.all(1+zhel>0))
    ck.check("covariance_symmetry",cov,cov.T,tol=CONFIG["covariance_tolerance"])
    ck.yes("positive_covariance_diagonal",np.all(np.diag(cov)>0))
    # Independent indexing witness: direct original flat-array addresses.
    for a,b in [(0,0),(0,len(ix)-1),(len(ix)//2,len(ix)//3),(len(ix)-1,len(ix)-1)]:
        ck.check("covariance_original_index",cov[a,b],values[int(ix[a])*n+int(ix[b])])
    metadata=dict(total_rows=n,selected_rows=len(ix),mask_sha256=hashlib.sha256(mask.astype("u1").tobytes()).hexdigest(),
        original_row_indices=ix.tolist(),CID=[str(x) for x in table["CID"][mask]],
        IDSURVEY=[int(x) for x in table["IDSURVEY"][mask]],zHD=zh.tolist(),zHEL=zhel.tolist(),
        m_b_corr=y.tolist(),covariance_diagonal=np.diag(cov).tolist(),
        covariance_selected_f64_sha256=hashlib.sha256(np.asarray(cov,dtype="<f8").tobytes()).hexdigest(),
        source_columns=list(columns))
    del full,values,table,stream,body
    return zh,zhel,y,cov,metadata

def forward(L,rhs):
    rhs=np.asarray(rhs,float);one=rhs.ndim==1
    B=rhs[:,None] if one else rhs;answer=np.empty_like(B)
    for i in range(len(L)):
        answer[i]=(B[i]-L[i,:i]@answer[:i])/L[i,i]
    return answer[:,0] if one else answer

def backward(L,rhs):
    rhs=np.asarray(rhs,float);one=rhs.ndim==1
    B=rhs[:,None] if one else rhs;answer=np.empty_like(B)
    for i in range(len(L)-1,-1,-1):
        answer[i]=(B[i]-L[i+1:,i]@answer[i+1:])/L[i,i]
    return answer[:,0] if one else answer

def profile_batch(Q,Y,L,white_one,precision_one,ck,context):
    # Columns are histories. The data covariance/factor are shared once.
    differences=Y[:,None]-Q;wd=forward(L,differences)
    denom=float(white_one@white_one)
    offsets=(white_one@wd)/denom
    residual=Q+offsets[None,:]-Y[:,None]
    white=forward(L,residual);score=np.sum(white*white,axis=0)
    direct_offsets=(precision_one@differences)/float(np.sum(precision_one))
    ck.check("profile_precision_offset",offsets,direct_offsets,np.maximum(1.,np.abs(offsets)),
             tol=CONFIG["solve_tolerance"],context=context)
    # Projection identity checks the full quadratic, not just its offset.
    projected=np.sum(wd*wd,axis=0)-(white_one@wd)**2/denom
    cancellation_scale=np.sum(wd*wd,axis=0)+(white_one@wd)**2/denom
    ck.check("profile_projection_score",score,projected,np.maximum(1.,cancellation_scale),
             tol=CONFIG["solve_tolerance"],context=context)
    derivative=2*(white_one@white)
    scale=2*np.sum(np.abs(white_one[:,None]*white),axis=0)
    ck.check("profile_stationarity",derivative,0.,np.maximum(1.,scale),context=context)
    return offsets,score,residual,white,derivative,denom


def golden(func, lo, hi):
    assert math.isfinite(lo) and math.isfinite(hi) and lo < hi
    ratio = (math.sqrt(5.)-1.)/2.
    x1, x2 = hi-ratio*(hi-lo), lo+ratio*(hi-lo)
    f1, f2 = func(x1), func(x2)
    history = []
    for iteration in range(CONFIG['golden_iterations']):
        history.append(dict(iteration=iteration, lo=lo, hi=hi, x1=x1, x2=x2,
                            score1=float(f1), score2=float(f2)))
        if hi-lo <= CONFIG['golden_width']:
            break
        if f1 <= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi-ratio*(hi-lo)
            f1 = func(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo+ratio*(hi-lo)
            f2 = func(x2)
    points = [(x1, f1), (x2, f2), ((lo+hi)/2., func((lo+hi)/2.))]
    x, value = min(points, key=lambda t: (t[1], t[0]))
    return dict(Omega_m=x, score=float(value), bracket=[lo, hi],
                converged=hi-lo <= CONFIG['golden_width'], iterations=history)


class Objective:
    def __init__(self, radiation, order, z, inv, zhel, y, L, white_one, white_y):
        self.radiation, self.order = radiation, order
        self.z, self.inv, self.zhel, self.y = z, inv, zhel, y
        self.L, self.one, self.wy = L, white_one, white_y
        self.den = float(white_one@white_one)
        nodes, weights = np.polynomial.legendre.leggauss(order)
        lo, width = np.r_[0., z[:-1]], z-np.r_[0., z[:-1]]
        self.zz = lo[:, None]+width[:, None]*(nodes+1.)/2.
        self.weights, self.width = weights, width
        self.matter, self.rad = (1+self.zz)**3-1., (1+self.zz)**4-1.
        self.cache = {}

    def many(self, values):
        missing = sorted(set(float(x) for x in values)-set(self.cache))
        assert len(self.cache)+len(missing) <= CONFIG['evaluation_cap_per_arm'], 'evaluation_cap'
        for start in range(0, len(missing), CONFIG['model_batch']):
            om = np.asarray(missing[start:start+CONFIG['model_batch']])
            CONTEXT.update(stage='profile_evaluation', radiation=self.radiation,
                           order=self.order, Omega_m=om.tolist())
            assert np.all(om >= 0.) and np.all(om <= 1-self.radiation)
            e2 = 1+om[:, None, None]*self.matter+self.radiation*self.rad
            assert np.all(np.isfinite(e2)) and np.all(e2 > 0.)
            dm = np.cumsum(self.width[None, :]*(1/np.sqrt(e2)@self.weights)/2., axis=1).T
            assert np.all(np.isfinite(dm)) and np.all(dm > 0.)
            q = 5*np.log10((1+self.zhel[:, None])*dm[self.inv])
            wq = forward(self.L, q)
            offsets = (self.one@(self.wy[:, None]-wq))/self.den
            residual = q+offsets[None, :]-self.y[:, None]
            white = wq+offsets[None, :]*self.one[:, None]-self.wy[:, None]
            scores = np.sum(white*white, axis=0)
            assert np.all(np.isfinite(scores)) and np.all(np.isfinite(offsets))
            for i, x in enumerate(om):
                gradient = 2*float(self.one@white[:, i])
                gradient_scale = max(1., 2*float(np.sum(abs(self.one*white[:, i]))))
                self.cache[float(x)] = dict(Omega_m=float(x), Omega_r=self.radiation,
                    Omega_Lambda=float(1-self.radiation-x), score=float(scores[i]),
                    magnitude_offset=float(offsets[i]), offset_gradient=gradient,
                    offset_gradient_normalized=abs(gradient)/gradient_scale,
                    distance=dm[:, i].copy(), magnitude_shape=q[:, i].copy(),
                    residual=residual[:, i].copy(), whitened_residual=white[:, i].copy())

    def score(self, x):
        self.many([x])
        return self.cache[float(x)]['score']

    def scalars(self, x):
        return {k: v for k, v in self.cache[float(x)].items() if not isinstance(v, np.ndarray)}

    def payload(self, x):
        return {k: v.tolist() if isinstance(v, np.ndarray) else v
                for k, v in self.cache[float(x)].items()}


def profile_arm(objective, count, ck, label):
    xs = np.linspace(0., 1-objective.radiation, count)
    objective.many(xs)
    scores = [objective.score(x) for x in xs]
    candidates = [dict(kind='left_endpoint', grid_index=0, Omega_m=float(xs[0]),
                       score=scores[0], bracket=[float(xs[0]), float(xs[0])]),
                  dict(kind='right_endpoint', grid_index=count-1, Omega_m=float(xs[-1]),
                       score=scores[-1], bracket=[float(xs[-1]), float(xs[-1])])]
    for i in range(1, count-1):
        if scores[i] <= scores[i-1] and scores[i] <= scores[i+1]:
            fit = golden(objective.score, float(xs[i-1]), float(xs[i+1]))
            ck.yes('golden_bracket_converged', fit['converged'], [label, i])
            fit.update(kind='refined_sampled_local_minimum', grid_index=i,
                       incoming_bracket=[float(xs[i-1]), float(xs[i+1])])
            candidates.append(fit)
    best = min(candidates, key=lambda r: (r['score'], r['Omega_m']))
    ck.check('all_profile_offset_stationarity',
             [r['offset_gradient_normalized'] for r in objective.cache.values()], 0.,
             tol=CONFIG['arithmetic_tolerance'], context=label)
    ck.yes('best_not_above_grid', best['score'] <= min(scores)+CONFIG['score_refinement_tolerance'], label)
    return dict(label=label, order=objective.order, grid_count=count,
                grid=[objective.scalars(x) for x in xs],
                evaluated_profile=[objective.scalars(x) for x in sorted(objective.cache)],
                candidates=[dict(r, readout=objective.payload(r['Omega_m'])) for r in candidates],
                best_Omega_m=best['Omega_m'], best_score=best['score'],
                best=objective.payload(best['Omega_m']),
                scope='Bounded sampled profile with all endpoints/local minima; no analytic global-optimality theorem')


def direct_dist(z, om, rad, order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    xx = z[:, None]*(nodes+1.)/2.
    e2 = 1+om*((1+xx)**3-1.)+rad*((1+xx)**4-1.)
    return z*((1/np.sqrt(e2))@weights)/2.


def witnesses(om, rad, ck, obj, label, white_one, precision_one):
    obj.many([om])
    p = obj.cache[float(om)]
    global64 = direct_dist(obj.z, om, rad, 64)
    ck.check('distance_global64', global64, p['distance'], p['distance'],
             tol=CONFIG['distance_tolerance'], context=label)
    q64 = 5*np.log10((1+obj.zhel)*global64[obj.inv])
    a = profile_batch(q64[:, None], obj.y, obj.L, white_one, precision_one, ck, label)
    ck.check('score_global64', a[1][0], p['score'],
             tol=CONFIG['score_refinement_tolerance'], context=label)
    ck.check('offset_global64', a[0][0], p['magnitude_offset'],
             tol=CONFIG['offset_refinement_tolerance'], context=label)
    ck.check('cached_profile_residual', a[2][:, 0], p['residual'],
             tol=CONFIG['solve_tolerance'], context=label)
    saved = []
    for i in sorted(set((0, len(obj.z)//2, len(obj.z)-1))):
        lo = -math.log1p(float(obj.z[i]))
        x = np.linspace(lo, 0., 2049)
        yy = np.exp(-x)
        f = yy/np.sqrt(1+om*(yy**3-1.)+rad*(yy**4-1.))
        value = float(-lo/2048/3*(f[0]+f[-1]+4*np.sum(f[1:-1:2])+2*np.sum(f[2:-1:2])))
        ck.check('Simpson_log_distance', value, p['distance'][i], p['distance'][i],
                 tol=CONFIG['distance_tolerance'], context=[label, i])
        saved.append(dict(index=i, zHD=float(obj.z[i]), Simpson2048=value,
                          primary=float(p['distance'][i]), signed_difference=value-p['distance'][i]))
    return dict(Omega_m=om, Omega_r=rad, global64_distance=global64.tolist(),
                global64_profile=dict(score=float(a[1][0]), offset=float(a[0][0]),
                    residual=a[2][:, 0].tolist(), whitened_residual=a[3][:, 0].tolist()),
                Simpson_witnesses=saved)


def qualify(ck):
    L = np.array([[2., 0., 0.], [.4, 1.3, 0.], [-.2, .3, .7]])
    X = np.arange(1., 10.).reshape(3, 3)
    ck.check('synthetic_forward', forward(L, L@X), X, np.maximum(1., abs(X)))
    ck.check('synthetic_backward', backward(L, L.T@X), X, np.maximum(1., abs(X)))
    C = L@L.T
    u = forward(L, np.ones(3))
    v = backward(L, u)
    ck.check('synthetic_precision', v, np.linalg.solve(C, np.ones(3)), np.maximum(1., abs(v)))
    q = np.array([1., 3., 4.])
    ans = profile_batch(q[:, None], q+17., L, u, v, ck, 'synthetic')
    ck.check('synthetic_offset', ans[0], 17., 17.)
    ck.check('synthetic_noiseless_score', ans[1], 0., tol=1e-18)
    other = profile_batch((q+2.)[:, None], q+17., L, u, v, ck, 'synthetic_shift')
    ck.check('synthetic_shift_residual', other[2], ans[2])
    ck.check('synthetic_shift_offset', other[0], ans[0]-2.)
    fit = golden(lambda x: (x-.27)**2, 0., 1.)
    ck.yes('synthetic_golden_width', fit['converged'])
    ck.check('synthetic_golden_location', fit['Omega_m'], .27, tol=2e-9)
    for direction in (1., -1.):
        fit = golden(lambda x: direction*x, 0., 1.)
        endpoint = 0. if direction > 0. else 1.
        ck.yes('synthetic_boundary_minimum',
               direction*endpoint <= fit['score'] and fit['converged'], direction)
    z = np.array([.0101, .1, .5, 1., 2.5])
    for om, exact in ((0., z), (1., 2*(1-1/np.sqrt(1+z)))):
        ck.check('synthetic_distance', direct_dist(z, om, 0., 64), exact, exact,
                 tol=CONFIG['distance_tolerance'], context=om)


def checkpoint(name, payload, owner):
    p = CP/(name+'.json')
    data = dict(name=name, owner=owner, input_sha256=dict(SEALS), payload=payload)
    h = exclusive(p, canonical(data))
    commit = dict(checkpoint=p.name, sha256=h, owner=owner, input_sha256=dict(SEALS))
    exclusive(CP/(name+'.COMMIT.json'), canonical(commit))
    assert json.loads(p.read_text()) == data
    assert json.loads((CP/(name+'.COMMIT.json')).read_text()) == commit
    return data


def main():
    global np
    reserved = [CP]+[J/(STEM+s) for s in ('_MANIFEST.json', '_RESULT.json',
                                         '_REPORT.md', '_RECEIPT.json', '_ERROR.json')]
    assert not any(p.exists() for p in reserved), 'existing_runtime_preserved'
    assert not AUTHOR_DRAFT, 'unsealed_author_guard'
    started = time.monotonic()
    parent, old, raw, raw_metadata = authenticate()
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    import numpy as runtime_numpy
    np = runtime_numpy
    owner = dict(owner='root', pid=os.getpid(), source_sha256=sha(__file__), started=utc())
    assert type(owner['pid']) is int and owner['pid'] > 0
    ck = Checks()
    manifest = dict(owner=owner, input_sha256=dict(SEALS), configuration=CONFIG,
        parent_result_sha256=PINS[PARENT+'_RESULT.json'],
        exposure=parent['manifest']['exposure'], native_fitted_shape_parameter_count=0,
        comparator_fitted_shape_parameter_count=1, common_offset_count_per_curve=1,
        inherited_ordinary_calibration_parameter_count=
            old['manifest']['inherited_ordinary_calibration_parameter_count'],
        all_four_native_eps_preserved=True, numpy_version=np.__version__, physical_flags=PHYSICAL)
    exclusive(J/(STEM+'_MANIFEST.json'), canonical(manifest))
    CP.mkdir()
    groups, families = [], []
    try:
        qualify(ck)
        zh, zhel, y, cov, data = load_data(raw, ck)
        assert len(y) == 1590
        for k, value in data.items():
            assert old['data'][k] == value, ('exact_selected_data', k)
        assert len(old['data']['excluded_original_row_indices']) == 111
        assert old['data']['repeated_CID_measurement_count'] == 117
        L = np.linalg.cholesky(cov)
        ck.check('Cholesky_reconstruction', L@L.T, cov, tol=CONFIG['covariance_tolerance'])
        one = forward(L, np.ones(len(y)))
        precision_one = backward(L, one)
        wy = forward(L, y)
        ck.check('precision_one_residual', cov@precision_one, np.ones(len(y)),
                 np.maximum(1., abs(cov)@abs(precision_one)), tol=CONFIG['solve_tolerance'])
        ck.check('white_data_residual', L@wy, y, np.maximum(1., abs(y)),
                 tol=CONFIG['solve_tolerance'])
        fixed = parent['manifest']['fixed_parent']
        S = fixed['OA']+fixed['OA']*fixed['d0']+fixed['OB']+fixed['OR']
        matter = (fixed['OA']*fixed['d0']+fixed['OB'])/S
        rad = fixed['OR']/S
        vacuum = fixed['OA']/S
        h0 = math.sqrt(S/fixed['rG'])
        ck.check('dust_normalized_closure', matter+rad+vacuum, 1.)
        z, inv = np.unique(zh, return_inverse=True)
        assert z.tolist() == parent['reference_copied_exactly']['unique_zHD']
        dust_obj = Objective(rad, 32, z, inv, zhel, y, L, one, wy)
        dust_obj.many([matter])
        dust = dust_obj.cache[matter]
        reference = parent['reference_copied_exactly']
        ref = reference['profile_rows'][0]
        ck.check('fixed_dust_distance_bridge', dust['distance'],
                 np.asarray(reference['dimensionless_distance_arms'])[:, 0]*h0,
                 dust['distance'], tol=CONFIG['distance_tolerance'])
        ck.check('fixed_dust_offset_bridge', dust['magnitude_offset'],
                 ref['magnitude_offset']-5*math.log10(h0),
                 tol=CONFIG['offset_refinement_tolerance'])
        ck.check('fixed_dust_score_bridge', dust['score'], ref['score'],
                 tol=CONFIG['score_refinement_tolerance'])
        ck.check('fixed_dust_residual_bridge', dust['residual'], ref['residual'],
                 tol=CONFIG['solve_tolerance'])
        for row in parent['rows']:
            for saved in row['pantheon']['profile_rows']:
                res, white = np.asarray(saved['residual']), np.asarray(saved['whitened_residual'])
                ck.check('saved_native_whitening', L@white, res,
                         tol=CONFIG['solve_tolerance'], context=[row['eps'], saved['arm']])
                ck.check('saved_native_score', float(white@white), saved['score'],
                         tol=2e-8, context=[row['eps'], saved['arm']])
        baseline = dict(data=old['data'], raw_metadata=raw_metadata, fixed=fixed,
            normalized_dust=dict(S=S, Omega_m=matter, Omega_r=rad, Omega_Lambda=vacuum,
                h_dust_today_over_Hstar=h0, magnitude_unit_shift=5*math.log10(h0),
                readout=dust_obj.payload(matter)),
            native_parent_rows_copied_exactly=parent['rows'],
            dust_reference_copied_exactly=reference,
            original_numerical_controls_copied=parent['controls'],
            original_52_controls_copied=parent['prior_numerical_gates_copied'],
            original_physical_flags_copied=parent['physical_flags'],
            original_NGC_flags_copied=parent['ngc_ancestral_flags'])
        groups.append(checkpoint('DATA_AND_FIXED_REFERENCE', baseline, owner))
        for label, radiation in (('MATCHED_FIXED_RADIATION', rad), ('ZERO_RADIATION_SUPPLEMENT', 0.)):
            arms, objs = [], []
            for count, order in zip(CONFIG['grids'], CONFIG['orders']):
                obj = Objective(radiation, order, z, inv, zhel, y, L, one, wy)
                arm_label = label+'_GRID'+str(count)+'_GL'+str(order)
                arm = profile_arm(obj, count, ck, arm_label)
                recheck()
                groups.append(checkpoint(arm_label, arm, owner))
                arms.append(arm)
                objs.append(obj)
                print(json.dumps(dict(family=label, arm=arm_label, completed=True)), flush=True)
            coarse, fine = arms
            ck.check('optimizer_Omega_refinement', coarse['best_Omega_m'], fine['best_Omega_m'],
                     tol=CONFIG['optimizer_Omega_tolerance'], context=label)
            ck.check('optimizer_score_refinement', coarse['best_score'], fine['best_score'],
                     tol=CONFIG['score_refinement_tolerance'], context=label)
            ck.check('optimizer_offset_refinement', coarse['best']['magnitude_offset'],
                     fine['best']['magnitude_offset'],
                     tol=CONFIG['optimizer_offset_tolerance'], context=label)
            witness_rows = [witnesses(c['Omega_m'], radiation, ck, objs[1],
                [label, c['kind'], c['grid_index']], one, precision_one)
                for c in fine['candidates']]
            comparison = [dict(eps=r['eps'], fixed_native_score=r['pantheon']['profile_rows'][0]['score'],
                              native_minus_optimized_LambdaCDM=
                              r['pantheon']['profile_rows'][0]['score']-fine['best_score'])
                          for r in parent['rows']]
            families.append(dict(label=label, fixed_Omega_r=radiation,
                Omega_m_interval=[0., 1-radiation], Omega_Lambda='1-Omega_m-Omega_r',
                primary=(label == 'MATCHED_FIXED_RADIATION'), arms=arms,
                numerical_witnesses=witness_rows, native_comparisons=comparison,
                scope='One fitted shape parameter plus same M; no fitted H0/radiation, superiority or native adoption'))
        assert len(groups) == 5 and len(families) == 2
        for group in groups:
            p = CP/(group['name']+'.json')
            assert json.loads(p.read_text()) == group
            assert json.loads((CP/(group['name']+'.COMMIT.json')).read_text()) == dict(
                checkpoint=p.name, sha256=sha(p), owner=owner, input_sha256=group['input_sha256'])
        recheck()
        passed = all(g['passed'] for g in ck.records)
        result = dict(status='NUMERICAL_PASS' if passed else 'NUMERICAL_FAILED',
            manifest=manifest, baseline=baseline, families=families, controls=ck.records,
            all_numerical_controls_passed=passed, physical_flags=PHYSICAL,
            elapsed_seconds=time.monotonic()-started,
            scope='Matched exposed SNe-only likelihood comparison; sampled optimization, no physical-origin/joint-evidence claim')
        rh = exclusive(J/(STEM+'_RESULT.json'), canonical(result))
        report = ['# Same-data flat-Lambda-CDM shape profiles', '', result['status'],
            '', 'All1590 measurements and full covariance retained. Each comparator fits Omega_m and one common magnitude offset.',
            'All four fixed native epsilon predictions are retained; no radiation branch or native epsilon is adopted.',
            '', '| Family | Grid/order | Omega_m | Score | Offset |',
            '|---|---|---:|---:|---:|']
        for f in families:
            for arm in f['arms']:
                report.append(f"| {f['label']} | {arm['grid_count']}/{arm['order']} | {arm['best_Omega_m']:.12g} | {arm['best_score']:.12g} | {arm['best']['magnitude_offset']:.12g} |")
        report.extend(['', 'Primary fixed radiation is OR/S from the adopted normalized dust reference; zero radiation is a disclosed supplemental family.',
            'The covariance/model-independent magnitude scale is absorbed by M; this does not measure H0.',
            'No p-value, superiority, blind-validation, joint-likelihood or native-origin claim. Every failed numerical predicate remains in JSON.'])
        exclusive(J/(STEM+'_REPORT.md'), ('\n'.join(report)+'\n').encode())
        assert json.loads((J/(STEM+'_RESULT.json')).read_text()) == result
        recheck()
        receipt = dict(status=result['status'], owner=owner, closed=utc(),
            elapsed_seconds=time.monotonic()-started, input_sha256=dict(SEALS),
            output_sha256=dict(CREATED), result_sha256=rh, checkpoint_pairs=len(groups),
            physical_flags=PHYSICAL)
        exclusive(J/(STEM+'_RECEIPT.json'), canonical(receipt))
        recheck()
        print(json.dumps(dict(status=result['status'], result_sha256=rh,
                              receipt_sha256=sha(J/(STEM+'_RECEIPT.json')))), flush=True)
        return 0 if passed else 3
    except Exception:
        data = dict(status='EXECUTION_ERROR_PRESERVED', owner=owner, failed=utc(),
            context=CONTEXT, traceback=traceback.format_exc(), input_sha256=dict(SEALS),
            output_sha256=dict(CREATED), completed_numerical_controls=ck.records,
            physical_flags=PHYSICAL)
        exclusive(J/(STEM+'_ERROR.json'), canonical(data))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-owned', action='store_true')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    assert args.root_owned and args.execute, 'root_only_explicit_execute'
    raise SystemExit(main())
