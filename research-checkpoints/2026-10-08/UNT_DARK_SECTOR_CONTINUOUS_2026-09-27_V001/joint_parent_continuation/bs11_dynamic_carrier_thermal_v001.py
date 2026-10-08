#!/usr/bin/env python3
"""Prospective fixed-sector thermal Kubo sums from sealed BS11 states; no solver."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=HERE/'BS11_DYNAMIC_CARRIER_THERMAL_V001.md'
SOURCE=HERE/'bs11_dynamic_carrier_thermal_v001.py'
COLD=HERE/'BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json'
DEST=HERE/'BS11_DYNAMIC_CARRIER_THERMAL_V001_RESULT.json'
REPORT=HERE/'BS11_DYNAMIC_CARRIER_THERMAL_V001_RESULT.md'
CP=HERE/'bs11_dynamic_carrier_thermal_v001_checkpoints'
TEMPERATURES=(0.,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1.)
PROBE_BETA=1e-6
OP_TOL,EIG_TOL,CHI_TOL,THERMO_TOL=1e-11,2e-10,2e-8,2e-10
MAX_RSS,MAX_SECONDS=512*1024*1024,60.
UD,DELTA,ER,EP,HFLIP,THOP=1.,0.,1.,1.,.1,.1

def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def exclusive(path,obj):
    with path.open('x',encoding='utf-8') as f:
        json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def event(kind,**data):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=kind,pid=os.getpid(),utc=utc(),**data),sort_keys=True)+'\n')
        f.flush();os.fsync(f.fileno())
def matrix_sha(np,a):return hashlib.sha256(np.ascontiguousarray(a,dtype='<f8').tobytes()).hexdigest()
def identity_inputs():
    cold=json.loads(COLD.read_text())
    anchors={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE),str(COLD):sha(COLD)}
    for path,digest in cold['input_sha256'].items():
        if sha(Path(path))!=digest:raise RuntimeError('Cold input anchor changed: '+path)
        anchors[path]=digest
    for row in cold['rows']:
        path=Path(row['array_path']);digest=sha(path)
        if digest!=row['array_sha256']:raise RuntimeError('Cold state array changed: '+str(path))
        anchors[str(path)]=digest
    return cold,anchors
def frozen():return dict(temperatures=list(TEMPERATURES),kB=1.,Ud=1.,
    ensemble='canonical separately fixed Nc; held records and supported graph',
    high_T_arithmetic_probe_beta=PROBE_BETA,high_T_probe_is_not_grid_row=True,
    high_T_tolerance='10 beta spectral_span max(1,coefficient_scale)+1e-10',
    Simpson_intervals=4096,Simpson_cutoff=40.,Simpson_absolute_tolerance=2e-9,
    source='same complete12node operational affine lapse',
    BLAS_threads=1,peak_RSS_limit_bytes=MAX_RSS,sector_seconds_limit=MAX_SECONDS,
    operator_tolerance=OP_TOL,eigen_tolerance=EIG_TOL,susceptibility_tolerance=CHI_TOL,
    thermodynamic_tolerance=THERMO_TOL,no_eigensolver=True)
def addcheck(checks,name,passed,evidence=None):
    c=dict(name=name,passed=bool(passed))
    if evidence is not None:c['evidence']=evidence
    checks.append(c)
def minimum2(np,a):
    return float((a[0,0]+a[1,1]-np.hypot(a[0,0]-a[1,1],a[0,1]+a[1,0]))/2)
def cov_basis(np,A,B):
    dim=A[0].shape[0]
    ma=np.array([np.trace(a)/dim for a in A]);mb=np.array([np.trace(b)/dim for b in B])
    return np.array([[np.sum(a*b)/dim-ma[i]*mb[j] for j,b in enumerate(B)] for i,a in enumerate(A)])

def reconstruct(np,case):
    # Literal new assembly from frozen primitive coefficients, not an old import.
    pm=np.array([p for p in range(64) if p.bit_count()==case['Nc']],dtype=np.int64)
    nb=np.array([[(n>>e)&1 for e in range(6)] for n in range(64)],dtype=float)
    pb=np.array([[(int(p)>>v)&1 for v in range(6)] for p in pm],dtype=float)
    m=len(pm);dim=64*m;rows=np.arange(dim);ns=rows//m;ps=rows%m
    pos=np.array([(np.cos(2*np.pi*v/6),np.sin(2*np.pi*v/6)) for v in range(6)])
    lr,lj,q=case['lambda_R'],case['lambda_J'],case['q']
    H=np.zeros((dim,dim));Gx=np.zeros_like(H);Gy=np.zeros_like(H)
    diagonal=np.zeros(dim);gx=np.zeros(dim);gy=np.zeros(dim);car=np.zeros((dim,2))
    for v in range(6):
        d=1+nb[ns,(v-1)%6]+nb[ns,v]
        onsite=UD*(d-2)**2+q*ER+EP*pb[ps,v]
        exterior=DELTA+lj*pb[ps,v]-lr*q
        diagonal+=onsite+UD+exterior
        owned=onsite+2*UD+1.5*exterior
        gx+=pos[v,0]*owned;gy+=pos[v,1]*owned
        car+=EP*pb[ps,v,None]*pos[v]
    index={int(p):j for j,p in enumerate(pm)}
    for e in range(6):
        u,v=e,(e+1)%6;w=(pos[u]+pos[v])/2
        a=pb[ps,u]+pb[ps,v]-2*pb[ps,u]*pb[ps,v]
        edge=nb[ns,e]*(DELTA+lj*a-2*lr*q)
        diagonal+=edge;gx+=w[0]*edge;gy+=w[1]*edge
        target=(ns^(1<<e))*m+ps
        H[rows,target]+=-HFLIP;Gx[rows,target]+=-HFLIP*w[0];Gy[rows,target]+=-HFLIP*w[1]
        use=(nb[ns,e]==1)&(a==1);src=rows[use]
        swapped=pm[ps[use]]^((1<<u)|(1<<v))
        dst=ns[use]*m+np.array([index[int(p)] for p in swapped],dtype=np.int64)
        H[src,dst]+=-THOP;Gx[src,dst]+=-THOP*w[0];Gy[src,dst]+=-THOP*w[1]
    H[rows,rows]=diagonal;Gx[rows,rows]=gx;Gy[rows,rows]=gy
    return H,[Gx,Gy],car,pm,nb,pb,ns,ps

def prepare(np,row,anchors):
    checks=[];case=row['case'];H,F,car,pm,nb,pb,ns,ps=reconstruct(np,case)
    matrices={'H':matrix_sha(np,H),'Gx':matrix_sha(np,F[0]),'Gy':matrix_sha(np,F[1])}
    addcheck(checks,'reconstructed_cold_matrix_hashes',matrices==row['matrix_sha256'])
    with np.load(row['array_path'],allow_pickle=False) as old:
        if json.loads(str(old['case_json']))!=case:raise RuntimeError('Cold case metadata mismatch')
        if json.loads(str(old['matrix_sha256_json']))!=matrices:raise RuntimeError('Cold matrix metadata mismatch')
        E=old['complete_eigenvalues'];V=old['eigenvectors_columns']
        if not np.array_equal(old['carrier_masks'],pm):raise RuntimeError('Cold carrier basis mismatch')
    dim=len(E);scale=max(1.,float(np.max(np.sum(np.abs(H),axis=1))))
    gscale=max(1.,*(float(np.max(np.sum(np.abs(g),axis=1))) for g in F))
    residual=0.
    for first in range(0,dim,128):
        last=min(first+128,dim)
        residual=max(residual,float(np.max(np.abs(H@V[:,first:last]-V[:,first:last]*E[first:last]))))
    addcheck(checks,'sealed_full_eigen_residual',residual<=EIG_TOL*scale,dict(maximum=residual,tolerance=EIG_TOL*scale))
    addcheck(checks,'resolved_unique_cold_ground',E[1]-E[0]>1e-10*scale)
    C=[np.diag(car[:,i]) for i in range(2)]
    R=[F[i]-C[i] for i in range(2)]
    basis=dict(full=cov_basis(np,F,F),carrier=cov_basis(np,C,C),rest=cov_basis(np,R,R),
               cross=cov_basis(np,C,R)+cov_basis(np,R,C))
    transformed={}
    for name,group in [('full',F),('carrier',C),('rest',R)]:
        transformed[name]=[V.T@(g@V) for g in group]
        for i,g in enumerate(transformed[name]):
            addcheck(checks,'eigenbasis_'+name+'_hermitian_'+str(i),np.max(np.abs(g-g.T))<=EIG_TOL*gscale)
    eigenbasis=dict(full=cov_basis(np,transformed['full'],transformed['full']),
        carrier=cov_basis(np,transformed['carrier'],transformed['carrier']),
        rest=cov_basis(np,transformed['rest'],transformed['rest']),
        cross=cov_basis(np,transformed['carrier'],transformed['rest'])+cov_basis(np,transformed['rest'],transformed['carrier']))
    for key in basis:
        error=float(np.max(np.abs(basis[key]-eigenbasis[key])))
        addcheck(checks,'high_T_trace_basis_custody_'+key,error<=2e-9*max(1.,float(np.max(np.abs(basis[key])))),dict(maximum=error))
    V2=V*V
    obs=[];obs_names=[]
    for v in range(6):
        for label,diag in [('incidence',nb[ns,v]),('carrier',pb[ps,v]),
            ('current_square',pb[ps,v]+pb[ps,(v+1)%6]-2*pb[ps,v]*pb[ps,(v+1)%6])]:
            obs.append(diag@V2);obs_names.append(label+'_'+str(v))
    if case['Nc']==3:
        for label,masks in [('contiguous_three_probability',(7,14,28,56,49,35)),('alternating_probability',(21,42))]:
            obs.append(np.isin(pm[ps],masks).astype(float)@V2);obs_names.append(label)
    metadata=dict(input_sha256=anchors,case=case,cold_array_sha256=row['array_sha256'],
                  cold_matrix_sha256=matrices,preparation_checks=checks,
                  primitive_high_T_coefficients={k:v.tolist() for k,v in basis.items()},
                  source_scale=gscale,H_infinity_scale=scale)
    arrays=dict(complete_eigenvalues=E,observable_eigen_diagonals=np.array(obs),
                observable_names_json=json.dumps(obs_names),metadata_json=json.dumps(metadata,sort_keys=True))
    for name,group in transformed.items():
        for i,g in enumerate(group):arrays[name+str(i)]=g
    return arrays,metadata

def source_groups(archive):
    return {name:[archive[name+'0'],archive[name+'1']] for name in ('full','carrier','rest')}
def means(np,group,p):return np.array([np.dot(p,np.diag(g)) for g in group])
def bilinear(np,A,B,p,W,beta):
    ma,mb=means(np,A,p),means(np,B,p)
    return np.array([[np.einsum('ab,ab,ab->',W,a,b,optimize=False)-beta*ma[i]*mb[j]
                     for j,b in enumerate(B)] for i,a in enumerate(A)])
def cold_bilinear(np,A,B,gaps):
    a=np.column_stack([g[1:,0] for g in A]);b=np.column_stack([g[1:,0] for g in B])
    return 2*a.T@(b/gaps[:,None])
def primitive_variance(np,A,p):
    avg=means(np,A,p)
    return np.array([[np.dot(p,np.sum(a*b,axis=1))-avg[i]*avg[j]
                     for j,b in enumerate(A)] for i,a in enumerate(A)])
def simpson_f(np,x):
    if x==0:return 1.
    limit=min(x,40.);u=np.linspace(0.,limit,4097);y=np.exp(-u)
    integral=(limit/4096)/3*(y[0]+y[-1]+4*np.sum(y[1:-1:2])+2*np.sum(y[2:-1:2]))
    return float(integral/x)

def compute(np,T,E,groups,obs,obs_names,row,metadata,probe=False):
    checks=[];dim=len(E);eps=E-E[0];gscale=metadata['source_scale']
    if T==0:
        p=np.zeros(dim);p[0]=1.;gaps=eps[1:]
        values={name:cold_bilinear(np,group,group,gaps) for name,group in groups.items()}
        values['cross']=cold_bilinear(np,groups['carrier'],groups['rest'],gaps)+cold_bilinear(np,groups['rest'],groups['carrier'],gaps)
        for key,field in [('full','chi_full'),('carrier','chi_carrier'),('rest','chi_rest'),('cross','chi_cross_signed')]:
            difference=float(np.max(np.abs(values[key]-np.array(row[field]))))
            addcheck(checks,'sealed_cold_chi_'+key,difference<=CHI_TOL*max(1.,float(np.max(np.abs(values[key])))),dict(maximum=difference))
        for name,field in [('full','all_excited_source_transition_vectors'),('carrier','all_excited_carrier_source_transition_vectors'),('rest','all_excited_rest_source_transition_vectors')]:
            actual=np.column_stack([g[1:,0] for g in groups[name]])
            addcheck(checks,'sealed_cold_transitions_'+name,np.max(np.abs(actual-np.array(row[field])))<=EIG_TOL*gscale)
        thermo=dict(F=float(E[0]),E=float(E[0]),S=0.,Cv=0.,uniform_lapse_response=0.,energy_variance=0.)
        weight_controls=None;variance_bounds=None
    else:
        beta=1/T;raw=np.exp(-beta*eps);Z=float(raw.sum());p=raw/Z;logZ=np.log(Z)
        mean=float(p@eps);variance=float(p@((eps-mean)**2))
        entropy=float(logZ+beta*mean);cv=beta**2*variance
        thermo=dict(F=float(E[0]-T*logZ),E=float(E[0]+mean),S=entropy,Cv=float(cv),
                    uniform_lapse_response=float(beta*variance),energy_variance=variance)
        addcheck(checks,'normalized_probability',abs(float(p.sum())-1)<=THERMO_TOL)
        nonzero=p>0;shannon=float(-np.dot(p[nonzero],np.log(p[nonzero])))
        addcheck(checks,'entropy_Shannon',abs(entropy-shannon)<=THERMO_TOL*max(1.,abs(entropy)))
        addcheck(checks,'F_equals_E_minus_TS',abs(thermo['F']-(thermo['E']-T*entropy))<=THERMO_TOL*max(1.,abs(thermo['E'])))
        addcheck(checks,'uniform_lapse_TC_v',abs(thermo['uniform_lapse_response']-T*cv)<=THERMO_TOL*max(1.,abs(T*cv)))
        uniform_direct=beta*float(p@(eps**2))-beta*mean**2
        addcheck(checks,'uniform_lapse_diagonal_Kubo',abs(uniform_direct-beta*variance)<=THERMO_TOL*max(1.,abs(beta*variance)))
        x=np.abs(eps[:,None]-eps[None,:])/T
        W=np.ones_like(x)
        np.divide(-np.expm1(-x),x,out=W,where=x!=0)
        W*=beta;W*=np.maximum(p[:,None],p[None,:])
        tolerance=1e-11*max(1.,beta*float(p.max()))
        lower=beta*np.sqrt(p[:,None]*p[None,:]);upper=beta*(p[:,None]+p[None,:])/2
        addcheck(checks,'Duhamel_logmean_lower',float(np.max(lower-W))<=tolerance)
        addcheck(checks,'Duhamel_logmean_upper',float(np.max(W-upper))<=tolerance)
        addcheck(checks,'logmean_symmetric',np.max(np.abs(W-W.T))<=tolerance)
        addcheck(checks,'exact_degenerate_diagonal',np.max(np.abs(np.diag(W)-beta*p))<=tolerance)
        sample_pairs=[(0,1),(0,2),(0,dim-1),(1,2),(dim//2,min(dim//2+1,dim-1)),(dim-2,dim-1)]
        samples=[]
        for a,b in sample_pairs:
            xx=float(x[a,b]);direct=1. if xx==0 else float(-np.expm1(-xx)/xx)
            integral=simpson_f(np,xx);error=abs(direct-integral)
            samples.append(dict(a=a,b=b,x=xx,divided_difference_f=direct,Duhamel_integral_f=integral,error=error))
            addcheck(checks,'Duhamel_quadrature_'+str(a)+'_'+str(b),error<=2e-9)
        values={name:bilinear(np,group,group,p,W,beta) for name,group in groups.items()}
        values['cross']=bilinear(np,groups['carrier'],groups['rest'],p,W,beta)+bilinear(np,groups['rest'],groups['carrier'],p,W,beta)
        variance_bounds={}
        for name,group in groups.items():
            cov=primitive_variance(np,group,p);difference=beta*cov-values[name]
            scale=max(1.,float(np.max(np.abs(beta*cov))),float(np.max(np.abs(values[name]))))
            addcheck(checks,'Kubo_variance_matrix_bound_'+name,minimum2(np,difference)>=-CHI_TOL*scale,
                     dict(minimum=minimum2(np,difference),tolerance=CHI_TOL*scale))
            variance_bounds[name]=dict(covariance=cov.tolist(),beta_covariance=(beta*cov).tolist(),
                                      bound_difference=difference.tolist())
        weight_controls=dict(Simpson_samples=samples,logmean_tolerance=tolerance)
        if probe:
            span=float(eps[-1]);addcheck(checks,'high_T_small_beta_span',beta*span<1e-3)
            for key,value in values.items():
                target=np.array(metadata['primitive_high_T_coefficients'][key])
                error=float(np.max(np.abs(value/beta-target)))
                tol=10*beta*span*max(1.,float(np.max(np.abs(target))))+1e-10
                addcheck(checks,'high_T_analytic_coefficient_'+key,error<=tol,dict(maximum=error,tolerance=tol))
        del x,W,lower,upper
    scale=max(1.,float(np.max(np.abs(values['full']))))
    addcheck(checks,'full_carrier_rest_cross',np.max(np.abs(values['full']-values['carrier']-values['rest']-values['cross']))<=CHI_TOL*scale)
    for name in ('full','carrier','rest'):
        addcheck(checks,'chi_'+name+'_PSD',minimum2(np,values[name])>=-CHI_TOL*max(1.,float(np.max(np.abs(values[name])))))
    full=values['full']
    addcheck(checks,'full_C6_isotropy',abs(full[0,0]-full[1,1])<=CHI_TOL*scale and abs(full[0,1])<=CHI_TOL*scale)
    avg={name:means(np,group,p).tolist() for name,group in groups.items()}
    addcheck(checks,'thermal_full_source_mean_null',max(map(abs,avg['full']))<=2e-8*gscale)
    cold_trace=float(row['chi_full'][0][0]+row['chi_full'][1][1])
    return dict(T=T,arithmetic_high_T_probe=probe,thermodynamics=thermo,
                chi_full_over_sealed_cold_trace=(float(np.trace(values['full']))/cold_trace
                    if cold_trace!=0 else None),
                ground_probability=float(p[0]),excited_probability=float(p[1:].sum()),
                first_excited_probability=float(p[1]),source_means=avg,
                chi={name:val.tolist() for name,val in values.items()},
                chi_traces={name:float(np.trace(val)) for name,val in values.items()},
                thermal_observables={name:float(value@p) for name,value in zip(obs_names,obs)},
                Kubo_variance_bounds=variance_bounds,Duhamel_controls=weight_controls,
                checks=checks,passed_count=sum(c['passed'] for c in checks),
                failed_count=sum(not c['passed'] for c in checks))

def load_operators(np,path,anchors,row):
    with np.load(path,allow_pickle=False) as data:
        metadata=json.loads(str(data['metadata_json']))
        if metadata['input_sha256']!=anchors or metadata['case']!=row['case'] \
            or metadata['cold_array_sha256']!=row['array_sha256'] \
            or metadata['cold_matrix_sha256']!=row['matrix_sha256']:
            raise RuntimeError('Operator array input custody mismatch')
        arrays={name:data[name] for name in data.files}
    E=arrays['complete_eigenvalues'];groups=source_groups(arrays)
    if any(g.shape!=(len(E),len(E)) or not np.all(np.isfinite(g)) for gs in groups.values() for g in gs):
        raise RuntimeError('Incomplete/foreign operator array')
    # Cold response is an independent recovery check even for an orphan NPZ.
    coldcheck=compute(np,0.,E,groups,arrays['observable_eigen_diagonals'],
                      json.loads(str(arrays['observable_names_json'])),row,metadata)
    if coldcheck['failed_count']:raise RuntimeError('Operator checkpoint fails sealed cold response')
    return arrays,metadata

def finish(receipt):
    checks=receipt['checks'][:]
    for s in receipt['sectors']:
        checks+=s['preparation_checks']+s['checks']
        for c in s['cells']+[s['high_T_control']]:checks+=c['checks']
    receipt['check_count']=len(checks);receipt['passed_count']=sum(c['passed'] for c in checks)
    receipt['failed_count']=len(checks)-receipt['passed_count'];receipt['completed_utc']=utc()
    payload=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with DEST.open('xb') as f:f.write(payload)
    digest=hashlib.sha256(payload).hexdigest()
    lines=['# BS11 dynamic-carrier thermal V001: saved result','',
        f"Status: {receipt['status']}; checks {receipt['passed_count']}/{receipt['check_count']}; failures {receipt['failed_count']}.",'',receipt['qualification'],'',
        '| Sector | T | ground probability | chi full | carrier | rest | signed cross | Cv | uniform lapse |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for s in receipt['sectors']:
        for c in s['cells']:
            v=c['chi_traces'];t=c['thermodynamics']
            lines.append(f"| {s['case']['name']} | {c['T']:.6g} | {c['ground_probability']:.9g} | {v['full']:.12g} | {v['carrier']:.12g} | {v['rest']:.12g} | {v['cross']:.12g} | {t['Cv']:.9g} | {t['uniform_lapse_response']:.9g} |")
    lines+=['','Full F/E/S/Cv, source means, all pair thermal Kubo response, signed cross terms, Duhamel controls and high-temperature arithmetic controls are saved in JSON. The beta1e-6 probe is a separate arithmetic control, not a grid row.','',
        'A fixed-temperature canonical preparation is assumed separately in each conserved carrier sector. Records remain held, support imposed and the lapse source operational. Thermal response includes all state pairs. No physical temperature conversion, photon-origin, volume work or physical gravity is established.','',
        f"Runtime {receipt['runtime_seconds']:.6g}s; peak RSS {receipt['peak_RSS_bytes']} bytes; PID {receipt['pid']}.",'',
        f'Result JSON SHA256: {digest}','',f"Exact unfinished sector/cell: {receipt.get('next_unfinished')}",'','Input SHA256 custody:']
    lines+=['- '+p+': '+h for p,h in receipt['input_sha256'].items()]
    with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(status=receipt['status'],sectors=len(receipt['sectors']),
        grid_cells=sum(len(s['cells']) for s in receipt['sectors']),checks=receipt['check_count'],
        passed=receipt['passed_count'],failed=receipt['failed_count'],runtime_seconds=receipt['runtime_seconds'],
        peak_RSS_bytes=receipt['peak_RSS_bytes'],json_sha256=digest,json_path=str(DEST),
        markdown_path=str(REPORT),next_unfinished=receipt.get('next_unfinished'),exception=receipt.get('exception')),indent=2))

def execute(resume):
    if sys.platform!='darwin':raise RuntimeError('This worker is restricted to this Mac')
    if Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Unexpected source path')
    if DEST.exists() or REPORT.exists():raise FileExistsError('Final receipt exists; no overwrite/replay')
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
    cold,anchors=identity_inputs();inputs=frozen();previous=[]
    if cold['status']!='QUALIFIED_ARITHMETIC' or len(cold['rows'])!=7:raise RuntimeError('Cold receipt is not qualified/seven-sector')
    cold_dir=Path(cold['rows'][0]['array_path']).parent
    cold_events=[json.loads(x) for x in (cold_dir/'events.jsonl').read_text().splitlines()]
    for row in cold['rows']:
        commits=[e for e in cold_events if e['event']=='row_complete' and e['case']==row['case']['name']]
        if not commits or commits[-1]['row_sha256']!=sha(cold_dir/(row['case']['name']+'.json')):raise RuntimeError('Cold journal commit mismatch')
    mp=CP/'manifest.json'
    if resume:
        manifest=json.loads(mp.read_text());previous=[json.loads(x) for x in (CP/'events.jsonl').read_text().splitlines()]
        if manifest['input_sha256']!=anchors or manifest['inputs']!=inputs or manifest['host']!=socket.gethostname():raise RuntimeError('Interrupted manifest mismatch')
        starts=[e for e in previous if e['event']=='run_start'];pid=starts[-1]['pid'] if starts else manifest['pid']
        try:os.kill(pid,0)
        except ProcessLookupError:pass
        else:raise RuntimeError('Latest worker PID still exists; ownership uncertain')
    else:
        CP.mkdir();exclusive(mp,dict(input_sha256=anchors,inputs=inputs,host=socket.gethostname(),pid=os.getpid(),created_utc=utc()))
    began=time.perf_counter();receipt=dict(status='RUNNING',started_utc=utc(),pid=os.getpid(),host=socket.gethostname(),
        input_sha256=anchors,inputs=inputs,sectors=[],checks=[],resume=resume,
        qualification='Fixed-Nc canonical equilibrium of supported BS09/BS11 states with held records and complete operational nodal source; no physical temperature conversion, photon origin, gravity, pressure, cosmic preparation or fit.')
    event('run_start',resume=resume)
    def authenticated(path,kind,key):
        commits=[e for e in previous if e['event']==kind and e['key']==key]
        return bool(commits and commits[-1]['sha256']==sha(path))
    try:
        import numpy as np
        for row in cold['rows']:
            case=row['case'];name=case['name'];receipt['next_unfinished']=dict(sector=name,cell='operators')
            sectorpath=CP/(name+'.json');op=CP/(name+'.operators.npz');started=CP/(name+'.started.json')
            if sectorpath.exists():
                if not authenticated(sectorpath,'sector_complete',name):raise RuntimeError('Sector journal authentication failed')
                sector=json.loads(sectorpath.read_text())
                if sector['input_sha256']!=anchors or sector['operator_sha256']!=sha(op):raise RuntimeError('Sector input/operator hash mismatch')
                receipt['sectors'].append(sector)
                if sector['failed_count']:raise RuntimeError('Preserved failed sector forbids retry')
                continue
            if started.exists() and not op.exists():raise RuntimeError('Begun sector lacks operator checkpoint; parent decision needed')
            if not started.exists():exclusive(started,dict(input_sha256=anchors,case=case,pid=os.getpid(),utc=utc()))
            sbegan=time.perf_counter()
            if op.exists():
                commits=[e for e in previous if e['event']=='operators_saved' and e['key']==name]
                if commits and commits[-1]['sha256']!=sha(op):raise RuntimeError('Operator checkpoint journal mismatch')
                arrays,metadata=load_operators(np,op,anchors,row)
            else:
                arrays,metadata=prepare(np,row,anchors)
                with op.open('xb') as f:
                    np.savez(f,**arrays);f.flush();os.fsync(f.fileno())
                event('operators_saved',key=name,sha256=sha(op))
            E=arrays['complete_eigenvalues'];groups=source_groups(arrays)
            obs=arrays['observable_eigen_diagonals'];obs_names=json.loads(str(arrays['observable_names_json']))
            sector=dict(case=case,input_sha256=anchors,operator_path=str(op),operator_sha256=sha(op),
                        preparation_checks=metadata['preparation_checks'],checks=[],cells=[])
            for index,T in enumerate(TEMPERATURES+(1/PROBE_BETA,)):
                probe=index==len(TEMPERATURES);label='high_T_control' if probe else 'T'+str(index)
                key=name+'_'+label;cellpath=CP/(key+'.json');receipt['next_unfinished']=dict(sector=name,cell=label)
                if cellpath.exists():
                    if not authenticated(cellpath,'cell_complete',key):raise RuntimeError('Cell journal authentication failed')
                    cell=json.loads(cellpath.read_text())
                    if cell['input_sha256']!=anchors or cell['operator_sha256']!=sector['operator_sha256']:raise RuntimeError('Cell source custody failed')
                else:
                    event('cell_start',key=key,T=T,probe=probe)
                    cell=compute(np,T,E,groups,obs,obs_names,row,metadata,probe)
                    cell.update(input_sha256=anchors,operator_sha256=sector['operator_sha256'])
                    exclusive(cellpath,cell);event('cell_complete',key=key,sha256=sha(cellpath),failed=cell['failed_count'])
                if probe:sector['high_T_control']=cell
                else:sector['cells'].append(cell)
            seconds=time.perf_counter()-sbegan;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            addcheck(sector['checks'],'sector_under_60seconds',seconds<MAX_SECONDS,dict(seconds=seconds,limit=MAX_SECONDS))
            addcheck(sector['checks'],'peak_under_512MiB',peak<MAX_RSS,dict(peak_bytes=peak,limit_bytes=MAX_RSS))
            sector['elapsed_seconds']=seconds;sector['peak_RSS_bytes']=peak
            sector['failed_count']=sum(not c['passed'] for c in sector['preparation_checks']+sector['checks'])+sum(c['failed_count'] for c in sector['cells']+[sector['high_T_control']])
            exclusive(sectorpath,sector);event('sector_complete',key=name,sha256=sha(sectorpath),failed=sector['failed_count'])
            receipt['sectors'].append(sector)
            print(json.dumps(dict(event='sector_complete',sector=name,failed=sector['failed_count'],seconds=seconds,peak_RSS_bytes=peak)),flush=True)
            del arrays,groups,E,obs;gc.collect()
            if sector['failed_count']:break
        _,endanchors=identity_inputs();addcheck(receipt['checks'],'all_input_bytes_unchanged',endanchors==anchors)
        addcheck(receipt['checks'],'all_seven_sectors_56_grid_cells',len(receipt['sectors'])==7 and sum(len(s['cells']) for s in receipt['sectors'])==56)
        names={s['case']['name'] for s in receipt['sectors']}
        receipt['next_unfinished']=next((dict(sector=r['case']['name'],cell='operators') for r in cold['rows'] if r['case']['name'] not in names),None)
        failed=any(not c['passed'] for c in receipt['checks']) or any(s['failed_count'] for s in receipt['sectors'])
        receipt['status']='FAILED' if failed else 'QUALIFIED_ARITHMETIC'
    except Exception:
        receipt['status']='ERROR';receipt['exception']=traceback.format_exc();event('error',exception=receipt['exception'],next_unfinished=receipt.get('next_unfinished'))
    receipt['runtime_seconds']=time.perf_counter()-began;receipt['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    event('run_complete',status=receipt['status']);finish(receipt)
    return 0 if receipt['status']=='QUALIFIED_ARITHMETIC' else 1

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true');parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    if args.resume and not args.execute:parser.error('--resume requires --execute and separate ownership approval')
    if args.execute:return execute(args.resume)
    _,anchors=identity_inputs();print(json.dumps(dict(mode='describe_only',inputs=frozen(),input_sha256=anchors),indent=2));return 0
if __name__=='__main__':sys.exit(main())
