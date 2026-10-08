#!/usr/bin/env python3
"""One prospective saved-state census-work application; no H or propagation."""
from pathlib import Path
import argparse, datetime, hashlib, json, math, os, resource, socket, sys, time, traceback

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
SOURCE=Path(__file__).resolve()
PROTOCOL=J/'NATIVE_UNCLAMPED_CENSUS_CREATION_V001.md'
PARENT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json'
PARENT_REPORT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.md'
PARENT_CP=J/'bs10_k33_nodal_signal_v001_checkpoints'
CP=J/'bs10_k33_census_creation_saved_v001_checkpoints'
OUT=J/'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.json'
REPORT=J/'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.md'
PARENT_SHA='7a4fc007d3ca9a46482091f4e6ab54a78c866dd4eabaeb19fc4d83b766c2499c'
PARENT_CANONICAL='0da65bdca466d621561b04a341d2881906d7586535b33bd07a6d3edba4e62240'
PARENT_REPORT_SHA='dbc549f522212fd9cd523a56d6e00304419d100cedc68cc1e07af3865db8a35b'
ENV=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS')
EXPECTED={(g,n,a) for g in (0.,.1) for n in (0,413) for a in (0.,5.,20.,50.)}
ATOL=5e-11
DELAYS=(0.,.1,.5,1.,2.,5.)
D_NORM_BOUND=8.7

def sha(p):
    p=Path(p).resolve()
    if not p.is_relative_to(ROOT):raise RuntimeError('Input outside sole root: '+str(p))
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def canonical(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def exclusive(p,x):
    with p.open('x',encoding='utf8') as f:
        json.dump(x,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def event(name,**kw):
    item=dict(event=name,pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw)
    with (CP/'events.jsonl').open('a',encoding='utf8') as f:
        f.write(json.dumps(item,sort_keys=True,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())

def components(mask,N):
    adj=[[] for _ in range(2*N)]
    for i in range(N):
        for j in range(N):
            if (mask>>(N*i+j))&1:
                adj[i].append(N+j);adj[N+j].append(i)
    unseen=set(range(2*N));count=0
    while unseen:
        stack=[unseen.pop()];count+=1
        while stack:
            for v in adj[stack.pop()]:
                if v in unseen:unseen.remove(v);stack.append(v)
    return count,[len(x) for x in adj]

def image(mask):
    out=0
    for i in range(3):
        for j in range(3):
            f=3*i+j
            if f!=0 and (mask>>f)&1:out|=1<<(4*i+j)
    if mask&1:
        for f in (3,12,15):out|=1<<f
    return out

def authenticate_parent():
    if sha(PARENT)!=PARENT_SHA:raise RuntimeError('Parent receipt digest mismatch')
    parent=json.loads(PARENT.read_text());base=dict(parent);digest=base.pop('canonical_payload_sha256')
    if digest!=PARENT_CANONICAL or canonical(base)!=digest:raise RuntimeError('Parent canonical mismatch')
    if parent['status']!='QUALIFIED_ARITHMETIC' or parent['failed_count'] or parent['passed_count']!=5272:
        raise RuntimeError('Parent qualification mismatch')
    if parent['manifest']['host']!=socket.gethostname():raise RuntimeError('Parent and current Mac host mismatch')
    custody=dict(parent['manifest']['input_sha256'])
    for p,h in custody.items():
        if sha(p)!=h:raise RuntimeError('Original input changed: '+p)
    mp=PARENT_CP/'manifest.json';ep=PARENT_CP/'events.jsonl'
    if json.loads(mp.read_text())!=parent['manifest']:raise RuntimeError('Parent manifest mismatch')
    events=[json.loads(line) for line in ep.read_text().splitlines() if line]
    if not any(e['event']=='started' and e['pid']==parent['manifest']['pid'] and e['manifest_sha256']==sha(mp) for e in events):raise RuntimeError('Parent started-manifest commit missing')
    if not any(e['event']=='result_saved' and e['sha256']==PARENT_SHA and e['canonical_payload_sha256']==PARENT_CANONICAL for e in events):raise RuntimeError('Parent raw/canonical result commit missing')
    if sha(PARENT_REPORT)!=PARENT_REPORT_SHA or not any(e['event']=='report_saved' and e['sha256']==PARENT_REPORT_SHA for e in events):raise RuntimeError('Parent report commit mismatch')
    if {(r['g'],r['start'],r['age']) for r in parent['rows']}!=EXPECTED or len(parent['rows'])!=16:
        raise RuntimeError('Frozen16-state census mismatch')
    custody.update({str(PARENT):PARENT_SHA,str(PARENT_REPORT):PARENT_REPORT_SHA,str(mp):sha(mp),str(ep):sha(ep),str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)})
    for name in ('CONNECTED_SUBDIVISION_GROWTH_CANDIDATE_V001.md','NATIVE_CARRIER_RULER_PATHWAY_V001.md','NATIVE_VOLUME_INCREMENT_PATHWAY.md'):
        p=J/name;custody[str(p)]=sha(p)
    for row in parent['rows']:
        key=f'g{int(row["g"]>0)}_n{row["start"]}_age{int(row["age"])}'
        rp=PARENT_CP/(key+'.json');bp=Path(row['bundle_path']);rh=sha(rp);bh=sha(bp)
        if json.loads(rp.read_text())!=row or row['failed_count'] or bh!=row['bundle_sha256']:
            raise RuntimeError('Parent row or bundle mismatch: '+key)
        if not any(e['event']=='row_complete' and e['key']==key and e['sha256']==rh and e['failed']==0 for e in events):
            raise RuntimeError('Parent row commit missing: '+key)
        if not any(e['event']=='bundle_saved' and e['key']==key and e['sha256']==bh for e in events):
            raise RuntimeError('Parent bundle commit missing: '+key)
        custody[str(rp)]=rh;custody[str(bp)]=bh
    return parent,custody

def execute():
    import numpy as np
    started=time.monotonic();rows=[];checks=[];custody={}
    def check(name,ok,evidence):checks.append(dict(name=name,passed=bool(ok),evidence=evidence))
    def equal(name,x,y,tolerance=ATOL):
        err=abs(x-y);tol=tolerance*max(1.,abs(x),abs(y))
        check(name,err<=tol,dict(actual=float(x),expected=float(y),error=float(err),tolerance=float(tol)))
    try:
        parent,custody=authenticate_parent()
        manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),source_sha256=sha(SOURCE),protocol_sha256=sha(PROTOCOL),input_sha256=custody,environment={k:os.environ[k] for k in ENV},inputs=dict(anchor=0,g=[0.,.1],starts=[0,413],ages=[0.,5.,20.,50.],source_delays=list(DELAYS),D_norm_bound=D_NORM_BOUND,N_from=3,N_to=4,Omega=.6,h_from=.2,h_to=.15,Ud=1.,dstar=2,Delta=0.,t=.1,lambdaJ=.25,lambdaR=.5,EP=1.,ER=1.,Nc=1,no_H_or_native_import=True,no_propagation=True,no_N4_vector=True,one_row_resident=True,resume=False))
        exclusive(CP/'manifest.json',manifest);event('manifest_saved',sha256=sha(CP/'manifest.json'))
        masks=np.arange(512,dtype=np.int64);occupied=(masks&1).astype(float)
        conn=np.array([components(int(n),3)[0]==1 for n in masks],dtype=float)
        image_masks=[image(int(n)) for n in masks]
        check('512_images_injective',len(set(image_masks))==512,dict(count=len(set(image_masks))))
        for n,target in enumerate(image_masks):
            oldc,oldd=components(n,3);newc,newd=components(target,4);bit=n&1
            mapped=[newd[v] for v in (0,1,2,4,5,6)]
            check(f'image{n}_degrees',mapped==oldd and newd[3]==newd[7]==2*bit,dict(old=oldd,new=newd))
            check(f'image{n}_component_identity',newc==oldc+2*(1-bit) and (newc==1)==bool(bit and oldc==1),dict(old_components=oldc,new_components=newc,n0=bit))
            code=[(target>>f)&1 for f in (3,12,15)]
            check(f'image{n}_reverse_code_support',not(target&1) and code==[bit]*3 and all(not((target>>f)&1) for f in (7,11,13,14)),dict(target_mask=target,code=code))
        target_conn=np.array([components(n,4)[0]==1 for n in image_masks],dtype=float)
        structural=checks.copy();exclusive(CP/'graph_images.json',dict(image_masks=image_masks,checks=structural,failed_count=sum(not c['passed'] for c in structural)));event('graph_images_saved',sha256=sha(CP/'graph_images.json'))
        carrier_ends=np.array([1.,0.,0.,1.,0.,0.])[None,:,None]
        occupied3=occupied[:,None,None];conn3=conn[:,None,None]
        def D_terms(v):
            hopping=np.zeros_like(v)
            hopping[1::2,0,:]=.1*v[1::2,3,:];hopping[1::2,3,:]=.1*v[1::2,0,:]
            rest=np.zeros_like(v)
            for f in range(1,9):rest+=.05*v[masks^(1<<f)]
            return (8.*(1.-occupied3)*v,hopping,rest,.2*v[masks^1])
        def D_action(v):
            out=8.*(1.-occupied3)*v+.2*v[masks^1]
            for f in range(1,9):out+=.05*v[masks^(1<<f)]
            out[1::2,0,:]+=.1*v[1::2,3,:];out[1::2,3,:]+=.1*v[1::2,0,:]
            return out
        for old in parent['rows']:
            row_start=time.monotonic();first=len(checks)
            selected=st=None
            key=f'g{int(old["g"]>0)}_n{old["start"]}_age{int(old["age"])}'
            with np.load(old['bundle_path'],allow_pickle=False) as z:
                metadata=json.loads(str(z['metadata_json']));cols=z['input_columns'];main=z['propagated_main_columns'];saved_delays=z['delays']
            if metadata['input_sha256']!=parent['manifest']['input_sha256'] or (metadata['g'],metadata['start'],metadata['age'])!=(old['g'],old['start'],old['age']):raise RuntimeError('Array metadata mismatch: '+key)
            if cols.shape!=(3,196608) or not np.all(np.isfinite(cols)):raise RuntimeError('Array shape/finite mismatch: '+key)
            if main.shape!=(6,3,196608) or not np.all(np.isfinite(main)) or tuple(saved_delays)!=DELAYS:raise RuntimeError('Saved six-delay columns mismatch: '+key)
            if metadata['certified_vector_error_ceilings']!=old['certified_vector_error_ceilings'] or metadata['input_column_norms']!=old['input_column_norms']:raise RuntimeError('Saved propagated error/norm metadata mismatch: '+key)
            equal(key+'_zero_delay_input_columns',float(np.max(np.abs(main[0]-cols))),0.)
            psi=cols[0].reshape(512,6,64).copy();del cols
            density=np.abs(psi)**2;norm=float(np.vdot(psi,psi).real)
            graph_prob=density.sum(axis=(1,2));car_prob=density.sum(axis=(0,2))
            def inner(label,vec):
                value=np.vdot(psi,vec);equal(key+'_'+label+'_imaginary',float(value.imag),0.)
                return float(value.real)
            w=inner('weight',occupied3*psi);w_sum=float(graph_prob[1::2].sum());equal(key+'_weight_two_forms',w,w_sum)
            cp=inner('occupied_carrier_ends',occupied3*carrier_ends*psi)
            cp_sum=float(density[1::2][:,(0,3),:].sum());equal(key+'_occupied_carrier_two_forms',cp,cp_sum)
            xvalues=[];xvector=np.zeros_like(psi);xeligible=np.zeros_like(psi)
            for f in range(9):
                gather=psi[masks^(1<<f)];x=inner('X'+str(f),gather)
                low=masks[((masks>>f)&1)==0]
                pair=2.*float(np.vdot(psi[low],psi[low^(1<<f)]).real)
                equal(key+f'_X{f}_bitpair',x,pair);xvalues.append(x)
                check(key+f'_X{f}_bound',abs(x)<=norm+ATOL,dict(value=x,norm=norm))
                if f:xvector+=gather;xeligible+=occupied3*gather
            xrest=inner('Xrest',xvector);equal(key+'_Xrest_sum',xrest,sum(xvalues[1:]))
            pxrest=inner('PXrest',xeligible)
            pxpair=0.
            for f in range(1,9):
                low=masks[(occupied==1)&(((masks>>f)&1)==0)]
                pxpair+=2.*float(np.vdot(psi[low],psi[low^(1<<f)]).real)
            equal(key+'_PXrest_bitpair',pxrest,pxpair)
            nT=np.zeros_like(psi);nT[1::2,0,:]=psi[1::2,3,:];nT[1::2,3,:]=psi[1::2,0,:]
            hop=inner('nT03',nT);hop_pair=2.*float(np.vdot(psi[1::2,0,:],psi[1::2,3,:]).real)
            equal(key+'_nT03_pair',hop,hop_pair)
            terms=dict(new_degree_baseline=8.*(norm-w),removed_direct_hopping=.1*hop,old_nonanchor_flip_normalization=.05*xrest,lost_old_anchor_flip=.2*xvalues[0])
            dvector=8.*(1.-occupied3)*psi+.1*nT+.05*xvector+.2*psi[masks^1]
            work=inner('D_direct',dvector);equal(key+'_D_four_terms',work,sum(terms.values()))
            eligible_numerator=.05*pxrest+.1*hop
            vacant_rest=xrest-pxrest
            branch_work=8.*(norm-w)+.05*vacant_rest+eligible_numerator+.2*xvalues[0]
            equal(key+'_D_branch_decomposition',work,branch_work)
            leak=inner('target_leakage_operator',(.18+.01*occupied3*carrier_ends)*psi)
            equal(key+'_target_leakage_coefficient',leak,.18*norm+.01*cp)
            oldconn=inner('old_connection',conn3*psi)
            newconn=inner('target_connection',target_conn[:,None,None]*psi)
            newconn_pair=float(graph_prob[(occupied==1)&(conn==1)].sum());equal(key+'_target_connection_bitformula',newconn,newconn_pair)
            lostconn=inner('lost_connection',(1.-occupied3)*conn3*psi);equal(key+'_connection_decomposition',oldconn,newconn+lostconn)
            equal(key+'_input_norm',norm,1.,2e-9)
            parent_means=old['response'][0]['means']
            equal(key+'_old_connection_parent',oldconn,parent_means['connected'],2e-8)
            for v in range(6):equal(key+f'_carrier{v}_parent',float(car_prob[v]),parent_means[f'carrier{v}'],2e-8)
            check(key+'_probability_bounds',-ATOL<=w<=norm+ATOL and -ATOL<=cp<=w+ATOL and -ATOL<=oldconn<=norm+ATOL and -ATOL<=newconn<=w+ATOL and -ATOL<=lostconn<=norm+ATOL,dict(w=w,cp=cp,old=oldconn,target=newconn,lost=lostconn,norm=norm))
            check(key+'_occupied_hop_bound',abs(hop)<=w+ATOL,dict(hop=hop,w=w))
            if w>0.:
                selected=occupied3*psi/(w**.5)
                conditional_work=eligible_numerator/w
                sx=np.zeros_like(psi)
                for f in range(1,9):sx+=selected[masks^(1<<f)]
                st=np.zeros_like(psi);st[:,0,:]=selected[:,3,:];st[:,3,:]=selected[:,0,:]
                direct=np.vdot(selected,.05*sx+.1*st)
                equal(key+'_conditional_work_two_forms',float(direct.real),conditional_work);equal(key+'_conditional_work_imaginary',float(direct.imag),0.)
                conditional_leak=.18+.01*cp/w
                leak_direct=np.vdot(selected,(.18+.01*carrier_ends)*selected)
                equal(key+'_conditional_leakage_two_forms',float(leak_direct.real),conditional_leak)
                conditional_conn=newconn/w;cc=np.vdot(selected,conn3*selected)
                equal(key+'_conditional_connection_two_forms',float(cc.real),conditional_conn)
                equal(key+'_conditional_norm',float(np.vdot(selected,selected).real),1.)
                eligible_status='DEFINED_EXACT_POSITIVE_WEIGHT'
            elif w==0.:
                conditional_work=conditional_leak=conditional_conn=None;eligible_status='UNDEFINED_EXACT_ZERO_WEIGHT'
                equal(key+'_zero_weight_numerator',eligible_numerator,0.);equal(key+'_zero_weight_ends',cp,0.);equal(key+'_zero_weight_target_connection',newconn,0.)
            else:raise RuntimeError('Negative raw occupation weight')
            if old['age']==0.:
                blank=old['start']==0
                equal(key+'_initial_work',work,8. if blank else 0.)
                equal(key+'_initial_target_leakage',leak,.18 if blank else .19)
                equal(key+'_initial_weight',w,0. if blank else 1.)
                check(key+'_initial_eligible_status',(eligible_status=='UNDEFINED_EXACT_ZERO_WEIGHT')==blank,dict(status=eligible_status,blank=blank))
                equal(key+'_initial_target_connection',newconn,0. if blank else 1.)
                if not blank:
                    equal(key+'_initial_conditional_work',conditional_work,0.)
                    equal(key+'_initial_conditional_leakage',conditional_leak,.19)
            source_rows=[]
            for index,delay in enumerate(DELAYS):
                sp=main[index,0].reshape(512,6,64);sx=main[index,1].reshape(512,6,64)
                snorm2=float(np.vdot(sp,sp).real);xnorm2=float(np.vdot(sx,sx).real)
                equal(key+f'_delay{delay}_psi_norm',snorm2,norm,2e-9)
                equal(key+f'_delay{delay}_source_tangent_norm',xnorm2,old['input_column_norms']['h0psi']**2,2e-9)
                dp=D_action(sp);dx=D_action(sx)
                cross=np.vdot(dp,sx);other=np.vdot(sp,dx)
                residual=abs(cross-other);tol=ATOL*max(1.,abs(cross),abs(other))
                check(key+f'_delay{delay}_Hermitian_left_right',residual<=tol,dict(error=float(residual),tolerance=float(tol)))
                kernel=2.*float(cross.imag)/norm
                pieces=D_terms(sp);piece_values=[2.*float(np.vdot(part,sx).imag)/norm for part in pieces]
                equal(key+f'_delay{delay}_kernel_decomposition',kernel,sum(piece_values))
                dmean=np.vdot(sp,dp);equal(key+f'_delay{delay}_mean_imaginary',float(dmean.imag),0.)
                raw_dmean=float(dmean.real)
                if delay==0.:equal(key+'_zero_delay_work_baseline',raw_dmean,work)
                control=old['certified_vector_error_ceilings'][index]
                if control['delay']!=delay:raise RuntimeError('Inherited error-ceiling delay mismatch')
                epsp=control['exact_vector_error_ceilings']['psi'];epsx=control['exact_vector_error_ceilings']['h0psi']
                pnorm=math.sqrt(snorm2);xnorm=math.sqrt(xnorm2)
                exact_kernel_bound=2.*D_NORM_BOUND*(epsp*xnorm+epsx*pnorm+epsp*epsx)/norm
                exact_mean_bound=D_NORM_BOUND*(2.*pnorm*epsp+epsp*epsp)/norm
                check(key+f'_delay{delay}_D_operator_bound',abs(raw_dmean)<=D_NORM_BOUND*snorm2+ATOL,dict(mean=raw_dmean,norm_squared=snorm2,bound=D_NORM_BOUND))
                source_rows.append(dict(delay=delay,raw_creation_work=raw_dmean,normalized_creation_work=raw_dmean/norm,complete_h0_plus_source_kernel=kernel,signed_source_kernel_terms=dict(zip(terms,piece_values)),raw_psi_norm_squared=snorm2,raw_source_tangent_norm_squared=xnorm2,source_tangent_norm=xnorm,D_norm_bound=D_NORM_BOUND,inherited_exact_vector_error_ceilings=control,induced_exact_arithmetic_kernel_error_ceiling=exact_kernel_bound,induced_exact_arithmetic_normalized_mean_error_ceiling=exact_mean_bound,floating_roundoff_certified=False,clock_corrected=False))
            result=dict(key=key,g=old['g'],start=old['start'],age=old['age'],raw_norm=norm,original_complete_energy=parent_means['H'],original_record_means=[parent_means[f'record{v}'] for v in range(6)],work_terms=terms,raw_unconditional_work=work,success_weight=w,normalized_success_probability=w/norm,X_values=xvalues,raw_Xrest=xrest,raw_PXrest=pxrest,raw_nT03=hop,raw_n0_carrier_end_occupation=cp,raw_target_leakage_squared=leak,raw_old_connected_probability=oldconn,raw_target_connected_probability=newconn,raw_lost_connected_probability=lostconn,eligible_status=eligible_status,eligible_conditional_work=conditional_work,eligible_conditional_leakage_squared=conditional_leak,eligible_conditional_connected_probability=conditional_conn,occupied_branch_work_numerator=eligible_numerator,vacant_rest_flip_expectation=vacant_rest,creation_work_source_response=source_rows,input_bundle_path=old['bundle_path'],input_bundle_sha256=old['bundle_sha256'],checks=checks[first:],failed_count=sum(not c['passed'] for c in checks[first:]),elapsed_seconds=time.monotonic()-row_start,peak_RSS_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            exclusive(CP/(key+'.json'),result);event('row_complete',key=key,sha256=sha(CP/(key+'.json')),failed=result['failed_count']);rows.append(result)
            print(json.dumps(dict(event='row_complete',key=key,work=work,weight=w,target_connection=newconn,failed=result['failed_count'])),flush=True)
            del psi,density,dvector,xvector,xeligible,nT,main,sp,sx,dp,dx,pieces,selected,st,gather
        for p,h in custody.items():
            if sha(p)!=h:raise RuntimeError('Input changed during extraction: '+p)
        status='QUALIFIED_SAVED_ARRAY_ARITHMETIC' if all(c['passed'] for c in checks) else 'FAILED_SAVED_ARRAY_ARITHMETIC'
        error=None
    except Exception as exc:
        status='FAILED_EXECUTION';error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc())
        event('failure',error=error)
    failed=sum(not c['passed'] for c in checks)
    output=dict(status=status,qualification='Exact added census-port compression and connected-incorporation arithmetic on frozen native states; no spontaneous growth, physical volume, pressure, gravity or future dynamics claim',input_sha256=custody,parent_sha256=PARENT_SHA,pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),rows=rows,checks=checks,passed_count=len(checks)-failed,failed_count=failed,error=error,resume=False,elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    output['canonical_payload_sha256']=canonical(output);exclusive(OUT,output);event('result_saved',sha256=sha(OUT),canonical_payload_sha256=output['canonical_payload_sha256'])
    lines=['# Native unconditional census creation: saved-state result','',f"{status}: {output['passed_count']}/{len(checks)} arithmetic controls; {len(rows)}/16 saved rows.",'',output['qualification'],'','| g | start / full E | age | raw work | eligible weight | target connected | lost connected | eligible work |','|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        conditional='undefined' if r['eligible_conditional_work'] is None else f"{r['eligible_conditional_work']:.12g}"
        lines.append(f"|{r['g']}|{r['start']} / {r['original_complete_energy']:.12g}|{r['age']}|{r['raw_unconditional_work']:.12g}|{r['success_weight']:.12g}|{r['raw_target_connected_probability']:.12g}|{r['raw_lost_connected_probability']:.12g}|{conditional}|")
    lines+=['','All96 saved-delay creation-work source kernels: PLUS complete-h0 impulse, original conditional generator age, no clock correction.','', '| g | start | age | delay | normalized work | R_D,h0 |','|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        for cell in r['creation_work_source_response']:
            lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{cell['delay']}|{cell['normalized_creation_work']:.12g}|{cell['complete_h0_plus_source_kernel']:.12g}|")
    lines+=['','Anchor0=(old0,old3), original conditional ages and all raw coherences were frozen before outcomes. The unconditional map retains n0=0 inputs and adds two isolated vertices in that arm. The normalized occupied-only comparison is separate; exact-zero weights are undefined.','',f'Parent raw SHA256: {PARENT_SHA}',f'Result raw SHA256: {sha(OUT)}','',f'Execution error: {error}' if error else 'No Hamiltonian, N4 vector, propagation, old helper import or solver was executed.']
    with REPORT.open('x',encoding='utf8') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    event('report_saved',sha256=sha(REPORT));print(json.dumps(dict(status=status,passed=output['passed_count'],failed=failed,result_sha256=sha(OUT))),flush=True)
    return 0 if status=='QUALIFIED_SAVED_ARRAY_ARITHMETIC' else 1

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true',required=True);args=parser.parse_args()
    if sys.platform!='darwin':raise RuntimeError('Same Mac only')
    if any(os.environ.get(k)!='1' for k in ENV):raise RuntimeError('Set all BLAS thread variables to1 before NumPy import')
    if os.environ.get('PYTHONDONTWRITEBYTECODE')!='1':raise RuntimeError('Disable bytecode writes')
    if OUT.exists() or REPORT.exists() or CP.exists():raise RuntimeError('Exclusive outputs/checkpoints exist; preserve them, no resume')
    CP.mkdir();event('started',ppid=os.getppid(),host=socket.gethostname(),source_sha256=sha(SOURCE),protocol_sha256=sha(PROTOCOL))
    return execute()

if __name__=='__main__':sys.exit(main())
