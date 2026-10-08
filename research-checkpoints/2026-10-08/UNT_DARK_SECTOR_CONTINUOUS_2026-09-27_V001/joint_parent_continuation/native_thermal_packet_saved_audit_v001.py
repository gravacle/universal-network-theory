"""Saved native vectors/arrays and static-operator arithmetic only; no evolution/eigensolver."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={};manifests=set();occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True);p.relative_to(ROOT);d=sha(p);assert digest is None or d==digest
    files[str(p.relative_to(ROOT))]=d;return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,d in json.loads(p.read_text())['files'].items():
        raw=Path(name);opts=[raw] if raw.is_absolute() else [ROOT/raw,p.parent/raw]
        matches={q.resolve() for q in opts if q.is_file() and q.resolve().is_relative_to(ROOT)}
        assert len(matches)==1;m=member(matches.pop(),d);occurrences+=1
        if m.name.endswith('_FROZEN.json'):manifest(m)
rp=member(HERE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json');fr=member(HERE/'NATIVE_THERMAL_PACKET_V001_FROZEN.json');manifest(fr)
wr=json.loads(rp.read_text());p=wr['payload'];assert wr['freeze_sha256']==sha(fr) and wr['payload_sha256']==hashlib.sha256(enc(p)).hexdigest()
counts={};maxima={};failures=[]
def ck(name,a,b=0,scale=1,tol=2e-10):
    er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300);mx=float(np.max(er))
    counts[name]=counts.get(name,0)+int(er.size);maxima[name]=max(maxima.get(name,0.),mx)
    if not np.all(np.isfinite(er)) or mx>tol:failures.append(dict(check=name,error=mx,tolerance=tol))
def yes(name,x):ck(name,int(bool(x)),1,tol=0)
def z(x):return np.array(x['real'])+1j*np.array(x['imag'])
def comm(a,b):return a@b-b@a
def static(q):
    # Direct basis-row construction, no spectral functions or producer import.
    edges=[(0,2),(0,3),(1,2),(1,3)];hv=np.zeros((4,64,64),complex);ns=np.zeros((4,64,64));ps=np.zeros((4,64,64));cc=np.zeros((4,64,64),complex)
    for mask in range(16):
        bits=[(mask>>e)&1 for e in range(4)];deg=[sum(bits[e] for e,uv in enumerate(edges) if v in uv) for v in range(4)]
        for carrier in range(4):
            col=4*mask+carrier;ps[carrier,col,col]=1
            for v in range(4):
                hv[v,col,col]=(deg[v]-1)**2+(carrier==v)+q
                for e,uv in enumerate(edges):
                    if v in uv:
                        hv[v,col,col]+=2*bits[e]+.25*bits[e]*(carrier==v)-.5*q*bits[e]
                        hv[v,4*(mask^(1<<e))+carrier,col]-=.25
                        if bits[e] and carrier in uv:
                            other=uv[1] if carrier==uv[0] else uv[0]
                            hv[v,4*mask+other,col]-=.25
            for e,(a,b) in enumerate(edges):
                ns[e,col,col]=bits[e]
                if bits[e] and carrier in (a,b):
                    other=b if carrier==a else a
                    cc[e,4*mask+other,col]=.5j*(1 if carrier==a else -1)
    H=sum(hv);pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
    cur=np.array([1j*comm(hv[a],hv[b]) for a,b in pairs]);obs=np.concatenate((hv,cur))
    return H,hv,cur,ns,ps,cc,obs
def cert(matrix,c,name):
    ck(name+'_Hermitian',matrix,matrix.conj().T)
    ev=np.asarray(c['eigenvalues']);tr=float(np.trace(matrix).real);scale=max(1,tr)
    ck(name+'_saved_trace',sum(ev),tr,scale)
    ck(name+'_saved_Frobenius',sum(ev*ev),float(np.sum(abs(matrix)**2)),max(1,float(np.sum(abs(matrix)**2))))
    ck(name+'_trace_scale',c['trace_scale'],scale,scale)
    ck(name+'_negative_certificate',c['negative_eigenvalue_absolute'],max(0,-ev.min()))
    yes(name+'_PSD_saved_gate',max(0,-ev.min())/scale<=1e-10)
    schwarz=abs(matrix)**2-np.outer(np.diag(matrix).real,np.diag(matrix).real)
    yes(name+'_Schwarz',np.max(schwarz)/scale**2<=1e-10)
yes('result_status',wr['status']=='COMPLETE' and not p['failures'])
yes('census',p['census']==dict(states=4,holds=44,retarded_blocks=264,probe_grams=216))
times=p['config']['times'];summaries=[];holds={};probes={};twotime={};producer_checks=0
for sector in p['sectors']:
    q=sector['record_occupation'];yes('sector_status',sector['status']=='COMPLETE' and not sector['failures'])
    producer_checks+=sum(sector['check_counts'].values())
    H,hv,cur,ns,ps,cc,obs=static(q);val=np.asarray(sector['energy_eigenvalues'])
    ck('spectrum_trace',val.sum(),np.trace(H).real,max(1,abs(np.trace(H).real)))
    ck('spectrum_square',val@val,np.sum(abs(H)**2),np.sum(abs(H)**2))
    ck('spectrum_cube',np.sum(val**3),np.trace(H@H@H).real,max(1,abs(np.trace(H@H@H).real)))
    groupindices=[i for g in sector['energy_groups'] for i in g['indices']]
    yes('group_partition',sorted(groupindices)==list(range(64)) and len(groupindices)==64)
    for g in sector['energy_groups']:ck('group_energy',val[g['indices']],g['energy'],tol=1e-10)
    incidence=np.asarray(sector['energy_current_incidence'])
    for h in sector['holds']:
        name,age=h['preparation'],h['age'];holds[(q,name,age)]=h;psi=z(h['state_vector'])
        norm=float(np.vdot(psi,psi).real);opv=(obs@psi).T;means=psi.conj()@opv;energy=float(np.vdot(psi,H@psi).real)
        ck('norm',h['norm'],norm);ck('normalized_state',norm,1)
        ck('all_observable_means',h['node_energy']+h['energy_current'],means)
        ck('absolute_energy',h['energy'],energy,tol=2e-8)
        expected=(21.5 if name=='cycle' else 15.5+q)
        ck('held_energy',energy,expected,tol=2e-8)
        ck('variance',h['energy_variance'],np.vdot(H@psi,H@psi).real-energy**2,tol=2e-8)
        ck('fixed_variance',h['energy_variance'],1.5,tol=2e-8)
        cov=opv.conj().T@opv-np.outer(means.conj(),means)
        ck('connected_covariance',z(h['connected_equal_time_covariance']),cov)
        cert(cov,h['covariance_control'],'equal_time')
        deriv=np.array([np.vdot(psi,1j*comm(H,x)@psi).real for x in hv])
        ck('energy_derivative',h['node_energy_derivative'],deriv)
        ck('current_continuity',deriv,incidence@np.asarray(h['energy_current']))
        ck('patch_flux',h['left_patch_flux'],deriv[:2].sum())
        ck('patch_energy',h['left_patch_energy'],sum(h['node_energy'][:2]))
        for label,ops in [('edge_occupation',ns),('carrier_population',ps),('carrier_current',cc)]:
            ck(label,h[label],[(np.vdot(psi,o@psi)).real for o in ops])
        ck('record_storage',h['record_storage_energy'],4*q*norm)
        ck('record_feedback',h['record_feedback_energy'],-q*sum(h['edge_occupation']))
        ck('source_doublecomm',h['incidence_source_moment'],[np.vdot(psi,comm(n,comm(H,n))@psi).real for n in ns])
    for row in sector['two_time']:
        name=row['preparation'];twotime[(q,name)]=row;M=z(row['correlation']);mu=np.array(row['means']);conn=M-np.outer(mu.conj(),mu)
        yes('Gram_shape',M.shape==(110,110) and len(mu)==110)
        cert(M,row['Gram_control'],'two_time');cert(conn,row['connected_Gram_control'],'two_time_connected')
        for ti,t in enumerate(times):
            h=holds[(q,name,t)];mean=np.array(h['node_energy']+h['energy_current'])
            ck('time_means',mu[10*ti:10*(ti+1)],mean)
            ck('equal_time_blocks',conn[10*ti:10*(ti+1),10*ti:10*(ti+1)],z(h['connected_equal_time_covariance']))
        pairs=set()
        for r in row['retarded_blocks']:
            ti,si=r['t_index'],r['s_index'];pairs.add((ti,si));block=M[10*ti:10*(ti+1),10*si:10*(si+1)];chi=-2*block.imag
            ck('retarded_blocks',r['chi'],chi)
            ck('source_work_Ward',chi[:4,:2].sum(),holds[(q,name,times[si])]['left_patch_flux'],tol=2e-8)
            ck('saved_total_source_work',r['total_energy_response_to_left_patch'],chi[:4,:2].sum())
            ck('conserved_covariance',block[:4,:4].sum(),holds[(q,name,times[0])]['initial_energy']**2+1.5,tol=2e-8)
        yes('causal_census',pairs=={(t,s) for t in range(11) for s in range(t+1)})
    for r in sector['probe_grams']:
        key=(q,r['preparation'],r['age'],r['duration'],r['omega'],r['sign']);yes('unique_probe',key not in probes);probes[key]=r
        K=z(r['K']);mean=z(r['mean']);C=z(r['connected_K']);D=z(r['dephased_K'])
        ck('probe_connected',C,K-np.outer(mean.conj(),mean))
        ck('probe_dephased_difference',z(r['coherent_minus_dephased']),K-D)
        cert(K,r['Gram_control'],'probe');cert(C,r['connected_Gram_control'],'probe_connected')
        ck('dephased_Hermitian',D,D.conj().T)
        yes('probe_norm',np.max(np.diag(K).real)<=r['duration']**2+1e-9)
        yes('probe_label',r['label']==('emission' if r['sign']==1 else 'absorption'))
        base=(q,r['preparation'],0.,r['duration'],r['omega'],r['sign'])
        if base in probes:ck('dephased_age_invariance',D,z(probes[base]['dephased_K']))
    for r in sector['stationary_spectra']:
        pop=np.asarray(r['group_population']);ener=np.array([g['energy'] for g in sector['energy_groups']]);name=r['preparation'];betas=[];inverted=0
        ck('stationary_population',sum(pop),1);yes('stationary_population_positive',pop.min()>=0)
        E=holds[(q,name,0.)]['initial_energy'];ck('stationary_energy',pop@ener,E,tol=2e-8)
        ck('stationary_variance',pop@(ener**2)-E**2,1.5,tol=2e-8)
        seen=set();zeroth=np.array(r['elastic_weight']);first=np.zeros(4)
        for line in r['lines']:
            a,b=line['low'],line['high'];seen.add((a,b));gap=ener[b]-ener[a]
            ck('line_gap',line['gap'],gap)
            ab=np.array(line['absorption']);em=np.array(line['emission']);yes('positive_weights',ab.min()>=0 and em.min()>=0)
            zeroth+=ab+em;first+=2*gap*(ab-em)
            for j,(u,v) in enumerate(zip(ab,em)):
                if min(u,v)>1e-12:
                    be=math.log(u/v)/gap;ck('beta_ratio',line['beta_eff'][j],be,max(1,abs(be)));betas.append(be);inverted+=be<0
                else:yes('undefined_beta',line['beta_eff'][j] is None)
        yes('line_census',seen=={(a,b) for a in range(len(ener)) for b in range(a+1,len(ener))})
        yes('projector_zeroth_bound',zeroth.min()>=0 and zeroth.max()<=1+1e-9)
        yes('doublecomm_norm_bound',np.max(abs(first))<=.5+1e-9)
        hh=[holds[(q,name,t)] for t in times]
        pp=[v for k,v in probes.items() if k[:2]==(q,name)]
        summaries.append(dict(q=q,preparation=name,initial_energy=E,patch_energy=[h['left_patch_energy'] for h in hh],
            patch_flux=[h['left_patch_flux'] for h in hh],max_abs_energy_current=max(max(abs(x) for x in h['energy_current']) for h in hh),
            max_abs_probe_offdiagonal=max(float(np.max(np.abs(z(x['connected_K'])-np.diag(np.diag(z(x['connected_K'])))))) for x in pp),
            max_coherent_dephased_difference=max(float(np.max(abs(z(x['coherent_minus_dephased'])))) for x in pp),
            stationary_beta_range=[min(betas),max(betas)] if betas else None,defined_beta_count=len(betas),inverted_beta_count=int(inverted),
            stationary_zeroth=zeroth.tolist(),stationary_first_doublecomm=first.tolist()))
yes('total_holds',len(holds)==44);yes('total_probes',len(probes)==216)
contrasts={}
for name in ('cycle','tree'):
    table=[]
    for age in times:
        a,b=holds[(0,name,age)],holds[(1,name,age)]
        table.append(dict(age=age,patch_energy_q0=a['left_patch_energy'],patch_energy_q1=b['left_patch_energy'],
            delta_patch=b['left_patch_energy']-a['left_patch_energy'],delta_flux=b['left_patch_flux']-a['left_patch_flux'],
            max_abs_current_difference=float(np.max(abs(np.array(b['energy_current'])-a['energy_current'])))))
    diffs=[]
    for key,r in probes.items():
        if key[:2]==(0,name):
            rr=probes[(1,)+key[1:]]
            diffs.append(dict(age=key[2],duration=key[3],omega=key[4],sign=key[5],
                max_K_difference=float(np.max(abs(z(rr['K'])-z(r['K'])))),
                max_connected_difference=float(np.max(abs(z(rr['connected_K'])-z(r['connected_K']))))))
    contrasts[name]=dict(hold_contrasts=table,probe_contrasts=diffs,
        max_probe_difference=max(d['max_K_difference'] for d in diffs),max_connected_probe_difference=max(d['max_connected_difference'] for d in diffs))
receipt=dict(status='PASS_SAVED_ARITHMETIC' if not failures else 'FAILED',scope='Static matrix reconstruction and saved arrays only. No native propagation, eigensolve, time integration or producer import. Saved Gram eigenvalue certificates checked by moments, not independently diagonalized; full two-time/probe matrices checked internally, not repropagated.',
    files=files,unique_files=len(files),recursive_manifests=len(manifests),manifest_member_occurrences=occurrences,
    checks=counts,maxima=maxima,failures=failures,total_checks=sum(counts.values()),producer_checks=producer_checks,
    producer_seconds=p['elapsed_seconds'],producer_peak_self_rss_bytes=max(s['peak_self_rss_bytes'] for s in p['sectors']),summaries=summaries,record_contrasts=contrasts)
print(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False))
