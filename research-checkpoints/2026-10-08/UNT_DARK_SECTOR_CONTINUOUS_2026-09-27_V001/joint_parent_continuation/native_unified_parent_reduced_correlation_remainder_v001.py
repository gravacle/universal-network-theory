"""Root-owned saved marginal/correlation arithmetic; no evolution or spectral calls."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import hashlib,json,math,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
NAME='NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001';PARENT='NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001';COMP='NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001'
TOL=1e-11;CASES=(('native',1.,.5),('feedback_off',1.,0.),('copy_off',0.,.5));MS=(8,12,16);KS=(0.,-.001,.001);TS=(0.,.25,.5,1.,2.)
PINS={'native_record_copy_canonical_maxwell_v001.py':'607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a',PARENT+'.md':'28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048',PARENT+'_RESULT.json':'d2ad69ba985d5b5ef21ecd2caa687578231c621a79c0d4eb34cdefb344ad90d3',PARENT+'_RECEIPT.json':'91bc8a7feafdbf6bc72ab8e072e7a1575ae0641c64d9c8b91eb1c6c7e64dd073','native_unified_parent_component_exchange_v001.py':'2da75f9a6c20643a7d6b4288a821fe64e72ceb9961495f9dc167949d3d2459a2',COMP+'.md':'c83dbcbbdb8cbb62c459cb8ffdbed49edfc7a2a9148c3c913057dedfc9507072',COMP+'_RESULT.json':'e47f1ec7031dc540412b185cf6c2d0e6441131f3b59befdc1c254eb49b8fae8b',COMP+'_RECEIPT.json':'cf88622b4c2c7806577f8cd3c74ac81a5bb3a0b57faeb143265b12d5acac6688','NATIVE_UNIFIED_PARENT_CORRELATION_SOURCE_AND_PRODUCT_INTERVAL_V001.md':'f62a63f3230ba90cbf645090f007c39c5b4ae3ae00c1d7459726efe388ccff9f'}
PINS[NAME+'.md']='2bca11d70888856b4b43489068bbeb3184cdf7066f34ef4b45ccb11843d0246a'
OUTS=[BASE/(NAME+s) for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def write(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    os.chmod(p,0o444)
def verify():
    for n,h in PINS.items():
        if sha(BASE/n)!=h:raise RuntimeError('Input seal mismatch '+n)
    return dict(PINS,**{Path(__file__).name:sha(Path(__file__))})
def finite(v):
    if isinstance(v,dict):
        for x in v.values():finite(x)
    elif isinstance(v,list):
        for x in v:finite(x)
    elif isinstance(v,float) and not math.isfinite(v):raise ValueError('Nonfinite saved value')
    elif not isinstance(v,(dict,list,str,int,float,bool,type(None))):raise TypeError('Saved type')
def pack(v):return dict(real=v.real.tolist(),imag=v.imag.tolist())
def unpack(v):return np.asarray(v['real'],float)+1j*np.asarray(v['imag'],float)
def frob(a):return math.sqrt(float(np.vdot(a,a).real))
def comm(a,b):return a@b-b@a
def embed(a,f):
    z=np.array([[1.]])
    for i in range(4):z=np.kron(z,a if i==f else np.eye(2))
    return z
def operators(g,lr,M,kappa):
    I=np.eye(16);Q=np.diag([0.,1.]);X=np.array([[0.,1.],[1.,0.]])
    ql,qr,n,xl,xr,xa,xc=(embed(a,i) for a,i in ((Q,0),(Q,1),(Q,2),(X,0),(X,1),(X,2),(X,3)))
    R=ql+qr;hn=3*I+R-xa+(2.25*I-lr*R-.5*xc)@n+g*(xl+xr)
    K0=np.diag(np.arange(M+1,dtype=float)+1);Kp=np.zeros((M+1,M+1))
    for i in range(M):Kp[i+1,i]=math.sqrt((i+1)*(i+2))
    Kx=(Kp+Kp.T)/2;B=2*K0;W=kappa*(K0+Kx)-kappa*(K0-Kx)/(1+kappa)
    return hn,n,B,W
def partials(a,d):
    z=a.reshape(16,d,16,d)
    return np.trace(z,axis1=1,axis2=3),np.trace(z,axis1=0,axis2=2)
def reduction(v,hn,n,B,W):
    d=v.shape[1];D=16*d;ket=v.ravel();rho=np.outer(ket,ket.conj());rn=v@v.conj().T;rf=v.T@v.conj();chi=rho-np.kron(rn,rf)
    norm=float(np.vdot(v,v).real);en=np.trace(n@rn);ew=np.trace(W@rf);mean_n=float(en.real);mean_w=float(ew.real)
    cn=v@W.T@v.conj().T-mean_w*rn;cf=v.T@n.T@v.conj()-mean_n*rf
    dn=-1j*comm(n,cn);df=-1j*comm(W,cf);mn=-1j*comm(hn+mean_w*n,rn);mf=-1j*comm(B+mean_n*W,rf)
    iv=(n@v)@W.T;ivket=iv.ravel();irate=-1j*(np.outer(ivket,ket.conj())-np.outer(ket,ivket.conj()));in_direct,if_direct=partials(irate,d)
    h_v=hn@v+v@B.T+iv;v_dot=-1j*h_v;direct_n=v_dot@v.conj().T+v@v_dot.conj().T;direct_f=v_dot.T@v.conj()+v.T@v_dot.conj()
    c4=chi.reshape(16,d,16,d);left=np.einsum('ab,ij,bjck->aick',n,W,c4,optimize=True).reshape(D,D);cor_full=-1j*(left-left.conj().T);cor_n,cor_f=partials(cor_full,d)
    weighted_w=np.einsum('ij,ajbk->aibk',W,c4,optimize=True);weighted_n=np.einsum('ab,bicj->aicj',n,c4,optimize=True)
    cn_direct=np.trace(weighted_w,axis1=1,axis2=3);cf_direct=np.trace(weighted_n,axis1=0,axis2=2)
    mats=dict(rho_native=rn,rho_field=rf,chi_native_weighted=cn,chi_field_weighted=cf,mean_native=mn,mean_field=mf,correlation_native=dn,correlation_field=df,total_native=mn+dn,total_field=mf+df,interaction_native=in_direct,interaction_field=if_direct,bare_field_generator=-1j*comm(B,rf),direct_native=direct_n,direct_field=direct_f)
    upper=math.sqrt(D)*frob(chi);wf=frob(W);an=2*wf*upper
    stats=dict(norm=norm,mean_n=mean_n,mean_w=mean_w,chi_frobenius=frob(chi),chi_trace_upper=upper,correlation_native_frobenius=frob(dn),correlation_field_frobenius=frob(df),correlation_native_trace_upper=4*frob(dn),correlation_field_trace_upper=math.sqrt(d)*frob(df),analytic_correlation_trace_upper=an,bare_stationarity_frobenius=frob(comm(rf,B)),mean_native_frobenius=frob(mn),mean_field_frobenius=frob(mf),native_rate_frobenius=frob(direct_n),field_rate_frobenius=frob(direct_f),native_purity=float(np.vdot(rn,rn).real),field_purity=float(np.vdot(rf,rf).real),native_linear_entropy=1-float(np.vdot(rn,rn).real),field_linear_entropy=1-float(np.vdot(rf,rf).real))
    number=B-2*np.eye(d)
    stats.update(mean_n_imag=float(en.imag),mean_w_imag=float(ew.imag),photon_number=float(np.trace(number@rf).real),photon_number_rate_direct=float(np.trace(number@direct_f).real),photon_number_rate_mean=float(np.trace(number@mf).real),photon_number_rate_correlation=float(np.trace(number@df).real))
    return mats,stats,dict(rho=rho,chi=chi,cn=cn_direct,cf=cf_direct,cor_n=cor_n,cor_f=cor_f),v
def main():
    if sys.argv[1:]!=['--root-owned']:raise SystemExit('root-only --root-owned required')
    if any(p.exists() for p in OUTS):raise RuntimeError('Existing exclusive output')
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();inputs=verify()
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());pr=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());component=json.loads((BASE/(COMP+'_RESULT.json')).read_text());cr=json.loads((BASE/(COMP+'_RECEIPT.json')).read_text())
    for z in (parent,pr,component,cr):finite(z)
    for name,data,receipt,source,count in ((PARENT,parent,pr,'native_record_copy_canonical_maxwell_v001.py',3348),(COMP,component,cr,'native_unified_parent_component_exchange_v001.py',3528)):
        if data['inputs']!=receipt['inputs'] or data['source_sha256']!=PINS[source] or data['inputs'][source]!=PINS[source] or receipt['outputs'][name+'_RESULT.json']!=PINS[name+'_RESULT.json'] or data['owner']!='root' or receipt['owner']!='root' or data['PID']!=receipt['PID']:raise ValueError('Parent binding '+name)
        if data['status']!='PASS' or data['failed']!=0 or receipt['status']!='PASS' or receipt['failed']!=0 or len(data['controls'])!=count or any(not x['passed'] for x in data['controls']) or len(data['rows'])!=135 or len(data['comparisons'])!=90:raise ValueError('Parent dispositions '+name)
        if (receipt['trials'],receipt['states'],receipt['comparisons'],receipt['checks' if name==PARENT else 'controls'])!=(27,135,90,count):raise ValueError('Parent receipt census '+name)
    if component['parent_controls']!=parent['controls'] or any(component['inputs'].get(k)!=PINS[k] for k in ('native_record_copy_canonical_maxwell_v001.py',PARENT+'_RESULT.json',PARENT+'_RECEIPT.json')):raise ValueError('Component ancestry')
    if len(parent['trials'])!=27 or parent['actuator_work']!=0. or parent['initial_interaction_energy']!=0. or parent['absolute_vacuum']!=2.:raise ValueError('Original fixture premise')
    old={(x['case'],x['kappa'],x['M'],x['tau']):x for x in parent['rows']};comp={(x['case'],x['kappa'],x['M'],x['tau']):x for x in component['rows']}
    if len(old)!=135 or len(comp)!=135:raise ValueError('Duplicate descriptors')
    controls=[];rows=[];trials=[];look={};seen=set()
    def check(label,a,b=0.,scale=1.):
        e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));s=max(1.,float(scale));controls.append(dict(label=label,error=e,scale=s,tolerance=TOL,passed=bool(math.isfinite(e) and e<=TOL*s)))
    for tr in parent['trials']:
        case,g,lr,M,kappa=tr['case'],tr['g'],tr['lambda_R'],tr['M'],tr['kappa'];key=(case,kappa,M)
        if (case,g,lr) not in CASES or M not in MS or kappa not in KS or key in seen or tr['dimension']!=16*(M+1) or [x['tau'] for x in tr['states']]!=list(TS):raise ValueError('Trial descriptor')
        seen.add(key);hn,n,B,W=operators(g,lr,M,kappa);bound=max(1.,frob(hn)+frob(B)+frob(W));tag=f'{case}:{kappa}:{M}'
        for label,a in (('HN',hn),('n',n),('B',B),('W',W)):check(tag+':hermitian:'+label,a,a.conj().T,scale=bound)
        check(tag+':projector',n@n,n);trials.append(dict(case=case,g=g,lambda_R=lr,M=M,kappa=kappa,HN=pack(hn),n=pack(n),B=pack(B),W=pack(W)))
        for sv in tr['states']:
            tau=sv['tau'];desc=(case,kappa,M,tau);v=unpack(sv['state']);vt=unpack(old[desc]['taylor_vector']);rtag=tag+':'+str(tau);methods={};memory={}
            for method,vec in (('spectral',v),('taylor',vt)):
                if vec.shape!=(16,M+1) or not np.all(np.isfinite(vec)):raise ValueError('Vector shape/finite')
                mats,stats,extra,vec=reduction(vec,hn,n,B,W);mtag=rtag+':'+method;d=M+1;norm=stats['norm'];rn=mats['rho_native'];rf=mats['rho_field'];rn_direct,rf_direct=partials(extra['rho'],d);ch_n,ch_f=partials(extra['chi'],d)
                check(mtag+':norm',norm,1.);check(mtag+':partial_native',rn,rn_direct);check(mtag+':partial_field',rf,rf_direct);check(mtag+':density_traces',[np.trace(rn),np.trace(rf)],[norm,norm])
                check(mtag+':chi_trace',np.trace(extra['chi']),norm-norm*norm);check(mtag+':chi_partial_native',ch_n,(1-norm)*rn);check(mtag+':chi_partial_field',ch_f,(1-norm)*rf)
                check(mtag+':weighted_native',mats['chi_native_weighted'],extra['cn'],scale=bound);check(mtag+':weighted_field',mats['chi_field_weighted'],extra['cf'],scale=bound)
                check(mtag+':corr_native',mats['correlation_native'],extra['cor_n'],scale=bound*bound);check(mtag+':corr_field',mats['correlation_field'],extra['cor_f'],scale=bound*bound)
                check(mtag+':native_rate',mats['total_native'],mats['direct_native'],scale=bound*bound);check(mtag+':field_rate',mats['total_field'],mats['direct_field'],scale=bound*bound)
                check(mtag+':native_interaction',mats['interaction_native'],-1j*stats['mean_w']*comm(n,rn)+mats['correlation_native'],scale=bound*bound);check(mtag+':field_interaction',mats['interaction_field'],-1j*stats['mean_n']*comm(W,rf)+mats['correlation_field'],scale=bound*bound)
                check(mtag+':all_matrix_hermiticity',[frob(a-a.conj().T) for a in mats.values()],scale=bound*bound);check(mtag+':all_rate_traces',[np.trace(a) for k,a in mats.items() if k not in ('rho_native','rho_field','chi_native_weighted','chi_field_weighted')],scale=bound*bound)
                check(mtag+':corr_native_bound',max(0.,stats['correlation_native_trace_upper']-stats['analytic_correlation_trace_upper']),scale=bound*bound);check(mtag+':corr_field_bound',max(0.,stats['correlation_field_trace_upper']-stats['analytic_correlation_trace_upper']),scale=bound*bound)
                check(mtag+':mean_imag',[stats['mean_n_imag'],stats['mean_w_imag']],scale=bound);check(mtag+':number_rate_split',stats['photon_number_rate_direct'],stats['photon_number_rate_mean']+stats['photon_number_rate_correlation'],scale=bound*bound)
                c=comp[desc][method];check(mtag+':original_energies',[np.trace(hn@rn),np.trace(B@rf),np.trace(W@(vec.T@n.T@vec.conj()))],[c['raw']['native'],c['raw']['bare_photon'],c['raw']['interaction']],scale=bound)
                methods[method]=dict(joint_amplitudes=pack(vec),matrices={k:pack(a) for k,a in mats.items()},scalars=stats,chi_representation='outer(flat(joint_amplitudes),conjugate)-kron(rho_native,rho_field)');memory[method]=(mats,stats,vec)
            sm,ss,_=memory['spectral'];tm,tt,_=memory['taylor'];check(rtag+':methods_matrices',[frob(sm[k]-tm[k]) for k in sm],scale=bound*bound);check(rtag+':methods_scalars',[ss[k] for k in ss],[tt[k] for k in ss],scale=bound*bound)
            delta={k:sm[k]-tm[k] for k in sm}
            row=dict(case=case,kappa=kappa,M=M,tau=tau,methods=methods,method_difference=dict(matrices={k:pack(z) for k,z in delta.items()},matrix_metrics={k:dict(frobenius=frob(z),max_absolute=float(np.max(np.abs(z)))) for k,z in delta.items()},scalars={k:ss[k]-tt[k] for k in ss},joint_amplitudes=pack(v-vt)));rows.append(row);look[desc]=memory
    comparisons=[]
    for case,g,lr in CASES:
        for kappa in KS:
            for lo,hi in ((8,12),(12,16)):
                for tau in TS:
                    a=look[(case,kappa,lo,tau)];b=look[(case,kappa,hi,tau)];methods={}
                    for method in ('spectral','taylor'):
                        am,ast,av=a[method];bm,bst,bv=b[method];dif={};metrics={};common={};tails={}
                        for k,z in am.items():
                            em=z if 'native' in k else np.pad(z,((0,hi-lo),(0,hi-lo)))
                            dz=bm[k]-em;dif[k]=pack(dz);metrics[k]=dict(frobenius=frob(dz),max_absolute=float(np.max(np.abs(dz))))
                            if 'native' not in k:
                                dc=bm[k][:lo+1,:lo+1]-z;tail=bm[k].copy();tail[:lo+1,:lo+1]=0
                                common[k]=pack(dc);tails[k]=pack(tail);metrics[k].update(common_frobenius=frob(dc),common_max_absolute=float(np.max(np.abs(dc))),high_tail_frobenius=frob(tail),high_tail_max_absolute=float(np.max(np.abs(tail))))
                        ev=np.pad(av,((0,0),(0,hi-lo)));an=am['rho_native'];af=np.pad(am['rho_field'],((0,hi-lo),(0,hi-lo)));bn=bm['rho_native'];bf=bm['rho_field'];ca=np.outer(ev.ravel(),ev.ravel().conj())-np.kron(an,af);cb=np.outer(bv.ravel(),bv.ravel().conj())-np.kron(bn,bf)
                        methods[method]=dict(matrix_differences=dif,matrix_metrics=metrics,common_field_differences=common,high_field_tails=tails,scalar_differences={k:bst[k]-ast[k] for k in ast},joint_difference=pack(bv-ev),chi_difference_frobenius=frob(cb-ca),chi_difference_trace_upper=math.sqrt(16*(hi+1))*frob(cb-ca))
                    comparisons.append(dict(case=case,kappa=kappa,M_low=lo,M_high=hi,tau=tau,methods=methods))
    if len(seen)!=27 or len(rows)!=135 or len(comparisons)!=90 or len(controls)!=6345:raise ValueError('Locked own census')
    if verify()!=inputs:raise RuntimeError('Inputs changed')
    failed=sum(not c['passed'] for c in controls);result=dict(name=NAME,owner='root',PID=os.getpid(),source_sha256=inputs[Path(__file__).name],inputs=inputs,started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,status='PASS' if not failed else 'FAIL',failed=failed,controls=controls,trials=trials,rows=rows,comparisons=comparisons,original_controls=parent['controls'],component_controls=component['controls'],parent_physical_claims=parent['physical_claims'],component_physical_claims=component['physical_claims'],physical_claims=dict(decoupled_fluids=False,temperature=False,thermal_origin=False,macroscopic_pressure_match=False,outgoing_radiation=False,cosmology=False))
    report=f'# Saved single-parent reduced correlation sources\n\n{result["status"]}: {len(controls)-failed}/{len(controls)} arithmetic controls; all27 trials,135 spectral/Taylor pairs and90 cutoff pairs retained.\n\nFull reduced matrices,exact compact connected density,correlation remainders,mean-field rates and bare-field stationarity norms are diagnostics. No nonzero-source or entanglement threshold qualifies a fluid or temperature. The original3348 and component3528 dispositions remain retained.\n'
    write(OUTS[0],canonical(result));write(OUTS[1],report.encode())
    if verify()!=inputs:raise RuntimeError('Post-result input changed')
    receipt=dict(owner='root',PID=os.getpid(),started_utc=started,closed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,outputs={p.name:sha(p) for p in OUTS[:2]},status=result['status'],failed=failed,trials=27,states=135,comparisons=90,controls=6345,original_controls=3348,component_controls=3528)
    write(OUTS[2],canonical(receipt))
    if verify()!=inputs or any(sha(BASE/n)!=h for n,h in receipt['outputs'].items()):raise RuntimeError('Post-publication seal')
    print(json.dumps(dict(status=result['status'],controls=len(controls),failed=failed,result_sha256=sha(OUTS[0]),receipt_sha256=sha(OUTS[2]))))
    return 0 if not failed else 3
if __name__=='__main__':raise SystemExit(main())
