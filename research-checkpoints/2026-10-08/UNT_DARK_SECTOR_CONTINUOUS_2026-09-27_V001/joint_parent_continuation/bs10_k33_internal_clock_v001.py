#!/usr/bin/env python3
"""Saved-vector internal absolute dial-phase readout; no propagation/solver."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import gc,hashlib,importlib.util,json,math,os,resource,socket,sys,time,traceback
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=J/'BS10_K33_INTERNAL_CLOCK_V001.md';SOURCE=J/'bs10_k33_internal_clock_v001.py'
RESULT=J/'BS10_K33_INTERNAL_CLOCK_V001_RESULT.json';REPORT=J/'BS10_K33_INTERNAL_CLOCK_V001_RESULT.md'
CP=J/'bs10_k33_internal_clock_v001_checkpoints'
NRESULT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json';NCP=J/'bs10_k33_nodal_signal_v001_checkpoints'
OLD_SOURCE=J/'bs10_k33_unclamped_formation_v001.py'
ANCHORS={
 'BS10_K33_NODAL_SIGNAL_V001_RESULT.json':'7a4fc007d3ca9a46482091f4e6ab54a78c866dd4eabaeb19fc4d83b766c2499c',
 'BS10_K33_NODAL_SIGNAL_V001_RESULT.md':'dbc549f522212fd9cd523a56d6e00304419d100cedc68cc1e07af3865db8a35b',
 'BS10_K33_NODAL_SIGNAL_V001.md':'a8abf2801422b4ae4e450ec4a2819f1d3cbdef9fdc937ec008e61d3c030b340d',
 'bs10_k33_nodal_signal_v001.py':'349828cfdb729fceb2593bd7084e348226206f4781c1af71aaeb137a76bfbbf9',
 'NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md':'07a321e8962070d1dbb48540c7674dba60c36b7b85c18f08776954b25262bbdc',
 'NATIVE_CARRIER_CONTROLLED_CLOCK_V001.md':'55e7514ecdc636bc2817d78d44ca5a50422f8be2002877e96c92fca04636108b',
 'NATIVE_PHASE_CLOCK_PROTOCOL_V001.md':'bb6ef50c0f7ba0d3271f9e07f5ba45ce973b24afdb5e2404460e628296404d48'}
GS=(0.,.1);STARTS=(0,413);AGES=(0.,5.,20.,50.);DELAYS=(0.,.1,.5,1.,2.,5.)
ALPHA=1e-5;AMP_FLOOR=.01;RATE_FLOOR=.001;ERROR_FACTOR=100.;FLOAT_VECTOR=2e-9
ENV_KEYS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','PYTHONDONTWRITEBYTECODE')

def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def canonical(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def exclusive(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def event(kind,**kw):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(event=kind,pid=os.getpid(),utc=utc(),**kw),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def rss():return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def cnum(z):return [float(complex(z).real),float(complex(z).imag)]
def check(c,name,ok,e=None):c.append(dict(name=name,passed=bool(ok),**({} if e is None else {'evidence':e})))
def close(np,c,name,x,y,tol=3e-8):
    err=float(np.max(np.abs(np.asarray(x)-np.asarray(y))));lim=tol*max(1.,float(np.max(np.abs(x))),float(np.max(np.abs(y))))
    check(c,name,err<=lim,dict(error=err,tolerance=lim))

def authenticate():
    hashes={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)}
    for name,h in ANCHORS.items():
        p=J/name
        if sha(p)!=h:raise RuntimeError('Frozen anchor changed: '+name)
        hashes[str(p)]=h
    receipt=json.loads(NRESULT.read_text())
    if receipt['status']!='QUALIFIED_ARITHMETIC' or receipt['failed_count'] or len(receipt['rows'])!=16:raise RuntimeError('Nodal parent unqualified/incomplete')
    unsealed=dict(receipt);claim=unsealed.pop('canonical_payload_sha256')
    if canonical(unsealed)!=claim or claim!='0da65bdca466d621561b04a341d2881906d7586535b33bd07a6d3edba4e62240':raise RuntimeError('Nodal canonical seal mismatch')
    manifest=json.loads((NCP/'manifest.json').read_text());events=[json.loads(x) for x in (NCP/'events.jsonl').read_text().splitlines() if x]
    if manifest!=receipt['manifest']:raise RuntimeError('Nodal manifest/receipt mismatch')
    if not any(x.get('event')=='started' and x.get('manifest_sha256')==sha(NCP/'manifest.json') for x in events):raise RuntimeError('Nodal started seal missing')
    for p,h in manifest['input_sha256'].items():
        if sha(Path(p))!=h:raise RuntimeError('Nodal original input changed: '+p)
        hashes[p]=h
    for p in (NCP/'manifest.json',NCP/'events.jsonl'):hashes[str(p)]=sha(p)
    for gi,g in enumerate(GS):
        p=NCP/f'g{gi}_preflight.json';h=sha(p)
        saved=json.loads(p.read_text())
        if saved['g']!=g or saved['input_sha256']!=manifest['input_sha256'] or any(not z['passed'] for z in saved['checks']):raise RuntimeError('Nodal preflight metadata failed')
        if not any(x.get('event')=='preflight_saved' and x.get('key')==f'g{gi}' and x.get('sha256')==h for x in events):raise RuntimeError('Nodal preflight journal mismatch')
        hashes[str(p)]=h
    census=[]
    for row in receipt['rows']:
        key=f'g{GS.index(row["g"])}_n{row["start"]}_age{int(row["age"])}';rp=NCP/(key+'.json');bp=Path(row['bundle_path'])
        if json.loads(rp.read_text())!=row or row['input_sha256']!=manifest['input_sha256'] or row['failed_count']:raise RuntimeError('Nodal row metadata mismatch')
        if not any(x.get('event')=='row_complete' and x.get('key')==key and x.get('sha256')==sha(rp) and x.get('failed')==0 for x in events):raise RuntimeError('Nodal row journal mismatch')
        if sha(bp)!=row['bundle_sha256'] or not any(x.get('event')=='bundle_saved' and x.get('key')==key and x.get('sha256')==row['bundle_sha256'] for x in events):raise RuntimeError('Nodal vector bundle seal mismatch')
        if tuple(x['delay'] for x in row['response'])!=DELAYS:raise RuntimeError('Nodal delay census mismatch')
        hashes[str(rp)]=sha(rp);hashes[str(bp)]=row['bundle_sha256'];census.append((row['g'],row['start'],row['age']))
    if sorted(census)!=sorted((g,n,t) for g in GS for n in STARTS for t in AGES):raise RuntimeError('Whole preparation census mismatch')
    if not any(x.get('event')=='result_saved' and x.get('sha256')==ANCHORS[NRESULT.name] and x.get('canonical_payload_sha256')==claim for x in events):raise RuntimeError('Nodal result journal mismatch')
    if not any(x.get('event')=='report_saved' and x.get('sha256')==ANCHORS['BS10_K33_NODAL_SIGNAL_V001_RESULT.md'] for x in events):raise RuntimeError('Nodal report journal mismatch')
    return hashes,receipt

def pauli(np,f):
    z=1.-2.*f['q'][:,0];perm=f['rows']^1
    X=lambda v:v[perm]
    Y=lambda v:-1j*z*v[perm]
    Z=lambda v:z*v
    B=lambda v:Z(v)-1j*Y(v)
    return z,perm,X,Y,Z,B

def kicknorms(np,cols):
    return {sign:math.sqrt(float(np.vdot(cols[0]-1j*sign*ALPHA*cols[1]-.5*ALPHA**2*cols[2],cols[0]-1j*sign*ALPHA*cols[1]-.5*ALPHA**2*cols[2]).real)) for sign in (1,-1)}

def readpoint(np,old,f,a,source_bound,row,j,cols,initial_norm,kick_norms,c):
    psi,q,q2=cols;z,perm,X,Y,Z,B=pauli(np,f);hp=old.apply(np,f,psi)
    zp=Z(psi);yp=Y(psi);bp=B(psi);norm=float(np.vdot(psi,psi).real)
    beta=complex(np.vdot(psi,bp));zdot=float(2*np.vdot(-1j*hp,zp).real);ydot=float(2*np.vdot(-1j*hp,yp).real);bdot=complex(zdot,-ydot)
    rz=float(2*np.vdot(zp,q).imag);ry=float(2*np.vdot(yp,q).imag);db=complex(rz,-ry)
    alternate=1j*(np.vdot(q,bp)-np.vdot(psi,B(q)))
    p=f['p'][:,0];degree=f['d'][:,0];comm=2*f['g']*np.vdot(psi,p*yp)+1j*np.vdot(psi,(1.-degree/2)*X(psi)+2*f['g']*p*zp)
    prefix=f't{DELAYS[j]}_';oldpoint=row['response'][j]
    close(np,c,prefix+'raw_norm',norm,row['input_norm'],2e-9)
    close(np,c,prefix+'Z_population',float(np.vdot(psi,zp).real),norm-2*oldpoint['means']['record0'],2e-8)
    close(np,c,prefix+'full_H_beta_dot_commutator',bdot,comm)
    close(np,c,prefix+'complex_source_tangent',db,alternate)
    close(np,c,prefix+'Z_local_source',rz,-2*oldpoint['local_plus_kernel']['record0'],2e-8)
    close(np,c,prefix+'Z_uniform_source',zdot,-2*oldpoint['uniform_H_kernel']['record0'],2e-8)
    close(np,c,prefix+'H_source_off_energy',float(np.vdot(psi,hp).real),oldpoint['means']['H'],2e-8)
    b=float(abs(beta));bd=float(abs(bdot));psi_norm=math.sqrt(norm);qnorm=math.sqrt(float(np.vdot(q,q).real))
    saved_ceiling=row['certified_vector_error_ceilings'][j]['exact_vector_error_ceilings']
    epsi=saved_ceiling['psi']+FLOAT_VECTOR*max(1.,psi_norm);eq=saved_ceiling['h0psi']+FLOAT_VECTOR*max(1.,qnorm)
    L=2*psi_norm*epsi+epsi**2;eb=2*L+1e-10*max(1.,b);ebdot=4*a*L+1e-10*max(1.,bd)
    edb=4*(qnorm*epsi+psi_norm*eq+epsi*eq)+1e-10*max(1.,abs(db))
    nu=kappa=enu=ekappa=None
    if b>eb:
        nu=float((bdot/beta).imag);kappa=float((db/beta).imag)
        enu=ebdot/(b-eb)+bd*eb/(b*(b-eb));ekappa=edb/(b-eb)+abs(db)*eb/(b*(b-eb))
    if f['g']==0:
        status='EXACT_ZERO_RATE_G0';close(np,c,prefix+'g0_exact_clock_amplitude',beta,norm);close(np,c,prefix+'g0_exact_zero_clock_rate',bdot,0.);close(np,c,prefix+'g0_exact_zero_clock_source',db,0.)
    elif b<AMP_FLOOR or b<=ERROR_FACTOR*eb:status='AMPLITUDE_UNCONDITIONED'
    elif nu is None or abs(nu)<RATE_FLOOR or abs(nu)<=ERROR_FACTOR*enu:status='RATE_UNCONDITIONED'
    else:status='QUALIFIED_LOCAL_ABSOLUTE_PHASE'
    if row['age']==0 and j==0:
        close(np,c,prefix+'initial_basis_beta',beta,1.);close(np,c,prefix+'initial_basis_beta_dot',bdot,2j*f['g'])
    plusminus={}
    for sign in (1,-1):
        v=(psi-1j*sign*ALPHA*q-.5*ALPHA**2*q2)/kick_norms[sign];plusminus[sign]=complex(np.vdot(v,B(v)))
    fd_beta=(plusminus[1]-plusminus[-1])/(2*ALPHA)
    tail=math.exp(ALPHA*source_bound)*(ALPHA*source_bound)**3/6
    fd_allowance=5e-7*2+2*(2*source_bound)**3*ALPHA**2/6+8*tail/ALPHA
    check(c,prefix+'complex_beta_centered_plus_kick',abs(fd_beta-db/initial_norm)<=fd_allowance,dict(error=float(abs(fd_beta-db/initial_norm)),tolerance=fd_allowance,analytic_Taylor_remainder=tail))
    fixed=uniform_fixed=zero_mean_fixed=clock_fixed=shift=eshift=phase_fd=None;conditioned_error={}
    if status=='QUALIFIED_LOCAL_ABSOLUTE_PHASE':
        shift=-kappa/nu;eshift=ekappa/(abs(nu)-enu)+abs(kappa)*enu/(abs(nu)*(abs(nu)-enu))
        hshift=-float((bdot/beta).imag)/nu
        fixed={};uniform_fixed={};zero_mean_fixed={}
        bounds={**{f'carrier{v}':1. for v in range(6)},**{f'record{v}':1. for v in range(6)},'M':9.,'connected':1.,'H':16.25+a,'h0':source_bound}
        for name in row['observables']:
            raw=oldpoint['local_plus_kernel'][name];odot=oldpoint['uniform_H_kernel'][name];ob=bounds[name]
            fixed[name]=raw+odot*shift;uniform_fixed[name]=odot+odot*hshift
            zero_mean_fixed[name]=(raw-odot/6)+odot*(shift-hshift/6)
            er=2*ob*(qnorm*epsi+psi_norm*eq+epsi*eq)+1e-10*max(1.,abs(raw))
            eod=2*a*ob*L+1e-10*max(1.,abs(odot));allow=3e-8*max(1.,ob,abs(raw),abs(fixed[name]))
            conditioned_error[name]=er+abs(odot)*eshift+abs(shift)*eod+eshift*eod+allow
            check(c,prefix+name+'_uniform_fixed_phase_zero',abs(uniform_fixed[name])<=conditioned_error[name],dict(error=abs(uniform_fixed[name]),tolerance=conditioned_error[name]))
            close(np,c,prefix+name+'_zero_mean_same_fixed_phase',zero_mean_fixed[name],fixed[name])
        clock_fixed=db+bdot*shift;phase_res=float((clock_fixed/beta).imag)
        check(c,prefix+'clock_fixed_phase_zero',abs(phase_res)<=ekappa+abs(shift)*enu+3e-8,dict(error=abs(phase_res),tolerance=ekappa+abs(shift)*enu+3e-8))
        check(c,prefix+'complete_local_work_retained',abs(fixed['H']-row['complete_local_impulse_work_derivative'])<=conditioned_error['H'],dict(error=abs(fixed['H']-row['complete_local_impulse_work_derivative']),tolerance=conditioned_error['H']))
        close(np,c,prefix+'fixed_phase_sumcarrier_zero',sum(fixed[f'carrier{v}'] for v in range(6)),0.)
        phase_angles={sign:math.atan2((v/beta).imag,(v/beta).real) for sign,v in plusminus.items()}
        phase_fd=(phase_angles[1]-phase_angles[-1])/(2*ALPHA)
        bmin=(b-eb)/initial_norm-4*source_bound*ALPHA
        if bmin<=0:raise ArithmeticError('Prospective phase-kick lower amplitude bound nonpositive')
        theta3=16*source_bound**3/bmin+3*(8*source_bound**2)*(4*source_bound)/bmin**2+2*(4*source_bound)**3/bmin**3
        phase_trunc=theta3*ALPHA**2/6
        phase_chord_error=8*tail/(1-tail)+8*tail**2/(1-tail)**2
        if bmin<=phase_chord_error:raise ArithmeticError('Taylor-kick angular bound denominator nonpositive')
        approximate_phase=phase_chord_error/(ALPHA*(bmin-phase_chord_error))
        phase_allow=fd_allowance/((b-eb)/initial_norm)+ekappa+phase_trunc+approximate_phase
        check(c,prefix+'nonlinear_phase_centered_plus_kick',abs(phase_fd-kappa)<=phase_allow,dict(error=abs(phase_fd-kappa),tolerance=phase_allow,plus_angle=phase_angles[1],minus_angle=phase_angles[-1],normalized_amplitude_lower_bound=bmin,nonlinear_third_derivative_bound=theta3,nonlinear_truncation_allowance=phase_trunc,normalized_Taylor_kick_complex_error=phase_chord_error,normalized_Taylor_kick_phase_allowance=approximate_phase))
    return dict(delay=DELAYS[j],comparison_scope='SOURCE_BOUNDARY_TANGENT_ONLY' if j==0 else 'INTERIOR_LOCAL_PHASE_CHART',clock_status=status,raw_norm=norm,beta=cnum(beta),beta_dot=cnum(bdot),source_delta_beta=cnum(db),amplitude=b,nu=nu,kappa=kappa,source_time_shift=shift,corrected_clock_tangent=None if clock_fixed is None else cnum(clock_fixed),fixed_phase_local=fixed,fixed_phase_uniform=uniform_fixed,fixed_phase_zero_mean=zero_mean_fixed,corrected_error_budget=conditioned_error,complete_local_work_derivative=row['complete_local_impulse_work_derivative'],raw_local_kernel=oldpoint['local_plus_kernel'],raw_uniform_kernel=oldpoint['uniform_H_kernel'],raw_means=oldpoint['means'],error_budgets=dict(psi_vector=epsi,h0psi_vector=eq,beta=eb,beta_dot=ebdot,delta_beta=edb,nu=enu,kappa=ekappa,time_shift=eshift,amplitude_to_error=b/eb,rate_to_error=None if enu is None or enu==0 else abs(nu)/enu),kick_control=dict(alpha=ALPHA,initial_fixed_norms={str(k):v for k,v in kick_norms.items()},beta_plus=cnum(plusminus[1]),beta_minus=cnum(plusminus[-1]),centered_delta_beta=cnum(fd_beta),centered_phase_derivative=phase_fd,analytic_Taylor_remainder=tail,complex_derivative_tolerance=fd_allowance))

def runrow(np,old,f,a,g_bound,row,hashes,t0):
    key=f'g{GS.index(row["g"])}_n{row["start"]}_age{int(row["age"])}';checks=[]
    with np.load(row['bundle_path'],allow_pickle=False) as z:
        meta=json.loads(str(z['metadata_json']));cols=z['propagated_main_columns'];initial=z['input_columns'];saved_delays=z['delays']
    if meta['input_sha256']!=row['input_sha256'] or meta['original_bundle_sha256']!=row['original_bundle_sha256'] or meta['input_column_norms']!=row['input_column_norms'] or meta['certified_vector_error_ceilings']!=row['certified_vector_error_ceilings'] or (meta['g'],meta['start'],meta['age'])!=(row['g'],row['start'],row['age']):raise RuntimeError('Saved bundle metadata mismatch')
    if cols.shape!=(6,3,old.DIM) or initial.shape!=(3,old.DIM) or not np.all(np.isfinite(cols)) or not np.all(np.isfinite(initial)) or tuple(saved_delays)!=DELAYS:raise RuntimeError('Saved full vector shape/census/finite mismatch')
    close(np,checks,'delay0_actual_initial_columns',cols[0],initial,2e-9)
    close(np,checks,'saved_all3_input_norms',np.sqrt(np.real(np.diag(initial.conj()@initial.T))),[row['input_column_norms'][x] for x in ('psi','h0psi','h0_squared_psi')],2e-9)
    n0=float(np.vdot(initial[0],initial[0]).real);kn=kicknorms(np,initial)
    points=[readpoint(np,old,f,a,g_bound,row,j,cols[j],n0,kn,checks) for j in range(6)]
    out=dict(g=row['g'],start=row['start'],age=row['age'],input_sha256=hashes,parent_row_bundle_path=row['bundle_path'],parent_row_bundle_sha256=row['bundle_sha256'],points=points,checks=checks,failed_count=sum(not z['passed'] for z in checks),elapsed_seconds=time.monotonic()-t0,peak_RSS_bytes=rss())
    p=CP/(key+'.json');exclusive(p,out);event('row_complete',key=key,path=str(p),sha256=sha(p),failed=out['failed_count']);print(json.dumps(dict(checkpoint=key,failed=out['failed_count'],qualified=sum(x['clock_status']=='QUALIFIED_LOCAL_ABSOLUTE_PHASE' for x in points),elapsed_seconds=out['elapsed_seconds'])),flush=True)
    return out

def execute():
    if sys.platform!='darwin':raise RuntimeError('Same Mac only')
    if any(p.exists() for p in (CP,RESULT,REPORT)):raise RuntimeError('Exclusive outputs exist; no replay/resume authorized')
    if any(os.environ.get(k)!='1' for k in ENV_KEYS):raise RuntimeError('One-thread environment required before NumPy import')
    hashes,parent=authenticate();CP.mkdir();t0=time.monotonic()
    manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),utc=utc(),input_sha256=hashes,environment={k:os.environ[k] for k in ENV_KEYS},inputs=dict(g=GS,starts=STARTS,ages=AGES,delays=DELAYS,B='Z0-iY0',absolute_pre_kick_phase_origin=True,amp_floor=AMP_FLOOR,rate_floor=RATE_FLOOR,error_factor=ERROR_FACTOR,floating_vector_budget=FLOAT_VECTOR,alpha=ALPHA,no_propagation=True,one_row_resident=True))
    exclusive(CP/'manifest.json',manifest);event('started',manifest_sha256=sha(CP/'manifest.json'));print(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),status='started')),flush=True)
    try:
        import numpy as np
        spec=importlib.util.spec_from_file_location('sealed_k33_clock_operator_helpers',OLD_SOURCE);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        rows=[];checks=[]
        for gi,g in enumerate(GS):
            f=old.fields(np,g);a=parent['Hamiltonian_controls'][gi]['halfwidth'];gb=parent['Hamiltonian_controls'][gi]['h0_norm_bound'];z,perm,X,Y,Z,B=pauli(np,f)
            v=np.exp(1j*(np.arange(old.DIM)%257)/257)/math.sqrt(old.DIM);w=np.exp(1j*(np.arange(old.DIM)%193)/193)/math.sqrt(old.DIM)
            close(np,checks,f'g{gi}_Y_square',Y(Y(v)),v);close(np,checks,f'g{gi}_Z_square',Z(Z(v)),v);close(np,checks,f'g{gi}_X_square',X(X(v)),v)
            close(np,checks,f'g{gi}_Y_Hermitian',np.vdot(w,Y(v)),np.vdot(Y(w),v));close(np,checks,f'g{gi}_X_B_commutator',X(B(v))-B(X(v)),2*B(v))
            bv=B(v);h=old.apply(np,f,v);bder=2*f['g']*np.vdot(v,f['p'][:,0]*Y(v))+1j*np.vdot(v,(1-f['d'][:,0]/2)*X(v)+2*f['g']*f['p'][:,0]*Z(v))
            close(np,checks,f'g{gi}_complete_probe_beta_dot',1j*(np.vdot(h,bv)-np.vdot(v,B(h))),bder)
            for row in (r for r in parent['rows'] if r['g']==g):rows.append(runrow(np,old,f,a,gb,row,hashes,t0));gc.collect()
            del f,v,w,bv,h;gc.collect()
        after,_=authenticate();check(checks,'all_input_bytes_unchanged',hashes==after);check(checks,'whole_16_snapshot_96_point_census',len(rows)==16 and sum(len(r['points']) for r in rows)==96)
        combined=checks+[z for r in rows for z in r['checks']];failed=[z for z in combined if not z['passed']];points=[p for r in rows for p in r['points']]
        counts={status:sum(p['clock_status']==status for p in points) for status in sorted({p['clock_status'] for p in points})}
        payload=dict(status='QUALIFIED_ARITHMETIC' if not failed else 'FAILED_ARITHMETIC',qualification='Finite ensemble record0 absolute phase readout and actual source-response comparison only; no continuous clock window, atomic/photon time, geometry, physical lapse, gravity, ruler, cosmology or formation qualification',manifest=manifest,rows=rows,checks=checks,clock_status_counts=counts,passed_count=len(combined)-len(failed),failed_count=len(failed),failed_checks=failed,runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss(),pid=os.getpid())
        payload['canonical_payload_sha256']=canonical(payload);exclusive(RESULT,payload);event('result_saved',sha256=sha(RESULT),canonical_payload_sha256=payload['canonical_payload_sha256'])
        lines=['# K3,3 internal absolute phase-clock V001: sealed result','',f"{payload['status']}; {payload['passed_count']}/{len(combined)} controls,16 snapshots/96 points.",'',payload['qualification'],'',f'Clock conditioning census: {json.dumps(counts,sort_keys=True)}','', '| g | seed | age | qualified points | amplitude range | signed raw rate range |','|---|---:|---:|---:|---|---|']
        for r in rows:
            amp=[p['amplitude'] for p in r['points']];nu=[p['nu'] for p in r['points'] if p['nu'] is not None];lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{sum(p['clock_status']=='QUALIFIED_LOCAL_ABSOLUTE_PHASE' for p in r['points'])}|[{min(amp):.9g},{max(amp):.9g}]|{None if not nu else [min(nu),max(nu)]}|")
        lines+=['','Absolute phase origin is fixed before the source kick; no post-kick phase reset. Every unqualified clock remains in the receipt. Source-off complete pulse work is retained. Uniform H response cancels only at a qualified internal phase readout; this does not calibrate any physical clock or ruler.',f"Runtime {payload['runtime_seconds']:.6f}s; peak RSS {payload['peak_RSS_bytes']}bytes; PID {os.getpid()}.",f'Raw result SHA256: {sha(RESULT)}',f"Canonical payload SHA256: {payload['canonical_payload_sha256']}",f'Protocol SHA256: {hashes[str(PROTOCOL)]}',f'Source SHA256: {hashes[str(SOURCE)]}','Every completed snapshot has exclusive checkpoint JSON and journal seal; original full vectors remain untouched. This single process ends here. No automatic resumption/replay is installed; root integrates existing continuation log/ledger.']
        with REPORT.open('x',encoding='utf-8') as out:out.write('\n'.join(lines)+'\n');out.flush();os.fsync(out.fileno())
        event('report_saved',sha256=sha(REPORT));print(json.dumps(dict(status=payload['status'],passed=payload['passed_count'],failed=payload['failed_count'],clock_status_counts=counts,result_sha256=sha(RESULT),report_sha256=sha(REPORT),runtime_seconds=payload['runtime_seconds'],peak_RSS_bytes=payload['peak_RSS_bytes'])),flush=True)
        return 0 if not failed else 2
    except BaseException as e:
        error=dict(status='INTERRUPTED_OR_FAILED',error=repr(e),traceback=traceback.format_exc(),pid=os.getpid(),runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss());exclusive(CP/'error.json',error);event('error',sha256=sha(CP/'error.json'));print(json.dumps(error),flush=True);return 3

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');args=p.parse_args()
    if args.execute:return execute()
    print('Prospective saved-vector readout source only; final root/readonly preflight and ownership approval required.');return 0
if __name__=='__main__':sys.exit(main())
