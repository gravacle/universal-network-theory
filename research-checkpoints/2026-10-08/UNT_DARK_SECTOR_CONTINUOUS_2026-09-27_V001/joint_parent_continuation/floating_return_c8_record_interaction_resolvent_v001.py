#!/usr/bin/env python3
"""NEW small record-dependent Schur operators; root alone may execute."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,resource,traceback,re
from pathlib import Path
import numpy as np
J=Path(__file__).resolve().parent;ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_RECORD_INTERACTION_RESOLVENT_V001'
CP=J/'floating_return_c8_record_interaction_resolvent_v001_checkpoints'
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='ebbfb9fb4c206696daf275fe95f49abbda1c26213f697cf04cfd235c5436ae13'
LAW='LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md'
PACKETS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001',1146,416),
         ('FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001','floating_return_c8_retained_record_geometry_v001',3018,1352))
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple((CYCLE[k],CYCLE[(k+1)%8]) for k in range(8))
PAIRS=tuple((a,b) for a in range(8) for b in range(8) if a!=b)
H=.2;T=.1;JC=.25;LAM=.5;TOL=5e-10
CHECKS=[];INPUTS={};COMMITS={};ACTIVE={};STARTED=False

def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):d.update(b)
    return d.hexdigest()

def read(p):return json.loads(Path(p).read_text())

def clean(v):
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,np.generic):return clean(v.item())
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,complex):return [clean(float(v.real)),clean(float(v.imag))]
    if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
    return v

def blob(v):return json.dumps(clean(v),sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def write_json(p,v):
    with Path(p).open('xb') as f:
        f.write(json.dumps(clean(v),sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def event(v):
    with (CP/'journal.jsonl').open('ab') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())

def commit(p,v,kind):
    h=write_json(p,v);COMMITS[Path(p).name]=h;event({'event':kind,'file':Path(p).name,'sha256':h});return h

def commit_npz(p,**a):
    with Path(p).open('xb') as f:np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
    h=sha(p);COMMITS[Path(p).name]=h;event({'event':'operators_saved','file':Path(p).name,'sha256':h});return h

def gate(name,a,b=0.,tol=TOL):
    a,b=np.asarray(a),np.asarray(b);ok=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    err=float(np.max(abs(a-b))) if ok else float('inf')
    CHECKS.append({'name':name,'error':clean(err),'tolerance':tol,'passed':ok and err<=tol})

def exact(name,ok):CHECKS.append({'name':name,'passed':bool(ok),'exact':True})

def input_id():return hashlib.sha256(blob(INPUTS)).hexdigest()

def recheck():
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h:raise RuntimeError('input changed: '+f)

def register(p,h):
    if sha(p)!=h:raise RuntimeError('input seal: '+str(p))
    k=str(Path(p).relative_to(ROOT))
    if k in INPUTS and INPUTS[k]!=h:raise RuntimeError('contradictory input seal: '+k)
    INPUTS[k]=h

def authenticate_parent(name,stem,count,frames):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'));a=read(J/(name+'_AUDIT.json'))
    if r['result_raw_sha256']!=sha(J/(name+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest() or r['report_sha256']!=sha(J/(name+'_RESULT.md')):raise RuntimeError('parent result/canonical/report: '+name)
    if p['failed']!=0 or r['failed']!=0 or p['passed']!=r['passed'] or p['input_sha256']!=r['input_sha256'] or len(p['checks'])!=p['passed'] or not all(c['passed'] for c in p['checks']):raise RuntimeError('parent arithmetic: '+name)
    if a['audit_status']!='PASS' or a['failed_assertions']!=0:raise RuntimeError('parent audit status: '+name)
    if frames==416:
        if a['result_raw_sha256']!=r['result_raw_sha256'] or a['receipt_sha256']!=sha(J/(name+'_RECEIPT.json')) or a['audited_preparations']!=104 or a['audited_tagged_frames']!=416 or a['audited_paired_reference_frames']!=416:raise RuntimeError('tagged audit identity/census')
    else:
        if a['preparations']!=104 or a['frames']!=1352:raise RuntimeError('release audit census')
        for suffix in ('_RESULT.json','_RECEIPT.json'):
            k=str((J/(name+suffix)).relative_to(ROOT))
            if a['input_sha256'][k]!=sha(ROOT/k):raise RuntimeError('release audit parent identity')
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cmap=r['checkpoint_sha256']
    if len(cmap)!=count or {f.name for f in cp.iterdir() if f.name!='journal.jsonl'}!=set(cmap):raise RuntimeError('parent checkpoint census: '+name)
    for f,h in cmap.items():register(cp/f,h)
    jb=(cp/'journal.jsonl').read_bytes();lines=jb.splitlines();es=[json.loads(x) for x in lines]
    if len(es)!=count+3 or hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256']:raise RuntimeError('parent journal prefix: '+name)
    expected_report={'event':'report_saved','sha256':r['report_sha256'],('paired_data_rows' if frames==416 else 'data_rows'):frames}
    if es[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} or es[-2]!=expected_report or es[-1]!={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))}:raise RuntimeError('parent final commits: '+name)
    m=read(cp/'manifest.json');mh=sha(cp/'manifest.json')
    if mh!=p['manifest_sha256'] or mh!=es[0]['manifest_sha256'] or m['input_sha256']!=r['input_sha256'] or es[0]['input_sha256']!=r['input_sha256'] or m['PID']!=r['original_manifest_PID'] or es[0]['PID']!=m['PID']:raise RuntimeError('parent manifest/start: '+name)
    commits={'manifest.json':mh}
    for e in es[1:-3]:
        if 'file' not in e or 'sha256' not in e or e['file'] in commits:raise RuntimeError('parent unique commit: '+name)
        commits[e['file']]=e['sha256']
    if commits!=cmap or len(p['preparations'])!=104:raise RuntimeError('parent committed map: '+name)
    register(cp/'journal.jsonl',sha(cp/'journal.jsonl'))
    return cmap

def authenticate():
    if sha(J/(NAME+'.md'))!=PROTOCOL_SHA:raise RuntimeError('unfrozen protocol')
    anchors=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',(J/(NAME+'.md')).read_text(),re.M)
    if len(anchors)!=17:raise RuntimeError('required17 direct inputs')
    for f,h in anchors:register(J/f,h)
    lawpins=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',(J/LAW).read_text(),re.M)
    if len(lawpins)!=15:raise RuntimeError('law15 ancestry inputs')
    for f,h in lawpins:register(J/f,h)
    register(J/(NAME+'.md'),PROTOCOL_SHA);register(Path(__file__).resolve(),sha(__file__))
    maps=[authenticate_parent(*p) for p in PACKETS]
    for mi,(stem,f) in enumerate(((PACKETS[0][1],'reaction_eigensystems.npz'),(PACKETS[1][1],'release_eigensystems.npz'))):
        cp=J/(stem+'_checkpoints');es=[json.loads(x) for x in (cp/'journal.jsonl').read_text().splitlines()]
        if [e for e in es if e.get('file')==f]!=[{'event':'eigensystems_saved','file':f,'sha256':maps[mi][f]}]:raise RuntimeError('unique matrix-bundle commit')

def literal(two):
    labels=PAIRS if two else tuple((a,) for a in range(8));ind={a:i for i,a in enumerate(labels)};d=len(labels)
    hop=np.zeros((d,d));anchor=np.zeros((d,d));cut=np.zeros(d);adj=np.zeros(d)
    for k,pos in enumerate(labels):
        occ=set(pos);cut[k]=int((0 in occ)!=(4 in occ))
        if two:adj[k]=any(occ=={u,v} for u,v in EDGES)
        for u,v in EDGES:
            for particle,a in enumerate(pos):
                dest=v if a==u else (u if a==v else None)
                if dest is not None and dest not in occ:
                    new=list(pos);new[particle]=dest;row=ind[tuple(new)];hop[row,k]=1
                    if {u,v}=={0,4}:anchor[row,k]=1
    eye=np.eye(d);ho=(11 if two else 9.5)*eye-T*hop-2*JC*np.diag(adj)
    he=ho+2*eye-JC*np.diag(cut)+T*anchor
    return labels,ho,he

def factor(name,a):
    gate(name+'_Hermitian',a,a.conj().T)
    try:l=np.linalg.cholesky(a);exact(name+'_positive_Cholesky',True);gate(name+'_factor_residual',l@l.conj().T,a);return l,True
    except np.linalg.LinAlgError:
        exact(name+'_positive_Cholesky',False);return np.zeros_like(a),False

def comm(a,b):return a@b-b@a

def entries(a,labels):
    coordinate={v:k for k,v in enumerate(CYCLE)}
    def steps(x,y):
        m=abs(coordinate[x]-coordinate[y]);return min(m,8-m)
    return {'labels':labels,'diagonal':np.diag(a),'offdiagonal_upper_all':[{'i':i,'j':j,'value':a[i,j],
        'supplied_cycle_steps_per_tag':[steps(x,y) for x,y in zip(labels[i],labels[j])]} for i in range(len(a)) for j in range(i+1,len(a))]}

def summary(a):
    off=a[~np.eye(len(a),dtype=bool)]
    return {'Frobenius_norm':float(np.linalg.norm(a,'fro')),'infinity_norm':float(np.linalg.norm(a,np.inf)),
            'diagonal_min':float(np.min(np.diag(a))),'diagonal_max':float(np.max(np.diag(a))),
            'offdiagonal_min':float(np.min(off)),'offdiagonal_max':float(np.max(off))}

def row(sector,s,mat,evals,vecs,labels,ho,he,z,gap0):
    start=len(CHECKS);d=len(ho);eye=np.eye(d);zero=np.zeros_like(eye);hes=he+LAM*s*eye
    full=np.block([[hes,-H*eye],[-H*eye,ho]])
    gate(sector+str(s)+'_literal_full',full,mat)
    gate(sector+str(s)+'_all_saved_modes',mat@vecs,vecs*evals[None,:]);gate(sector+str(s)+'_basis',vecs.T@vecs,np.eye(2*d))
    gate(sector+str(s)+'_matrix_Hermitian',mat,mat.T);exact(sector+str(s)+'_simple_saved_ground',evals[1]>evals[0])
    exact(sector+str(s)+'_complete_saved_spectrum_order',bool(np.all(np.isfinite(evals)) and np.all(np.diff(evals)>=0)))
    r=np.linalg.solve(z*eye-hes,eye);sigma=H*H*r;sigmaz=-H*H*r@r;metric=eye-sigmaz
    gap=gap0+LAM*s
    cf0,p0=factor('negative_Sigma',-sigma);cf1,p1=factor('negative_Sigma_z',-sigmaz);cf2,p2=factor('norm_metric',metric)
    factor('empty_gap_bound',hes-(z+gap)*eye+TOL*eye)
    gate('real_inverse_residual',(z*eye-hes)@r,eye);gate('norm_metric_identity',metric,eye+H*H*r.T@r)
    exact('Sigma_Frobenius_ceiling',np.linalg.norm(sigma,'fro')<=math.sqrt(d)*H*H/gap+TOL)
    exact('Sigma_z_Frobenius_ceiling',np.linalg.norm(sigmaz,'fro')<=math.sqrt(d)*H*H/gap**2+TOL)
    m=z*np.eye(2*d)-mat;schur=z*eye-ho-sigma
    gate('all_occupied_Schur_columns',m@np.vstack((-H*r,eye)),np.vstack((zero,schur)))
    left=np.block([[eye,zero],[H*r,eye]]);middle=np.block([[z*eye-hes,zero],[zero,schur]]);right=np.block([[eye,H*r],[zero,eye]])
    gate('full_LDU',left@middle@right,m)
    zc=z+1j*H;rc=np.linalg.solve(zc*eye-hes,eye);sc=zc*eye-ho-H*H*rc;goo=np.linalg.solve(sc,eye)
    gc=np.block([[rc+H*H*rc@goo@rc,-H*rc@goo],[-H*goo@rc,goo]])
    direct=np.linalg.solve(zc*np.eye(2*d)-mat,np.eye(2*d))
    gate('complex_full_G_comparison',gc,direct);gate('complex_full_G_residual',(zc*np.eye(2*d)-mat)@gc,np.eye(2*d))
    n=np.block([[zero,zero],[zero,eye]]);htheta=1j*comm(n,mat);hcontact=-comm(n,comm(n,mat))
    gate('phase_first_native_vertex',htheta,np.block([[zero,1j*H*eye],[-1j*H*eye,zero]]))
    gate('phase_second_direct_contact',hcontact,np.block([[zero,H*eye],[H*eye,zero]]))
    gd1=gc@htheta@gc;gd2=gc@hcontact@gc+2*gc@htheta@gc@htheta@gc
    gate('phase_first_resolvent_Ward',gd1,1j*comm(n,gc));gate('phase_second_resolvent_Ward',gd2,-comm(n,comm(n,gc)))
    gate('occupied_phase_first_null',gd1[d:,d:]);gate('occupied_phase_second_null',gd2[d:,d:])
    e0=float(evals[0]);v=vecs[:,0];empty=v[:d];occupied=v[d:]
    exact('saved_ground_below_empty_bound',e0<z+gap);rp=np.linalg.solve(e0*eye-hes,eye)
    pole_sigma=H*H*rp;pole_sigmaz=-H*H*rp@rp;pole_metric=eye-pole_sigmaz
    gate('saved_pole_empty_reconstruction',empty,-H*rp@occupied)
    gate('saved_pole_empty_norm',np.vdot(empty,empty),np.vdot(occupied,-pole_sigmaz@occupied),1e-9)
    gate('saved_pole_complete_norm',np.vdot(occupied,pole_metric@occupied),1.,1e-9)
    npz=sector+'_s%d.npz'%s;js=sector+'_s%d.json'%s
    nh=commit_npz(CP/npz,R=r,Sigma=sigma,Sigma_z=sigmaz,norm_metric=metric,negative_Sigma_factor=cf0,
        negative_Sigma_z_factor=cf1,norm_metric_factor=cf2,Schur=schur,complex_R=rc,complex_Schur=sc,
        complex_G=gc,complex_G_direct=direct,complex_G_theta=gd1,complex_G_thetatheta=gd2,
        pole_R=rp,pole_Sigma=pole_sigma,pole_Sigma_z=pole_sigmaz,pole_norm_metric=pole_metric,
        saved_ground_vector=v,saved_matrix=mat,labels=np.array(labels,dtype=np.int64))
    out={'sector':sector,'s':s,'zbar':z,'complex_zbar':[z,H],'carrier_dimension':d,'gap_bound':gap,
         'operator_ceiling':H*H/gap,'Sigma_z_operator_ceiling':H*H/gap**2,'summary':summary(sigma),
         'signed_Sigma_entries':entries(sigma,labels),'saved_base_ground_energy':e0,'saved_ground_empty_probability':float(np.vdot(empty,empty).real),
         'positive_factor_available':[p0,p1,p2],'operators_file':npz,'operators_sha256':nh,
         'input_map_sha256':input_id(),'checks':CHECKS[start:]}
    commit(CP/js,out,'row_saved');out['row_file']=js
    return out,r,sigma

def main():
    global STARTED,ACTIVE
    started=time.monotonic()
    if sys.argv[1:]!=['--execute']:raise RuntimeError('root-only exact --execute required')
    if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise RuntimeError('reserved output exists; no retry/overwrite')
    authenticate();CP.mkdir();STARTED=True
    manifest={'PID':os.getpid(),'Python':sys.version,'NumPy':np.__version__,'threads':1,'input_sha256':INPUTS,
              'parameters':{'s':[0,1,2],'real_zbar':{'reference':9.5,'tagged':11},'complex_imaginary':H,'h':H,'t':T,'j':JC,'lambda':LAM,'tolerance':TOL}}
    mh=write_json(CP/'manifest.json',manifest);COMMITS['manifest.json']=mh
    event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':INPUTS})
    with np.load(J/(PACKETS[0][1]+'_checkpoints')/'reaction_eigensystems.npz',allow_pickle=False) as f:
        data={k:f[k].copy() for k in f.files}
    with np.load(J/(PACKETS[1][1]+'_checkpoints')/'release_eigensystems.npz',allow_pickle=False) as f:
        release={k:f[k].copy() for k in f.files}
    gate('saved_global_cycle',data['cycle_global_nodes'],np.array(CYCLE));gate('saved_ordered_pairs',data['ordered_tagged_pairs'],np.array(PAIRS))
    for suffix in ('matrices','eigenvalues','eigenvectors'):
        gate('separately_owned_reference_'+suffix,data['reference_base_'+suffix],release['base_'+suffix])
    rows=[];differences=[];ground={}
    for sector,two,z,gap0 in (('reference',False,9.5,1.65),('tagged',True,11.,1.)):
        ACTIVE={'sector':sector};labels,ho,he=literal(two);rs=[];sigmas=[]
        matrices=data[sector+'_base_matrices'];ev=data[sector+'_base_eigenvalues'];vs=data[sector+'_base_eigenvectors']
        exact(sector+'_full_census_shapes',matrices.shape==(3,2*len(ho),2*len(ho)) and ev.shape==(3,2*len(ho)) and vs.shape==matrices.shape)
        for s in range(3):
            ACTIVE={'sector':sector,'s':s};out,r,sig=row(sector,s,matrices[s],ev[s],vs[s],labels,ho,he,z,gap0)
            rows.append(out);rs.append(r);sigmas.append(sig);ground[sector,s]=(out['saved_base_ground_energy'],out['saved_ground_empty_probability'])
        ds=[];arrays={};start=len(CHECKS)
        for i,k in ((0,1),(0,2),(1,2)):
            a=sigmas[k]-sigmas[i];analytic=LAM*(k-i)*H*H*rs[k]@rs[i]
            gate(sector+'_record_increment_%d_%d'%(i,k),a,analytic);l,ok=factor(sector+'_record_increment_positive_%d_%d'%(i,k),a)
            bound=LAM*(k-i)*H*H/((gap0+LAM*k)*(gap0+LAM*i));exact('increment_Frobenius_ceiling',np.linalg.norm(a,'fro')<=math.sqrt(len(ho))*bound+TOL)
            arrays['increment_%d_%d'%(i,k)]=a;arrays['increment_factor_%d_%d'%(i,k)]=l
            ds.append({'from_s':i,'to_s':k,'operator_ceiling':bound,'positive_factor_available':ok,'summary':summary(a),'signed_entries':entries(a,labels)})
        nf=sector+'_all_record_differences.npz';nh=commit_npz(CP/nf,**arrays)
        diff={'sector':sector,'all_three_record_differences':ds,'operators_file':nf,'operators_sha256':nh,'input_map_sha256':input_id(),'checks':CHECKS[start:]}
        jf=sector+'_all_record_differences.json';commit(CP/jf,diff,'differences_saved');diff['row_file']=jf;differences.append(diff)
    binding=[]
    for s in range(3):
        u=LAM*s;disc=math.sqrt((2+u)**2+4*H*H);e0=8+(2+u-disc)/2;p0=(1-(2+u)/disc)/2
        e1,p1=ground['reference',s];e2,p2=ground['tagged',s];b=e2-2*e1+e0
        binding.append({'s':s,'u_lambda_s':u,'E0_min_without_common_ARpop':e0,'E1_min_without_common_ARpop':e1,
                        'E2_min_without_common_ARpop':e2,'B_s':b,'Delta_B_s':b-(binding[0]['B_s'] if binding else b),
                        'empty_probability_0':p0,'empty_probability_1':p1,'empty_probability_2':p2,'loading_slope_dB_du':p2-2*p1+p0})
        exact('binding_row_finite_'+str(s),all(math.isfinite(float(v)) for v in binding[-1].values()))
        gate('common_ARpop_cancels_'+str(s),(e2+.25*s)-2*(e1+.25*s)+(e0+.25*s),b,1e-9)
    exact('six_resolvent_two_difference_three_binding_census',len(rows)==6 and len(differences)==2 and len(binding)==3)
    commit(CP/'all_binding_outcomes.json',{'binding':binding,'scope':'same clamped-q spectral addition curvature; signs never gated','input_map_sha256':input_id()},'binding_saved')
    recheck();failed=sum(not c['passed'] for c in CHECKS);status='QUALIFIED_ARITHMETIC' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'PID':os.getpid(),'passed':len(CHECKS)-failed,'failed':failed,'checks':CHECKS,
            'input_sha256':INPUTS,'manifest_sha256':mh,'rows':rows,'record_differences':differences,'binding':binding,
            'elapsed_seconds':time.monotonic()-started,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'complete finite supplied-C8 Schur operators and clamped-record equilibrium additions; not actual mature trajectories, gravity or a physical metric'}
    raw=write_json(RESULT,result);canonical=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# C8 record interaction resolvent V001','',status+'. Arithmetic controls %d/%d; failed %d.'%(result['passed'],len(CHECKS),failed),'',
           'All six rows, all signed operators and all three record differences per carrier sector are retained in the committed JSON/NPZ. Real full inverses were not taken. The common ARpop shift remains source energy.','',
           '| Sector | s | zbar | Sigma diagonal range | Sigma offdiagonal range | Frobenius norm | Analytical operator ceiling |','|---|---:|---:|---|---|---:|---:|']
    for r in rows:
        v=r['summary'];lines.append('| %s | %d | %.8g | [%+.12g,%+.12g] | [%+.12g,%+.12g] | %.12g | %.12g |'%(r['sector'],r['s'],r['zbar'],v['diagonal_min'],v['diagonal_max'],v['offdiagonal_min'],v['offdiagonal_max'],v['Frobenius_norm'],r['operator_ceiling']))
    lines+=['','| Sector | Loading increment | Signed diagonal range | Signed offdiagonal range | Frobenius norm | Operator ceiling |','|---|---|---|---|---:|---:|']
    for d in differences:
        for r in d['all_three_record_differences']:
            v=r['summary'];lines.append('| %s | %d to %d | [%+.12g,%+.12g] | [%+.12g,%+.12g] | %.12g | %.12g |'%(d['sector'],r['from_s'],r['to_s'],v['diagonal_min'],v['diagonal_max'],v['offdiagonal_min'],v['offdiagonal_max'],v['Frobenius_norm'],r['operator_ceiling']))
    lines+=['','| s | E0 | E1 | E2 | B_s | B_s minus B_0 | dB/du |','|---:|---:|---:|---:|---:|---:|---:|']
    for b in binding:lines.append('| %d | %.12g | %.12g | %.12g | %+.12g | %+.12g | %+.12g |'%(b['s'],b['E0_min_without_common_ARpop'],b['E1_min_without_common_ARpop'],b['E2_min_without_common_ARpop'],b['B_s'],b['Delta_B_s'],b['loading_slope_dB_du']))
    lines+=['','B_0 retains the direct interaction. Loading increments and slopes are not sign selected. B_s is clamped-q equilibrium addition curvature, not a mature prepared-state reaction or gravity. The negative virtual shift becomes less negative with record loading at the fixed subthreshold arguments. Pole normalization is not a physical metric.']
    if len(rows)!=6 or len(binding)!=3:raise RuntimeError('report census')
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'resolvent_rows':6,'difference_rows':6,'binding_rows':3})
    recheck();receipt={'status':status,'PID':os.getpid(),'input_sha256':INPUTS,'checkpoint_sha256':COMMITS,
        'result_raw_sha256':raw,'result_canonical_sha256':canonical,'report_sha256':rh,'passed':result['passed'],'failed':failed,
        'journal_prefix_sha256':sha(CP/'journal.jsonl'),'elapsed_seconds':time.monotonic()-started,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    rr=write_json(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr})
    print(json.dumps({'status':status,'passed':result['passed'],'failed':failed,'raw_sha256':raw,'receipt_sha256':rr,'elapsed_seconds':receipt['elapsed_seconds']}))
    return 0 if failed==0 else 3

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:
        info={'status':'EXECUTION_ERROR_PRESERVED','PID':os.getpid(),'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),
              'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'committed_checkpoint_sha256':COMMITS}
        if not ERROR.exists():write_json(ERROR,info)
        if STARTED:event({'event':'error','sha256':sha(ERROR),'error_type':type(e).__name__})
        print(str(e),file=sys.stderr);sys.exit(3)
