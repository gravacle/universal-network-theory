"""NEW fixed .99 same-parent Pantheon+ profile; root --execute only.
No producer import, cosmological/state fit, BBN/atomic/calibration or trajectory.
"""
import os
for _thread_variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_thread_variable]='1'
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import base64
import hashlib
import io
import json
import math
import time
import urllib.parse
import zlib
import numpy as np
BASE=Path(__file__).resolve().parent
HERE=BASE
STEM='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V001'
PROTOCOL_SHA='b7a6b63d0ef2da2dbc147543e152d3503192951b2d5b8cbec925559d627c9ae8'
PINS={'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py': '0440a959e2a662203b57f3da39afee973f41cc90fbe289520415f50f3da94f3b', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001.md': '74e0c0ce3be19e1cb115d47f21eefeaf122f3530b1d4bd6a3eae194c0960051f', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RESULT.json': '844d085f18ab85589793858d24fb4a3333741175c6a7d5b41792d83b331ee403', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': 'e0dab9c7d3e335001908ed10f43972b4f6b97658061490087720a3ffcb2d16d7', 'pantheon_finite_pressure_v001.py': '02b27f41f2cb0072e5d3b2418f3633b78338554fdea206046dc20e9c3197a350', 'PANTHEON_FINITE_PRESSURE_PROTOCOL_V001.md': '561f024fc1f31992c911a3edff5f1776f565fbc274eaefbe523a8aa42af21f87', 'PANTHEON_INPUT_SELECTION_V001.md': 'be486e54eed8acc14f345aa8382cdc8aec8e6f448f9691d876bc5cd6adf71fa2', 'fetch_pantheon_reference_v001.py': '03d001317e99dedbdc43838abfd9eab46e62e339e021e3a2cea518e1f3b1a5f3', 'pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json': 'c2408ce5f9914c349d926a89e8124adc8828b7f885075aa8a08e0d5a9e4357bb', 'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json': '58317db1be2c6591309a206f6ac6b54d564218f596f639457389eaaa5945a573', 'pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json': '1be77d822136ac140b6e1bb7b260133c6d91fcd901e34cd002ef40d089b14497', 'pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json': '1d1aaeef696bcc99c711b05bb5c6226936485d927b063acda6c561e726fe5eaf'}
HELPER_SHA={'decode_receipt': 'eeef7b943bb5c00d887f3265c271edf2784b884a3eb656d60c2f7ff69e45dada', 'load_data': '869dd2ad368e6e97b3817326fa30bb1a5c3224f1b190a8c23a99c9024b66ba57', 'forward': '10e1416b0621828cd660bc725b7f272bd2b530bb086d8a2f9e5d4e83deb3f667', 'backward': '84b5a3cbb60dd96969f3ffa57f4db51018ce1d3b3d9a6ee421ed6c5d41025a11', 'profile_batch': '0f5dcc5f2c28beb582c3be79e6b5f4dca7c23c75ddb93dc10586f4d3316229ed'}
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001'
BACKGROUND_SPAN_SHA='eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2'
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
COMMIT='c447f0fea703fcd0fff57de5000947b5ca81286b'
RECEIPTS={'vector':'pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json','covariance':'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json','readme':'pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json','likelihood':'pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json'}
REMOTE_PATHS={'vector':'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat','covariance':'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov','readme':'Pantheon+_Data/4_DISTANCES_AND_COVAR/README','likelihood':'Pantheon+_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon+_only_cosmosis_likelihood.py'}
CONFIG=dict(expected_total_rows=1701,redshift_cut_exclusive=.01,source_size_ceiling=64*1024*1024,covariance_tolerance=2e-12,arithmetic_tolerance=2e-11,solve_tolerance=2e-10,distance_tolerance=2e-10,offset_refinement_tolerance=2e-9,score_refinement_tolerance=2e-6,profiled_parameters=['common magnitude offset'],observational_success_gate=None)
SHAPES=('CURRENT','DUST_LIMIT')
ARMS=('PRIMARY','INTERVAL8','GLOBAL64')
SEALS={}
CREATED={}
RUN_SOURCE=''
RUN_MANIFEST=''


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(name,obj,raw=False):
    p=BASE/name;data=obj if raw else (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h;return h

def seal(p,h):
    p=Path(p).resolve()
    if not (p.is_relative_to(BASE.parent.parent.resolve()) or (p==Path('/usr/bin/clang').resolve() and h==COMPILER_SHA)) or sha(p)!=h:raise AssertionError('Input path/seal '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting seal')
    SEALS[str(p)]=h

def recheck():
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed sealed input/prefix '+p)
    if sha(__file__)!=RUN_SOURCE:raise AssertionError('Changed source')

def journal(event,**data):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(event=event,owner='root',pid=os.getpid(),time=now(),source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,**data),sort_keys=True)+'\n')


class Checks:
    def __init__(self):self.records=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG['arithmetic_tolerance'] if tol is None else tol
        er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
        mx=float(np.max(er));ok=bool(np.all(np.isfinite(er)) and mx<=tol)
        self.records.append(dict(name=name,error=mx,tolerance=tol,scalar_count=int(er.size),passed=ok,context=context))
    def yes(self,name,value,context=None):self.check(name,int(bool(value)),1.,context=context)


def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))

def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    raw=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    if (raw['status']!='NEW_BBN_ACOUSTIC_ARITHMETIC_PASS' or receipt['status']!=raw['status'] or not raw['all_numerical_gates_passed']
        or len(raw['numerical_gates'])!=22 or not all(g['passed'] for g in raw['numerical_gates'])
        or receipt['source_sha256']!=PINS['constrained_u_clock_gradient_bbn_acoustic_readout_v001.py']
        or receipt['result_sha256']!=PINS[PARENT+'_RESULT.json'] or raw['manifest']!=receipt['manifest']):raise AssertionError('Acoustic source/parent qualification')
    for p,h in dict(receipt['manifest']['input_sha256'],**receipt['output_sha256']).items():seal(p,h)
    seal(BASE/(PARENT+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(PARENT+'_JOURNAL.jsonl'),receipt['journal_sha256'])
    events=[json.loads(t) for t in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    if ([e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE']
        or [e['arm'] for e in events[1:-1]]!=['DEFAULT','HALF','THIN','QUADRATURE']
        or events[-1]['status']!=raw['status'] or events[-1]['result_sha256']!=receipt['result_sha256']
        or events[-1]['gate_count']!=22 or events[-1]['passed']!=22):raise AssertionError('Acoustic natural closure')
    owner=events[0]['pid']
    for e in events:
        if (e['owner']!='root' or type(e['pid']) is not int or e['pid']!=owner or e['source_sha256']!=receipt['source_sha256']
            or e['manifest_sha256']!=receipt['manifest_sha256']):raise AssertionError('Acoustic root/source/manifest/PID')
    for e,row in zip(events[1:-1],raw['rows']):
        pn=PARENT+'_'+row['label']+'_CP.json';cn=PARENT+'_'+row['label']+'_CP_COMMIT.json';co=json.loads((BASE/cn).read_text())
        if (e['payload']!=pn or e['sha256']!=sha(BASE/pn) or e['commit_sha256']!=sha(BASE/cn)
            or co!=dict(manifest=raw['manifest'],arm=row['label'],payload=pn,sha256=e['sha256']) or json.loads((BASE/pn).read_text())!=row):raise AssertionError('Acoustic full committed arm')
    old=(BASE/'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py').read_text();own=Path(__file__).read_text()
    old=(BASE/'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py').read_text();own=Path(__file__).read_text()
    n0=next(n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    n1=next(n for n in ast.parse(own).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    if ast.get_source_segment(old,n0)!=ast.get_source_segment(own,n1) or hashlib.sha256(ast.get_source_segment(own,n1).encode()).hexdigest()!=BACKGROUND_SPAN_SHA:raise AssertionError('Exact current background span')
    ps=(BASE/'pantheon_finite_pressure_v001.py').read_text();pt=ast.parse(ps);ot=ast.parse(own)
    for name,h in HELPER_SHA.items():
        n0=next(n for n in pt.body if isinstance(n,ast.FunctionDef) and n.name==name)
        n1=next(n for n in ot.body if isinstance(n,ast.FunctionDef) and n.name==name)
        b0=ast.get_source_segment(ps,n0);b1=ast.get_source_segment(own,n1)
        if b0!=b1 or hashlib.sha256(b1.encode()).hexdigest()!=h:raise AssertionError('Pure Pantheon helper '+name)
    sources={};metadata={}
    for key,rel in RECEIPTS.items():
        p=BASE/rel;sources[key],metadata[key],parts=decode_receipt(p,key)
        for part in parts:seal(part,sha(part))
    return raw,sources,metadata


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


def expansion(a,fixed,shape):
    aa=np.asarray(a,float)
    if shape=='CURRENT':
        return np.array([background(math.log(float(t)),fixed)['h'] for t in aa.reshape(-1)]).reshape(aa.shape)
    if shape!='DUST_LIMIT':raise AssertionError('Frozen shape')
    return np.sqrt((fixed['OA']*(1+fixed['d0']/aa**3)+fixed['OB']/aa**3+fixed['OR']/aa**4)/fixed['rG'])


def gauss_intervals(func,lo,hi,n):
    t,w=np.polynomial.legendre.leggauss(n)
    lo,hi=np.asarray(lo,float),np.asarray(hi,float)
    xx=lo[:,None]+(hi-lo)[:,None]*(t+1)/2
    return (hi-lo)*(func(xx)@w)/2


def distances(func,z):
    lo=np.concatenate(([0.],z[:-1]));hi=z
    primary=np.cumsum(gauss_intervals(func,lo,hi,16))
    coarse=np.cumsum(gauss_intervals(func,lo,hi,8))
    global64=gauss_intervals(func,np.zeros_like(z),z,64)
    return np.column_stack((primary,coarse,global64))


def simpson_log(fixed,shape,z,panels=2048):
    lo=-math.log1p(float(z));xx=np.linspace(lo,0.,panels+1)
    vv=np.exp(-xx)/expansion(np.exp(xx),fixed,shape)
    return float((0-lo)/panels/3*(vv[0]+vv[-1]+4*sum(vv[1:-1:2])+2*sum(vv[2:-1:2])))


def qualify(ck):
    L=np.array([[2.,0.,0.],[.4,1.3,0.],[-.2,.3,.7]]);X=np.arange(1.,10.).reshape(3,3)
    ck.check('synthetic_forward',forward(L,L@X),X,np.maximum(1.,abs(X)))
    ck.check('synthetic_backward',backward(L,L.T@X),X,np.maximum(1.,abs(X)))
    C=L@L.T;one=np.ones(3);u=forward(L,one);v=backward(L,u)
    ck.check('synthetic_precision',v,np.linalg.solve(C,one),np.maximum(1.,abs(v)))
    q=np.array([1.,3.,4.]);y=q+17.;ans=profile_batch(q[:,None],y,L,u,v,ck,'synthetic')
    ck.check('synthetic_offset',ans[0],17.,17.);ck.check('synthetic_score',ans[1],0.,tol=1e-18)
    shifted=profile_batch((q+2.)[:,None],y,L,u,v,ck,'synthetic_shift')
    ck.check('synthetic_offset_shift',shifted[0],ans[0]-2.);ck.check('synthetic_residual_shift',shifted[2],ans[2])
    z=np.array([.0101,.1,.5,1.,2.5]);hel=z+np.array([.001,-.001,.002,-.002,.003])
    for mode in ('constant','matter'):
        func=(lambda zz:np.ones_like(zz)) if mode=='constant' else (lambda zz:(1+zz)**(-1.5))
        dm=distances(func,z);exact=z if mode=='constant' else 2*(1-1/np.sqrt(1+z))
        ck.check('synthetic_distance',dm,exact[:,None],np.ones_like(dm),tol=CONFIG['distance_tolerance'],context=mode)
        ck.check('synthetic_luminosity_convention',(1+hel)*dm[:,0],(1+z)*(1+hel)*dm[:,0]/(1+z),np.ones(len(z)),context=mode)


def shape_payload(shape,fixed,zh,zhel,y,L,white_one,precision_one,ck):
    z,inv=np.unique(zh,return_inverse=True)
    dm=distances(lambda zz:1/expansion(1/(1+zz),fixed,shape),z)
    if dm.shape!=(len(z),3) or not np.all(np.isfinite(dm)) or not np.all(dm>0):raise AssertionError('Positive complete distance arms')
    for arm,col in (('INTERVAL8',1),('GLOBAL64',2)):
        ck.check('distance_refinement',dm[:,col],dm[:,0],dm[:,0],tol=CONFIG['distance_tolerance'],context=[shape,arm])
    witness=[]
    for i in sorted(set((0,len(z)//2,len(z)-1))):
        value=simpson_log(fixed,shape,z[i]);ck.check('independent_Simpson_log',value,dm[i,0],dm[i,0],tol=CONFIG['distance_tolerance'],context=[shape,i])
        witness.append(dict(index=i,zHD=float(z[i]),Simpson2048=value,primary=float(dm[i,0]),signed_difference=float(value-dm[i,0])))
    q=5*np.log10((1+zhel[:,None])*dm[inv,:])
    ans=profile_batch(q,y,L,white_one,precision_one,ck,shape)
    for col,arm in ((1,'INTERVAL8'),(2,'GLOBAL64')):
        ck.check('offset_refinement',ans[0][col],ans[0][0],tol=CONFIG['offset_refinement_tolerance'],context=[shape,arm])
        ck.check('score_refinement',ans[1][col],ans[1][0],tol=CONFIG['score_refinement_tolerance'],context=[shape,arm])
    unit=299792.458/fixed['Hunit'];rows=[]
    for col,arm in enumerate(ARMS):
        rows.append(dict(arm=arm,magnitude_offset=float(ans[0][col]),score=float(ans[1][col]),profile_derivative=float(ans[4][col]),profile_curvature=2*ans[5],implied_absolute_M_at_fixed_Hstar=float(ans[0][col]-25-5*math.log10(unit)),magnitude_shape=q[:,col].tolist(),residual=(ans[2][:,col]).tolist(),whitened_residual=ans[3][:,col].tolist(),signed_offset_minus_primary=float(ans[0][col]-ans[0][0]),signed_score_minus_primary=float(ans[1][col]-ans[1][0])))
    return dict(shape=shape,unique_zHD=z.tolist(),dimensionless_distance_arms=dm.tolist(),luminosity_unit_Mpc=unit,profile_rows=rows,Simpson_witnesses=witness,H_today_km_s_Mpc=float(fixed['Hunit']*expansion(np.array([1.]),fixed,shape)[0]),scope='Fixed shape, one common magnitude offset; mathematical ablation is not refitted LCDM')


def main():
    global RUN_SOURCE,RUN_MANIFEST
    tick=time.monotonic();RUN_SOURCE=sha(__file__)
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Existing runtime prefix including orphan/failure preserved before manifest')
    parent,sources,transport=authenticate();ck=Checks();qualify(ck)
    zh,zhel,y,cov,data=load_data(sources,ck)
    if len(y)!=1590 or len(data['original_row_indices'])!=1590:raise AssertionError('Frozen1590 measurement census')
    # CID repeats are retained measurements, not multiple independent supernovae.
    data['repeated_CID_measurement_count']=len(data['CID'])-len(set(data['CID']))
    data['excluded_original_row_indices']=sorted(set(range(1701))-set(data['original_row_indices']))
    if len(data['excluded_original_row_indices'])!=111:raise AssertionError('Frozen111 exclusions')
    L=np.linalg.cholesky(cov);ck.check('Cholesky_reconstruction',L@L.T,cov,tol=CONFIG['covariance_tolerance'])
    one=np.ones(len(y));white_one=forward(L,one);precision_one=backward(L,white_one)
    ck.check('full_precision_one_residual',cov@precision_one,one,np.maximum(1.,abs(cov)@abs(precision_one)),tol=CONFIG['solve_tolerance'])
    ck.check('white_one_residual',L@white_one,one,np.maximum(1.,abs(L)@abs(white_one)),tol=CONFIG['solve_tolerance'])
    del cov
    fixed=parent['manifest']['fixed'];ordinary=parent['manifest']['ordinary']
    manifest=dict(source_sha256=RUN_SOURCE,input_sha256=dict(SEALS),fixed=fixed,ordinary=ordinary,transport=transport,configuration=CONFIG,shapes=list(SHAPES),arms=list(ARMS),numpy_version=np.__version__,measurement_count=1590,new_profiled_nuisance_count_per_shape=1,inherited_ordinary_calibration_parameter_count=2,exposure='D/H+compressed theta ancestor calibration and historical Pantheon-derived context; no blind holdout')
    RUN_MANIFEST=write(STEM+'_MANIFEST.json',manifest);journal('OWNER_START');rows=[]
    for shape in SHAPES:
        recheck();row=shape_payload(shape,fixed,zh,zhel,y,L,white_one,precision_one,ck)
        pn=STEM+'_'+shape+'_CP.json';cn=STEM+'_'+shape+'_CP_COMMIT.json';h=write(pn,row);ch=write(cn,dict(manifest=manifest,shape=shape,payload=pn,sha256=h));journal('CHECKPOINT',shape=shape,payload=pn,sha256=h,commit_sha256=ch);rows.append(row)
        print(json.dumps(dict(shape=shape,status='COMPLETE_FIXED_PROFILE_CHECKPOINT')),flush=True)
    aa,bb=[r['profile_rows'][0] for r in rows]
    ablation=dict(score_current_minus_dust=aa['score']-bb['score'],offset_current_minus_dust=aa['magnitude_offset']-bb['magnitude_offset'],residual_current_minus_dust=(np.array(aa['residual'])-np.array(bb['residual'])).tolist(),whitened_current_minus_dust=(np.array(aa['whitened_residual'])-np.array(bb['whitened_residual'])).tolist(),scope='Predetermined same-inventory eps->0 ablation; not independently fitted cosmology or evidence ranking')
    ok=all(g['passed'] for g in ck.records);status='NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS' if ok else 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_FAILED'
    result=dict(status=status,all_numerical_gates_passed=ok,manifest=manifest,data=data,rows=rows,paired_ablation=ablation,numerical_gates=ck.records,elapsed_seconds=time.monotonic()-tick,scope='Exposed1590 full-covariance measurement profile; no H0/absolute-M measurement, physical fit, joint likelihood, p-value, superiority or inflation/thermal-origin claim')
    recheck();rh=write(STEM+'_RESULT.json',result)
    report=['# NEW fixed .99 common-action Pantheon+ profile V001','',status,f"{sum(g['passed'] for g in ck.records)}/{len(ck.records)} fixed numerical controls PASS.",'','1590 published measurements, full STAT+SYS covariance and one common magnitude offset per fixed shape. No physical parameter fit. Duplicate SN measurements retained.','', '| Shape | Arm | Score | Magnitude offset | Htoday km/s/Mpc |','|---|---|---:|---:|---:|']
    for row in rows:
        for arm in row['profile_rows']:report.append(f"| {row['shape']} | {arm['arm']} | {arm['score']:.12g} | {arm['magnitude_offset']:.12g} | {row['H_today_km_s_Mpc']:.12g} |")
    report+=['',f"CURRENT-minus-DUST primary score: {ablation['score_current_minus_dust']:.12g}.",'DUST is the fixed eps->0 same-inventory ablation, not an optimized LCDM comparison. Ancestor calibration/data exposure is counted; no blind holdout, p-value or superiority claim. All signed numerical arms/failures and per-measurement residuals remain in JSON.']
    reph=write(STEM+'_REPORT.md',('\n'.join(report)+'\n').encode(),True);recheck()
    ev=[json.loads(s) for s in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    if len(ev)!=3 or [e['event'] for e in ev]!=['OWNER_START','CHECKPOINT','CHECKPOINT'] or [e['shape'] for e in ev[1:]]!=list(SHAPES):raise AssertionError('Two ordered complete shape commits')
    for e in ev:
        if e['owner']!='root' or e['pid']!=os.getpid() or e['source_sha256']!=RUN_SOURCE or e['manifest_sha256']!=RUN_MANIFEST:raise AssertionError('Root/source/manifest/PID custody')
    for e,row in zip(ev[1:],rows):
        pn=STEM+'_'+row['shape']+'_CP.json';cn=STEM+'_'+row['shape']+'_CP_COMMIT.json'
        if e['payload']!=pn or e['sha256']!=sha(BASE/pn) or e['commit_sha256']!=sha(BASE/cn) or json.loads((BASE/cn).read_text())!=dict(manifest=manifest,shape=row['shape'],payload=pn,sha256=e['sha256']) or json.loads((BASE/pn).read_text())!=row:raise AssertionError('Full committed shape payload')
    recheck();journal('OWNER_COMPLETE',status=status,result_sha256=rh,gate_count=len(ck.records),passed=sum(g['passed'] for g in ck.records))
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=RUN_SOURCE,manifest=manifest,manifest_sha256=RUN_MANIFEST,result_sha256=rh,report_sha256=reph,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),output_sha256=dict(CREATED)))
    recheck();print(json.dumps(dict(status=status,result_sha256=rh,elapsed_seconds=result['elapsed_seconds'])),flush=True);return 0 if ok else 3


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root alone launches --execute')
    if list(BASE.glob(STEM+'_*')):raise SystemExit('Existing runtime prefix; no retry/failure mutation')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),pid=os.getpid(),time=now(),source_sha256=sha(__file__)));raise
