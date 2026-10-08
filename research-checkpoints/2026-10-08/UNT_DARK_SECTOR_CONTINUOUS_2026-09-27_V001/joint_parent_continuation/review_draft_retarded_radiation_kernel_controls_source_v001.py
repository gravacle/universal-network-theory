"""Prospective radiation-panel kernel arithmetic. Root --execute only.
Reusable helpers have no legacy imports, calibration or top-level quadrature.
This is not a coupled metric/radiation trajectory or a galaxy prediction.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import time
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001'
PROTOCOL_SHA='41382651db10e971712455adea35a512d41e805907a83e508c5a54f3c78cee58'
PINS={'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V001.md':'0a2a64f56ee544cd0b4f0c0ce21240fb8d4cde7ebcb877231519e6f02fade639',
      'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md':'1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2',
      'constrained_u_clock_gradient_early_transfer_v004.py':'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07'}
PHASES=(0.,.125,1.,4.,16.,64.)
OPACITIES=(0.,1e-8,.1,1.,10.,48.,100.,1e6)
BESSEL_X=(0.,.125,1.,3.999,4.,8.,16.,32.,64.)
SI_X=(0.,.125,1.,4.,7.999,8.,8.001,16.,64.,256.,4096.,100000.)
PRIMITIVE_STARTS=(0.,4.,8.,64.,4096.,100000.)
PRIMITIVE_WIDTHS=(.25,1.,4.)
CFG=dict(panel_tolerance=2e-10,bessel_tolerance=2e-11,primitive_tolerance=2e-11,
         reality_tolerance=2e-12,endpoint_tolerance=5e-15,
         phase_values=list(PHASES),opacity_values=list(OPACITIES),
         panel_orders=[16,32],angular_orders=[128,256],
         series_terms=52,laplace_limit=64.,opacity_limit=48.,source_powers=[0,1,2],
         multipoles=[0,1,2],derivatives=[0,1,2,3],kernel_rows=1728,
         bessel_rows=108,primitive_increment_rows=54,checkpoint_count=10)
ROW_FIELDS=['phase','opacity','l','r','p','panel16','panel32','angular128_real',
            'angular128_imag','angular256_real','angular256_imag','tail_bound']
SEALS={}
CREATED={}
SOURCE_SHA=''
MANIFEST_SHA=''
QUADRATURE={}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def encoded(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,value):
    raw=encoded(value);p=BASE/name
    with p.open('xb') as f:f.write(raw)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h;return h
def recheck():
    if sha(__file__)!=SOURCE_SHA:raise AssertionError('Changed worker source')
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed sealed input/output '+p)
def journal(event,**data):
    obj=dict(event=event,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,
             manifest_sha256=MANIFEST_SHA,time=now(),**data)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('ab') as f:f.write(encoded(obj))

class Checks:
    def __init__(self):self.rows=[]
    def check(self,name,a,b=0.,tol=0.,scale=1.,tag=''):
        error=float(abs(a-b)/scale)
        self.rows.append(dict(name=name,tag=tag,error=error,tolerance=float(tol),
                              scale=float(scale),passed=bool(math.isfinite(error) and error<=tol)))
    def result(self):
        return dict(count=len(self.rows),failed=sum(not r['passed'] for r in self.rows),rows=self.rows)

def gauss(n,kind='legendre'):
    key=(kind,n)
    if key not in QUADRATURE:
        QUADRATURE[key]=(np.polynomial.legendre.leggauss(n) if kind=='legendre'
                         else np.polynomial.laguerre.laggauss(n))
    return QUADRATURE[key]

def polynomial(l,mu):
    if l==0:return np.ones_like(mu)
    if l==1:return mu
    if l==2:return (3*mu*mu-1)/2
    raise ValueError('Frozen low-moment kernel only')

def bessel(l,r,x):
    """Literal differentiated factorial/sin-cos forms; x may be an array."""
    x=np.asarray(x,dtype=float);ax=abs(x);out=np.zeros_like(ax);small=ax<4
    v=ax[small];coef=1./math.prod(range(1,2*l+2,2));ans=np.zeros_like(v)
    for m in range(CFG['series_terms']):
        power=l+2*m
        if power>=r:
            falling=math.prod(range(power-r+1,power+1)) if r else 1
            ans+=coef*falling*v**(power-r)
        coef/=-2*(m+1)*(2*l+2*(m+1)+1)
    out[small]=ans
    s,c=({-1:1.},{} ) if l==0 else ({-2:1.},{-1:-1.}) if l==1 else ({-3:3.,-1:-1.},{-2:-3.})
    for _ in range(r):
        sn={};cn={}
        for power,a in s.items():
            sn[power-1]=sn.get(power-1,0.)+power*a;cn[power]=cn.get(power,0.)+a
        for power,a in c.items():
            cn[power-1]=cn.get(power-1,0.)+power*a;sn[power]=sn.get(power,0.)-a
        s,c=sn,cn
    v=ax[~small]
    sv=sum(a*v**p for p,a in s.items());cv=sum(a*v**p for p,a in c.items())
    out[~small]=sv*np.sin(v)+cv*np.cos(v)
    return out*np.where(x<0,(-1)**(l+r),1)

def angular_bessel(l,r,x,n):
    mu,w=gauss(n);x=np.asarray(x,dtype=float)
    return (1j**l/2)*np.exp(-1j*x[...,None]*mu)@ (w*polynomial(l,mu)*(-1j*mu)**r)

def complex_moment(p,z):
    z=np.asarray(z,dtype=complex);out=np.zeros_like(z);small=abs(z)<1
    v=z[small];term=np.ones_like(v);ans=np.zeros_like(v)
    for m in range(CFG['series_terms']):
        ans+=term/(m+p+1);term*=-v/(m+1)
    out[small]=ans
    v=z[~small];end=np.exp(-v);value=-np.expm1(-v)/v
    for order in range(1,p+1):value=(order*value-end)/v
    out[~small]=value;return out

def angular_panel(l,r,p,a,b,n):
    mu,w=gauss(n);moment=complex_moment(p,a+1j*b*mu)
    return complex((1j**l/2)*np.dot(w*polynomial(l,mu)*(-1j*mu)**r,moment))

def panel(l,r,p,a,b,n):
    """Normalized Delta=1 panel; returns integral and explicit opacity tail."""
    u,w=gauss(n);limit=min(a,CFG['opacity_limit']) if a>CFG['opacity_limit'] else 1.
    rate=max(1.,b/a) if a>CFG['opacity_limit'] else max(1.,a,b)
    pieces=max(1,math.ceil(limit*rate/8));parts=[]
    for i in range(pieces):
        left=limit*i/pieces;right=limit*(i+1)/pieces;t=(left+right)/2+(right-left)*u/2
        v=t/a if a>CFG['opacity_limit'] else t
        jac=1/a if a>CFG['opacity_limit'] else 1.
        parts.append(float((right-left)*jac/2*np.dot(w,np.exp(-a*v)*v**p*bessel(l,r,b*v))))
    tail=math.exp(-CFG['opacity_limit'])/a if a>CFG['opacity_limit'] else 0.
    return math.fsum(parts),tail

def sine_integral(x,n=64,independent=False):
    if abs(x)<=8:
        return math.fsum((-1)**m*x**(2*m+1)/((2*m+1)*math.factorial(2*m+1))
                         for m in range(CFG['series_terms'])),0.
    sign=1 if x>0 else -1;x=abs(x)
    if not independent:
        u,w=gauss(n,'laguerre');f=float(np.dot(w,1/(1+(u/x)**2)))/x
        g=float(np.dot(w,u/(1+(u/x)**2)))/(x*x);tail=0.
    else:
        u,w=gauss(n);fs=[];gs=[]
        for left in range(0,64,4):
            t=left+2+2*u;weight=2*w*np.exp(-t)/(1+(t/x)**2)
            fs.append(float(sum(weight))/x);gs.append(float(np.dot(weight,t))/(x*x))
        f=math.fsum(fs);g=math.fsum(gs);tail=math.exp(-64)*(1/x+65/(x*x))
    return sign*(math.pi/2-math.cos(x)*f-math.sin(x)*g),tail

def primitive(l,x):
    si,_=sine_integral(x)
    if l==0:return si
    if l==1:return -float(bessel(0,0,x))
    return si/2-1.5*float(bessel(1,0,x))

def checkpoint(stage,index,rows,checks,fields):
    payload=dict(stage=stage,index=index,row_fields=fields,rows=rows,checks=checks.result())
    if payload['checks']['failed']:status='FAILED_ARITHMETIC'
    else:status='PASS_ARITHMETIC'
    pn=STEM+f'_CP{index:02d}.json';cn=STEM+f'_CP{index:02d}_COMMIT.json';h=write(pn,payload)
    ch=write(cn,dict(stage=stage,index=index,status=status,payload=pn,payload_sha256=h,
                     source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,owner='root',pid=os.getpid()))
    journal('CHECKPOINT',stage=stage,index=index,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch)
    recheck();return dict(stage=stage,index=index,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch,
                         row_count=len(rows),check_count=len(checks.rows),failed=payload['checks']['failed'])

def verify_prefix(refs):
    events=[json.loads(x) for x in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    if len(events)!=11 or events[0]['event']!='OWNER_START' or len(refs)!=10:raise AssertionError('Full root/checkpoint census')
    for ev in events:
        if (ev['owner'],ev['pid'],ev['source_sha256'],ev['manifest_sha256'])!=('root',os.getpid(),SOURCE_SHA,MANIFEST_SHA):raise AssertionError('Owner/source/manifest identity')
    for i,(ev,ref) in enumerate(zip(events[1:],refs)):
        if ev['event']!='CHECKPOINT' or any(ev[k]!=ref[k] for k in ('index','stage','payload','payload_sha256','commit','commit_sha256')) or ref['index']!=i:raise AssertionError('Ordered checkpoint identity')
        co=json.loads((BASE/ref['commit']).read_text());pl=json.loads((BASE/ref['payload']).read_text())
        if sha(BASE/ref['payload'])!=ref['payload_sha256'] or sha(BASE/ref['commit'])!=ref['commit_sha256']:raise AssertionError('Complete checkpoint byte hashes')
        if co!=dict(stage=ref['stage'],index=i,status='FAILED_ARITHMETIC' if ref['failed'] else 'PASS_ARITHMETIC',payload=ref['payload'],payload_sha256=ref['payload_sha256'],source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,owner='root',pid=os.getpid()):raise AssertionError('Commit schema')
        if pl['stage']!=ref['stage'] or pl['index']!=i or len(pl['rows'])!=ref['row_count'] or len(pl['checks']['rows'])!=ref['check_count'] or pl['checks']['count']!=ref['check_count'] or pl['checks']['failed']!=ref['failed']:raise AssertionError('Committed payload schema/census')
    expected={STEM+'_MANIFEST.json',STEM+'_JOURNAL.jsonl'}|{r[k] for r in refs for k in ('payload','commit')}
    if {p.name for p in BASE.glob(STEM+'_*')}!=expected:raise AssertionError('Orphan runtime prefix')

def main():
    global SOURCE_SHA,MANIFEST_SHA
    tick=time.monotonic();SOURCE_SHA=sha(__file__)
    for name,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():
        if sha(BASE/name)!=h:raise AssertionError('Input pin '+name)
        SEALS[str((BASE/name).resolve())]=h
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',dict(source_sha256=SOURCE_SHA,input_sha256=SEALS,configuration=CFG,numpy_version=np.__version__,scope='Mathematical kernel arithmetic only; no physical history or coupled trajectory'))
    journal('OWNER_START');refs=[];checks=Checks();rows=[]
    for x in BESSEL_X:
        for l in range(3):
            for r in range(4):
                f=float(bessel(l,r,x));a=complex(angular_bessel(l,r,x,256));rows.append([x,l,r,f,a.real,a.imag])
                checks.check('bessel_angular',f,a.real,CFG['bessel_tolerance'],1+abs(a),f'{x}:{l}:{r}');checks.check('bessel_reality',a.imag,tol=CFG['reality_tolerance'])
    for l,r,value in ((0,0,1.),(0,1,0.),(0,2,-1/3),(0,3,0.),(1,0,0.),(1,1,1/3),(1,2,0.),(1,3,-1/5),(2,0,0.),(2,1,0.),(2,2,2/15),(2,3,0.)):
        checks.check('zero_endpoint',float(bessel(l,r,0.)),value,CFG['endpoint_tolerance'])
    for name,l,value,pol in (('photon_quad_monopole',0,0.,False),('photon_quad_quadrupole',2,.1,False),('polarization_monopole',0,.5,True),('polarization_quadrupole',2,.1,True)):
        actual=(.75*(float(bessel(l,0,0.))+float(bessel(l,2,0.))) if pol else .25*(float(bessel(l,0,0.))+3*float(bessel(l,2,0.))))
        checks.check(name,actual,value,CFG['endpoint_tolerance'])
    if len(rows)!=108:raise AssertionError('Bessel census')
    refs.append(checkpoint('BESSEL',0,rows,checks,['x','l','r','literal','angular_real','angular_imag']))
    checks=Checks();rows=[]
    for x in SI_X:
        a,_=sine_integral(x,32);b,_=sine_integral(x,64);c,tail=sine_integral(x,16,True);d,_=sine_integral(x,32,True)
        rows.append([x,a,b,c,d,tail]);checks.check('Si_laguerre_refinement',a,b,CFG['primitive_tolerance']);checks.check('Si_independent_refinement',c,d,CFG['primitive_tolerance']);checks.check('Si_independent',b,d,CFG['primitive_tolerance']+tail)
    increments=[]
    u,w=gauss(32);u2,w2=gauss(64)
    for x in PRIMITIVE_STARTS:
        for width in PRIMITIVE_WIDTHS:
            for l in range(3):
                a=primitive(l,x+width)-primitive(l,x);b=float(width/2*np.dot(w,bessel(l,0,x+width*(u+1)/2)));c=float(width/2*np.dot(w2,bessel(l,0,x+width*(u2+1)/2)))
                increments.append([x,width,l,a,b,c]);checks.check('primitive_increment',a,c,CFG['primitive_tolerance']);checks.check('primitive_increment_refinement',b,c,CFG['primitive_tolerance'])
    if len(increments)!=54:raise AssertionError('Primitive increment census')
    refs.append(checkpoint('PRIMITIVES',1,dict(Si=rows,increments=increments),checks,dict(Si=['x','laguerre32','laguerre64','independent16','independent32','tail'],increments=['start','width','l','primitive','gauss32','gauss64'])))
    for i,a in enumerate(OPACITIES):
        checks=Checks();rows=[]
        for b in PHASES:
            for l in range(3):
                for r in range(4):
                    for p in range(3):
                        v16,t=panel(l,r,p,a,b,16);v32,_=panel(l,r,p,a,b,32);u128=angular_panel(l,r,p,a,b,128);u256=angular_panel(l,r,p,a,b,256)
                        rows.append([b,a,l,r,p,v16,v32,u128.real,u128.imag,u256.real,u256.imag,t]);tag=f'{a}:{b}:{l}:{r}:{p}'
                        for name,x,y in (('panel_refinement',v16,v32),('angular_refinement',u128.real,u256.real),('independent_fine',v32,u256.real),('independent_coarse',v16,u128.real)):
                            checks.check(name,x,y,CFG['panel_tolerance']+t,1+abs(y),tag)
                        checks.check('angular128_reality',u128.imag,tol=CFG['reality_tolerance'],tag=tag);checks.check('angular256_reality',u256.imag,tol=CFG['reality_tolerance'],tag=tag)
        if len(rows)!=216:raise AssertionError('All panel rows per opacity')
        refs.append(checkpoint(f'PANEL_{i}',i+2,rows,checks,ROW_FIELDS));print(json.dumps(dict(stage=f'PANEL_{i}',rows=len(rows),failed=checks.result()['failed'])),flush=True)
    verify_prefix(refs);recheck();failures=sum(r['failed'] for r in refs)
    status='PASS_KERNEL_ARITHMETIC' if not failures else 'FAIL_KERNEL_ARITHMETIC'
    result=dict(status=status,configuration=CFG,checkpoint_references=refs,check_count=sum(r['check_count'] for r in refs),failed_checks=failures,input_sha256=SEALS,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,elapsed_seconds=time.monotonic()-tick,scope='Arithmetic kernels only. No physical forcing history, seed or coupled metric trajectory evaluated.')
    rh=write(STEM+'_RESULT.json',result);recheck();report=write(STEM+'_REPORT.json',dict(status=status,scope=result['scope'],checkpoint_references=refs,failed_checks=failures))
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=10);recheck()
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,result_sha256=rh,report_sha256=report,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),input_sha256=SEALS,output_sha256=dict(CREATED),checkpoint_count=10));recheck()
    print(json.dumps(dict(status=status,checks=result['check_count'],elapsed_seconds=result['elapsed_seconds'])),flush=True);return 0 if not failures else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');args=ap.parse_args()
    if not args.execute:raise SystemExit('Root alone launches --execute')
    if list(BASE.glob(STEM+'_*')):raise SystemExit('Existing runtime prefix preserved; this small packet has no resume')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),owner='root',pid=os.getpid(),source_sha256=sha(__file__),time=now()));raise
