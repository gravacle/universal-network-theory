"""Guarded conditional same-data SN+BAO late-shape joint profile. Root only."""
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
STEM = 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001'
PARENT = 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001'
SN = 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001'
BAO = 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002'
OLD = 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002'
HELPER_SOURCE = 'constrained_u_clock_gradient_bbn_pantheon_profile_v002.py'
EPS = (1e-6, 1e-5, 1e-4, 1e-3)
C_KMS = 299792.458
EXTERNAL_READONLY_PINS = {'/usr/bin/clang': '179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'}
PINS = {'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002.md': 'ecb771122c94d8a9a36d2e9d6fc01983a4ffa26ff60d2d5364edbe55253b6b23', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002_RECEIPT.json': '9c489ec4ca988b95d067151639dda84aa7f3de689fafd7c44017a7f55e8e0644', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002_RESULT.json': '12743287b22d4dc96ff21b9134f5d8d04db9081c41bd55bd6aabec1f6fdb4979', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': '4ea9d4615ee248ffd0143cf862348bbc3648d080ac5e6d8cde3ba1dabdca2e3b', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RESULT.json': '8ccfba9bbded7faf0c2c3eb6250fb49f7d7f2951dbd71fc305f42cb81a3cd67b', 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001.md': 'b0bfe3ddd7fafaec34f0d424b359f285abce69463a9a82ddcc7822b4aa884e17', 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001_RECEIPT.json': '993e8885e17d094f184d6ee7ce4f214e0a337ba84ac76426c5e61b409cb391b9', 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001_RESULT.json': 'd1752b60a809c576dd86ec87ed8df6b08cd533d428cbf0b67f1555f59bb8599c', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001.md': '9125291f442dfd3aebb63199de2c707e3f86ec3d02c236f87d606772f9a879ec', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'DESI_BAO_SAVED_AUDIT_V001.json': '2917a6cb521ffa532880859502cd83713bae51dd8a0940c32ed6aa163261e467', 'DESI_BAO_SHAPE_PROTOCOL_V001.md': '3144f98ea5f91ce6dec600dc0ab0452de69cb5e3952819be896c7ec403429d2e', 'DESI_BAO_SHAPE_V001_FROZEN.json': '8847e8267450d694cb59b25790767a88a187888d13e0dcc7076ccab7e399b461', 'DESI_BAO_SHAPE_V001_RESULTS.json': '1b7f1b02b2988e0109c1afd01f4ca621e36f1cd5729261ebff676853596f3fe7', 'PANTHEON_INPUT_SELECTION_V001.md': 'be486e54eed8acc14f345aa8382cdc8aec8e6f448f9691d876bc5cd6adf71fa2', 'constrained_u_clock_gradient_bbn_desi_bao_v002.py': '9016e6730ee4a243c8a90e5f98f63ba5159fec906b1f94f898f2eea3f44f9ac3', 'constrained_u_clock_gradient_bbn_pantheon_profile_v002.py': '976fc4c2b91a5b84e54723ba2d7bdf0508fd5275e6d35dfd615523869744b917', 'constrained_u_pantheon_flat_lcdm_profile_v001.py': '882efbcaddd8f293a91e4fe2bdcb52f27981deb5b4db08346e25a6f25e0e6d72', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'desi_bao_shape_v001.py': '8c5cb5febaccb1d4320840add24addccd7002ae03905e36876f222256d5fabe6', 'desi_dr2_bao_external_v001/README.md': '5f21b88b1a6d6264174f7ecd2b1e0baf78a62c9feb467c5fe3865eb3ba9b70f6', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt': '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt': '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585', 'fetch_pantheon_reference_v001.py': '03d001317e99dedbdc43838abfd9eab46e62e339e021e3a2cea518e1f3b1a5f3', 'pantheon_inputs_v001/COVARIANCE_V001.part000.b64': '96e41bebcfe6217606c01656011d6e75d43076932706547fc27093071aa38898', 'pantheon_inputs_v001/COVARIANCE_V001.part001.b64': '341b243ea87a15275b570fa34c58d8296df7d78b5c9dd91e3db2c2775a0bd81e', 'pantheon_inputs_v001/COVARIANCE_V001.part002.b64': '8c73a43d20fe428423e4e84bbbe649d3037fcf8f53d00524dddd4955431b9236', 'pantheon_inputs_v001/COVARIANCE_V001.part003.b64': 'ab6f98037a4c3fe64c8448622efe42525e0d7abd6afd733e3a349dcfdb8850d9', 'pantheon_inputs_v001/COVARIANCE_V001.part004.b64': '63aadd0d4eac0e47138f9eec9602d75c63c3e425e34b4e830257367fdfab1e21', 'pantheon_inputs_v001/COVARIANCE_V001.part005.b64': '1342a15074048c948e3b7684024e1c8ae9153874b227be564f2dc42632e7119b', 'pantheon_inputs_v001/COVARIANCE_V001.part006.b64': '4ac5e9000ca304e96cc6745624997f6b8cb5ecc03f49c0a6c41ff656d0a9146f', 'pantheon_inputs_v001/COVARIANCE_V001.part007.b64': 'd224830e719c84927724ac3f938200d8f90112b4ab0d22dd8cadb753129692d9', 'pantheon_inputs_v001/COVARIANCE_V001.part008.b64': '938771ea6c8b4f6fb27bafdb7c17cfdc6099c6ee3e3617588aa52b63822e17b6', 'pantheon_inputs_v001/COVARIANCE_V001.part009.b64': '8392b21df6c52f72f95ea6eac31afb9d594c33ab5e7bd737b2f7167422474eb0', 'pantheon_inputs_v001/COVARIANCE_V001.part010.b64': 'dd0f98d0864dd0a6b3d824c883d5c988024b77e832ae44de09ee7fffafb93d88', 'pantheon_inputs_v001/COVARIANCE_V001.part011.b64': '18625dd0a97c0e326cd29d3340f1262777f55d89761631538072ec6fd3dd82db', 'pantheon_inputs_v001/COVARIANCE_V001.part012.b64': 'a0ce31a52f8b0f3357b8462534973785c082b0a17820826ee292f6d52e75fe4a', 'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json': '58317db1be2c6591309a206f6ac6b54d564218f596f639457389eaaa5945a573', 'pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json': '1d1aaeef696bcc99c711b05bb5c6226936485d927b063acda6c561e726fe5eaf', 'pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json': '1be77d822136ac140b6e1bb7b260133c6d91fcd901e34cd002ef40d089b14497', 'pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json': 'c2408ce5f9914c349d926a89e8124adc8828b7f885075aa8a08e0d5a9e4357bb', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001.md': '6f8869df3f6cc58deda9b73c566c697452988dcdd208c76d5630d6e6799e1820'}
HELPER_SHA = {'decode_receipt': 'eeef7b943bb5c00d887f3265c271edf2784b884a3eb656d60c2f7ff69e45dada', 'load_data': '869dd2ad368e6e97b3817326fa30bb1a5c3224f1b190a8c23a99c9024b66ba57', 'forward': '10e1416b0621828cd660bc725b7f272bd2b530bb086d8a2f9e5d4e83deb3f667', 'backward': '84b5a3cbb60dd96969f3ffa57f4db51018ce1d3b3d9a6ee421ed6c5d41025a11', 'profile_batch': '0f5dcc5f2c28beb582c3be79e6b5f4dca7c23c75ddb93dc10586f4d3316229ed'}
COMMIT = 'c447f0fea703fcd0fff57de5000947b5ca81286b'
REMOTE_PATHS = {'vector': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', 'covariance': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov', 'readme': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/README', 'likelihood': 'Pantheon+_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon+_only_cosmosis_likelihood.py'}
RECEIPTS = {'vector': 'pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json', 'covariance': 'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json', 'readme': 'pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json', 'likelihood': 'pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json'}
CONFIG = {'arithmetic_tolerance': 2e-11, 'covariance_tolerance': 2e-12, 'distance_tolerance': 2e-10, 'evaluation_cap_per_arm': 4096, 'expected_total_rows': 1701, 'golden_iterations': 80, 'golden_width': 1e-10, 'grids': [257, 513], 'model_batch': 16, 'observational_success_gate': None, 'offset_refinement_tolerance': 2e-09, 'optimizer_Omega_tolerance': 2e-07, 'optimizer_offset_tolerance': 2e-07, 'orders': [16, 32], 'profiled_parameters': ['common Omega_m (comparator only)', 'common SN magnitude offset', 'common BAO reference scale'], 'redshift_cut_exclusive': 0.01, 'score_refinement_tolerance': 2e-06, 'solve_tolerance': 2e-10, 'source_size_ceiling': 67108864, 'bao_gauss_orders': [48, 96], 'bao_distance_tolerance': 2e-12, 'bao_simpson_tolerance': 2e-11, 'bao_score_tolerance': 2e-08, 'bao_scale_tolerance': 2e-09, 'optimizer_scale_tolerance': 2e-07, 'likelihood_product': 'explicit zero cross-survey covariance premise'}
CP = J / "constrained_u_joint_pantheon_desi_shape_v001_checkpoints"
PHYSICAL = {'native_origin_qualified': False, 'physical_ruler_joint_qualified': False, 'model_superiority_qualified': False, 'unused_validation_qualified': False, 'new_native_parameter_adopted': False, 'H0_measured': False, 'analytic_global_optimum_proved': False, 'derived_cross_survey_independence': False}
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
    assert p.read_bytes() == raw, ('exclusive_byte_reread', p.name)
    p.chmod(0o444)
    h = sha(p)
    CREATED[p.relative_to(J).as_posix()] = h
    return h

def merge(mp):
    for n, h in mp.items():
        p = Path(n)
        p = p if p.is_absolute() else J/p
        p = p.resolve(strict=True)
        if p.as_posix() in EXTERNAL_READONLY_PINS:
            assert h == EXTERNAL_READONLY_PINS[p.as_posix()], 'external_ancestor_byte_seal'
            rel = p.as_posix()
        else:
            p.relative_to(J)
            rel = p.relative_to(J).as_posix()
        assert isinstance(h, str) and len(h) == 64 and sha(p) == h, ('byte_seal', rel)
        assert rel not in SEALS or SEALS[rel] == h, ('conflicting_seal', rel)
        SEALS[rel] = h

def recheck():
    for n, h in {**SEALS, **CREATED}.items():
        assert sha(J/n) == h, ('changed_input_or_output', n)

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

def direct_dist(z, om, rad, order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    xx = z[:, None]*(nodes+1.)/2.
    e2 = 1+om*((1+xx)**3-1.)+rad*((1+xx)**4-1.)
    return z*((1/np.sqrt(e2))@weights)/2.

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
    data = json.loads(canonical(data))
    h = exclusive(p, canonical(data))
    commit = dict(checkpoint=p.name, sha256=h, owner=owner, input_sha256=dict(SEALS))
    exclusive(CP/(name+'.COMMIT.json'), canonical(commit))
    assert json.loads(p.read_text()) == data
    assert json.loads((CP/(name+'.COMMIT.json')).read_text()) == commit
    return data

class SNObjective:
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

def background(a,f):
 a=np.asarray(a,float);ep=f['eps'];norm=1/ep-math.log1p(1/ep);d=f['d0']/a**3;target=.5*ep*norm*d;s=target.copy()
 for _ in range(12):
  q=np.sqrt(1+ep*s/(1+s));dq=ep/(2*q*(1+s)**2);s-=(s*q-target)/(q+s*dq)
 q=np.sqrt(1+ep*s/(1+s));pex=(np.log1p(s)-s/(1+s))/norm
 cs=ep*s/(2+(4+3*ep)*s+2*(1+ep)*s*s);A=1.5*f['OA']/f['rG'];w=A*q*d;rho=A*(1+q*d-pex)
 h=np.sqrt((2/3)*(1.5*f['OB']/f['rG']/a**3+1.5*f['OR']/f['rG']/a**4+rho))
 return dict(s=s,q=q,cs=cs,w=w,rho=rho,h=h,d=d,A=A,charge_error=np.abs(2*q*s/(ep*norm)/d-1))


def authenticate():
    merge(PINS)
    merge({Path(__file__).name: sha(__file__)})
    parent = json.loads((J/(PARENT+'_RESULT.json')).read_text())
    er = json.loads((J/(PARENT+'_RECEIPT.json')).read_text())
    em = json.loads((J/(PARENT+'_MANIFEST.json')).read_text())
    assert parent['manifest'] == em and er['owner'] == em['owner'] == 'root'
    assert er['pid'] == em['pid'] and type(er['pid']) is int and er['pid'] > 0
    assert er['started'] == em['started'] and er['closed'] > er['started']
    assert er['status'] == parent['status'] == 'NUMERICAL_PASS'
    assert er['result_sha256'] == PINS[PARENT+'_RESULT.json']
    assert er['manifest_sha256'] == sha(J/(PARENT+'_MANIFEST.json'))
    merge(em['input_sha256']); merge(er['output_sha256'])
    assert len(parent['controls']) == 31 and all(c['passed'] is True for c in parent['controls'])
    assert len(parent['prior_numerical_gates_copied']) == 52
    assert [r['eps'] for r in parent['rows']] == list(EPS)
    assert all(v is False for v in parent['physical_flags'].values())
    for row in parent['rows']:
        n=PARENT+'_EPS_'+format(row['eps'],'.0e').replace('-','m')+'_CP.json'
        assert json.loads((J/n).read_text()) == row
    sn = json.loads((J/(SN+'_RESULT.json')).read_text())
    sr = json.loads((J/(SN+'_RECEIPT.json')).read_text())
    sm = json.loads((J/(SN+'_MANIFEST.json')).read_text())
    assert sn['manifest'] == sm and sr['owner'] == sm['owner']
    assert sr['owner']['owner'] == 'root' and sr['closed'] > sr['owner']['started']
    assert sr['status'] == sn['status'] == 'NUMERICAL_PASS' and sr['checkpoint_pairs'] == 5
    assert sr['result_sha256'] == PINS[SN+'_RESULT.json']
    assert len(sn['controls']) == 131 and all(c['passed'] is True for c in sn['controls'])
    assert all(v is False for v in sn['physical_flags'].values())
    merge(sr['input_sha256']); merge(sr['output_sha256'])
    assert sn['baseline']['native_parent_rows_copied_exactly'] == parent['rows']
    assert sn['baseline']['fixed'] == em['fixed_parent']
    assert [f['label'] for f in sn['families']] == ['MATCHED_FIXED_RADIATION','ZERO_RADIATION_SUPPLEMENT']
    assert sn['families'][0]['fixed_Omega_r'] == sn['baseline']['normalized_dust']['Omega_r']
    assert sn['families'][1]['fixed_Omega_r'] == 0.
    pairs=0
    for name in sr['output_sha256']:
        if name.endswith('.COMMIT.json'):
            cp=J/name.replace('.COMMIT.json','.json'); data=json.loads(cp.read_text())
            assert data['owner'] == sr['owner'] and data['input_sha256'] == sr['input_sha256']
            assert json.loads((J/name).read_text()) == dict(checkpoint=cp.name,sha256=sha(cp),owner=data['owner'],input_sha256=data['input_sha256'])
            pairs+=1
    assert pairs == 5
    bao=json.loads((J/(BAO+'_RESULT.json')).read_text())
    br=json.loads((J/(BAO+'_RECEIPT.json')).read_text())
    bm=json.loads((J/(BAO+'_MANIFEST.json')).read_text())
    assert bao['manifest'] == br['manifest'] == bm
    assert bao['status'] == br['status'] == 'NEW_BBN_PREDICTED_RULER_BAO_ARITHMETIC_PASS'
    assert br['result_sha256'] == PINS[BAO+'_RESULT.json']
    assert br['manifest_sha256'] == sha(J/(BAO+'_MANIFEST.json'))
    assert bm['physical'] == em['fixed_parent']
    assert len(bao['numerical_gates']) == 5 and all(c['passed'] is True for c in bao['numerical_gates'])
    merge(bm['input_sha256']); merge(br['output_sha256'])
    cp=J/(BAO+'_VECTOR_CP.json');assert json.loads(cp.read_text()) == bao
    assert json.loads((J/(BAO+'_VECTOR_CP_COMMIT.json')).read_text()) == dict(payload=cp.name,sha256=sha(cp),manifest=bm)
    events=[json.loads(x) for x in (J/(BAO+'_JOURNAL.jsonl')).read_text().splitlines()]
    assert [e['event'] for e in events] == ['OWNER_START','CHECKPOINT','OWNER_COMPLETE']
    for e in events:
        assert e['owner']=='root' and e['pid']==events[0]['pid'] and type(e['pid']) is int and e['pid']>0
        assert e['source_sha256']==br['source_sha256'] and e['manifest_sha256']==br['manifest_sha256']
    assert events[-1]['status']==bao['status'] and events[-1]['passed']==events[-1]['gate_count']==5
    assert events[-1]['time'] > events[0]['time'] and events[-1]['result_sha256']==sha(J/(BAO+'_RESULT.json'))
    oldbao=json.loads((J/'DESI_BAO_SHAPE_V001_RESULTS.json').read_text())['payload']
    assert [r['value'] for r in oldbao['data']['order']] == bao['data']
    assert oldbao['data']['covariance'] == bao['covariance']
    assert [[r['z'],r['quantity']] for r in oldbao['data']['order']] == bm['order']
    assert oldbao['checks']['total']==1160 and oldbao['checks']['failed']==0
    own=Path(__file__).read_text(); hs=(J/HELPER_SOURCE).read_text()
    for name,h in HELPER_SHA.items():
        parts=[ast.get_source_segment(x,next(n for n in ast.parse(x).body if isinstance(n,ast.FunctionDef) and n.name==name)) for x in (own,hs)]
        assert parts[0]==parts[1] and hashlib.sha256(parts[0].encode()).hexdigest()==h
    bg=(J/'constrained_u_shared_eps_ngc_pantheon_v001.py').read_text()
    parts=[ast.get_source_segment(x,next(n for n in ast.parse(x).body if isinstance(n,ast.FunctionDef) and n.name=='background')) for x in (own,bg)]
    assert parts[0]==parts[1]
    raw, metadata={},{}
    for key,n in RECEIPTS.items():
        raw[key],metadata[key],parts=decode_receipt(J/n,key)
        for part in parts:merge({part.relative_to(J).as_posix():sha(part)})
    return parent,sn,bao,oldbao,raw,metadata


def bao_vector(expansion, order=96, simpson=False):
    z=np.array([r[0] for r in ORDER]);labels=[r[1] for r in ORDER]
    if simpson:
        nodes=np.linspace(0.,1.,2049);weights=np.ones(2049)
        weights[1:-1:2]=4.;weights[2:-1:2]=2.
        xx=z[:,None]*nodes[None,:]
        dm=z*((1/expansion(xx))@weights)/(3*2048)
    else:
        nodes,weights=np.polynomial.legendre.leggauss(order)
        xx=z[:,None]*(nodes+1.)/2.
        dm=z*((1/expansion(xx))@weights)/2.
    dh=1/expansion(z);dv=np.cbrt(z*dm*dm*dh)
    assert all(np.all(np.isfinite(a)) and np.all(a>0) for a in (dm,dh,dv))
    values={'DM_over_rs':dm,'DH_over_rs':dh,'DV_over_rs':dv}
    return np.array([values[label][i] for i,label in enumerate(labels)])


def bao_fit(vector, data, chol):
    fw=forward(chol,vector);yw=forward(chol,data)
    aa=float(fw@fw);bb=float(fw@yw);cc=float(yw@yw)
    assert math.isfinite(aa) and aa>0 and math.isfinite(bb) and math.isfinite(cc)
    raw=bb/aa;amplitude=max(0.,raw)
    residual=amplitude*vector-data;white=forward(chol,residual)
    score=float(white@white);gradient=2*(amplitude*aa-bb)
    envelope=2*(abs(amplitude*aa)+abs(bb))
    quadratic=amplitude*amplitude*aa-2*amplitude*bb+cc
    assert all(math.isfinite(v) for v in (raw,amplitude,score,gradient,quadratic))
    return dict(Aref=amplitude,Araw=raw,boundary_active=raw<=0.,score=score,
        gradient=gradient,gradient_normalized=(max(0.,-gradient) if raw<=0. else abs(gradient))/max(1.,envelope),hessian=2*aa,
        quadratic_score=quadratic,reference_H_r_d_km_s=C_KMS/amplitude if amplitude>0 else None,
        dimensionless_distance_vector=vector.tolist(),prediction=(amplitude*vector).tolist(),
        residual=residual.tolist(),whitened_residual=white.tolist())


def bao_checks(ck, main, other, label):
    ck.check('BAO_scale_comparison',main['Aref'],other['Aref'],max(1.,abs(main['Aref'])),tol=CONFIG['bao_scale_tolerance'],context=label)
    ck.check('BAO_score_comparison',main['score'],other['score'],tol=CONFIG['bao_score_tolerance'],context=label)
    ck.check('BAO_quadratic_score',main['score'],main['quadratic_score'],tol=CONFIG['bao_score_tolerance'],context=label)
    ck.check('BAO_amplitude_stationarity',main['gradient_normalized'],0.,context=label)


def seed_sn(obj, arm, parent_hash):
    assert arm['order']==obj.order
    for r in arm['evaluated_profile']:
        assert r['Omega_r']==obj.radiation and 0<=r['Omega_m']<=1-obj.radiation
        obj.cache[r['Omega_m']]=dict(r,SN_origin='copied_parent_scalar',SN_parent_sha256=parent_hash,SN_parent_arm=arm['label'])
    for c in arm['candidates']:
        r=c['readout'];old=obj.cache[r['Omega_m']]
        for k,v in old.items():
            if k not in ('SN_origin','SN_parent_sha256','SN_parent_arm'):assert r[k]==v
        obj.cache[r['Omega_m']]=dict(r,SN_origin='copied_parent_candidate',SN_parent_sha256=parent_hash,SN_parent_arm=arm['label'])
    assert len(obj.cache)==len(arm['evaluated_profile'])


class JointObjective:
    def __init__(self, sn, bao_order, data, chol):
        self.sn,self.order,self.radiation=sn,sn.order,sn.radiation
        self.bao_order,self.data,self.chol=bao_order,data,chol
        self.cache={}

    def many(self, values):
        wanted=sorted(set(float(x) for x in values)-set(self.cache))
        assert len(self.cache)+len(wanted)<=CONFIG['evaluation_cap_per_arm'],'joint_evaluation_cap'
        self.sn.many(wanted)
        for om in wanted:
            def expansion(z):return np.sqrt(1+om*((1+z)**3-1)+self.radiation*((1+z)**4-1))
            fit=bao_fit(bao_vector(expansion,self.bao_order),self.data,self.chol)
            r=self.sn.cache[om]
            self.cache[om]=dict(Omega_m=om,Omega_r=self.radiation,Omega_Lambda=1-self.radiation-om,
                score=r['score']+fit['score'],sn_score=r['score'],bao_score=fit['score'],
                magnitude_offset=r['magnitude_offset'],Aref=fit['Aref'],
                offset_gradient_normalized=r['offset_gradient_normalized'],
                amplitude_gradient_normalized=fit['gradient_normalized'],
                SN_origin=r.get('SN_origin','new_joint_point'),bao_fit=fit)

    def score(self,x):
        self.many([x]);return self.cache[float(x)]['score']

    def scalars(self,x):return {k:v for k,v in self.cache[float(x)].items() if k!='bao_fit'}

    def payload(self,x):
        return dict(self.cache[float(x)],sn_readout=self.sn.payload(float(x)))


def joint_arm(obj, old_arm, ck, label):
    xs=[r['Omega_m'] for r in old_arm['grid']];obj.many(xs)
    scores=[obj.score(x) for x in xs]
    candidates=[dict(kind='left_endpoint',grid_index=0,Omega_m=xs[0],score=scores[0],bracket=[xs[0],xs[0]]),
        dict(kind='right_endpoint',grid_index=len(xs)-1,Omega_m=xs[-1],score=scores[-1],bracket=[xs[-1],xs[-1]])]
    for i in range(1,len(xs)-1):
        if scores[i]<=scores[i-1] and scores[i]<=scores[i+1]:
            fit=golden(obj.score,xs[i-1],xs[i+1]);fit.update(kind='refined_sampled_local_minimum',grid_index=i,incoming_bracket=[xs[i-1],xs[i+1]])
            candidates.append(fit)
    best=min(candidates,key=lambda r:(r['score'],r['Omega_m']))
    ck.yes('all_joint_golden_brackets',all(c.get('converged',True) for c in candidates),label)
    ck.check('all_joint_SN_stationarity',[r['offset_gradient_normalized'] for r in obj.cache.values()],0.,context=label)
    ck.check('all_joint_BAO_stationarity',[r['amplitude_gradient_normalized'] for r in obj.cache.values()],0.,context=label)
    ck.check('all_joint_sum_identity',[r['score']-(r['sn_score']+r['bao_score']) for r in obj.cache.values()],0.,context=label)
    ck.yes('joint_best_not_above_grid',best['score']<=min(scores)+CONFIG['score_refinement_tolerance'],label)
    return dict(label=label,grid_count=len(xs),SN_order=obj.order,BAO_order=obj.bao_order,
        incoming_SN_profile_copied_exactly=old_arm,grid=[obj.scalars(x) for x in xs],
        evaluated_profile=[obj.scalars(x) for x in sorted(obj.cache)],
        candidates=[dict(c,readout=obj.payload(c['Omega_m'])) for c in candidates],
        best=obj.payload(best['Omega_m']),best_score=best['score'],best_Omega_m=best['Omega_m'])


def joint_witness(om, obj, ck, label, precision_one):
    obj.many([om]);saved=obj.cache[om];sn=obj.sn
    distance=direct_dist(sn.z,om,obj.radiation,64)
    q=5*np.log10((1+sn.zhel)*distance[sn.inv])
    a=profile_batch(q[:,None],sn.y,sn.L,sn.one,precision_one,ck,label)
    ck.check('joint_SN_global64_score',a[1][0],saved['sn_score'],tol=CONFIG['score_refinement_tolerance'],context=label)
    ck.check('joint_SN_global64_offset',a[0][0],saved['magnitude_offset'],tol=CONFIG['offset_refinement_tolerance'],context=label)
    primary=sn.cache[om]
    if 'distance' in primary:
        ck.check('joint_SN_global64_distance',distance,np.asarray(primary['distance']),distance,tol=CONFIG['distance_tolerance'],context=label)
    simpson=[]
    for i in sorted(set((0,len(sn.z)//2,len(sn.z)-1))):
        lo=-math.log1p(float(sn.z[i]));x=np.linspace(lo,0.,2049);y=np.exp(-x)
        f=y/np.sqrt(1+om*(y**3-1)+obj.radiation*(y**4-1))
        value=float(-lo/2048/3*(f[0]+f[-1]+4*np.sum(f[1:-1:2])+2*np.sum(f[2:-1:2])))
        ck.check('joint_SN_Simpson_log',value,distance[i],distance[i],tol=CONFIG['distance_tolerance'],context=[label,i])
        simpson.append(dict(index=i,zHD=float(sn.z[i]),Simpson2048=value,global64=float(distance[i])))
    def expansion(z):return np.sqrt(1+om*((1+z)**3-1)+obj.radiation*((1+z)**4-1))
    fine=bao_vector(expansion,128);ind=bao_vector(expansion,simpson=True)
    ck.check('joint_BAO_global128_distance',fine,saved['bao_fit']['dimensionless_distance_vector'],fine,tol=CONFIG['bao_distance_tolerance'],context=label)
    ck.check('joint_BAO_Simpson_distance',ind,fine,fine,tol=CONFIG['bao_simpson_tolerance'],context=label)
    b=bao_fit(fine,obj.data,obj.chol);bi=bao_fit(ind,obj.data,obj.chol)
    bao_checks(ck,saved['bao_fit'],b,label);bao_checks(ck,b,bi,[label,'Simpson'])
    ck.check('joint_global_score',a[1][0]+b['score'],saved['score'],tol=CONFIG['score_refinement_tolerance'],context=label)
    return dict(Omega_m=om,Omega_r=obj.radiation,SN_global64_distance=distance.tolist(),
        primary_distance_available=('distance' in primary),
        SN_global64_profile=dict(offset=float(a[0][0]),score=float(a[1][0]),residual=a[2][:,0].tolist(),whitened_residual=a[3][:,0].tolist()),
        SN_Simpson_witnesses=simpson,BAO_global128=b,BAO_Simpson=bi)


def whole_checkpoints(groups,owner):
    assert len(groups)==6 and len(list(CP.glob('*.json')))==12
    for group in groups:
        cp=CP/(group['name']+'.json');assert json.loads(cp.read_text())==group
        assert group['owner']==owner and group['input_sha256']==SEALS
        assert json.loads((CP/(group['name']+'.COMMIT.json')).read_text()) == dict(checkpoint=cp.name,sha256=sha(cp),owner=owner,input_sha256=group['input_sha256'])


def main():
    global np,ORDER
    reserved=[CP]+[J/(STEM+s) for s in ('_MANIFEST.json','_RESULT.json','_REPORT.md','_RECEIPT.json','_ERROR.json')]
    assert not any(p.exists() for p in reserved),'existing_runtime_preserved'
    assert not AUTHOR_DRAFT,'unsealed_author_guard'
    tick=time.monotonic();parent,sn_parent,physical_bao,old_bao,raw,metadata=authenticate()
    for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
    import numpy as runtime_numpy
    np=runtime_numpy;ORDER=physical_bao['manifest']['order']
    owner=dict(owner='root',pid=os.getpid(),source_sha256=sha(__file__),started=utc())
    ck=Checks();groups=[];census=[];families=[]
    manifest=dict(owner=owner,input_sha256=dict(SEALS),configuration=CONFIG,numpy_version=np.__version__,
        SN_parent_sha256=PINS[SN+'_RESULT.json'],native_parent_sha256=PINS[PARENT+'_RESULT.json'],
        predicted_ruler_parent_sha256=PINS[BAO+'_RESULT.json'],exposure=parent['manifest']['exposure'],
        conditional_cross_covariance='Zero SN/BAO cross-covariance is explicitly assumed; not measured',
        native_profiled_nuisance_count=2,comparator_profiled_nuisance_count=3,
        inherited_ordinary_calibration_count=sn_parent['manifest']['inherited_ordinary_calibration_parameter_count'],
        all_four_native_eps_preserved=True,physical_flags=PHYSICAL)
    exclusive(J/(STEM+'_MANIFEST.json'),canonical(manifest));CP.mkdir()
    try:
        qualify(ck)
        zh,zhel,y,cov,data=load_data(raw,ck)
        assert len(y)==1590
        for k,v in data.items():assert sn_parent['baseline']['data'][k]==v,('same_SN_data',k)
        L=np.linalg.cholesky(cov);one=forward(L,np.ones(len(y)));wy=forward(L,y);precision_one=backward(L,one)
        ck.check('SN_Cholesky_reconstruction',L@L.T,cov,tol=CONFIG['covariance_tolerance'])
        ck.check('SN_precision_one',cov@precision_one,np.ones(len(y)),np.maximum(1.,abs(cov)@abs(precision_one)),tol=CONFIG['solve_tolerance'])
        bd=np.asarray(physical_bao['data']);bc=np.asarray(physical_bao['covariance']);BL=np.linalg.cholesky(bc)
        ck.check('BAO_covariance_symmetry',bc,bc.T,tol=CONFIG['covariance_tolerance'])
        ck.check('BAO_Cholesky_reconstruction',BL@BL.T,bc,tol=CONFIG['covariance_tolerance'])
        zz,inv=np.unique(zh,return_inverse=True);fixed=parent['manifest']['fixed_parent']
        for f in sn_parent['families']:
            assert [a['grid_count'] for a in f['arms']]==CONFIG['grids'] and [a['order'] for a in f['arms']]==CONFIG['orders']
        baseline=dict(SN_baseline_copied_exactly=sn_parent['baseline'],SN_families_copied_exactly=sn_parent['families'],
            SN_controls_copied_exactly=sn_parent['controls'],SN_flags_copied_exactly=sn_parent['physical_flags'],
            native_parent_copied_exactly=parent,predicted_ruler_BAO_copied_exactly=physical_bao,
            old_BAO_shape_reference_copied_exactly=old_bao,raw_metadata=metadata,
            scope='Saved SN profiles copied, physical-ruler BAO separate; joint uses profiled late scale')
        groups.append(checkpoint('DATA_AND_PARENTS',baseline,owner));census.append(dict(stage='data_and_synthetic',controls=len(ck.records)))
        synthetic=np.array([1.,2.,4.]);SY=37*synthetic;SL=np.diag([.7,.9,1.1]);fit=bao_fit(synthetic,SY,SL)
        ck.check('synthetic_BAO_amplitude',fit['Aref'],37.,37.)
        ck.check('synthetic_BAO_noiseless',fit['score'],0.,tol=1e-18)
        before=len(ck.records);native=[]
        for row in parent['rows']:
            CONTEXT.update(stage='native_BAO',eps=row['eps']);f=dict(fixed,eps=row['eps'])
            def expansion(z):return background(1/(1+z),f)['h']
            bg=background(np.asarray(1.),f);v48=bao_vector(expansion,48);v96=bao_vector(expansion,96)
            v128=bao_vector(expansion,128);vs=bao_vector(expansion,simpson=True)
            b48,b96,b128,bs=[bao_fit(v,bd,BL) for v in (v48,v96,v128,vs)]
            ck.check('native_BAO_Gauss48_96',v48,v96,v96,tol=CONFIG['bao_distance_tolerance'],context=row['eps'])
            ck.check('native_BAO_Gauss96_128',v96,v128,v128,tol=CONFIG['bao_distance_tolerance'],context=row['eps'])
            ck.check('native_BAO_Simpson',vs,v128,v128,tol=CONFIG['bao_simpson_tolerance'],context=row['eps'])
            for other in (b48,b128,bs):bao_checks(ck,b96,other,row['eps'])
            ck.check('native_background_charge',background(1/(1+np.array([r[0] for r in ORDER])),f)['charge_error'],0.,tol=2e-12,context=row['eps'])
            assert float(bg['cs'])>0 and math.isfinite(float(bg['h']))
            native.append(dict(eps=row['eps'],SN_payload_copied_exactly=row['pantheon'],
                SN_score_copied_exactly=row['pantheon']['profile_rows'][0]['score'],BAO_Gauss48=b48,BAO_Gauss96=b96,
                BAO_Gauss128=b128,BAO_Simpson2048=bs,primary_joint_score=row['pantheon']['profile_rows'][0]['score']+b96['score'],
                E_today=float(bg['h']),H_reference='Hstar',H_today_r_d_km_s=float(bg['h'])*b96['reference_H_r_d_km_s'] if b96['Aref']>0 else None))
            if row['eps']==EPS[0]:ck.check('native_current_physical_distance_bridge',v96*C_KMS/f['Hunit'],physical_bao['distance_vector_Mpc'],physical_bao['distance_vector_Mpc'],tol=CONFIG['bao_distance_tolerance'])
        groups.append(checkpoint('FOUR_NATIVE_BAO',native,owner));census.append(dict(stage='native_BAO',controls=len(ck.records)-before))
        before=len(ck.records)
        oldbest=old_bao['comparator']['profiles'][-1]['best'];om=oldbest['Omega_m']
        oldvector=bao_vector(lambda z:np.sqrt(1+om*((1+z)**3-1)),96);oldfit=bao_fit(oldvector,bd,BL)
        ck.check('old_zero_radiation_BAO_reduction_score',oldfit['score'],oldbest['fit']['chi2'],tol=CONFIG['bao_score_tolerance'])
        ck.check('old_zero_radiation_BAO_reduction_scale',oldfit['Aref'],oldbest['fit']['A'],oldbest['fit']['A'],tol=CONFIG['bao_scale_tolerance'])
        ck.check('old_zero_radiation_BAO_reduction_prediction',oldfit['prediction'],oldbest['fit']['prediction'],np.maximum(1.,abs(np.asarray(oldfit['prediction']))),tol=CONFIG['arithmetic_tolerance'])
        reductions=[]
        for family in sn_parent['families']:
            om=family['arms'][-1]['best_Omega_m'];d=direct_dist(zz,om,family['fixed_Omega_r'],64)
            a=profile_batch((5*np.log10((1+zhel)*d[inv]))[:,None],y,L,one,precision_one,ck,['SN_only_reduction',family['label']])
            ck.check('saved_SN_only_reduction_score',a[1][0],family['arms'][-1]['best_score'],tol=CONFIG['score_refinement_tolerance'],context=family['label'])
            ck.check('saved_SN_only_reduction_offset',a[0][0],family['arms'][-1]['best']['magnitude_offset'],tol=CONFIG['offset_refinement_tolerance'],context=family['label'])
            reductions.append(dict(label=family['label'],saved_best=family['arms'][-1]['best'],global64_score=float(a[1][0]),global64_offset=float(a[0][0])))
        census.append(dict(stage='single_likelihood_reductions',controls=len(ck.records)-before))
        for parent_family in sn_parent['families']:
            label=parent_family['label'];rad=parent_family['fixed_Omega_r'];arms=[];objects=[];before=len(ck.records)
            for old_arm,bo in zip(parent_family['arms'],CONFIG['bao_gauss_orders']):
                so=SNObjective(rad,old_arm['order'],zz,inv,zhel,y,L,one,wy);seed_sn(so,old_arm,PINS[SN+'_RESULT.json'])
                obj=JointObjective(so,bo,bd,BL);name=label+'_GRID'+str(old_arm['grid_count'])+'_JOINT'
                CONTEXT.update(stage='joint_profile',family=label,arm=name)
                arm=joint_arm(obj,old_arm,ck,name);recheck();groups.append(checkpoint(name,arm,owner));arms.append(arm);objects.append(obj)
                print(json.dumps(dict(stage='joint_profile_complete',family=label,arm=name)),flush=True)
            coarse,fine=arms
            ck.check('joint_Omega_refinement',coarse['best_Omega_m'],fine['best_Omega_m'],tol=CONFIG['optimizer_Omega_tolerance'],context=label)
            ck.check('joint_score_refinement',coarse['best_score'],fine['best_score'],tol=CONFIG['score_refinement_tolerance'],context=label)
            ck.check('joint_M_refinement',coarse['best']['magnitude_offset'],fine['best']['magnitude_offset'],tol=CONFIG['optimizer_offset_tolerance'],context=label)
            ck.check('joint_A_refinement',coarse['best']['Aref'],fine['best']['Aref'],max(1.,abs(fine['best']['Aref'])),tol=CONFIG['optimizer_scale_tolerance'],context=label)
            witness=[joint_witness(c['Omega_m'],objects[-1],ck,[label,c['kind'],c['grid_index']],precision_one) for c in fine['candidates']]
            comparisons=[dict(eps=n['eps'],fixed_native_joint_score=n['primary_joint_score'],native_minus_joint_comparator=n['primary_joint_score']-fine['best_score']) for n in native]
            families.append(dict(label=label,primary=parent_family['primary'],fixed_Omega_r=rad,Omega_m_interval=[0.,1-rad],arms=arms,
                witnesses=witness,native_comparisons=comparisons,scope='Common Omega_m conditional product score, same M+A; no physical-ruler fit or superiority'))
            census.append(dict(stage=label,controls=len(ck.records)-before,fine_candidates=len(fine['candidates']),
                joint_evaluations=[len(o.cache) for o in objects],SN_new_evaluations=[sum('SN_origin' not in r for r in o.sn.cache.values()) for o in objects]))
        assert sum(r['controls'] for r in census)==len(ck.records)-2,'census_excludes_two_synthetic_BAO_controls'
        witness_count=sum(len(f['witnesses']) for f in families)
        unsaved_primary_distance_count=sum(not w['primary_distance_available'] for f in families for w in f['witnesses'])
        assert len(ck.records)==139+20*witness_count-unsaved_primary_distance_count,'prospective_control_census'
        whole_checkpoints(groups,owner);recheck();ok=all(c['passed'] for c in ck.records)
        result=dict(status='NUMERICAL_PASS' if ok else 'NUMERICAL_FAILED',manifest=manifest,baseline=baseline,native_rows=native,
            single_likelihood_reductions=dict(SN=reductions,old_zero_radiation_BAO=dict(saved=oldbest,reproduced=oldfit)),families=families,
            numerical_controls=ck.records,control_census=census,synthetic_BAO_control_count=2,all_numerical_controls_passed=ok,
            planned_control_census=dict(fixed=139,fine_candidate_witnesses=witness_count,controls_per_witness=20,
                missing_saved_primary_distances=unsaved_primary_distance_count,total=139+20*witness_count-unsaved_primary_distance_count),
            physical_flags=PHYSICAL,elapsed_seconds=time.monotonic()-tick,
            scope='Conditional independent SN+BAO late-shape comparison, equally profiled M/A; fixed four EPS, one extra comparator shape parameter')
        rh=exclusive(J/(STEM+'_RESULT.json'),canonical(result))
        report=['# Conditional shared SNe plus BAO late-shape comparison', '',result['status'],'',
            '1590 full-covariance SNe and13 full-covariance BAO rows. Their likelihood product assumes zero cross-survey covariance.',
            'All four fixed native epsilon curves are retained with M+A nuisances; comparator fits one common Omega_m plus M+A.',
            'The eps1e-6 physically predicted ruler interval is copied separately, without refitting. Wide-epsilon physical rulers remain open.','',
            '| Family | Grid/SN/BAO order | Common Omega_m | Joint score | SN score | BAO score | M | Aref |',
            '|---|---|---:|---:|---:|---:|---:|---:|']
        for f in families:
            for a in f['arms']:
                b=a['best'];report.append(f"| {f['label']} | {a['grid_count']}/{a['SN_order']}/{a['BAO_order']} | {b['Omega_m']:.12g} | {b['score']:.12g} | {b['sn_score']:.12g} | {b['bao_score']:.12g} | {b['magnitude_offset']:.12g} | {b['Aref']:.12g} |")
        report+=['','| Fixed epsilon | Copied SN score | Profiled BAO score | Joint score | Native inferred Htoday*r_d km/s |','|---|---:|---:|---:|---:|']
        for n in native:report.append(f"| {n['eps']:.0e} | {n['SN_score_copied_exactly']:.12g} | {n['BAO_Gauss96']['score']:.12g} | {n['primary_joint_score']:.12g} | {n['H_today_r_d_km_s']} |")
        report+=['','Aref=c/(Href*r_d); native Href=Hstar and Htoday*r_d=c*E(1)/Aref. No H0 or physical ruler is separately measured.',
            'Primary matched radiation and zero-radiation supplement are both retained, without outcome selection. No epsilon adoption, p-value, superiority, blind validation or full early-universe joint inference. All numerical failures and original controls remain.']
        exclusive(J/(STEM+'_REPORT.md'),('\n'.join(report)+'\n').encode())
        assert json.loads((J/(STEM+'_RESULT.json')).read_text())==result;whole_checkpoints(groups,owner);recheck()
        receipt=dict(status=result['status'],owner=owner,closed=utc(),elapsed_seconds=time.monotonic()-tick,input_sha256=dict(SEALS),
            output_sha256=dict(CREATED),result_sha256=rh,checkpoint_pairs=len(groups),control_count=len(ck.records),physical_flags=PHYSICAL)
        exclusive(J/(STEM+'_RECEIPT.json'),canonical(receipt));recheck()
        print(json.dumps(dict(status=result['status'],result_sha256=rh,receipt_sha256=sha(J/(STEM+'_RECEIPT.json')))),flush=True)
        return 0 if ok else 3
    except Exception:
        exclusive(J/(STEM+'_ERROR.json'),canonical(dict(status='EXECUTION_ERROR_PRESERVED',owner=owner,failed=utc(),context=CONTEXT,
            traceback=traceback.format_exc(),input_sha256=dict(SEALS),output_sha256=dict(CREATED),controls=ck.records,physical_flags=PHYSICAL)))
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true');parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();assert args.root_owned and args.execute,'root_only_explicit_execute'
    raise SystemExit(main())
