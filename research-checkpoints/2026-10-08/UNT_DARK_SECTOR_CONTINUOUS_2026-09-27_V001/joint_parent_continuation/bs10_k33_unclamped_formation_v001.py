#!/usr/bin/env python3
"""Prospective full native K3,3 incidence/record witness; no old solver replay."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import gc,hashlib,json,math,os,resource,socket,sys,time,traceback
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001.md'
SOURCE=HERE/'bs10_k33_unclamped_formation_v001.py'
RESULT=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json'
REPORT=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.md'
CP=HERE/'bs10_k33_unclamped_formation_v001_checkpoints'
OLD=HERE/'BS10_SIX_RECORD_FORMATION_V001_RESULT.json'
NATIVE=HERE.parent/'recovered_sources/BS_MICRO_ACTION.md'
EDGES=tuple((i,3+j) for i in range(3) for j in range(3))
UD,ER,EP,LR,LJ,OMEGA,N,THOP=1.,1.,1.,.5,.25,.6,3,.1
HFLIP=OMEGA/N
GS=(0.,.1);STARTS=(0,413);TIMES=(0.,1.,2.,5.,10.,20.,50.);TINY=(.001,.002)
SCHEDULE=[('main'+str(i),t,False) for i,t in enumerate(TIMES)]
SCHEDULE += [('early'+str(i)+'_'+sign,sgn*t,True) for i,t in enumerate(TINY) for sign,sgn in [('plus',1),('minus',-1)]]
DIM,M,FFT_N,ALPHA=196608,1200,8192,1.
CENTER,PAD=16.25,1e-12
OP_TOL,OBS_TOL,PSD_TOL=1e-11,2e-8,1e-11
TAYLOR_DEGREE=160;MAX_RSS=512*1024*1024;MAX_SECONDS=180.
PERM=(0,2,1,5,4,3)

def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def exclusive(path,value):
    with path.open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def event(kind,**values):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=kind,utc=utc(),pid=os.getpid(),**values),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def check(items,name,passed,evidence=None):
    item=dict(name=name,passed=bool(passed))
    if evidence is not None:item['evidence']=evidence
    items.append(item)
def cjson(a):return dict(real=a.real.tolist(),imag=a.imag.tolist())
def inputs():return dict(dimension=DIM,Nc=1,N=N,edges=[list(e) for e in EDGES],exterior_registers=0,
    dynamic_incidence='all9',dynamic_records='all6',U_d=UD,Delta=0,d_star=2,epsilon_r=ER,epsilon_psi=EP,
    lambda_R=LR,lambda_J=LJ,Omega=OMEGA,h_N=HFLIP,t=THOP,g=list(GS),other_copy_ports=0,
    starts=list(STARTS),cycle_edges=[0,2,3,4,7,8],carrier_start=0,record_start='allblank',
    times=list(TIMES),tiny=list(TINY),Chebyshev_degree=M,FFT_N=FFT_N,refinement_FFT_N=2*FFT_N,
    tail_alpha=ALPHA,center=CENTER,outward_halfwidth_pad=PAD,certified_truncation_alias_limit=1e-12,
    coefficient_refinement_l1_limit=2e-11,Taylor_degree=TAYLOR_DEGREE,Taylor_tau=1.,
    source_tolerance=OP_TOL,observable_tolerance=OBS_TOL,PSD_tolerance=PSD_TOL,
    BLAS_threads=1,node_weight_arm=[1.000001,.999998,1.000003,.999999,1.000002,.999997],
    source_scope='six-node ownership algebra only; no geometry/physical gravity',
    graph_permutation=list(PERM),conditional_coherent_content_witness='same pure seed,content|+>',
    peak_RSS_limit_bytes=MAX_RSS,Hamiltonian_time_limit_seconds=MAX_SECONDS)
def anchors():
    old=json.loads(OLD.read_text())
    if old['status']!='QUALIFIED_ARITHMETIC' or old['failed_count']:raise RuntimeError('Old native witness unqualified')
    paths=[PROTOCOL,SOURCE,NATIVE,OLD,HERE/'NATIVE_DETUNED_JOINT_WORK_PROTOCOL_V001.md',
        HERE/'NATIVE_DETUNED_JOINT_WORK_V001_RESULT.json',HERE/'NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md',
        HERE.parent/'NATIVE_OVERLAPPING_RECORD_PAID_FORMATION_V001.md']
    paths += [Path(p) for p in old['input_sha256']]
    hashes={str(p):sha(p) for p in paths}
    for path,digest in old['input_sha256'].items():
        if hashes[path]!=digest:raise RuntimeError('Old source/native anchor changed')
    for h in old['Hamiltonians']:
        for row in h['states']:
            bundle=Path(row['bundle_path'])
            if str(bundle) not in hashes:hashes[str(bundle)]=sha(bundle)
            if hashes[str(bundle)]!=row['bundle_sha256']:raise RuntimeError('Old state bundle changed')
    return hashes

def graph_metadata(np,bits,degrees):
    comps=[];largest=[];carrier_size=[]
    for mask in range(512):
        adj=[set() for _ in range(6)]
        for edge,(u,v) in enumerate(EDGES):
            if (mask>>edge)&1:adj[u].add(v);adj[v].add(u)
        unseen=set(range(6));groups=[]
        while unseen:
            todo=[min(unseen)];group=set()
            while todo:
                v=todo.pop()
                if v not in group:group.add(v);todo.extend(adj[v]-group)
            unseen-=group;groups.append(group)
        comps.append(len(groups));largest.append(max(map(len,groups)))
        carrier_size.append([next(len(group) for group in groups if v in group) for v in range(6)])
    edgecount=bits.sum(axis=1).astype(int);comp=np.array(comps);two=np.all(degrees==2,axis=1)
    return dict(M=edgecount,components=comp,largest=np.array(largest),carrier_size=np.array(carrier_size),
        connected=comp==1,degree2=two,cycle=two&(comp==1),cycle_rank=edgecount-6+comp)

def fields(np,g):
    rows=np.arange(DIM);ns=rows//384;c=(rows//64)%6;r=rows%64
    bits=np.array([[(mask>>e)&1 for e in range(9)] for mask in range(512)],dtype=np.uint8)
    rbits=np.array([[(mask>>v)&1 for v in range(6)] for mask in range(64)],dtype=np.uint8)
    deg=np.zeros((512,6),dtype=np.int16)
    for e,(u,v) in enumerate(EDGES):deg[:,u]+=bits[:,e];deg[:,v]+=bits[:,e]
    d=deg[ns];q=rbits[r];p=np.eye(6)[c];nb=bits[ns]
    current=LJ*d[rows,c].astype(float);feedback=-LR*np.sum(q*d,axis=1)
    parts=dict(degree=UD*np.sum((d-2)**2,axis=1),carrier_storage=np.full(DIM,EP),
        record_storage=ER*q.sum(axis=1),current_square=current,record_feedback=feedback)
    D=sum(parts.values());flips=[((ns^(1<<e))*6+c)*64+r for e in range(9)]
    neighbors=np.array([[3+j for j in range(3)] if v<3 else [i for i in range(3)] for v in range(6)])
    edge_for=np.array([[3*v+j for j in range(3)] if v<3 else [3*i+(v-3) for i in range(3)] for v in range(6)])
    targets=[(ns*6+neighbors[c,j])*64+r for j in range(3)]
    hop_edges=[edge_for[c,j] for j in range(3)];activity=[nb[rows,e] for e in hop_edges]
    copy=(ns*6+c)*64+(r^(1<<c))
    perm_edges=[]
    for u,v in EDGES:
        a,b=PERM[u],PERM[v];perm_edges.append(3*a+(b-3))
    mapn=np.array([sum(((mask>>e)&1)<<perm_edges[e] for e in range(9)) for mask in range(512)])
    mapr=np.array([sum(((mask>>v)&1)<<PERM[v] for v in range(6)) for mask in range(64)])
    perm=(mapn[ns]*6+np.array(PERM)[c])*64+mapr[r]
    return dict(rows=rows,ns=ns,c=c,r=r,p=p,q=q,nb=nb,bits=bits,d=d,deg=deg,D=D,parts=parts,
        flips=flips,targets=targets,hop_edges=hop_edges,activity=activity,copy=copy,perm=perm,g=g,
        graph=graph_metadata(np,bits,deg))

def apply(np,f,v):
    out=f['D']*v
    for idx in f['flips']:out-=HFLIP*v[idx]
    for idx,active in zip(f['targets'],f['activity']):out-=THOP*active*v[idx]
    out+=f['g']*v[f['copy']]
    return out
def weighted(np,f,v,Nv):
    diagonal=np.zeros(DIM)
    for node in range(6):
        diagonal+=Nv[node]*(UD*(f['d'][:,node]-2)**2+ER*f['q'][:,node]+EP*f['p'][:,node])
    mid=np.array([(Nv[u]+Nv[w])/2 for u,w in EDGES])
    for edge,(u,w) in enumerate(EDGES):
        diagonal+=mid[edge]*f['nb'][:,edge]*(LJ*(f['p'][:,u]+f['p'][:,w])-LR*(f['q'][:,u]+f['q'][:,w]))
    out=diagonal*v
    for edge,idx in enumerate(f['flips']):out-=HFLIP*mid[edge]*v[idx]
    for idx,active,edges in zip(f['targets'],f['activity'],f['hop_edges']):out-=THOP*active*mid[edges]*v[idx]
    out+=f['g']*Nv[f['c']]*v[f['copy']]
    return out

def logtail(z,K):return math.log(2)+abs(z)*math.sinh(ALPHA)-K*ALPHA-math.log1p(-math.exp(-ALPHA))
def coefficient_table(np,a):
    coefficients=[];controls=[]
    for key,tau,early in SCHEDULE:
        z=a*tau
        if tau==0:
            cn=np.zeros(M+1,dtype=complex);cn[0]=1;error=0.;lt=la=total_log=None;bound=0.
        else:
            first=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(FFT_N)/FFT_N)))/FFT_N
            second=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(2*FFT_N)/(2*FFT_N))))/(2*FFT_N)
            c1=first[:M+1].copy();cn=second[:M+1].copy();c1[1:]*=2;cn[1:]*=2
            error=float(np.sum(np.abs(c1-cn)));lt=logtail(z,M+1);la=math.log(2*M+1)+logtail(z,FFT_N-M)
            hi=max(lt,la);total_log=hi+math.log(math.exp(lt-hi)+math.exp(la-hi))
            bound=math.exp(total_log) if total_log>-690 else 1e-300
        controls.append(dict(key=key,tau=tau,truncation_log=lt,alias_log=la,certified_total_log=total_log,
            certified_error_ceiling=bound,coefficient_refinement_l1=error,passed=bound<1e-12 and error<2e-11))
        coefficients.append(cn*np.exp(-1j*CENTER*tau))
    return np.array(coefficients),controls
def propagate(np,f,seed,a,coeff):
    v0=np.zeros(DIM,dtype=complex);v0[seed]=1
    states=coeff[:,0,None]*v0[None,:]
    v1=(apply(np,f,v0)-CENTER*v0)/a;states+=coeff[:,1,None]*v1[None,:]
    for m in range(2,M+1):
        v2=2*(apply(np,f,v1)-CENTER*v1)/a-v0;states+=coeff[:,m,None]*v2[None,:];v0,v1=v1,v2
    return states
def taylor(np,f,seed):
    term=np.zeros(DIM,dtype=complex);term[seed]=1;out=term.copy()
    for k in range(1,TAYLOR_DEGREE+1):term=(-1j/k)*(apply(np,f,term)-CENTER*term);out+=term
    return out*np.exp(-1j*CENTER)

def preflight(np,f,a):
    checks=[];g=f['g'];R=9*HFLIP+THOP*f['d'][f['rows'],f['c']]+g
    check(checks,'nine_flip_maps_involutive',all(np.array_equal(idx[idx],f['rows']) for idx in f['flips']))
    check(checks,'copy_map_involutive',np.array_equal(f['copy'][f['copy']],f['rows']))
    for j,idx in enumerate(f['targets']):
        back=np.zeros(DIM,dtype=bool)
        for target,active in zip(f['targets'],f['activity']):back|=(target[idx]==f['rows'])&(active[idx]==f['activity'][j])
        check(checks,'carrier_hop_adjoint_'+str(j),bool(np.all(back)))
    check(checks,'exact_diagonal_range',float(f['D'].min())==1.5 and float(f['D'].max())==31.)
    rowbound=float(np.max((np.abs(f['D']-CENTER)+R)/a));check(checks,'absolute_rescaled_row_bound',rowbound<=1,dict(maximum=rowbound))
    check(checks,'integer_degree_lower_bound',bool(np.all((f['d']-2)*((f['d']-2)-f['q'])>=0)))
    check(checks,'current_hop_positive_block',LJ>=abs(THOP))
    probe=np.exp(1j*(np.arange(DIM)%257)/257)/np.sqrt(DIM)
    other=np.exp(1j*(np.arange(DIM)%193)/193)/np.sqrt(DIM)
    hp=apply(np,f,probe);ho=apply(np,f,other)
    check(checks,'complex_Hermitian_probe',abs(np.vdot(other,hp)-np.vdot(ho,probe))<=2e-10)
    check(checks,'whole_node_ownership',np.max(np.abs(weighted(np,f,probe,np.ones(6))-hp))<=OP_TOL)
    check(checks,'uniform_lapse_algebra',np.max(np.abs(weighted(np,f,probe,np.full(6,.93))-.93*hp))<=OP_TOL)
    weights=np.array(inputs()['node_weight_arm']);perturb=weighted(np,f,probe,weights)-hp
    explicit=np.zeros(DIM,dtype=complex)
    for node in range(6):
        unit=np.zeros(6);unit[node]=weights[node]-1;explicit+=weighted(np,f,probe,unit)
    check(checks,'node_weight_linearity',np.max(np.abs(perturb-explicit))<=OP_TOL)
    pm=f['perm'];check(checks,'graph_permutation_involutive',np.array_equal(pm[pm],f['rows']))
    check(checks,'graph_relabel_H_covariance',np.max(np.abs(apply(np,f,probe[pm])-hp[pm]))<=OP_TOL)
    meta=f['graph'];check(checks,'six_degree2_masks_all_connected',int(meta['degree2'].sum())==6 and np.array_equal(meta['degree2'],meta['cycle']))
    connected_max=float(f['D'][meta['connected'][f['ns']]].max())
    check(checks,'connected_exact_diagonal_maximum',connected_max==9.75,dict(maximum=connected_max))
    check(checks,'degree2_exact_diagonal_constant',bool(np.all(f['D'][meta['degree2'][f['ns']]]==1.5)))
    check(checks,'graph_degree_handshake',np.array_equal(f['deg'].sum(axis=1),2*meta['M']))
    check(checks,'nonnegative_cycle_rank',bool(np.all(meta['cycle_rank']>=0)))
    for start,initial,variance in [(0,25.,.36+g*g),(413,1.5,.38+g*g)]:
        seedidx=start*384;seed=np.zeros(DIM);seed[seedidx]=1;action=apply(np,f,seed)
        e=float(action[seedidx]);var=float(np.vdot(action,action).real-e*e);coefficient=f['q'].T@(np.abs(action)**2)
        check(checks,'initial_mean_'+str(start),abs(e-initial)<=OP_TOL,dict(value=e))
        check(checks,'initial_variance_'+str(start),abs(var-variance)<=OP_TOL,dict(value=var,expected=variance))
        check(checks,'positive_copy_sign_'+str(start),abs(action[seedidx+1]-g)<=OP_TOL)
        check(checks,'early_Hseed_q0_'+str(start),abs(float(coefficient[0])-g*g)<=OP_TOL)
        check(checks,'early_Hseed_otherq_'+str(start),np.max(np.abs(coefficient[1:]))<=OP_TOL)
        check(checks,'prepared_graph_relabel_invariant_'+str(start),pm[seedidx]==seedidx)
    remainder_log=a+(TAYLOR_DEGREE+1)*math.log(a)-math.lgamma(TAYLOR_DEGREE+2)
    check(checks,'Taylor_exact_remainder_bound',remainder_log<math.log(1e-12),dict(log_bound=remainder_log))
    return checks

def sqrt_density(np,rho):
    vals,V=np.linalg.eigh(rho)
    if vals[0]<-PSD_TOL:raise ArithmeticError('Record density violates PSD tolerance')
    root=(V*np.sqrt(np.maximum(vals,0)))@V.conj().T
    return root,vals,dict(negative_clip_count=int(np.sum(vals<0)),minimum=float(vals[0]),square_root_residual=float(np.max(np.abs(root@root-rho))))
def record_labels(np):
    masks=np.arange(64);zero=sum(((masks>>v)&1)*(3**v) for v in range(6));return zero,2*zero
def observe(np,f,start,tau,early,psi):
    checks=[];prob=np.abs(psi)**2;graphprob=prob.reshape(512,6,64).sum(axis=(1,2))
    rho=psi.reshape(3072,64).T@psi.reshape(3072,64).conj();root,eigs,info=sqrt_density(np,rho)
    P=float(np.real(rho[0,0]));gamma=P*P;labels0,labels1=record_labels(np)
    overlap=(labels0[:,None]==labels1[None,:]).astype(float);direct=complex(np.sum(overlap*rho))
    sv=np.linalg.svd(root@overlap@root,compute_uv=False);independent=float(np.sum(sv)**2)
    check(checks,'physical_alphabet_overlap_only_blank',int(overlap.sum())==1 and overlap[0,0]==1)
    check(checks,'full_state_norm',abs(float(prob.sum())-1)<=OBS_TOL)
    check(checks,'density_trace',abs(complex(np.trace(rho))-1)<=OBS_TOL)
    check(checks,'density_Hermitian',np.max(np.abs(rho-rho.conj().T))<=2e-10)
    check(checks,'density_PSD',float(eigs[0])>=-PSD_TOL)
    check(checks,'density_sqrt_residual',info['square_root_residual']<=OBS_TOL)
    check(checks,'physical729_fidelity_via_isometries',abs(independent-gamma)<=OBS_TOL,dict(independent=independent,probability_gamma=gamma,difference=independent-gamma))
    check(checks,'direct_content_overlap',abs(direct-P)<=OBS_TOL)
    content=np.array([[1,direct],[direct.conjugate(),1]],dtype=complex)/2
    purity=float(np.real(np.trace(content@content)));check(checks,'content_purity_relation',abs(purity-(1+gamma)/2)<=OBS_TOL)
    ce=np.array([(1+abs(direct))/2,(1-abs(direct))/2]);positive=ce[ce>0];cs=float(-np.sum(positive*np.log(positive)))
    q=prob@f['q'];p=prob@f['p'];n=prob@f['nb'];d=prob@f['d'];qdegree=prob@(f['q']*f['d'])
    energy={k:float(prob@v) for k,v in f['parts'].items()}
    energy['incidence_flip']=-HFLIP*sum(float(np.real(np.vdot(psi,psi[idx]))) for idx in f['flips'])
    energy['carrier_hopping']=-THOP*sum(float(np.real(np.vdot(psi,act*psi[idx]))) for idx,act in zip(f['targets'],f['activity']))
    energy['record_copy']=f['g']*float(np.real(np.vdot(psi,psi[f['copy']])))
    action=apply(np,f,psi);total=float(np.real(np.vdot(psi,action)));second=float(np.vdot(action,action).real)
    initial=25. if start==0 else 1.5;variance=(.36 if start==0 else .38)+f['g']**2
    check(checks,'complete_energy_components',abs(sum(energy.values())-total)<=OBS_TOL*max(1.,abs(total)))
    check(checks,'unitary_energy_conserved',abs(total-initial)<=OBS_TOL*max(1.,abs(initial)))
    check(checks,'energy_second_moment_conserved',abs(second-initial*initial-variance)<=OBS_TOL*max(1.,initial*initial+variance))
    node_energy=[float(np.real(np.vdot(psi,weighted(np,f,psi,np.eye(6)[v])))) for v in range(6)]
    check(checks,'six_owned_node_energies_sum',abs(sum(node_energy)-total)<=OBS_TOL*max(1.,abs(total)))
    degree_square=float(prob@np.sum((f['d']-2)**2,axis=1));bound=.5*degree_square-.8-f['g']
    check(checks,'native_degree_energy_lower_bound',total>=bound-OBS_TOL*max(1.,abs(total)),dict(E=total,lower_bound=bound))
    check(checks,'fixed_carrier_number',abs(float(p.sum())-1)<=OBS_TOL)
    meta=f['graph'];em=float(graphprob@meta['M']);conn=float(graphprob@meta['connected']);markov=min(1.,em/5)
    connection_energy_ceiling=min(1.,(31+2.1+f['g']-initial)/21.25)
    degree2_energy_ceiling=min(1.,(31+2.1+f['g']-initial)/29.5)
    degree2_probability=float(graphprob@meta['degree2'])
    check(checks,'connected_conserved_energy_ceiling',conn<=connection_energy_ceiling+OBS_TOL,dict(probability=conn,ceiling=connection_energy_ceiling))
    check(checks,'degree2_conserved_energy_ceiling',degree2_probability<=degree2_energy_ceiling+OBS_TOL,dict(probability=degree2_probability,ceiling=degree2_energy_ceiling))
    check(checks,'connected_M_bound',conn<=markov+OBS_TOL)
    if start==0:
        limit=math.sin(HFLIP*abs(tau))**2 if HFLIP*abs(tau)<=math.pi/2 else 1.
        check(checks,'blank_preparation_each_edge_speed_bound',float(n.max())<=limit+OBS_TOL,dict(limit=limit,maximum=float(n.max())))
        check(checks,'blank_preparation_M_speed_bound',em<=9*limit+OBS_TOL,dict(limit=9*limit,mean=em))
    check(checks,'degree_mean_handshake',abs(float(d.sum())-2*em)<=OBS_TOL)
    check(checks,'graph_probability_normalized',abs(float(graphprob.sum())-1)<=OBS_TOL)
    check(checks,'degree2_cycle_probability_equal',abs(float(graphprob@meta['degree2'])-float(graphprob@meta['cycle']))<=OBS_TOL)
    check(checks,'prepared_graph_relabel_trajectory',np.max(np.abs(psi-psi[f['perm']]))<=OBS_TOL)
    if f['g']==0:
        check(checks,'null_records_blank',float(q.sum())<=OBS_TOL and abs(P-1)<=OBS_TOL)
        check(checks,'null_visibility_gamma_one',abs(gamma-1)<=OBS_TOL)
    if early and f['g']!=0:
        leading=f['g']**2*tau**2
        for key,ratio in [('q0',float(q[0])/leading),('Pblank',(1-P)/leading),('gamma',(1-gamma)/(2*leading))]:check(checks,'early_coefficient_'+key,abs(ratio-1)<=1e-5,dict(ratio=ratio))
        check(checks,'early_otherrecords_no_tau_squared',float(q[1:].sum())<=1e-7*leading+1e-20)
    positive=eigs[eigs>0];entropy=float(-np.sum(positive*np.log(positive)))
    graphstats=dict(edge_mean=em,edge_count_distribution=[float(graphprob[meta['M']==k].sum()) for k in range(10)],
        connected_probability=conn,connected_M_bound=markov,components_mean=float(graphprob@meta['components']),
        connected_conserved_energy_ceiling=connection_energy_ceiling,degree2_conserved_energy_ceiling=degree2_energy_ceiling,
        component_count_distribution=[float(graphprob[meta['components']==k].sum()) for k in range(1,7)],
        largest_component_mean=float(graphprob@meta['largest']),
        largest_component_distribution=[float(graphprob[meta['largest']==k].sum()) for k in range(1,7)],
        carrier_component_mean=float(np.sum(prob.reshape(512,6,64).sum(axis=2)*meta['carrier_size'])),
        cycle_rank_mean=float(graphprob@meta['cycle_rank']),degree2_probability=float(graphprob@meta['degree2']),
        connected_degree2_cycle_probability=float(graphprob@meta['cycle']),blank_probability=float(graphprob[0]),
        graph512_probabilities=graphprob.tolist(),degree_square_mean=degree_square)
    return dict(g=f['g'],start=start,tau=tau,auxiliary_early_arm=early,P_allblank=P,gamma_rec=gamma,
        gamma_independent_physical_fidelity=independent,record_mean=q.tolist(),carrier_mean=p.tolist(),incidence_mean=n.tolist(),degree_mean=d.tolist(),
        record_degree_joint_mean=qdegree.tolist(),record_total=float(q.sum()),graph=graphstats,
        record_density64=cjson(rho),record_density_eigenvalues=eigs.tolist(),record_entropy=entropy,
        fidelity_square_root_diagnostic=info,fidelity_singular_values=sv.tolist(),physical729_content0_indices=labels0.tolist(),physical729_content1_indices=labels1.tolist(),
        coherent_content_density=cjson(content),direct_content_overlap=dict(real=direct.real,imag=direct.imag),fringe_visibility=abs(direct),
        coherent_content_purity=purity,coherent_content_entropy=cs,coherent_content_scope='same pure seed; content-exchange paired branches only',
        complete_energy=total,complete_energy_second_moment=second,initial_complete_energy=initial,initial_energy_variance=variance,
        complete_energy_components=energy,complete_owned_node_energy=node_energy,native_degree_energy_lower_bound=bound,
        checks=checks,failed_count=sum(not item['passed'] for item in checks))

def finish(receipt):
    checks=receipt['checks'][:]
    for h in receipt['Hamiltonians']:
        checks+=h['checks']
        for row in h['states']:checks+=row['checks']
    receipt.update(check_count=len(checks),passed_count=sum(c['passed'] for c in checks),failed_count=sum(not c['passed'] for c in checks),completed_utc=utc())
    payload=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with RESULT.open('xb') as out:out.write(payload)
    digest=hashlib.sha256(payload).hexdigest()
    lines=['# BS10 unclamped K3,3 formation V001: saved result','',f"Status {receipt['status']}; checks {receipt['passed_count']}/{receipt['check_count']}; failures {receipt['failed_count']}.",'',receipt['qualification'],'',
        '| g | seed | tau | mean M | P connected | total records | P_allblank / visibility | gamma_rec |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for h in receipt['Hamiltonians']:
        for row in h['states']:
            if not row['auxiliary_early_arm']:lines.append(f"| {row['g']:.2f} | {row['start']} | {row['tau']:.6g} | {row['graph']['edge_mean']:.9g} | {row['graph']['connected_probability']:.9g} | {row['record_total']:.9g} | {row['P_allblank']:.12g} | {row['gamma_rec']:.12g} |")
    lines+=['','Blank and cycle starts have different initial complete energies25/1.5 and retain both histories. Graph projectors are undirected connectivity diagnostics, not a physical geometry. Content visibility is the special pure paired-content construction; no irreversible sealing/bath/physical gravity claim.',
        '',f'Result JSON SHA256: {digest}',f"Runtime {receipt['runtime_seconds']:.6g}s; peak RSS {receipt['peak_RSS_bytes']} bytes; PID {receipt['pid']}.",f"Exact unfinished work: {receipt.get('next_unfinished')}"]
    with REPORT.open('x',encoding='utf-8') as out:out.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(status=receipt['status'],Hamiltonians=len(receipt['Hamiltonians']),states=sum(len(h['states']) for h in receipt['Hamiltonians']),checks=receipt['check_count'],passed=receipt['passed_count'],failed=receipt['failed_count'],runtime_seconds=receipt['runtime_seconds'],peak_RSS_bytes=receipt['peak_RSS_bytes'],json_sha256=digest,json_path=str(RESULT),markdown_path=str(REPORT),next_unfinished=receipt.get('next_unfinished'),exception=receipt.get('exception')),indent=2))

def execute(resume):
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Wrong local context')
    if RESULT.exists() or REPORT.exists():raise FileExistsError('Final receipt exists; no overwrite')
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
    custody=anchors();frozen=inputs();previous=[];mp=CP/'manifest.json'
    if resume:
        manifest=json.loads(mp.read_text());previous=[json.loads(line) for line in (CP/'events.jsonl').read_text().splitlines()]
        if manifest['inputs']!=frozen or manifest['input_sha256']!=custody or manifest['host']!=socket.gethostname():raise RuntimeError('Resume custody mismatch')
        starts=[e for e in previous if e['event']=='run_start'];pid=starts[-1]['pid'] if starts else manifest['pid']
        try:os.kill(pid,0)
        except ProcessLookupError:pass
        else:raise RuntimeError('Latest PID exists; ownership uncertain')
    else:CP.mkdir();exclusive(mp,dict(inputs=frozen,input_sha256=custody,host=socket.gethostname(),pid=os.getpid(),utc=utc()))
    began=time.perf_counter();receipt=dict(status='RUNNING',started_utc=utc(),pid=os.getpid(),host=socket.gethostname(),inputs=frozen,input_sha256=custody,Hamiltonians=[],checks=[],resume=resume,
        qualification='Full finite native K3,3 incidence/record/copy law and graph-invariant preparation histories; special pure content-coherence witness. No selected geometry, physical clock/ruler/volume, bath, irreversible sealing or gravitational/cosmological normalization.')
    event('run_start',resume=resume)
    def authenticated(path,kind,key):
        commits=[e for e in previous if e['event']==kind and e['key']==key]
        return bool(commits and commits[-1]['sha256']==sha(path))
    try:
        import numpy as np
        for ig,g in enumerate(GS):
            label='g'+str(ig);hp=CP/(label+'.json');receipt['next_unfinished']=dict(Hamiltonian=label,state='controls')
            if hp.exists():
                if not authenticated(hp,'Hamiltonian_complete',label):raise RuntimeError('Hamiltonian receipt mismatch')
                h=json.loads(hp.read_text())
                if h['input_sha256']!=custody:raise RuntimeError('Hamiltonian input mismatch')
                for bundle_name in {row['bundle_path'] for row in h['states']}:
                    refs=[row for row in h['states'] if row['bundle_path']==bundle_name];bundle=Path(bundle_name);key=label+'_n'+str(refs[0]['start'])
                    if bundle.parent!=CP or not authenticated(bundle,'bundle_saved',key):raise RuntimeError('Completed H bundle commit mismatch')
                    digest=sha(bundle)
                    if any(row['input_sha256']!=custody or row['bundle_sha256']!=digest for row in refs):raise RuntimeError('Completed H bundle input/hash mismatch')
                for row in h['states']:
                    statekey=label+'_n'+str(row['start'])+'_'+row['time_key'];rp=CP/(statekey+'.json')
                    if not authenticated(rp,'state_complete',statekey) or json.loads(rp.read_text())!=row:raise RuntimeError('Completed H state receipt mismatch')
                receipt['Hamiltonians'].append(h)
                if h['failed_count']:raise RuntimeError('Preserved failure forbids rerun')
                continue
            hbegan=time.perf_counter();f=fields(np,g);a=float(np.nextafter(14.75+9*HFLIP+3*THOP+g+PAD,np.inf))
            coeff,ccontrols=coefficient_table(np,a);controls=preflight(np,f,a)
            for item in ccontrols:check(controls,'certified_coefficients_'+item['key'],item['passed'],item)
            h=dict(g=g,input_sha256=custody,center=CENTER,halfwidth=a,coefficient_controls=ccontrols,checks=controls,states=[])
            pp=CP/(label+'_preflight.json')
            preflight_receipt=dict(input_sha256=custody,g=g,center=CENTER,halfwidth=a,coefficient_controls=ccontrols,checks=controls)
            if pp.exists():
                if not authenticated(pp,'preflight_complete',label) or json.loads(pp.read_text())!=preflight_receipt:raise RuntimeError('Preflight receipt custody mismatch')
            else:
                exclusive(pp,preflight_receipt);event('preflight_complete',key=label,sha256=sha(pp))
            h.update(preflight_path=str(pp),preflight_sha256=sha(pp))
            if any(not item['passed'] for item in controls):raise ArithmeticError('Preflight numerical control failed')
            for start in STARTS:
                bundle=CP/(label+'_n'+str(start)+'.bundle.npz');bundlekey=label+'_n'+str(start)
                if bundle.exists():
                    if not authenticated(bundle,'bundle_saved',bundlekey):raise RuntimeError('Bundle lacks matching journal commit; manual recovery required')
                    with np.load(bundle,allow_pickle=False) as data:
                        if json.loads(str(data['input_sha256_json']))!=custody or float(data['g'])!=g or int(data['start'])!=start or json.loads(str(data['schedule_json']))!=[list(s) for s in SCHEDULE]:raise RuntimeError('Bundle metadata mismatch')
                        states=data['full_states']
                    if states.shape!=(len(SCHEDULE),DIM) or not np.all(np.isfinite(states)):raise RuntimeError('Partial bundle')
                else:
                    states=propagate(np,f,start*384,a,coeff)
                    with bundle.open('xb') as out:np.savez(out,full_states=states,input_sha256_json=json.dumps(custody,sort_keys=True),g=g,start=start,schedule_json=json.dumps(SCHEDULE));out.flush();os.fsync(out.fileno())
                    event('bundle_saved',key=bundlekey,sha256=sha(bundle))
                digest=sha(bundle)
                for j,(timekey,tau,early) in enumerate(SCHEDULE):
                    key=bundlekey+'_'+timekey;rp=CP/(key+'.json');psi=states[j];receipt['next_unfinished']=dict(Hamiltonian=label,state=key)
                    if rp.exists():
                        if not authenticated(rp,'state_complete',key):raise RuntimeError('State receipt mismatch')
                        row=json.loads(rp.read_text())
                        if row['input_sha256']!=custody or row['bundle_sha256']!=digest or row['bundle_index']!=j or row['time_key']!=timekey:raise RuntimeError('State input/bundle changed')
                    else:
                        row=observe(np,f,start,tau,early,psi);row.update(input_sha256=custody,bundle_path=str(bundle),bundle_sha256=digest,bundle_index=j,time_key=timekey)
                        exclusive(rp,row);event('state_complete',key=key,sha256=sha(rp),failed=row['failed_count'])
                    h['states'].append(row)
                for j in range(len(TINY)):
                    plus=states[len(TIMES)+2*j];minus=states[len(TIMES)+2*j+1]
                    check(h['checks'],'time_reversal_'+str(start)+'_'+str(j),np.max(np.abs(minus-plus.conj()))<=OBS_TOL)
                independent=taylor(np,f,start*384);error=float(np.max(np.abs(independent-states[1])))
                check(h['checks'],'independent_Taylor_tau1_'+str(start),error<=OBS_TOL,dict(maximum=error))
                event('preparation_complete',key=bundlekey,states=len(SCHEDULE),elapsed_seconds=time.perf_counter()-hbegan)
                print(json.dumps(dict(event='preparation_complete',g=g,start=start,states=len(SCHEDULE),seconds=time.perf_counter()-hbegan)),flush=True)
                del states,independent;gc.collect()
            elapsed=time.perf_counter()-hbegan;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            check(h['checks'],'Hamiltonian_under_180seconds',elapsed<MAX_SECONDS,dict(seconds=elapsed,limit=MAX_SECONDS))
            check(h['checks'],'peak_under_512MiB',peak<MAX_RSS,dict(peak_bytes=peak,limit_bytes=MAX_RSS))
            h.update(elapsed_seconds=elapsed,peak_RSS_bytes=peak);h['failed_count']=sum(not c['passed'] for c in h['checks'])+sum(row['failed_count'] for row in h['states'])
            exclusive(hp,h);event('Hamiltonian_complete',key=label,sha256=sha(hp),failed=h['failed_count']);receipt['Hamiltonians'].append(h)
            print(json.dumps(dict(event='Hamiltonian_complete',g=g,states=len(h['states']),failed=h['failed_count'],seconds=elapsed)),flush=True)
            del f,coeff;gc.collect()
            if h['failed_count']:break
        final=anchors();check(receipt['checks'],'input_bytes_unchanged',final==custody)
        check(receipt['checks'],'two_Hamiltonians_44_states',len(receipt['Hamiltonians'])==2 and sum(len(h['states']) for h in receipt['Hamiltonians'])==44)
        failed=any(not c['passed'] for c in receipt['checks']) or any(h['failed_count'] for h in receipt['Hamiltonians'])
        receipt['status']='FAILED' if failed else 'QUALIFIED_ARITHMETIC';receipt['next_unfinished']=None if len(receipt['Hamiltonians'])==2 else dict(Hamiltonian='g1',state='controls')
    except Exception:
        receipt['status']='ERROR';receipt['exception']=traceback.format_exc();event('error',exception=receipt['exception'],next_unfinished=receipt.get('next_unfinished'))
    receipt['runtime_seconds']=time.perf_counter()-began;receipt['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;event('run_complete',status=receipt['status']);finish(receipt)
    return 0 if receipt['status']=='QUALIFIED_ARITHMETIC' else 1
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true');args=p.parse_args()
    if args.resume and not args.execute:p.error('--resume requires --execute and separate approval')
    if args.execute:return execute(args.resume)
    print(json.dumps(dict(mode='describe_only',inputs=inputs(),input_sha256=anchors()),indent=2));return 0
if __name__=='__main__':sys.exit(main())
