"""Saved-only inclusive component exchange; root alone evaluates sealed vectors."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import hashlib,json,math,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
NAME='NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001'
PARENT='NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001'
TOL=1e-11;OMEGA=1.;MS=(8,12,16);KAPPAS=(0.,-.001,.001);TIMES=(0.,.25,.5,1.,2.)
CASES=(('native',1.,.5),('feedback_off',1.,0.),('copy_off',0.,.5))
LABELS=('carrier','record','link','bare_field','interaction')
EDGES=((0,2),(1,2),(2,4),(3,4))
PINS={'native_record_copy_canonical_maxwell_v001.py':'607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a',PARENT+'_RESULT.json':'d2ad69ba985d5b5ef21ecd2caa687578231c621a79c0d4eb34cdefb344ad90d3',PARENT+'_RECEIPT.json':'91bc8a7feafdbf6bc72ab8e072e7a1575ae0641c64d9c8b91eb1c6c7e64dd073','../recovered_sources/BS_MICRO_ACTION.md':'00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec'}
PINS[NAME+'.md']='c83dbcbbdb8cbb62c459cb8ffdbed49edfc7a2a9148c3c913057dedfc9507072'
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
    elif isinstance(v,float) and not math.isfinite(v):raise ValueError('Nonfinite saved tree')
    elif not isinstance(v,(dict,list,str,int,float,bool,type(None))):raise TypeError('Unsupported saved value')
def unpack(d,M):
    v=np.asarray(d['real'],float)+1j*np.asarray(d['imag'],float)
    if v.shape!=(16,M+1) or not np.all(np.isfinite(v)):raise ValueError('Saved vector shape/finite')
    return v
def embed(a,f):
    z=np.array([[1.]])
    for i in range(4):z=np.kron(z,a if i==f else np.eye(2))
    return z
def operators(g,lr,M,kappa):
    I=np.eye(16);Q=np.diag([0.,1.]);X=np.array([[0.,1.],[1.,0.]])
    ql,qr,n,xl,xr,xa,xc,cr=(embed(a,i) for a,i in ((Q,0),(Q,1),(Q,2),(X,0),(X,1),(X,2),(X,3),(Q,3)))
    R=ql+qr;C=I+n@(.25*I-.5*xc);Rec=R-lr*n@R+g*(xl+xr);L=2*I+2*n-xa
    compact=3*I+R-xa+(2.25*I-lr*R-.5*xc)@n+g*(xl+xr)
    K0=np.diag(np.arange(M+1,dtype=float)+1);Kp=np.zeros((M+1,M+1))
    for i in range(M):Kp[i+1,i]=math.sqrt((i+1)*(i+2))
    Kx=(Kp+Kp.T)/2;HD=OMEGA*(K0-Kx);HB=OMEGA*(K0+Kx);H0=2*OMEGA*K0;W=kappa*HB-kappa*HD/(1+kappa)
    components=((C,np.eye(M+1)),(Rec,np.eye(M+1)),(L,np.eye(M+1)),(I,H0),(n,W))
    return components,compact,dict(R=R,n=n,carrier_right=cr,number=np.diag(2*np.arange(M+1))),HD,HB
def applied(v,pair):return pair[0]@v@pair[1].T
def expectation(v,av):
    z=np.vdot(v,av)
    if abs(z.imag)>TOL*max(1.,abs(z.real)):raise ArithmeticError('Nonreal Hermitian expectation')
    return float(z.real)
def commutators(parts):
    out={}
    for a in range(5):
        for b in range(a+1,5):
            na,fa=parts[a];nb,fb=parts[b]
            out[(a,b)]=(nb@na,fb@fa,na@nb,fa@fb)
    return out
def measure(v,parts,hn,o,comms):
    av=[applied(v,p) for p in parts];hv=sum(av);energies=[expectation(v,x) for x in av]
    powers=np.array([[-2*float(np.vdot(av[b],av[a]).imag) for b in range(5)] for a in range(5)])
    direct=np.zeros((5,5))
    for (a,b),(n1,f1,n2,f2) in comms.items():
        z=expectation(v,1j*(n1@v@f1.T-n2@v@f2.T));direct[a,b]=z;direct[b,a]=-z
    derivative=[-2*float(np.vdot(hv,x).imag) for x in av]
    native_av=hn@v
    raw=dict(native=expectation(v,native_av),bare_photon=energies[3],interaction=energies[4],record=expectation(v,o['R']@v),incidence=expectation(v,o['n']@v),carrier_right=expectation(v,o['carrier_right']@v),number=expectation(v,v@o['number'].T))
    for key,op in (('record_current',o['R']),('link_current',o['n'])):raw[key]=expectation(v,1j*(hn@op-op@hn)@v)
    carrier_rate=-2*float(np.vdot(hv,o['carrier_right']@v).imag)
    native_carrier_rate=expectation(v,1j*(hn@o['carrier_right']-o['carrier_right']@hn)@v)
    number_rate=-2*float(np.vdot(hv,v@o['number'].T).imag)
    return dict(energies=energies,changes=[e-e0 for e,e0 in zip(energies,(1.,0.,2.,2.,0.))],powers=powers.tolist(),direct_powers=direct.tolist(),edge_powers={LABELS[a]+'<-'+LABELS[b]:float(direct[a,b]) for a,b in EDGES},derivatives=derivative,native_derivative=math.fsum(derivative[:3]),field_derivative=math.fsum(derivative[3:]),raw=raw,total=expectation(v,hv),carrier_rate=carrier_rate,native_carrier_rate=native_carrier_rate,number_rate=number_rate)
def main():
    if sys.argv[1:]!=['--root-owned']:raise SystemExit('root-only --root-owned required')
    if any(p.exists() for p in OUTS):raise RuntimeError('Existing exclusive output')
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();inputs=verify()
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());finite(parent);finite(receipt)
    if receipt['inputs']!=parent['inputs'] or parent['inputs']['native_record_copy_canonical_maxwell_v001.py']!=PINS['native_record_copy_canonical_maxwell_v001.py'] or parent['inputs']['../recovered_sources/BS_MICRO_ACTION.md']!=PINS['../recovered_sources/BS_MICRO_ACTION.md']:raise ValueError('Parent input/source binding')
    if receipt['outputs'][PARENT+'_RESULT.json']!=PINS[PARENT+'_RESULT.json'] or receipt['owner']!='root' or parent['owner']!='root' or receipt['PID']!=parent['PID'] or parent['source_sha256']!=PINS['native_record_copy_canonical_maxwell_v001.py']:raise ValueError('Parent receipt/owner binding')
    if (receipt['trials'],receipt['states'],receipt['comparisons'],receipt['checks'],receipt['failed'],receipt['status'])!=(27,135,90,3348,0,'PASS') or parent['status']!='PASS' or parent['failed']!=0 or len(parent['trials'])!=27 or len(parent['rows'])!=135 or len(parent['comparisons'])!=90 or len(parent['controls'])!=3348 or any(not c['passed'] for c in parent['controls']):raise ValueError('Parent census/disposition')
    if parent['actuator_work']!=0. or parent['initial_interaction_energy']!=0. or parent['absolute_vacuum']!=2.:raise ValueError('Parent energy premise')
    oldrows={(r['case'],r['kappa'],r['M'],r['tau']):r for r in parent['rows']};oldcomp={(r['case'],r['kappa'],r['M_low'],r['M_high'],r['tau']):r for r in parent['comparisons']}
    if len(oldrows)!=135 or len(oldcomp)!=90:raise ValueError('Duplicate parent descriptors')
    controls=[];rows=[];operator_rows=[];lookup={};vectors={};seen=set()
    def check(label,a,b=0.,scale=1.):
        e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));s=max(1.,float(scale));controls.append(dict(label=label,error=e,scale=s,tolerance=TOL,passed=bool(math.isfinite(e) and e<=TOL*s)))
    for tr in parent['trials']:
        label=tr['case'];g=tr['g'];lr=tr['lambda_R'];M=tr['M'];kappa=tr['kappa'];key=(label,kappa,M)
        if (label,g,lr) not in CASES or M not in MS or kappa not in KAPPAS or key in seen or tr['dimension']!=16*(M+1) or len(tr['states'])!=5 or [x['tau'] for x in tr['states']]!=list(TIMES):raise ValueError('Parent trial schema')
        seen.add(key);parts,hn,o,HD,HB=operators(g,lr,M,kappa);comms=commutators(parts);tag=f'{label}:{kappa}:{M}'
        scale=sum(float(np.linalg.norm(n,np.inf)*np.linalg.norm(f,np.inf)) for n,f in parts)
        check(tag+':native_sum',sum(p[0] for p in parts[:3]),hn,scale=scale)
        for a,p in enumerate(parts):z=np.kron(*p);check(tag+':hermitian:'+str(a),z,z.conj().T,scale=scale)
        norms={}
        for (a,b),(n1,f1,n2,f2) in comms.items():
            z=1j*(np.kron(n1,f1)-np.kron(n2,f2));norms[f'{a}:{b}']=float(np.linalg.norm(z,np.inf));check(tag+':comm_hermitian:'+str((a,b)),z,z.conj().T,scale=scale*scale)
            if (a,b) not in EDGES:check(tag+':forbidden_operator:'+str((a,b)),z,scale=scale*scale)
        operator_rows.append(dict(case=label,kappa=kappa,M=M,commutator_norms=norms))
        for saved in tr['states']:
            tau=saved['tau'];desc=(label,kappa,M,tau);old=oldrows[desc];v=unpack(saved['state'],M);vt=unpack(old['taylor_vector'],M);s=measure(v,parts,hn,o,comms);t=measure(vt,parts,hn,o,comms);rtag=tag+':'+str(tau)
            for field in ('energies','powers','derivatives'):check(rtag+':spectral_taylor:'+field,s[field],t[field],scale=scale*scale if field!='energies' else scale)
            rkeys=tuple(s['raw']);check(rtag+':spectral_taylor:raw',[s['raw'][k] for k in rkeys],[t['raw'][k] for k in rkeys],scale=scale*scale)
            check(rtag+':parent_readouts',[s['raw'][k] for k in rkeys],[old[k] for k in rkeys],scale=scale*scale);check(rtag+':parent_total',s['total'],old['total'],scale=scale)
            for method,z in (('spectral',s),('taylor',t)):
                p=np.asarray(z['powers']);d=z['derivatives'];mtag=rtag+':'+method
                check(mtag+':direct_commutators',p,z['direct_powers'],scale=scale*scale);check(mtag+':component_derivatives',p.sum(axis=1),d,scale=scale*scale);check(mtag+':antisymmetry',p+p.T,scale=scale*scale);check(mtag+':total_power',math.fsum(d),scale=scale*scale)
                check(mtag+':total_energy',math.fsum(z['energies']),z['total'],scale=scale);check(mtag+':number_power',z['number_rate']*OMEGA,d[3],scale=scale*scale);check(mtag+':carrier_current',z['carrier_rate'],z['native_carrier_rate'],scale=scale*scale)
            if tau==0.:check(rtag+':initial_components',s['energies'],[1.,0.,2.,2.,0.],scale=scale);check(rtag+':initial_total',s['total'],5.,scale=scale)
            row=dict(case=label,kappa=kappa,M=M,tau=tau,spectral=s,taylor=t);rows.append(row);lookup[desc]=row;vectors[desc]=v
    comparisons=[]
    for label,g,lr in CASES:
        for kappa in KAPPAS:
            for lo,hi in ((8,12),(12,16)):
                for tau in TIMES:
                    a=lookup[(label,kappa,lo,tau)];b=lookup[(label,kappa,hi,tau)];old=oldcomp[(label,kappa,lo,hi,tau)];signed={m:{f:(np.asarray(b[m][f])-np.asarray(a[m][f])).tolist() for f in ('energies','powers','derivatives')} for m in ('spectral','taylor')}
                    v=vectors[(label,kappa,lo,tau)];z=vectors[(label,kappa,hi,tau)];embedded=np.zeros_like(z);embedded[:,:lo+1]=v;err=float(np.linalg.norm(z-embedded));tag=f'cutoff:{label}:{kappa}:{lo}:{hi}:{tau}'
                    dif=signed['spectral']['energies'];check(tag+':parent_signed_energy',[math.fsum(dif[:3]),dif[3],dif[4]],[old['signed']['native'],old['signed']['photon_gain'],old['signed']['interaction']]);check(tag+':parent_joint_state_error',err,old['joint_state_error'])
                    comparisons.append(dict(case=label,kappa=kappa,M_low=lo,M_high=hi,tau=tau,signed=signed,joint_state_error=err,parent_comparison=old))
    if len(seen)!=27 or len(rows)!=135 or len(comparisons)!=90 or len(controls)!=3528:raise ValueError('Own locked census')
    if verify()!=inputs:raise RuntimeError('Input changed')
    failed=sum(not c['passed'] for c in controls);result=dict(name=NAME,owner='root',PID=os.getpid(),source_sha256=inputs[Path(__file__).name],inputs=inputs,started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,status='PASS' if not failed else 'FAIL',failed=failed,controls=controls,component_labels=list(LABELS),allowed_unordered_edges=[list(x) for x in EDGES],operators=operator_rows,rows=rows,comparisons=comparisons,parent_controls=parent['controls'],parent_physical_claims=parent['physical_claims'],absolute_initial_components=[1.,0.,2.,2.,0.],actuator_work=0.,physical_claims=dict(macroscopic_pressure_match=False,thermal_origin=False,matter_origin=False,outgoing_radiation=False,cosmology=False))
    report=f'# Saved native component exchange\n\n{result["status"]}: {len(controls)-failed}/{len(controls)} arithmetic/operator controls; all27 trials,135 spectral/Taylor state pairs and90 cutoff pairs retained.\n\nCarrier, record, link, bare-field and interaction terms form one inclusive energy ledger. Only the four declared operator edges exchange energy; the field communicates with native energy through the link term. This split does not allocate a macroscopic P(X) fluid or establish thermal/outgoing radiation. Original3348 controls and all physical claim dispositions remain retained.\n'
    write(OUTS[0],canonical(result));write(OUTS[1],report.encode())
    if verify()!=inputs:raise RuntimeError('Post-result input changed')
    own=dict(owner='root',PID=os.getpid(),started_utc=started,closed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,outputs={p.name:sha(p) for p in OUTS[:2]},status=result['status'],failed=failed,trials=27,states=135,comparisons=90,controls=3528,parent_controls=3348)
    write(OUTS[2],canonical(own))
    if verify()!=inputs or any(sha(BASE/n)!=h for n,h in own['outputs'].items()):raise RuntimeError('Post-publication seal')
    print(json.dumps(dict(status=result['status'],controls=len(controls),failed=failed,result_sha256=sha(OUTS[0]),receipt_sha256=sha(OUTS[2]))))
    return 0 if not failed else 3
if __name__=='__main__':raise SystemExit(main())
