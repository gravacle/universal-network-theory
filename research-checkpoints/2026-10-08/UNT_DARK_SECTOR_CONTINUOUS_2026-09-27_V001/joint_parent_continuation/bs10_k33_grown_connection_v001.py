#!/usr/bin/env python3
"""Prospective encoded N4 connection derivatives; no N4 vector/propagation."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import gc, hashlib, importlib.util, json, math, os, resource, socket, sys, time, traceback
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
SOURCE=J/'bs10_k33_grown_connection_v001.py'
PROTOCOL=J/'BS10_K33_GROWN_CONNECTION_V001.md'
RESULT=J/'BS10_K33_GROWN_CONNECTION_V001_RESULT.json'
REPORT=J/'BS10_K33_GROWN_CONNECTION_V001_RESULT.md'
CP=J/'bs10_k33_grown_connection_v001_checkpoints'
PARENT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json'
PCP=J/'bs10_k33_nodal_signal_v001_checkpoints'
OLD_SOURCE=J/'bs10_k33_unclamped_formation_v001.py'
ANCHORS={
 'BS10_K33_NODAL_SIGNAL_V001_RESULT.json':'7a4fc007d3ca9a46482091f4e6ab54a78c866dd4eabaeb19fc4d83b766c2499c',
 'BS10_K33_NODAL_SIGNAL_V001_RESULT.md':'dbc549f522212fd9cd523a56d6e00304419d100cedc68cc1e07af3865db8a35b',
 'BS10_K33_NODAL_SIGNAL_V001.md':'a8abf2801422b4ae4e450ec4a2819f1d3cbdef9fdc937ec008e61d3c030b340d',
 'bs10_k33_nodal_signal_v001.py':'349828cfdb729fceb2593bd7084e348226206f4781c1af71aaeb137a76bfbbf9',
 'NATIVE_UNCLAMPED_CENSUS_CREATION_V001.md':'92d6e1b2b2ce862832a6032cd6c4e891e7bbd1a7e9bb8079e62c3a66251112fb',
 'bs10_k33_census_creation_saved_v001.py':'ca5429b498a274c26765667a2f4f5ab333d998e9d9cb07894c0243b2f77d9948',
 'bs10_k33_unclamped_formation_v001.py':'2a6d6326592dee5fb04ba47776ea495df68c0acdf7dce22f26f4be0eae0a1b6c',
 'BS10_K33_UNCLAMPED_FORMATION_V001.md':'8391edb0b3ac88268605f30d6e9589c05871fd570f48bee18ae845fcaec060c6',
 'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json':'21bf1c0abaf548364665aee7d5e4559f3a0457899fcb25f3f7e35cc52d7c317b'}
CANONICAL_PARENT='0da65bdca466d621561b04a341d2881906d7586535b33bd07a6d3edba4e62240'
GS=(0.,.1);STARTS=(0,413);AGES=(0.,5.,20.,50.);DELAYS=(0.,.1,.5,1.,2.,5.)
ENV=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','PYTHONDONTWRITEBYTECODE')
TAU=.01;ATOL=5e-11;FLOAT_VECTOR=2e-9
CENTER4=21.5;RADIUS4=23.4;SPECTRUM4=(-1.9,44.9)
C1=2.4;C2=112.32;REMAINDER=876.096
TARGET_FLIPS=(0,3,12,15,7,11,13,14)
VIRTUAL=((0,1),(0,2),(3,4),(3,5))

def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):
    p=Path(p).resolve()
    if not p.is_relative_to(ROOT):raise RuntimeError('Input outside sole project root: '+str(p))
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def canonical(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def exclusive(p,v):
    with p.open('x',encoding='utf-8') as f:
        json.dump(v,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def event(name,**kw):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=name,pid=os.getpid(),utc=utc(),**kw),sort_keys=True,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
def rss():return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def check(c,name,ok,e=None):c.append(dict(name=name,passed=bool(ok),**({} if e is None else {'evidence':e})))
def close(np,c,name,x,y,tol=ATOL):
    x=np.asarray(x);y=np.asarray(y)
    err=float(np.max(np.abs(x-y)));limit=tol*max(1.,float(np.max(np.abs(x))),float(np.max(np.abs(y))))
    check(c,name,err<=limit,dict(error=err,tolerance=limit))
def cnum(z):return [float(complex(z).real),float(complex(z).imag)]
def classification(lo,hi):
    return 'POSITIVE' if lo>0. else ('NEGATIVE' if hi<0. else 'INCONCLUSIVE')

def authenticate():
    hashes={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)}
    for name,h in ANCHORS.items():
        p=J/name
        if sha(p)!=h:raise RuntimeError('Frozen anchor changed: '+name)
        hashes[str(p)]=h
    parent=json.loads(PARENT.read_text());base=dict(parent);claim=base.pop('canonical_payload_sha256')
    if claim!=CANONICAL_PARENT or canonical(base)!=claim:raise RuntimeError('Parent canonical seal mismatch')
    if parent['status']!='QUALIFIED_ARITHMETIC' or parent['failed_count'] or parent['passed_count']!=5272 or len(parent['rows'])!=16:raise RuntimeError('Parent qualification/census mismatch')
    if parent['manifest']['host']!=socket.gethostname():raise RuntimeError('Same Mac host mismatch')
    mp=PCP/'manifest.json';ep=PCP/'events.jsonl'
    manifest=json.loads(mp.read_text());events=[json.loads(s) for s in ep.read_text().splitlines() if s]
    if manifest!=parent['manifest']:raise RuntimeError('Parent manifest mismatch')
    if not any(e['event']=='started' and e.get('pid')==manifest['pid'] and e.get('manifest_sha256')==sha(mp) for e in events):raise RuntimeError('Parent started-manifest seal missing')
    for p,h in manifest['input_sha256'].items():
        if sha(p)!=h:raise RuntimeError('Original parent input changed: '+p)
        hashes[p]=h
    hashes[str(mp)]=sha(mp);hashes[str(ep)]=sha(ep)
    for gi,g in enumerate(GS):
        p=PCP/f'g{gi}_preflight.json';saved=json.loads(p.read_text());h=sha(p)
        if saved['g']!=g or saved['input_sha256']!=manifest['input_sha256'] or any(not c['passed'] for c in saved['checks']):raise RuntimeError('Parent preflight metadata/check mismatch')
        if not any(e['event']=='preflight_saved' and e.get('key')==f'g{gi}' and e.get('sha256')==h for e in events):raise RuntimeError('Parent preflight journal missing')
        hashes[str(p)]=h
    census=[]
    for row in parent['rows']:
        key=f'g{GS.index(row["g"])}_n{row["start"]}_age{int(row["age"])}';rp=PCP/(key+'.json');bp=Path(row['bundle_path'])
        if json.loads(rp.read_text())!=row or row['input_sha256']!=manifest['input_sha256'] or row['failed_count']:raise RuntimeError('Parent row metadata/check mismatch: '+key)
        rh=sha(rp);bh=sha(bp)
        if bh!=row['bundle_sha256']:raise RuntimeError('Parent bundle digest mismatch: '+key)
        if not any(e['event']=='row_complete' and e.get('key')==key and e.get('sha256')==rh and e.get('failed')==0 for e in events):raise RuntimeError('Parent row journal missing: '+key)
        if not any(e['event']=='bundle_saved' and e.get('key')==key and e.get('sha256')==bh for e in events):raise RuntimeError('Parent bundle journal missing: '+key)
        if tuple(p['delay'] for p in row['response'])!=DELAYS:raise RuntimeError('Parent delay census mismatch')
        hashes[str(rp)]=rh;hashes[str(bp)]=bh;census.append((row['g'],row['start'],row['age']))
    if sorted(census)!=sorted((g,n,a) for g in GS for n in STARTS for a in AGES):raise RuntimeError('Whole16 preparation census mismatch')
    if not any(e['event']=='result_saved' and e.get('sha256')==ANCHORS[PARENT.name] and e.get('canonical_payload_sha256')==claim for e in events):raise RuntimeError('Parent result journal missing')
    if not any(e['event']=='report_saved' and e.get('sha256')==ANCHORS['BS10_K33_NODAL_SIGNAL_V001_RESULT.md'] for e in events):raise RuntimeError('Parent report journal missing')
    return hashes,parent

def components(mask,N,extra=()):
    adj=[set() for _ in range(2*N)]
    for i in range(N):
        for j in range(N):
            if (mask>>(N*i+j))&1:adj[i].add(N+j);adj[N+j].add(i)
    for u,v in extra:adj[u].add(v);adj[v].add(u)
    unseen=set(range(2*N));count=0
    while unseen:
        stack=[unseen.pop()];count+=1
        while stack:
            for v in adj[stack.pop()]:
                if v in unseen:unseen.remove(v);stack.append(v)
    return count,[len(a) for a in adj]
def image(mask):
    result=0
    for i in range(3):
        for j in range(3):
            f=3*i+j
            if f and (mask>>f)&1:result|=1<<(4*i+j)
    if mask&1:
        for f in (3,12,15):result|=1<<f
    return result

def graph_flags(np):
    checks=[];rows=[];images=[];offimage_sets=[set() for _ in TARGET_FLIPS]
    for n in range(512):
        target=image(n);images.append(target);occ=n&1
        oldc,oldd=components(n,3);newc,newd=components(target,4)
        conn=int(oldc==1);c0=occ*conn;cminus=int(components(n&~1,3)[0]==1)
        virtual=[int(components(n,3,(link,))[0]==1) for link in VIRTUAL]
        actual=[int(components(target^(1<<f),4)[0]==1) for f in TARGET_FLIPS]
        expected=[occ*conn]+[occ*cminus]*3+[occ*c for c in virtual]
        mapped=[newd[v] for v in (0,1,2,4,5,6)]
        check(checks,f'graph{n}_old_new_degrees',mapped==oldd and newd[3]==newd[7]==2*occ,dict(old=oldd,new=newd))
        check(checks,f'graph{n}_image_connection',newc==oldc+2*(1-occ) and int(newc==1)==c0,dict(old_components=oldc,target_components=newc,C0=c0))
        code=[(target>>f)&1 for f in (3,12,15)]
        check(checks,f'graph{n}_image_code',not(target&1) and code==[occ]*3 and all(not((target>>f)&1) for f in (7,11,13,14)),dict(code=code,target_mask=target))
        for j,f in enumerate(TARGET_FLIPS):
            check(checks,f'graph{n}_targetflip{f}_connection',actual[j]==expected[j],dict(actual=actual[j],expected=expected[j]))
            offimage_sets[j].add(target^(1<<f))
        bridge=occ*conn*(1-cminus);healing=occ*(1-conn)*sum(virtual)
        direct=.0225*(sum(actual)-8*c0)
        via_virtual=.0225*occ*(3*cminus+sum(virtual)-7*conn)
        via_signed=-.0675*bridge+.0225*healing
        close(np,checks,f'graph{n}_BminusK_twoforms',direct,via_virtual)
        close(np,checks,f'graph{n}_bridge_healing_decomposition',direct,via_signed)
        rows.append(dict(old_mask=n,target_mask=target,n0=occ,C3=conn,C0=c0,Cminus=cminus,virtual_connected=virtual,target_flip_connected=actual,anchor_bridge=bridge,healing_count=healing,BminusC0K=direct))
    check(checks,'512_images_injective',len(set(images))==512,dict(count=len(set(images))))
    check(checks,'4096_flip_outputs_distinct',len(set().union(*offimage_sets))==4096 and all(len(s)==512 for s in offimage_sets),dict(channel_counts=[len(s) for s in offimage_sets],union_count=len(set().union(*offimage_sets))))
    check(checks,'flip_outputs_outside_image',not(set(images)&set().union(*offimage_sets)))
    payload=dict(target_flip_bits=TARGET_FLIPS,virtual_links=VIRTUAL,rows=rows,checks=checks,failed_count=sum(not c['passed'] for c in checks))
    exclusive(CP/'graph_flags.json',payload);event('graph_flags_saved',sha256=sha(CP/'graph_flags.json'),failed=payload['failed_count'])
    return rows,checks

def D_action(np,v,masks,occupied):
    x=v.reshape(512,6,64);out=8.*(1.-occupied[:,None,None])*x+.2*x[masks^1]
    for f in range(1,9):out+=.05*x[masks^(1<<f)]
    out[1::2,0,:]+=.1*x[1::2,3,:];out[1::2,3,:]+=.1*x[1::2,0,:]
    return out.reshape(-1)
def A_independent(np,f,v):
    out=(f['D']+8.*(1.-(f['ns']&1)))*v
    for idx in f['flips'][1:]:out-=.15*v[idx]
    for idx,active,edge in zip(f['targets'],f['activity'],f['hop_edges']):out-=.1*active*(edge!=0)*v[idx]
    out+=f['g']*v[f['copy']]
    return out

def coefficient_bands(P0,P1,P2,n,eps,allowances):
    a0,a1,a2=allowances;L=2.*math.sqrt(n)*eps+eps*eps
    t=TAU;poly=P0+P1*t+.5*P2*t*t;change=P1*t+.5*P2*t*t
    ae=a0+a1*t+.5*a2*t*t;ad=a1*t+.5*a2*t*t
    rem=REMAINDER*t**3
    raw_error=ae+n*rem;normalized_error=ae/n+rem
    original_error=L*(1.+C1*t+.5*C2*t*t)+ae+rem
    original_change_error=L*(C1*t+.5*C2*t*t)+ad+rem
    raw_change_error=ad+n*rem;normalized_change_error=ad/n+rem
    stored_p1=(P1-a1,P1+a1);original_p1=(P1-(C1*L+a1),P1+(C1*L+a1))
    return dict(interval=[0.,TAU],tau=TAU,vector_budget=eps,quadratic_expectation_vector_error_factor=L,coefficient_arithmetic_allowances=list(allowances),remainder_coefficient=REMAINDER,
      whole_interval_formula=dict(raw='a0+a1*t+a2*t^2/2+876.096*n*t^3',normalized_stored='(a0+a1*t+a2*t^2/2)/n+876.096*t^3',conditional_original_exact='Lerr*(1+2.4*t+56.16*t^2)+a0+a1*t+a2*t^2/2+876.096*t^3',conditional_original_change='Lerr*(2.4*t+56.16*t^2)+a1*t+a2*t^2/2+876.096*t^3'),
      raw_polynomial=poly,raw_ideal_stored_probability_band=[poly-raw_error,poly+raw_error],normalized_stored_polynomial=poly/n,normalized_ideal_stored_probability_band=[poly/n-normalized_error,poly/n+normalized_error],conditional_original_exact_probability_band=[poly-original_error,poly+original_error],
      raw_change_polynomial=change,raw_ideal_stored_change_band=[change-raw_change_error,change+raw_change_error],normalized_stored_change_polynomial=change/n,normalized_ideal_stored_change_band=[change/n-normalized_change_error,change/n+normalized_change_error],conditional_original_exact_change_band=[change-original_change_error,change+original_change_error],
      stored_change_status=classification(change-raw_change_error,change+raw_change_error),conditional_original_change_status=classification(change-original_change_error,change+original_change_error),raw_stored_P1_band=list(stored_p1),conditional_original_P1_band=list(original_p1),stored_P1_status=classification(*stored_p1),conditional_original_P1_status=classification(*original_p1),probability_bounds_clipped=False,floating_budgets_conditional=True,directed_roundoff_certified=False)

def run_row(np,old,f,parent,row,flags,hashes):
    started=time.monotonic();checks=[]
    key=f'g{GS.index(row["g"])}_n{row["start"]}_age{int(row["age"])}'
    with np.load(row['bundle_path'],allow_pickle=False) as z:
        meta=json.loads(str(z['metadata_json']));cols=z['input_columns'];delays=z['delays']
    if cols.shape!=(3,old.DIM) or not np.all(np.isfinite(cols)) or tuple(delays)!=DELAYS:raise RuntimeError('Saved column shape/finite/delay mismatch: '+key)
    if meta['input_sha256']!=row['input_sha256'] or meta['original_bundle_sha256']!=row['original_bundle_sha256'] or meta['input_column_norms']!=row['input_column_norms'] or meta['certified_vector_error_ceilings']!=row['certified_vector_error_ceilings'] or (meta['g'],meta['start'],meta['age'])!=(row['g'],row['start'],row['age']):raise RuntimeError('Saved bundle metadata mismatch: '+key)
    allnorms=[math.sqrt(float(np.vdot(v,v).real)) for v in cols]
    close(np,checks,'all3_input_norm_metadata',allnorms,[row['input_column_norms'][s] for s in ('psi','h0psi','h0_squared_psi')],2e-9)
    psi=cols[0].copy();del cols
    n=float(np.vdot(psi,psi).real)
    if n<=0.:raise ArithmeticError('Nonpositive raw input norm')
    close(np,checks,'raw_input_norm',n,row['input_norm'],2e-9);close(np,checks,'physical_normalized_seed_compatibility',n,1.,2e-9)
    masks=np.arange(512);occupied=(masks&1).astype(float)
    C3=np.array([r['C3'] for r in flags],dtype=float);C0=np.array([r['C0'] for r in flags],dtype=float)
    bm=np.array([r['BminusC0K'] for r in flags]);bridge=np.array([r['anchor_bridge'] for r in flags]);heal=np.array([r['healing_count'] for r in flags])
    cvec=C0[f['ns']];cp=cvec*psi
    # Exactly two sealed native actions on this stored input and its C0 projection.
    hp=old.apply(np,f,psi);dp=D_action(np,psi,masks,occupied);ap=hp+dp
    hcp=old.apply(np,f,cp);dcp=D_action(np,cp,masks,occupied);acp=hcp+dcp
    close(np,checks,'Apsi_independent_compression',ap,A_independent(np,f,psi))
    close(np,checks,'AC0psi_independent_compression',acp,A_independent(np,f,cp))
    close(np,checks,'A_Hermitian_contraction',np.vdot(psi,acp),np.vdot(ap,cp))
    Hmean=np.vdot(psi,hp);close(np,checks,'complete_H_imaginary',Hmean.imag,0.)
    parent_mean=row['response'][0]['means'];close(np,checks,'complete_H_parent',Hmean.real,parent_mean['H'],2e-8)
    V=psi.reshape(512,6,64);density=np.abs(V)**2;graphp=density.sum(axis=(1,2));carrierp=density.sum(axis=(0,2))
    oldconn=float(np.dot(C3,graphp));target=float(np.dot(C0,graphp))
    close(np,checks,'old_connected_parent',oldconn,parent_mean['connected'],2e-8)
    for v in range(6):
        close(np,checks,f'carrier{v}_parent',carrierp[v],parent_mean[f'carrier{v}'],2e-8)
        close(np,checks,f'record{v}_parent',float(np.vdot(psi,f['q'][:,v]*psi).real),parent_mean[f'record{v}'],2e-8)
    p0z=np.vdot(psi,cp);close(np,checks,'P0_imaginary',p0z.imag,0.);P0=float(p0z.real)
    close(np,checks,'P0_probability_sum',P0,target)
    p1inner=np.vdot(cp,ap);P1=2.*float(p1inner.imag)
    p1der=2.*float(np.vdot(-1j*ap,cp).real);close(np,checks,'P1_derivative_form',P1,p1der)
    p1pair=0.
    for bit in range(1,9):
        low=masks[((masks>>bit)&1)==0];high=low^(1<<bit)
        diff=(C0[high]-C0[low])[:,None,None]
        p1pair+=.3*float(np.vdot(diff*V[low],V[high]).imag)
    close(np,checks,'P1_nonanchor_coherence_form',P1,p1pair)
    diagonalterm=2.*float(np.vdot(ap,cvec*ap).real);crossterm=-2.*float(np.vdot(acp,ap).real)
    bmmean=float(np.dot(bm,graphp));bridgeweight=float(np.dot(bridge,graphp));healingweight=float(np.dot(heal,graphp))
    signed_bridge=-.135*bridgeweight;signed_healing=.045*healingweight;leakterm=2.*bmmean
    close(np,checks,'P2_signed_leakage_decomposition',leakterm,signed_bridge+signed_healing)
    P2=diagonalterm+crossterm+leakterm
    p2alt=2.*float(np.vdot(ap,cvec*ap-acp).real)+leakterm
    close(np,checks,'P2_vector_contraction_form',P2,p2alt)
    operatorbound=dict(P0=n,P1=C1*n,P2=C2*n)
    check(checks,'P0_projector_bound',-ATOL<=P0<=n+ATOL,dict(value=P0,norm_squared=n))
    check(checks,'P1_complete_target_operator_bound',abs(P1)<=C1*n+ATOL,dict(value=P1,bound=C1*n))
    check(checks,'P2_complete_target_operator_bound',abs(P2)<=C2*n+ATOL,dict(value=P2,bound=C2*n))
    check(checks,'bridge_healing_weights_bounds',-ATOL<=bridgeweight<=n+ATOL and -ATOL<=healingweight<=4*n+ATOL,dict(bridge=bridgeweight,healing=healingweight,norm_squared=n))
    if row['age']==0.:
        close(np,checks,'initial_basis_P0',P0,0. if row['start']==0 else 1.)
        close(np,checks,'initial_basis_P1',P1,0.);close(np,checks,'initial_basis_P2',P2,0.)
        close(np,checks,'initial_basis_bridge_weight',bridgeweight,0.);close(np,checks,'initial_basis_healing_weight',healingweight,0.)
    a0=ATOL*max(1.,abs(P0),target)
    a1=ATOL*max(1.,abs(P1),abs(p1der),abs(p1pair),2*abs(p1inner))
    a2=ATOL*max(1.,abs(P2),abs(p2alt),abs(diagonalterm),abs(crossterm),abs(leakterm),abs(signed_bridge),abs(signed_healing))
    inherited=row['certified_vector_error_ceilings'][0]
    if inherited['delay']!=0.:raise RuntimeError('Delay0 inherited-vector error mismatch')
    eps=FLOAT_VECTOR*max(1.,math.sqrt(n))+inherited['exact_vector_error_ceilings']['psi']
    bands=coefficient_bands(P0,P1,P2,n,eps,(a0,a1,a2))
    close(np,checks,'frozen_endpoint_polynomial_twoforms',bands['raw_polynomial'],P0+TAU*(P1+.5*P2*TAU))
    check(checks,'finite_bounds_ordered',all(bands[k][0]<=bands[k][1] for k in ('raw_ideal_stored_probability_band','normalized_ideal_stored_probability_band','conditional_original_exact_probability_band','raw_ideal_stored_change_band','conditional_original_exact_change_band')))
    out=dict(key=key,g=row['g'],start=row['start'],age=row['age'],raw_norm_squared=n,input_column_norms=allnorms,input_sha256=hashes,parent_bundle_path=row['bundle_path'],parent_bundle_sha256=row['bundle_sha256'],original_complete_energy=float(Hmean.real),original_record_means=[parent_mean[f'record{v}'] for v in range(6)],old_connected_probability=oldconn,raw_target_initial_connected_probability=P0,P1=P1,P2=P2,normalized_stored_P0=P0/n,normalized_stored_P1=P1/n,normalized_stored_P2=P2/n,P2_terms=dict(compressed_positive=diagonalterm,compressed_cross=crossterm,offimage_leakage=leakterm,bridge=signed_bridge,healing=signed_healing),raw_anchor_bridge_weight=bridgeweight,raw_healing_link_count_weight=healingweight,raw_BminusC0K_mean=bmmean,ideal_target_operator_bounds=operatorbound,conditional_inherited_delay0_error=inherited,bands=bands,native_apply_call_count=2,no_target_vector=True,no_propagation=True,checks=checks,failed_count=sum(not c['passed'] for c in checks),elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=rss())
    p=CP/(key+'.json');exclusive(p,out);event('row_complete',key=key,sha256=sha(p),failed=out['failed_count'])
    print(json.dumps(dict(event='row_complete',key=key,P0=P0,P1=P1,P2=P2,conditional_endpoint_change_status=bands['conditional_original_change_status'],failed=out['failed_count'],elapsed_seconds=out['elapsed_seconds'])),flush=True)
    return out

def execute():
    if sys.platform!='darwin':raise RuntimeError('Same Mac only')
    if any(p.exists() for p in (CP,RESULT,REPORT)):raise RuntimeError('Exclusive output exists; no replay/resume authorized')
    if any(os.environ.get(k)!='1' for k in ENV):raise RuntimeError('One-thread/PYTHONDONTWRITEBYTECODE environment required before NumPy')
    hashes,parent=authenticate();CP.mkdir();started=time.monotonic()
    manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),utc=utc(),input_sha256=hashes,source_sha256=sha(SOURCE),protocol_sha256=sha(PROTOCOL),environment={k:os.environ[k] for k in ENV},inputs=dict(g=GS,starts=STARTS,ages=AGES,N_from=3,N_to=4,anchor=0,unconditional_isometry=True,tau=TAU,whole_interval=[0.,TAU],spectrum4=SPECTRUM4,center4=CENTER4,radius4=RADIUS4,connection_first_derivative_norm=C1,connection_second_derivative_norm=C2,third_remainder_coefficient=REMAINDER,float_vector_budget=FLOAT_VECTOR,arithmetic_allowance=ATOL,allowed_native_helpers=['fields','apply','graph_metadata'],allowed_native_metadata=['DIM','SCHEDULE'],native_apply_per_snapshot=2,one_row_resident=True,no_N4_vector=True,no_propagation=True,no_old_producer=True,no_resume=True))
    exclusive(CP/'manifest.json',manifest);event('started',manifest_sha256=sha(CP/'manifest.json'));print(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),status='started')),flush=True)
    try:
        import numpy as np
        flags,checks=graph_flags(np)
        if any(not c['passed'] for c in checks):raise RuntimeError('Graph structural checks failed; saved flags preserved')
        spec=importlib.util.spec_from_file_location('sealed_N3_pure_grown_connection_helpers',OLD_SOURCE);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        if old.DIM!=196608 or not any(tag=='main0' and age==0. and not signed for tag,age,signed in old.SCHEDULE):raise RuntimeError('Frozen native metadata mismatch')
        close(np,checks,'derivative_remainder_coefficient',C1*(2*RADIUS4)**2/6.,REMAINDER)
        close(np,checks,'second_derivative_norm_bound',C1*(2*RADIUS4),C2)
        close(np,checks,'complete_target_spectral_radius',max(abs(SPECTRUM4[0]-CENTER4),abs(SPECTRUM4[1]-CENTER4)),RADIUS4)
        rows=[]
        for g in GS:
            f=old.fields(np,g)
            check(checks,f'g{g}_pure_fields_configuration',f['g']==g and len(f['flips'])==9 and len(f['targets'])==3 and f['D'].shape==(196608,))
            for row in (r for r in parent['rows'] if r['g']==g):
                rows.append(run_row(np,old,f,parent,row,flags,hashes));gc.collect()
            del f;gc.collect()
        after,_=authenticate();check(checks,'all_input_bytes_unchanged',hashes==after)
        check(checks,'whole16_census',len(rows)==16 and sorted((r['g'],r['start'],r['age']) for r in rows)==sorted((g,n,a) for g in GS for n in STARTS for a in AGES))
        check(checks,'exactly32_pure_native_actions',sum(r['native_apply_call_count'] for r in rows)==32)
        combined=checks+[c for r in rows for c in r['checks']];failed=[c for c in combined if not c['passed']]
        counts={k:sum(r['bands']['conditional_original_change_status']==k for r in rows) for k in ('POSITIVE','NEGATIVE','INCONCLUSIVE')}
        slope_counts={k:sum(r['bands']['conditional_original_P1_status']==k for r in rows) for k in ('POSITIVE','NEGATIVE','INCONCLUSIVE')}
        payload=dict(status='QUALIFIED_ARITHMETIC' if not failed else 'FAILED_ARITHMETIC',qualification='Exact encoded target connection derivatives and bounded interval0..0.01 only; floating implementation/assigned original-state budgets conditional. No target propagation, later formed phase, physical clock/volume, pressure, metric, cosmology or Stage3 closure.',manifest=manifest,rows=rows,checks=checks,conditional_endpoint_change_counts=counts,conditional_initial_slope_counts=slope_counts,passed_count=len(combined)-len(failed),failed_count=len(failed),failed_checks=failed,runtime_seconds=time.monotonic()-started,peak_RSS_bytes=rss(),pid=os.getpid())
        payload['canonical_payload_sha256']=canonical(payload);exclusive(RESULT,payload);event('result_saved',sha256=sha(RESULT),canonical_payload_sha256=payload['canonical_payload_sha256'])
        lines=['# Encoded N4 initial connection dynamics V001: sealed result','',f"{payload['status']}; {payload['passed_count']}/{len(combined)} controls; all16 preparations.",'',payload['qualification'],'',f"Endpoint tau={TAU}; conditional original-state endpoint change census: {json.dumps(counts,sort_keys=True)}.",f"Conditional original-state initial slope census: {json.dumps(slope_counts,sort_keys=True)}.",'','| g | seed | age | raw norm | target P0 | P1 | P2 | normalized stored polynomial at.01 | conditional original probability band | conditional change |','|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
        for r in rows:
            b=r['bands'];lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{r['raw_norm_squared']:.12g}|{r['P0']:.10g}|{r['P1']:.10g}|{r['P2']:.10g}|{b['normalized_stored_polynomial']:.10g}|{b['conditional_original_exact_probability_band']}|{b['conditional_original_change_status']}|")
        lines+=['','The full input norm and signed bridge/healing terms are retained. All original records/copy histories remain in the16-state census. Initial seed slopes/curvatures being zero do not imply zero later target evolution. No unqualified sign or remainder-inconclusive interval is relabeled success/failure of growth.','', 'The876.096|t|³ mathematical remainder applies throughout0<=t<=.01. Scalar normalized-stored predictions and conditional original exact-seed probability bands are separate; original vectors were never renormalized. Assigned floating budgets/arithmetic allowances are not directed-rounding certificates. No target quantum array or evolution was constructed.',f"Runtime {payload['runtime_seconds']:.6f}s; peak RSS {payload['peak_RSS_bytes']}bytes; PID{os.getpid()}.",f'Raw result SHA256:{sha(RESULT)}',f"Canonical payload SHA256:{payload['canonical_payload_sha256']}",f'Protocol SHA256:{hashes[str(PROTOCOL)]}',f'Source SHA256:{hashes[str(SOURCE)]}','Exclusive graph and per-state JSON checkpoints and journal commits are preserved. This process ends here; no automatic continuation/replay/resume is installed. Root integrates the existing continuation log/ledger.']
        with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
        event('report_saved',sha256=sha(REPORT));print(json.dumps(dict(status=payload['status'],passed=payload['passed_count'],failed=payload['failed_count'],conditional_endpoint_change_counts=counts,conditional_initial_slope_counts=slope_counts,result_sha256=sha(RESULT),report_sha256=sha(REPORT),runtime_seconds=payload['runtime_seconds'],peak_RSS_bytes=payload['peak_RSS_bytes'])),flush=True)
        return 0 if not failed else 2
    except BaseException as e:
        error=dict(status='INTERRUPTED_OR_FAILED',error=repr(e),traceback=traceback.format_exc(),pid=os.getpid(),runtime_seconds=time.monotonic()-started,peak_RSS_bytes=rss())
        exclusive(CP/'error.json',error);event('error',sha256=sha(CP/'error.json'));print(json.dumps(error),flush=True);return 3

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');a=p.parse_args()
    if a.execute:return execute()
    print('Prospective source only; root/independent full preflight and live ownership approval required. No calculation launched.');return 0
if __name__=='__main__':sys.exit(main())
