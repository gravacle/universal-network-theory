"""Prospective manufactured cubic-memory and conservative collision controls.
No physical state, trajectory, incoming seed, calibration or producer main.
Root alone executes this immutable packet after full independent preflight.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import argparse,ast,hashlib,json,math,os,time,traceback
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V002'
PROTOCOL_SHA='87c11b6814c2376145f694b3c78ebc51d4a1bfc49496d00387868e501a587052'
PINS={'constrained_u_galaxy_horizon_actual_opacity_v001.py': '7b77dad9b5e7b28fad8616325139b526364016087dfa916d31cfe78dc5a18dc1', 'actual_opacity_retarded_radiation_kernel_v001.py': 'b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721', 'CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001_RESULT.json': 'f59da94c6cec859618210adc64cb2a4ddb42e911afd48d8daf47527a3085b7fb', 'CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001_RECEIPT.json': '60a2a57efb71a8653da5ea993dd291601f275cf86d4bb24c8bcf1e960e7d2a80', 'constrained_u_horizon_trace_drag_attribution_v002.py': '1e84f620b00770f43080becbe67af8ead68258a9d16002b373de4bf28efa834c', 'CONSTRAINED_U_HORIZON_TRACE_DRAG_ATTRIBUTION_V002_RESULT.json': 'a2c4f1246e09795547be911da1a1108b173730444d7390ae82f27a7e50425886', 'CONSTRAINED_U_HORIZON_TRACE_DRAG_ATTRIBUTION_V002_RECEIPT.json': 'a96a8131523b345644b0b9bb90227d236faf91d4d8e374fc946c428356418993', 'constrained_u_cubic_radiation_conservation_controls_v001.py': '63b546dc4e6ca71bff2b1991be9ae3a44c1b26a8f728addea6c5705e1a779499', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V001.md': '8f6acfc92f3d6a064bff41a42b79a1256715933a886d4838b0a9a34b85a05c99', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V001_RESULT.json': '5ba16f3c18db8a133dd40caa3d51f1ef34e9b5f3a0975202cb5b0936ddd459f6', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V001_RECEIPT.json': '38926bbc4fea3da659852c8a86ace322de6e942c99440342fb4bc96158c2ce78'}
DEPTHS=(.001,.1,1.,10.,1000.)
PHASES=(0.,.1,1.,4.,8.)
REFINEMENTS=(4,8,16)
METHOD_REFINEMENTS=(16,32,64)
RB_VALUES=(.01,.1,1.,10.)
CAP=48.
EPS=np.finfo(float).eps
SEALS={};OUTPUTS={};SOURCE_SHA=None;MANIFEST_SHA=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def builtin(v):
    if isinstance(v,dict):return {str(k):builtin(z) for k,z in v.items()}
    if isinstance(v,(tuple,list)):return [builtin(z) for z in v]
    if isinstance(v,np.ndarray):return builtin(v.tolist())
    if isinstance(v,np.generic):return builtin(v.item())
    return v

def write(name,obj):
    data=(json.dumps(builtin(obj),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);return sha(p)

def recheck():
    if sha(__file__)!=SOURCE_SHA:raise AssertionError('Immutable source')
    for p,h in dict(SEALS,**OUTPUTS).items():
        if sha(p)!=h:raise AssertionError('Changed sealed bytes '+p)

def journal(event,**fields):
    row=builtin(dict(time=datetime.now(timezone.utc).isoformat(),event=event,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**fields))
    data=json.dumps(row,sort_keys=True,allow_nan=False)+'\n'
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(data)

def load_angular():
    p=BASE/'constrained_u_galaxy_horizon_actual_opacity_v001.py'
    if sha(p)!=PINS[p.name]:raise AssertionError('Exact angular helper parent')
    nodes=[n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('gauss','bessel')]
    if {n.name for n in nodes}!={'gauss','bessel'}:raise AssertionError('Only two pure declared definitions')
    env=dict(np=np,math=math,lru_cache=lru_cache)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<pure-angular-definitions>','exec'),env)
    return env['gauss'],env['bessel']

def coefficients(nodes):
    """Ascending-power Lagrange coefficients, no empirical interpolant."""
    out=[]
    for i,xi in enumerate(nodes):
        poly=np.array([1.])
        for j,xj in enumerate(nodes):
            if j!=i:poly=np.polynomial.polynomial.polymul(poly,[-xj,1.])/(xi-xj)
        out.append(poly)
    return np.array(out)

def polynomial(poly,x,derivative=0):
    answer=np.zeros_like(np.asarray(x,float))
    for p in range(derivative,len(poly)):
        answer+=poly[p]*math.prod(range(p-derivative+1,p+1))*np.asarray(x,float)**(p-derivative)
    return answer

def geometry(profile,depth,end,panels,order,gauss):
    """Conformal interval [0,end], backward EXACT manufactured optical depth.
    Constant Gamma=depth; radiation Gamma=2*depth/(1+eta)^2.
    The radiation full [0,1] optical depth is also exactly depth.
    """
    total=depth*end if profile=='CONSTANT' else 2*depth*(1-1/(1+end))
    bound=min(total,CAP);u,w=gauss(order);ts=[];ws=[]
    for i in range(panels):
        lo=bound*i/panels;hi=bound*(i+1)/panels
        ts.append((lo+hi)/2+(hi-lo)*u/2);ws.append((hi-lo)*w/2)
    t=np.concatenate(ts);dt=np.concatenate(ws)
    if profile=='CONSTANT':
        eta=end-t/depth;gamma=np.full_like(t,depth)
    elif profile=='RADIATION':
        eta=1/(1/(1+end)+t/(2*depth))-1;gamma=2*depth/(1+eta)**2
    else:raise AssertionError('Frozen manufactured profile')
    if np.any(eta< -2e-12) or np.any(eta>end+2e-12) or not np.all(gamma>0):raise ArithmeticError('Manufactured positive coordinate')
    collision=dt*np.exp(-t);metric=collision/gamma
    minimum_gamma=depth if profile=='CONSTANT' else 2*depth/(1+end)**2
    return dict(total=float(total),eta=eta,gamma=gamma,collision=collision,metric=metric,
        collision_tail=math.exp(-CAP) if total>CAP else 0.,metric_tail=math.exp(-CAP)/minimum_gamma if total>CAP else 0.)

def moments(profile,depth,k,panels,order,gauss,bessel):
    geo=geometry(profile,depth,1.,panels,order,gauss);x=k*(1-geo['eta'])
    mm=np.empty((5,3,4));cc=np.empty_like(mm)
    for l in range(5):
        for r in range(3):
            angular=bessel(l,r,x)
            for p in range(4):
                factor=geo['eta']**p*angular
                mm[l,r,p]=math.fsum(float(z) for z in geo['metric']*factor)
                cc[l,r,p]=math.fsum(float(z) for z in geo['collision']*factor)
    return geo,mm,cc

def collision_moments(z):
    """I_p=int_0^1 z exp[-z(1-v)]v^p dv, p0..3.
    Positive series below8, stable finite recurrence above; no fitted damping.
    """
    if z<0:raise ValueError('Positive collision depth')
    if z==0:return np.zeros(4)
    if z<8:
        terms=[];term=1.
        for n in range(120):
            if n:term*=z/n
            terms.append(term)
        return np.array([z*math.exp(-z)*math.fsum(term/(n+p+1) for n,term in enumerate(terms)) for p in range(4)])
    ans=[-math.expm1(-z)]
    for p in range(1,4):ans.append(1-p*ans[-1]/z)
    return np.array(ans)

def constant_source_weights(z,node,poly):
    powers=np.array([node**p for p in range(4)])
    return poly@(powers*collision_moments(z*node))

def collision_panel(previous,rb,depth,dt,scheme,nodes,poly):
    """Only a manufactured two-fluid homogeneous collision problem.
    MIXED uses Gauss baryon rows plus cubic retarded photon values.
    CONSERVATIVE_J uses the SAME photon equation and exact combined momentum.
    All stage values return; conservation alone does not gate damping accuracy.
    """
    vb0,vg0=previous;z=depth*dt;J=rb*vb0+vg0
    ws=[constant_source_weights(z,float(node),poly) for node in nodes[1:]]
    attenuation=np.exp(-z*nodes[1:])
    c1,c2=nodes[1:3];root=math.sqrt(3)
    A=np.array([[.25,.25-root/6],[.25+root/6,.25]])
    if scheme=='MIXED':
        mat=np.zeros((6,6));rhs=np.zeros(6)
        for i in range(2):
            mat[2*i,2*i]=1.;rhs[2*i]=vb0
            for j in range(2):mat[2*i,2*j]+=z*A[i,j]/rb;mat[2*i,2*j+1]-=z*A[i,j]/rb
        mat[4,4]=1.;rhs[4]=vb0
        for j in range(2):mat[4,2*j]+=z/(2*rb);mat[4,2*j+1]-=z/(2*rb)
        for i,(weights,atten) in enumerate(zip(ws,attenuation)):
            row=2*i+1;mat[row,row]=1.;mat[row,[0,2,4]]-=weights[1:];rhs[row]=atten*vg0+weights[0]*vb0
        solution=np.linalg.solve(mat,rhs);stages=solution.reshape(3,2);end=stages[-1].copy()
    elif scheme=='CONSERVATIVE_J':
        mat=np.eye(3)+np.array([weights[1:]/rb for weights in ws])
        rhs=np.array([atten*vg0+weights[0]*vb0+math.fsum(float(w) for w in weights[1:])*J/rb for weights,atten in zip(ws,attenuation)])
        solution=np.linalg.solve(mat,rhs);stages=np.column_stack(((J-solution)/rb,solution));end=stages[-1].copy()
    else:raise AssertionError('Two declared methods only')
    residual=np.array([math.fsum(float(a*b) for a,b in zip(row,solution))-float(r) for row,r in zip(mat,rhs)])
    denominator=abs(mat)@abs(solution)+abs(rhs)
    error=float(np.max(abs(residual)/np.maximum(denominator,1e-30)))
    return end,stages,error

def collision_run(rb,depth,incoming,panels,scheme,nodes,poly):
    initial=np.array(incoming,float);state=initial.copy();history=[];residual=0.;conservation=0.
    J=rb*initial[0]+initial[1];Jscale=rb*abs(initial[0])+abs(initial[1])
    for i in range(panels):
        state,stages,error=collision_panel(state,rb,depth,1/panels,scheme,nodes,poly)
        residual=max(residual,error);conservation=max(conservation,abs(rb*state[0]+state[1]-J)/Jscale)
        history.append(dict(panel=i,end=state.copy(),stages=stages))
    slip=(initial[1]-initial[0])*math.exp(-depth*(1+1/rb));eq=J/(1+rb)
    exact=np.array([eq-slip/(1+rb),eq+rb*slip/(1+rb)])
    return dict(endpoint=state,exact=exact,maximum_matrix_residual=residual,maximum_momentum_error=conservation,
        damping_error=abs((state[1]-state[0])-slip),velocity_error=float(np.max(abs(state-exact))),history=history)

def authenticate_previous():
    """Complete saved-only closure, preserving every original2398 disposition.
    No kernel, method, rate or saved-state contraction is called here.
    """
    stem='CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V001'
    r=json.loads((BASE/(stem+'_RESULT.json')).read_text());receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
    manifest=json.loads((BASE/(stem+'_MANIFEST.json')).read_text())
    if (r['manifest']!=manifest or manifest['source_sha256']!=PINS['constrained_u_cubic_radiation_conservation_controls_v001.py']
        or receipt['source_sha256']!=manifest['source_sha256'] or receipt['result_sha256']!=PINS[stem+'_RESULT.json']
        or receipt['status']!=r['status'] or r['status']!='MANUFACTURED_CONSERVATIVE_METHOD_FAILED'
        or receipt['checkpoint_count']!=4 or receipt['category_dispositions']!=r['category_dispositions']):raise AssertionError('Whole original failed envelope')
    if len(r['numerical_gates'])!=2398 or sum(not g['passed'] for g in r['numerical_gates'])!=125:raise AssertionError('All original2398/125 dispositions')
    expected={'KERNEL':True,'MIXED':False,'CONSERVATIVE_J':False,'GAUSS_PRODUCT':True,'TRAPEZOID_COMPARATOR':False}
    if r['category_dispositions']!=expected or r['all_controls_passed'] or r['conservative_method_qualified']:raise AssertionError('No original method promotion')
    for g in r['numerical_gates']:
        if type(g['passed']) is not bool or g['passed']!=bool(math.isfinite(g['error']) and g['error']<=g['tolerance']):raise AssertionError('Exact original predicate')
    for mapping in (receipt['input_sha256'],receipt['output_sha256']):
        for filename,h in mapping.items():
            path=Path(filename).resolve()
            if path.parent!=BASE or sha(path)!=h or (str(path) in SEALS and SEALS[str(path)]!=h):raise AssertionError('Original complete byte map')
            SEALS[str(path)]=h
    if receipt['input_sha256']!=manifest['inputs'] or sha(BASE/(stem+'_MANIFEST.json'))!=receipt['manifest_sha256'] or sha(BASE/(stem+'_JOURNAL.jsonl'))!=receipt['journal_sha256']:raise AssertionError('Exact original manifest/journal')
    events=[json.loads(z) for z in (BASE/(stem+'_JOURNAL.jsonl')).read_text().splitlines()]
    stages=['KERNEL','COLLISION','PRODUCT','SUMMARY']
    if [e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE']:raise AssertionError('Original natural six events')
    if any(e['owner']!='root' or e['pid']!=13980 or e['source_sha256']!=manifest['source_sha256'] or e['manifest_sha256']!=receipt['manifest_sha256'] for e in events):raise AssertionError('Original root/source/PID closure')
    if events[-1]['status']!=r['status'] or events[-1]['result_sha256']!=receipt['result_sha256'] or events[-1]['controls']!=2398 or events[-1]['passed']!=2273:raise AssertionError('Original exact terminal')
    previous=None;names=set()
    for stage,e in zip(stages,events[1:5]):
        pn=stem+'_'+stage+'_CP.json';cn=pn[:-5]+'_COMMIT.json';payload=json.loads((BASE/pn).read_text());commit=json.loads((BASE/cn).read_text())
        expected_commit=dict(source_sha256=manifest['source_sha256'],manifest_sha256=receipt['manifest_sha256'],owner='root',pid=13980,stage=stage,payload=pn,sha256=sha(BASE/pn))
        if commit!=expected_commit or payload['manifest']!=manifest or payload['stage']!=stage or set(payload)!={'manifest','stage','rows','gates'}:raise AssertionError('Full original pair schemas')
        if (BASE/pn).read_bytes()!=(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode() or (BASE/cn).read_bytes()!=(json.dumps(commit,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode():raise AssertionError('Finite canonical original pair')
        if e['stage']!=stage or e['payload']!=pn or e['sha256']!=sha(BASE/pn) or e['commit_sha256']!=sha(BASE/cn):raise AssertionError('Original pair/event byte binding')
        if previous is not None and (payload['rows'][:len(previous['rows'])]!=previous['rows'] or payload['gates'][:len(previous['gates'])]!=previous['gates']):raise AssertionError('Whole original row/gate prefixes')
        previous=payload;names.update((pn,cn))
    if {p.name for p in BASE.glob(stem+'_*_CP*.json')}!=names or previous['rows']!=r['rows'] or previous['gates']!=r['numerical_gates']:raise AssertionError('Original four pair/result complete closure')
    return dict(source_sha256=manifest['source_sha256'],result_sha256=receipt['result_sha256'],receipt_sha256=PINS[stem+'_RECEIPT.json'],status=r['status'],category_dispositions=r['category_dispositions'],all_original_numerical_gates=r['numerical_gates'],original_passed=2273,original_failed=125,checkpoint_count=4,journal_event_count=6,physical_trajectory=False)

def main():
    global SOURCE_SHA,MANIFEST_SHA
    if PROTOCOL_SHA=='PENDING':raise AssertionError('Prospective protocol unsealed')
    SOURCE_SHA=sha(__file__);tick=time.monotonic()
    for name,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():
        p=(BASE/name).resolve()
        if p.parent!=BASE or sha(p)!=h:raise AssertionError('Exact declared local input '+name)
        SEALS[str(p)]=h
    # These hashes are context only: no saved physical state or inherited RHS is read.
    original_attempt=authenticate_previous()
    gauss,bessel=load_angular();nodes=np.array([0.,.5-math.sqrt(3)/6,.5+math.sqrt(3)/6,1.]);poly=coefficients(nodes)
    manifest=builtin(dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),profiles=['CONSTANT','RADIATION'],depths=DEPTHS,phases=PHASES,
        kernel_product_panels=REFINEMENTS,method_panels=METHOD_REFINEMENTS,original_attempt=original_attempt,orders=[16,32],rb_values=RB_VALUES,schemes=['MIXED','CONSERVATIVE_J'],incoming_basis=[[1.,0.],[0.,1.]],
        nodes=nodes,cap=CAP,gate_count=2398,numpy_version=np.__version__,physical_trajectory=False))
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('x'):pass
    journal('OWNER_START')
    gates=[];rows=[];records=[]
    def check(name,error,tolerance=2e-11,category='KERNEL',**ids):
        gates.append(builtin(dict(name=name,error=float(error),tolerance=float(tolerance),passed=bool(math.isfinite(error) and error<=tolerance),category=category,**ids)))
    def checkpoint(stage):
        recheck();pn=STEM+'_'+stage+'_CP.json';payload=builtin(dict(manifest=manifest,stage=stage,rows=rows,gates=gates));ph=write(pn,payload)
        cn=pn[:-5]+'_COMMIT.json';commit=dict(source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,owner='root',pid=os.getpid(),stage=stage,payload=pn,sha256=ph)
        ch=write(cn,commit);records.append((pn,cn,payload,commit));journal('CHECKPOINT',stage=stage,payload=pn,sha256=ph,commit_sha256=ch)
    for i in range(4):
        for j in range(4):check('lagrange_cardinal',abs(float(polynomial(poly[j],nodes[i]))-(i==j)),2e-12,i=i,j=j)
    for x in np.linspace(0,1,11):
        for p in range(4):
            interpolation=np.array([math.fsum(float(nodes[j]**p*poly[j,z]) for j in range(4)) for z in range(4)])
            for r in range(4):
                exact=math.prod(range(p-r+1,p+1))*x**(p-r) if p>=r else 0.
                check('cubic_derivative_reproduction',abs(float(polynomial(interpolation,x,r))-exact),2e-12,x=float(x),p=p,r=r)
    for profile in ('CONSTANT','RADIATION'):
        for depth in DEPTHS:
            geo=geometry(profile,depth,1.,16,32,gauss);mass=-math.expm1(-min(depth,CAP));cscale=min(depth,1.)
            check('optical_mass',abs(math.fsum(float(z) for z in geo['collision'])-mass)/cscale,profile=profile,depth=depth)
            check('positive_coordinate',max(float(np.max(-geo['eta'])),float(np.max(geo['eta']-1.)),0.),profile=profile,depth=depth)
            check('measure_identity',float(np.max(abs(geo['metric']*geo['gamma']-geo['collision'])))/max(float(np.max(abs(geo['collision']))),1e-300),profile=profile,depth=depth)
            for k in PHASES:
                values={n:moments(profile,depth,k,n,16,gauss,bessel) for n in REFINEMENTS}
                reference=moments(profile,depth,k,16,32,gauss,bessel)
                mscale=max(math.fsum(float(z) for z in reference[0]['metric']),1e-300)
                for n in (4,8):
                    check('optical_panel_refinement_metric',float(np.max(abs(values[n][1]-values[16][1])))/mscale,profile=profile,depth=depth,k=k,panels=n)
                    check('optical_panel_refinement_collision',float(np.max(abs(values[n][2]-values[16][2])))/cscale,profile=profile,depth=depth,k=k,panels=n)
                check('optical_order_refinement_metric',float(np.max(abs(values[16][1]-reference[1])))/mscale,profile=profile,depth=depth,k=k)
                check('optical_order_refinement_collision',float(np.max(abs(values[16][2]-reference[2])))/cscale,profile=profile,depth=depth,k=k)
                mm,cc=reference[1:];visibility=math.exp(-depth)
                for l in range(5):
                    for p in range(4):
                        direct=4*p*mm[l,0,p-1] if p else 0.
                        terms=[4. if l==0 else 0.,-4*visibility*float(bessel(l,0,np.array(k))) if p==0 else 0.,4*k*mm[l,1,p],-4*cc[l,0,p]]
                        converted=math.fsum(float(z) for z in terms);scale=max(1.,abs(direct)+math.fsum(abs(float(z)) for z in terms))
                        check('derivative_free_metric_identity',abs(direct-converted)/scale,profile=profile,depth=depth,k=k,l=l,p=p)
                rows.append(dict(kind='CUBIC_KERNEL',profile=profile,depth=depth,k=k,refinements={str(n):dict(metric=v[1],collision=v[2]) for n,v in values.items()},reference=dict(metric=mm,collision=cc),collision_tail=reference[0]['collision_tail'],metric_tail=reference[0]['metric_tail']))
    for depth in DEPTHS:
        _,mm,cc=moments('CONSTANT',depth,0.,16,32,gauss,bessel);oracle=collision_moments(depth)
        for p in range(4):
            check('constant_polynomial_collision',abs(cc[0,0,p]-oracle[p])/min(depth,1.),depth=depth,p=p)
            check('constant_polynomial_metric',abs(mm[0,0,p]-oracle[p]/depth)/max(min(1.,1/depth),1e-300),depth=depth,p=p)
    checkpoint('KERNEL')
    for rb in RB_VALUES:
        for depth in DEPTHS:
            for basis,incoming in enumerate(((1.,0.),(0.,1.))):
                for scheme in ('MIXED','CONSERVATIVE_J'):
                    values={n:collision_run(rb,depth,incoming,n,scheme,nodes,poly) for n in METHOD_REFINEMENTS}
                    for n,v in values.items():
                        check('collision_matrix_residual',v['maximum_matrix_residual'],category=scheme,rb=rb,depth=depth,basis=basis,panels=n)
                        check('collision_combined_momentum',v['maximum_momentum_error'],category=scheme,rb=rb,depth=depth,basis=basis,panels=n)
                    check('collision_endpoint_velocity',values[64]['velocity_error'],1e-5,category=scheme,rb=rb,depth=depth,basis=basis)
                    check('collision_endpoint_damping',values[64]['damping_error'],1e-5,category=scheme,rb=rb,depth=depth,basis=basis)
                    check('collision_time_refinement',float(np.max(abs(values[32]['endpoint']-values[64]['endpoint']))),1e-5,category=scheme,rb=rb,depth=depth,basis=basis)
                    rows.append(dict(kind='COLLISION_METHOD',scheme=scheme,rb=rb,depth=depth,basis=basis,incoming=incoming,refinements=values))
    checkpoint('COLLISION')
    product_runs={}
    parameters=((3.,1.),(4.,2.),(4.,1.5),(3.3,.7))
    for n in REFINEMENTS:
        dx=1/n;gauss_total=0.;trap_total=0.;species=[]
        for species_index,(alpha,beta) in enumerate(parameters):
            gi=[];ti=[];parts=[]
            for i in range(n):
                lo=i*dx;hi=(i+1)*dx;p0,p1=math.exp(-alpha*lo),math.exp(-alpha*hi);u0,u1=math.exp(beta*lo),math.exp(beta*hi)
                px0,px1=-alpha*p0,-alpha*p1;ux0,ux1=beta*u0,beta*u1
                ru=u1-u0-dx*(ux0+ux1)/2;rp=p1-p0-dx*(px0+px1)/2
                pieces=[(p0+p1)*ru/2,(u0+u1)*rp/2,-dx*((p1-p0)*(ux1-ux0)+(u1-u0)*(px1-px0))/4]
                direct=p1*u1-p0*u0-dx*(px0*u0+p0*ux0+px1*u1+p1*ux1)/2
                scale=math.fsum(abs(v) for v in pieces)+abs(p1*u1)+abs(p0*u0)+dx*(abs(px0*u0)+abs(p0*ux0)+abs(px1*u1)+abs(p1*ux1))/2
                check('exact_product_decomposition',abs(direct-math.fsum(pieces)),4096*EPS*scale+1e-280,panels=n,species=species_index,panel=i)
                qnodes=lo+dx*nodes[1:3];forces=(alpha-beta)*np.exp((beta-alpha)*qnodes)
                gi.append(dx*math.fsum(float(z) for z in forces)/2)
                ti.append(dx*(alpha-beta)*(p0*u0+p1*u1)/2);parts.append(dict(panel=i,velocity=pieces[0],background=pieces[1],product=pieces[2],direct=direct))
            exact_delta=math.exp(beta-alpha)-1;gr=exact_delta+math.fsum(gi);tr=exact_delta+math.fsum(ti)
            gauss_total+=gr;trap_total+=tr;species.append(dict(alpha=alpha,beta=beta,gauss_residual=gr,trapezoid_residual=tr,parts=parts))
        product_runs[n]=dict(gauss_residual=gauss_total,trapezoid_residual=trap_total,species=species)
    for method,field in (('GAUSS_PRODUCT','gauss_residual'),('TRAPEZOID_COMPARATOR','trapezoid_residual')):
        check('manufactured_product_conservation',abs(product_runs[16][field]),1e-5,category=method)
        check('manufactured_product_refinement',abs(product_runs[8][field]-product_runs[16][field]),1e-5,category=method)
    rows.append(dict(kind='PRODUCT_CONSERVATION',refinements=product_runs));checkpoint('PRODUCT')
    if len(gates)!=2398:raise AssertionError('Frozen2398 control census')
    categories={name:all(g['passed'] for g in gates if g['category']==name) for name in ('KERNEL','MIXED','CONSERVATIVE_J','GAUSS_PRODUCT','TRAPEZOID_COMPARATOR')}
    all_pass=all(g['passed'] for g in gates)
    qualified=categories['KERNEL'] and categories['CONSERVATIVE_J'] and categories['GAUSS_PRODUCT']
    status=('MANUFACTURED_CONSERVATIVE_METHOD_PASS' if all_pass else 'MANUFACTURED_CONSERVATIVE_METHOD_PASS_COMPARATORS_FAILED') if qualified else 'MANUFACTURED_CONSERVATIVE_METHOD_FAILED'
    recheck();result=dict(status=status,all_controls_passed=all_pass,conservative_method_qualified=qualified,category_dispositions=categories,manifest=manifest,rows=rows,numerical_gates=gates,elapsed_seconds=time.monotonic()-tick,
        scope='Manufactured bounded kernel/damping/conservation only; no physical trajectory, seed, full-FLRW or uniform stiff fourth-order qualification')
    rh=write(STEM+'_RESULT.json',result)
    report=BASE/(STEM+'_REPORT.md');body='# Manufactured cubic radiation and conservation controls V002\n\n'+status+'\n\n'+str(sum(g['passed'] for g in gates))+'/2398 controls PASS.\n\n'+json.dumps(categories,sort_keys=True)+'\n\nAll comparator failures remain. No physical state or trajectory was advanced.\n'
    with report.open('xb') as f:f.write(body.encode())
    report.chmod(0o444);OUTPUTS[str(report.resolve())]=sha(report)
    checkpoint('SUMMARY');journal('OWNER_COMPLETE',status=status,result_sha256=rh,controls=len(gates),passed=sum(g['passed'] for g in gates))
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);OUTPUTS[str(jp.resolve())]=sha(jp)
    events=[json.loads(z) for z in jp.read_text().splitlines()]
    if [e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'] or any(e['owner']!='root' or e['pid']!=os.getpid() or e['source_sha256']!=SOURCE_SHA or e['manifest_sha256']!=MANIFEST_SHA for e in events):raise AssertionError('Exact root natural journal closure')
    for (pn,cn,payload,commit),event in zip(records,events[1:5]):
        if json.loads((BASE/pn).read_text())!=payload or json.loads((BASE/cn).read_text())!=commit or event['stage']!=payload['stage'] or event['payload']!=pn or event['sha256']!=sha(BASE/pn) or event['commit_sha256']!=sha(BASE/cn):raise AssertionError('Exact complete checkpoint and event binding')
    if len(list(BASE.glob(STEM+'_*_COMMIT.json')))!=4:raise AssertionError('Exactly four stage pairs')
    recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,result_sha256=rh,report_sha256=sha(report),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),input_sha256=dict(SEALS),output_sha256=dict(OUTPUTS),checkpoint_count=4,category_dispositions=categories))
    recheck();return 0 if qualified else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root only after frozen full peer review')
    if any(BASE.glob(STEM+'_*')):raise SystemExit('Exclusive nonresumable prefix exists; preserve/refuse')
    try:raise SystemExit(main())
    except Exception:
        write(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json',dict(status='ERROR_PRESERVED',source_sha256=SOURCE_SHA,time=datetime.now(timezone.utc).isoformat(),traceback=traceback.format_exc()))
        raise
