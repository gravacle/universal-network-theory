"""Build independent bounded LO review from the previous Codex3 numerical methods."""
from pathlib import Path
import ast
import hashlib
import json
D=Path(__file__).resolve().parent
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/certificates/review_certificates_cx3v003.py')
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='071d2b781ca84de0f2f96cba1bd4d5640b32d5a444004e717c894417b79c0559'
old=BASE.read_text();tree=ast.parse(old)
names={'sha','read','load','Context','search','common_roster','quadrature','gas_P','gas_F'}
parts=[ast.get_source_segment(old,n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
s='''"""0552 independent LO shell review: no certificate/checker imports or worker runs.
Production source/symbol definitions are shared; integration, rho search, algebra
and gas radial-factor reconstruction are independent. Saved C4R3 only.
"""
import sys,os,json,math,hashlib,itertools,time,resource
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
OUT=Path(__file__).resolve().parent
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
CERT=ART/'tail_scheme_impl_c2/certificates_v003'
RECORD=CERT/'gates/LO_CERT_V003_MS128.json'
RECORD_SHA='9fdb897ae3b80dd6a3d2cf9ff273619dbf5fa419405cc8dacd1fa77ee2539268'
DATE_U='Sun Oct 18 15:00:13 UTC 2026'
READS=set()
def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.exec','os.spawn','os.posix_spawn','os.fork','os.forkpty','os.remove','os.unlink','os.rename','os.replace','os.rmdir') or event.startswith('socket.'):
        raise RuntimeError('FORBIDDEN_OPERATION '+event)
    if event=='open' and isinstance(args[0],(str,bytes)):
        p=Path(os.fsdecode(args[0]));absolute=str(p.absolute());real=str(p.resolve())
        if '/runs_ext/UVT_' in real or 'KMAX_A2F10_C5H_RUN_V001' in real:raise RuntimeError('FORBIDDEN_RUN_READ')
        if 'NGC3198' in real.upper() and any(x in real.upper() for x in ('TARGET','OBSERVED')) and 'TARGET_FREE' not in real.upper():raise RuntimeError('FORBIDDEN_NGC_TARGET')
        mode,flags=args[1],args[2]
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing:
            if Path(real).parent!=OUT or not flags & os.O_EXCL:raise RuntimeError('NEW_LO_OUTPUTS_ONLY')
        elif '/Research/' in absolute or '/UNT_' in real:READS.add(absolute)
sys.addaudithook(audit)
'''+ '\n\n'.join(parts)+'\n'
s=s.replace('M_s=64)','M_s=128)')
s+='''
def output(name,data):
    data.update(date_u=DATE_U,utc=datetime.now(timezone.utc).isoformat(),label='TESTED_SAVED_REPLAY_SOURCE_QUADRATURE_ONLY',
        source={'path':__file__,'sha256':sha(__file__)},peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scientific_launches=0,real_targets_opened=False)
    data['read_dependencies']=[{'path':p,'sha256':sha(p)} for p in sorted(READS) if Path(p).is_file()]
    with (OUT/name).open('x') as f:json.dump(data,f,sort_keys=True,indent=2,allow_nan=False);f.write('\\n')
    print(json.dumps({'output':name,'sha256':sha(OUT/name),'seconds':round(time.time()-START,3),'peak_rss_bytes':data['peak_rss_bytes']}),flush=True)

def context_source():
    assert sha(RECORD)==RECORD_SHA
    rec=read(RECORD);ctx=Context();ros,jn=common_roster(ctx)
    assert ros.gas.M_s==128
    assert ros.digest()==rec['build']['roster_digest']
    assert ros.gas.record()==rec['build']['roster_gas']
    assert float(ctx.res['identity']['route_a']['custody']['physical']['gamma'])==ctx.gamma
    return rec,ctx,ros,jn

def static_review():
    rec,ctx,ros,jn=context_source()
    checks=[]
    def ck(name,value,details=None):checks.append({'name':name,'passed':bool(value),'details':details})
    ck('required_source_gas_M_s_field',type(rec.get('source_gas_M_s')) is int and rec.get('source_gas_M_s')==128,
       {'source_gas_M_s':rec.get('source_gas_M_s'),'actual_gas_M_s':rec.get('gas_M_s')})
    ck('actual_source_M_s128_and_roster_digest',ros.gas.M_s==128 and ros.digest()==rec['build']['roster_digest'])
    ck('config_roster_and_declared_M_s128',rec['gas_M_s']==rec['tail_config_gas']['M_s']==rec['build']['roster_gas']['M_s']==128)
    for label,pin in dict(rec['pins'],producer=rec['producer'],common=rec['common']).items():ck('byte_pin_'+label,sha(pin['path'])==pin['sha256'])
    producer=Path(rec['producer']['path']).read_text();common=Path(rec['common']['path']).read_text()
    ck('producer_passes128_to_roster_and_config','C3.ddo_roster(U, RS, PV, jn, \'C4R3\', C3.MS_PROD)' in producer and 'M_s=C3.MS_PROD' in producer and 'MS_PROD = 128' in common)
    ck('producer_missing_field_confirmed','source_gas_M_s' not in producer and 'gas_M_s=int(C3.MS_PROD)' in producer)
    rows=read(rec['pins']['row_binding']['path'])['query_rows'];prereg=read(rec['pins']['prereg_v005']['path'])
    ids=[r['id'] for r in rows];R=np.array([r['radius_m'] for r in rows]);tau=np.array(prereg['tau_km_s'])
    v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']])
    ck('row_ids_radii_tau_saved_predictions',ids==rec['row_ids']==prereg['row_ids'] and np.array_equal(R/ctx.kpc,rec['R_kpc']) and np.array_equal(tau,rec['tau_km_s']) and np.array_equal(v,rec['v_state_km_s']))
    ranges=[sh['range_inverse_kpc'] for sh in rec['shells']]
    ck('ten_contiguous_shells_cover4_to363',len(ranges)==10 and ranges[0][0]==4 and ranges[-1][1]==363 and all(a[1]==b[0] for a,b in zip(ranges,ranges[1:])))
    for P in (64,128):ck('coverage_full_reach_P'+str(P),rec['coverage_inverse_kpc'][1]>=math.sqrt(2)*2*P and rec['envelope_bound']['coverage_max_inverse_kpc']>=math.sqrt(2)*2*P,{'required':math.sqrt(2)*2*P,'available':rec['coverage_inverse_kpc'][1]})
    errors=[]
    for sh in rec['shells']:
        ratio=v*R*sh['rho_used']*sh['B1_per_m']/4/tau
        err=float(np.max(np.abs(ratio-np.asarray(sh['per_row_over_tau']))))
        errors.append(err)
        ck('shell_algebra_'+str(sh['range_inverse_kpc']),np.allclose(ratio,sh['per_row_over_tau'],rtol=5e-15,atol=0) and math.isclose(float(max(ratio)),sh['max_over_tau'],rel_tol=5e-15),err)
        ck('shell_rho_envelope_and_tolerance_'+str(sh['range_inverse_kpc']),sh['rho_used']==max(sh['rho_G_sampled'],sh['rho_G_envelope']) and sh['max_over_tau']<=.005)
    ck('summed_all10_tolerance',math.isclose(math.fsum(sh['max_over_tau'] for sh in rec['shells']),rec['summed_max_over_tau'],rel_tol=5e-15) and rec['summed_max_over_tau']<=.05)
    ck('envelope_estimate_not_proof_labeled','not a proven' in rec['label'] and 'not a proven' in rec['envelope_bound']['label'])
    # Small independent normalized Lagrange reconstruction verifies actual Ms128
    # radial factors. This is distinct from trusting the producer's record label.
    kp=np.array([0.,128.,154.25,193.5,227.6,255.99])/ctx.kpc
    own=gas_P(ros.gas,kp,128,jn);actual=ros.gas.radial_factors(kp,jn.j0)
    relative=float(np.max(np.abs(own-actual))/np.max(np.abs(own)))
    ck('independent_Ms128_radial_factor_replica',relative<1e-12,relative)
    output('LO_STATIC_REVIEW_V001.json',{'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'record':{'path':str(RECORD),'sha256':RECORD_SHA},
       'record_contract':'FAIL_REQUIRED_FIELD' if not checks[0]['passed'] else 'PASS','source_roster_digest':ros.digest(),'source_gas_M_s_measured':ros.gas.M_s,
       'max_algebra_error':max(errors),'numeric_shell_max':max(sh['max_over_tau'] for sh in rec['shells']),'summed_max_over_tau':rec['summed_max_over_tau'],
       'source_scope':'Actual permitted C4R3 saved source reconstructed at Ms128; no producer/checker import or scientific solve.'})

def integral(level):
    rec,ctx,ros,jn=context_source();shell=next(sh for sh in rec['shells'] if sh['range_inverse_kpc']==[128.,256.])
    width=.5;n=16;nodes=np.cos(np.pi*np.arange(n)/(n-1));bw=(-1.)**np.arange(n);bw[[0,-1]]*=.5
    zz=(np.arange(513)[:,None]+(nodes[None,:]+1)/2)*width
    tab=ros.vertical_factors(zz.ravel()/ctx.kpc,299792458.).reshape(513,n,-1)
    def interpolate(z,table):
        panel=np.minimum(np.floor(z/width).astype(int),512);u=2*(z/width-panel)-1;d=u[:,None]-nodes
        hit=np.abs(d)<1e-14;d[hit]=1.;a=bw/d;a[hit.any(axis=1)]=0.;a[hit]=1.;a/=a.sum(axis=1)[:,None]
        return np.einsum('ij,ij...->i...',a,table[panel])
    ztest=np.random.default_rng(552128).uniform(0,256,150);direct=ros.vertical_factors(ztest/ctx.kpc,299792458.);approx=interpolate(ztest,tab)
    interpolation=float(np.max(np.abs(direct-approx))/np.max(np.abs(direct)))
    assert interpolation<1e-11
    step,order=(.5,10) if level=='coarse' else (.25,12)
    p1,w1=quadrature(0,127,step,order);u,wu=quadrature(0,1,1/8,order);p2=128-u*u;w2=2*u*wu
    p3,w3=quadrature(128,255,step,order);p4=256-u*u;w4=2*u*wu
    kp=np.r_[p1,p2,p3,p4];wp=np.r_[w1,w2,w3,w4]
    P=ros.radial_factors(kp/ctx.kpc,jn.j0);B0=0.;B1=0.;node_count=0
    for j,k in enumerate(kp):
        low=math.sqrt(max(0.,128**2-k*k));high=math.sqrt(max(0.,256**2-k*k));z,wz=quadrature(low,high,step,order)
        Sv=interpolate(z,tab@P[j]);km=np.sqrt(k*k+z*z)/ctx.kpc
        base=(4*np.pi*k*wp[j]/ctx.kpc**3)*wz*np.abs(Sv)/(4*ctx.gamma*km**2)/(2*np.pi)**3
        B0+=float(base.sum());B1+=float(np.sum(base*km));node_count+=len(z)
        if j%1000==0:print(json.dumps({'level':level,'radial_nodes_complete':j,'total':len(kp),'seconds':round(time.time()-START,1)}),flush=True)
    v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']]);R=np.array(rec['R_kpc'])*ctx.kpc;tau=np.array(rec['tau_km_s'])
    derived=float(np.max(v*R/tau)*shell['rho_used']*B1/4)
    output('LO_INTEGRAL_'+level.upper()+'_V001.json',{'shell':[128.,256.],'source_gas_M_s':ros.gas.M_s,'source_roster_digest':ros.digest(),
      'panel_width':step,'order':order,'B0':B0,'B1':B1,'k_perp_nodes':len(kp),'tensor_nodes_evaluated':node_count,
      'vertical_interpolation_max_relative':interpolation,'certificate_B0':shell['B0'],'certificate_B1':shell['B1_per_m'],
      'B1_relative_difference':abs(B1/shell['B1_per_m']-1),'max_over_tau_using_certificate_rho':derived,'shell_tolerance':.005,'numeric_pass':derived<=.005,
      'method':'Independent nested cylindrical GL integration of complete spherical shell128<|k|<=256, abs source; endpoint square-root maps; barycentric vertical interpolation validated directly. Shared continuum source implementation; no certificate producer/checker imports.'})

def rho():
    assert sha(RECORD)==RECORD_SHA
    ctx=Context();rec=read(RECORD);shell=next(sh for sh in rec['shells'] if sh['range_inverse_kpc']==[128.,256.])
    answer=search(ctx,128,256,'RHO',552256)
    witness=shell['rho_envelope_search'];point=np.r_[witness['t_at'],witness['dir_at'],witness['k_at_inverse_kpc']]
    recomputed=ctx.quantity(point,'RHO')
    output('LO_RHO_REVIEW_V001.json',{'shell':[128.,256.],'own_search':answer,'certificate_rho':shell['rho_used'],
        'certificate_witness_recomputed':recomputed,'witness_relative_difference':abs(recomputed/shell['rho_used']-1),
        'qualification':'Independent direct symbol binding and own sampled/local search; numerical estimate, not interval/Lipschitz proof. Certificate witness evaluation is separately labeled.'})

if __name__=='__main__':
    for key in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):assert os.environ.get(key)=='1'
    START=time.time()
    if sys.argv[1]=='static':static_review()
    elif sys.argv[1]=='rho':rho()
    elif sys.argv[1] in ('coarse','refined'):integral(sys.argv[1])
    else:raise ValueError('unknown mode')
'''
compile(s,'<lo-review>','exec')
p=D/'review_lo_ms128_cx3v001.py'
with p.open('x') as f:f.write(s)
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
