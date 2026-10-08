"""Saved-array/algebra audit only. No producer import, quadrature, or evolution."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def encode(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files={}; manifests=set(); occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True); p.relative_to(ROOT); h=sha(p)
    assert digest is None or h==digest
    files[str(p.relative_to(ROOT))]=h
    return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,h in json.loads(p.read_text())['files'].items():
        n=Path(name);opts=[n] if n.is_absolute() else [ROOT/n,p.parent/n]
        hits={x.resolve() for x in opts if x.is_file() and x.resolve().is_relative_to(ROOT)}
        assert len(hits)==1
        q=member(hits.pop(),h);occurrences+=1
        if q.name.endswith('_FROZEN.json'):manifest(q)
def packet(p,freeze=None):
    p=member(p);w=json.loads(p.read_text())
    assert hashlib.sha256(encode(w['payload'])).hexdigest()==w['payload_sha256']
    if freeze is not None:assert w['freeze_sha256']==sha(freeze)
    return w['payload']

fr=member(HERE/'FINITE_SLICE_GROWTH_TRANSFER_V001_FROZEN.json');manifest(fr)
rp=member(HERE/'FINITE_SLICE_GROWTH_TRANSFER_V001_BENCHMARK.json')
p=packet(rp,fr);cfg=p['configuration'];labels=p['observable_labels']
counts={};maxima={};failures=[]
def ck(name,a,b=0,scale=1,tol=2e-10):
    e=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
    v=float(np.max(e));counts[name]=counts.get(name,0)+int(e.size)
    maxima[name]=max(maxima.get(name,0.),v)
    if not np.all(np.isfinite(e)) or v>tol:failures.append(dict(check=name,error=v,tolerance=tol))
def yes(name,x):ck(name,int(bool(x)),1,tol=0)
yes('status',p['status']=='COMPLETE_BENCHMARK_ONLY' and p['benchmark_only'] and not p['failures'])
yes('configuration_frozen',cfg==json.loads(fr.read_text())['configuration'])
prior=HERE/'FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json'
rows=[]
for i in range(5):
    old=packet(HERE/f'FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{i}.json',prior)
    yes('background_status',old['status']=='COMPLETE_BACKGROUND_SUBSET' and not old['failures'])
    rows.extend(old['records'])
yes('complete_input_census',len(rows)==335 and p['expected_full_history_count']==335)
yes('inherited_source_record',p['source_record']==rows[p['case_index']])
yes('first_finite_benchmark',p['case_index']==next(i for i,r in enumerate(rows) if r['finite_gap']))
expected=[dict(case_index=i,background_id=r['background_id'],point_id=r['point_id'],finite_gap=r['finite_gap']) for i,r in enumerate(rows)]
yes('history_labels',p['history_census']==expected)
yes('mechanical_copy_census',len(p['mechanical_label_mapping'])==4 and sorted(r['spectrum_index'] for r in p['mechanical_label_mapping'])==list(range(4)))
yes('two_columns',p['basis_columns']==[[1.,0.],[0.,1.]])
yes('four_wavenumbers',[r['k_Mpc_inverse'] for r in p['results']]==cfg['k_Mpc_inverse'])
small=[0,1,2,3,4,5,6,10,11,12,13,15,16,17,18]
all_runs=[];phase_errors=[];sample_constraint_errors=[];eds_errors=[]

def runcheck(run,K,row,bg,dust=False,eds=False):
    all_runs.append(run);samples=run['samples'];n=run['angle_order']
    yes('sample_census',len(samples)==10)
    ys=np.asarray(run['initial_state']);yes('initial_full_shape',ys.shape==(1+2*(6+2*n),))
    ck('initial_eta',ys[0],0,tol=0)
    q=ys[1:].reshape(2,6+2*n)
    omr=0 if eds else row['Omega_ordinary_radiation']
    vals=np.asarray([s['values'] for s in samples]);yes('sample_shape',vals.shape==(10,2,21))
    ck('epochs',[s['A'] for s in samples],cfg['A_outputs'],cfg['A_outputs'])
    yes('monotone_coordinates',all(samples[j+1]['x']>samples[j]['x'] and samples[j+1]['eta_bar']>samples[j]['eta_bar'] for j in range(9)))
    for j,s in enumerate(samples):
        A,H,w=s['A'],s['H_over_Hcal'],s['w'];h=H/A;v=np.asarray(s['values'])
        eb=1.5*row['Omega_b']*A;er=1.5*omr*A*A
        eh=1.5*row['Omega_exc']*A if dust else 1.5*(H*H-row['Omega_b']*A**3-bg['Omega_Lambda']-omr*A**4)/A**2
        yes('physical_background',H>0 and 0<=w<=1/3 and 0<=s['cI2']<=1/3 and eh>0)
        ck('Weyl',v[:,2],(v[:,0]+v[:,1])/2)
        ck('slip',v[:,3],v[:,0]-v[:,1])
        ck('shear_slip',v[:,0]-v[:,1],-4*er*v[:,13]/K**2)
        ck('hard_comoving_density',v[:,10],v[:,4]+3*h*(1+w)*v[:,7]/K**2,np.maximum(1,abs(v[:,10])))
        ck('baryon_comoving_density',v[:,11],v[:,5]+3*h*v[:,8]/K**2,np.maximum(1,abs(v[:,11])))
        ck('radiation_comoving_density',v[:,12],v[:,6]+4*h*v[:,9]/K**2,np.maximum(1,abs(v[:,12])))
        ck('physical_clock_tilt',v[:,15],K*A*v[:,14],np.maximum(1,abs(v[:,15])))
        ck('physical_velocities',v[:,16:19],v[:,7:10]/K,np.maximum(1,abs(v[:,16:19])))
        U=(eh*(1+w)*v[:,7]+eb*v[:,8]+4*er*v[:,9]/3)/K**2
        terms=np.array([K*K*v[:,1],3*h*U,eh*v[:,4],eb*v[:,5],er*v[:,6]])
        norm=np.maximum(1,np.sum(abs(terms),axis=0));res=np.sum(terms,axis=0)
        ck('Hamiltonian_saved_raw',v[:,19],res,norm)
        ck('Hamiltonian_saved_normalization',v[:,20],res/norm)
        sample_constraint_errors.append(float(max(abs(res/norm))))
        yes('accepted_constraint_dominates_samples',max(abs(v[:,20]))<=run['accepted_step_Hamiltonian_max']+1e-14)
        pe=abs(K*(s['eta_bar']-s['eta_bar_quadrature']));phase_errors.append(pe)
        ck('saved_conformal_integral_agreement',K*s['eta_bar'],K*s['eta_bar_quadrature'],tol=cfg['phase_integral_tolerance'])
        if dust:
            ck('dust_density_equality',v[:,4],v[:,5],np.maximum(1,abs(v[:,5])),tol=0)
            ck('dust_velocity_equality',v[:,7],v[:,8],np.maximum(1,abs(v[:,8])),tol=0)
        if j==0:
            total=eh*(1+w)+eb+4*er/3
            mus=[]
            for col,(psi,slope) in enumerate(cfg['initial_columns']):
                vel=h*(psi+slope)/total;d=-K*K*psi/total-3*h*vel
                want=[psi,(1+w)*d,K*K*vel,d,K*K*vel,0]
                ck('initial_scalar_vector',q[col,:6],want,np.maximum(1,abs(np.asarray(want))))
                ck('initial_Ehat',q[col,6:6+n],4*d/3+4*psi,max(1,abs(4*d/3+4*psi)))
                mu=-q[col,6+n:]/(4*K*vel);mus.append(mu)
                yes('initial_angular_support',np.all((mu>0)&(mu<1)) and np.all(np.diff(mu)>0))
                ck('initial_angular_symmetry',mu+mu[::-1],1)
                ck('initial_tangent',(U[col]-h*v[col,0])/h,slope)
                ck('initial_radiation_density',v[col,6],4*d/3,max(1,abs(d)))
                ck('initial_common_velocity',v[col,7:10],K*K*vel,max(1,abs(K*K*vel)))
            ck('initial_shared_angles',mus[0],mus[1])
        if eds:
            a=1/A;ai=1/101;want=[]
            ck('EdS_background',H,A**1.5,H)
            for psi0,q0 in cfg['initial_columns']:
                qi=q0*(ai/a)**2.5;psi=psi0+2*q0/5*(1-(ai/a)**2.5)
                theta=2*K*K*(psi+qi)/(3*h)
                de=-2*K*K*psi/(3*h*h)-2*(psi+qi)
                clock=2*(psi0+2*q0/5)*(a**1.5-ai**1.5)/3+2*q0*ai**2.5*(1/a-1/ai)/5
                want.append([psi,de,theta,clock])
            want=np.asarray(want);err=abs(v[:,[1,4,7,14]]-want)/np.maximum(1,abs(want))
            eds_errors.append(float(err.max()));ck('closed_EdS_oracle',err,0,tol=cfg['transfer_tolerance'])
    peak=np.asarray(run['accepted_step_sampled_max_per_column'])
    yes('smallness_labels',run['sampled_smallness_observables']==[labels[i] for i in small])
    yes('accepted_peak_dominates_samples',np.all(peak+1e-12>=np.max(abs(vals[:,:,small]),axis=(0,2))))
    ck('illustrative_linear_amplitude',run['illustrative_amplitude_for_sampled_1percent'],.01/np.maximum(peak,1))
    st=run['statistics'];yes('integrator_metadata',st['accepted_steps']>=9 and st['rejected_steps']>=0 and st['maximum_accepted_embedded_error']<=1 and 0<st['min_step']<=st['max_step']<=cfg['maximum_step']+1e-15)
    return vals

runcheck(p['EdS_control'],5.,dict(Omega_b=.2,Omega_exc=.8),dict(Omega_Lambda=0),dust=True,eds=True)
summaries=[];refines=[[],[]]
for ik,r in enumerate(p['results']):
    K=r['k_Mpc_inverse']*cfg['c_km_s']/p['background']['H0_km_s_Mpc'];ck('wavenumber_units',r['K_dimensionless'],K,K)
    X=K*2*(1-101**(-.5))/math.sqrt(p['background']['Omega_m']);ck('phase_upper_bound',r['maximum_phase_bound'],X,max(1,X))
    for cert in r['angular_kernel_certificates']:
        n=cert['order'];logs=[]
        for d in range(5):
            lc=4*math.lgamma(n+1)-3*math.lgamma(2*n+1)-math.log(2*n+1)
            terms=[math.lgamma(2*n+1)-math.lgamma(j+1)-math.lgamma(2*n-j+1)+math.lgamma(d+1)-math.lgamma(d-j+1)+(2*n-j)*math.log(X) for j in range(d+1)]
            top=max(terms);logs.append(math.log(2)+lc+top+math.log(sum(math.exp(t-top) for t in terms)))
        ck('analytic_angular_log_certificate',cert['monomial_log_bounds'],logs,np.maximum(1,abs(np.array(logs))))
        bound=2*sum(math.exp(t) for t in logs);ck('analytic_angular_bound',cert['combined_bound'],bound)
        yes('angular_certificate_gate',bound<=cfg['angular_kernel_tolerance'])
    primary={}
    for label,branch in r['branches'].items():
        yes('three_resolutions',[rr['tag'] for rr in branch['runs']]==['coarse','tight','primary'])
        aa=[]
        for it,run in enumerate(branch['runs']):
            yes('angle_time_configuration',run['angle_order']==cfg['angle_orders'][ik]*(2 if it==2 else 1) and run['tight']==(it>0))
            aa.append(runcheck(run,K,p['source_record'],p['background'],dust=label=='dust_comparator'))
        for j in range(2):
            b=aa[j+1][:,:,:19];scale=np.maximum(1,np.max(abs(b),axis=0));err=np.max(abs(aa[j][:,:,:19]-b)/scale[None,:,:],axis=0)
            ck('stored_refinement',branch['comparisons'][j]['normalized_max_by_basis_and_observable'],err)
            yes('refinement_gate',err.max()<=cfg['transfer_tolerance']);refines[j].append(float(err.max()))
        primary[label]=aa[2]
    delta=primary['candidate']-primary['dust_comparator'];ck('full_signed_dust_contrast',r['primary_minus_dust_signed'],delta,np.maximum(1,abs(delta)))
    scale=np.maximum(1,np.max(abs(primary['dust_comparator'][:,:,:19]),axis=0))
    normalized=np.max(abs(delta[:,:,:19])/scale[None,:,:],axis=0)
    summaries.append(dict(k_Mpc_inverse=r['k_Mpc_inverse'],maximum_normalized_candidate_dust_difference=float(normalized.max()),normalized_by_basis_observable=normalized.tolist(),final_candidate=primary['candidate'][-1].tolist(),final_dust=primary['dust_comparator'][-1].tolist(),final_signed_difference=delta[-1].tolist()))
ck('global_time_refinement',p['maxima']['time_refinement'],max(refines[0]))
ck('global_angle_refinement',p['maxima']['angle_refinement'],max(refines[1]))
ck('global_constraint_report',p['maxima']['propagated_Hamiltonian'],max(r['accepted_step_Hamiltonian_max'] for r in all_runs))
ck('global_EdS_report',p['maxima']['exact_EdS_metric_density_clock'],max(eds_errors))
yes('producer_control_census',sum(p['counts'].values())==4532 and len(all_runs)==25)
out=dict(status='PASS' if not failures else 'FAIL',scope='Saved-array arithmetic and exact analytic identities only; no producer import, ODE, background/angle quadrature, or new physical prediction.',result_sha256=sha(rp),freeze_sha256=sha(fr),payload_sha256=json.loads(rp.read_text())['payload_sha256'],audit_source_sha256=sha(Path(__file__)),authenticated_unique_files=len(files),authenticated_manifests=len(manifests),manifest_member_occurrences=occurrences,check_counts=counts,maxima=maxima,failures=failures,producer_counts=p['counts'],producer_maxima=p['maxima'],producer_seconds=p['seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],benchmark_case=p['case_index'],background=p['background'],source_point=dict(point_id=p['source_record']['point_id'],Delta=p['source_record']['Delta'],finite_gap=p['source_record']['finite_gap'],inherited_local_BBN_rectangle=p['source_record']['inherited_local_BBN_rectangle']),summaries=summaries,caveats=['Accepted-step global maxima are authenticated reports and checked against retained output samples, not independently reconstructed from unsaved steps.','Initial angular nodes reconstructed from stored initial dipoles; quadrature weights and intermediate full angular states are not regenerated.','Only one of 335 histories is complete in this benchmark. Candidate/dust differences are conditional basis responses, not observational growth or a selected perturbation spectrum.'])
print(json.dumps(out,sort_keys=True,separators=(',',':'),allow_nan=False))
