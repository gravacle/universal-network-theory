#!/usr/bin/env python3
"""NEW saved-vector exact-symmetry conditioning diagnostic; root alone executes.
No eigensolver, propagation, RNG, producer import, physical state or old-result edit.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import sys,json,re,hashlib,math,time,traceback
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_SAVED_SYMMETRY_PROJECTOR_DIAGNOSTIC_V001';STEM='floating_return_c8_saved_symmetry_projector_diagnostic_v001'
CP=J/(STEM+'_checkpoints');RESULT=J/(NAME+'_RESULT.json');MD=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='e6a102a14fd50bdd3d5d2e682b9118487b3d250ff96d34b2def70ee4bc149e4b'
CERT='FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001';CSTEM='floating_return_c8_relative_energy_projector_certificate_v001'
LOCAL='FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001';LSTEM='floating_return_c8_localized_lapse_response_v001'
CYCLE=(0,4,3,7,2,6,1,5);REFLECTION={CYCLE[j]:CYCLE[(1-j)%8] for j in range(8)}
ARS=(F(0),F(1,8),F(7,40),F(1,4));OPS=('Vc','Vm','H','n','I');OP=5e-10;ETA=.2
INPUTS={};COMMITS={};CHECKS=[];ACTIVE={};STARTED=False;T0=0.
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def clean(x):
    if isinstance(x,np.ndarray):return clean(x.tolist())
    if isinstance(x,np.generic):return clean(x.item())
    if isinstance(x,complex):return [float(x.real),float(x.imag)]
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,float) and not math.isfinite(x):return {'nonfinite_float':repr(x)}
    return x
def check(name,ok,**evidence):
    CHECKS.append({'name':name,'passed':bool(ok),**clean(evidence)})
    if not ok:raise AssertionError(name)
def close(name,a,b,tol=OP):
    a,b=np.asarray(a),np.asarray(b);finite=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)));err=float(np.max(abs(a-b))) if finite else math.inf
    check(name,finite and err<=tol,maximum_absolute_error=err,tolerance=tol)
def fnorm(a):return float(np.sqrt(np.sum(abs(a)**2)))
def pin(p,h):
    p=Path(p).resolve();key=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    if key in INPUTS:check('consistent input '+key,INPUTS[key]==h);return
    check('input seal '+key,sha(p)==h);INPUTS[key]=h
def path(k):return Path(k) if Path(k).is_absolute() else ROOT/k
def recheck():
    for k,h in INPUTS.items():check('unchanged input '+k,sha(path(k))==h)
def write(p,x):
    with Path(p).open('xb') as f:f.write(canon(clean(x))+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def event(x):
    with (CP/'journal.jsonl').open('ab') as f:f.write(canon(clean(x))+b'\n');f.flush();os.fsync(f.fileno())
def save(name,x):
    h=write(CP/name,x);COMMITS[name]=h;event({'event':'stage_saved','file':name,'sha256':h});return h
def bundle(name,arrays):
    check('finite numerical bundle '+name,all(np.all(np.isfinite(v)) for v in arrays.values() if np.asarray(v).dtype.kind in 'biufc'))
    with (CP/name).open('xb') as f:np.savez(f,**arrays);f.flush();os.fsync(f.fileno())
    h=sha(CP/name);COMMITS[name]=h;event({'event':'stage_saved','file':name,'sha256':h});return h
def packet(name,stem,files,events):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'))
    for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json'):pin(J/(name+suffix),sha(J/(name+suffix)))
    check(name+' complete result',p['failed']==r['failed']==0 and p['passed']==r['passed']==len(p['checks']) and all(c['passed'] for c in p['checks']))
    check(name+' raw/canonical/report',r['result_raw_sha256']==sha(J/(name+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(canon(p)).hexdigest() and r['report_sha256']==sha(J/(name+'_RESULT.md')) and p['input_sha256']==r['input_sha256'])
    for k,h in r['input_sha256'].items():pin(path(k),h)
    cm=r['checkpoint_sha256'];check(name+' checkpoint census',len(cm)==files and set(cm)=={x.name for x in cp.iterdir() if x.name!='journal.jsonl'})
    for f,h in cm.items():pin(cp/f,h)
    raw=(cp/'journal.jsonl').read_bytes();ls=raw.splitlines(keepends=True);es=[json.loads(x) for x in ls]
    check(name+' prefix/commit census',len(es)==events and hashlib.sha256(b''.join(ls[:-1])).hexdigest()==r['journal_prefix_sha256'] and es[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))})
    check(name+' final result/report commits',es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and es[-2]['event']=='report_saved' and es[-2]['sha256']==r['report_sha256'])
    m=read(cp/'manifest.json');mh=sha(cp/'manifest.json');check(name+' manifest/start',mh==p['manifest_sha256'] and m['input_sha256']==r['input_sha256'] and es[0]['event']=='started' and es[0]['manifest_sha256']==mh and es[0]['input_sha256']==r['input_sha256'] and m['PID']==p['PID']==r['PID']==es[0]['PID'])
    commit={'manifest.json':mh}
    for e in es[1:-3]:check(name+' unique commit '+e['file'],e['file'] not in commit);commit[e['file']]=e['sha256']
    check(name+' complete checkpoint journal',commit==cm);pin(cp/'journal.jsonl',sha(cp/'journal.jsonl'));return p,r
def authenticate():
    protocol=J/(NAME+'.md');check('frozen protocol',sha(protocol)==PROTOCOL_SHA)
    pins=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',protocol.read_text(),re.M);check('fifteen direct pins',len(pins)==15)
    for f,h in pins:pin(J/f,h)
    pin(protocol,PROTOCOL_SHA);pin(__file__,sha(__file__))
    cert,cr=packet(CERT,CSTEM,21,24);local,lr=packet(LOCAL,LSTEM,7594,7597)
    a=read(J/(LOCAL+'_AUDIT.json'));check('accepted localized audit',a['audit_status']=='PASS' and a['failed_assertions']==0 and a['result_raw_sha256']==lr['result_raw_sha256'] and a['receipt_sha256']==sha(J/(LOCAL+'_RECEIPT.json')) and (a['audited_preparations'],a['audited_source_frames'],a['audited_channel_time_rows'])==(104,1664,4160))
    check('certificate full census',cert['component_count']==18 and cert['saved_mode_count']==384)
    data=J/(LSTEM+'_checkpoints/reused_localized_response_bases.npz');check('receipt owns reused bases',lr['checkpoint_sha256'][data.name]==sha(data))
    return cert,data
def permutations(two):
    labels=[(a,b) for a in range(8) for b in range(8) if a!=b] if two else [(a,) for a in range(8)]
    index={p:i for i,p in enumerate(labels)};d=len(labels)
    rr=np.array([bit*d+index[tuple(REFLECTION[v] for v in p)] for bit in (0,1) for p in labels])
    ss=np.array([bit*d+index[tuple(reversed(p))] for bit in (0,1) for p in labels]) if two else np.arange(2*d)
    check('commuting involutions '+str(two),np.array_equal(rr[rr],np.arange(2*d)) and np.array_equal(ss[ss],np.arange(2*d)) and np.array_equal(rr[ss],ss[rr]))
    return labels,rr,ss
def source40(labels):
    """Complete local Vc0 without record scalar terms, in integer units40."""
    d=len(labels);index={p:i for i,p in enumerate(labels)};occ=np.array([[int(v in p) for p in labels] for v in range(8)])
    pe=np.diag(np.r_[np.ones(d,dtype=np.int64),np.zeros(d,dtype=np.int64)]);n=np.eye(2*d,dtype=np.int64)-pe
    x=np.zeros((2*d,2*d),dtype=np.int64);x[:d,d:]=np.eye(d,dtype=np.int64);x[d:,:d]=np.eye(d,dtype=np.int64)
    bare=40*(np.eye(2*d,dtype=np.int64)+pe+np.diag(np.tile(occ[0],2)))-4*x
    for u,v in ((0,4),(0,5)):
        cut=occ[u]+occ[v]-2*occ[u]*occ[v]
        for bit in ((1,) if v==4 else (0,1)):
            off=bit*d;bare[off:off+d,off:off+d]+=5*np.diag(cut)
            for col,p in enumerate(labels):
                for species,site in enumerate(p):
                    if site not in (u,v):continue
                    dest=v if site==u else u
                    if dest in p:continue
                    q=list(p);q[species]=dest;bare[off+index[tuple(q)],off+col]-=2
    current=8j*(n@x-x@n);return bare,pe,n,current,x
def component_distance(ray,root,others):
    point=F.from_float(float(ray));ds=[]
    for r in others:
        if r['root_ID']==root['root_ID']:continue
        lo,hi=map(F,r['native_interval']);ds.append(max(lo-point,point-hi,F(0)))
    return min(ds) if ds else None
def process(sector,two,stage,saved):
    labels,rr,ss=permutations(two);d=len(labels);n=2*d;bare40,pe,nphys,current40,x=source40(labels)
    ev=saved[sector+'_eigenvalues'];vec=saved[sector+'_eigenvectors'];hs=saved[sector+'_base_matrices'];oldbare=saved[sector+'_bare_Vc_eigenbasis']
    check('saved six loading shapes '+sector,ev.shape==(3,n) and vec.shape==(3,n,n) and hs.shape==(3,n,n))
    roots={r['root_ID']:r for r in stage['root_intervals']};all_modes=[];loadings=[];components=[]
    for s in range(3):
        ACTIVE.update(sector=sector,s=s,phase='saved_exact_component_witness')
        h=hs[s];a=np.rint(20*h.real).astype(np.int64);close('integer action '+sector+str(s),20*h,a)
        check('exact integer symmetries '+sector+str(s),np.array_equal(a,a.T) and np.array_equal(a[np.ix_(rr,rr)],a) and np.array_equal(a[np.ix_(ss,ss)],a))
        ids=stage['loading_rows'][s]['mode_exact_root_ID'];close('old certified energies '+sector+str(s),ev[s],stage['loading_rows'][s]['saved_native_eigenvalues'],0.)
        check('simple complete original root census '+sector+str(s),len(ids)==n and len(set(ids))==n and all(roots[r]['multiplicity_by_loading'][s]==1 for r in ids))
        close('old complete Gram '+sector+str(s),vec[s].conj().T@vec[s],np.eye(n));close('old complete action '+sector+str(s),h@vec[s],vec[s]*ev[s][None,:])
        close('literal bare vertex '+sector+str(s),vec[s].conj().T@(bare40/40)@vec[s],oldbare[s])
        source_rows=[]
        for q0 in (0,1):
            q4=s-q0
            if q4 not in (0,1):continue
            for q5 in (0,1):
                for ar in ARS:
                    vc=bare40+20*q0*pe+int(40*ar)*q0*np.eye(n,dtype=np.int64)
                    vm=vc+10*((q0-q4)*nphys+(q0-q5)*np.eye(n,dtype=np.int64))
                    ops40=(vc,vm,2*a+int(40*ar)*(q0+q4+q5)*np.eye(n,dtype=np.int64),40*nphys,current40)
                    check('exact all-source S selection '+str((sector,s,q0,q4,q5,ar)),all(np.array_equal(o[np.ix_(ss,ss)],o) for o in ops40))
                    source_rows.append({'q0':q0,'q4':q4,'q5':q5,'AR':str(ar),'S_even_all_five':True,'R_even_Vc':bool(np.array_equal(vc[np.ix_(rr,rr)],vc)),'R_even_Vm':bool(np.array_equal(vm[np.ix_(rr,rr)],vm)),'complete_source_norm_order':OPS,'complete_source_Frobenius_upper_norm':[fnorm(vc/40),fnorm(vm/40),fnorm(h)+8*float(ar)*math.sqrt(n),fnorm(nphys),fnorm(current40/40)],'other_record_popcount':'all0..8 total occupations bounded by8; AR scalar commutes S/R and is retained in physical ancestor'})
        projected=np.zeros_like(vec[s],dtype=complex);resolution=np.zeros((n,n),object);resolution[:]=F(0);cw=[];mode_rows=[]
        ops=(bare40/40,pe,nphys,current40/40,h)
        opnorm=[fnorm(o) for o in ops]
        for ci,label in enumerate(stage['component_labels']):
            if label['s']!=s:continue
            sc,rc=label['S_character'],label['R_character'];prefix=f'{sector}_s{s}_S{sc:+d}_R{rc:+d}'
            rec=read(J/(CSTEM+'_checkpoints')/(prefix+'.json'));m=rec['dimension'];w=np.zeros((n,m),dtype=np.int64)
            for col,column in enumerate(rec['signed_orbit_basis']):
                for row,val in column.items():w[int(row),col]=val
            g=np.array(rec['Gram_diagonal'],np.int64);k=np.array(rec['integer_similar_block'],np.int64)
            check('complete exact component '+prefix,rec['sector']==sector and rec['s']==s and rec['S_character']==sc and rec['R_character']==rc and m==label['dimension'] and np.array_equal(w.T@w,np.diag(g)) and np.all(g>0) and np.array_equal(a@w,w@k) and np.array_equal(g[:,None]*k,(g[:,None]*k).T) and np.array_equal(w[rr],rc*w) and np.array_equal(w[ss],sc*w))
            for col in range(m):
                occupied=np.flatnonzero(w[:,col])
                for row in occupied:
                    for row2 in occupied:resolution[row,row2]+=F(int(w[row,col]*w[row2,col]),int(g[col]))
            indices=[i for i,rid in enumerate(ids) if roots[rid]['component_multiplicity'][ci]]
            check('root unique exact component '+prefix,len(indices)==m and all(roots[ids[i]]['component_multiplicity'][ci]==1 and sum(roots[ids[i]]['component_multiplicity'])==1 for i in indices))
            j=w/np.sqrt(g)[None,:];hc=(np.sqrt(g)[:,None]*k/np.sqrt(g)[None,:])/20;close('orthonormal exact orbit '+prefix,j.T@j,np.eye(m));close('symmetric component action '+prefix,hc,hc.T)
            others=[roots[ids[i]] for i in indices];local_rows=[]
            for mode in indices:
                v=vec[s,:,mode];pv=(v+rc*v[rr])/2
                if two:pv=(pv+sc*pv[ss])/2
                pv2=j@(j.T@v);close('independent signed orbit projection '+prefix+str(mode),pv,pv2)
                norm=fnorm(v);pnorm=fnorm(pv);check('positive finite projected norm '+prefix+str(mode),math.isfinite(pnorm) and pnorm>0 and norm>0)
                vn=pv/pnorm;projected[:,mode]=vn;coord=j.T@vn;ray=float(np.vdot(coord,hc@coord).real);res=fnorm(hc@coord-ray*coord)
                close('projected characters '+prefix+str(mode),np.r_[vn[rr]-rc*vn,vn[ss]-sc*vn],0.)
                dist=component_distance(ray,roots[ids[mode]],others);angle=min(1.,res/float(dist)) if dist is not None and dist>0 else None
                discard=fnorm(v-pv);projangle=discard/norm;normdefect=abs(norm*norm-1)
                row={'sector':sector,'s':s,'mode':mode,'root_ID':ids[mode],'S':sc,'R':rc,'original_energy':float(ev[s,mode]),'original_norm':norm,'discarded_norm':discard,'projected_norm':pnorm,'new_Rayleigh':ray,'Rayleigh_minus_original':ray-float(ev[s,mode]),'projected_residual':res,'other_same_component_distance':None if dist is None else str(dist),'component_angle_estimate':angle,'projection_angle_estimate':projangle,'old_norm_defect':normdefect,'status':'NON_DIRECTED_COMPONENT_ESTIMATE' if angle is not None else 'REFUSED_COMPONENT_SEPARATION','source_norm_order':('bare_Vc','Pempty','n','I','Hbar'),'source_Frobenius_upper_norm':opnorm,'projected_to_certified_expectation_estimate':None if angle is None else [2*z*angle for z in opnorm],'original_normalized_to_projected_expectation_estimate':[2*z*projangle for z in opnorm],'original_raw_norm_defect_estimate':[z*normdefect for z in opnorm],'original_raw_to_certified_total_estimate':None if angle is None else [2*z*(angle+projangle)+z*normdefect for z in opnorm],'full_source_control_error_contributions':[{'q0':sr['q0'],'q4':sr['q4'],'q5':sr['q5'],'AR':sr['AR'],'operator_order':OPS,'projected_residual_angle_term':None if angle is None else [2*z*angle for z in sr['complete_source_Frobenius_upper_norm']],'original_projection_angle_term':[2*z*projangle for z in sr['complete_source_Frobenius_upper_norm']],'original_raw_norm_defect_term':[z*normdefect for z in sr['complete_source_Frobenius_upper_norm']]} for sr in source_rows]}
                local_rows.append(row);mode_rows.append(row);all_modes.append(row)
            b=j.T@projected[:,indices];gram=b.conj().T@b;ACTIVE.update(component=prefix,phase='complete_component_Cholesky')
            l=np.linalg.cholesky(gram);close('Cholesky Gram '+prefix,l@l.conj().T,gram);check('positive triangular Cholesky '+prefix,np.all(np.diag(l).real>0) and np.array_equal(np.triu(l,1),np.zeros_like(l)))
            q=np.linalg.solve(l,b.conj().T).conj().T;xi=fnorm(q.conj().T@q-np.eye(m));check('complete polar witness '+prefix,math.isfinite(xi) and xi<1)
            dd=xi/(1+math.sqrt(1-xi));energies=ev[s,indices];delta_matrix=np.diag(energies);res=fnorm(hc@q-q*energies[None,:]);hnorm=fnorm(hc);delta=res+(hnorm+float(np.max(abs(energies))))*dd;epol=hnorm*dd*(1+math.sqrt(1+xi))
            knew=q.conj().T@hc@q;close('new component Hermitian '+prefix,knew,knew.conj().T)
            zeta=(11. if two else 9.5)+1j*ETA;ident=np.eye(m);lhs=zeta*ident-knew;oldlhs=zeta*ident-delta_matrix
            newr=np.linalg.solve(lhs,ident);oldr=np.linalg.solve(oldlhs,ident);close('new complex solve residual '+prefix,lhs@newr,ident);close('old complex solve residual '+prefix,oldlhs@oldr,ident)
            rdiff=fnorm(newr-oldr);estimate=math.sqrt(m)*(delta+epol)/(ETA*ETA)
            summary={'sector':sector,'s':s,'S':sc,'R':rc,'dimension':m,'mode_indices':indices,'root_IDs':[ids[i] for i in indices],'Gram_Frobenius':fnorm(gram-np.eye(m)),'nominal_Q_Gram_Frobenius':xi,'polar_distance_estimate':dd,'complete_action_residual_Frobenius':res,'Hcomponent_Frobenius_upper_norm':hnorm,'delta_estimate':delta,'nominal_polar_coordinate_correction':epol,'zeta':[zeta.real,zeta.imag],'resolvent_difference_Frobenius':rdiff,'resolvent_operator_error_estimate':(delta+epol)/(ETA*ETA),'resolvent_Frobenius_error_estimate':estimate,'same_component_unitary_Liouvillian_Abel_operator_estimate':2*delta/(ETA*ETA),'estimate_exceeds_observed_resolvent_difference':bool(estimate>=rdiff),'estimate_scope':'exact-arithmetic inequalities evaluated nondirected; magnitude is diagnostic, not response acceptance','mode_rows':local_rows}
            arrays={'original_mode_indices':np.array(indices),'original_root_IDs':np.array([ids[i] for i in indices]),'old_vectors':vec[s][:,indices],'old_eigenvalues':energies,'new_projected_vectors':projected[:,indices],'exact_signed_orbit_W':w,'exact_Gram_diagonal':g,'exact_integer_similar_block':k,'orbit_isometry':j,'Hcomponent':hc,'projected_coordinates_B':b,'Gram':gram,'Cholesky_L':l,'nominal_unitary_Q':q,'Knew_full_not_eigensystem':knew,'old_D':delta_matrix,'new_complex_resolvent':newr,'old_diagonal_complex_resolvent':oldr}
            bh=bundle(prefix+'.npz',arrays);summary['bundle_file']=prefix+'.npz';summary['bundle_sha256']=bh;save(prefix+'.json',summary);components.append(summary);cw.append(j)
        check('exact complete rational orbit resolution '+sector+str(s),all(resolution[i,j]==int(i==j) for i in range(n) for j in range(n)))
        close('full projected vector Gram '+sector+str(s),projected.conj().T@projected,np.eye(n))
        physicalops=(bare40/40,pe,nphys,current40/40,h);oldops=np.array([vec[s].conj().T@o@vec[s] for o in physicalops]);newops=np.array([projected.conj().T@o@projected for o in physicalops])
        schars=np.array([row['S'] for row in sorted(mode_rows,key=lambda x:x['mode'])]);rchars=np.array([row['R'] for row in sorted(mode_rows,key=lambda x:x['mode'])]);cross_s=schars[:,None]!=schars[None,:];cross_r=rchars[:,None]!=rchars[None,:]
        close('projected all-source cross-S selection '+sector+str(s),newops[:,cross_s],0.) if np.any(cross_s) else check('reference all-S plus '+str(s),bool(np.all(schars==1)))
        here=[c for c in components if c['s']==s];pair_bounds=[{'S':c['S'],'first_R':c['R'],'second_R':v['R'],'exact_unitary_pair_Liouvillian_Abel_operator_estimate':(c['delta_estimate']+v['delta_estimate'])/(ETA*ETA),'nominal_coordinate_pair_Liouvillian_Abel_operator_estimate':(c['delta_estimate']+v['delta_estimate']+c['nominal_polar_coordinate_correction']+v['nominal_polar_coordinate_correction'])/(ETA*ETA),'scope':'nondirected pair bound; opposite-R transitions retained, no Liouvillian solve/static qualification'} for c in here for v in here if c['S']==v['S']]
        row={'sector':sector,'s':s,'dimension':n,'mode_rows':sorted(mode_rows,key=lambda x:x['mode']),'literal_source_selection_controls':source_rows,'old_cross_S_source_max':float(np.max(abs(oldops[:,cross_s]))) if np.any(cross_s) else 0.,'projected_cross_S_source_max':float(np.max(abs(newops[:,cross_s]))) if np.any(cross_s) else 0.,'opposite_R_source_max_each':np.max(abs(newops[:,cross_r]),axis=1).tolist(),'opposite_R_transitions_retained':True,'same_S_component_pair_Abel_bounds':pair_bounds,'original_near_poles_and_refusals':'UNMODIFIED_IN_FROZEN_ANCESTORS'}
        prefix=sector+'_s'+str(s)+'_complete';bh=bundle(prefix+'.npz',{'old_Hbar':h,'old_eigenvalues':ev[s],'old_vectors':vec[s],'new_projected_vectors':projected,'root_IDs':np.array(ids),'S_characters':schars,'R_characters':rchars,'source_matrix_order':np.array(('bare_Vc','Pempty','n','I','Hbar')),'old_source_matrices':oldops,'new_projected_source_matrices':newops,'opposite_R_mask':cross_r,'cross_S_mask':cross_s})
        row['bundle_file']=prefix+'.npz';row['bundle_sha256']=bh;save(prefix+'.json',row);loadings.append(row)
    return loadings,components,all_modes
def main():
    global STARTED,T0
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
    if any(p.exists() for p in (CP,RESULT,MD,RECEIPT,ERROR)):raise SystemExit('Exclusive diagnostic path exists.')
    cert,data=authenticate();recheck();CP.mkdir();STARTED=True;T0=time.monotonic();mh=write(CP/'manifest.json',{'PID':os.getpid(),'input_sha256':INPUTS,'mode_count':384,'component_count':18,'loading_count':6,'new_eigensolver_calls':0,'physical_state_change':False,'operator_tolerance':OP,'complex_arguments':{'tagged':[11.,ETA],'reference':[9.5,ETA]},'norm_estimates':'nondirected; no old response requalification'});COMMITS['manifest.json']=mh;event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':INPUTS})
    with np.load(data,allow_pickle=False) as f:
        check('true inherited global cycle/pair map',f['cycle_global_nodes'].tolist()==list(CYCLE) and f['ordered_tagged_pairs'].tolist()==[[a,b] for a in range(8) for b in range(8) if a!=b])
        saved={k:f[k].copy() for k in ('tagged_eigenvalues','tagged_eigenvectors','tagged_base_matrices','tagged_bare_Vc_eigenbasis','reference_eigenvalues','reference_eigenvectors','reference_base_matrices','reference_bare_Vc_eigenbasis')}
    loads=[];components=[];modes=[]
    for sector,two in (('tagged',True),('reference',False)):
        stage=next(x for x in cert['sector_census'] if x['sector']==sector);ls,cs,ms=process(sector,two,stage,saved);loads+=ls;components+=cs;modes+=ms
    check('full fixed diagnostic census',len(loads)==6 and len(components)==18 and len(modes)==384 and len(COMMITS)==49)
    recheck()
    lines=['# Saved symmetry-projector diagnostic V001','','All384 original modes,6 loadings and18 components retained. Estimates are nondirected; old response results/refusals are unchanged. Localized opposite-R transitions and genuine odd physical modes remain. No eigensolver, trajectory, producer import or physical state change.','','| sector | s | old cross-S source maximum | projected cross-S maximum |','|---|---:|---:|---:|']
    for r in loads:lines.append('|%s|%d|%.12g|%.12g|'%(r['sector'],r['s'],r['old_cross_S_source_max'],r['projected_cross_S_source_max']))
    lines+=['','| sector | s | S | R | dimension | delta estimate | resolvent difference F | nondirected F estimate |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in components:lines.append('|%s|%d|%d|%d|%d|%.12g|%.12g|%.12g|'%(r['sector'],r['s'],r['S'],r['R'],r['dimension'],r['delta_estimate'],r['resolvent_difference_Frobenius'],r['resolvent_Frobenius_error_estimate']))
    lines+=['','All384 individual norms, discarded pieces, projected residuals, within-component distances and three separate expectation-error contributions are in RESULT.json. Original and projected vectors, exact W/G/K, complete new coordinate action and both complex solves are lossless in49 checkpoint files. The new Knew is not a replacement eigensystem. No true static response accuracy is certified.','']
    check('report six/eighteen rows',sum(l.startswith('|tagged|') or l.startswith('|reference|') for l in lines)==24)
    result={'status':'PASS_SAVED_SYMMETRY_DIAGNOSTIC_NON_DIRECTED','failed':0,'passed':len(CHECKS),'checks':CHECKS.copy(),'input_sha256':INPUTS,'manifest_sha256':mh,'PID':os.getpid(),'elapsed_seconds':time.monotonic()-T0,'loading_rows':loads,'component_rows':components,'mode_rows':modes,'scope':'All old modes/vectors remain. Exact S selection for five declared operators only. Opposite-R transitions and genuine odd modes retained; no old response/refusal requalification, physical state, passivity or gravity claim.'}
    raw=write(RESULT,result);ch=hashlib.sha256(canon(clean(result))).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':ch});lines+=['Result SHA256: '+raw,'']
    with MD.open('x') as f:f.write('\n'.join(lines));f.flush();os.fsync(f.fileno())
    rh=sha(MD);event({'event':'report_saved','sha256':rh,'loading_rows':6,'component_rows':18,'mode_rows':384})
    for k,h in INPUTS.items():
        if sha(path(k))!=h:raise RuntimeError('post-output input changed '+k)
    cm={p.name:sha(p) for p in CP.iterdir() if p.name!='journal.jsonl'}
    if cm!=COMMITS:raise RuntimeError('final exact49 checkpoint map')
    receipt={'status':result['status'],'failed':0,'passed':result['passed'],'input_sha256':INPUTS,'checkpoint_sha256':cm,'result_raw_sha256':raw,'result_canonical_sha256':ch,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'PID':os.getpid(),'old_response_modified':False}
    rr=write(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr});print(json.dumps({'status':result['status'],'passed':result['passed'],'result_raw_sha256':raw,'receipt_sha256':rr}),flush=True)
if __name__=='__main__':
    try:main()
    except Exception as e:
        if STARTED and not ERROR.exists():
            eh=write(ERROR,{'status':'EXECUTION_ERROR_PRESERVED','error':repr(e),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'completed_sha256':COMMITS,'input_sha256':INPUTS,'source_sha256':sha(__file__),'PID':os.getpid()});event({'event':'error','sha256':eh})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
