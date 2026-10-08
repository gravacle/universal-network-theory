#!/usr/bin/env python3
"""Prospective exact polynomial check; only the root executor may freeze/run."""
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
THIS = J/'native_finite_gap_formation_exact_v001.py'
NOTE = J/'NATIVE_FINITE_GAP_FORMATION_V001.md'
PROTOCOL = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_PROTOCOL_V001.md'
FREEZE = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_FROZEN.json'
INTENT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_INTENT.json'
RESULT = J/'NATIVE_FINITE_GAP_FORMATION_EXACT_V001_RESULTS.json'
PINS = {
 J.parent/'recovered_sources/BS_MICRO_ACTION.md':'00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
 J/'NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md':'6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39',
 J/'NATIVE_COHERENT_WRITER_UNITALITY_V001.md':'882da1d5745a7b67dd16ed4c4b370f01fb590279ad00e801d1109d76ed01cfef',
 J/'NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md':'fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b',
 J/'NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_RESULT.md':'3133247093b1bba7096b5e049d88f88985c7c21401678b58902569359e286075',
 J/'NATIVE_CALORIMETER_ENERGY_ORIGIN_AND_RESONANT_PORT_V001.md':'1f8a0d04767f039ccc4af50b6f412129092cdcf8016e71c83d04893fb336b5fb',
}
CONFIG = dict(variables=['epsilon','g','lambda','nu'], matrix_dimension=4,
 order=6, initial_diagonal=['1/2','0','1/2','0'], coefficient_variable='u=tau/hbar',
 arithmetic='exact sparse multivariate Fraction polynomials', tolerances=None,
 cpu_soft_seconds=5,cpu_hard_seconds=6,cooperative_wall_seconds=10,
 external_wall_seconds=10,external_sampled_rss_bytes=268435456,
 maximum_terms_per_polynomial=4096,maximum_result_bytes=1048576)
DEADLINE = None
ZERO = (0,0,0,0)

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def bound(p):
    p=Path(p); r=p.resolve();need(r.is_relative_to(ROOT) and r==p,'Path ownership')
    return p
def raw(p): return bound(p).read_bytes()
def artifact(p):
    b=raw(p); return dict(path=str(p),bytes=len(b),sha256=sha(b))
def publish(p,b):
    p=bound(p);need(not p.exists(),'Exclusive publication refused')
    with tempfile.NamedTemporaryFile(prefix='.finite_gap_exact_',dir=J,delete=False) as f:
        temp=Path(f.name); f.write(b);f.flush();os.fsync(f.fileno())
    try: os.link(temp,p)
    finally: temp.unlink()
def frozen():
    files={}
    for p,h in PINS.items():
        a=artifact(p);need(a['sha256']==h,'Changed evidence '+str(p));files[str(p)]=h
    for p in (THIS,NOTE,PROTOCOL):files[str(p)]=artifact(p)['sha256']
    return dict(schema='NATIVE_FINITE_GAP_FORMATION_EXACT_FREEZE_V001',files=files,config=CONFIG)
def tick():
    if DEADLINE is not None: need(time.monotonic()<DEADLINE,'Cooperative time bound')
def clean(p):
    q={k:v for k,v in p.items() if v}
    need(len(q)<=CONFIG['maximum_terms_per_polynomial'],'Polynomial bound');return q
def mono(powers=ZERO,value=1):return {} if not value else {tuple(powers):F(value)}
def add(a,b):
    d=dict(a)
    for k,v in b.items():d[k]=d.get(k,F(0))+v
    return clean(d)
def scale(a,x):return clean({k:v*F(x) for k,v in a.items()})
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    tick();d={}
    for k,v in a.items():
        for l,w in b.items():
            m=tuple(x+y for x,y in zip(k,l));d[m]=d.get(m,F(0))+v*w
    return clean(d)
def serial(p):
    return [dict(powers=list(k),numerator=v.numerator,denominator=v.denominator) for k,v in sorted(p.items())]
def zeros(n=4):return [[{} for _ in range(n)] for _ in range(n)]
def ident(n=4):
    z=zeros(n)
    for i in range(n):z[i][i]=mono()
    return z
def madd(a,b):return [[add(x,y) for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def mscale(a,x):return [[scale(v,x) for v in r] for r in a]
def mmul(a,b):
    n=len(a);out=zeros(n)
    for i in range(n):
        for j in range(n):
            for k in range(n):out[i][j]=add(out[i][j],mul(a[i][k],b[k][j]))
    return out
def comm(a,b):return madd(mmul(a,b),mscale(mmul(b,a),-1))
def trace(a):
    r={}
    for i in range(len(a)):r=add(r,a[i][i])
    return r
def expectation(o,r):return trace(mmul(o,r))
def ptrace(r):return [[add(r[2*i][2*j],r[2*i+1][2*j+1]) for j in range(2)] for i in range(2)]
def transpose(r):return [list(x) for x in zip(*r)]
def mserial(a):return [[serial(v) for v in r] for r in a]
def atzero(p,var):return {k:v for k,v in p.items() if k[var]==0}

def calculate(out):
    eps,g,lam,nu=[mono(tuple(int(i==j) for i in range(4))) for j in range(4)]
    Hh=zeros();Hs=zeros();Hb=zeros();V=zeros();G=zeros();q=zeros()
    for i in (2,3):Hh[i][i]=eps;q[i][i]=mono()
    for i in (1,3):Hb[i][i]=nu
    G[0][2]=g;G[2][0]=g;G[1][3]=g;G[3][1]=g
    V[2][3]=lam;V[3][2]=lam
    Hs=madd(Hh,G);H=madd(madd(Hs,Hb),V)
    rho=zeros();rho[0][0]=mono(value=F(1,2));rho[2][2]=mono(value=F(1,2))
    observables=dict(q=q,held_energy=Hh,active_energy=Hs,fragment_energy=Hb,
                     copy_interaction=V,formation_energy=G,total_on_energy=H)
    out['hamiltonian_without_fixed_identity']=mserial(H)
    out['initial_density']=mserial(rho)
    out['checks']=checks=[];out['series']=series={k:[] for k in observables}
    out['reduced_density_coefficients']=[]
    def check(name,a,b):
        ok=a==b;checks.append(dict(name=name,passed=ok))
        if not ok:checks[-1]['actual']=a;checks[-1]['expected']=b
    def pc(name,a,b):check(name,serial(a),serial(b))
    def mc(name,a,b):check(name,mserial(a),mserial(b))
    mc('fixed_identity_commutes',comm(H,ident()),zeros())
    mc('held_q_source_commutator_zero',comm(Hh,q),zeros())
    pc('initial_trace_one',trace(rho),mono())
    pc('initial_copy_turn_on_work_zero',expectation(V,rho),{})
    pc('initial_formation_turn_on_work_zero',expectation(G,rho),{})
    C=rho;coeffs={k:[] for k in observables};reduced=[]
    for n in range(7):
        tick()
        if n:C=comm(H,C)
        part=ptrace(C);reduced.append(part)
        sign=(-1)**(n//2) if n%2==0 else (-1)**((n+1)//2)
        coeff=mscale(part,F(sign,math.factorial(n)))
        out['reduced_density_coefficients'].append(dict(order=n,
            factor='real' if n%2==0 else 'imaginary_i',matrix=mserial(coeff)))
        mc('commutator_transpose_order_'+str(n),transpose(C),mscale(C,(-1)**n))
        pc('trace_order_'+str(n),trace(C),mono() if n==0 else {})
        for name,O in observables.items():
            a=expectation(O,C)
            if n%2:pc('real_observable_odd_zero_'+name+'_'+str(n),a,{})
            c=scale(a,F(sign,math.factorial(n)));coeffs[name].append(c)
            series[name].append(dict(order=n,factor='real' if n%2==0 else 'imaginary_i',polynomial=serial(c)))
        if n:
            pc('on_energy_conservation_'+str(n),coeffs['total_on_energy'][n],{})
            pc('copy_switch_ledger_'+str(n),add(coeffs['active_energy'][n],coeffs['fragment_energy'][n]),scale(coeffs['copy_interaction'][n],-1))
            pc('both_switches_held_ledger_'+str(n),add(coeffs['held_energy'][n],coeffs['fragment_energy'][n]),scale(add(coeffs['copy_interaction'][n],coeffs['formation_energy'][n]),-1))
            for var in (1,2,3):
                mc('zero_parameter_reduced_identity_'+str(var)+'_'+str(n),
                   [[atzero(v,var) for v in r] for r in part],zeros(2))
    for n in range(1,4):mc('reduced_orders_below_four_'+str(n),reduced[n],zeros(2))
    r4=zeros(2);r4[0][1]=mono((0,1,2,1),-2);r4[1][0]=mono((0,1,2,1),-2)
    mc('fourth_nested_reduced_commutator_for_I_over_two',reduced[4],r4)
    pc('fragment_energy_order_two',coeffs['fragment_energy'][2],mono((0,0,2,1),F(1,2)))
    pc('active_energy_order_four',coeffs['active_energy'][4],mono((0,2,2,1),F(-1,6)))
    pc('formation_off_order_four',scale(coeffs['formation_energy'][4],-1),mono((0,2,2,1),F(1,6)))
    for n in range(1,6):pc('held_population_below_six_'+str(n),coeffs['q'][n],{})
    pc('held_population_order_six',coeffs['q'][6],mono((1,2,2,1),F(-1,72)))
    pc('held_energy_order_six',coeffs['held_energy'][6],mono((2,2,2,1),F(-1,72)))
    out['check_count']=len(checks);out['failure_count']=sum(not r['passed'] for r in checks)
    out['switch_off_series']={name:[dict(order=n,polynomial=serial(scale(coeffs[obs][n],-1))) for n in range(7)]
                            for name,obs in [('copy','copy_interaction'),('formation','formation_energy')]}
    out['classification']=dict(nonunital_at_four_verified=reduced[4]==r4,
        active_energy_order_four_identity_verified=coeffs['active_energy'][4]==mono((0,2,2,1),F(-1,6)),
        held_population_first_nonzero_generic_order=next((n for n in range(1,7) if coeffs['q'][n]),None),
        held_energy_first_nonzero_generic_order=next((n for n in range(1,7) if coeffs['held_energy'][n]),None),
        nu_nonnegative_required_for_stated_sign=True,epsilon_unrestricted=True,
        coefficient_identity_passed=out['failure_count']==0,
        stationary_attractor_established=False,physical_density_identified=False,
        absolute_volume_or_source_completion=False,held_q_retarded_response_nonzero=False)
    need(out['failure_count']==0,'Exact polynomial check failed; coefficients retained')

def main():
    global DEADLINE
    need(Path.cwd().resolve()==ROOT and Path(__file__).resolve()==THIS,'Fixed workspace/source')
    need(sys.argv[1:] in (['freeze'],['run']),'One operation: freeze or run')
    f=frozen()
    if sys.argv[1]=='freeze':
        need(not INTENT.exists() and not RESULT.exists(),'Attempt predates freeze')
        publish(FREEZE,enc(f)+b'\n');print(enc(artifact(FREEZE)).decode());return 0
    need(json.loads(raw(FREEZE))==f,'Changed freeze/source/input')
    need(not INTENT.exists() and not RESULT.exists(),'No implicit retry or overwrite')
    intent=dict(schema='NATIVE_FINITE_GAP_FORMATION_EXACT_INTENT_V001',source_sha256=sha(raw(THIS)),
                freeze_sha256=sha(raw(FREEZE)),target=str(RESULT),config=CONFIG)
    publish(INTENT,enc(intent)+b'\n')
    out=dict(status='EXACT_CHECK_FAILED_RETAINED',intent=artifact(INTENT),inputs=f['files'],
      numerical_propagation=False,observational_fit=False,physical_qualification=False,
      formed_state_established=False,thermal_qualified=False,Stage3_complete=False)
    try:
        resource.setrlimit(resource.RLIMIT_CPU,(CONFIG['cpu_soft_seconds'],CONFIG['cpu_hard_seconds']))
        DEADLINE=time.monotonic()+CONFIG['cooperative_wall_seconds']
        calculate(out)
        need(frozen()==f,'Changed end inputs')
        out['status']='EXACT_POLYNOMIAL_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION'
    except BaseException:out['error']=traceback.format_exc()
    wrapped=dict(schema='NATIVE_FINITE_GAP_FORMATION_EXACT_RESULT_V001',freeze_sha256=sha(raw(FREEZE)),
                 payload_sha256=sha(enc(out)),payload=out)
    b=enc(wrapped)+b'\n';need(len(b)<=CONFIG['maximum_result_bytes'],'Bounded result size')
    publish(RESULT,b);a=artifact(RESULT);a['status']=out['status'];print(enc(a).decode())
    return int(out['status']=='EXACT_CHECK_FAILED_RETAINED')
if __name__=='__main__':sys.exit(main())
