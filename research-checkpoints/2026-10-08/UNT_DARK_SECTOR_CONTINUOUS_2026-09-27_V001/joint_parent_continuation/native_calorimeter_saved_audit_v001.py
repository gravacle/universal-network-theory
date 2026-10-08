"""Saved calorimeter arrays and algebra only; no producer import or evolution."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={};manifests=set();occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True);p.relative_to(ROOT);h=sha(p);assert digest is None or h==digest
    files[str(p.relative_to(ROOT))]=h;return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,h in json.loads(p.read_text())['files'].items():
        n=Path(name);opts=[n] if n.is_absolute() else [ROOT/n,p.parent/n]
        hits={x.resolve() for x in opts if x.is_file() and x.resolve().is_relative_to(ROOT)}
        assert len(hits)==1;q=member(hits.pop(),h);occurrences+=1
        if q.name.endswith('_FROZEN.json'):manifest(q)
def packet(p,fr):
    p=member(p);w=json.loads(p.read_text());assert w['freeze_sha256']==sha(fr)
    assert w['payload_sha256']==hashlib.sha256(enc(w['payload'])).hexdigest()
    return w
fr=member(HERE/'NATIVE_CALORIMETER_PORTS_V001_FROZEN.json');manifest(fr)
rp=member(HERE/'NATIVE_CALORIMETER_PORTS_V001_RESULTS.json');wr=packet(rp,fr);p=wr['payload'];cfg=p['config']
old=packet(HERE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json',HERE/'NATIVE_THERMAL_PACKET_V001_FROZEN.json')['payload']
counts={};maxima={};failures=[]
def ck(name,a,b=0,scale=1,tol=2e-10):
    er=abs(np.asarray(a)-np.asarray(b))/np.maximum(abs(np.asarray(scale)),1e-300);mx=float(np.max(er))
    counts[name]=counts.get(name,0)+int(er.size);maxima[name]=max(maxima.get(name,0.),mx)
    if not np.all(np.isfinite(er)) or mx>tol:failures.append(dict(check=name,error=mx,tolerance=tol))
def yes(name,x):ck(name,int(bool(x)),1,tol=0)
def z(x):return np.asarray(x['real'])+1j*np.asarray(x['imag'])
def key(r,include_g=True):
    keys=['record_occupation','preparation','age','omega','duration','probe_input']
    return tuple(r[k] for k in keys+(['coupling'] if include_g else []))
yes('status',wr['status']=='COMPLETE' and not p['failures'])
yes('frozen_config',cfg==json.loads(fr.read_text())['config'])
sectors={s['record_occupation']:s for s in old['sectors']}
holds={(q,r['preparation'],r['age']):r for q,s in sectors.items() for r in s['holds']}
grams={(q,r['preparation'],r['age'],r['omega'],r['duration'],r['sign']):r for q,s in sectors.items() for r in s['probe_grams']}
rows={key(r):r for r in p['rows']}
expected=set(itertools.product(cfg['record_occupations'],cfg['native_preparations'],cfg['ages'],cfg['frequencies'],cfg['durations'],cfg['probe_inputs'],cfg['couplings']))
yes('complete_648_census',set(rows)==expected and len(p['rows'])==648)
yes('spectra_census',len(p['spectra'])==12 and len({(s['record_occupation'],s['omega'],s['coupling']) for s in p['spectra']})==12)
methods={(s['record_occupation'],s['omega'],s['coupling'],s['duration']):s for s in p['methods']}
yes('methods_census',len(methods)==36 and len(p['methods'])==36)
specs={(s['record_occupation'],s['omega'],s['coupling']):s for s in p['spectra']}
lower=np.array([[0.,1.],[0.,0.]]);num=lower.T@lower;ident=np.eye(2)
ns=[np.kron(num,ident),np.kron(ident,num)];aa=[np.kron(lower,ident),np.kron(ident,lower)];cross=aa[0].T@aa[1]
def tail(zv,n):
    return n*math.log(zv/2)-math.lgamma(n+1)+zv*zv/(4*(n+1))-math.log1p(-zv/(2*(n+1)))
for s in p['spectra']:
    ev=np.asarray(s['eigenvalues']);ne=np.asarray(sectors[s['record_occupation']]['energy_eigenvalues']);om,g=s['omega'],s['coupling']
    yes('spectrum_shape_order',ev.shape==(256,) and np.all(np.diff(ev)>=0))
    ck('spectrum_trace',sum(ev),4*sum(ne)+256*om,max(1,abs(sum(ev))))
    expected2=4*np.sum(ne**2)+384*om*om+8*om*sum(ne)+256*g*g
    ck('spectrum_square',np.sum(ev**2),expected2,expected2)
    lo,hi=s['gershgorin'];yes('spectrum_enclosure',ev[0]>=lo-2e-11 and ev[-1]<=hi+2e-11)
for k,m in methods.items():
    q,om,g,T=k;sp=specs[k[:3]];lo,hi=sp['gershgorin'];info=m['Chebyshev'];zv=(hi-lo)*T/2;n=info['degree'];M=info['fft_samples']
    ck('Chebyshev_argument',info['z'],zv,max(1,zv))
    yes('Chebyshev_census',len(m['dual_vector_errors'])==18 and M>=max(64,4*(n+1)) and M&(M-1)==0)
    for label,logv in [('truncation',math.log(2)+tail(zv,n+1)),('alias',math.log(4*(n+1))+tail(zv,M-n))]:
        rec=info[label];ck('Chebyshev_log_certificate',rec['log_bound'],logv,max(1,abs(logv)))
        ck('Chebyshev_bound',rec['bound'],math.exp(logv) if logv>-745 else 0)
        yes('Chebyshev_bound_scope',not rec['exact_zero'] and rec['underflow']==(logv<=-745))
    yes('tail_and_dual_gates',info['truncation']['bound']<1e-18 and max(m['dual_vector_errors'])<=cfg['state_tolerance'])

derived_ledger=[];weakmax={};bound_ratios=[];vacuum=[];examples=[]
for r in p['rows']:
    q,name,age,om,T,pinput,g=key(r);rho=z(r['probe_density']);means=z(r['mean_lowering']);occup=np.asarray(r['probe_occupation'])
    ck('rho_Hermitian',rho,rho.conj().T);ck('rho_trace',np.trace(rho),1)
    yes('rho_shape',rho.shape==(4,4))
    for size in range(1,5):
        for ids in itertools.combinations(range(4),size):
            determinant=np.linalg.det(rho[np.ix_(ids,ids)])
            ck('principal_minor_imaginary',determinant.imag)
            yes('principal_minor_PSD',determinant.real>=-cfg['state_tolerance'])
    calculated_occ=np.array([np.trace(rho@n).real for n in ns]);calculated_mean=np.array([np.trace(rho@a) for a in aa]);cc=np.trace(rho@cross)
    ck('probe_occupations',occup,calculated_occ);ck('probe_means',means,calculated_mean)
    ck('probe_cross',z(r['cross_coherence']),cc);ck('probe_connected',z(r['connected_cross']),cc-means[0].conjugate()*means[1])
    yes('occupation_range',np.all(occup>=-2e-9) and np.all(occup<=1+2e-9))
    hold=holds[(q,name,age)];ck('same_saved_native_energy',r['native_energy'],hold['energy'])
    e0=om*sum(int(x) for x in pinput);ep=om*sum(occup)
    ck('initial_probe_energy',r['probe_energy_initial'],e0);ck('final_probe_energy',r['probe_energy_final'],ep)
    dn=r['native_energy_final']-hold['energy'];dp=ep-e0;wo=-r['interaction_energy_before_off']
    ck('native_debit',r['delta_native_energy'],dn);ck('probe_gain',r['delta_probe_energy'],dp)
    ck('switch_on',r['switch_on_work'],0,tol=0);ck('switch_off',r['switch_off_work'],wo)
    ck('total_on',r['total_on_energy'],r['native_energy_final']+ep+r['interaction_energy_before_off'])
    ck('on_conservation',r['total_on_energy'],hold['energy']+e0,tol=cfg['energy_tolerance'])
    ledger=dn+dp-wo;derived_ledger.append(abs(ledger));ck('work_ledger_saved',r['work_ledger_residual'],ledger)
    ck('work_ledger_gate',ledger,0,tol=cfg['energy_tolerance'])
    b=2*abs(g)*T;r2=math.cosh(b)-1;r3=math.sinh(b)-b
    bounds=dict(beta=b,probability=2*b*r3+r3*r3+r2*r2,cross=2*b*r3+r3*r3,mean=r3+2*r2*math.sinh(b))
    bounds['connected']=bounds['cross']+2*b*bounds['mean']+bounds['mean']**2
    for label,v in bounds.items():ck('Dyson_bounds',r['rigorous_Dyson_bounds'][label],v)
    flip=[];refs=[]
    for j,edge in enumerate([0,3]):
        occ=int(pinput[j]);flip.append(1-occup[j] if occ else occup[j])
        ref=grams[(q,name,age,om,T,-1 if occ else 1)]['K']['real'][edge][edge];refs.append(ref)
    ck('flip_probability',r['flip_probability'],flip);ck('kernel_diagonals',r['weak_flip_coefficient'],refs)
    coefficient_error=np.asarray(flip)/g**2-np.asarray(refs);ck('coefficient_errors',r['flip_coefficient_error'],coefficient_error)
    actual_error=abs(np.asarray(flip)-g*g*np.asarray(refs))
    yes('population_Dyson_gate',np.max(actual_error)<=bounds['probability']+cfg['weak_bound_roundoff_allowance'])
    bound_ratios.append(float(np.max(actual_error)/(bounds['probability']+cfg['weak_bound_roundoff_allowance'])))
    weakmax[g]=max(weakmax.get(g,0),float(max(abs(coefficient_error))))
    metaindex=cfg['native_preparations'].index(name)*9+cfg['ages'].index(age)*3+cfg['probe_inputs'].index(pinput)
    ck('row_method_association',r['dual_state_error'],methods[(q,om,g,T)]['dual_vector_errors'][metaindex])
    if pinput=='00':
        ref=grams[(q,name,age,om,T,1)];em=-1j*g*np.exp(-1j*om*T)*z(ref['mean'])[[0,3]];ec=g*g*z(ref['K'])[0,3];econ=g*g*z(ref['connected_K'])[0,3];wr0=r['vacuum_weak_comparison']
        for label,got,expected0 in [('expected_mean',z(wr0['expected_mean']),em),('expected_cross',z(wr0['expected_cross']),ec),('expected_connected',z(wr0['expected_connected']),econ),('mean_error',z(wr0['mean_error']),means-em),('cross_coefficient_error',z(wr0['cross_coefficient_error']),(cc-ec)/g**2),('connected_coefficient_error',z(wr0['connected_coefficient_error']),(z(r['connected_cross'])-econ)/g**2)]:ck('vacuum_'+label,got,expected0)
        for label,error in [('mean',float(np.max(abs(means-em)))),('cross',abs(cc-ec)),('connected',abs(z(r['connected_cross'])-econ))]:yes('vacuum_Dyson_gate',error<=bounds[label]+cfg['weak_bound_roundoff_allowance'])
        v=dict(record_occupation=q,preparation=name,age=age,omega=om,duration=T,coupling=g,probe_gain=dp,native_debit=-dn,switch_work=wo,native_fraction=-dn/dp,switch_fraction=wo/dp,connected_cross_abs=float(abs(z(r['connected_cross']))))
        vacuum.append(v)
        if age==.5 and om==1.5 and T==1 and g==.005:examples.append(v)
    else:yes('no_wrong_vacuum_record',r['vacuum_weak_comparison'] is None)
seen=set()
for r in p['coupling_refinement']:
    k=tuple(r['key']);seen.add(k);a=rows[k+(.01,)];b=rows[k+(.005,)]
    ck('pair_coarse',r['coarse_error'],a['flip_coefficient_error']);ck('pair_fine',r['fine_error'],b['flip_coefficient_error'])
    ck('pair_difference',r['normalized_coefficient_difference'],np.array(b['flip_coefficient_error'])-a['flip_coefficient_error'])
yes('pair_census',len(seen)==324 and len(p['coupling_refinement'])==324)
ck('reported_ledger_max',p['maximum_errors']['switch_work_ledger'],max(derived_ledger))
ck('reported_dual_max',p['maximum_errors']['independent_Chebyshev_state'],max(max(x['dual_vector_errors']) for x in p['methods']))
summary={}
for label in cfg['probe_inputs']:
    rr=[r for r in p['rows'] if r['probe_input']==label]
    summary[label]={k:dict(min=min(r[k] for r in rr),max=max(r[k] for r in rr),positive=sum(r[k]>2e-10 for r in rr),negative=sum(r[k]<-2e-10 for r in rr),within_2e_10=sum(abs(r[k])<=2e-10 for r in rr)) for k in ['delta_native_energy','delta_probe_energy','switch_off_work']}
out=dict(status='PASS' if not failures else 'FAIL',scope='Saved-density/kernel/energy arithmetic and finite polynomial spectral moments only; no coupled/native producer, eigenproblem or propagation.',result_sha256=sha(rp),freeze_sha256=sha(fr),payload_sha256=wr['payload_sha256'],audit_source_sha256=sha(Path(__file__)),authenticated_unique_files=len(files),authenticated_manifests=len(manifests),manifest_member_occurrences=occurrences,check_counts=counts,maxima=maxima,failures=failures,producer_check_counts=p['check_counts'],producer_maxima=p['maximum_errors'],producer_seconds=p['elapsed_seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],source_work_by_probe_input=summary,vacuum_fraction_ranges={k:[min(r[k] for r in vacuum),max(r[k] for r in vacuum)] for k in ['native_fraction','switch_fraction']},vacuum_native_gain_count=sum(r['native_debit']<-2e-10 for r in vacuum),vacuum_native_debit_count=sum(r['native_debit']>2e-10 for r in vacuum),vacuum_source_examples=examples,maximum_normalized_flip_coefficient_error_by_g={str(k):v for k,v in weakmax.items()},maximum_population_bound_utilization=max(bound_ratios),caveats=['Saved final native/coupled state vectors are absent; their energy expectations and dual-action discrepancies remain authenticated producer certificates, not repropagated checks.','Every principal minor of each saved Hermitian probe density is checked without eigensolving; this is independent of its saved PSD check.','Signs within2e-10 in the descriptive census are explicitly unresolved at that audit scale, not recoded as zero.','Source fractions are cyclic-switch energy accounting, not photon production efficiencies or thermodynamic temperatures.'])
print(json.dumps(out,sort_keys=True,separators=(',',':'),allow_nan=False))
