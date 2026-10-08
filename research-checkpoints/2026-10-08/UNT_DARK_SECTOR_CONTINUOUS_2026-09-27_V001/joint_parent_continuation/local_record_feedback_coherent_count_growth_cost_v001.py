#!/usr/bin/env python3
"""Saved 16-state D²/variance only. No native producer, H, or history execution."""
import os, sys, json, hashlib, math, time
from pathlib import Path
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE=Path(__file__).resolve()
PROTOCOL=J/'LOCAL_RECORD_FEEDBACK_COHERENT_COUNT_GROWTH_COST_V001.md'
PROTOCOL_SHA='4722728dd519f1a0409ac9a12e88ec71bf3579f25caf0982f6a0a5a583869c4e'
PINS={
    "BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.json": "be5bce8c92163cdb10000e1e706a1b6ad8b1a01c15299ad5a7d6f6a8e9b40ccf",
    "BS10_K33_LOCAL_PROPER_BOND_V001.md": "adc621de1903c22f7309e2efda958874af1373a0e1243d6018010700bb16996d",
    "BS10_K33_LOCAL_PROPER_BOND_V001_RECEIPT.json": "3063faf3ce99b544cdb1442a04577adc86dbf41766fae7063607e809e77957d5",
    "BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.json": "614c876af835afbf542203cc9a2422716c3f6d2b0ebff77c0d80e56ccfa5d809",
    "BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.md": "ba07087be2317f2c1324b4fe06e1c488c8bc7456e8713a58639a9512abd39f40",
    "BS10_K33_NODAL_SIGNAL_V001.md": "a8abf2801422b4ae4e450ec4a2819f1d3cbdef9fdc937ec008e61d3c030b340d",
    "BS10_K33_NODAL_SIGNAL_V001_RESULT.json": "7a4fc007d3ca9a46482091f4e6ab54a78c866dd4eabaeb19fc4d83b766c2499c",
    "KINETIC_RULER_AND_PHYSICAL_CENSUS_HYPOTHESIS_V001.md": "f5b2986719281523ba348822292ee20d8bb3062c082c42eb0192dbf3ddb50af1",
    "LOCAL_COUNT_SUPPLY_STABILITY_AND_RESOURCE_GATE_V001.md": "0c73b602820f7bcf85ee8410855f6a82f28aa0b60274ae6c5d9287ac3e584637",
    "LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md": "e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43",
    "LOCAL_PROPER_BOND_NORMALIZATION_V001.md": "9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b",
    "LOCAL_RECORD_FEEDBACK_FLOATING_CAP_COUNT_COMPLETION_V001.md": "97562eae265f43cef842a5cfb125aede1d8edce2b7b6e21a0292634b3d3a21c7",
    "bs10_k33_census_creation_saved_v001.py": "ca5429b498a274c26765667a2f4f5ab333d998e9d9cb07894c0243b2f77d9948",
    "bs10_k33_local_proper_bond_v001.py": "4c9a761b913993765ac2018f52d8d7ea88bf0e22d836e1c437a87efdc8419c60",
    "bs10_k33_nodal_signal_v001.py": "349828cfdb729fceb2593bd7084e348226206f4781c1af71aaeb137a76bfbbf9",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n0_age0.bundle.npz": "5198a2484bbf14bd67d648cc58faf80b97cae045cb8f9d5c661be573e1cdc534",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n0_age20.bundle.npz": "22760378e1281de116824f38b503eaca90b1c5ac76d35cd9e92dff5b0534d5ef",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n0_age5.bundle.npz": "7b009f0693d6470ddc56d10120f976a7fef390bfe1d07e4455522655de73b261",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n0_age50.bundle.npz": "100e0e5c5dc84d8b892bb69ac79f034e2c57acf491d36be28252423e438de150",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n413_age0.bundle.npz": "ff2f65ef730c467623dd2a808efe65aea78069b67ac6f7621a67497287d78fff",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n413_age20.bundle.npz": "cc5d6df5bcf0728141b526f8df851fd3e5d1eb2718990683838e31a19ed2dc82",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n413_age5.bundle.npz": "008aa970eec3700f7306f2dcc5060a23f402bc362137b9c0156d61ab7937aab1",
    "bs10_k33_nodal_signal_v001_checkpoints/g0_n413_age50.bundle.npz": "3476459a1808f6daee0ba13f66983192e629af759e803e719fa24dc0f7270839",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n0_age0.bundle.npz": "b0a377dc0c0d1aed2c40c05788dc050c4bfe4895a12f7c68f5bf866096a018f5",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n0_age20.bundle.npz": "2046c59ab589f97a6a4f04496622f658d658c955da49b7623eb1585afaa4055a",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n0_age5.bundle.npz": "0ba4e64c031144aa4069909ee733781ecdc635bdd8ef7031a60a29d379c7732b",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n0_age50.bundle.npz": "289b5c46140c4c5e27b60e1f667ecb3ac921a9b65ebf41026186a5deea66bd3d",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n413_age0.bundle.npz": "2dc17dda39eb3594c1f67e48590626df302d82208699cfaaaca6d3d44663db85",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n413_age20.bundle.npz": "88c1009f40fda5302b52c4febb435ee57175a3e493d93ef3f7c357be9d3db28c",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n413_age5.bundle.npz": "ec697306f4570b9d4d551bee3281a939e46ecfb97da8343317a0a42fc3adc329",
    "bs10_k33_nodal_signal_v001_checkpoints/g1_n413_age50.bundle.npz": "4776ce99e6e428d75901daff3895624f124fa222f89d1f46b6768f260a0a2a0e"
}
NAME='COHERENT_COUNT_GROWTH_COST_V001'
OUT=J/(NAME+'_RESULT.json'); REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json'); ERROR=J/(NAME+'_ERROR.json')
CP=J/'coherent_count_growth_cost_v001_checkpoints'
CHECKS=[]; INPUTS={}; ACTIVE={}; ATOL=5e-11

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def canonical(o):
    return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def safe(o):
    if isinstance(o,float) and not math.isfinite(o): return {'nonfinite':repr(o)}
    if isinstance(o,dict): return {str(k):safe(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [safe(v) for v in o]
    return o

def check(name,ok,**evidence):
    CHECKS.append(dict(name=name,passed=bool(ok),evidence=safe(evidence)))
    if not ok: raise AssertionError(name)

def close(name,x,y):
    err=abs(x-y); allowance=ATOL*max(1.,abs(y))
    check(name,math.isfinite(x) and math.isfinite(y) and err<=allowance,
          actual=x,expected=y,residual=err,allowance=allowance)

def pin(p,h):
    p=Path(p).resolve(); actual=sha(p)
    check('seal:'+str(p),actual==h,actual=actual,expected=h)
    if str(p) in INPUTS: check('same-seal:'+str(p),INPUTS[str(p)]==h)
    INPUTS[str(p)]=h

def read(p): return json.loads(Path(p).read_text())

def exclusive(p,o,text=False):
    data=o if text else json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n'
    with Path(p).open('x') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    return sha(p)

def event(kind,**kw):
    with (CP/'events.jsonl').open('a') as f:
        f.write(json.dumps(dict(event=kind,pid=os.getpid(),**kw),sort_keys=True,allow_nan=False)+'\n')
        f.flush(); os.fsync(f.fileno())

def rat(v): return int(v['numerator'])/int(v['denominator'])

def event_has(events,kind,**kw):
    return any(e.get('event')==kind and all(e.get(k)==v for k,v in kw.items()) for e in events)

def authenticate():
    pin(PROTOCOL,PROTOCOL_SHA); pin(SOURCE,sha(SOURCE))
    for n,h in PINS.items(): pin(J/n,h)
    local=read(J/'BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.json')
    receipt=read(J/'BS10_K33_LOCAL_PROPER_BOND_V001_RECEIPT.json')
    census=read(J/'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.json')
    nodal=read(J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json')
    for label,o in [('local',local),('census',census),('nodal',nodal)]:
        check(label+'_passed',o['failed_count']==0 and all(c['passed'] for c in o['checks']))
        b=dict(o); digest=b.pop('canonical_payload_sha256')
        check(label+'_canonical',canonical(b)==digest)
    for o in (local,census,nodal['manifest']):
        for p,h in o['input_sha256'].items(): pin(Path(p) if Path(p).is_absolute() else J/p,h)
    lcp=J/'bs10_k33_local_proper_bond_v001_checkpoints'
    ncp=J/'bs10_k33_nodal_signal_v001_checkpoints'
    pin(lcp/'manifest.json',receipt['manifest_sha256']);pin(lcp/'events.jsonl',receipt['journal_sha256'])
    check('local_receipt_identities',all(receipt[k]==local[k] for k in
          ('pid','source_sha256','protocol_sha256','canonical_payload_sha256','check_count','passed_count','failed_count','row_sha256','input_sha256')))
    check('local_receipt_raw_report',receipt['result_sha256']==sha(J/'BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.json') and receipt['report_sha256']==sha(J/'BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.md'))
    pin(ncp/'manifest.json',sha(ncp/'manifest.json'));pin(ncp/'events.jsonl',sha(ncp/'events.jsonl'))
    check('nodal_manifest',read(ncp/'manifest.json')==nodal['manifest'])
    le=[json.loads(x) for x in (lcp/'events.jsonl').read_text().splitlines()]
    ne=[json.loads(x) for x in (ncp/'events.jsonl').read_text().splitlines()]
    for label,es,o,mp,result_event,result_name in (
          ('local',le,local,lcp/'manifest.json','result_completed','BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.json'),
          ('nodal',ne,nodal,ncp/'manifest.json','result_saved','BS10_K33_NODAL_SIGNAL_V001_RESULT.json')):
        pid=o['pid'] if label=='local' else o['manifest']['pid']
        starts=[e for e in es if e.get('event')=='started']
        check(label+'_start',len(starts)==1 and starts[0]['pid']==pid and starts[0]['manifest_sha256']==sha(mp))
        check(label+'_result_commit',event_has(es,result_event,pid=pid,sha256=sha(J/result_name),canonical_payload_sha256=o['canonical_payload_sha256']))
    oldm=read(J/'bs10_k33_unclamped_formation_v001_checkpoints/manifest.json')['inputs']
    check('packing_manifest',oldm['dimension']==196608 and oldm['Nc']==1 and oldm['N']==3 and oldm['carrier_start']==0 and oldm['record_start']=='allblank' and oldm['edges']==[[i,3+j] for i in range(3) for j in range(3)])
    expected=[f'g{g}_n{n}_age{a}' for g in (0,1) for n in (0,413) for a in (0,5,20,50)]
    check('exact16order',[r['key'] for r in census['rows']]==expected==[r['key'] for r in local['rows']])
    check('nodal16',len(nodal['rows'])==16)
    nr={Path(r['bundle_path']).stem.replace('.bundle',''):r for r in nodal['rows']}
    for r in census['rows']:
        k=r['key']; bp=Path(r['input_bundle_path']); b=nr[k]
        check(k+'_parent_bundle',r['input_bundle_sha256']==b['bundle_sha256']==PINS[str(bp.relative_to(J))] and str(bp)==b['bundle_path'])
        check(k+'_labels',r['g']==b['g'] and r['start']==b['start'] and r['age']==b['age'])
        pin(ncp/(k+'.json'),sha(ncp/(k+'.json')))
        check(k+'_nodal_row_commit',event_has(ne,'row_complete',key=k,sha256=sha(ncp/(k+'.json'))))
        check(k+'_nodal_bundle_commit',event_has(ne,'bundle_saved',key=k,sha256=r['input_bundle_sha256']))
        pin(lcp/(k+'.json'),local['row_sha256'][k])
        check(k+'_local_row_commit',event_has(le,'row_completed',key=k,sha256=local['row_sha256'][k]))
    return local,census,nr

def moments(np,row,old,nodal):
    key=row['key']; ACTIVE.update(key=key,bundle=row['input_bundle_path'],phase='saved-state contraction')
    with np.load(row['input_bundle_path'],allow_pickle=False) as z:
        cols=z['input_columns']; metadata=json.loads(str(z['metadata_json']))
        check(key+'_shape',cols.shape==(3,196608) and cols.dtype==np.dtype('complex128'))
        check(key+'_metadata',metadata['g']==row['g'] and metadata['start']==row['start'] and metadata['age']==row['age'] and set(metadata['input_column_norms'])=={'psi','h0psi','h0_squared_psi'} and metadata['input_sha256']==nodal['input_sha256'])
        check(key+'_error_provenance',metadata['certified_vector_error_ceilings']==nodal['certified_vector_error_ceilings'] and metadata['original_bundle_sha256']==nodal['original_bundle_sha256'])
        psi=cols[0].reshape(512,6,64).copy()
    masks=np.arange(512); n=(masks&1).astype(float)[:,None,None]
    tx=np.zeros_like(psi); tx[:,0,:]=psi[:,3,:]; tx[:,3,:]=psi[:,0,:]
    xp=psi[masks^1]; xt=tx[masks^1]
    ends=np.zeros_like(psi);ends[:,0,:]=psi[:,0,:];ends[:,3,:]=psi[:,3,:]
    dp=8*(1-n)*psi+.1*n*tx+.2*xp
    poly=64*(1-n)*psi+.01*n*ends+.04*psi+1.6*xp+.02*xt
    norm=float(np.vdot(psi,psi).real);d1=np.vdot(psi,dp);d2=np.vdot(psi,poly)
    sq=float(np.vdot(dp,dp).real); lk=np.vdot(psi,.32*psi+.01*n*ends)
    for label,z in [('norm',norm),('D',d1.real),('D²_poly',d2.real),('D²_norm',sq),('leak',lk.real)]:
        check(key+'_finite_'+label,math.isfinite(float(z)))
    check(key+'_positive_norm',norm>0)
    close(key+'_saved_norm',norm,row['raw_norm']);close(key+'_local_norm',norm,rat(old['raw_state_norm_squared']))
    close(key+'_metadata_norm',norm,metadata['input_norm'])
    close(key+'_D_imaginary',float(d1.imag),0.);close(key+'_D²_imaginary',float(d2.imag),0.);close(key+'_leak_imaginary',float(lk.imag),0.)
    close(key+'_D²_two_routes',sq,float(d2.real))
    mu=float(d1.real)/norm;m2=sq/norm;var=m2-mu*mu;kap=float(lk.real)/norm
    close(key+'_mean_benchmark',mu,rat(old['normalized_local_work']))
    close(key+'_leak_benchmark',kap,rat(old['normalized_local_leakage']))
    check(key+'_variance_no_clip',var>=-ATOL*max(1.,m2),raw_variance=var)
    check(key+'_operator_ranges',abs(mu)<=8.3+ATOL and -ATOL<=m2<=8.3**2+ATOL and .32-ATOL<=kap<=.33+ATOL)
    if row['age']==0:
        target=(8.,64.04,.04,.32) if row['start']==0 else (0.,.05,.05,.33)
        for label,x,y in zip(('mu','m2','var','leak'),(mu,m2,var,kap),target):close(key+'_age0_'+label,x,y)
    return dict(key=key,g=row['g'],start=row['start'],age=row['age'],bundle_sha256=row['input_bundle_sha256'],
        raw_norm_squared=norm,raw_D=float(d1.real),raw_D2_norm=sq,raw_D2_polynomial=float(d2.real),raw_leak=float(lk.real),
        mu_D=mu,second_D=m2,variance_D=var,leakage=kap,shift_polynomial_s_ascending=[m2+kap,2*mu,1.],
        symbolic_shift='s=2*Sself+nu*P-Delta_d',symbolic_fourth_bracket='(s+mu_D)^2+variance_D+leakage+4*epsilon^2',
        detuning_independent_floor_without_4epsilon_squared=var+kap,
        probability_coefficients=dict(tau2='epsilon^2',tau3=0,tau4='-epsilon^2*((s+mu_D)^2+variance_D+leakage+4*epsilon^2)/12',remainder='O(tau^5), no finite-interval certificate'),
        network_work_leading='epsilon^2*tau^2*(mu_D+2*Sself)',
        inherited=dict(P1_directed_roundoff_certified=old['P1_directed_roundoff_certified'],P1_floating_budgets_conditional=old['P1_floating_budgets_conditional'],physically_qualified_mean_sign=old['physically_qualified_mean_sign'],
          original_input_norm=nodal['input_norm'],certified_vector_error_ceilings=metadata['certified_vector_error_ceilings'],source_state_qualification='Original saved history; no new cap evolution or physical q4 inclusion'))

def main():
    if sys.argv[1:]!=['--execute']: raise SystemExit('Explicit --execute required; no contraction performed.')
    started=time.monotonic(); rows=[]
    try:
        check('exclusive_paths',not any(p.exists() for p in (OUT,REPORT,RECEIPT,ERROR,CP)))
        local,census,nodal=authenticate()
        CP.mkdir();mh=exclusive(CP/'manifest.json',dict(pid=os.getpid(),source_sha256=sha(SOURCE),protocol_sha256=PROTOCOL_SHA,input_sha256=INPUTS,keys=[r['key'] for r in census['rows']],resume=False))
        event('started',manifest_sha256=mh)
        import numpy as np
        for r,old in zip(census['rows'],local['rows']):
            b=moments(np,r,old,nodal[r['key']]); rows.append(b)
            h=exclusive(CP/(r['key']+'.json'),b);event('state_completed',key=r['key'],sha256=h)
            print(r['key']+' completed',flush=True)
        for p,h in list(INPUTS.items()):pin(p,h)
        check('complete16',len(rows)==16)
        result=dict(status='SAVED_STATE_LOCAL_COST_MOMENTS_ARITHMETIC',source_sha256=sha(SOURCE),protocol_sha256=PROTOCOL_SHA,input_sha256=INPUTS,manifest_sha256=mh,rows=rows,check_count=len(CHECKS),passed_count=len(CHECKS),failed_count=0,checks=CHECKS.copy(),pid=os.getpid(),runtime_seconds=time.monotonic()-started,scope='Symbolic coherent count coefficients only; no physical q4 adoption, donor fit, rate, pressure or metric')
        result['canonical_payload_sha256']=canonical(result);rh=exclusive(OUT,result);event('result_completed',sha256=rh,canonical_payload_sha256=result['canonical_payload_sha256'])
        lines=['# Saved coherent-count cost moments V001','',result['status'],'','| State | μD | 〈D²〉 | VarD | κ | VarD+κ |','|---|---:|---:|---:|---:|---:|']
        for r in rows:lines.append('| '+r['key']+' | '+' | '.join(format(r[k],'.16g') for k in ('mu_D','second_D','variance_D','leakage','detuning_independent_floor_without_4epsilon_squared'))+' |')
        lines+=['','Every τ4 bracket is (s+μD)²+VarD+κ+4ε². Neither s nor ε is selected. Pnew=ε²τ²−ε²τ4 bracket/12+O(τ5).','No finite-interval remainder, physical four-port insertion, directed-rounding trajectory qualification, pressure or expansion rate is earned.','',f'Checks: {len(CHECKS)}/{len(CHECKS)}. Raw SHA256: {rh}.']
        ph=exclusive(REPORT,'\n'.join(lines)+'\n',text=True);event('report_completed',sha256=ph)
        for p,h in INPUTS.items():
            if sha(p)!=h: raise AssertionError('Post-output input seal: '+p)
        eh=sha(CP/'events.jsonl')
        exclusive(RECEIPT,dict(status=result['status'],source_sha256=sha(SOURCE),protocol_sha256=PROTOCOL_SHA,input_sha256=INPUTS,result_sha256=rh,canonical_payload_sha256=result['canonical_payload_sha256'],report_sha256=ph,manifest_sha256=mh,journal_sha256=eh,check_count=len(CHECKS),passed_count=len(CHECKS),failed_count=0,pid=os.getpid()))
    except BaseException as e:
        if not ERROR.exists():exclusive(ERROR,safe(dict(status='ARITHMETIC_FAILED',type=type(e).__name__,message=str(e),active=ACTIVE,completed_keys=[r['key'] for r in rows],checks=CHECKS,input_sha256=INPUTS,source_sha256=sha(SOURCE),protocol_sha256=PROTOCOL_SHA)))
        raise

if __name__=='__main__':main()
