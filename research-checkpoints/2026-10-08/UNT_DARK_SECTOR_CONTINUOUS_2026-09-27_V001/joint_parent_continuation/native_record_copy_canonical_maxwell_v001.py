"""Prospective constant native-copy/positive Maxwell fixture; root alone executes."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import hashlib,json,math,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
NAME='NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001'
TOL=1e-11;OMEGA=1.;MS=(8,12,16);KAPPAS=(0.,-.001,.001);TIMES=(0.,.25,.5,1.,2.)
CASES=(('native',1.,.5),('feedback_off',1.,0.),('copy_off',0.,.5))
PINS={'RECORD_ADDITION_PROTOCOL.md': '2021e117b74d760cd3d731018cd91f3cba6ef92415beda9d951f9d6a42daff49', 'record_addition_compute.py': '4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10', 'NATIVE_CANONICAL_MAXWELL_POSITIVITY_AND_VACUUM_GROWTH_V001.md': '3f57f9b9b0844903aa8dac4bd31c76372e5f6ce613e123b1c535270e03fb43f3', 'NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md': '7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b', 'NATIVE_CANONICAL_MAXWELL_PAIR_V003.md': 'f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048', '../recovered_sources/BS_MICRO_ACTION.md': '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec'}
PINS[NAME+'.md']='28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048'
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
def pack(v):return dict(real=v.real.tolist(),imag=v.imag.tolist())
def embed(a,f):
    z=np.array([[1.]])
    for i in range(4):z=np.kron(z,a if i==f else np.eye(2))
    return z

def native(g,lr):
    I=np.eye(16);N=np.diag([0.,1.]);X=np.array([[0.,1.],[1.,0.]]);Y=np.array([[0.,1j],[-1j,0.]])
    ql,qr,n,xl,xr,xa,xc,yc=(embed(a,i) for a,i in ((N,0),(N,1),(N,2),(X,0),(X,1),(X,2),(X,3),(Y,3)))
    R=ql+qr
    terms=dict(flip=-xa,bias=4*n,degree=2*(n-I)@(n-I),carrier=I,record=R,writer=0*I,
      hop=-.5*n@xc,feedback=-lr*n@R,current_squared=.25*n@yc@yc,copy_left=g*xl,copy_right=g*xr)
    H=sum(terms.values());compact=3*I+R-xa+(2.25*I-lr*R-.5*xc)@n+g*(xl+xr)
    return H,dict(R=R,ql=ql,qr=qr,n=n,carrier=embed(N,3)),terms,compact

def fields(M,kappa):
    K0=np.diag(np.arange(M+1,dtype=float)+1);Kp=np.zeros((M+1,M+1))
    for i in range(M):Kp[i+1,i]=math.sqrt((i+1)*(i+2))
    Kx=(Kp+Kp.T)/2;HD=OMEGA*(K0-Kx);HB=OMEGA*(K0+Kx)
    H0=2*OMEGA*K0;W=kappa*HB-kappa*HD/(1+kappa)
    return H0,W,HD,HB,np.diag(2*np.arange(M+1,dtype=float))

def taylor(app,v,t,bound):
    s=max(1,math.ceil(abs(t)*bound/.5));dt=t/s;r=abs(dt)*bound
    mag=1.;order=0
    for order in range(1,201):
        mag*=r/order;tail=math.exp(r)*mag*r/(order+1)
        if tail<=1e-18:break
    else:raise ArithmeticError('Taylor tail')
    u=v.copy()
    for _ in range(s):
        term=u.copy();out=u.copy()
        for k in range(1,order+1):term=(-1j*dt/k)*app(term);out+=term
        u=out
    return u,dict(substeps=s,order=order,local_tail=tail,accumulated_tail=s*tail*math.exp(s*tail))

def main():
    if sys.argv[1:]!=['--root-owned']:raise SystemExit('root-only --root-owned required')
    if any(p.exists() for p in OUTS):raise RuntimeError('Existing exclusive output')
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();inputs=verify()
    rows=[];trials=[];checks=[];states={};comparisons=[]
    def check(label,a,b=0.,scale=1.):
        e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));s=max(1.,float(scale))
        checks.append(dict(label=label,error=e,scale=s,tolerance=TOL,passed=bool(math.isfinite(e) and e<=TOL*s)))
    def ex(v,av):
        z=np.vdot(v,av)
        if abs(z.imag)>TOL*max(1.,abs(z.real)):raise ArithmeticError('Nonreal Hermitian readout')
        return float(z.real)
    for label,g,lr in CASES:
        hn,o,terms,compact=native(g,lr);p=o['n'];R=o['R'];rn=np.diag(R).real.astype(int)
        check(label+':compact',hn,compact,scale=np.linalg.norm(hn,np.inf))
        for key,a in terms.items():check(label+':term_hermitian:'+key,a,a.conj().T,scale=np.linalg.norm(a,np.inf))
        for kappa in KAPPAS:
            for M in MS:
                h0,wk,hd,hb,ng=fields(M,kappa);K=16*(M+1);tag=f'{label}:{kappa}:{M}'
                H=np.kron(hn,np.eye(M+1))+np.kron(np.eye(16),h0)+np.kron(p,wk)
                eg,vg=np.linalg.eigh(H);v0=np.zeros((16,M+1),complex);v0[0,0]=1.
                def app(v):return hn@v+v@h0.T+(p@v)@wk.T
                bound=float(np.linalg.norm(hn,np.inf)+np.linalg.norm(h0,np.inf)+np.linalg.norm(p,np.inf)*np.linalg.norm(wk,np.inf))
                check(tag+':hermitian',H,H.conj().T,scale=bound)
                check(tag+':eigen_equation',H@vg,vg*eg,scale=bound)
                check(tag+':eigen_orthogonal',vg.conj().T@vg,np.eye(K))
                check(tag+':field_lower',max(0.,2*OMEGA-float(np.linalg.eigvalsh(h0+wk)[0])))
                a1=app(v0);a2=app(a1);bkap=kappa*(2+kappa)/(2*(1+kappa));contact=OMEGA*kappa*kappa/(1+kappa)
                def coeff(appA):return ex(a1,appA(a1))-float(np.vdot(v0,appA(a2)).real)
                check(tag+':early_record',coeff(lambda v:R@v),2*g*g)
                check(tag+':early_incidence',coeff(lambda v:p@v),1.)
                check(tag+':early_bare_photon_tau2',coeff(lambda v:v@h0.T),0.)
                check(tag+':early_interaction',coeff(lambda v:(p@v)@wk.T),contact)
                check(tag+':early_native',coeff(lambda v:hn@v),-contact)
                check(tag+':early_number_tau4',2*float(np.vdot(a2[:,1]/2,a2[:,1]/2).real),OMEGA*OMEGA*bkap*bkap)
                initial_total=ex(v0,app(v0));check(tag+':initial_absolute',initial_total,3+2*OMEGA)
                trial=dict(case=label,g=g,lambda_R=lr,kappa=kappa,M=M,dimension=K,eigenvalues=eg.tolist(),states=[])
                weights=vg.conj().T@v0.ravel()
                for tau in TIMES:
                    v=(vg@(np.exp(-1j*tau*eg)*weights)).reshape(16,M+1);vt,td=taylor(app,v0,tau,bound)
                    tagt=tag+f':{tau}';check(tagt+':spectral_taylor',np.linalg.norm(v-vt));check(tagt+':norm',ex(v,v),1.)
                    EN=ex(v,hn@v);E0=ex(v,v@h0.T);EI=ex(v,(p@v)@wk.T);ET=ex(v,app(v))
                    F=E0+EI-2*OMEGA;G=E0-2*OMEGA;D=3-EN;ledger=math.fsum([EN,E0,EI,-initial_total])
                    prob=np.abs(v)**2;joint=np.array([prob[rn==i,:].sum(axis=0) for i in range(3)])
                    rprob=joint.sum(axis=1);fprob=joint.sum(axis=0);rmean=ex(v,R@v);number=ex(v,v@ng.T)
                    cov=float(np.sum(joint*np.arange(3)[:,None]*(2*np.arange(M+1))[None,:])-rmean*number)
                    vals=dict(native=EN,native_change=EN-3,native_debit=D,bare_photon=E0,photon_gain=G,interaction=EI,
                      inclusive_field_excess=F,total=ET,ledger=ledger,number=number,record=rmean,record_left=ex(v,o['ql']@v),
                      record_right=ex(v,o['qr']@v),incidence=ex(v,p@v),carrier_right=ex(v,o['carrier']@v),cov_record_photon=cov,
                      record_current=ex(v,1j*(hn@R-R@hn)@v),link_current=ex(v,1j*(hn@p-p@hn)@v),top=float(fprob[-1]),
                      kappa_contact=ex(v,(p@v)@(hb-hd/(1+kappa)**2).T),kappa_second=ex(v,(p@v)@(2*hd/(1+kappa)**3).T))
                    check(tagt+':total_ledger',ledger,scale=abs(EN)+abs(E0)+abs(EI)+abs(initial_total))
                    check(tagt+':energy_split',math.fsum([G,-D,EI]),scale=abs(G)+abs(D)+abs(EI))
                    check(tagt+':field_bound',max(0.,-F));check(tagt+':native_bound',max(0.,-D));check(tagt+':joint_normalization',joint.sum(),1.)
                    if lr==0.:check(tagt+':record_field_factorization',joint,rprob[:,None]*fprob[None,:])
                    if g==0.:check(tagt+':blank_records',rprob,[1.,0.,0.])
                    row=dict(case=label,kappa=kappa,M=M,tau=tau,**vals,record_probabilities=rprob.tolist(),
                      record_pair_joint=joint.tolist(),taylor=td,taylor_vector=pack(vt))
                    rows.append(row);trial['states'].append(dict(tau=tau,state=pack(v)))
                    states[(label,kappa,M,tau)]=(v,vals)
                trials.append(trial)
    for label,g,lr in CASES:
        for kappa in KAPPAS:
            for lo,hi in ((8,12),(12,16)):
                for tau in TIMES:
                    v,a=states[(label,kappa,lo,tau)];z,b=states[(label,kappa,hi,tau)];embedded=np.zeros_like(z);embedded[:,:lo+1]=v
                    tag=f'cutoff:{label}:{kappa}:{lo}:{hi}:{tau}';err=float(np.linalg.norm(z-embedded));check(tag+':state',err)
                    diff={k:b[k]-a[k] for k in a}
                    for k,d in diff.items():check(tag+':'+k,d,scale=max(1.,abs(a[k]),abs(b[k])))
                    comparisons.append(dict(case=label,kappa=kappa,M_low=lo,M_high=hi,tau=tau,joint_state_error=err,signed=diff))
    assert len(rows)==135 and len(trials)==27 and len(comparisons)==90
    if verify()!=inputs:raise RuntimeError('Input changed')
    failed=sum(not c['passed'] for c in checks)
    result=dict(name=NAME,source_sha256=inputs[Path(__file__).name],inputs=inputs,owner='root',PID=os.getpid(),
      started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,
      status='PASS' if failed==0 else 'FAIL',failed=failed,controls=checks,trials=trials,rows=rows,comparisons=comparisons,
      actuator_work=0.,initial_interaction_energy=0.,absolute_vacuum=2*OMEGA,
      physical_claims=dict(outgoing_radiation=False,thermal_origin=False,matter_origin=False,macroscopic_pressure_match=False,cosmology=False))
    report=f'# Constant native record-copy/Maxwell branch\n\n{result["status"]}: {len(checks)-failed}/{len(checks)} controls;27 trials,135 states,90 cutoff comparisons.\n\nComplete signed native/bare-field/interaction ledger and record–photon joint probabilities are retained. Constant-plateau actuator work and initial interaction storage are zero; coupled field counts do not establish outgoing radiation, thermalization or the macroscopic pressure branch.\n'
    write(OUTS[0],canonical(result));write(OUTS[1],report.encode())
    if verify()!=inputs:raise RuntimeError('Post-result input changed')
    receipt=dict(owner='root',PID=os.getpid(),started_utc=started,closed_utc=datetime.now(timezone.utc).isoformat(),
      inputs=inputs,outputs={p.name:sha(p) for p in OUTS[:2]},status=result['status'],trials=27,states=135,comparisons=90,checks=len(checks),failed=failed)
    write(OUTS[2],canonical(receipt))
    if verify()!=inputs or any(sha(BASE/n)!=h for n,h in receipt['outputs'].items()):raise RuntimeError('Post-publication seal')
    print(json.dumps(dict(status=result['status'],checks=len(checks),failed=failed,result_sha256=sha(OUTS[0]),receipt_sha256=sha(OUTS[2]))))
    return 0 if failed==0 else 3
if __name__=='__main__':raise SystemExit(main())
