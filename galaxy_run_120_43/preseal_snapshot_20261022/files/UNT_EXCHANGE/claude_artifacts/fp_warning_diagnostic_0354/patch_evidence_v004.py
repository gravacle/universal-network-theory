"""Synthetic evidence V004 for the 0354 patch proposal V004 (review NOTE corrections N1-N3; N5 tests E8-E11 added): producer V002 vs PATCH_PROPOSAL on the SAME generic 16-site toy (not UNT),
fixture spec and pins; compares all computed content, warning counts, flag accounting, PYTHONWARNINGS=error, and NaN injection.
Run without -I (NumPy user site). Work dir argv[1] or temp. Never deletes."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
V2=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/bind_coupling_0351/producer_A/owned_bind_coupling_reference_producer_v002.py')
PR=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/fp_warning_diagnostic_0354/PATCH_PROPOSAL_bind_producer_v004.py')
SPEC_REAL=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/bind_coupling_0351/producer_A/BIND_COUPLING_REFERENCE_FROZEN_SPEC_V001.json')
T=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp(prefix='fp_patch_v004_'));T.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
A1="CASE_IDS=['L4','L6']";A2='def run_case(L,p,checks,dfam):'
GENERIC='''
import json as _tj
_MODE=_tj.loads(os.environ.get('BC_TEST_MODE','{}'))
_CUR=['']
_OOS=set()
_orig_solve=np.linalg.solve
def _solve_t(a,b):  # TEST-ONLY: in mode inf_solve, the full-inverse solve returns one inf entry (eigh already succeeded)
 r=_orig_solve(a,b)
 if _MODE.get(_CUR[0])=='inf_solve' and np.ndim(b)==2 and b.shape[0]==b.shape[1]:r=r.copy();r[0,0]=float('inf')
 return r
np.linalg.solve=_solve_t
_N=16
_G=np.zeros((_N,_N))
for _i in range(_N):
 for _d,_wt in ((1,1.0),(5,0.3)):
  _j=(_i+_d)%_N;_G[_i,_j]=_G[_j,_i]=-_wt
_Bo=np.zeros((_N,_N));_Bo[0,0]=-0.3
_Bn=np.zeros((_N,_N));_Bn[8,8]=-0.3
def _ham(a,b):return sum(i!=j for i,j in zip(a,b))
def q_sites(L):return [0,3,8,11]  # TEST-ONLY
def assemble(L,bits,p):  # TEST-ONLY generic 16-site toy, NOT (M)
 c=0.5*_ham(bits,X_BITS)*_ham(bits,Y_BITS)
 M=_G+bits[0]*_Bo+bits[1]*_Bn+c*np.eye(_N)
 if _MODE.get(_CUR[0])=='nan' and bits==(1,1,1,1,0,0):M=M.copy();M[2,2]=float('nan')
 if _MODE.get(_CUR[0])=='oos_warn' and _CUR[0] not in _OOS:_OOS.add(_CUR[0]);_z=np.float64(1.0)/np.float64(0.0)  # TEST-ONLY out-of-site warning
 return M,Fraction(0)
def analytic_lambda(L):return {'k_L':0.0,'lambda_L':float(np.linalg.eigvalsh(-(_G+_Bo))[-1]),'method':'TEST-ONLY'}
'''
def build(tag,src):
    d=T/tag;d.mkdir();docs={}
    for k in ('feshbach_source','source_family_companion','all_even_family_proof','all_even_family_review','feshbach_distinct_review','freezing'):
        f=d/(k+'.md');f.write_bytes(('synthetic '+k).encode());docs[k]=(str(f),sha(f.read_bytes()))
    spec=json.loads(SPEC_REAL.read_text());spec['bound_documents']={k:{'path':docs[k][0],'sha256':docs[k][1]} for k in docs if k!='freezing'};spec['freezing_document']={'path':docs['freezing'][0],'sha256':docs['freezing'][1]}
    sb=json.dumps(spec).encode();(d/'spec.json').write_bytes(sb)
    over='SPEC=%r\nBOUND=%r\nFREEZING=%r  # TEST-ONLY\n'%((str(d/'spec.json'),sha(sb)),{k:docs[k] for k in docs if k!='freezing'},docs['freezing'])
    s=src.read_text().replace(A1,over+A1).replace(A2,GENERIC+A2)
    s=s.replace(" res=analyze(L,p,checks)"," _CUR[0]=CASE_IDS[[4,6].index(L)];res=analyze(L,p,checks)",1).replace(" try:res=analyze(L,p,checks)"," _CUR[0]=CASE_IDS[[4,6].index(L)]\n try:res=analyze(L,p,checks)",1)
    pf=d/'producer.py';pf.write_text(s);return d,pf
def run(d,pf,mode=None,env_extra=None):
    env=dict(os.environ);env['BC_TEST_MODE']=json.dumps(mode or {});env.pop('PYTHONWARNINGS',None)
    if env_extra:env.update(env_extra)
    r=subprocess.run([sys.executable,'-B',str(pf),'--output',str(d/'out.json'),'--journal',str(d/'j.jsonl')],capture_output=True,text=True,env=env,timeout=60)
    o=json.loads((d/'out.json').read_text()) if (d/'out.json').exists() else None
    return r.returncode,o,r.stderr
def strip(o):
    o=json.loads(json.dumps(o))
    for k in ('schema','pins','environment','resources','floating_point_warnings_captured'):o.pop(k,None)
    for c in o['cases']:c.pop('backend_flag_events',None)
    return o
res=[]
def case(n,ok,det=''):res.append((n,bool(ok),det));print(('PASS ' if ok else 'FAIL ')+n+(' | '+det if det else ''))
d2,p2=build('v002',V2);rc2,o2,e2=run(d2,p2)
dp,pp=build('proposal',PR);rcp,op,ep=run(dp,pp)
case('E1 both COMPLETED on the generic 16-site toy',rc2==0 and rcp==0 and o2['status']==op['status']=='COMPLETED',e2[-200:]+ep[-200:])
case('E2 all computed content bit-identical (JSON-equal) between V002 and the proposal',strip(o2)==strip(op))
w2={k:v['count'] for k,v in o2['floating_point_warnings_captured'].items()};wp={k:v['count'] for k,v in op['floating_point_warnings_captured'].items()}
case('E3 V002 reproduces the saved-run pattern (1008 RuntimeWarnings per case = 4 flags x 252 N x N matmuls); proposal emits 0 RuntimeWarnings',w2=={'L4':1008,'L6':1008} and wp=={'L4':0,'L6':0},json.dumps([w2,wp]))
fe=op['cases'][0]['backend_flag_events']
case('E4 proposal accounts every flagged product at the four sites (64+64+62+62=252), all four kinds, all VERIFIED (finite, within non-BLAS bound)',{k:v['calls_with_flags'] for k,v in fe.items()}=={'eig_residual':64,'eig_orthogonality':64,'spectral_inverse':62,'inverse_residual':62} and all(v['classification']=='FLAGGED_PRODUCTS_FINITE_WITHIN_NONBLAS_ROUNDING_BOUND' and v['all_within_nonblas_bound'] is True and v['nonfinite_products']==0 and v['bound_evaluated_products']==v['calls_with_flags'] and set(v['flag_kinds'])=={'divide by zero','overflow','underflow','invalid value'} for v in fe.values()),json.dumps({k:[v['calls_with_flags'],v['max_abs_deviation_over_finite_deviations']] for k,v in fe.items()}))
d3,p3=build('proposal_pywarn_error',PR);rc3,o3,e3=run(d3,p3,env_extra={'PYTHONWARNINGS':'error'})
case('E5 proposal under PYTHONWARNINGS=error: COMPLETED, stderr empty, identical content',rc3==0 and e3=='' and strip(o3)==strip(op))
d4,p4=build('proposal_nan',PR);rc4,o4,e4=run(d4,p4,mode={'L4':'nan'})
c4=o4['cases'][0]
case('E6 genuine NaN input end-to-end: L4 CASE_ERROR (eigh refuses; not hidden), run FAILED exit 1, flag events attached; L6 unaffected',rc4==1 and o4['status']=='FAILED' and c4['status']=='CASE_ERROR' and 'backend_flag_events' in c4 and o4['cases'][1]['status']=='COMPUTED',json.dumps(c4.get('error')))
# unit: mm() on a genuinely non-finite product (direct, generic 16x16)
ns={'__name__':'proposal_unit'};exec(compile(PR.read_text(),str(PR),'exec'),ns)
np_=ns['np'];A=np_.eye(16);A[0,0]=float('inf');B=np_.ones((16,16));ns['FLAG_EVENTS'].clear()
import warnings as _w
with _w.catch_warnings(record=True) as WW:
    _w.simplefilter('always');out=ns['mm']('unit_site',A,B)
rep=ns['flag_report']()
case('E6b unit: a genuinely non-finite product is NOT masked: returned as inf/nan, recorded FLAGGED_PRODUCT_NOT_VERIFIED (all_finite false, all_within_nonblas_bound null: N1), no RuntimeWarning swallowed into success',(not np_.all(np_.isfinite(out))) and rep['unit_site']['classification']=='FLAGGED_PRODUCT_NOT_VERIFIED' and rep['unit_site']['all_finite'] is False and rep['unit_site']['all_within_nonblas_bound'] is None and rep['unit_site']['nonfinite_products']==1 and rep['unit_site']['bound_evaluated_products']==0,json.dumps(rep['unit_site']))
UA=np_.eye(16);UB=np_.ones((16,16));ns['FLAG_EVENTS'].clear();out2=ns['mm']('unit_ok',UA,UB);rep2=ns['flag_report']()
case('E6c unit: an exact finite flagged product is VERIFIED and bit-identical to the plain matmul',bool(np_.array_equal(out2,np_.einsum('ij,jk->ik',UA,UB,optimize=False))) and all(v['classification']=='FLAGGED_PRODUCTS_FINITE_WITHIN_NONBLAS_ROUNDING_BOUND' for v in rep2.values()),json.dumps(rep2))
d5,p5=build('v002_nan',V2);rc5,o5,e5=run(d5,p5,mode={'L4':'nan'})
case('E7 V002 on the same NaN input also fails (CASE_ERROR): behaviour on genuine failures unchanged',rc5==1 and o5['cases'][0]['status']=='CASE_ERROR')
# ---- N5 additions ----
d8,p8=build('proposal_inf_solve',PR);rc8,o8,e8=run(d8,p8,mode={'L4':'inf_solve'})
c8=o8['cases'][0] if o8 else {};ir=c8.get('backend_flag_events',{}).get('inverse_residual',{})
cf8=[x for x in (o8 or {}).get('check_failures',[]) if x.get('case_id')=='L4']
case('E8 in-pipeline non-finite flagged product (inverse_residual after eigh succeeded): reported nonfinite, all_within_nonblas_bound null, NOT_VERIFIED; run not a clean COMPLETED (CASE_ERROR or check failure)',
 rc8 in (0,1) and o8 is not None and ir.get('nonfinite_products',0)>=1 and ir.get('all_within_nonblas_bound','x') is None and ir.get('classification')=='FLAGGED_PRODUCT_NOT_VERIFIED' and (c8.get('status')=='CASE_ERROR' or any(x['check']=='backend_flag_unverified' for x in cf8)) and o8['cases'][1]['status']=='COMPUTED',
 json.dumps({'rc':rc8,'status':(o8 or {}).get('status'),'L4':c8.get('status'),'error':c8.get('error'),'inverse_residual':ir,'cf':cf8})[:900])
import numpy as _np
ns['FLAG_EVENTS'].clear();g0=_np.geterr();c0=_np.geterrcall();raised=None
try:ns['mm']('unit_exc',_np.ones((16,16)),_np.ones((15,16)))
except ValueError as e:raised='ValueError'
case('E9a errstate and seterrcall restored after an exception inside mm',raised=='ValueError' and _np.geterr()==g0 and _np.geterrcall() is c0,json.dumps({'raised':raised}))
ok_in=True;after_raises=False
with _np.errstate(all='raise'):
    try:ns['mm']('unit_raise',_np.eye(16),_np.ones((16,16)))
    except FloatingPointError:ok_in=False
    try:_np.eye(16)@_np.ones((16,16))
    except FloatingPointError:after_raises=True
case("E9b inside an outer errstate(all='raise'): mm does not raise, and a plain flagged matmul afterwards still raises (outer state restored)",ok_in and after_raises and _np.geterr()==g0,json.dumps({'mm_ok':ok_in,'plain_raises_after':after_raises}))
d10,p10=build('proposal_oos',PR);rc10,o10,e10=run(d10,p10,mode={'L4':'oos_warn'})
d11,p11=build('v002_oos',V2);rc11,o11,e11=run(d11,p11,mode={'L4':'oos_warn'})
wc=lambda o:{k:v['count'] for k,v in o['floating_point_warnings_captured'].items()}
case('E10 out-of-site warning stays visible in the pipeline: proposal L4 captures exactly 1 (V002 captures 1009), L6 0 vs 1008; content identical to the clean run',
 rc10==0 and wc(o10)=={'L4':1,'L6':0} and wc(o11)=={'L4':1009,'L6':1008} and strip(o10)==strip(op),json.dumps([wc(o10),wc(o11)]))
ns['FLAG_EVENTS'].clear();SA=_np.full((16,16),1e-160);SB=_np.full((16,16),1e-160)
with _np.errstate(all='ignore'):plain=SA@SB
o12=ns['mm']('unit_subnormal',SA,SB);r12=ns['flag_report']().get('unit_subnormal')
case('E11 N3: a product with subnormal results is bit-identical to plain matmul and, if flagged, verified via the absolute underflow term',
 bool(_np.array_equal(o12,plain)) and (r12 is None or r12['classification']=='FLAGGED_PRODUCTS_FINITE_WITHIN_NONBLAS_ROUNDING_BOUND'),json.dumps({'flagged':r12 is not None,'report':r12,'sample':float(o12[0,0])}))
print('WORKDIR',T);print('SUMMARY',sum(ok for _,ok,_ in res),'/',len(res),'passed')
