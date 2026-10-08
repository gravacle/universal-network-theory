#!/usr/bin/env python3
"""Inert prospective source-algebra check. Root alone may freeze and execute."""
import hashlib
import json
import math
import os
from pathlib import Path
from fractions import Fraction as F
import resource
import sys
import tempfile
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'native_finite_fragment_source_exact_v001.py'
NOTE = J/'NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md'
PROTOCOL = J/'NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_PROTOCOL_V001.md'
FREEZE = J/'NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_FROZEN.json'
INTENT = J/'NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_INTENT.json'
RESULT = J/'NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_RESULTS.json'
PINS = {
 J/'native_autonomous_volume_formation_v001.py':'8cdffaded72a83d6117dd0bf61e944d1c5b9f0e8800e4a7f2dd36ff477175317',
 J/'NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md':'724f8d8c4a7bbcc7ce4ba9fa37f750e92d96b732db78ef1cc1347fcd52a7a7d5',
 J/'NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md':'81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96',
 J/'NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_REVIEW_INDEPENDENT_V001.md':'f4fc58088118d483c5ca5216c885b2a5bcfa7f9b481d53cfa05dcd165b094483',
}
CONFIG = dict(dimension=384, order=4, variables=['a','lambda','nu'],
 field='Q[a]/(a^3-2), a is the positive real cube root of 2',
 state_order=['Q3','C2','rL2','rR2','n2','carrier2','bL2','bR2'],
 preparations=['A_Qminus','A_Qplus','B_Qminus','B_Qplus'],
 inherited_J_Omega_g=[1,1,1], source_scale='Z=gamma0*z, gamma0 symbolic',
 coefficient_variable='u=t/hbar; S/gamma0^2=hbar^-2 sum m_n*u^n',
 tolerances=None, maximum_total_symbol_degree=7, maximum_terms_per_polynomial=128,
 maximum_fraction_bits=512, maximum_monomial_products=3000000,
 maximum_operator_entries=10000, maximum_result_bytes=2097152,
 cpu_soft_seconds=30,cpu_hard_seconds=35,cooperative_wall_seconds=45,
 external_wall_seconds=45,external_sampled_rss_bytes=268435456)
N = 384
DEADLINE = None
PRODUCTS = 0
MAX_TERMS = 0
MAX_VECTOR = 0

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def bound(p):
    p=Path(p);r=p.resolve();need(r==p and r.is_relative_to(ROOT),'Path ownership');return p
def raw(p):
    b=bound(p).read_bytes();need(len(b)<=4194304,'Bounded source/input');return b
def art(p):
    b=raw(p);return dict(path=str(p),bytes=len(b),sha256=sha(b))
def publish(p,b):
    need(len(b)<=CONFIG['maximum_result_bytes'],'Publication size')
    p=bound(p);need(not p.exists(),'Exclusive publication refused')
    with tempfile.NamedTemporaryFile(prefix='.fragment_exact_',dir=J,delete=False) as f:
        tmp=Path(f.name);f.write(b);f.flush();os.fsync(f.fileno())
    try:os.link(tmp,p)
    finally:tmp.unlink()
def frozen():
    files={}
    for p,h in PINS.items():
        need(art(p)['sha256']==h,'Changed pinned source '+str(p));files[str(p)]=h
    for p in (THIS,NOTE,PROTOCOL):files[str(p)]=art(p)['sha256']
    return dict(schema='NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_FREEZE_V001',files=files,config=CONFIG)
def tick():
    if DEADLINE is not None:need(time.monotonic()<DEADLINE,'Cooperative wall bound')
def clean(p):
    global MAX_TERMS
    p={k:v for k,v in p.items() if v}
    need(len(p)<=CONFIG['maximum_terms_per_polynomial'],'Polynomial term bound')
    for (a,l,n),v in p.items():
        need(0<=a<3 and l>=0 and n>=0 and l+n<=7,'Canonical field/degree bound')
        need(max(abs(v.numerator).bit_length(),v.denominator.bit_length())<=512,'Rational bit bound')
    MAX_TERMS=max(MAX_TERMS,len(p));return p
def mono(a=0,l=0,n=0,value=1):
    q,r=divmod(a,3);return clean({(r,l,n):F(value)*2**q}) if value else {}
def const(x):return mono(value=x)
def add(p,q):
    d=dict(p)
    for k,v in q.items():d[k]=d.get(k,F(0))+v
    return clean(d)
def scale(p,x):return clean({k:v*F(x) for k,v in p.items()})
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    global PRODUCTS
    tick();d={};PRODUCTS+=len(p)*len(q)
    need(PRODUCTS<=CONFIG['maximum_monomial_products'],'Exact operation budget')
    for (a,l,n),v in p.items():
        for (b,k,m),w in q.items():
            carry,r=divmod(a+b,3);key=(r,l+k,n+m)
            d[key]=d.get(key,F(0))+v*w*2**carry
    return clean(d)
def ser(p):return [dict(a_power=a,lambda_power=l,nu_power=n,numerator=v.numerator,denominator=v.denominator) for (a,l,n),v in sorted(p.items())]
def zero_lam(p):return {k:v for k,v in p.items() if k[1]==0}
def vec_clean(v):
    global MAX_VECTOR
    v={k:p for k,p in v.items() if p};need(len(v)<=N and all(0<=k<N for k in v),'Vector bound')
    MAX_VECTOR=max(MAX_VECTOR,len(v));return v
def vadd(v,w,factor=1):
    d=dict(v)
    for k,p in w.items():d[k]=add(d.get(k,{}),scale(p,factor))
    return vec_clean(d)
def vmul(v,p):return vec_clean({k:mul(x,p) for k,x in v.items()})
def inner(v,w):
    p={}
    for k in v.keys() & w.keys():p=add(p,mul(v[k],w[k]))
    return p
def basis(i):return {i:const(1)}
def op():return [{} for _ in range(N)]
def put(o,col,row,p):
    if p:o[col][row]=add(o[col].get(row,{}),p)
def finish(o):
    o=[vec_clean(c) for c in o];need(sum(map(len,o))<=CONFIG['maximum_operator_entries'],'Operator support bound');return o
def plus(*operators):
    z=op()
    for o in operators:
        for col,rows in enumerate(o):
            for row,p in rows.items():put(z,col,row,p)
    return finish(z)
def act(o,v):
    tick();out={}
    for col,p in v.items():
        for row,q in o[col].items():out[row]=add(out.get(row,{}),mul(q,p))
    return vec_clean(out)
def jact(h,z,v):return vadd(act(h,act(z,v)),act(z,act(h,v)),-1)
def mact(h,z,v):return vadd(act(z,jact(h,z,v)),jact(h,z,act(z,v)),-1)
def decode(i):
    Q,bits=divmod(i,128)
    return (Q,)+tuple((bits>>k)&1 for k in range(6,-1,-1))
S=(mono(a=2,value=F(1,2)),const(1),mono(a=1))
SI=(mono(a=1),const(1),mono(a=2,value=F(1,2)))
S3=(const(F(1,2)),const(1),const(2))
LAM=mono(l=1)
NU=mono(n=1)

def build(family,extended):
    pieces={k:op() for k in ('HQ','HC','native','formation','gap','copy')}
    z=op();hq=op();sop=op();fd=op();r=op();nb=op();acorrection=op()
    for i in range(N):
        Q,C,L,R,n,c,bL,bR=decode(i);s,si=S[Q],SI[Q];rec=L+R
        put(pieces['HQ'],i,i,const(1 if Q in (0,2) else 2))
        put(hq,i,i,const(1 if Q in (0,2) else 2))
        for q2 in (Q-1,Q+1):
            if 0<=q2<3:
                put(pieces['HQ'],i,i+(q2-Q)*128,const(-1));put(hq,i,i+(q2-Q)*128,const(-1))
        put(pieces['HC'],i,i,const(1));put(pieces['HC'],i,i^64,const(-1))
        put(sop,i,i,s);put(r,i,i,const(rec));put(nb,i,i,const(bL+bR))
        if family=='A':
            diagonal=scale(si,F(3+rec)+n*(F(9,4)-F(rec,2)))
            incidence=scale(si,-1);carrier=scale(si,F(-n,2));formation=si
            zd=const((1+F(n,4))*(2*c-1)+(1-F(n,2))*(R-L));zf=const(1)
        else:
            diagonal=add(const(1+rec+n*(2-F(rec,2))),add(scale(si,F(n,4)),scale(S3[Q],2)))
            incidence=const(-1);carrier=scale(si,F(-n,2));formation=const(1)
            zd=add(scale(add(s,const(F(n,4))),2*c-1),scale(s,(1-F(n,2))*(R-L)));zf=s
        put(pieces['native'],i,i,diagonal);put(pieces['native'],i,i^8,incidence)
        put(pieces['native'],i,i^4,carrier)
        if C:
            for mask,sign in ((32,-1),(16,1)):
                put(pieces['formation'],i,i^mask,formation);put(z,i,i^mask,scale(zf,sign))
        put(z,i,i,zd)
        put(fd,i,i,scale(NU,bR-bL))
        if L:put(fd,i,i^2,scale(LAM,-1))
        if R:put(fd,i,i^1,LAM)
        for occupied,rmask,bmask in ((L,32,2),(R,16,1)):
            # -lambda*Y_C*Y_r*X_b has real coefficient +lambda*(-1)^(C+r).
            put(acorrection,i,i^64^rmask^bmask,scale(LAM,(-1)**(C+occupied)))
        if extended:
            f=si if family=='A' else const(1)
            put(pieces['gap'],i,i,scale(mul(f,NU),bL+bR))
            if L:put(pieces['copy'],i,i^2,mul(f,LAM))
            if R:put(pieces['copy'],i,i^1,mul(f,LAM))
            for row,p in fd[i].items():put(z,i,row,mul(zf,p))
    pieces={k:finish(v) for k,v in pieces.items()}
    parent=plus(*(pieces[k] for k in ('HQ','HC','native','formation')))
    h=plus(parent,pieces['gap'],pieces['copy'])
    return dict(H=h,Z=finish(z),parent=parent,gap=pieces['gap'],copy=pieces['copy'],
                HQ=finish(hq),s=finish(sop),Fd=finish(fd),R=finish(r),Nb=finish(nb),
                A_correction=finish(acorrection),components=pieces)

def calculate(out):
    checks=out['checks']=[];cases=out['cases']=[]
    def check(name,ok,detail=None):
        row=dict(name=name,passed=bool(ok))
        if not ok and detail is not None:row['difference']=detail
        checks.append(row)
    def pc(name,p,q):check(name,p==q,ser(sub(p,q)))
    def vc(name,v,w):
        d=vadd(v,w,-1);check(name,not d,[dict(index=i,polynomial=ser(p)) for i,p in sorted(d.items())])
    # Independent elementary field identities precede physical operators.
    pc('positive_root_field_a_cubed',mul(mono(a=2),mono(a=1)),const(2))
    for q in range(3):pc('inverse_scale_'+str(q),mul(S[q],SI[q]),const(1))
    models={(f,e):build(f,e) for f in ('A','B') for e in (False,True)}
    for (family,extended),m in models.items():
        for label in ('H','Z','parent','gap','copy','R','Nb'):
            o=m[label];ok=all(p==o[row].get(col,{}) for col,rows in enumerate(o) for row,p in rows.items())
            check('real_symmetric_'+family+'_'+str(extended)+'_'+label,ok)
    # These current identities are checked on EVERY basis column, not sampled.
    for family in ('A','B'):
        old=models[family,False];new=models[family,True];ok=True;first=None
        for i in range(N):
            v=basis(i);d=vadd(jact(new['H'],new['Z'],v),jact(old['H'],old['Z'],v),-1)
            if family=='B':
                fv=act(new['Fd'],v)
                rem=vadd(act(new['HQ'],act(new['s'],fv)),act(new['s'],act(new['HQ'],fv)),-1)
                d=vadd(d,rem,-1)
            if d and first is None:first=dict(column=i,residual=[dict(index=j,polynomial=ser(p)) for j,p in sorted(d.items())])
            ok=ok and not d
        check('all_384_columns_current_identity_'+family,ok,first)
    for family in ('A','B'):
        for Q in (0,2):
            pair={}
            for extended in (False,True):
                m=models[family,extended];h,z=m['H'],m['Z'];psi=basis(Q*128+64)
                label=family+'_Q'+str(Q)+'_'+('extended' if extended else 'original')
                row=dict(label=label,Q_index=Q,extended=extended,series={},moment_commutator_series=[])
                cases.append(row);v=[psi]
                for k in range(5):v.append(act(h,v[-1]))
                zv=[act(z,w) for w in v[:5]];zzv=[act(z,w) for w in zv];hzv=[act(h,w) for w in zv]
                def series(bilinear,label2):
                    result=[]
                    for order in range(5):
                        real={};imag={}
                        for k in range(order+1):
                            j=order-k;p=scale(bilinear(j,k),F((-1)**k,math.factorial(j)*math.factorial(k)))
                            if order%2==0:real=add(real,scale(p,(-1)**(order//2)))
                            else:imag=add(imag,scale(p,(-1)**((order-1)//2)))
                        pc('imaginary_expectation_zero_'+label+'_'+label2+'_'+str(order),imag,{})
                        if order%2:pc('odd_expectation_zero_'+label+'_'+label2+'_'+str(order),real,{})
                        result.append(real)
                    row['series'][label2]=[dict(order=k,polynomial=ser(p)) for k,p in enumerate(result)]
                    return result
                def moment(j,k):
                    return sub(sub(scale(inner(zv[j],hzv[k]),2),inner(zzv[j],v[k+1])),inner(v[j+1],zzv[k]))
                moments=series(moment,'signed_moment');pair[extended]=moments
                # Independent nested commutators use operator actions, not the
                # bilinear moment formula or its factorial convolution.
                memo={}
                def nested(n,k):
                    key=(n,k)
                    if key not in memo:
                        memo[key]=mact(h,z,v[k]) if n==0 else vadd(act(h,nested(n-1,k)),nested(n-1,k+1),-1)
                    return memo[key]
                for n in range(5):
                    p=nested(n,0).get(Q*128+64,{})
                    if n%2:pc('odd_nested_commutator_'+label+'_'+str(n),p,{});c={}
                    else:c=scale(p,F((-1)**(n//2),math.factorial(n)))
                    pc('independent_moment_coefficient_'+label+'_'+str(n),c,moments[n])
                    row['moment_commutator_series'].append(dict(order=n,polynomial=ser(c)))
                norm=series(lambda j,k:inner(v[j],v[k]),'norm')
                obs={}
                for name in ('H','parent','gap','copy','R','Nb'):
                    ov=[act(m[name],w) for w in v[:5]]
                    obs[name]=series(lambda j,k:inner(v[j],ov[k]),name)
                for n in range(5):
                    pc('norm_'+label+'_'+str(n),norm[n],const(1) if n==0 else {})
                    pc('complete_energy_ledger_'+label+'_'+str(n),obs['H'][n],add(obs['parent'][n],add(obs['gap'][n],obs['copy'][n])))
                    if n:pc('closed_energy_'+label+'_'+str(n),obs['H'][n],{})
                e0=add(const(2),scale(SI[Q],3)) if family=='A' else add(const(3),scale(S3[Q],2))
                pc('absolute_initial_energy_'+label,obs['H'][0],e0)
                pc('initial_source_moment_'+label,moments[0],{})
                f=SI[Q] if family=='A' else const(1)
                pc('original_blank_R_order2_'+label,obs['R'][2],scale(mul(f,f),2))
                pc('blank_fragment_order0_'+label,obs['Nb'][0],{})
                pc('blank_fragment_order2_'+label,obs['Nb'][2],{})
                expected=scale(mul(mul(mul(f,f),mul(f,f)),mul(LAM,LAM)),F(1,2)) if extended else {}
                pc('fragment_population_order4_'+label,obs['Nb'][4],expected)
                if family=='A' and extended:
                    old=models[family,False]
                    for k in (0,1):
                        delta=vadd(mact(h,z,v[k]),mact(old['H'],old['Z'],v[k]),-1)
                        vc('A_Pauli_moment_identity_on_power_'+str(Q)+'_'+str(k),delta,act(m['A_correction'],v[k]))
            differences=[sub(pair[True][n],pair[False][n]) for n in range(5)]
            out.setdefault('differences',[]).append(dict(family=family,Q_index=Q,
                coefficients=[dict(order=n,polynomial=ser(p)) for n,p in enumerate(differences)],
                fourth_order_identically_zero=not differences[4],sign_not_evaluated=True))
            for n in range(5):pc('lambda_zero_moment_'+family+'_'+str(Q)+'_'+str(n),zero_lam(pair[True][n]),pair[False][n])
            for n in (0,2):pc('unchanged_leading_moment_'+family+'_'+str(Q)+'_'+str(n),differences[n],{})
    out['check_count']=len(checks);out['failure_count']=sum(not r['passed'] for r in checks)
    out['algebra_usage']=dict(monomial_products=PRODUCTS,maximum_terms=MAX_TERMS,maximum_vector_support=MAX_VECTOR)
    out['coverage']=dict(current_operator_identities='all 384 basis columns per A/B',
        A_Pauli_moment_identity='two original endpoint blanks and each first H-power only',
        moment_series='all original/extended four preparations through order 4, two methods',
        no_full_matrix_export=True,no_finite_time_value=True,no_sign_gate=True)
    need(out['failure_count']==0,'Exact identity mismatch; actual coefficients retained')

def main():
    global DEADLINE
    need(Path.cwd().resolve()==ROOT and Path(__file__).resolve()==THIS,'Fixed source/workspace')
    need(sys.argv[1:] in (['freeze'],['run']),'Operation must be freeze or run')
    f=frozen()
    if sys.argv[1]=='freeze':
        need(not INTENT.exists() and not RESULT.exists(),'Attempt predates freeze')
        publish(FREEZE,enc(f)+b'\n');print(enc(art(FREEZE)).decode());return 0
    need(json.loads(raw(FREEZE))==f,'Freeze/source/input changed')
    need(not INTENT.exists() and not RESULT.exists(),'No implicit retry/overwrite')
    freeze_hash=sha(raw(FREEZE));source_hash=sha(raw(THIS))
    publish(INTENT,enc(dict(schema='NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_INTENT_V001',source_sha256=source_hash,
        freeze_sha256=freeze_hash,target=str(RESULT),config=CONFIG))+b'\n')
    out=dict(status='EXACT_SOURCE_CHECK_FAILED_RETAINED',intent=art(INTENT),inputs=f['files'],
        numerical_propagation=False,observational_fit=False,physical_qualification=False,
        formed_state_established=False,passivity_established=False,thermal_qualified=False,
        propagation_allowed=False,Stage3_complete=False)
    try:
        resource.setrlimit(resource.RLIMIT_CPU,(30,35));DEADLINE=time.monotonic()+45
        calculate(out);need(frozen()==f,'Changed end source/input pins')
        out['status']='EXACT_SOURCE_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION'
    except BaseException:
        out['error']=traceback.format_exc()
        out['algebra_usage_on_exit']=dict(monomial_products=PRODUCTS,maximum_terms=MAX_TERMS,maximum_vector_support=MAX_VECTOR)
    wrapped=dict(schema='NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_RESULT_V001',freeze_sha256=freeze_hash,
        payload_sha256=sha(enc(out)),payload=out)
    data=enc(wrapped)+b'\n';publish(RESULT,data)
    print(enc(dict(path=str(RESULT),bytes=len(data),sha256=sha(data),status=out['status'])).decode())
    return int(out['status']=='EXACT_SOURCE_CHECK_FAILED_RETAINED')
if __name__=='__main__':sys.exit(main())
