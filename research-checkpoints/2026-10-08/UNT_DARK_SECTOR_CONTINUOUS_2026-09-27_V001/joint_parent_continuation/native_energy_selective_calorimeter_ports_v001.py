"""NEW gap-aggregated native energy-selective ports. Root --execute only.
No legacy imports/initializers, old propagators, state resets or arbitrary gaps.
"""
import os
import sys
sys.dont_write_bytecode=True
for _k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[_k]='1'
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import time
import numpy as np

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent.resolve()
STEM='NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001'
PROTOCOL_SHA='145993fbd35cb52be09169c2dbfcee4e059a3bc45a6f8f696ba6f5081e535d44'
PINS={'native_thermal_packet_v001.py': '380e736479e7dd9a670a10a06410bb27a6e4aff44e8c23f9fe52f03a7a4ff837', 'NATIVE_THERMAL_PACKET_PROTOCOL_V001.md': '08b9d07768c0f6c4c2e635b9affe623f1ca04914d2d53e1524d2a5a013ddf632', 'NATIVE_THERMAL_PACKET_V001_RESULTS.json': '8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538', 'NATIVE_THERMAL_PACKET_V001_FROZEN.json': '4a6ed3c387bc87961264806ef630f988199bfdde0b3f9d81fb53b11a2c40f0b3', 'NATIVE_THERMAL_PACKET_V001_SAVED_AUDIT.json': '2c3f6d7a33e337f0a38878da0038b5935c192de6e45760771e6359a343d58095', 'native_calorimeter_ports_v001.py': 'dd04a76c43d7b649fa1829c678924040651b96a78efa6d78dc105df78b5e40f9', 'NATIVE_CALORIMETER_PORTS_PROTOCOL_V001.md': '7b343eec0228adc3a1cc4c3de0f4c42bc8c1017b5fd166932def658c22ba006c', 'NATIVE_CALORIMETER_PORTS_V001_RESULTS.json': '0dd6bb4ecc1b4e3875d603755de98e6b0dbe8028a416c7509fa8cca9ce8516ed', 'NATIVE_CALORIMETER_PORTS_V001_FROZEN.json': 'dd3eada48d549bfd53663fc362375ef56c9d7a186807719aa0cb5933c55c44fe', 'NATIVE_CALORIMETER_PORTS_V001_SAVED_AUDIT.json': '97bba6fddc5c19a7585ab6c07626eb47ae4acbda22b08fe1102db1d0129b56f7', 'NATIVE_CALORIMETER_ENERGY_ORIGIN_AND_RESONANT_PORT_V001.md': '1f8a0d04767f039ccc4af50b6f412129092cdcf8016e71c83d04893fb336b5fb'}
OPERATOR_SPAN_SHA='e9197f1f5b191882f4693c5f75e2646614eb3443cb67badf98529f724d3338df'
PARAMETERS=dict(hbar=1.,Omega=1.,U_d=1.,d_star=1.,Delta=4.,epsilon_psi=1.,t_hop=.5,lambda_J=.25)
RECORD_PARAMETERS=dict(epsilon_r=1.,lambda_R=.5)
CFG=dict(record_occupations=[0,1],native_preparations=['cycle','tree'],ages=[0.,.5,2.],probe_edges=[0,3],probe_inputs=['00','10','01'],couplings=[.01,.005],durations=[.25,1.,2.],group_tolerance=1e-10,operator_tolerance=2e-11,state_tolerance=2e-9,energy_tolerance=2e-8,weak_roundoff=2e-9,group_bound_factor=16,gap_bound_factor=16,roundoff_factor=64,bundle_gap_count=16,taylor_tail=1e-19,taylor_max_terms=256)
ROW_FIELDS=['native_energy_final','probe_energy_initial','probe_energy_final','interaction_energy','total_on_energy','delta_native','delta_probe','switch_on_work','switch_off_work','ledger_residual','norm','free_second_moment_initial','free_second_moment_final','dual_state_error','flip0','flip1','weak_flip0','weak_flip1','scaled_flip_error0','scaled_flip_error1']+['rho_'+str(i) for i in range(16)]
SEALS={}
CREATED={}
RUN_SOURCE=''
RUN_MANIFEST=''
EPOCH=0

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def encoded(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def read(p):return json.loads(Path(p).read_text())
def cjson(a):
    a=np.asarray(a);return dict(real=a.real.tolist(),imag=a.imag.tolist())
def carr(a):return np.array(a['real'])+1j*np.array(a['imag'])
def write(name,obj):
    p=BASE/name;raw=encoded(obj)
    with p.open('xb') as f:f.write(raw)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h;return h
def seal(p,h):
    p=Path(p).resolve()
    if not p.is_relative_to(ROOT) or sha(p)!=h:raise AssertionError('Input seal '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting seal')
    SEALS[str(p)]=h
def recheck():
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed input/output '+p)
    if sha(__file__)!=RUN_SOURCE:raise AssertionError('Changed source')
def span(source,name):
    n=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
    return ''.join(source.splitlines(keepends=True)[n.lineno-1:n.end_lineno])

class Checks:
    def __init__(self):self.counts={};self.maxima={};self.failures=[]
    def check(self,name,value,expected=0.,tol=None,tag=''):
        error=float(np.max(abs(np.asarray(value)-np.asarray(expected))))
        tol=CFG['operator_tolerance'] if tol is None else tol
        self.counts[name]=self.counts.get(name,0)+1;self.maxima[name]=max(self.maxima.get(name,0.),error)
        if not math.isfinite(error) or error>tol:self.failures.append(dict(name=name,tag=tag,error=error,tolerance=tol))
    def merge(self,d):
        for k,v in d['counts'].items():self.counts[k]=self.counts.get(k,0)+v
        for k,v in d['maxima'].items():self.maxima[k]=max(self.maxima.get(k,0.),v)
        self.failures.extend(d['failures'])
    def data(self):return dict(counts=self.counts,maxima=self.maxima,failures=self.failures)

# Literal authenticated operators(record_occupation) is inserted here at authoring.
def operators(record_occupation):
    """Node partition (primary) versus a separately assembled full row operator."""
    edges = [(i, 2+j) for i in range(2) for j in range(2)]
    masks = np.arange(16)
    bits = ((masks[:, None] >> np.arange(4)) & 1).astype(float)
    deg = np.zeros((16, 4))
    n, flips, hop, carrier_current = [], [], [], []
    ident4 = np.eye(4)
    p = [np.kron(np.eye(16), np.diag(ident4[v])) for v in range(4)]
    for edge, (u, v) in enumerate(edges):
        deg[:, u] += bits[:, edge]
        deg[:, v] += bits[:, edge]
        n.append(np.diag(np.repeat(bits[:, edge], 4)))
        x = np.zeros((16, 16))
        x[masks ^ (1 << edge), masks] = 1.
        flips.append(np.kron(x, ident4))
        transfer = np.zeros((4, 4))
        transfer[u, v] = transfer[v, u] = 1.
        current = np.zeros((4, 4), dtype=complex)
        current[v, u], current[u, v] = 1j, -1j
        hop.append(np.kron(np.diag(bits[:, edge]), transfer))
        carrier_current.append(PARAMETERS['t_hop'] * np.kron(np.diag(bits[:, edge]), current))
    hv = []
    for v in range(4):
        local = np.diag(np.repeat(PARAMETERS['U_d'] * (deg[:, v]-PARAMETERS['d_star'])**2, 4))
        local += PARAMETERS['epsilon_psi'] * p[v]
        local += RECORD_PARAMETERS['epsilon_r'] * record_occupation * np.eye(64)
        for edge, ends in enumerate(edges):
            if v in ends:
                local += (PARAMETERS['Delta'] * n[edge] / 2
                          - PARAMETERS['Omega'] * flips[edge] / 4
                          - PARAMETERS['t_hop'] * hop[edge] / 2
                          + PARAMETERS['lambda_J'] * n[edge] @ p[v]
                          - RECORD_PARAMETERS['lambda_R'] * record_occupation * n[edge])
        hv.append(local.astype(complex))
    h = sum(hv)
    row = np.zeros((64, 64), dtype=complex)
    for mask in range(16):
        occupied = [(mask >> edge) & 1 for edge in range(4)]
        degrees = [sum(occupied[e] for e, ends in enumerate(edges) if v in ends) for v in range(4)]
        baseline = PARAMETERS['Delta'] * sum(occupied) + PARAMETERS['U_d'] * sum((d-PARAMETERS['d_star'])**2 for d in degrees)
        baseline += (4*RECORD_PARAMETERS['epsilon_r']*record_occupation
                     -2*RECORD_PARAMETERS['lambda_R']*record_occupation*sum(occupied))
        for v in range(4):
            index = 4*mask+v
            row[index, index] = baseline + PARAMETERS['epsilon_psi'] + PARAMETERS['lambda_J'] * degrees[v]
            for edge, (left, right) in enumerate(edges):
                row[index, 4*(mask ^ (1 << edge))+v] -= PARAMETERS['Omega']/2
                if occupied[edge] and v in (left, right):
                    other = right if v == left else left
                    row[index, 4*mask+other] -= PARAMETERS['t_hop']
    return h, row, hv, n, p, carrier_current, edges


def authenticate():
    for n,h in PINS.items():seal(BASE/n,h)
    seal(BASE/(STEM+'.md'),PROTOCOL_SHA)
    if hashlib.sha256(span((BASE/'native_thermal_packet_v001.py').read_text(),'operators').encode()).hexdigest()!=OPERATOR_SPAN_SHA:raise AssertionError('Literal native operator span')
    if span(Path(__file__).read_text(),'operators')!=span((BASE/'native_thermal_packet_v001.py').read_text(),'operators'):raise AssertionError('Native operator byte complement')
    packet=read(BASE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json');cal=read(BASE/'NATIVE_CALORIMETER_PORTS_V001_RESULTS.json')
    for name,obj,freeze in [('native',packet,'NATIVE_THERMAL_PACKET_V001_FROZEN.json'),('calorimeter',cal,'NATIVE_CALORIMETER_PORTS_V001_FROZEN.json')]:
        if obj['status']!='COMPLETE' or obj['payload']['failures'] or hashlib.sha256(encoded(obj['payload'])[:-1]).hexdigest()!=obj['payload_sha256'] or obj['freeze_sha256']!=PINS[freeze]:raise AssertionError('Accepted parent envelope '+name)
        f=read(BASE/freeze)
        for p,h in f['files'].items():seal(ROOT/p,h)
    a=read(BASE/'NATIVE_THERMAL_PACKET_V001_SAVED_AUDIT.json');b=read(BASE/'NATIVE_CALORIMETER_PORTS_V001_SAVED_AUDIT.json')
    if a['status']!='PASS_SAVED_ARITHMETIC' or b['status']!='PASS' or a['failures'] or b['failures']:raise AssertionError('Saved parent audits')
    old=packet['payload']
    if old['parameters']!=PARAMETERS or old['record_parameters']!=RECORD_PARAMETERS:raise AssertionError('Full native parameters')
    for new,prior in [('ages','probe_ages'),('native_preparations','labels'),('durations','durations'),('record_occupations','record_occupations')]:
        if CFG[new]!=old['config'][prior]:raise AssertionError('Inherited census '+new)
    for k in ('couplings','probe_inputs','probe_edges'):
        if CFG[k]!=cal['payload']['config'][k]:raise AssertionError('Inherited detector census '+k)
    if len(old['sectors'])!=2 or any(s['status']!='COMPLETE' or s['failures'] or len(s['energy_groups'])!=48 or len(s['energy_eigenvalues'])!=64 for s in old['sectors']):raise AssertionError('Qualified full spectrum census')
    return old

def spectral(q,saved,witness=None):
    ck=Checks();h,row,hv,incidence,_,_,edges=operators(q);ck.check('native_partition_vs_row',h,row)
    if witness is None:e,U=np.linalg.eigh(h)
    else:
        if witness['q']!=q:raise AssertionError('Witness sector')
        e=np.array(witness['eigenvalues']);U=carr(witness['eigenvectors'])
    ck.check('native_spectrum_parent',e,saved['energy_eigenvalues']);ck.check('native_eigensystem',h@U,U*e)
    ck.check('native_unitarity',U.conj().T@U,np.eye(64))
    defect=float(np.linalg.norm(U.conj().T@U-np.eye(64),'fro'))
    if defect>=1:raise AssertionError('No complete polar spectral witness')
    dp=defect/(1+math.sqrt(1-defect));r=float(np.linalg.norm(h@U-U*e,'fro'));hn=float(np.linalg.norm(h,'fro'))
    delta=r+(hn+float(max(abs(e))))*dp;pad=CFG['roundoff_factor']*np.finfo(float).eps*max(1.,hn,float(max(abs(e))))
    groups=[];flat=[]
    for i,g in enumerate(saved['energy_groups']):
        ix=g['indices'];flat.extend(ix);center=float(np.mean(e[ix]));width=float(np.ptp(e[ix]))
        ck.check('native_group_parent_energy',center,g['energy'])
        groups.append(dict(ID=i,indices=ix,energy=center,width=width,qualified=bool(width<=CFG['group_bound_factor']*delta+pad)))
    if flat!=list(range(64)):raise AssertionError('Complete saved degenerate group partition')
    for i,g in enumerate(groups):
        separation=min([abs(g['energy']-t['energy']) for j,t in enumerate(groups) if j!=i])
        g['qualified']=bool(g['qualified'] and separation>2*delta+pad)
    pairs=[dict(ID=f'{i}:{j}',low=i,high=j,gap=groups[j]['energy']-groups[i]['energy']) for i in range(48) for j in range(i+1,48)]
    ordered=sorted(pairs,key=lambda d:(d['gap'],d['low'],d['high']));clusters=[]
    for p in ordered:
        if not clusters or p['gap']-clusters[-1]['first_gap']>CFG['group_tolerance']:clusters.append(dict(ID=len(clusters),first_gap=p['gap'],pairs=[]))
        clusters[-1]['pairs'].append(p)
    for g in clusters:
        gaps=[p['gap'] for p in g['pairs']];g['omega']=sum(gaps)/len(gaps);g['span']=max(gaps)-min(gaps)
        low=[p['low'] for p in g['pairs']];high=[p['high'] for p in g['pairs']]
        qualified=g['omega']>2*delta+pad and g['span']<=CFG['gap_bound_factor']*delta+pad and len(set(low))==len(low) and len(set(high))==len(high) and all(groups[i]['qualified'] for i in low+high)
        g['status']='QUALIFIED_FINITE_RESOLUTION_GAP_GROUP' if qualified else 'UNRESOLVED_NEAR_GAP_OR_PROJECTOR';g['implied_row_count']=108
    for i,g in enumerate(clusters):
        if any(abs(g['omega']-clusters[j]['omega'])<=g['span']+clusters[j]['span']+4*delta+2*pad for j in (i-1,i+1) if 0<=j<len(clusters)):g['status']='UNRESOLVED_NEAR_GAP_OR_PROJECTOR'
    O=[U.conj().T@incidence[k]@U for k in CFG['probe_edges']]
    holds=[];meta=[];columns=[]
    for label in CFG['native_preparations']:
        for age in CFG['ages']:
            selected=[d for d in saved['holds'] if d['preparation']==label and d['age']==age]
            if len(selected)!=1:raise AssertionError('Complete six saved incoming holds')
            hold=selected[0];psi=carr(hold['state_vector']);ck.check('native_initial_norm',np.vdot(psi,psi),1.,CFG['state_tolerance']);ck.check('native_initial_energy',np.vdot(psi,h@psi),hold['energy'],CFG['energy_tolerance'])
            holds.append(U.conj().T@psi)
            for inp in CFG['probe_inputs']:
                probe=np.eye(4)[:,int(inp,2)];columns.append(np.kron(holds[-1],probe));meta.append(dict(preparation=label,age=age,probe_input=inp,native_energy=hold['energy']))
    hb=U.conj().T@h@U;frame_remainder=float(np.linalg.norm(hb-np.diag(e),'fro'))
    wit=dict(q=q,eigenvalues=e.tolist(),eigenvectors=cjson(U),native_H=cjson(h),incidence_spectral=[cjson(a) for a in O],groups=groups,gap_groups=clusters,zero_elastic_group_IDs=list(range(48)),pair_count=len(pairs),uncertainty=dict(frobenius_residual=r,gram_defect=defect,polar_distance=dp,ordered_eigenvalue_error_estimate=delta,native_frame_remainder_F=frame_remainder,roundoff_pad=pad,directed_interval=False),checks=ck.data())
    if witness is not None and wit!=witness:raise AssertionError('Resumed complete spectral witness differs')
    return wit,e,hb,groups,clusters,O,holds,np.column_stack(columns),meta

def gap_operator(g,groups,O,e,ck):
    A=[np.zeros((64,64),complex) for _ in O];blocks=[];source_norm=[0.,0.]
    for p in g['pairs']:
        lo=groups[p['low']]['indices'];hi=groups[p['high']]['indices'];one=[]
        for j,o in enumerate(O):
            b=o[np.ix_(lo,hi)];A[j][np.ix_(lo,hi)]=b;source_norm[j]=max(source_norm[j],float(np.linalg.svd(b,compute_uv=False)[0]));one.append(cjson(b))
        blocks.append(dict(pair_ID=p['ID'],low_indices=lo,high_indices=hi,probe_blocks=one))
    # Structural vertices keep every matched pair, even a numerically tiny source.
    parent=list(range(192))
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    for p in g['pairs']:
        for probe in range(4):
            for bit in (2,1):
                if not probe&bit:
                    x=find(4*p['high']+probe);y=find(4*p['low']+(probe|bit));parent[x]=y
    classes={}
    for gi in range(48):
        for probe in range(4):classes.setdefault(find(4*gi+probe),[]).extend(4*np.array(groups[gi]['indices'])+probe)
    components=[sorted(int(i) for i in ix) for ix in classes.values() if len(ix)>1]
    # A degenerate spectator group is retained, but need not be eigensolved.
    raising=[np.kron(np.array([[0.,0.],[1.,0.]]),np.eye(2)),np.kron(np.eye(2),np.array([[0.,0.],[1.,0.]]))]
    V=sum(np.kron(a,b)+np.kron(a.conj().T,b.T) for a,b in zip(A,raising))
    free=np.repeat(e,4)+g['omega']*np.tile([0,1,1,2],64)
    ck.check('port_Hermitian',V,V.conj().T);ck.check('native_selected_norm_bound',max(0.,max(source_norm)-1.))
    ck.check('free_energy_commutator',(free[:,None]-free[None,:])*V)
    used=[i for ix in components for i in ix]
    if len(used)!=len(set(used)):raise AssertionError('Disjoint structural components')
    remaining=sorted(set(range(256))-set(used));mask=np.ones((256,256),bool)
    for ix in components:mask[np.ix_(ix,ix)]=False
    ck.check('all_off_component_couplings',V[mask])
    absent=bool(max(np.linalg.norm(a,'fro') for a in A)<=CFG['operator_tolerance'])
    return A,V,free,components,remaining,dict(source_blocks=blocks,source_block_norms=source_norm,numerical_resolution_absent=absent,components=components,spectator_indices=remaining)

def taylor_action(k,initial,T):
    # Independent direct small-block Taylor; no spectral function/import used.
    x=abs(T)*float(np.max(np.sum(abs(k),axis=1)));term=initial.copy();out=term.copy()
    for order in range(1,CFG['taylor_max_terms']+1):
        term=(-1j*T/order)*(k@term);out+=term
        tail=math.exp(x+(order+1)*math.log(x)-math.lgamma(order+2)) if x else 0.
        if tail<CFG['taylor_tail']:return out,dict(terms=order,norm_argument=x,analytic_tail=tail)
    raise ArithmeticError('Prospective Taylor max-term guard')

def evolve(V,free,components,initial,g,T,ck):
    final=np.exp(-1j*free*T)[:,None]*initial;oracle=final.copy();methods=[]
    for ix in components:
        vc=V[np.ix_(ix,ix)]
        if not np.any(vc):continue
        center=float(np.mean(free[ix]));k=np.diag(free[ix]-center)+g*vc
        val,U=np.linalg.eigh(k);ck.check('small_component_eigen_residual',k@U,U*val,tol=CFG['state_tolerance']);ck.check('small_component_unitarity',U.conj().T@U,np.eye(len(ix)),tol=CFG['state_tolerance'])
        z=initial[ix];out=U@(np.exp(-1j*val*T)[:,None]*(U.conj().T@z));dual,info=taylor_action(k,z,T)
        final[ix]=np.exp(-1j*center*T)*out;oracle[ix]=np.exp(-1j*center*T)*dual;methods.append(dict(indices=ix,free_span=float(np.ptp(free[ix])),**info))
    errors=np.linalg.norm(final-oracle,axis=0);ck.check('independent_shifted_Taylor_action',errors,tol=CFG['state_tolerance'])
    return final,errors,methods

def packrho(rho):return [float(x.real) for x in np.diag(rho)]+[v for i in range(4) for j in range(i+1,4) for v in (float(rho[i,j].real),float(rho[i,j].imag))]

def gap_packet(q,g,e,hb,groups,O,holds,initial,meta):
    ck=Checks();out=dict(q=q,gap_ID=g['ID'],gap=g,row_fields=ROW_FIELDS,row_order='coupling,duration,incoming_column',checks=None,rows=[],comparisons=[],weak_coefficients=[],methods=[])
    if g['status']!='QUALIFIED_FINITE_RESOLUTION_GAP_GROUP':
        out['refused_row_count']=108;out['checks']=ck.data();return out
    A,V,free,components,spectators,structure=gap_operator(g,groups,O,e,ck);out['structure']=structure
    remainder=float(np.linalg.norm(hb-np.diag(e),'fro'));commdiag=float(np.linalg.norm((free[:,None]-free[None,:])*V,'fro'))
    structure['spectral_diagonal_commutator_F']=commdiag;structure['native_frame_remainder_F']=remainder;structure['full_native_free_commutator_error_estimate']=commdiag+4*remainder;structure['directed_error_bounds']=False
    lower=np.array([[0.,1.],[0.,0.]]);ap=[np.kron(lower,np.eye(2)),np.kron(np.eye(2),lower)];num=[a.T@a for a in ap];cross=ap[0].T@ap[1]
    coefficients=[]
    for p in holds:
        avg=[np.vdot(p,a@p) for a in A];down=[float(np.linalg.norm(a@p)**2) for a in A];up=[float(np.linalg.norm(a.conj().T@p)**2) for a in A]
        coh=np.vdot(A[0]@p,A[1]@p);coefficients.append((avg,down,up,coh));out['weak_coefficients'].append(dict(mean=cjson(avg),down=down,reverse=up,cross=cjson(coh),connected=cjson(coh-avg[0].conjugate()*avg[1])))
    nprobe=np.array([0.,1.,1.,2.]);initial_shape=initial.reshape(64,4,18);initial_hfree=(hb@initial_shape.reshape(64,72)).reshape(64,4,18)+g['omega']*nprobe[None,:,None]*initial_shape
    f0=np.sum(initial_shape.conj()*initial_hfree,axis=(0,1)).real;f20=np.sum(abs(initial_hfree)**2,axis=(0,1))
    initV=np.sum(initial.conj()*(V@initial),axis=0);ck.check('initial_number_state_port_mean',initV)
    diag_probe=g['omega']*np.tile(nprobe,64);cache={}
    for coupling in CFG['couplings']:
        for T in CFG['durations']:
            final,errors,methods=evolve(V,free,components,initial,coupling,T,ck);out['methods'].append(dict(g=coupling,T=T,components=methods,native_frame_propagator_remainder_estimate=T*remainder,free_mean_endpoint_error_estimate=abs(coupling)*T*commdiag+2*remainder,directed=False))
            beta=2*abs(coupling)*T;r2=math.cosh(beta)-1.;r3=math.sinh(beta)-beta
            pbound=2*beta*r3+r3*r3+r2*r2;cbound=2*beta*r3+r3*r3;mbound=r3+2*r2*math.sinh(beta);kbound=cbound+2*beta*mbound+mbound*mbound
            ck.check('analytic_port_V_bound',max(0.,max(out['structure']['source_block_norms'])-1.))
            vstate=V@final;shaped=final.reshape(64,4,18);native_action=(hb@shaped.reshape(64,72)).reshape(64,4,18);free_action=native_action+g['omega']*nprobe[None,:,None]*shaped
            native_means=np.sum(shaped.conj()*native_action,axis=(0,1)).real;free_seconds=np.sum(abs(free_action)**2,axis=(0,1))
            for col,m in enumerate(meta):
                tag=f'{q}:{g["ID"]}:{coupling}:{T}:{col}';psi=final[:,col];prob=abs(psi)**2
                en=float(native_means[col]);ed=float(np.dot(prob,diag_probe));ev=coupling*float(np.vdot(psi,vstate[:,col]).real);norm=float(sum(prob));second=float(free_seconds[col])
                initial_probe=g['omega']*m['probe_input'].count('1');dn=en-m['native_energy'];dd=ed-initial_probe;won=coupling*float(initV[col].real);woff=-ev;ledger=dn+dd-won-woff
                ck.check('native_plus_probe_debit',dn+dd,tol=CFG['energy_tolerance'],tag=tag);ck.check('interaction_mean_zero',ev,tol=CFG['energy_tolerance'],tag=tag);ck.check('on_energy_conservation',en+ed+ev,f0[col]+won,CFG['energy_tolerance'],tag);ck.check('cyclic_switch_work_ledger',ledger,tol=CFG['energy_tolerance'],tag=tag)
                ck.check('state_norm',norm,1.,CFG['state_tolerance'],tag);ck.check('free_second_moment',second,f20[col],CFG['energy_tolerance'],tag)
                shape=psi.reshape(64,4);rho=shape.T@shape.conj();ck.check('probe_density_Hermitian',rho,rho.conj().T,tag=tag);ck.check('probe_density_trace',np.trace(rho),1.,CFG['state_tolerance'],tag);ck.check('probe_density_PSD',max(0.,-float(np.linalg.eigvalsh(rho).min())),tol=CFG['state_tolerance'],tag=tag)
                occupation=[float(np.trace(rho@n).real) for n in num];means=np.array([np.trace(rho@a) for a in ap]);coh=np.trace(rho@cross);conn=coh-means[0].conjugate()*means[1]
                ck.check('probe_energy_occupations',g['omega']*sum(occupation),ed,CFG['state_tolerance'],tag)
                avg,down,up,c0=coefficients[col//3];weak=[T*T*(up[j] if m['probe_input'][j]=='1' else down[j]) for j in range(2)];flip=[1-occupation[j] if m['probe_input'][j]=='1' else occupation[j] for j in range(2)]
                for j in range(2):ck.check('population_Dyson_bound',max(0.,abs(flip[j]-coupling**2*weak[j])-pbound),tol=CFG['weak_roundoff'],tag=tag+':'+str(j))
                if m['probe_input']=='00':
                    expected=-1j*coupling*T*np.exp(-1j*g['omega']*T)*np.array(avg)
                    ck.check('vacuum_mean_Dyson_bound',max(0.,float(max(abs(means-expected)))-mbound),tol=CFG['weak_roundoff'],tag=tag)
                    ck.check('vacuum_cross_Dyson_bound',max(0.,abs(coh-coupling**2*T*T*c0)-cbound),tol=CFG['weak_roundoff'],tag=tag)
                    ck.check('vacuum_connected_Dyson_bound',max(0.,abs(conn-coupling**2*T*T*(c0-avg[0].conjugate()*avg[1]))-kbound),tol=CFG['weak_roundoff'],tag=tag)
                row=[en,initial_probe,ed,ev,en+ed+ev,dn,dd,won,woff,ledger,norm,float(f20[col]),second,float(errors[col])]+flip+weak+[flip[j]/coupling**2-weak[j] for j in range(2)]+packrho(rho)
                if len(row)!=len(ROW_FIELDS):raise AssertionError('Frozen compact row columns')
                out['rows'].append(row);cache[(coupling,T,col)]=(flip,coh,conn,np.diag(rho).real)
            for label in range(2):
                for inp in range(3):
                    x=cache[(coupling,T,label*9+inp)]
                    for age in (1,2):
                        y=cache[(coupling,T,label*9+3*age+inp)]
                        ck.check('age_invariant_number_and_equal_gap_cross',np.r_[y[3]-x[3],y[1]-x[1]],tol=CFG['state_tolerance'],tag=f'{q}:{g["ID"]}:{label}:{inp}:{age}')
    for T in CFG['durations']:
        for col in range(18):
            a,b=[cache[(x,T,col)] for x in CFG['couplings']]
            out['comparisons'].append(dict(T=T,column=col,signed_halving_scaled_flip_difference=[b[0][j]/CFG['couplings'][1]**2-a[0][j]/CFG['couplings'][0]**2 for j in range(2)],signed_halving_scaled_cross_difference=cjson(b[1]/CFG['couplings'][1]**2-a[1]/CFG['couplings'][0]**2),signed_halving_scaled_connected_difference=cjson(b[2]/CFG['couplings'][1]**2-a[2]/CFG['couplings'][0]**2)))
    if len(out['rows'])!=108 or len(out['comparisons'])!=54:raise AssertionError('All inherited columns/windows/halving controls')
    out['checks']=ck.data();return out

def journal(event,**data):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(encoded(dict(event=event,owner='root',pid=os.getpid(),epoch=EPOCH,time=now(),source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,**data)).decode())

def validate_payload(payload,stage):
    if payload['stage']!=stage:raise AssertionError('Checkpoint stage identity')
    if stage.startswith('SPECTRAL_'):
        w=payload['witness'];q=int(stage.rsplit('_',1)[1])
        if w['q']!=q or len(w['eigenvalues'])!=64 or len(w['groups'])!=48 or w['pair_count']!=1128 or sorted(p['ID'] for g in w['gap_groups'] for p in g['pairs'])!=sorted(f'{i}:{j}' for i in range(48) for j in range(i+1,48)):raise AssertionError('Full native spectral/pair checkpoint census')
    else:
        q,start,end=[int(x) for x in stage.split('_')[1:]];packets=payload['gap_packets']
        if [p['gap_ID'] for p in packets]!=list(range(start,end)) or any(p['q']!=q or p['row_fields']!=ROW_FIELDS for p in packets):raise AssertionError('Full gap bundle identity')
        for p in packets:
            qualified=p['gap']['status']=='QUALIFIED_FINITE_RESOLUTION_GAP_GROUP'
            if (len(p['rows'])!=(108 if qualified else 0) or len(p['comparisons'])!=(54 if qualified else 0) or (not qualified and p['refused_row_count']!=108) or any(len(row)!=len(ROW_FIELDS) or not all(math.isfinite(v) for v in row) for row in p['rows'])):raise AssertionError('Full committed gap row schema/census')

def runtime_start(manifest,resume):
    global RUN_MANIFEST,EPOCH
    mp=BASE/(STEM+'_MANIFEST.json');jp=BASE/(STEM+'_JOURNAL.jsonl');existing=list(BASE.glob(STEM+'_*'))
    if not resume:
        if existing:raise FileExistsError('Existing runtime prefix preserved')
        RUN_MANIFEST=write(mp.name,manifest);EPOCH=0;journal('OWNER_START');return {}
    if not mp.exists() or not jp.exists() or read(mp)!=manifest or any(p.name.startswith((STEM+'_FAILED',STEM+'_RESULT',STEM+'_RECEIPT',STEM+'_REPORT')) for p in existing):raise AssertionError('No resume of completed/failed/orphan/changed run')
    RUN_MANIFEST=sha(mp);CREATED[str(mp.resolve())]=RUN_MANIFEST;events=[json.loads(s) for s in jp.read_text().splitlines()]
    completed={};owners={};last_cp=-1;expected={mp.name,jp.name}
    for ev in events:
        if ev['owner']!='root' or ev['source_sha256']!=RUN_SOURCE or ev['manifest_sha256']!=RUN_MANIFEST:raise AssertionError('Journal root/source/manifest')
        ep=ev['epoch']
        if ev['event']=='OWNER_START':
            if ep!=len(owners) or ep in owners or not isinstance(ev['pid'],int):raise AssertionError('Owner epoch')
            owners[ep]=ev['pid']
        elif ev['event']=='CHECKPOINT':
            if ep not in owners or ev['pid']!=owners[ep] or ev['index']!=last_cp+1 or ev['stage'] in completed:raise AssertionError('Ordered committed root checkpoint')
            pn=STEM+f'_CP{ev["index"]:04d}.json';cn=STEM+f'_CP{ev["index"]:04d}_COMMIT.json'
            if ev['payload']!=pn or ev['commit']!=cn or sha(BASE/pn)!=ev['payload_sha256'] or sha(BASE/cn)!=ev['commit_sha256']:raise AssertionError('Committed byte digest')
            co=read(BASE/cn);payload=read(BASE/pn)
            if co!=dict(source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,owner='root',pid=ev['pid'],epoch=ep,index=ev['index'],stage=ev['stage'],payload=pn,payload_sha256=ev['payload_sha256']):raise AssertionError('Commit source/owner/stage')
            validate_payload(payload,ev['stage']);completed[ev['stage']]=(payload,pn,cn);last_cp+=1;expected.update((pn,cn))
            CREATED[str((BASE/pn).resolve())]=ev['payload_sha256'];CREATED[str((BASE/cn).resolve())]=ev['commit_sha256']
        else:raise AssertionError('Unexpected runtime journal event')
    if not owners or events[0]['event']!='OWNER_START' or {p.name for p in existing}!=expected:raise AssertionError('Uncommitted/orphan runtime files preserved/refused')
    EPOCH=len(owners);journal('OWNER_START');return completed

def checkpoint(stage,payload,completed,index):
    if stage in completed:
        old,pn,cn=completed[stage]
        if old!=payload:raise AssertionError('Changed committed checkpoint')
        return pn,cn
    validate_payload(payload,stage);pn=STEM+f'_CP{index:04d}.json';cn=STEM+f'_CP{index:04d}_COMMIT.json';ph=write(pn,payload)
    ch=write(cn,dict(source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,owner='root',pid=os.getpid(),epoch=EPOCH,index=index,stage=stage,payload=pn,payload_sha256=ph));journal('CHECKPOINT',index=index,stage=stage,payload=pn,commit=cn,payload_sha256=ph,commit_sha256=ch);return pn,cn

def validate_runtime_prefix(references):
    events=[json.loads(s) for s in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()];owners={};cp=[]
    for ev in events:
        if ev['owner']!='root' or ev['source_sha256']!=RUN_SOURCE or ev['manifest_sha256']!=RUN_MANIFEST:raise AssertionError('Final root/source/manifest journal')
        ep=ev['epoch']
        if ev['event']=='OWNER_START':
            if ep!=len(owners) or ep in owners:raise AssertionError('Final owner epoch')
            owners[ep]=ev['pid']
        elif ev['event']=='CHECKPOINT':
            i=len(cp)
            if ep not in owners or ev['pid']!=owners[ep] or ev['index']!=i or i>=len(references):raise AssertionError('Final complete checkpoint prefix')
            r=references[i];co=read(BASE/r['commit']);payload=read(BASE/r['payload'])
            if ev['stage']!=r['stage'] or ev['payload']!=r['payload'] or ev['commit']!=r['commit'] or sha(BASE/r['payload'])!=r['sha256'] or r['sha256']!=ev['payload_sha256'] or sha(BASE/r['commit'])!=ev['commit_sha256']:raise AssertionError('Final full committed bytes')
            if co!=dict(source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,owner='root',pid=ev['pid'],epoch=ep,index=i,stage=r['stage'],payload=r['payload'],payload_sha256=r['sha256']):raise AssertionError('Final source/owner commit')
            validate_payload(payload,r['stage']);cp.append(r['stage'])
        else:raise AssertionError('Unexpected prepublication journal event')
    if not owners or owners.get(EPOCH)!=os.getpid() or len(cp)!=len(references):raise AssertionError('Complete current owner/census')
    expected={STEM+'_MANIFEST.json',STEM+'_JOURNAL.jsonl'}|{r[k] for r in references for k in ('payload','commit')}
    if {p.name for p in BASE.glob(STEM+'_*')}!=expected:raise AssertionError('Final orphan/runtime namespace')

def main(resume):
    global RUN_SOURCE
    tick=time.monotonic();RUN_SOURCE=sha(__file__);old=authenticate()
    manifest=dict(source_sha256=RUN_SOURCE,input_sha256=dict(SEALS),configuration=CFG,parameters=PARAMETERS,record_parameters=RECORD_PARAMETERS,numpy_version=np.__version__,row_fields=ROW_FIELDS,scope='NEW adopted selective coupling; numerical-resolution spectral groups, no thermal/photon/physical-volume/cosmology qualification')
    completed=runtime_start(manifest,resume);aggregate=Checks();references=[];index=0;qualified=refused=rows=absent=0;maxdim=0
    stages=[]
    for q in CFG['record_occupations']:
        saved=next(s for s in old['sectors'] if s['record_occupation']==q);stage=f'SPECTRAL_{q}'
        wit=completed[stage][0]['witness'] if stage in completed else None
        witness,e,hb,groups,gaps,O,holds,initial,meta=spectral(q,saved,wit);payload=dict(stage=stage,witness=witness,incoming_columns=meta)
        stages.append(stage);pn,cn=checkpoint(stage,payload,completed,index);index+=1;aggregate.merge(witness['checks']);references.append(dict(stage=stage,payload=pn,commit=cn,sha256=sha(BASE/pn)))
        for start in range(0,len(gaps),CFG['bundle_gap_count']):
            end=min(len(gaps),start+CFG['bundle_gap_count']);stage=f'GAPS_{q}_{start}_{end}';stages.append(stage)
            if stage in completed:
                payload=completed[stage][0]
                if [p['gap'] for p in payload['gap_packets']]!=gaps[start:end]:raise AssertionError('Changed resumed gap membership')
            else:payload=dict(stage=stage,gap_packets=[gap_packet(q,g,e,hb,groups,O,holds,initial,meta) for g in gaps[start:end]])
            pn,cn=checkpoint(stage,payload,completed,index);index+=1;references.append(dict(stage=stage,payload=pn,commit=cn,sha256=sha(BASE/pn)))
            for p in payload['gap_packets']:
                aggregate.merge(p['checks']);rows+=len(p['rows'])
                if p['gap']['status']=='QUALIFIED_FINITE_RESOLUTION_GAP_GROUP':
                    qualified+=1;absent+=int(p['structure']['numerical_resolution_absent']);maxdim=max(maxdim,max((len(x) for x in p['structure']['components']),default=0))
                else:refused+=1
            recheck();print(json.dumps(dict(q=q,gap_range=[start,end],checkpoint=pn,rows_retained=rows,unresolved_groups=refused)),flush=True)
    if list(completed)!=stages[:len(completed)] or rows!=108*qualified or qualified+refused>2256:raise AssertionError('All completed stages/full row census')
    validate_runtime_prefix(references)
    aggregate.check('complete_pair_census',sum(1128 for _ in CFG['record_occupations']),2256)
    ok=not aggregate.failures;status='SELECTIVE_PORT_ARITHMETIC_FAILED' if not ok else ('SELECTIVE_PORT_ARITHMETIC_PASS_WITH_REFUSALS' if refused else 'SELECTIVE_PORT_ARITHMETIC_PASS')
    result=dict(status=status,manifest=manifest,checks=aggregate.data(),checkpoint_references=references,census=dict(record_sectors=2,native_energy_groups=96,positive_pair_IDs=2256,zero_elastic_groups=96,qualified_gap_groups=qualified,unresolved_gap_groups=refused,refused_implied_rows=108*refused,retained_rows=rows,numerical_resolution_absent_groups_retained=absent,halving_comparisons=54*qualified,maximum_component_dimension=maxdim),elapsed_seconds=time.monotonic()-tick,scope=manifest['scope'],residual_estimates_directed=False,final_vectors_saved=False)
    recheck();rh=write(STEM+'_RESULT.json',result)
    report=dict(title='NEW native energy-selective calorimeter ports V001',status=status,census=result['census'],maxima=aggregate.maxima,failures=aggregate.failures,energy_ledger='All absolute native terms retained; both probe directions and switching work retained. Expected zero switching work is the selective-port theorem, checked at frozen finite resolution.',qualification='Actual coupling is new gap-aggregated Aomega, not the completed local rectangular port; no Gibbs reset, common temperature, photon/irreversible bath or cosmic attribution.')
    recheck();reph=write(STEM+'_REPORT.json',report);journal('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=index)
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=RUN_SOURCE,manifest=manifest,manifest_sha256=RUN_MANIFEST,result_sha256=rh,report_sha256=reph,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),output_sha256=dict(CREATED),checkpoint_count=index))
    recheck();print(json.dumps(dict(status=status,census=result['census'],elapsed_seconds=result['elapsed_seconds'])),flush=True);return 0 if ok else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    if not args.execute:raise SystemExit('Root alone launches --execute')
    if (not args.resume and list(BASE.glob(STEM+'_*'))) or (args.resume and any(p.name.startswith((STEM+'_FAILED',STEM+'_RESULT',STEM+'_RECEIPT',STEM+'_REPORT')) for p in BASE.glob(STEM+'_*'))):raise SystemExit('Existing completed/failed/non-resumed namespace preserved')
    try:raise SystemExit(main(args.resume))
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),owner='root',pid=os.getpid(),time=now(),source_sha256=sha(__file__)))
        raise
